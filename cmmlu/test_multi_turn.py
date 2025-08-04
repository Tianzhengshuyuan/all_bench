import os
import re
import csv
import time
import openai
import argparse
from openai import OpenAI
from mistralai import Mistral
from volcenginesdkarkruntime import Ark

# 配置 DeepSeek API 客户端
deepseek_client = OpenAI(api_key="sk-09da13b2c97948628523d042d6a02f06", base_url="https://api.deepseek.com")
kimi_client = OpenAI(api_key="sk-ODuizMlUC22phanBhvYz6dBjx2yrz7vhKhcjKnoIrYssThQo", base_url="https://api.moonshot.cn/v1")
doubao_client = Ark(api_key="196b33be-8abb-4af3-9fba-6e266b2dd942")
mistral_client = Mistral(api_key="zWUDyBGqEIdJAtJoxnsr6ACcLTgz1auH")
qwen_client = OpenAI(api_key="sk-341becd932d743f2a750495a0f9f3ede", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

def call_deepseek_api(messages):
    """
    调用 DeepSeek API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
    try:
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=args.temperature,
            stream=False
        )
        return response.choices[0].message
    except Exception as e:
        print(f"调用 DeepSeek API 时出错: {e}")
        return "API 调用失败"
   
def call_gpt_api(messages):
    """
    调用 gpt API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
    os.environ["HTTP_PROXY"] = "http://localhost:7890"
    os.environ["HTTPS_PROXY"] = "http://localhost:7890"
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            temperature=args.temperature,
            stream=False
        )
        return response.choices[0].message
    except Exception as e:
        print(f"调用 gpt API 时出错: {e}")
        return "API 调用失败" 

def call_kimi_api(messages):
    """
    调用 Kimi API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
    try:
        response = kimi_client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=messages,
            temperature=args.temperature,
            stream=False
        )
        return response.choices[0].message
    except Exception as e:
        print(f"调用 Kimi API 时出错: {e}")
        return "API 调用失败"
    
def call_doubao_api(messages):
    """
    调用 豆包 API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
    try:
        response = doubao_client.chat.completions.create(
            model="doubao-1.5-pro-32k-250115",
            # model="doubao-1.5-thinking-pro-250415",
            messages=messages,
            temperature=args.temperature,
            stream=False
        )
        return response.choices[0].message
    except Exception as e:
        print(f"调用 豆包 API 时出错: {e}")
        return "API 调用失败"
    

def call_mistral_api(messages):
    """
    调用 Mistral API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
    try:
        response = mistral_client.chat.complete(
            model="mistral-large-2407",
            # model="mistral-medium-latest",
            messages=messages,
            temperature=args.temperature,
            stream=False
        )
        return response.choices[0].message
    except Exception as e:
        print(f"调用 Mistral API 时出错: {e}")
        return "API 调用失败"
    
def call_qwen_api(messages):
    try:
        response = qwen_client.chat.completions.create(
            model="qwen-plus", 
            messages=messages,
            temperature=args.temperature,
            stream=False
        )
        return response.choices[0].message
    except Exception as e:
        print(f"调用 Qwen API 时出错: {e}")
        return "❌" 
    
def call_qwen25_api(messages):
    try:
        response = qwen_client.chat.completions.create(
            model="qwen2.5-32b-instruct", 
            messages=messages,
            temperature=args.temperature,
            stream=False
        )
        return response.choices[0].message
    except Exception as e:
        print(f"调用 Qwen API 时出错: {e}")
        return "❌" 
    
def extract_answer_from_response(response):
    """
    从回答中提取被####包裹的答案（允许任意内容）
    """
    match = re.search(r'####(.*?)####', response, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return "无匹配"
    
def test_multi_turn(input_file):
    # 读取所有行到内存
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        all_rows = [row for row in reader if row and len(row) >= 2]  # 至少两列

    question_pair_count = 0
    right_count1 = 0
    right_count2 = 0
    start_time = time.time()

    n = len(all_rows)
    for i in range(n):
        row1 = all_rows[i]
        row2 = all_rows[(i + 1) % n]  # 循环到首行

        question_pair_count += 1
        
        text1 = (
            f"question: {row1[1]}\n"
            f"A: {row1[2]}\n"
            f"B: {row1[3]}\n"
            f"C: {row1[4]}\n"
            f"D: {row1[5]}"
        )
        text2 = (
            f"question: {row2[1]}\n"
            f"A: {row2[2]}\n"
            f"B: {row2[3]}\n"
            f"C: {row2[4]}\n"
            f"D: {row2[5]}"
        )
        # 第一轮
        prompt1 = f"以下是选择题，请直接给出正确答案的选项，使用两个####围起来，比如####B####，不要返回任何其他内容\n{text1}"
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt1}
        ]
        print(f"第{i+1}组 第一轮题目:\n{prompt1}\n")
        if args.model == "deepseek":
            response1 = call_deepseek_api(messages)
        elif args.model == "gpt":
            response1 = call_gpt_api(messages)
        elif args.model == "kimi":
            response1 = call_kimi_api(messages)
        elif args.model == "doubao":
            response1 = call_doubao_api(messages)
        elif args.model == "mistral":
            response1 = call_mistral_api(messages)
        elif args.model == "qwen":
            response1 = call_qwen_api(messages)
        elif args.model == "qwen25":
            response1 = call_qwen25_api(messages)
        
        if hasattr(response1, "content"):
            print(f"{args.model}回答: {response1.content} \n正确答案是: {row1[6]}\n")
            answer1 = extract_answer_from_response(response1.content)
            if answer1 == row1[6].strip():
                right_count1 += 1
        else:
            continue

        # 第二轮
        messages.append({"role": "assistant", "content": response1.content})  # assistant角色
        messages.append({"role": "user", "content": text2})
        print(f"第{i+1}组 第二轮题目:\n{text2}\n")
        if args.model == "deepseek":
            response2 = call_deepseek_api(messages)
        elif args.model == "gpt":
            response2 = call_gpt_api(messages)
        elif args.model == "kimi":
            response2 = call_kimi_api(messages)
        elif args.model == "doubao":
            response2 = call_doubao_api(messages)
        elif args.model == "mistral":
            response2 = call_mistral_api(messages)
        elif args.model == "qwen":
            response2 = call_qwen_api(messages)
        elif args.model == "qwen25":
            response2 = call_qwen25_api(messages)

        if hasattr(response2, "content"):
            print(f"{args.model}回答: {response2.content} \n正确答案是: {row2[6]}\n")
            answer2 = extract_answer_from_response(response2.content)
            if answer2 == row2[6].strip():
                right_count2 += 1

    end_time = time.time()
    total_time = end_time - start_time
    if question_pair_count != 0:       
        print(f"{os.path.basename(filepath)}测试完毕！总题数: {question_pair_count}, 第一轮正确答案数: {right_count1}, 正确率: {right_count1 / question_pair_count:.2%}，第二轮正确答案数: {right_count2}, 正确率: {right_count2 / question_pair_count:.2%}, 总耗时: {total_time:.2f}秒")
    return question_pair_count, right_count1, right_count2


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量调用 DeepSeek 翻译")
    parser.add_argument('--dir', required=True, help="输入文件所在文件夹")
    parser.add_argument('--temperature', type=float, default=0.2, help="API 回答多样性，默认 0.2")
    parser.add_argument('--model', type=str, default="deepseek", help="使用的模型，如gpt、deepseek")
    args = parser.parse_args()

    total_questions = 0
    total_right1 = 0
    total_right2 = 0
    
    for filename in os.listdir(args.dir):
        filepath = os.path.join(args.dir, filename)
        if os.path.isfile(filepath) and filepath.endswith(".csv"):
            q, r1, r2 = test_multi_turn(filepath)
            total_questions += q
            total_right1 += r1
            total_right2 += r2

    if total_questions != 0:
        print(f"\n全部统计: 总题数: {total_questions}, 第一轮正确答案数: {total_right1}, 正确率: {total_right1 / total_questions:.2%}, 第二轮正确答案数: {total_right2}, 正确率: {total_right2 / total_questions:.2%}")
