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
def test_single_turn(input_file, language, few_shot_file, args, cot, few, filling):
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        all_rows = [row for row in reader if row and len(row) >= 2]
    right_count = 0
    total = len(all_rows)
    
    # few-shot拼接
    few_shot_examples = ""
    if few == 1:
        few_shot_examples = get_few_shot_examples(few_shot_file, filling, cot)

    start_time = time.time()
    for i, row in enumerate(all_rows):
        question = row[0]
        answer = row[1] if filling == 1 else row[5]  # 填空题取第2列，选择题取第6列
        prompt = build_prompt(language, cot, few, filling, few_shot_examples, row)
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

# == multi-turn测试 ==
def test_multi_turn(input_file, language, few_shot_file, args, cot, few, filling):
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        all_rows = [row for row in reader if row and len(row) >= 2]  # 至少两列
    right_count1 = 0
    right_count2 = 0
    total = len(all_rows)
    
    # few-shot拼接
    few_shot_examples = ""
    if few == 1:
        few_shot_examples = get_few_shot_examples(few_shot_file, filling, cot)
        
    start_time = time.time()
    for i in range(total):
        row1 = all_rows[i]
        row2 = all_rows[(i + 1) % total]  # 循环到首行
        
        # 第一轮
        prompt1 = build_prompt(language, cot, few, filling, few_shot_examples, row1)
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt1}
        ]
        print(f"第{i+1}组 第一轮题目:\n{prompt1}\n")
        response1 = call_LLM_api(args.model, messages, args)
        true_answer1 = row1[1] if filling == 1 else row1[5]  # 填空题取第2列，选择题取第6列
        print(f"{args.model}回答: {response1} \n正确答案是: {true_answer1}\n")
        answer1 = extract_answer_from_response(response1)
        if answer1 == true_answer1.strip():
            right_count1 += 1

        # 第二轮
        prompt2 = build_prompt(language, cot, few, filling, few_shot_examples, row2)
        messages.append({"role": "assistant", "content": response1})  # assistant角色
        messages.append({"role": "user", "content": prompt2})  # 添加第二轮问题
        print(f"第{i+1}组 第二轮题目:\n{prompt2}\n")
        response2 = call_LLM_api(args.model, messages, args)
        true_answer2 = row2[1] if filling == 1 else row2[5]  # 填空题取第2列，选择题取第6列
        print(f"{args.model}回答: {response2} \n正确答案是: {true_answer2}\n")
        answer2 = extract_answer_from_response(response2)
        if answer2 == true_answer2.strip():
            right_count2 += 1

    end_time = time.time()
    total_time = end_time - start_time
    print(f"总题组数: {total}, 第一轮正确答案数: {right_count1}, 正确率: {right_count1 / total:.2%}，第二轮正确答案数: {right_count2}, 正确率: {right_count2 / total:.2%}, 总耗时: {total_time:.2f}秒")

if __name__ == "__main__":
    # == 通用参数解析 ==
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="doubao")
    parser.add_argument("--csv_dir", type=str, default="csv")
    parser.add_argument("--pkl_path", type=str, default="related_work_data.pkl")
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--top_p", type=float, default=1.0)
    parser.add_argument("--presence_penalty", type=float, default=0.0)
    parser.add_argument("--max_tokens", type=int, default=1024)
    parser.add_argument("--start", type=int, default=0, help="从第几个config开始测试，默认从头开始")
    parser.add_argument("--end", type=int, default=None)
    args = parser.parse_args()

    # == 读取pkl文件 ==
    with open(args.pkl_path, 'rb') as f:
        data = pickle.load(f)
    print("PKL内容如下：")
    print(data)
    # == 主流程 ==
    start_index = args.start
    end_index = args.end if args.end is not None else len(data)
    print(f"将从第 {start_index} 个配置开始测试。")
    for key, value in enumerate(tqdm(data[start_index:end_index], desc="采样测试进度", initial=start_index, total=len(data))):
        real_key = key + start_index
        print(f"处理key: {real_key}, 配置: {value}")

        # 根据value设置参数
        args.temperature = value.get('Temperature', args.temperature)
        args.top_p = value.get('top_p', args.top_p)
        args.presence_penalty = value.get('presence_penalty', args.presence_penalty)
        args.max_tokens = value.get('max_tokens', args.max_tokens)
        
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
        
        language = language_map.get(value['language'], None)
        question_type = value['question_type']
        question_tran = value['question_tran']
        
        cot = value.get('cot', 0)
        few = value.get('few', 0)
        mul = value.get('mul', 0)

        # 选择文件
        try:
            test_file = select_csv_file(language, question_type, question_tran, args.csv_dir)
            few_shot_file = f"csv/few_shot_examples_{language}.csv"
            print(f"选择测试文件: {test_file}")
        except Exception as e:
            print(f"文件选择失败: {e}")
            continue

        # 测试方法
        if mul:
            print("采用multi-turn测试")
            test_multi_turn(test_file, language, few_shot_file, args, cot=cot, few=few, filling=question_type)
        else:
            print("采用单轮测试")
            test_single_turn(test_file, language, few_shot_file, args, cot=cot, few=few, filling=question_type)

    print("全部测试完成！")