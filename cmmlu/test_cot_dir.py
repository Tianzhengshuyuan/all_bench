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
    
def extract_answer_from_response(response):
    """
    从回答中提取被####包裹的答案
    """
    match = re.search(r'####\s*([A-D])\s*####', response)
    if match:
        return match.group(1).strip()
    else:
        return None
    
def test_cot(filepath):
    # 读取输入 CSV
    with open(filepath, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        question_count = 0
        right_count = 0
        start_time = time.time()  # 记录开始时间
        
        for row in reader:
            question_count += 1
            if not row:  # 跳过空行
                continue
            text = (
                f"question: {row[1]}\n"
                f"A: {row[2]}\n"
                f"B: {row[3]}\n"
                f"C: {row[4]}\n"
                f"D: {row[5]}"
            )
            prompt = f"下面这道选择题的答案是什么？逐步分析并选出正确选项，最后的答案请使用两个####围起来，比如####B####：\n{text}"
            print(f"题目:\n{text}\n")
            if args.model == "deepseek":
                response = call_deepseek_api(prompt)
            elif args.model == "gpt":
                response = call_gpt_api(prompt)
            elif args.model == "kimi":
                response = call_kimi_api(prompt)
            elif args.model == "doubao":
                response = call_doubao_api(prompt)
            elif args.model == "mistral":
                response = call_mistral_api(prompt)
            elif args.model == "qwen":
                response = call_qwen_api(prompt)
                
            print(f"{args.model}回答:\n{response}， \n正确答案是: {row[6]}\n")
            answer = extract_answer_from_response(response)
            if answer == row[6].strip():
                right_count += 1
        end_time = time.time()  # 记录结束时间
        total_time = end_time - start_time
    if question_count != 0:
        print(f"总题数: {question_count}, 正确答案数: {right_count}, 正确率: {right_count / question_count:.2%}, 耗时: {total_time:.2f}秒")    
    return question_count, right_count
          
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量调用 DeepSeek 翻译")
    parser.add_argument('--dir', required=True, help="输入文件夹名，包含多个CSV文件")
    parser.add_argument('--temperature', type=float, default=0.2, help="API 回答多样性，默认 0.2")
    parser.add_argument('--model', type=str, default="deepseek", help="使用的模型，如gpt、deepseek")
    args = parser.parse_args()
    
    total_questions = 0
    total_right = 0
    
    for filename in os.listdir(args.dir):
        filepath = os.path.join(args.dir, filename)
        if os.path.isfile(filepath) and filepath.endswith(".csv"):
            q, r = test_cot(filepath)
            total_questions += q
            total_right += r

    if total_questions != 0:
        print(f"\n全部统计: 总题数: {total_questions}, 正确答案数: {total_right}, 正确率: {total_right / total_questions:.2%}")
