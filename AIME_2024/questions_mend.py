import os
import re
import ast
import csv
import json
import time
import pickle
import openai
import argparse
import itertools
from tqdm import tqdm
from openai import OpenAI
from datetime import datetime
from mistralai import Mistral
from volcenginesdkarkruntime import Ark

CHAR_PER_TOKEN = {
    "yy": 5.3,     # English
    "zw": 1.7,     # 中文
    "ry": 1.0,     # 日语
    "ey": 3.8,     # 俄语
    "fy": 4.3,     # 法语
    "alby": 2.6,   # 阿拉伯语
}
SHORT_RATIO = 0.4

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


deepseek_client = OpenAI(api_key="sk-09da13b2c97948628523d042d6a02f06", base_url="https://api.deepseek.com")
kimi_client = OpenAI(api_key="sk-ODuizMlUC22phanBhvYz6dBjx2yrz7vhKhcjKnoIrYssThQo", base_url="https://api.moonshot.cn/v1")
doubao_client = Ark(api_key="196b33be-8abb-4af3-9fba-6e266b2dd942")
# mistral_client = Mistral(api_key="zWUDyBGqEIdJAtJoxnsr6ACcLTgz1auH")
# mistral_client = Mistral(api_key="GYCQ8pMgX3E51NsmAjqrwI25zLZClHxo")
mistral_client = Mistral(api_key="8ucMzW3yRXLyXGqW6WkuuOuVucM1VgXI")
qwen_client = OpenAI(api_key="sk-341becd932d743f2a750495a0f9f3ede", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
gemini_client = OpenAI(api_key="AIzaSyB1Kwa7mos2CuVQmvOZYtQd8ql4AljYx_g", base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

PROMPT_TEMPLATES = {
    "english": {
        "fill_cot_few":      "The following are fill-in-the-blank questions. Analyze them step by step and enclose the final answer with two pairs of ####, for example: ####6####.\n{few_shot_examples}\n{content}",
        "fill_cot":          "The following is fill-in-the-blank question. Analyze it step by step and enclose the final answer with two pairs of ####, for example: ####6####.\n{content}",
        "choice_cot_few":    "The following are multiple-choice questions. Analyze them step by step and enclose the final answer with two pairs of ####, for example: ####A####.\n{few_shot_examples}\n{content}",
        "choice_cot":        "The following is multiple-choice question. Analyze it step by step and enclose the final answer with two pairs of ####, for example: ####A####.\n{content}",
        "fill_nocot_few":    "The following are fill-in-the-blank questions. Please return only the correct answer and nothing else. Please enclose the final answer with two pairs of ####, for example: ####6####.\n{few_shot_examples}\n{content}",
        "fill_nocot":        "The following is fill-in-the-blank question. Please return only the correct answer and nothing else. Please enclose the final answer with two pairs of ####, for example: ####6####.\n{content}",
        "choice_nocot_few":  "The following are multiple-choice questions. Please return only the correct answer and nothing else. Please enclose the final answer with two pairs of ####, for example: ####A####.\n{few_shot_examples}\n{content}",
        "choice_nocot":      "The following is multiple-choice question. Please return only the correct answer and nothing else. Please enclose the final answer with two pairs of ####, for example: ####A####.\n{content}",
    },
    "chinese": {
        "fill_cot_few":      "以下是填空题，请逐步分析，并用两个连续的####括起最终答案，例如：####6####。\n{few_shot_examples}\n{content}",
        "fill_cot":          "以下是填空题，请逐步分析，并用两个连续的####括起最终答案，例如：####6####。\n{content}",
        "choice_cot_few":    "以下是选择题，请逐步分析，并用两个连续的####括起最终答案，例如：####A####。\n{few_shot_examples}\n{content}",
        "choice_cot":        "以下是选择题，请逐步分析，并用两个连续的####括起最终答案，例如：####A####。\n{content}",
        "fill_nocot_few":    "以下是填空题，请只返回正确答案，不要返回其他内容。请用两个连续的####括起最终答案，例如：####6####。\n{few_shot_examples}\n{content}",
        "fill_nocot":        "以下是填空题，请只返回正确答案，不要返回其他内容。请用两个连续的####括起最终答案，例如：####6####。\n{content}",
        "choice_nocot_few":  "以下是选择题，请只返回正确答案，不要返回其他内容。请用两个连续的####括起最终答案，例如：####A####。\n{few_shot_examples}\n{content}",
        "choice_nocot":      "以下是选择题，请只返回正确答案，不要返回其他内容。请用两个连续的####括起最终答案，例如：####A####。\n{content}",
    },
    "japanese": {
        "fill_cot_few":      "次の空欄補充問題を段階的に分析し、最終的な答えを####6####のように####で囲んでください。\n{few_shot_examples}\n{content}",
        "fill_cot":          "次の空欄補充問題を段階的に分析し、最終的な答えを####6####のように####で囲んでください。\n{content}",
        "choice_cot_few":    "次の選択問題を段階的に分析し、最終的な答えを####A####のように####で囲んでください。\n{few_shot_examples}\n{content}",
        "choice_cot":        "次の選択問題を段階的に分析し、最終的な答えを####A####のように####で囲んでください。\n{content}",
        "fill_nocot_few":    "次の空欄補充問題について、正しい答えのみを返し、他の内容は返さないでください。最終的な答えは####6####のように####で囲んでください。\n{few_shot_examples}\n{content}",
        "fill_nocot":        "次の空欄補充問題について、正しい答えのみを返し、他の内容は返さないでください。最終的な答えは####6####のように####で囲んでください。\n{content}",
        "choice_nocot_few":  "次の選択問題について、正しい答えのみを返し、他の内容は返さないでください。最終的な答えは####A####のように####で囲んでください。\n{few_shot_examples}\n{content}",
        "choice_nocot":      "次の選択問題について、正しい答えのみを返し、他の内容は返さないでください。最終的な答えは####A####のように####で囲んでください。\n{content}",
    },
    "russian": {
        "fill_cot_few":      "Ниже приведены задания на заполнение пропусков. Проанализируйте их поэтапно и заключите окончательный ответ в две пары ####, например: ####6####.\n{few_shot_examples}\n{content}",
        "fill_cot":          "Ниже приведены задания на заполнение пропусков. Проанализируйте их поэтапно и заключите окончательный ответ в две пары ####, например: ####6####.\n{content}",
        "choice_cot_few":    "Ниже приведены задания с выбором ответа. Проанализируйте их поэтапно и заключите окончательный ответ в две пары ####, например: ####A####.\n{few_shot_examples}\n{content}",
        "choice_cot":        "Ниже приведены задания с выбором ответа. Проанализируйте их поэтапно и заключите окончательный ответ в две пары ####, например: ####A####.\n{content}",
        "fill_nocot_few":    "Ниже приведены задания на заполнение пропусков. Пожалуйста, верните только правильный ответ, без лишних комментариев. Окончательный ответ заключите в две пары ####, например: ####6####.\n{few_shot_examples}\n{content}",
        "fill_nocot":        "Ниже приведены задания на заполнение пропусков. Пожалуйста, верните только правильный ответ, без лишних комментариев. Окончательный ответ заключите в две пары ####, например: ####6####.\n{content}",
        "choice_nocot_few":  "Ниже приведены задания с выбором ответа. Пожалуйста, верните только правильный ответ, без лишних комментариев. Окончательный ответ заключите в две пары ####, например: ####A####.\n{few_shot_examples}\n{content}",
        "choice_nocot":      "Ниже приведены задания с выбором ответа. Пожалуйста, верните только правильный ответ, без лишних комментариев. Окончательный ответ заключите в две пары ####, например: ####A####.\n{content}",
    },
    "arabic": {
        "fill_cot_few":      "الأسئلة التالية هي أسئلة فراغات. حللها خطوة بخطوة وضع الإجابة النهائية بين علامتي ####، مثلاً: ####6####.\n{few_shot_examples}\n{content}",
        "fill_cot":          "الأسئلة التالية هي أسئلة فراغات. حللها خطوة بخطوة وضع الإجابة النهائية بين علامتي ####، مثلاً: ####6####.\n{content}",
        "choice_cot_few":    "الأسئلة التالية هي أسئلة اختيار من متعدد. حللها خطوة بخطوة وضع الإجابة النهائية بين علامتي ####، مثلاً: ####A####.\n{few_shot_examples}\n{content}",
        "choice_cot":        "الأسئلة التالية هي أسئلة اختيار من متعدد. حللها خطوة بخطوة وضع الإجابة النهائية بين علامتي ####، مثلاً: ####A####.\n{content}",
        "fill_nocot_few":    "الأسئلة التالية هي أسئلة فراغات. يرجى إرجاع الإجابة الصحيحة فقط ولا شيء غيرها. ضع الإجابة النهائية بين علامتي ####، مثلاً: ####6####.\n{few_shot_examples}\n{content}",
        "fill_nocot":        "الأسئلة التالية هي أسئلة فراغات. يرجى إرجاع الإجابة الصحيحة فقط ولا شيء غيرها. ضع الإجابة النهائية بين علامتي ####، مثلاً: ####6####.\n{content}",
        "choice_nocot_few":  "الأسئلة التالية هي أسئلة اختيار من متعدد. يرجى إرجاع الإجابة الصحيحة فقط ولا شيء غيرها. ضع الإجابة النهائية بين علامتي ####، مثلاً: ####A####.\n{few_shot_examples}\n{content}",
        "choice_nocot":      "الأسئلة التالية هي أسئلة اختيار من متعدد. يرجى إرجاع الإجابة الصحيحة فقط ولا شيء غيرها. ضع الإجابة النهائية بين علامتي ####، مثلاً: ####A####.\n{content}",
    },
    "french": {
        "fill_cot_few":      "Les questions suivantes sont des questions à compléter. Analysez-les étape par étape et encadrez la réponse finale avec deux paires de ####, par exemple : ####6####.\n{few_shot_examples}\n{content}",
        "fill_cot":          "Les questions suivantes sont des questions à compléter. Analysez-les étape par étape et encadrez la réponse finale avec deux paires de ####, par exemple : ####6####.\n{content}",
        "choice_cot_few":    "Les questions suivantes sont des questions à choix multiples. Analysez-les étape par étape et encadrez la réponse finale avec deux paires de ####, par exemple : ####A####.\n{few_shot_examples}\n{content}",
        "choice_cot":        "Les questions suivantes sont des questions à choix multiples. Analysez-les étape par étape et encadrez la réponse finale avec deux paires de ####, par exemple : ####A####.\n{content}",
        "fill_nocot_few":    "Les questions suivantes sont des questions à compléter. Veuillez ne retourner que la bonne réponse et rien d’autre. Encadrez la réponse finale avec deux paires de ####, par exemple : ####6####.\n{few_shot_examples}\n{content}",
        "fill_nocot":        "Les questions suivantes sont des questions à compléter. Veuillez ne retourner que la bonne réponse et rien d’autre. Encadrez la réponse finale avec deux paires de ####, par exemple : ####6####.\n{content}",
        "choice_nocot_few":  "Les questions suivantes sont des questions à choix multiples. Veuillez ne retourner que la bonne réponse et rien d’autre. Encadrez la réponse finale avec deux paires de ####, par exemple : ####A####.\n{few_shot_examples}\n{content}",
        "choice_nocot":      "Les questions suivantes sont des questions à choix multiples. Veuillez ne retourner que la bonne réponse et rien d’autre. Encadrez la réponse finale avec deux paires de ####, par exemple : ####A####.\n{content}",
    }
}

# == 文件名映射 ==
language_map = {
    'alby': 'arabic',
    'ey': 'russian',
    'fy': 'french',
    'ry': 'japanese',
    'yy': 'english',
    'zw': 'chinese'
}

question_type_map = {
    0: 'choice',
    1: 'filling'
}


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

def call_deepseekv3_api(messages, args):
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
    
def call_qwen3_api(messages, args):
    try:
        response = qwen_client.chat.completions.create(
            model="qwen3-30b-a3b",
            messages=messages,
            temperature=args.temperature,
            top_p=args.top_p,
            presence_penalty=args.presence_penalty,
            max_tokens=args.max_tokens,
            stream=False,
            extra_body={"enable_thinking": False}
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 Qwen3 API 时出错: {e}")
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
    
def call_kimik2_api(messages, args):
    try:
        response = kimi_client.chat.completions.create(
            model="kimi-k2-0711-preview",
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
    
def call_kimiv1_api(messages, args):
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
        print(f"调用 MistralS API 时出错: {e}")
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
        print(f"调用 MistralL API 时出错: {e}")
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
    
def call_gemini_api(messages, args):
    try:
        response = gemini_client.chat.completions.create(
            model="gemini-2.0-flash-lite",
            messages=messages,
            temperature=args.temperature,
            top_p=args.top_p,
            presence_penalty=args.presence_penalty,
            max_tokens=args.max_tokens,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 Gemini API 时出错: {e}")
        return "API 调用失败"
    
def call_LLM_api(model, messages, args):
    if model == "doubao":
        return call_doubao_api(messages, args)
    elif model == "deepseekv3":
        return call_deepseekv3_api(messages, args)    
    elif model == "kimik2":
        return call_kimik2_api(messages, args)
    elif model == "kimiv1":
        return call_kimiv1_api(messages, args)
    elif model == "mistralS":
        return call_mistralS_api(messages, args)    
    elif model == "mistralM":
        return call_mistralM_api(messages, args)
    elif model == "mistralL":
        return call_mistralL_api(messages, args)
    elif model == "qwen":
        return call_qwen_api(messages, args)
    elif model == "qwen25": 
        return call_qwen25_api(messages, args)
    elif model == "qwen3":
        return call_qwen3_api(messages, args)
    elif model == "gpt35":
        return call_gpt35_api(messages, args)
    elif model == "gpt41":
        return call_gpt41_api(messages, args)
    elif model == "gemini": 
        return call_gemini_api(messages, args)
    
# == 筛选文件 ==
def select_csv_file(lang_str, question_type, question_tran, csv_dir):
    type_str = question_type_map.get(question_type, None)
    if lang_str is None or type_str is None:
        raise ValueError(f"未知language或question_type: {language}, {question_type}")

    files = os.listdir(csv_dir)
    filtered_files = []
    for fname in files:
        if lang_str in fname and type_str in fname:
            if question_tran == 0 and "adjusted" not in fname:
                filtered_files.append(fname)
            elif question_tran == 1 and "adjusted" in fname:
                filtered_files.append(fname)
    if not filtered_files:
        raise FileNotFoundError("未找到匹配的csv文件！")
    return os.path.join(csv_dir, filtered_files[0])

# == 提取模型答案 ==
def extract_answer_from_response(content):
    import re
    # 匹配 ####answer####
    m = re.search(r'####(.*?)####', content)
    if m:
        return m.group(1).strip()
    return content.strip()

# == few-shot内容读取 ==
def get_few_shot_examples(few_shot_file, filling, cot):
    examples = []
    with open(few_shot_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if filling == 1:
                if cot == 1:
                    example = (
                        f"question: {row[0]}\n"
                        f"{row[1]}\n"
                        f"####{row[2]}####"
                    )
                else:
                    example = (
                        f"question: {row[0]}\n"
                        f"####{row[2]}####"
                    )
            else:
                if cot == 1:
                    example = (
                        f"question: {row[0]}\n"
                        f"A: {row[3]}\n"
                        f"B: {row[4]}\n"
                        f"C: {row[5]}\n"
                        f"D: {row[6]}\n"
                        f"{row[1]}\n"
                        f"####{row[7]}####"
                    )
                else:
                    example = (
                        f"question: {row[0]}\n"
                        f"A: {row[3]}\n"
                        f"B: {row[4]}\n"
                        f"C: {row[5]}\n"
                        f"D: {row[6]}\n"
                        f"####{row[7]}####"
                    )
            examples.append(example)
            if len(examples) >= 5:
                break
    return "\n\n".join(examples)

def build_prompt(language, cot, few_shot, filling, few_shot_examples, row):
    if filling == 1:  # 填空
        if cot == 1:
            key = "fill_cot_few" if few_shot == 1 else "fill_cot"
        else:
            key = "fill_nocot_few" if few_shot == 1 else "fill_nocot"
        content = row[0]
    else:  # 选择
        if cot == 1:
            key = "choice_cot_few" if few_shot == 1 else "choice_cot"
        else:
            key = "choice_nocot_few" if few_shot == 1 else "choice_nocot"
        content = (
            f"question: {row[0]}\n"
            f"A: {row[1]}\n"
            f"B: {row[2]}\n"
            f"C: {row[3]}\n"
            f"D: {row[4]}"
        )

    prompt = PROMPT_TEMPLATES[language][key].format(
        few_shot_examples=few_shot_examples if few_shot == 1 else "",
        content=content
    )
    return prompt

# == 单轮测试 ==
def test_single_turn(index, input_file, language, few_shot_file, args, cot, few, filling):
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        all_rows = [row for row in reader if row and len(row) >= 2]

    total = len(all_rows)
    right = 0
    
    # few-shot拼接
    few_shot_examples = ""
    if few == 1:
        few_shot_examples = get_few_shot_examples(few_shot_file, filling, cot)

    row = all_rows[index-1]
    question = row[0]
    true_answer = row[1] if filling == 1 else row[5]  # 填空题取第2列，选择题取第6列
    prompt = build_prompt(language, cot, few, filling, few_shot_examples, row)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    # print(f"第{index}题 prompt:\n{prompt}\n")
    response = call_LLM_api(args.model, messages, args)
    answer = extract_answer_from_response(response)
    if answer == true_answer.strip():
        right = 1
    return response, right

# == multi-turn测试 ==
def test_multi_turn(index, input_file, language, few_shot_file, args, cot, few, filling):
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        all_rows = [row for row in reader if row and len(row) >= 2]  # 至少两列

    total = len(all_rows)
    right = 0
    # few-shot拼接
    few_shot_examples = ""
    if few == 1:
        few_shot_examples = get_few_shot_examples(few_shot_file, filling, cot)
        
    row1 = all_rows[index-1]
    row2 = all_rows[(index) % total]  # 循环到首行
    true_answer1 = row1[1] if filling == 1 else row1[5]  # 填空题取第2列，选择题取第6列
    true_answer2 = row2[1] if filling == 1 else row2[5]  # 填空题取第2列，选择题取第6列
    
    # 第一轮
    prompt1 = build_prompt(language, cot, few, filling, few_shot_examples, row1)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt1}
    ]
    # print(f"第{index}组 第一轮题目:\n{prompt1}\n")
    response1 = call_LLM_api(args.model, messages, args)

    # 第二轮
    prompt2 = build_prompt(language, cot, few, filling, few_shot_examples, row2)
    messages.append({"role": "assistant", "content": response1})  # assistant角色
    messages.append({"role": "user", "content": prompt2})  # 添加第二轮问题
    # print(f"第{index}组 第二轮题目:\n{prompt2}\n")
    response2 = call_LLM_api(args.model, messages, args)
    answer2 = extract_answer_from_response(response2)
    if answer2 == true_answer2.strip():
        right = 1
    return response2, right
    
def repair_answer(cfg, logfile, index):
    args.temperature = cfg.get('Temperature', args.temperature)
    args.top_p = cfg.get('top_p', args.top_p)
    args.presence_penalty = cfg.get('presence_penalty', args.presence_penalty)
    args.max_tokens = cfg.get('max_tokens', args.max_tokens)
    
    if "kimi" in args.model and args.temperature > 1.0:
        args.temperature = 1.0
    elif "qwen" in args.model and args.temperature > 1.9:
        args.temperature = 1.9
    elif "mistral" in args.model:
        if args.temperature > 1.5:
            args.temperature = 1.5
        elif args.temperature == 0.0:
            args.top_p = 1.0
            
    if args.model == "qwen3" and args.max_tokens > 16384:
        args.max_tokens = 16384
    elif args.model == "qwen25" and args.max_tokens > 8192:
        args.max_tokens = 8192
    elif "deepseek" in args.model and args.max_tokens > 8192:
        args.max_tokens = 8192
    
    language = language_map.get(cfg['language'], None)
    question_type = cfg['question_type']
    question_tran = cfg['question_tran']
    
    cot = cfg.get('cot', 0)
    few = cfg.get('few', 0)
    mul = cfg.get('mul', 0)

    # 选择文件
    try:
        test_file = select_csv_file(language, question_type, question_tran, args.csv_dir)
        few_shot_file = f"csv/few_shot_examples_{language}.csv"
        # print(f"选择测试文件: {test_file}")
    except Exception as e:
        print(f"文件选择失败: {e}")

    # 测试方法
    if mul:
        # print("采用multi-turn测试")
        answer, right = test_multi_turn(index, test_file, language, few_shot_file, args, cot=cot, few=few, filling=question_type)
    else:
        # print("采用单轮测试")
        answer, right = test_single_turn(index, test_file, language, few_shot_file, args, cot=cot, few=few, filling=question_type)
    return answer, right

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


def write_invalid_json(fout, logfile, idx, cfg, key):
    record = {"file": logfile, "idx": idx, "key": key, "cfg": cfg}
    fout.write(json.dumps(record, ensure_ascii=False) + "\n")
    fout.flush()

# == 写入日志函数 ==
def append_supplementary_log(supplementary_log_path, ori_file, cfg, idx, new_answer, new_right):
    record = {
        "file": ori_file,
        "idx": idx,
        "cfg": cfg,
        "new_answer": new_answer,
        "new_right": new_right
    }
    with open(supplementary_log_path, "a", encoding="utf-8") as sf:
        sf.write(json.dumps(record, ensure_ascii=False) + "\n")
        
def record_and_repair_invalid(supplementary_log_path, logfile, ori_file, block_lines, cfg, fout, key):
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

    save_odd = -1
    for idx, content in enumerate(answers, 1):
        if mul == 1:
            if len(content) < threshold and check_invalid(content):
                print("idx:", idx)
                if idx % 2 == 1:
                    save_odd = idx
                else:
                    if save_odd == idx - 1:
                        continue
                write_invalid_json(fout, logfile, int((idx+1) / 2), cfg, key)
                # new_answer, new_right = repair_answer(cfg, logfile, int((idx+1) / 2))
                # append_supplementary_log(supplementary_log_path, ori_file, cfg, int((idx+1) / 2), new_answer, new_right)                    
        else:
            if len(content) < threshold and check_invalid(content):
                write_invalid_json(fout, logfile, idx, cfg, key)
                # new_answer, new_right = repair_answer(cfg, logfile, idx)
                # append_supplementary_log(supplementary_log_path, ori_file, cfg, idx, new_answer, new_right)

def detect_invalid_answers(label):
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
    
    invalid_record_path = os.path.join("invalid_records", f"invalid_records_{label}.txt")
    supplementary_log_path = os.path.join("supplementary_logs", f"supplementary_log_{label}.txt")
    with open(invalid_record_path, "w", encoding="utf-8") as fout:
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
                current_key = None
                current_lines = []

                for line in lines:
                    m_cfg = key_cfg_pattern.search(line)
                    if m_cfg:
                        # 处理旧配置块（仅当匹配所有 key）
                        if current_cfg and current_lines:
                            if config_match(current_cfg, target_configs):
                                record_and_repair_invalid(supplementary_log_path, filepath, f"{folder}/{fname}", current_lines, current_cfg, fout, current_key)
                        # 更新新配置
                        try:
                            current_key = int(m_cfg.group(1))
                            current_cfg = ast.literal_eval(m_cfg.group(2))
                        except Exception as e:
                            print(f"[WARN] 配置解析失败: {e} → {line.strip()}")
                            current_key = None
                            current_cfg = None
                        current_lines = []
                        continue

                    if current_cfg is not None:
                        current_lines.append(line)

                # 文件结束时处理最后一块
                if current_cfg and current_lines:
                    if config_match(current_cfg, target_configs):
                        record_and_repair_invalid(supplementary_log_path, filepath, f"{folder}/{fname}", current_lines, current_cfg, fout, current_key)


# ===========================================================
# 主入口
# ===========================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="doubao")
    parser.add_argument("--csv_dir", type=str, default="csv")
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--top_p", type=float, default=1.0)
    parser.add_argument("--presence_penalty", type=float, default=0.0)
    parser.add_argument("--max_tokens", type=int, default=1024)
    parser.add_argument("--start", type=int, default=0, help="从第几个config开始测试，默认从头开始")
    parser.add_argument("--end", type=int, default=None)
    args = parser.parse_args()

    os.makedirs("invalid_records", exist_ok=True)
    os.makedirs("supplementary_logs", exist_ok=True)

    detect_invalid_answers(args.model)
