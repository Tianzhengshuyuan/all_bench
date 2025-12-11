import os
import re
import ast
import itertools
import pickle
import random

# ====== 全局变量定义 ======
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

# ====== 工具函数 ======
def generate_config_space(consider_vars):
    keys = list(consider_vars)
    domains = [VARIABLES[k][0] for k in keys]
    combos = list(itertools.product(*domains))
    config_list = []
    for combo in combos:
        config = {k: combo[i] for i, k in enumerate(keys)}
        for k in VARIABLES:
            if k not in config:
                config[k] = VARIABLES[k][1]
        config_list.append(config)
    return config_list

def parse_config(line, filepath=None, lineno=None):
    m = re.search(r", 配置=(\{.*\})", line)
    if m:
        config_str = m.group(1)
        try:
            config = ast.literal_eval(config_str)
            return config
        except Exception as e:
            loc_info = ""
            if filepath and lineno:
                loc_info = f"[文件: {filepath}, 行: {lineno}] "
            preview = config_str[:1000] + ("..." if len(config_str) > 1000 else "")
            print(f"{loc_info}解析配置失败: {e}\n内容预览: {preview}")
    return None

# ====== 主逻辑 ======
def find_missing_configs(label, consider_vars, output_pkl):
    folders = ["anova_all", "anova_all2"]
    existing_folders = [f for f in folders if os.path.exists(f)]
    target_configs = generate_config_space(consider_vars)
    print(f"{label}: 总目标配置 {len(target_configs)}")

    target_set = set([frozenset(cfg.items()) for cfg in target_configs])
    found_cfgs = set()

    for folder in existing_folders:
        for fname in os.listdir(folder):
            if f"_{label}_" not in fname:
                continue
            filepath = os.path.join(folder, fname)
            with open(filepath, "r", encoding="utf-8") as f:
                for lineno, line in enumerate(f, start=1):
                    if "配置={" in line:
                        cfg = parse_config(line, filepath=filepath, lineno=lineno)
                        if cfg:
                            found_cfgs.add(frozenset(cfg.items()))

    missing_cfgs = [dict(cfg) for cfg in target_set - found_cfgs]
    print(f"{label}: 缺失 {len(missing_cfgs)} 个配置")

    random.shuffle(missing_cfgs)
    with open(output_pkl, "wb") as f:
        pickle.dump(missing_cfgs, f)
    print(f"{label}: 已保存到 {output_pkl}")
    return missing_cfgs

if __name__ == "__main__":
    labels = ["deepseekv3","kimiv1","doubao","qwen","qwen25","mistralL","mistralM","gpt35","gpt41"]
    for label in labels:
        consider_vars = LABEL_CONSIDER_VARS[label]
        output_file = f"missing_{label}.pkl"
        missing = find_missing_configs(label, consider_vars, output_file)
        print("示例缺失配置：", missing[:3])
        print("="*50)