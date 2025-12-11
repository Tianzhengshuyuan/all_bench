import os
import re
import ast
import json
import itertools
from datetime import datetime

CHAR_PER_TOKEN = {
    "yy": 5.3,     # English
    "zw": 1.7,     # 中文
    "ry": 1.0,     # 日语
    "ey": 3.8,     # 俄语
    "fy": 4.3,     # 法语
    "alby": 2.6,   # 阿拉伯语
}
SHORT_RATIO = 0.2

VARIABLES = {
    "language": (["alby","ey","fy","ry","yy","zw"], "yy"),
    "cot": ([0,1], 0),
    "few": ([0,1], 0),
    "mul": ([0,1], 0),
    "Temperature": ([0.0,1.0,2.0], 1.0),
    "max_tokens": ([10,100,4000], 4000),
    "top_p": ([0.2,0.6,1.0], 0.6),
    "presence_penalty": ([-0.5,0.5,1.5], 0.5),
    "question_type": ([0,1], 0),
    "question_tran": ([0,1], 0),
}

LABEL_CONSIDER_VARS = {
    "deepseekv3": ["question_type", "cot", "max_tokens", "few", "language"],
    "doubao": ["question_type", "cot", "max_tokens", "presence_penalty", "few"],
    "kimiv1": ["question_type", "cot", "mul", "few", "language"],
    "qwen": ["question_type", "cot", "max_tokens", "few", "language"],
    "qwen25": ["question_type", "cot", "max_tokens", "few", "mul"],
    "gpt35": ["question_type", "cot", "mul", "few", "Temperature"],
    "gpt41": ["question_type", "cot", "max_tokens", "Temperature", "top_p"],
    "mistralL": ["question_type", "cot", "max_tokens", "mul", "few"],
    "mistralM": ["question_type", "cot", "max_tokens", "few", "mul"]
}

ALL_LABELS = [
    "deepseekv3",
    "doubao",
    "gpt35",
    "gpt41",
    "kimiv1",
    "mistralL",
    "mistralM",
    "qwen",
    "qwen25"
]


# ===========================================================
# 生成配置空间
# ===========================================================
def generate_config_space(consider_vars):
    keys = list(consider_vars)
    domains = [VARIABLES[k][0] for k in keys]
    combos = itertools.product(*domains)
    config_list = []
    for combo in combos:
        cfg = {}
        # 考虑的变量组合
        for i, k in enumerate(keys):
            cfg[k] = combo[i]
        # 其他变量填默认值
        for k in VARIABLES:
            if k not in cfg:
                cfg[k] = VARIABLES[k][1]
        config_list.append(cfg)
    return config_list


# ===========================================================
# 判断配置是否属于 target_configs（对所有键严格比较）
# ===========================================================
def config_match(cfg, target_configs):
    """
    比较所有 VARIABLES 的 key，
    只有所有字段完全一致才返回 True。
    """
    for tcfg in target_configs:
        same = True
        for key in VARIABLES.keys():
            if cfg.get(key) != tcfg.get(key):
                same = False
                break
        if same:
            return True
    return False


# ===========================================================
# 检测逻辑
# ===========================================================
def check_invalid(content):
    pattern_mark = re.compile(r"####[^#\n]*####")
    has_boxed = "\\boxed" in content
    has_marked = bool(pattern_mark.search(content))
    if not has_boxed and not has_marked:
        return True
    return False


def write_invalid_json(fout, logfile, idx, cfg):
    record = {"file": logfile, "idx": idx, "cfg": cfg}
    fout.write(json.dumps(record, ensure_ascii=False) + "\n")
    fout.flush()


def check_and_record_invalid(block_lines, cfg, logfile, fout):
    mul = cfg.get("mul", 0)
    max_tokens = int(cfg.get("max_tokens", 0))
    language = cfg.get("language", "yy")

    char_per_token = CHAR_PER_TOKEN.get(language, 3.0)
    threshold = max_tokens * char_per_token * SHORT_RATIO

    answers = []
    current = []
    inside = False

    start_pattern = re.compile(r"回答:")
    correct_pattern = re.compile(r"正确答案是:" if mul == 1 else r"正确答案:")

    for line in block_lines:
        if start_pattern.search(line):
            if inside:
                answers.append("\n".join(current).strip())
                current = []
            inside = True
            after = line.split(":", 1)[-1]
            current = [after.strip()]
            continue

        if correct_pattern.search(line):
            if inside:
                answers.append("\n".join(current).strip())
                current = []
                inside = False
            continue

        if inside:
            current.append(line.strip())

    if inside and current:
        answers.append("\n".join(current).strip())

    for idx, content in enumerate(answers, 1):
        if mul == 1:
            # 多轮时仅偶数回答判定截断
            if idx % 2 == 0 and len(content) < threshold and check_invalid(content):
                write_invalid_json(fout, logfile, int(idx / 2), cfg)
        else:
            if len(content) < threshold and check_invalid(content):
                write_invalid_json(fout, logfile, idx, cfg)


# ===========================================================
# 主检测函数
# ===========================================================
def detect_invalid_answers(label, output_path):
    """
    只关注配置在 target_configs 中的 case（全键匹配），
    检测回答是否被截断。
    """
    folders = ["anova_all", "anova_all2"]
    existing_folders = [f for f in folders if os.path.exists(f)]

    if not existing_folders:
        print("[WARN] 未找到 anova_all 或 anova_all2 文件夹，跳过。")
        return

    consider_vars = LABEL_CONSIDER_VARS.get(label)
    if not consider_vars:
        print(f"[WARN] {label} 未在 LABEL_CONSIDER_VARS 定义，跳过。")
        return

    target_configs = generate_config_space(consider_vars)
    print(f"[INFO] {label}: 生成 {len(target_configs)} 目标配置组合（全键匹配）")

    key_cfg_pattern = re.compile(r"key\s*=\s*(\d+),\s*配置=(\{.*\})")

    with open(output_path, "w", encoding="utf-8") as fout:
        fout.write(f"# ===== {datetime.now().strftime('%F %T')} 检测 {label} =====\n")

        for folder in existing_folders:
            for fname in os.listdir(folder):
                if f"_{label}_" not in fname:
                    continue

                filepath = os.path.join(folder, fname)
                print(f"[SCAN] {filepath}")

                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                current_cfg = None
                current_lines = []

                for line in lines:
                    m_cfg = key_cfg_pattern.search(line)
                    if m_cfg:
                        # 处理旧配置块（仅当匹配所有 key）
                        if current_cfg and current_lines:
                            if config_match(current_cfg, target_configs):
                                check_and_record_invalid(current_lines, current_cfg, filepath, fout)
                        # 更新新配置
                        try:
                            current_cfg = ast.literal_eval(m_cfg.group(2))
                        except Exception as e:
                            print(f"[WARN] 配置解析失败: {e} → {line.strip()}")
                            current_cfg = None
                        current_lines = []
                        continue

                    if current_cfg is not None:
                        current_lines.append(line)

                # 文件结束时处理最后一块
                if current_cfg and current_lines:
                    if config_match(current_cfg, target_configs):
                        check_and_record_invalid(current_lines, current_cfg, filepath, fout)


# ===========================================================
# 主入口
# ===========================================================
if __name__ == "__main__":
    base_output_dir = "invalid_records"
    os.makedirs(base_output_dir, exist_ok=True)

    for label in ALL_LABELS:
        print(f"\n====================== 检测模型 {label} ======================")
        output_file = os.path.join(base_output_dir, f"invalid_records_{label}.txt")
        detect_invalid_answers(label, output_file)
        print(f"[DONE] {label} 输出文件: {output_file}")