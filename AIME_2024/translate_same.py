import csv
import argparse
import os
import re
import time
import openai
from volcenginesdkarkruntime import Ark
from openai import OpenAI
from fractions import Fraction
from sympy import sympify, E
from sympy.core.sympify import SympifyError

deepseek_client = OpenAI(api_key="sk-09da13b2c97948628523d042d6a02f06", base_url="https://api.deepseek.com")
kimi_client = OpenAI(api_key="sk-ODuizMlUC22phanBhvYz6dBjx2yrz7vhKhcjKnoIrYssThQo", base_url="https://api.moonshot.cn/v1")
qwen_client = OpenAI(api_key="sk-e6cfbb89c5f642aa9c0342974158fb96", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
doubao_client = Ark(api_key="196b33be-8abb-4af3-9fba-6e266b2dd942")

    
def call_deepseek_api(question, temperature=0):
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
            temperature=temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 DeepSeek API 时出错: {e}")
        return "❌"

# == API 调用 ==
def call_doubao_api(question, temperature=0):
    try:
        response = doubao_client.chat.completions.create(
            model="doubao-1-5-pro-32k-250115",  # 注意模型名称拼写
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            temperature=temperature,
            stream=False,
        )
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"调用 豆包 API 时出错: {e}")
        return "API 调用失败"
    
def call_gpt_api(question, temperature=0):
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
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            temperature=temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 gpt API 时出错: {e}")
        return "❌" 
    
def call_kimi_api(question, temperature=0):
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
            temperature=temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 Kimi API 时出错: {e}")
        return "❌"
    
def   call_qwen_api(question, temperature=0):
    try:
        response = qwen_client.chat.completions.create(
            model="qwen-plus", 
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': question},
            ],
            temperature=temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 Qwen API 时出错: {e}")
        return "❌"
   
def parse_translation(translation: str):
    if not isinstance(translation, str):
        return str(translation), ""

    text = translation.strip()

    # 按 '####' 分割
    parts = text.split("####")
    # 例如 "####题目####答案####" -> ["", "题目", "答案", ""]
    # 过滤掉纯空白部分
    parts = [p.strip() for p in parts if p.strip() != ""]

    if len(parts) >= 2:
        question = parts[0]
        answer = parts[1]
        return question, answer
    elif len(parts) == 1:
        # 只有一个内容，认为是题目
        return parts[0], ""
    else:
        # 完全无法解析
        return text, ""
 
def parse_choice_translation(translation):

    pattern = re.compile(
        r"^(.*?)\s*\nA\s*[:：]\s*(.*?)\s*\nB\s*[:：]\s*(.*?)\s*\nC\s*[:：]\s*(.*?)\s*\nD\s*[:：]\s*(.*)$",
        re.DOTALL
    )
    m = pattern.match(translation.strip())
    if m:
        return [m.group(i).strip() for i in range(1, 6)]
    else:
        print("解析翻译结果时出错")
        return None
     
def get_output_filename(input_name, language):
    # 获取不带扩展名的文件主名
    base = os.path.splitext(os.path.basename(input_name))[0]
    # 语言全部小写，空格换成下划线
    lang = language.strip().replace(" ", "_").lower()
    return f"{base}_{lang}.csv"
    
def translate(args):
    output_path = os.path.join(args.out_csv, get_output_filename(args.input, args.language))
    total_count = 0
    success_count = 0
    start_time = time.time()  # 记录开始时间
    
    # 如果设置了 line 参数，只修改输出文件的指定行
    if args.line is not None:
        # 读取输入文件获取原始问题
        with open(args.input, 'r', encoding='utf-8') as infile:
            input_rows = list(csv.reader(infile))
        
        # 检查输出文件是否存在
        if not os.path.exists(output_path):
            print(f"错误: 输出文件 {output_path} 不存在，请先运行完整翻译")
            return
        
        # 读取输出文件的所有行
        with open(output_path, 'r', encoding='utf-8') as outfile:
            output_rows = list(csv.reader(outfile))
        
        # 检查行号是否有效
        if args.line < 1 or args.line > len(input_rows):
            print(f"错误: 行号 {args.line} 超出范围 (1-{len(input_rows)})")
            return
        
        # 获取要翻译的行（从输入文件）
        row = input_rows[args.line - 1]
        if not row or row[0] == "x":
            print(f"警告: 第 {args.line} 行是空行或特殊行，跳过")
            return
        
        # 构建翻译文本
        text = (
            f"问题：{row[0]}\n"
            f"A: {row[1]}\n"
            f"B: {row[2]}\n"
            f"C: {row[3]}\n"
            f"D: {row[4]}\n"
        )
        prompt = f"请把下面的选择题翻译成 {args.language}. 不要翻译开头的\"问题\"标识和选择题的四个选项标识 A、B、C、D，只翻译问题的具体内容以及四个选项的具体内容。只翻译，不要返回任何其他内容 \n{text}"
        
        # 调用 API 翻译
        if args.model == "qwen":
            print("调用 Qwen API 进行翻译...")
            translation = call_qwen_api(prompt, temperature=args.temperature)
        elif args.model == "doubao":
            print("调用 豆包 API 进行翻译...")
            translation = call_doubao_api(prompt, temperature=args.temperature)
        else:
            print("调用 DeepSeek API 进行翻译...")
            translation = call_deepseek_api(prompt, temperature=args.temperature)
        
        print(f"问题翻译:\n{translation}\n")
        parsed = parse_choice_translation(translation)
        
        if parsed is None:
            print(f"错误: 无法解析翻译结果，跳过该行")
            return
        
        # 更新输出文件的指定行
        if args.line <= len(output_rows):
            output_rows[args.line - 1] = [row[0], parsed[1], parsed[2], parsed[3], parsed[4], row[5] if len(row) > 5 else ""]
        else:
            # 如果输出文件行数不够，补充到指定行
            while len(output_rows) < args.line - 1:
                output_rows.append([])
            output_rows.append([row[0], parsed[1], parsed[2], parsed[3], parsed[4], row[5] if len(row) > 5 else ""])
        
        # 写回输出文件
        with open(output_path, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(output_rows)
        
        print(f"已更新输出文件 {output_path} 的第 {args.line} 行")
        return
    
    # 原来的逻辑：处理所有行
    # 读取输入 CSV
    with open(args.input, 'r', encoding='utf-8') as infile, \
         open(args.original, 'r', encoding='utf-8') as orifile, \
         open(output_path, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        ori_reader = csv.reader(orifile)
        writer = csv.writer(outfile)

        index = 1
        for i, (row, ori_row) in enumerate(zip(reader, ori_reader)): 
            total_count += 1            
            if not row:  # 跳过空行
                continue
            if row[0] == "x":
                writer.writerow([row[0], row[1]])
                continue
            # text = (
            #     f"问题：{row[0]}\n"
            #     f"A: {row[1]}\n"
            #     f"B: {row[2]}\n"
            #     f"C: {row[3]}\n"
            #     f"D: {row[4]}\n"
            # )
            # prompt = f"{row[0]}\n请把上面的内容翻译为 {args.language}。保留下面这个部分翻译版本中的全部内容，只新增下面这个翻译中不存在的部分到相应位置：\n{ori_row[0]}\n只翻译，不要返回任何其他信息"
            # prompt = f"{row[0]}\n请把上面的内容转换为 {args.language}。保留下面这个翻译版本中的全部内容，只改变与之不同的数字：\n{ori_row[0]}\n只转换，不要返回任何其他信息"
            prompt = f"{row[0]}\n请把上面的内容翻译为 {args.language}。只翻译，不要返回任何其他信息"
            # prompt = f"Question:{row[0]}\nAnswer:{row[1]}\n请把上面的题目和答案的内容均翻译为 {args.language}，不要忘记翻译答案，翻译后的版本不要包含"问题"、"答案"字样。只翻译，不要返回任何其他信息。如果题目是填空题，不要用正确答案填充题目，保留题目原来的形式。最终结果使用####隔开，例如：####指数函数 $ y = a^x $ 与对数函数 $ y = \log_a x $ 的图像关于哪条直线对称？####y=x####"
            # prompt = f"请把下面的选择题翻译成 {args.language}. 不要翻译开头的\"问题\"标识和选择题的四个选项标识 A、B、C、D，只翻译问题的具体内容以及四个选项的具体内容。只翻译，不要返回任何其他内容 \n{text}"
            
            if args.model == "qwen":
                print("调用 Qwen API 进行翻译...")
                translation = call_qwen_api(prompt, temperature=args.temperature)
            elif args.model == "doubao":
                print("调用 豆包 API 进行翻译...")
                translation = call_doubao_api(prompt, temperature=args.temperature)
            else:
                print("调用 DeepSeek API 进行翻译...")
                translation = call_deepseek_api(prompt, temperature=args.temperature)
            print(f"问题翻译:\n{translation}\n")
            # question_parsed, answer_parsed = parse_translation(translation)
            # parsed = parse_choice_translation(translation)

            success_count += 1
            writer.writerow([translation, row[1]])
            # writer.writerow([row[0], parsed[1], parsed[2], parsed[3], parsed[4], row[5]])
            index += 1
            
    end_time = time.time()  # 记录结束时间
    total_time = end_time - start_time
    avg_time = total_time / total_count if total_count > 0 else 0
            
    print(f"翻译结果已保存到: {output_path}，总共 {total_count} 行，成功翻译 {success_count} 行，平均每行耗时 {avg_time:.2f} 秒")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量调用 DeepSeek 翻译")
    parser.add_argument('--input', required=True, help="输入 CSV 文件名")
    parser.add_argument('--original', required=True, help="对应的MES文件")
    parser.add_argument('--out_csv', default='./csv', help="输出CSV 文件所在文件夹")
    parser.add_argument('--language', required=True, help="目标语言，如 French, German, Japanese 等")
    parser.add_argument('--temperature', type=float, default=0.2, help="API 回答多样性，默认 0.2")
    parser.add_argument('--model', type=str, default="deepseek", help="使用的模型，如gpt、deepseek、kimi、qwen")
    parser.add_argument('--line', type=int, default=None, help="专门翻译某行")
    args = parser.parse_args()

    translate(args)