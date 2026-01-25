import re
import os
import ast
import pandas as pd
import argparse
import numpy as np
from tqdm import trange
import warnings
# # 设置环境变量抑制警告
# os.environ['PYTHONWARNINGS'] = 'ignore'
# # 抑制所有警告
# warnings.simplefilter('ignore')
# warnings.filterwarnings('ignore')
import statsmodels.formula.api as smf
# # 在导入 statsmodels 后再次设置，确保覆盖其内部警告
# warnings.simplefilter('ignore')
# warnings.filterwarnings('ignore')

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
        # 对于该配置：我们会有 30 道题；对于多轮，只看第二轮的结果

        # 单轮：通过 "第X题使用扰动类型 Y"
        # 多轮：需要追踪 "multi-turn 第i组 第一轮 / 第二轮"
        # 策略：
        #   - 遇到配置行 -> current_config = {...}, mode_multi = (mul == 1) 或按日志内容判断
        #   - 对单轮：
        #       看到 "第i题使用扰动类型 y" -> current_question_id, current_augmentation
        #       之后找到第一条判对行 -> 记一条记录
        #   - 对多轮：
        #       先会出现 "第i题使用扰动类型 y"
        #       然后有 "multi-turn 第i组 第一轮" (忽略对错)
        #       然后 "multi-turn 第i组 第二轮" 之后的第一条判对行 -> 记一条记录

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
                print(f"current_config={current_config}")
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
                        print(f"解析单轮结果....question_id={qid}, augmentation={aug_type}, accuracy={correct}, LLMs={label}")
                        # 这里不展开 30 个 augmentation 字段，避免高维稀疏问题
                        if "augmentations" in row:
                            row.pop("augmentations")
                        records.append(row)
                    # 更新 i
                    i = j + 1 if correct is not None else j
                    continue

            # ---------------- 多轮逻辑 ----------------
            else:
                question_start = question_id_and_aug_type.search(line)
                if question_start:
                    # 接下来会有 multi-turn 第qid组 第一轮
                    print("发现第一轮第一行")
                    j = i + 1
                    correct = None
                    aug_type_second = None
                    found_first_round = False
                    found_first_result = False
                    found_second_q_aug = False
                    found_second_round = False
                    
                    while j < total_lines:
                        l2 = lines[j]
                        # 新配置行，说明本题还没等到结果就进了下一个配置
                        if pattern_config.search(l2):
                            break

                        # 检测第一轮开始（连续两行中的第二行）
                        if pattern_multi_first_round.search(l2):
                            print("发现第一轮第二行")
                            found_first_round = True
                            j += 1
                            continue

                        # 找到并跳过第一轮的结果
                        if found_first_round and not found_first_result:
                            flag, corr = parse_correct_from_line(l2)
                            if flag:
                                found_first_result = True
                                j += 1
                                continue

                        # 检测第二轮的题号和扰动类型（第Y题使用扰动类型 Z）
                        if found_first_result and not found_second_q_aug:
                            second_question_start = question_id_and_aug_type.search(l2)
                            if second_question_start:
                                print("发现第二轮第一行")
                                qid = int(second_question_start.group(1))
                                aug_type_second = int(second_question_start.group(2))
                                found_second_q_aug = True
                                j += 1
                                continue

                        # 检测第二轮开始（连续两行中的第二行）
                        if found_second_q_aug and pattern_multi_second_round.search(l2):
                            print("发现第二轮第二行")
                            found_second_round = True
                            j += 1
                            continue

                        # 在第二轮开始后，查找第二轮的结果
                        if found_second_round:
                            flag, corr = parse_correct_from_line(l2)
                            if flag:
                                correct = corr
                                break
                        
                        j += 1

                    # 只统计第二轮的结果
                    if correct is not None and aug_type_second is not None:
                        print(f"解析第二轮结果....question_id={qid}, augmentation={aug_type_second}, accuracy={correct}, LLMs={label}")
                        row = dict(current_config)
                        row["question_id"] = qid  # 使用第二轮的题号
                        row["augmentation"] = aug_type_second  # 使用第二轮的扰动类型
                        row["accuracy"] = correct
                        row["LLMs"] = label
                        if "augmentations" in row:
                            row.pop("augmentations")
                        records.append(row)
                    i = j + 1 if correct is not None else j
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
def run_mixed_for_label_question(folder, label, outdir="mixed_ames_result"):
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
    # 这里用二值 accuracy，但是 MixedLM 默认是高斯；如果你想做严格的二项 GLMM，
    # 目前 Python 生态支持没那么好，建议用 R glmer。这里先用 Linear Mixed Model 近似。
    model = smf.mixedlm(formula, data=df, groups=df["question_id"])
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        result = model.fit(reml=False, method="lbfgs")

    os.makedirs(outdir, exist_ok=True)
    out_path = os.path.join(outdir, f"{label}_mixed_question.txt")
    with open(out_path, "w", encoding="utf-8") as fout:
        fout.write("==== Mixed Effects Model (Random Intercept: question_id) ====\n")
        fout.write(f"LLM: {label}\n\n")
        fout.write(format_mixed_summary_sorted(result))
    print(f"[INFO] {label} 混合模型(随机题目)结果已保存到 {out_path}")


def run_mixed_for_label_augmentation(folder, label, outdir="mixed_ames_result"):
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
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        result = model.fit(reml=False, method="lbfgs")

    os.makedirs(outdir, exist_ok=True)
    out_path = os.path.join(outdir, f"{label}_mixed_augmentation.txt")
    with open(out_path, "w", encoding="utf-8") as fout:
        fout.write("==== Mixed Effects Model (Random Intercept: augmentation) ====\n")
        fout.write(f"LLM: {label}\n\n")
        fout.write(format_mixed_summary_sorted(result))
    print(f"[INFO] {label} 混合模型(随机扰动)结果已保存到 {out_path}")


# ===================== 多 LLM 一起：增加固定效应 LLMs =====================
def run_mixed_vs_llms_question(folder, outdir="mixed_ames_result"):
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
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        result = model.fit(reml=False, method="lbfgs")

    os.makedirs(outdir, exist_ok=True)
    out_path = os.path.join(outdir, "mixed_vs_llms_question.txt")
    with open(out_path, "w", encoding="utf-8") as fout:
        fout.write("==== Mixed Effects Model (Random Intercept: question_id, fixed LLMs) ====\n\n")
        fout.write(format_mixed_summary_sorted(result))
    print(f"[INFO] Mixed LLMs (question random) 结果已保存到 {out_path}")


def run_mixed_vs_llms_augmentation(folder, outdir="mixed_ames_result"):
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
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
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
    args = parser.parse_args()

    outdir = "mixed_ames_result"
    os.makedirs(outdir, exist_ok=True)

    label_list = ["deepseekv3", "kimiv1", "doubao", "qwen25", "qwen",
                  "mistralM", "mistralL", "gpt35", "gpt41"]

    for label in label_list:
        run_mixed_for_label_question(args.folder, label, outdir=outdir)
        run_mixed_for_label_augmentation(args.folder, label, outdir=outdir)

    run_mixed_vs_llms_question(args.folder, outdir=outdir)
    run_mixed_vs_llms_augmentation(args.folder, outdir=outdir)