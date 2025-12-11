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

kimi_client = OpenAI(api_key="sk-PKbPiYj76SgZgYIxx5liZUexfqZYsUsqSHDXp5RMZ28iMqqr", base_url="https://api.moonshot.cn/v1")
doubao_client = Ark(api_key="65c0c79f-e50a-4626-992a-360293751d33")
mistral_client = Mistral(api_key="GYCQ8pMgX3E51NsmAjqrwI25zLZClHxo")
qwen_client = OpenAI(api_key="sk-6f348558fd63438faa04c58794e0199a", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
deepseek_client = OpenAI(api_key="sk-84733ef2d077471499462cf48c94fd62", base_url="https://api.deepseek.com")

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
        # response = deepseek_client.chat.completions.create(
        response = doubao_client.chat.completions.create(
            # model="deepseek-chat",
            model="deepseek-v3-250324",
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
    
def call_mistralM_api(messages, args):
    try:
        response = mistral_client.chat.complete(
            model="mistral-medium-latest",
            messages=messages,
            temperature=args.temperature,
            top_p=args.top_p,
            presence_penalty=args.presence_penalty,
            max_tokens=args.max_tokens,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 MistralM API 时出错: {e}")
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
    
def call_gpt41_api(messages, args):
    os.environ["HTTP_PROXY"] = "http://localhost:7890"
    os.environ["HTTPS_PROXY"] = "http://localhost:7890"
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.chat.completions.create(
            model="gpt-4.1",
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
    elif model == "mistralM":
        return call_mistralM_api(messages, args)
    elif model == "mistralL":   
        return call_mistralL_api(messages, args)
    elif model == "gpt35":
        return call_gpt35_api(messages, args)
    elif model == "gpt4":
        return call_gpt4_api(messages, args)
    elif model == "gpt41":
        return call_gpt41_api(messages, args)
    
# == 提取模型答案 ==
def extract_answer_from_response(content):
    import re
    # 匹配 ####answer####
    m = re.search(r'####(.*?)####', content)
    if m:
        return m.group(1).strip()
    return content.strip()  
import json
# == 单轮测试 ==
def test_default(input_file, args):
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        all_rows = [row for row in reader if row and len(row) >= 2]
    right_count = 0
    total = len(all_rows)
    
    start_time = time.time()
    all_data =[]
    
    for i, row in enumerate(all_rows):
        data = {}
        question = row[0]
        answer = row[1] 
        if args.cot:
            prompt = f"The following is fill-in-the-blank question. Analyze it step by step and enclose the final answer with two pairs of ####, for example: ####6####.\n{row[0]}"
        else:
            prompt = f"The following is fill-in-the-blank question. Please return only the correct answer and nothing else. Please enclose the final answer with two pairs of ####, for example: ####6####.\n{row[0]}"
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        print(f"第{i+1}题 prompt:\n{prompt}\n")
        start_time1 = time.time()
        response = call_LLM_api(args.model, messages, args)
        print(f"模型回答: {response} \n正确答案: {answer}\n",flush=True)
        model_answer = extract_answer_from_response(response)
        data['llm_response'] = response
        data['llm_answer'] = model_answer
        data['answer'] = answer
        data['time'] = time.time()-start_time1
        data['prompt'] = prompt
        all_data.append(data.copy())
        if model_answer == answer.strip():
            right_count += 1
    end_time = time.time()
    print(f"总题数: {total}, 正确数: {right_count}, 正确率: {right_count/total:.2%}, 耗时: {end_time - start_time:.2f}s")
    answer_file = "./result/"+input_file[8:-4]+"_"+args.model+"_"+str(args.cot)+"_answer.json"
    with open(answer_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # == 通用参数解析 ==
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="doubao")
    parser.add_argument("--csv_dir", type=str, default="csv")
    parser.add_argument("--temperature", type=float)
    parser.add_argument("--top_p", type=float)
    parser.add_argument("--presence_penalty")
    parser.add_argument("--max_tokens", type=int)
    parser.add_argument("--cot", action="store_true", help="是否使用COT")
    parser.add_argument("--input", type=str, default="csv/filling_english_analogical.csv", help="输入的CSV文件路径")
    args = parser.parse_args()
    test_default(args.input, args)

