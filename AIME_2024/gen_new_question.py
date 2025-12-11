import json
import random
import itertools
import sympy as sp
import csv
import math
import argparse
from math import comb
from fractions import Fraction
from solution_bank import *

def load_problem_bank(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)["problems"]

def random_parameters(param_schema: dict, relations: list = None, fixed_param: dict = None, dependency_parameters: dict = None, max_attempts: int = 5000) -> dict:
    params = dict(fixed_param or {})
    names_to_generate = [name for name in param_schema if name not in params]

    # 若没有关系要求则简单生成
    if not relations and not dependency_parameters:
        for name in names_to_generate:
            spec = param_schema[name]
            if spec["type"] == "int":
                params[name] = random.randrange(spec["min"], spec["max"] + 1, spec.get("step", 1))
        return params

    attempts = 0
    while attempts < max_attempts:
        attempts += 1
        trial_params = dict(params)
        # 先生成所有未固定参数
        for name in names_to_generate:
            spec = param_schema[name]
            if spec["type"] == "int":
                trial_params[name] = random.randrange(spec["min"], spec["max"] + 1, spec.get("step", 1))
                
        if dependency_parameters:
            for dep_name, dep_info in dependency_parameters.items():
                base_name = dep_info["depends_on"]

                # 如果依赖参数尚未生成则跳过
                if base_name not in trial_params:
                    continue

                base_val = trial_params[base_name]
                rule_type = dep_info.get("rule_type", "mapping")

                # --- 条件逻辑型依赖 ---
                if rule_type == "conditional":
                    selected_value = None
                    for rule in dep_info["rules"]:
                        try:
                            # 安全评估条件表达式
                            cond_result = eval(rule["condition"], {"math": math}, trial_params)
                            if cond_result:
                                selected_value = random.choice(rule["choices"])
                                break
                        except Exception:
                            continue
                    if selected_value is not None:
                        trial_params[dep_name] = selected_value

                # --- 旧版本映射型依赖 ---
                elif rule_type == "mapping":
                    mapping = dep_info["mapping"]
                    key = str(base_val)
                    if key in mapping:
                        trial_params[dep_name] = random.choice(mapping[key])
                        
        # 检查是否满足全部关系表达式
        ok = True
        if relations:
            for rel in relations:
                try:
                    # 安全 eval 环境
                    if not eval(rel["expression"], {"math": math}, trial_params):
                        ok = False
                        break
                except Exception:
                    ok = False
                    break
        if ok:
            return trial_params

    raise ValueError(f"无法在 {max_attempts} 次尝试内生成满足条件的参数组合。")

def execute_solution(problem: dict, params: dict) -> int:
    func_name = problem["solution_rule"]["name"]
    func = globals().get(func_name)
    if not func:
        raise ValueError(f"Function {func_name} not defined")
    return func(**params)

# === 保存题目到CSV文件的函数 ===
def save_questions_to_csv(questions: list, csv_file: str = "composed_questions.csv"):
    if not questions:
        print("没有题目可保存")
        return
    
    # 检查文件是否存在，如果不存在则创建并写入表头[5](@ref)
    file_exists = False
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            file_exists = True
    except FileNotFoundError:
        file_exists = False
    
    with open(csv_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # 如果文件不存在，写入表头
        if not file_exists:
            writer.writerow(["Question", "Answer"])
            
        # 写入所有题目和答案及来源
        for q in questions:
            source_info = q.get("source_problems", "N/A")
            writer.writerow([q["question"], q["answer"], source_info, q.get("k", "N/A")])
    
# === 修改后的拼接函数 ===
def compose_multiple_problems(problem1, problem2, num1=100, num2=10, num3=100, num4=10, symbol_name="k", csv_file="composed_questions.csv"):
    """
    构造多道拼接题目：
    - 对第一题尝试num1个随机参数组合
    - 找到num2个可以作为第二题输入的第一题输出
    - 对每个可用输出，生成num3个第二题参数组合
    - 共生成num2*num3道题目
    """
    all_composed_questions = []
    
    # 1️.尝试生成第一题参数组合，最多尝试num1个
    valid_outputs = []  # 存储可用的第一题输出及其信息
    attempted_combinations = 0
    
    print(f"尝试生成最多 {num1} 个第一题参数组合，寻找 {num2} 个可用输出...")
    
    while attempted_combinations < num1 and len(valid_outputs) < num2:
        try:
            # 生成第一题参数
            params1 = random_parameters(param_schema=problem1["parameters"], relations=problem1.get("relations"), fixed_param=None, dependency_parameters=problem1.get("dependency_parameters"))
            ans1 = execute_solution(problem1, params1)
            
            # 检查这个输出是否能作为第二题的某个输入参数，不考虑范围依赖其他参数的参数
            matched_param = None
            for pname, pspec in problem2["parameters"].items():
                if "relation" in pspec:
                    continue
                if pspec["type"] == "int" and pspec["min"] <= ans1 <= pspec["max"]:
                    matched_param = pname
                    break
            
            if matched_param is not None:
                # 检查是否已经存在相同的输出值（避免重复）
                if not any(output_info["output1"] == ans1 for output_info in valid_outputs):
                    valid_outputs.append({
                        "output1": ans1,
                        "params1": params1.copy(),
                        "matched_param": matched_param
                    })
                    print(f"【{len(valid_outputs)}】 当第一题参数为{params1}时，得到可用输出: {ans1}，匹配第二题参数: {matched_param}")
            
            attempted_combinations += 1
            
        except Exception as e:
            # print(f"生成第一题参数时出错: {e}")
            attempted_combinations += 1
            continue
    
    print(f"尝试了 {attempted_combinations} 个组合，找到 {len(valid_outputs)} 个可用输出\n")
    
    if not valid_outputs:
        print("未找到任何可用输出，无法生成题目")
        return []
    
    # 3️.对每个可用输出，生成第二题的多个参数组合
    total_generated = 0
    
    for i, output_info in enumerate(valid_outputs):
        ans1 = output_info["output1"]
        matched_param = output_info["matched_param"]
        params1 = output_info["params1"]
                
        # 为这个输出生成num4个第二题参数组合
        second_problem_combinations = []
        attempts = 0
        
        while attempts < num3 and len(second_problem_combinations) < num4:
            try:
                # 生成第二题参数，但跳过已匹配的参数
                fixed_param = {matched_param: ans1}
                params2 = random_parameters(param_schema=problem2["parameters"], relations=problem2.get("relations"), fixed_param=fixed_param, dependency_parameters=problem2.get("dependency_parameters"))
                if matched_param in params2:
                    params2.pop(matched_param)
                
                # 检查这个组合是否已经存在
                combo_key = str(sorted(params2.items()))
                if not any(str(sorted(combo.items())) == combo_key 
                          for combo in second_problem_combinations):
                    second_problem_combinations.append(params2.copy())
                    attempts = 0  # 重置尝试计数
                else:
                    attempts += 1
                    
            except Exception as e:
                attempts += 1
                continue
        
        print(f"为输出【{i+1}】{matched_param}={ans1} 生成 {len(second_problem_combinations)} 个第二题参数组合： {second_problem_combinations}")
        
        # 4️.为每个组合生成题目
        for j, params2 in enumerate(second_problem_combinations):
            # ✅ 安全替换 JSON 模板中的占位变量 ${var}
            def safe_replace(template: str, params: dict):
                text = template
                for pname, value in params.items():
                    text = text.replace("{" + pname + "}", str(value))
                return text

            # 第一题文本
            q1_text = safe_replace(problem1["question_template"], params1)
            q1_text = q1_text.replace(" ,", ",")
            
            # 第二题文本（带符号化变量）
            q2_text = safe_replace(problem2["question_template"], params2)
            q2_symbolic = q2_text.replace("{" + matched_param + "}", f"{symbol_name}")
            q2_symbolic = q2_symbolic[0] + q2_symbolic[1:]
            
            # 拼接最终题面
            combined_question = f"{q1_text} Let the answer be ${symbol_name}$. {q2_symbolic}"
            
            # 计算最终答案
            full_params2 = params2.copy()
            full_params2[matched_param] = ans1
            final_answer = execute_solution(problem2, full_params2)
            
            # 添加到题目列表
            all_composed_questions.append({
                "question": combined_question,
                "answer": final_answer,
                "source_problems": f"{problem1['problem_id']}→{problem2['problem_id']}",
                "k": ans1,
                "metadata": {
                    "first_problem_params": params1,
                    "second_problem_params": full_params2,
                    "link_param": matched_param,
                    "output_value": ans1
                }
            })
            
            total_generated += 1   
    return all_composed_questions

# === 主控制函数 ===
def synthesize_multiple_composed_problems(json_file: str, num1=100, num2=10, num3=100, num4=10, symbol_name="k", csv_file="composed_questions.csv", method=0, q1_id=None, q2_id=None):
    """
    主函数：生成多个组合题目

    method:
      0 → 相邻成对组合（题 i 与题 i+1）
      1 → 仅组合指定的两题（由 q1_id、q2_id 指定）
      其他 → 所有题的两两排列组合
    """

    problems = load_problem_bank(json_file)

    if len(problems) < 2:
        print("需要至少两个题目来组合")
        return

    results = []
    failed_pairs = []

    # ================== 核心逻辑 ==================
    if method == 0:
        # 按顺序相邻组合，最后一题与第一题也组合
        pairs = [(problems[i], problems[(i + 1) % len(problems)]) for i in range(len(problems))]
        print(f"⚙️ 使用『循环相邻组合模式（首尾相连）』，共 {len(pairs)} 对题目。")

    elif method == 1:
        # 使用指定 ID 的两道题组合
        if q1_id is None or q2_id is None:
            print("❌ 当 method=1 时，必须提供 q1_id 与 q2_id 参数。")
            return

        id_map = {p["problem_id"]: p for p in problems}
        if q1_id not in id_map or q2_id not in id_map:
            print(f"❌ 指定的 problem_id 不存在：q1_id={q1_id}, q2_id={q2_id}")
            return

        problem1, problem2 = id_map[q1_id], id_map[q2_id]
        pairs = [(problem1, problem2)]
        print(f"⚙️ 使用『指定题目组合模式』：[ {q1_id} → {q2_id} ]")

    else:
        # 全排列组合
        pairs = list(itertools.permutations(problems, 2))
        print(f"⚙️ 使用『全排列组合模式』，共 {len(pairs)} 对题目。")
    # ===================================================

    for idx, (problem1, problem2) in enumerate(pairs, 1):
        print("==========================================================================================================")
        print(f"[{idx}/{len(pairs)}] Selected pair: "
              f"[{problem1['problem_id']}][{problem1['title']}] → "
              f"[{problem2['problem_id']}][{problem2['title']}]")

        composed = compose_multiple_problems(problem1, problem2, num1, num2, num3, num4, symbol_name, csv_file)

        if composed:
            save_questions_to_csv(composed, csv_file)
            results.extend(composed)
            print(f"✅ 已生成 {len(composed)} 道题并保存。")
        else:
            print(f"⚠️ 未生成任何题目。")
            failed_pairs.append({
                "index": idx,
                "problem1": problem1,
                "problem2": problem2
            })

    # 打印统计结果
    print(f"===== 全部完成: 共生成 {len(results)} 道组合题 =====")

    if failed_pairs:
        print(f"⚠️ 以下 {len(failed_pairs)} 对题目组合未生成任何题目：")
        for fail in failed_pairs:
            print(f"  [{fail['index']}] "
                  f"[{fail['problem1']['problem_id']}][{fail['problem1']['title']}] → "
                  f"[{fail['problem2']['problem_id']}][{fail['problem2']['title']}]")
    else:
        print("✅ 所有题目组合均成功生成。")

    return results


# === 演示 ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成多道拼接题目")
    parser.add_argument("--json_file", type=str, default="a_mes/question_meta.json", help="题库JSON文件路径")
    parser.add_argument("--csv_file", type=str, default="csv_cat/composed_questions.csv", help="输出CSV文件名")
    parser.add_argument("--num1", type=int, default=1000, help="尝试的第一题参数组合数量")
    parser.add_argument("--num2", type=int, default=10, help="希望得到的第一题可用输出数量")
    parser.add_argument("--num3", type=int, default=1000, help="尝试的第二题剩余参数组合数量")
    parser.add_argument("--num4", type=int, default=10, help="希望得到的第二题剩余参数组合数量")
    parser.add_argument("--method", type=int, default=0, help="生成组合的方法")
    parser.add_argument("--q1_id", type=int, default=1, help="第一题ID（可选）")
    parser.add_argument("--q2_id", type=int, default=2, help="第二题ID（可选）")
    args = parser.parse_args()
    
    # 运行前清空 CSV 文件
    open(args.csv_file, "w").close()
    
    # 可以调整参数来控制生成数量
    synthesize_multiple_composed_problems(
        args.json_file, 
        num1=args.num1,    
        num2=args.num2,     
        num3=args.num3,   
        num4=args.num4,  
        csv_file=args.csv_file,
        method=args.method,
        q1_id=args.q1_id,
        q2_id=args.q2_id
    )