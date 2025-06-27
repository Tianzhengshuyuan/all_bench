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

def call_deepseek_api(question):
    """
    调用 DeepSeek API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
    try:
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            temperature=args.temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 DeepSeek API 时出错: {e}")
        return "API 调用失败"
   
def call_gpt_api(question):
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
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            temperature=args.temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 gpt API 时出错: {e}")
        return "API 调用失败" 

def call_kimi_api(question):
    """
    调用 Kimi API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
    try:
        response = kimi_client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            temperature=args.temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 Kimi API 时出错: {e}")
        return "API 调用失败"
    
def call_doubao_api(question):
    """
    调用 豆包 API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
    try:
        response = doubao_client.chat.completions.create(
            model="doubao-1.5-pro-32k-250115",
            # model="doubao-1.5-thinking-pro-250415",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            temperature=args.temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 豆包 API 时出错: {e}")
        return "API 调用失败"
    
def call_mistral_api(question):
    """
    调用 Mistral API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
    try:
        response = mistral_client.chat.complete(
            model="mistral-large-2407",
            # model="mistral-medium-latest",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            temperature=args.temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 Mistral API 时出错: {e}")
        return "API 调用失败"
    
def call_qwen_api(question):
    try:
        response = qwen_client.chat.completions.create(
            model="qwen-plus", 
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': question},
            ],
            temperature=args.temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 Qwen API 时出错: {e}")
        return "❌"
    
def load_few_shot_examples():
    examples = []
    with open(args.input_few_shot, 'r', encoding='utf-8') as fs:
        reader = csv.reader(fs)
        for row in reader:
            if not row or len(row) < 6:
                continue
            example = (
                f"question: {row[0]}\n"
                f"A: {row[1]}\n"
                f"B: {row[2]}\n"
                f"C: {row[3]}\n"
                f"D: {row[4]}\n"
                f"answer: {row[5]}"
            )
            examples.append(example)
    return "\n\n".join(examples)
    
def extract_answer_from_response(response):
    """
    从回答中提取被####包裹的答案（允许任意内容）
    """
    match = re.search(r'####(.*?)####', response, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return "无匹配"
    
def test_multi_turn():
    # 读取输入 CSV
    with open(args.input, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        question_count = 0
        right_count1 = 0
        right_count2 = 0
        start_time = time.time()  # 记录开始时间

        for row in reader:
            question_count += 1
            if not row:  # 跳过空行
                continue

            prompt1 = f"What is the answer to the following math question? Only provide the final result. Do not return anything else. Please use two pairs of #### to surround your answer, for example, ####6####: \n{row[0]}"
            print(f"题目:\n{prompt1}\n")
            if args.model == "deepseek":
                response1 = call_deepseek_api(prompt1)
            elif args.model == "gpt":
                response1 = call_gpt_api(prompt1)
            elif args.model == "kimi":
                response1 = call_kimi_api(prompt1)
            elif args.model == "doubao":
                response1 = call_doubao_api(prompt1)
            elif args.model == "mistral":
                response1 = call_mistral_api(prompt1)
            elif args.model == "qwen":
                response1 = call_qwen_api(prompt1)
                
            print(f"{args.model}回答:{response1} \n正确答案是: {row[1]}\n")
            answer1 = extract_answer_from_response(response1)
            if answer1 == row[1].strip():
                right_count1 += 1
            else:
                continue
            
            prompt2= f"{prompt1}\n{response1}\n{row[2]}\n"
            print(f"第二轮题目:\n{prompt2}\n")
            if args.model == "deepseek":
                response2 = call_deepseek_api(prompt2)
            elif args.model == "gpt":
                response2 = call_gpt_api(prompt2)
            elif args.model == "kimi":
                response2 = call_kimi_api(prompt2)
            elif args.model == "doubao":
                response2 = call_doubao_api(prompt2)
            elif args.model == "mistral":
                response2 = call_mistral_api(prompt2)
            elif args.model == "qwen":
                response2 = call_qwen_api(prompt2)
                
            print(f"{args.model}回答:{response2} \n正确答案是: {row[3]}\n")
            answer2 = extract_answer_from_response(response2)
            if answer2 == row[3].strip():
                right_count2 += 1
        end_time = time.time()  # 记录结束时间
        total_time = end_time - start_time
    if question_count != 0:
        print(f"总题数: {question_count}, 第一轮正确答案数: {right_count1}, 正确率: {right_count1 / question_count:.2%}，第二轮正确答案数: {right_count2}, 正确率: {right_count2 / question_count:.2%}, 耗时: {total_time:.2f}秒")        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量调用 DeepSeek 翻译")
    parser.add_argument('--input', required=True, help="输入 CSV 文件名")
    parser.add_argument('--temperature', type=float, default=0.2, help="API 回答多样性，默认 0.2")
    parser.add_argument('--model', type=str, default="deepseek", help="使用的模型，如gpt、deepseek")
    args = parser.parse_args()

    test_multi_turn()
