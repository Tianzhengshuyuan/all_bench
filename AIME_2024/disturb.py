import csv
import argparse
import os
import re
import time
import openai
from openai import OpenAI
from mistralai import Mistral
from fractions import Fraction
from sympy import sympify, E
from sympy.core.sympify import SympifyError
from volcenginesdkarkruntime import Ark

deepseek_client = OpenAI(api_key="sk-09da13b2c97948628523d042d6a02f06", base_url="https://api.deepseek.com")
qwen_client = OpenAI(api_key="sk-341becd932d743f2a750495a0f9f3ede", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
doubao_client = Ark(api_key="196b33be-8abb-4af3-9fba-6e266b2dd942")
kimi_client = OpenAI(api_key="sk-ODuizMlUC22phanBhvYz6dBjx2yrz7vhKhcjKnoIrYssThQo", base_url="https://api.moonshot.cn/v1")
mistral_client = Mistral(api_key="GYCQ8pMgX3E51NsmAjqrwI25zLZClHxo")

def call_deepseek_api(question, temperature=0):
    try:
        response = doubao_client.chat.completions.create(
            # model="deepseek-v3-250324", #deepseek-v3
            model="deepseek-v3-1-terminus",
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

def call_kimik2_api(question, temperature=0):
    try:
        response = kimi_client.chat.completions.create(
            model="kimi-k2-0711-preview",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            temperature=temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 kimi API 时出错: {e}")
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
            model="gpt-5",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            # temperature=temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 gpt API 时出错: {e}")
        return "❌" 
    
def call_doubao_api(question, temperature=0):
    """
    调用 doubao API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
    try:
        response = doubao_client.chat.completions.create(
            # model="doubao-1.5-pro-32k-250115",
            # model="doubao-seed-1-6-lite-251015",
            model="doubao-seed-1-6-thinking-250715",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            temperature=temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 doubao API 时出错: {e}")
        return "❌"
    
def call_qwen_api(question, temperature=0):
    try:
        response = qwen_client.chat.completions.create(
            # model="qwen-plus", 
            model="qwen3-max",
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
    
def call_mistral_api(question, temperature=0):
    """
    调用 doubao API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
    try:
        response = mistral_client.chat.completions.create(
            model="mistral-medium-latest",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            temperature=temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 mistral API 时出错: {e}")
        return "❌"
        
def get_output_filename(input_name, language):
    # 获取不带扩展名的文件主名
    base = os.path.splitext(os.path.basename(input_name))[0]
    # 语言全部小写，空格换成下划线
    lang = language.strip().replace(" ", "_").lower()
    return f"{lang}_{base}.csv"
    
def disturb(args):
    output_path = os.path.join(args.out_csv, get_output_filename(args.input, args.method))
    
    total_count = 0
    success_count = 0
    start_time = time.time()  # 记录开始时间
    # 读取输入 CSV
    with open(args.input, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            total_count += 1            
            if not row:  # 跳过空行
                continue
            if args.method == "disturb1":
                prompt = """示例：\n
                            Jen enters a lottery by picking $4$ distinct numbers from $S=\{1,2,3,\cdots,9,10\}.$ 
                            $4$ numbers are randomly chosen from $S.$ She wins a prize if at least two of her numbers were $2$ of the randomly chosen numbers, 
                            and wins the grand prize if all four of her numbers were the randomly chosen numbers. 
                            The probability of her winning the grand prize given that she won a prize is $\tfrac{m}{n}$ where $m$ and $n$ are relatively prime positive integers. Find $m+n$. \n
                            调整为：\n
                            The weather today seems quite pleasant, and it might be a great day for a picnic. 
                            Jen enters a lottery by picking $4$ distinct numbers from $S=\{1,2,3,\cdots,9,10\}.$ 
                            $4$ numbers are randomly chosen from $S.$ Also, there are some beautiful flowers blooming in the nearby park. She wins a prize if at least two of her numbers were $2$ of the randomly chosen numbers, 
                            and wins the grand prize if all four of her numbers were the randomly chosen numbers. 
                            The probability of her winning the grand prize given that she won a prize is $\tfrac{m}{n}$ where $m$ and $n$ are relatively prime positive integers. Find $m+n$. \n
                            请按照示例的方法，给下面的题目在随机的位置加入和题目完全无关的冗余语句，只添加，原题的内容不进行增删和修改：\n
                        """ + row[0]
            elif args.method == "disturb2":
                prompt = """示例：\n
                            Jen enters a lottery by picking $4$ distinct numbers from $S=\{1,2,3,\cdots,9,10\}.$ 
                            $4$ numbers are randomly chosen from $S.$ She wins a prize if at least two of her numbers were $2$ of the randomly chosen numbers, 
                            and wins the grand prize if all four of her numbers were the randomly chosen numbers. 
                            The probability of her winning the grand prize given that she won a prize is $\tfrac{m}{n}$ where $m$ and $n$ are relatively prime positive integers. Find $m+n$. \n
                            调整为：\n
                            Jen enters a lottery by picking $4$ distinct numbers from $S=\{1,2,3,\cdots,9,10\}.$ 
                            $4$ numbers are randomly chosen from $S.$ She wins a prize if at least two of her numbers were $2$ of the randomly chosen numbers, 
                            and wins the grand prize if all four of her numbers were the randomly chosen numbers. 
                            In probability theory, conditional probability measures the likelihood of an event occurring given that another event has already happened. 
                            The probability of her winning the grand prize given that she won a prize is $\tfrac{m}{n}$ where $m$ and $n$ are relatively prime positive integers. Find $m+n$.
                            请按照示例的方法，给下面的题目在随机的位置插入一条和题目相关的冗余语句，解释题目中的某个概念，只添加，原题的内容不进行增删和修改：\n
                        """ + row[0]
            elif args.method == "disturb3":
                # prompt = """示例：\n
                #             Jen enters a lottery by picking $4$ distinct numbers from $S=\{1,2,3,\cdots,9,10\}.$ 
                #             $4$ numbers are randomly chosen from $S.$ She wins a prize if at least two of her numbers were $2$ of the randomly chosen numbers, 
                #             and wins the grand prize if all four of her numbers were the randomly chosen numbers. 
                #             The probability of her winning the grand prize given that she won a prize is $\tfrac{m}{n}$ where $m$ and $n$ are relatively prime positive integers. Find $m+n$. \n
                #             调整为：\n
                #             Jen enters a lottery by picking $4$ distinct numbers from $S=\{1,2,3,\cdots,9,10\}.$ 
                #             $4$ numbers are randomly chosen from $S.$ She wins a prize if at least two of her numbers were $2$ of the randomly chosen numbers, 
                #             and wins the grand prize if all four of her numbers were the randomly chosen numbers. 
                #             The probability of her winning the grand prize given that she won a prize is $\tfrac{m}{n}$ where $m$ and $n$ are relatively prime positive integers. 
                #             The numbers Jen picks at the beginning might affect her probability of winning the grand prize. Find $m+n$.
                            
                #             请按照类似上面示例的方法，在下面题目的随机位置插入一条冗余语句，诱导答题者往错误的方向思考题目解法，从而难以解题。返回增加冗余后的题目，原题的内容不进行增删和修改，不要返回任何其他内容\n
                #         """ + "题目是：\n" + row[0] + "\n这道题目的正确解法如下，诱导错误思路的冗余语句要绕开这些思路：\n" + row[1]         
                prompt = """
                【任务目标】
                你需要在一道题目文本中，插入一条“迷惑性冗余语句”，让读者朝错误方向思考或解题。插入后的题目仍然具有完整、自然的逻辑结构。

                【注意事项】
                1. 不允许删改原题内容，除插入的冗余语句外，题目的其他部分必须保持完全一致。
                2. 插入位置要合理自然，冗余语句只能插在“相关概念或符号”出现之后，不可提前引用尚未定义的概念；
                3. 冗余语句必须引导读者往错误方向思考或解题，但不能显露为“引导错误”或“干扰信息”，不得出现诸如“这是错误的思路”或“注意不要被误导”之类的说明。
                4. 冗余语句不得直接或间接表达正确解法、正确分析方法或正确结果。
                5. 冗余语句的内容应与原题主题相关，看似有助于解题，但其实是干扰的——例如常见但错误的推理方式、错误的假设、易混淆的数理关系等。
                6. 你的输出只包含“加上冗余语句后的题目完整文本”，不得包含任何其他信息。

                【参考示例】
                原题：
                Jen enters a lottery by picking $4$ distinct numbers from $S=\\{1,2,3,\\cdots,9,10\\}.$ 
                $4$ numbers are randomly chosen from $S.$ She wins a prize if at least two of her numbers were among the randomly chosen numbers, 
                and wins the grand prize if all four of her numbers were the randomly chosen numbers. 
                The probability of her winning the grand prize given that she won a prize is $\\tfrac{m}{n}$ where $m$ and $n$ are relatively prime positive integers. Find $m+n$.

                调整后（插入干扰性冗余语句）：
                Jen enters a lottery by picking $4$ distinct numbers from $S=\\{1,2,3,\\cdots,9,10\\}.$ 
                Some people believe that choosing consecutive numbers increases the chance of matching more numbers, though this isn't proven. 
                $4$ numbers are randomly chosen from $S.$ She wins a prize if at least two of her numbers were among the randomly chosen numbers, 
                and wins the grand prize if all four of her numbers were the randomly chosen numbers. 
                The probability of her winning the grand prize given that she won a prize is $\\tfrac{m}{n}$ where $m$ and $n$ are relatively prime positive integers. 
                Find $m+n$.
                
                你的生成目标是模仿上面的“调整后”效果。

                【待处理题目】
                题目是：
                """ + row[0] + """

                这道题目的正确解法如下（用于避开这些思路，不能在冗余语句中体现或暗示下列方法）：
                """ + row[1] + """
                """   
            print(f"原文:\n{row[0]}\n")
            if args.model == "deepseek":
                print("调用 deepseek API 进行转换...")
                disturbed_question = call_deepseek_api(prompt, temperature=args.temperature)
            elif args.model == "gpt":
                print("调用 gpt API 进行转换...")
                disturbed_question = call_gpt_api(prompt, temperature=args.temperature)
            elif args.model == "mistral":
                print("调用 mistral API 进行转换...")
                disturbed_question = call_mistral_api(prompt, temperature=args.temperature)
            elif args.model == "doubao":
                print("调用 doubao API 进行转换...")
                disturbed_question = call_doubao_api(prompt, temperature=args.temperature)
            elif args.model == "qwen":
                print("调用 Qwen API 进行转换...")
                disturbed_question = call_qwen_api(prompt, temperature=args.temperature)
            elif args.model == "kimi":
                print("调用 kimi API 进行转换...")
                disturbed_question = call_kimik2_api(prompt, temperature=args.temperature)
            print(f"转换后的题目:\n{disturbed_question}\n")
            success_count += 1
            if args.method == "disturb3":
                writer.writerow([disturbed_question, row[2]])
            else:
                writer.writerow([disturbed_question, row[1]])
    end_time = time.time()  # 记录结束时间
    total_time = end_time - start_time
    avg_time = total_time / total_count if total_count > 0 else 0
            
    print(f"转换结果已保存到: {output_path}，总共 {total_count} 行，成功转换 {success_count} 行，平均每行耗时 {avg_time:.2f} 秒")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量调用 DeepSeek 翻译")
    parser.add_argument('--input', required=True, help="输入 CSV 文件名")
    parser.add_argument('--out_csv', default='./csv', help="输出CSV 文件所在文件夹")
    parser.add_argument('--temperature', type=float, default=0.2, help="API 回答多样性，默认 0.2")
    parser.add_argument('--model', type=str, default="deepseek", help="使用的模型，如gpt、deepseek、kimi、qwen")
    parser.add_argument('--method', type=str, default="disturb1", help="使用的方法名称，用于输出文件命名")
    args = parser.parse_args()

    disturb(args)