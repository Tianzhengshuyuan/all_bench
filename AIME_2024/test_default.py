import os
import re
import csv
import time
from tqdm import tqdm
import pickle
import openai
import argparse
from openai import OpenAI
from mistralai import Mistral
from volcenginesdkarkruntime import Ark

deepseek_client = OpenAI(api_key="sk-09da13b2c97948628523d042d6a02f06", base_url="https://api.deepseek.com")
kimi_client = OpenAI(api_key="sk-ODuizMlUC22phanBhvYz6dBjx2yrz7vhKhcjKnoIrYssThQo", base_url="https://api.moonshot.cn/v1")
doubao_client = Ark(api_key="196b33be-8abb-4af3-9fba-6e266b2dd942")
mistral_client = Mistral(api_key="zWUDyBGqEIdJAtJoxnsr6ACcLTgz1auH")
qwen_client = OpenAI(api_key="sk-341becd932d743f2a750495a0f9f3ede", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

# == API 调用 ==
def call_doubao_api(messages, args):
    try:
        response = doubao_client.chat.completions.create(
            model="doubao-1.5-pro-32k-250115",
            messages=messages,
            temperature=args.temperature,
            top_p=args.top_p,
            presence_penalty=args.presence_penalty,
            max_tokens=args.max_tokens,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 豆包 API 时出错: {e}")
        return "API 调用失败"

def call_deepseek_api(messages, args):
    try:
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=args.temperature,
            top_p=args.top_p,
            presence_penalty=args.presence_penalty,
            max_tokens=args.max_tokens,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 deepseek API 时出错: {e}")
        return "API 调用失败"

def call_qwen_api(messages, args):
    try:
        response = qwen_client.chat.completions.create(
            model="qwen-plus",
            messages=messages,
            temperature=args.temperature,
            top_p=args.top_p,
            presence_penalty=args.presence_penalty,
            max_tokens=args.max_tokens,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 Qwen API 时出错: {e}")
        return "API 调用失败"
    
def call_qwen25_api(messages, args):
    try:
        response = qwen_client.chat.completions.create(
            model="qwen2.5-32b-instruct",
            messages=messages,
            temperature=args.temperature,
            top_p=args.top_p,
            presence_penalty=args.presence_penalty,
            max_tokens=args.max_tokens,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 Qwen2.5 API 时出错: {e}")
        return "API 调用失败"
    
def call_kimi_api(messages, args):
    try:
        response = kimi_client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=messages,
            temperature=args.temperature,
            top_p=args.top_p,
            presence_penalty=args.presence_penalty,
            max_tokens=args.max_tokens,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 kimi API 时出错: {e}")
        return "API 调用失败"
    
def call_mistralS_api(messages, args):
    try:
        response = mistral_client.chat.complete(
            model="mistral-small-latest",
            messages=messages,
            temperature=args.temperature,
            top_p=args.top_p,
            presence_penalty=args.presence_penalty,
            max_tokens=args.max_tokens,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 Mistral API 时出错: {e}")
        return "API 调用失败"
    
def call_mistralL_api(messages, args):
    try:
        response = mistral_client.chat.complete(
            model="mistral-large-latest",
            messages=messages,
            temperature=args.temperature,
            top_p=args.top_p,
            presence_penalty=args.presence_penalty,
            max_tokens=args.max_tokens,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 Mistral API 时出错: {e}")
        return "API 调用失败"
        
def call_gpt35_api(messages, args):
    os.environ["HTTP_PROXY"] = "http://localhost:7890"
    os.environ["HTTPS_PROXY"] = "http://localhost:7890"
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=args.temperature,
            top_p=args.top_p,
            presence_penalty=args.presence_penalty,
            max_tokens=args.max_tokens,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 gpt API 时出错: {e}")
        return "API 调用失败"
    
def call_gpt4_api(messages, args):
    os.environ["HTTP_PROXY"] = "http://localhost:7890"
    os.environ["HTTPS_PROXY"] = "http://localhost:7890"
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            temperature=args.temperature,
            top_p=args.top_p,
            presence_penalty=args.presence_penalty,
            max_tokens=args.max_tokens,
            stream=False
        )
        print(response)
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 gpt API 时出错: {e}")
        return "API 调用失败"
    
def call_LLM_api(model, messages, args):
    if model == "doubao":
        return call_doubao_api(messages, args)
    elif model == "deepseek":
        return call_deepseek_api(messages, args)    
    elif model == "kimi":
        return call_kimi_api(messages, args)
    elif model == "qwen":
        return call_qwen_api(messages, args)
    elif model == "qwen25": 
        return call_qwen25_api(messages, args)
    elif model == "mistralS":
        return call_mistralS_api(messages, args)
    elif model == "mistralL":   
        return call_mistralL_api(messages, args)
    elif model == "gpt35":
        return call_gpt35_api(messages, args)
    elif model == "gpt4":
        return call_gpt4_api(messages, args)
    
# == 提取模型答案 ==
def extract_answer_from_response(content):
    import re
    # 匹配 ####answer####
    m = re.search(r'####(.*?)####', content)
    if m:
        return m.group(1).strip()
    return content.strip()
    

# == 单轮测试 ==
def test_default(input_file, args):
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        all_rows = [row for row in reader if row and len(row) >= 2]
    right_count = 0
    total = len(all_rows)
    
    start_time = time.time()
    for i, row in enumerate(all_rows):
        question = row[0]
        answer = row[1] 
        prompt = f"The following is fill-in-the-blank question. Please return only the correct answer and nothing else. Please enclose the final answer with two pairs of ####, for example: ####6####.\n{row[0]}"
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        print(f"第{i+1}题 prompt:\n{prompt}\n")
        response = call_LLM_api(args.model, messages, args)
        print(f"模型回答: {response} \n正确答案: {answer}\n")
        model_answer = extract_answer_from_response(response)
        if model_answer == answer.strip():
            right_count += 1
    end_time = time.time()
    print(f"总题数: {total}, 正确数: {right_count}, 正确率: {right_count/total:.2%}, 耗时: {end_time - start_time:.2f}s")

if __name__ == "__main__":
    # == 通用参数解析 ==
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="doubao")
    parser.add_argument("--csv_dir", type=str, default="csv")
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--top_p", type=float, default=1.0)
    parser.add_argument("--presence_penalty", type=float, default=0.0)
    parser.add_argument("--max_tokens", type=int, default=1024)
    args = parser.parse_args()

    test_default("csv/filling_english.csv", args)

