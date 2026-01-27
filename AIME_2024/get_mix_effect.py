import re
import os
import ast
import pandas as pd
import argparse
import numpy as np
from tqdm import trange
import warnings
from statsmodels.regression.mixed_linear_model import MixedLM
import statsmodels.api as sm
# 全局变量：控制是否显示警告（默认False，保持向后兼容，即默认抑制警告）
SHOW_WARNINGS = False

def setup_warnings(show: bool):
    """
    设置警告处理机制
    - show=True: 不处理警告，让警告正常显示
    - show=False: 抑制所有警告
    """
    global SHOW_WARNINGS
    SHOW_WARNINGS = show
    if not show:
        # 设置环境变量抑制警告
        os.environ['PYTHONWARNINGS'] = 'ignore'
        # 抑制所有警告
        warnings.simplefilter('ignore')
        warnings.filterwarnings('ignore')
    else:
        # 恢复默认警告行为，让警告正常显示
        if 'PYTHONWARNINGS' in os.environ:
            del os.environ['PYTHONWARNINGS']
        warnings.resetwarnings()

# 初始化时默认抑制警告（保持向后兼容）
setup_warnings(False)

import statsmodels.formula.api as smf

# 在导入 statsmodels 后再次设置，确保覆盖其内部警告
if not SHOW_WARNINGS:
    warnings.simplefilter('ignore')
    warnings.filterwarnings('ignore')

# ===================== 日志解析正则 =====================

# 配置行
pattern_config = re.compile(
    r"配置 key=(\d+), 配置="
)

def extract_balanced_dict(s, start_pos):
    """
    从字符串 s 的 start_pos 位置开始，提取一个平衡的字典字符串（包括嵌套的 {}）
    返回 (dict_str, end_pos)，其中 dict_str 是完整的字典字符串，end_pos 是结束位置
    """
    if start_pos >= len(s) or s[start_pos] != '{':
        return None, start_pos
    
    brace_count = 0
    i = start_pos
    in_string = False
    string_char = None
    escape_next = False
    
    while i < len(s):
        char = s[i]
        
        if escape_next:
            escape_next = False
            i += 1
            continue
        
        if char == '\\':
            escape_next = True
            i += 1
            continue
        
        if not in_string:
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    return s[start_pos:i+1], i + 1
            elif char in ("'", '"'):
                in_string = True
                string_char = char
        else:
            if char == string_char:
                in_string = False
                string_char = None
        
        i += 1
    
    return None, start_pos

# 单轮：题号 + 扰动类型
question_id_and_aug_type = re.compile(
    r"第(\d+)题使用扰动类型\s*(\d+)"
)

# 多轮：题号 + 扰动类型
pattern_multi_first_round = re.compile(
    r"multi-turn\s*第(\d+)组\s*第一轮"
)
pattern_multi_second_round = re.compile(
    r"multi-turn\s*第(\d+)组\s*第二轮"
)

# 判对关键词（3类）
pattern_judge_doubao = re.compile(
    r"LLM-JUDGE-DOUBAO 回复：(?P<ans>可以|不可以)"
)

pattern_str_cmp = re.compile(
    r"比较字符串结果，答案(?P<ans>正确|错误)"
)

pattern_int_cmp = re.compile(
    r"比较整数结果.*?，答案(?P<ans>正确|错误)"
)

# 错误模式：invalid literal for int() 错误
pattern_error_int_parse = re.compile(
    r"ERROR.*?出错:.*?invalid literal for int\(\) with base 10:"
)

def parse_correct_from_line(line: str):
    """
    返回 (is_decision, correct)
    - is_decision: 这一行是否是“给出最终对错判断”的行
    - correct: 若 is_decision=True，则为 1/0；否则为 None
    """
    m1 = pattern_judge_doubao.search(line)
    if m1:
        return True, 1 if m1.group("ans") == "可以" else 0

    m2 = pattern_str_cmp.search(line)
    if m2:
        return True, 1 if m2.group("ans") == "正确" else 0

    m3 = pattern_int_cmp.search(line)
    if m3:
        return True, 1 if m3.group("ans") == "正确" else 0

    m4 = pattern_error_int_parse.search(line)
    if m4:
        return True, 0  # 出现 int() 解析错误，判定为错误

    return False, None

# ===================== 因子名称映射 =====================
factor_name_map = {
    "language": "Language",
    "question_type": "Question Format",
    "cot": "COT",
    "max_tokens": "max_tokens",
    "Temperature": "temperature",
    "presence_penalty": "presence_penalty",
    "top_p": "top_p",
    "question_tran": "Question Paraphrase",
    "few": "Shot",
    "mul": "Multi Turn",
    "LLMs": "LLMs",
    "question_id": "Question",
    "augmentation": "Augmentation"
}

def pretty_factor_name(name: str) -> str:
    return factor_name_map.get(name, name)


def format_mixed_summary_sorted(result) -> str:
    """
    生成与 result.summary().as_text() 格式相同的字符串，但固定效应按 p 值升序排列
    （最显著的因子在前）。Intercept 保持首位，Group Var 等方差参数保持末尾。
    """
    raw = result.summary().as_text()
    lines = raw.split("\n")

    # 定位 params 表头行（含 "Coef." 与 "Std.Err."）
    start = None
    for i, L in enumerate(lines):
        if "Coef." in L and "Std.Err." in L:
            start = i
            break
    if start is None:
        return raw

    model_block = "\n".join(lines[:start])
    header = lines[start]
    sep = lines[start + 1] if start + 1 < len(lines) and lines[start + 1].strip().startswith("-") else "----------------------------------------------------------------------"

    # 从原始输出中提取每行的格式（保持原始格式）
    # 先建立参数名到行的映射
    param_lines = {}
    all_param_names = list(result.params.index)
    
    for i in range(start + 2, len(lines)):
        line = lines[i]
        if line.strip().startswith("-") or not line.strip():
            break
        # 对每个参数名，检查行是否以它开头（去除前导空格后）
        stripped = line.strip()
        for param_name in all_param_names:
            if stripped.startswith(param_name):
                # 确保参数名后面是空格、数字或负号（避免部分匹配）
                next_pos = len(param_name)
                if next_pos >= len(stripped) or stripped[next_pos] in [' ', '\t', '-'] or stripped[next_pos].isdigit():
                    param_lines[param_name] = line
                    break

    names = list(result.params.index)
    intercept = [n for n in names if n == "Intercept"]
    var = [n for n in names if "Var" in n]
    fixed = [n for n in names if n not in intercept and n not in var]
    # 排序：先按 p 值升序（p 越小越显著），p 值相同时按 coef 绝对值降序（影响越大越靠前）
    # 对于 p 值非常接近的情况（差异 < 1e-40），视为相同，按 coef 绝对值排序
    p_threshold = 1e-40
    def sort_key(n):
        p = result.pvalues[n]
        # 将极小的 p 值（< 1e-40）都视为 0，这样它们会按 coef 绝对值排序
        p_normalized = 0.0 if p < p_threshold else p
        return (p_normalized, -abs(result.params[n]))
    fixed_sorted = sorted(fixed, key=sort_key)
    order = intercept + fixed_sorted + var

    # 使用原始格式的行，按新顺序排列
    rows = []
    for n in order:
        if n in param_lines:
            rows.append(param_lines[n])
        else:
            # 如果原始输出中没有（不应该发生），使用格式化字符串
            c = result.params[n]
            se = result.bse[n]
            z = result.tvalues[n]
            p = result.pvalues[n]
            ci_df = result.conf_int()
            if n in ci_df.index:
                low, hi = ci_df.loc[n, 0], ci_df.loc[n, 1]
                ci_str = f"  {low:6.3f} {hi:6.3f}"
            else:
                ci_str = " " * 16
            rows.append(f"{n:28}{c:8.3f}    {se:8.3f}    {z:8.3f} {p:8.3f}  {ci_str}")

    table = "\n".join([header, sep] + rows + [sep])
    return model_block + "\n" + table + "\n"


# ===================== 日志解析 =====================
def parse_log_files_mixed(folder: str, label: str) -> pd.DataFrame:
    """
    解析一个 LLM 的全部日志：
    - 每行数据是一道题
    - 列包括:
      language, cot, few, mul, question_type, question_tran,
      Temperature, max_tokens, top_p, presence_penalty,
      augmentation, question_id, accuracy(0/1), LLMs
    """
    records = []

    for fname in os.listdir(folder):
        if not fname.startswith(f"sample_test_{label}_"):
            continue
        fpath = os.path.join(folder, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        print(f"fname={fname}")
        current_config = None   # dict: 实验配置
        mode_multi = False      # 是否多轮
        
        i = 0
        total_lines = len(lines)
        while i < total_lines:
            line = lines[i]

            # 1) 解析配置行
            m_cfg = pattern_config.search(line)
            if m_cfg:
                key = int(m_cfg.group(1))
                # 找到配置字典的起始位置（在 "配置=" 之后）
                config_start = m_cfg.end()
                config_str, end_pos = extract_balanced_dict(line, config_start)
                current_config = ast.literal_eval(config_str)
                # print(f"current_config={current_config}")
                # 决定是否多轮（你可根据 config_dict['mul'] == 1 来判断）
                if current_config is not None and "mul" in current_config:
                    mode_multi = bool(current_config["mul"])
                else:
                    mode_multi = False
                i += 1
                continue

            # 若当前没有有效配置，跳过
            if current_config is None:
                i += 1
                continue

            # ---------------- 单轮逻辑 ----------------
            if not mode_multi:
                question_start = question_id_and_aug_type.search(line)
                if question_start:
                    qid = int(question_start.group(1))
                    aug_type = int(question_start.group(2))
                    # 之后的若干行，直到遇到第一个“判对关键词”
                    j = i + 1
                    correct = None
                    while j < total_lines:
                        flag, corr = parse_correct_from_line(lines[j])
                        if flag:
                            correct = corr
                            break
                        # 如果遇到新配置行，也说明这题没有判对信息（防御性）
                        if pattern_config.search(lines[j]):
                            break
                        j += 1

                    if correct is not None:
                        row = dict(current_config)  # 复制配置
                        row["question_id"] = qid
                        row["augmentation"] = aug_type
                        row["accuracy"] = correct
                        row["LLMs"] = label
                        # print(f"解析单轮结果....question_id={qid}, augmentation={aug_type}, accuracy={correct}, LLMs={label}")
                        # 这里不展开 30 个 augmentation 字段，避免高维稀疏问题
                        if "augmentations" in row:
                            row.pop("augmentations")
                        records.append(row)
                    # 更新 i
                    i = j + 1 if correct is not None else j
                    continue

            # ---------------- 多轮逻辑 ----------------
            else:
                # 在从1到30的循环中，直接找第二轮的相关信息
                start_pos = i  # 记录多轮逻辑的起始位置
                for group_id in range(1, 31):  # i从1到30
                    target_question_id = group_id + 1  # 第i+1题
                    if target_question_id > 30:
                        target_question_id = 1
                    j = start_pos
                    found_question_aug = False
                    found_second_round = False
                    correct = None
                    aug_type = None
                    qid = None
                    
                    # 查找"第i+1题使用扰动类型x"
                    while j < total_lines:
                        l2 = lines[j]
                        # 新配置行，说明还没找到就进了下一个配置
                        if pattern_config.search(l2):
                            break
                        
                        # 查找"第target_question_id题使用扰动类型x"
                        question_start = question_id_and_aug_type.search(l2)
                        if question_start:
                            found_qid = int(question_start.group(1))
                            if found_qid == target_question_id:
                                aug_type = int(question_start.group(2))
                                qid = found_qid
                                found_question_aug = True
                                # 检查下一行是否是"multi-turn 第i组 第二轮"
                                if j + 1 < total_lines:
                                    next_line = lines[j + 1]
                                    second_round_match = pattern_multi_second_round.search(next_line)
                                    if second_round_match:
                                        found_group_id = int(second_round_match.group(1))
                                        if found_group_id == group_id:
                                            found_second_round = True
                                            j = j + 2  # 跳过题号行和multi-turn行
                                            break
                                # 如果下一行不是第二轮标记，继续查找
                                j += 1
                                continue
                        
                        j += 1
                    
                    if not found_question_aug or not found_second_round:
                        continue  # 没找到对应的题号或第二轮标记，继续下一个group_id
                    
                    # 在第二轮开始后，查找第二轮的结果
                    while j < total_lines:
                        l2 = lines[j]
                        # 新配置行，说明还没找到结果就进了下一个配置
                        if pattern_config.search(l2):
                            break
                        
                        flag, corr = parse_correct_from_line(l2)
                        if flag:
                            correct = corr
                            break
                        
                        j += 1
                    
                    # 记录结果
                    if correct is not None and aug_type is not None and qid is not None:
                        # print(f"解析第二轮结果....question_id={qid}, augmentation={aug_type}, accuracy={correct}, LLMs={label}, group_id={group_id}")
                        row = dict(current_config)
                        row["question_id"] = qid
                        row["augmentation"] = aug_type
                        row["accuracy"] = correct
                        row["LLMs"] = label
                        if "augmentations" in row:
                            row.pop("augmentations")
                        records.append(row)
                
                # 多轮逻辑处理完后，需要更新i的位置
                # 找到下一个配置行的位置，或者文件末尾
                i = start_pos
                while i < total_lines:
                    if pattern_config.search(lines[i]):
                        break
                    i += 1
                continue

            i += 1

    df = pd.DataFrame(records)
    if len(df) == 0:
        print(f"[WARNING] Label={label} 没有解析到任何题目记录")
        return df

    # 类型转换
    # 题号 & augmentation -> category/int
    df["question_id"] = df["question_id"].astype(int).astype(str)  # 作为分类
    df["augmentation"] = df["augmentation"].astype(int).astype(str)
    # 其他离散因子也转成分类，方便 MixedLM / 其它建模工具
    for col in ["language", "question_type", "question_tran", "few", "cot", "mul"]:
        if col in df.columns:
            df[col] = df[col].astype(str)
    return df

# ===================== 混合效应模型（statsmodels 版：分两层） =====================
def run_mixed_for_label_question(folder, label, outdir="mixed_ames_result", show_warnings=False):
    """
    模型1：随机截距在 question_id 上：
      accuracy ~ 10 个固定因子 + (1 | question_id)
    """
    df = parse_log_files_mixed(folder, label)
    if len(df) == 0:
        return

    # 构造公式：固定效应与原 ANOVA 一致
    fixed_effects = [
        "C(language)", "C(question_type)", "C(question_tran)",
        "C(few)", "C(cot)", "C(mul)",
        "C(Temperature)", "C(max_tokens)", "C(top_p)", "C(presence_penalty)"
    ]
    formula = "accuracy ~ " + " + ".join(fixed_effects)

    # MixedLM: groups=question_id
    # 这里用二值 accuracy，但是 MixedLM 默认是高斯；如果要做严格的二项 GLMM，
    # 目前 Python 生态支持没那么好，建议用 R glmer。这里先用 Linear Mixed Model 近似。
    model = smf.mixedlm(formula, data=df, groups=df["question_id"])
    if not show_warnings:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            result = model.fit(reml=False, method="lbfgs")
    else:
        result = model.fit(reml=False, method="lbfgs")

    os.makedirs(outdir, exist_ok=True)
    out_path = os.path.join(outdir, f"{label}_mixed_question.txt")
    with open(out_path, "w", encoding="utf-8") as fout:
        fout.write("==== Mixed Effects Model (Random Intercept: question_id) ====\n")
        fout.write(f"LLM: {label}\n\n")
        fout.write(format_mixed_summary_sorted(result))
    print(f"[INFO] {label} 混合模型(随机题目)结果已保存到 {out_path}")


def run_mixed_for_label_augmentation(folder, label, outdir="mixed_ames_result", show_warnings=False):
    """
    模型2：随机截距在 augmentation 上：
      accuracy ~ 10 个固定因子 + (1 | augmentation)
    """
    df = parse_log_files_mixed(folder, label)
    if len(df) == 0:
        return

    fixed_effects = [
        "C(language)", "C(question_type)", "C(question_tran)",
        "C(few)", "C(cot)", "C(mul)",
        "C(Temperature)", "C(max_tokens)", "C(top_p)", "C(presence_penalty)"
    ]
    formula = "accuracy ~ " + " + ".join(fixed_effects)

    model = smf.mixedlm(formula, data=df, groups=df["augmentation"])
    if not show_warnings:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            result = model.fit(reml=False, method="lbfgs")
    else:
        result = model.fit(reml=False, method="lbfgs")

    os.makedirs(outdir, exist_ok=True)
    out_path = os.path.join(outdir, f"{label}_mixed_augmentation.txt")
    with open(out_path, "w", encoding="utf-8") as fout:
        fout.write("==== Mixed Effects Model (Random Intercept: augmentation) ====\n")
        fout.write(f"LLM: {label}\n\n")
        fout.write(format_mixed_summary_sorted(result))
    print(f"[INFO] {label} 混合模型(随机扰动)结果已保存到 {out_path}")


def run_mixed_for_label_question_and_aug(folder, label, outdir="mixed_ames_result", show_warnings=False):
    """
    单个 LLM：
      近似实现：accuracy ~ 10 固定因子 + (1 | question_id) + (1 | augmentation)

    实现方式：
      - 使用 statsmodels.MixedLM 的通用接口
      - groups 取 question_id
      - 在 exog_re 中加入两列：
          * 一列常数列 -> question 随机截距
          * 一列 augmentation 的哑变量（或缩放后的数值）-> 近似表示 augmentation 层的随机效应

    注意：这不是完整的交叉随机效应实现，而是一个实用的近似。
    """

    df = parse_log_files_mixed(folder, label)
    if len(df) == 0:
        print(f"[WARNING] Label={label} 在双随机 MixedLM 中没有数据，跳过")
        return

    # 固定效应设计：与你原来的 MixedLM 保持一致
    fixed_effects = [
        "C(language)", "C(question_type)", "C(question_tran)",
        "C(few)", "C(cot)", "C(mul)",
        "C(Temperature)", "C(max_tokens)", "C(top_p)", "C(presence_penalty)"
    ]
    formula = "accuracy ~ " + " + ".join(fixed_effects)

    # 用 patsy 构造固定效应设计矩阵
    import patsy
    y, X = patsy.dmatrices(formula, data=df, return_type="dataframe")

    # groups：以题目为主分组
    groups = df["question_id"].astype("category")

    # 构造随机效应设计矩阵 exog_re：
    #   col0: 截距列，对应 (1 | question_id)
    #   col1..k: augmentation 的哑变量列，近似表示 (1 | augmentation)
    #
    # 简化做法：只加一列“augmentation_编码”为随机斜率（比全哑变量节省参数，收敛更稳）
    # 如果你愿意接受参数多一些，可以用 one-hot。
    #
    # 这里只演示“单列数值编码”的版本：
    aug_cat = df["augmentation"].astype("category")
    aug_codes = aug_cat.cat.codes.astype(float)  # 0,1,2,... 数值编码

    Z = pd.DataFrame({
        "RE_Intercept": 1.0,            # question 随机截距
        "RE_AugCode": aug_codes         # augmentation 编码的随机斜率
    })

    # MixedLM 通用接口
    model = MixedLM(endog=y["accuracy"], exog=X, groups=groups, exog_re=Z)

    if not show_warnings:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = model.fit(reml=False, method="lbfgs")
    else:
        result = model.fit(reml=False, method="lbfgs")

    # 输出结果：固定效应 + 随机效应协方差成分
    os.makedirs(outdir, exist_ok=True)
    out_path = os.path.join(outdir, f"{label}_mixed_question_plus_aug.txt")
    with open(out_path, "w", encoding="utf-8") as fout:
        fout.write("==== MixedLM 近似双随机效应模型 ====\n")
        fout.write(f"LLM: {label}\n")
        fout.write(f"Formula (fixed): {formula}\n")
        fout.write("Random structure: groups=question_id, exog_re=[Intercept, AugCode]\n\n")

        # 固定效应结果
        fout.write("---- Fixed Effects (sorted by p-value) ----\n")
        fe = pd.DataFrame({
            "Coef": result.params,
            "SE": result.bse,
            "z": result.tvalues,
            "p": result.pvalues,
        })
        # 只保留固定效应行（忽略随机效应协方差参数）
        fe = fe.loc[X.columns]
        fe_sorted = fe.sort_values(by="p")
        fout.write(fe_sorted.to_string())
        fout.write("\n\n")

        # 随机效应协方差矩阵
        fout.write("---- Random Effects Covariance (for [Intercept, AugCode]) ----\n")
        cov_re = result.cov_re  # 2x2 矩阵：截距方差、协方差、AugCode 方差
        fout.write(cov_re.to_string())
        fout.write("\n\n")

        fout.write("---- Residual variance ----\n")
        fout.write(str(result.scale))
        fout.write("\n")

    print(f"[INFO] {label} 的近似双随机 MixedLM 结果已保存到 {out_path}")

# ===================== 使用 Bambi 的双随机效应模型（单 LLM） =====================
def run_bambi_mixed_for_label_question_and_aug(
    folder,
    label,
    outdir="mixed_ames_result",
    draws=2000,
    chains=4,
    target_accept=0.95,
):
    """
    使用 Bambi + PyMC 对单个 LLM 拟合标准的双随机效应模型（Logistic GLMM）：

        accuracy ~ 10 个固定因子
                    + (1 | question_id)
                    + (1 | augmentation)

    固定因子：
        language, question_type, question_tran,
        few, cot, mul,
        Temperature, max_tokens, top_p, presence_penalty

    随机效应：
        - question_id 随机截距
        - augmentation 随机截距

    结果写入 outdir / f"{label}_bambi_mixed_question_aug.txt"
    """

    try:
        import bambi as bmb
        import pymc as pm
        import arviz as az
    except ImportError as e:
        print(
            f"[WARNING] 运行 Bambi 模型失败：{e}. "
            "请先安装依赖：pip install bambi pymc arviz"
        )
        return

    df = parse_log_files_mixed(folder, label)
    if len(df) == 0:
        print(f"[WARNING] Label={label} 在 Bambi 双随机模型中没有数据，跳过")
        return

    # 将离散变量显式设为 category（有助于 Bambi 正确建模）
    cat_cols = [
        "language", "question_type", "question_tran",
        "few", "cot", "mul",
        "Temperature", "max_tokens", "top_p", "presence_penalty",
        "question_id", "augmentation",
    ]
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype("category")

    # accuracy 应为 0/1
    # 若存在 True/False 或字符串，强制转成 int
    df["accuracy"] = df["accuracy"].astype(int)

    # 构建 Bambi 模型公式
    # 这里 deliberately 不加 C()，因为我们已将变量设为 category，Bambi 会自动按分类变量处理。
    formula = (
        "accuracy ~ "
        "language + question_type + question_tran + "
        "few + cot + mul + "
        "Temperature + max_tokens + top_p + presence_penalty + "
        "(1|question_id) + (1|augmentation)"
    )

    print(f"[INFO] 使用 Bambi 拟合 {label} 的双随机 Logistic 模型...")
    print(f"[INFO] Formula: {formula}")

    # accuracy是二分类，因此使用伯努利分布
    model = bmb.Model(formula, data=df, family="bernoulli")

    # 拟合模型（MCMC，马尔科夫链蒙特卡洛方法）
    idata = model.fit(draws=draws, chains=chains, target_accept=target_accept)

    # 汇总结果
    # 获取固定效应变量名：从 common_terms 获取，并添加 Intercept
    # 注意：Bambi 中固定效应存储在 components['p'].common_terms 中
    fixed_effect_vars = []
    if 'p' in model.components:
        comp = model.components['p']
        # common_terms 包含除 Intercept 外的固定效应
        fixed_effect_vars = list(comp.common_terms.keys())
        # 如果有 intercept_term，添加 Intercept
        if comp.intercept_term is not None:
            fixed_effect_vars = ['Intercept'] + fixed_effect_vars
    
    fe_summary = az.summary(
        idata,
        var_names=fixed_effect_vars,
        kind="stats",
    )
    
    # 对固定效应按影响大小排序（按 mean 的绝对值降序，但 Intercept 保持在最前面）
    if 'Intercept' in fe_summary.index:
        intercept_row = fe_summary.loc[['Intercept']]
        other_rows = fe_summary.drop('Intercept')
        # 按 mean 的绝对值降序排序
        other_rows = other_rows.reindex(
            other_rows['mean'].abs().sort_values(ascending=False).index
        )
        fe_summary = pd.concat([intercept_row, other_rows])
    else:
        # 如果没有 Intercept，直接按 mean 的绝对值降序排序
        fe_summary = fe_summary.reindex(
            fe_summary['mean'].abs().sort_values(ascending=False).index
        )

    # 随机效应标准差（group-level sd）
    # Bambi 对 group-level sd 的命名规则为 1|group_name_sigma
    re_vars = []
    for name in idata.posterior.data_vars:
        # 查找以 "1|" 开头且以 "_sigma" 结尾的变量（随机效应的标准差）
        if name.startswith("1|") and name.endswith("_sigma"):
            re_vars.append(name)
    re_summary = az.summary(idata, var_names=re_vars, kind="stats") if re_vars else None
    
    # 对随机效应标准差按影响大小排序（按 mean 降序）
    if re_summary is not None and not re_summary.empty:
        re_summary = re_summary.reindex(
            re_summary['mean'].sort_values(ascending=False).index
        )

    # 写结果到文件
    os.makedirs(outdir, exist_ok=True)
    out_path = os.path.join(outdir, f"{label}_bambi_mixed_question_aug.txt")
    with open(out_path, "w", encoding="utf-8") as fout:
        fout.write("==== Bambi Bayesian Mixed Effects Model ====\n")
        fout.write(f"LLM: {label}\n")
        fout.write("Family: Bernoulli (logit link)\n")
        fout.write(f"Formula: {formula}\n\n")

        fout.write("---- Fixed Effects (posterior summary) ----\n")
        fout.write("(Sorted by |mean|, descending; Intercept first)\n")
        fout.write(fe_summary.to_string())
        fout.write("\n\n")

        if re_summary is not None and not re_summary.empty:
            fout.write("---- Random Effects SD (posterior summary) ----\n")
            fout.write("(Sorted by mean, descending)\n")
            fout.write(re_summary.to_string())
            fout.write("\n\n")
        else:
            fout.write("---- Random Effects SD: 未在 posterior 中找到以 'sd_' 开头的变量 ----\n\n")

        fout.write("---- Sampling diagnostics ----\n")
        # 使用 kind='diagnostics' 获取诊断统计信息，而不是 stat_focus
        diag = az.summary(idata, kind="diagnostics")
        
        # 对诊断信息按可靠性排序：
        # 计算可靠性得分：r_hat 越接近1越好，ess_bulk 越大越好
        if 'r_hat' in diag.columns and 'ess_bulk' in diag.columns:
            diag['reliability_score'] = (
                (1.0 - abs(diag['r_hat'] - 1.0)) * 1000 +  # r_hat 接近1的得分
                diag['ess_bulk'] / 10  # ess_bulk 的得分（除以10避免数值过大）
            )
            diag = diag.sort_values('reliability_score', ascending=False)
            diag = diag.drop('reliability_score', axis=1)  # 删除临时列
            fout.write("(Sorted by reliability: r_hat closest to 1.0, then ess_bulk highest)\n")
        else:
            fout.write("(No sorting applied)\n")
        
        fout.write(diag.to_string())
        fout.write("\n")

    print(f"[INFO] {label} 的 Bambi 双随机混合模型结果已保存到 {out_path}")

# ===================== 使用 R (lme4) 的双随机效应模型（单 LLM） =====================
def run_r_mixed_for_label_question_and_aug(
    folder,
    label,
    outdir="mixed_ames_result_r"
):
    """
    使用 R 的 lme4::glmer 对单个 LLM 拟合标准的双随机效应模型（Logistic GLMM）：

        accuracy ~ 10 个固定因子
                    + (1 | question_id)
                    + (1 | augmentation)

    固定因子：
        language, question_type, question_tran,
        few, cot, mul,
        Temperature, max_tokens, top_p, presence_penalty

    随机效应：
        - question_id 随机截距
        - augmentation 随机截距

    结果写入 outdir / f"{label}_r_mixed_question_aug.txt"
    
    输出排序：
        固定效应按以下规则排序：
        1. Intercept 保持在最前面
        2. 其他因子按 p 值升序排序（最显著的在前）
        3. p 值相同时，按 Estimate 绝对值降序排序（效应最大的在前）
        这样"最重要的发现"（既显著又效应大）会优先显示。
    """
    import subprocess
    import tempfile

    df = parse_log_files_mixed(folder, label)
    if len(df) == 0:
        print(f"[WARNING] Label={label} 在 R 双随机模型中没有数据，跳过")
        return

    # 将离散变量显式设为 category/string（R 需要因子类型）
    cat_cols = [
        "language", "question_type", "question_tran",
        "few", "cot", "mul",
        "Temperature", "max_tokens", "top_p", "presence_penalty",
        "question_id", "augmentation",
    ]
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype(str)

    # accuracy 应为 0/1
    df["accuracy"] = df["accuracy"].astype(int)

    # 构建 R 模型公式
    formula = (
        "accuracy ~ "
        "language + question_type + question_tran + "
        "few + cot + mul + "
        "Temperature + max_tokens + top_p + presence_penalty + "
        "(1|question_id) + (1|augmentation)"
    )

    print(f"[INFO] 使用 R (lme4::glmer) 拟合 {label} 的双随机 Logistic 模型...")
    print(f"[INFO] Formula: {formula}")

    # 使用 R 脚本方式
    # 创建临时 CSV 文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as tmp_csv:
        df.to_csv(tmp_csv.name, index=False)
        csv_path = tmp_csv.name

    # 创建临时 R 脚本
    with tempfile.NamedTemporaryFile(mode='w', suffix='.R', delete=False, encoding='utf-8') as tmp_r:
        r_script = """
# 开始计时
start_time <- Sys.time()
cat("==== R 脚本开始执行 ====\\n")
cat("开始时间:", format(start_time, "%%Y-%%m-%%d %%H:%%M:%%S"), "\\n\\n")

# 加载必要的库
if (!require("lme4", quietly = TRUE)) {{
stop("请先安装 lme4 包: install.packages('lme4')")
}}

# 读取数据
df <- read.csv("%s", stringsAsFactors = TRUE)

# 确保 accuracy 是整数
df$accuracy <- as.integer(df$accuracy)

# 将分类变量转为因子
df$language <- as.factor(df$language)
df$question_type <- as.factor(df$question_type)
df$question_tran <- as.factor(df$question_tran)
df$few <- as.factor(df$few)
df$cot <- as.factor(df$cot)
df$mul <- as.factor(df$mul)
df$Temperature <- as.factor(df$Temperature)
df$max_tokens <- as.factor(df$max_tokens)
df$top_p <- as.factor(df$top_p)
df$presence_penalty <- as.factor(df$presence_penalty)
df$question_id <- as.factor(df$question_id)
df$augmentation <- as.factor(df$augmentation)

# 拟合模型
formula <- accuracy ~ language + question_type + question_tran + 
        few + cot + mul + 
        Temperature + max_tokens + top_p + presence_penalty + 
        (1|question_id) + (1|augmentation)

# gmler用于拟合广义线性混合效应模型，family二项分布，logit链接，适用于二分类因变量
# 使用 bobyqa 优化器，maxfun=1e5，最大函数评估次数为100000
model <- glmer(formula, data = df, family = binomial(link = "logit"),
            control = glmerControl(optimizer = "bobyqa", optCtrl = list(maxfun = 1e5)))

# 输出结果
cat("==== R (lme4::glmer) Mixed Effects Model ====\\n")
cat("LLM: %s\\n")
cat("Family: Binomial (logit link)\\n")
cat("Formula:", as.character(formula), "\\n\\n")

cat("---- Fixed Effects (sorted by p-value, then |Estimate|) ----\\n")
coef_summary <- summary(model)$coefficients

# 将 Intercept 单独处理（保持在最前面）
intercept_row <- coef_summary[rownames(coef_summary) == "(Intercept)", , drop = FALSE]
other_rows <- coef_summary[rownames(coef_summary) != "(Intercept)", , drop = FALSE]

# 对非 Intercept 行进行排序：
# 1. 首先按 p 值升序（p 值越小越显著）
# 2. 然后按 Estimate 绝对值降序（效应越大越靠前）
if (nrow(other_rows) > 0) {{
    # 提取 p 值和 Estimate 用于排序
    p_values <- other_rows[, "Pr(>|z|)"]
    estimates <- other_rows[, "Estimate"]
    
    # 计算排序键：p 值优先（升序），然后按 Estimate 绝对值降序
    sort_key <- order(p_values, -abs(estimates))
    other_rows_sorted <- other_rows[sort_key, , drop = FALSE]
    
    # 重新组合：Intercept 在最前面，然后是排序后的其他行
    coef_summary_sorted <- rbind(intercept_row, other_rows_sorted)
}} else {{
    coef_summary_sorted <- intercept_row
}}

# 格式化输出：对数字列进行格式化
coef_formatted <- coef_summary_sorted
coef_formatted[, "Estimate"] <- formatC(coef_summary_sorted[, "Estimate"], format = "f", digits = 6)
coef_formatted[, "Std. Error"] <- formatC(coef_summary_sorted[, "Std. Error"], format = "f", digits = 6)
coef_formatted[, "z value"] <- formatC(coef_summary_sorted[, "z value"], format = "f", digits = 4)
# p 值格式化：显示 6 位小数
coef_formatted[, "Pr(>|z|)"] <- formatC(coef_summary_sorted[, "Pr(>|z|)"], format = "f", digits = 6)
print(coef_formatted)

cat("\\n\\n---- Random Effects SD ----\\n")
print(VarCorr(model))

cat("\\n\\n---- Model Fit Statistics ----\\n")
cat("AIC:", AIC(model), "\\n")
cat("BIC:", BIC(model), "\\n")

cat("\\n\\n==== Overall Factor Effects (Likelihood Ratio Tests) ====\\n")

factors <- c("language", "question_type", "question_tran",
             "few", "cot", "mul",
             "Temperature", "max_tokens", "top_p", "presence_penalty")

full_formula <- formula
full_logLik  <- as.numeric(logLik(model))

overall_results <- data.frame(
  factor       = character(),
  df           = numeric(),
  Chisq        = numeric(),
  p_value      = numeric(),
  delta_logLik = numeric(),
  stringsAsFactors = FALSE
)

for (fct in factors) {
  # 关键：使用字符 "~ . - factor" 再转成 formula
  update_rhs <- as.formula(paste("~ . -", fct))
  reduced_formula <- update(full_formula, update_rhs)

  cat("Testing factor:", fct, "\n")
  print(reduced_formula)

  model_reduced <- glmer(
    reduced_formula,
    data    = df,
    family  = binomial(link = "logit"),
    control = glmerControl(optimizer = "bobyqa",
                           optCtrl   = list(maxfun = 1e5))
  )
  
  # anova 比较两个嵌套模型，test = "Chisq"：使用卡方检验，检验移除该因子后模型拟合是否显著变差
  lrt <- anova(model_reduced, model, test = "Chisq")

  # p值小，chisq大，说明移除该因子后模型拟合显著变差，因子显著（chisq_val = 2 x delta_logLik）
  df_diff        <- lrt$Df[2] - lrt$Df[1] # 移除该因子后模型的自由度差
  chisq_val      <- lrt$Chisq[2] # 移除该因子后模型的卡方值（衡量模型差异）
  p_val          <- lrt$`Pr(>Chisq)`[2] # p值，衡量因子显著性
  reduced_logLik <- as.numeric(logLik(model_reduced)) # 移除该因子后模型的对数似然值
  delta_logLik   <- full_logLik - reduced_logLik # 对数似然差值
  
  # 将结果添加到 overall_results 数据框中
  overall_results <- rbind(
    overall_results,
    data.frame(
      factor       = fct,
      df           = df_diff,
      Chisq        = chisq_val,
      p_value      = p_val,
      delta_logLik = delta_logLik,
      stringsAsFactors = FALSE
    )
  )
}

overall_results_sorted <- overall_results[
  order(overall_results$p_value, -overall_results$delta_logLik),
]

# 格式化输出：对数字列进行格式化
overall_formatted <- overall_results_sorted
# df 列：如果是 NA 保持 NA，否则格式化为整数
overall_formatted$df <- ifelse(is.na(overall_results_sorted$df),
                                NA_character_,
                                formatC(overall_results_sorted$df, format = "f", digits = 0))
overall_formatted$Chisq <- formatC(overall_results_sorted$Chisq, format = "f", digits = 6)
# p 值格式化：显示 6 位小数
overall_formatted$p_value <- formatC(overall_results_sorted$p_value, format = "f", digits = 6)
overall_formatted$delta_logLik <- formatC(overall_results_sorted$delta_logLik, format = "f", digits = 6)

cat("\\n")
print(overall_formatted, row.names = FALSE)

# 结束计时
end_time <- Sys.time()
elapsed_time <- as.numeric(difftime(end_time, start_time, units = "secs"))
cat("\\n\\n==== R 脚本执行完成 ====\\n")
cat("结束时间:", format(end_time, "%%Y-%%m-%%d %%H:%%M:%%S"), "\\n")
cat("总耗时:", round(elapsed_time, 2), "秒 (", round(elapsed_time / 60, 2), "分钟)\\n")
""" % (csv_path, label)
        tmp_r.write(r_script)
        r_script_path = tmp_r.name

    # 执行 R 脚本
    os.makedirs(outdir, exist_ok=True)
    out_path = os.path.join(outdir, f"{label}_r_mixed_question_aug.txt")
    
    try:
        # 调用 R 执行脚本，将输出重定向到文件
        result = subprocess.run(
            ["Rscript", r_script_path],
            capture_output=True,
            text=True,
            check=True
        )
        
        # 将输出写入结果文件
        with open(out_path, "w", encoding="utf-8") as fout:
            fout.write(result.stdout)
            if result.stderr:
                fout.write("\n---- R Warnings/Errors ----\n")
                fout.write(result.stderr)
        
        print(f"[INFO] {label} 的 R (lme4) 双随机混合模型结果已保存到 {out_path}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] 执行 R 脚本失败：{e}")
        print(f"R 错误输出：{e.stderr}")
    except FileNotFoundError:
        print("[ERROR] 未找到 R 可执行文件。请确保 R 已安装并在 PATH 中。")
    finally:
        # 清理临时文件
        try:
            os.unlink(csv_path)
            os.unlink(r_script_path)
        except:
            pass
    
# ===================== 多 LLM 一起：增加固定效应 LLMs =====================
def run_mixed_for_llms_question(folder, outdir="mixed_ames_result", show_warnings=False):
    """
    所有 LLM 合并：
      accuracy ~ 10 固定因子 + C(LLMs) + (1 | question_id)
    """
    label_list = ["deepseekv3", "kimiv1", "doubao", "qwen25", "qwen",
                  "mistralM", "mistralL", "gpt35", "gpt41"]
    dfs = []
    for label in label_list:
        df_label = parse_log_files_mixed(folder, label)
        if len(df_label) > 0:
            dfs.append(df_label)
    if not dfs:
        print("[WARNING] 没有解析到任何数据")
        return
    df_all = pd.concat(dfs, ignore_index=True)

    fixed_effects = [
        "C(language)", "C(question_type)", "C(question_tran)",
        "C(few)", "C(cot)", "C(mul)",
        "C(Temperature)", "C(max_tokens)", "C(top_p)", "C(presence_penalty)",
        "C(LLMs)"
    ]
    formula = "accuracy ~ " + " + ".join(fixed_effects)

    model = smf.mixedlm(formula, data=df_all, groups=df_all["question_id"])
    if not show_warnings:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            result = model.fit(reml=False, method="lbfgs")
    else:
        result = model.fit(reml=False, method="lbfgs")

    os.makedirs(outdir, exist_ok=True)
    out_path = os.path.join(outdir, "mixed_vs_llms_question.txt")
    with open(out_path, "w", encoding="utf-8") as fout:
        fout.write("==== Mixed Effects Model (Random Intercept: question_id, fixed LLMs) ====\n\n")
        fout.write(format_mixed_summary_sorted(result))
    print(f"[INFO] Mixed LLMs (question random) 结果已保存到 {out_path}")


def run_mixed_for_llms_augmentation(folder, outdir="mixed_ames_result", show_warnings=False):
    """
    所有 LLM 合并：
      accuracy ~ 10 固定因子 + C(LLMs) + (1 | augmentation)
    """
    label_list = ["deepseekv3", "kimiv1", "doubao", "qwen25", "qwen",
                  "mistralM", "mistralL", "gpt35", "gpt41"]
    dfs = []
    for label in label_list:
        df_label = parse_log_files_mixed(folder, label)
        if len(df_label) > 0:
            dfs.append(df_label)
    if not dfs:
        print("[WARNING] 没有解析到任何数据")
        return
    df_all = pd.concat(dfs, ignore_index=True)

    fixed_effects = [
        "C(language)", "C(question_type)", "C(question_tran)",
        "C(few)", "C(cot)", "C(mul)",
        "C(Temperature)", "C(max_tokens)", "C(top_p)", "C(presence_penalty)",
        "C(LLMs)"
    ]
    formula = "accuracy ~ " + " + ".join(fixed_effects)

    model = smf.mixedlm(formula, data=df_all, groups=df_all["augmentation"])
    if not show_warnings:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            result = model.fit(reml=False, method="lbfgs")
    else:
        result = model.fit(reml=False, method="lbfgs")

    os.makedirs(outdir, exist_ok=True)
    out_path = os.path.join(outdir, "mixed_vs_llms_augmentation.txt")
    with open(out_path, "w", encoding="utf-8") as fout:
        fout.write("==== Mixed Effects Model (Random Intercept: augmentation, fixed LLMs) ====\n\n")
        fout.write(format_mixed_summary_sorted(result))
    print(f"[INFO] Mixed LLMs (augmentation random) 结果已保存到 {out_path}")


# ===================== 入口 =====================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mixed-Effects 主程序 (逐 label + LLMs)")
    parser.add_argument("--folder", type=str, default="ames_log_2026", help="日志文件夹路径")
    parser.add_argument("--show_warnings", type=lambda x: (str(x).lower() == 'true'), 
                        default=False, help="是否显示警告 (True: 不处理警告，让警告正常显示; False: 抑制所有警告, 默认False)")
    args = parser.parse_args()

    # 根据参数设置警告处理
    setup_warnings(args.show_warnings)
    # 在导入 statsmodels 后再次设置，确保覆盖其内部警告
    if not args.show_warnings:
        warnings.simplefilter('ignore')
        warnings.filterwarnings('ignore')

    outdir = "mixed_ames_result"
    os.makedirs(outdir, exist_ok=True)

    label_list = ["deepseekv3", "kimiv1", "doubao", "qwen25", "qwen",
                  "mistralM", "mistralL", "gpt35", "gpt41"]

    for label in label_list:
        # run_mixed_for_label_question(args.folder, label, outdir=outdir, show_warnings=args.show_warnings)
        # run_mixed_for_label_augmentation(args.folder, label, outdir=outdir, show_warnings=args.show_warnings)
        # run_mixed_for_label_question_and_aug(args.folder, label, outdir=outdir, show_warnings=args.show_warnings)
        # run_bambi_mixed_for_label_question_and_aug(args.folder, label, outdir=outdir)
        run_r_mixed_for_label_question_and_aug(args.folder, label, outdir=outdir)
        
    # run_mixed_for_llms_question(args.folder, outdir=outdir, show_warnings=args.show_warnings)
    # run_mixed_for_llms_augmentation(args.folder, outdir=outdir, show_warnings=args.show_warnings)