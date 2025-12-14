import os
import csv
import time
import openai
import textwrap
import argparse
import re
import subprocess
import tempfile
import ast
import json
import random
import datetime
from openai import OpenAI
from mistralai import Mistral
from dataclasses import dataclass
from volcenginesdkarkruntime import Ark
from typing import List, Dict, Optional, Literal, Tuple, Any


deepseek_client = OpenAI(api_key="sk-09da13b2c97948628523d042d6a02f06", base_url="https://api.deepseek.com")
qwen_client = OpenAI(api_key="sk-b1c771fc24dd4cb89653163a74bf9e43", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
doubao_client = Ark(api_key="196b33be-8abb-4af3-9fba-6e266b2dd942")
kimi_client = OpenAI(api_key="sk-ODuizMlUC22phanBhvYz6dBjx2yrz7vhKhcjKnoIrYssThQo", base_url="https://api.moonshot.cn/v1")
mistral_client = Mistral(api_key="Wc1s1rVoW5TzceucND85yQoF4urCvO5f")

ModelName = Literal["deepseek", "qwen", "doubao", "kimi", "mistral", "gpt"]

# 全局默认模型选择（优先级低于下方细粒度配置）
DEFAULT_STAGE_MODEL = {
    "analyzer": "deepseek",
    "analogical_fallback": "qwen",
    "redundancy": "doubao",
    "novel": "kimi",
}

# AnalogicalTransformer 内部不同子步骤可各自指定模型
DEFAULT_ROLE_MODEL = {
    "extract": "doubao_1_5_pro_32k",     # 知识点提取
    "analysis": "doubao_1_5_pro_32k",    # 可逆条件分析（analogical-3）
    "codegen": "gpt5", # 代码生成
    "check": "mistral_medium",    # 硬编码检查
    "refine": "gpt5",  # 代码精炼
    "variant": "gpt5",     # 数字/条件变体生成
    "range": "gpt5",  # 变量取值范围确定
}


# 统一 LLMClient 封装
class LLMClient:
    def __init__(self, model_name: ModelName, temperature: float = 0.2):
        self.model_name = model_name
        self.temperature = temperature

    def chat(self, prompt: str, system: str = "You are a helpful assistant.") -> str:
        if self.model_name == "deepseek_v3":
            return self._call_deepseek_v3(prompt, system)
        elif self.model_name == "deepseek_v3_2":
            return self._call_deepseek_v3_2(prompt, system)
        elif self.model_name == "deepseek_r1":
            return self._call_deepseek_r1(prompt, system)
        elif self.model_name == "qwen_max":
            return self._call_qwen_max(prompt, system)
        elif self.model_name == "doubao_seed_thinking":
            return self._call_doubao_seed_thinking(prompt, system)
        elif self.model_name == "doubao_seed":
            return self._call_doubao_seed(prompt, system)
        elif self.model_name == "doubao_1_5_thinking_pro":
            return self._call_doubao_1_5_thinking_pro(prompt, system)
        elif self.model_name == "doubao_1_5_pro_32k":
            return self._call_doubao_1_5_pro_32k(prompt, system)
        elif self.model_name == "kimi_k2":
            return self._call_kimi_k2(prompt, system)
        elif self.model_name == "kimi_k2_thinking":
            return self._call_kimi_k2_thinking(prompt, system)
        elif self.model_name == "mistral_medium":
            return self._call_mistral_medium(prompt, system)
        elif self.model_name == "mistral_large":
            return self._call_mistral_large(prompt, system)
        elif self.model_name == "mistral_codestral":
            return self._call_mistral_codestral(prompt, system)
        elif self.model_name == "gpt5":
            return self._call_gpt5(prompt, system)
        elif self.model_name == "gpt4_1":
            return self._call_gpt4_1(prompt, system)
        else:
            raise ValueError(f"Unknown model_name: {self.model_name}")

    def _call_deepseek_v3(self, question: str, system: str) -> str:
        try:
            resp = doubao_client.chat.completions.create(
                model="deepseek-v3-250324",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": question},
                ],
                temperature=self.temperature,
                stream=False
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"调用 DeepSeek V3 API 时出错: {e}")
            return "❌"
    
    def _call_deepseek_v3_2(self, question: str, system: str) -> str:
        # https://console.volcengine.com/ark/region:ark+cn-beijing/model/detail?Id=deepseek-v3-2
        try:
            resp = doubao_client.chat.completions.create(
                model="deepseek-v3-2-251201",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": question},
                ],
                temperature=self.temperature,
                stream=False
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"调用 DeepSeek V3.2 API 时出错: {e}")
            return "❌"

    def _call_deepseek_r1(self, question: str, system: str) -> str:
        # https://console.volcengine.com/ark/region:ark+cn-beijing/model/detail?Id=deepseek-r1
        try:
            resp = doubao_client.chat.completions.create(
                model="deepseek-r1-251201",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": question},
                ],
                temperature=self.temperature,
                stream=False
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"调用 DeepSeek R1 API 时出错: {e}")
            return "❌"
        
    def _call_kimi_k2(self, question: str, system: str) -> str:
        # https://platform.moonshot.cn/docs/pricing/chat#%E4%BA%A7%E5%93%81%E5%AE%9A%E4%BB%B7
        try:
            resp = kimi_client.chat.completions.create(
                model="kimi-k2-0905-preview",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": question},
                ],
                temperature=self.temperature,
                stream=False
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"调用 Kimi K2 API 时出错: {e}")
            return "❌"
        
    def _call_kimi_k2_thinking(self, question: str, system: str) -> str:
        # https://platform.moonshot.cn/docs/pricing/chat#%E4%BA%A7%E5%93%81%E5%AE%9A%E4%BB%B7
        try:
            resp = kimi_client.chat.completions.create(
                model="kimi-k2-thinking",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": question},
                ],
                temperature=self.temperature,
                stream=False
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"调用 Kimi K2 Thinking API 时出错: {e}")
            return "❌"

    def _call_gpt5(self, question: str, system: str) -> str:
        try:
            os.environ["HTTP_PROXY"] = "http://localhost:7890"
            os.environ["HTTPS_PROXY"] = "http://localhost:7890"
            openai.api_key = os.getenv("OPENAI_API_KEY")
            resp = openai.chat.completions.create(
                model="gpt-5",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": question},
                ],
                stream=False
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"调用 GPT 5 API 时出错: {e}")
            return "❌"
    
    def _call_gpt4_1(self, question: str, system: str) -> str:
        try:
            os.environ["HTTP_PROXY"] = "http://localhost:7890"
            os.environ["HTTPS_PROXY"] = "http://localhost:7890"
            openai.api_key = os.getenv("OPENAI_API_KEY")
            resp = openai.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": question},
                ],
                stream=False
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"调用 GPT 4.1 API 时出错: {e}")
            return "❌"

    def _call_doubao_seed_thinking(self, question: str, system: str) -> str:
        # https://console.volcengine.com/ark/region:ark+cn-beijing/model/detail?Id=doubao-seed-1-6-thinking
        try:
            resp = doubao_client.chat.completions.create(
                model="doubao-seed-1-6-thinking-250715",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": question},
                ],
                temperature=self.temperature,
                stream=False
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"调用 Doubao Seed Thinking API 时出错: {e}")
            return "❌"

    def _call_doubao_seed(self, question: str, system: str) -> str:
        # https://console.volcengine.com/ark/region:ark+cn-beijing/model/detail?Id=doubao-seed-1-6try:
        try:
            resp = doubao_client.chat.completions.create(
                model="doubao-seed-1-6-251015",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": question},
                ],
                temperature=self.temperature,
                stream=False
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"调用 Doubao Seed API 时出错: {e}")
            return "❌"

    def _call_doubao_1_5_thinking_pro(self, question: str, system: str) -> str:
        # https://console.volcengine.com/ark/region:ark+cn-beijing/model/detail?Id=doubao-1-5-thinking-pro
        try:
            resp = doubao_client.chat.completions.create(
                model="doubao-1-5-thinking-pro-250415",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": question},
                ],
                temperature=self.temperature,
                stream=False
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"调用 Doubao-1.5-thinking-pro API 时出错: {e}")
            return "❌"
        
    def _call_doubao_1_5_pro_32k(self, question: str, system: str) -> str:
        # https://console.volcengine.com/ark/region:ark+cn-beijing/model/detail?Id=doubao-1-5-pro-32k
        try:
            resp = doubao_client.chat.completions.create(
                model="doubao-1-5-pro-32k-250115",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": question},
                ],
                temperature=self.temperature,
                stream=False
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"调用 Doubao-1.5-pro-32k API 时出错: {e}")
            return "❌"

    def _call_qwen_max(self, question: str, system: str) -> str:
        try:
            resp = qwen_client.chat.completions.create(
                model="qwen3-max",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": question},
                ],
                temperature=self.temperature,
                stream=False
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"调用 Qwen API 时出错: {e}")
            return "❌"

    def _call_mistral_medium(self, question: str, system: str) -> str:
        try:
            resp = mistral_client.chat.complete(
                model="mistral-medium-latest",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": question},
                ],
                temperature=self.temperature,
                stream=False
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"调用 Mistral API 时出错: {e}")
            return "❌"
    
    def _call_mistral_large(self, question: str, system: str) -> str:
        try:
            resp = mistral_client.chat.complete(
                model="mistral-large-latest",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": question},
                ],
                temperature=self.temperature,
                stream=False
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"调用 Mistral Large API 时出错: {e}")
            return "❌"
        
    def _call_mistral_codestral(self, question: str, system: str) -> str:
        try:
            resp = mistral_client.chat.complete(
                model="codestral-2508",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": question},
                ],
                temperature=self.temperature,
                stream=False
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"调用 Mistral Codestral API 时出错: {e}")
            return "❌"


# 数据结构
@dataclass
class ProblemItem:
    original_question: str
    solution: str = ""
    true_answer: str = ""
    augmented_question: str = ""
    augmented_true_answer: str = ""
    method_used: str = ""
    analogical_mapping_note: str = ""
    transformed_question: str = ""


class ProblemAnalyzer:
    """可选：题目分析模块（目前不强制使用，只用于留下结构位）"""

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def analyze(self, item: ProblemItem) -> ProblemItem:
        prompt = textwrap.dedent(f"""
            你是一个数学教育专家，负责对竞赛题目进行结构化分析。

            请阅读下面的题目和（可选的）解析，提取以下信息：
            1. 主要涉及的知识点（用英文关键词列表形式给出，如 ["probability", "conditional probability"]）。
            2. 题目大致难度（easy / medium / hard 三选一）。
            3. 推理类型（如 "combinatorics", "geometry", "algebra", "number theory", "calculus", "functional equation" 等）。

            题目：
            {item.original_question}

            解析（如有）：
            {item.solution}

            请以 JSON 格式输出，字段名为：knowledge_tags, difficulty, reasoning_type。不要输出多余文字。
            """)
        resp = self.llm.chat(prompt)
        item.knowledge_tags = resp
        return item


class RedundancyInjector:
    """
    负责 analogical-1 中的三种冗余方式：
    method 1 -> disturb1
    method 2 -> disturb2
    method 3 -> disturb3
    """
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def inject(self, item: ProblemItem, method_num: str) -> ProblemItem:
        base_question = item.original_question  
        solution = item.solution

        if method_num == "1":
            # analogical-1 / disturb1：加入无关冗余语句
            prompt = textwrap.dedent("""
                【示例】
                Jen enters a lottery by picking $4$ distinct numbers from $S=\{1,2,3,\cdots,9,10\}.$ 
                $4$ numbers are randomly chosen from $S.$ She wins a prize if at least two of her numbers were $2$ of the randomly chosen numbers, 
                and wins the grand prize if all four of her numbers were the randomly chosen numbers. 
                The probability of her winning the grand prize given that she won a prize is $\tfrac{m}{n}$ where $m$ and $n$ are relatively prime positive integers. Find $m+n$. 
                调整为：
                The weather today seems quite pleasant, and it might be a great day for a picnic. 
                Jen enters a lottery by picking $4$ distinct numbers from $S=\{1,2,3,\cdots,9,10\}.$ 
                $4$ numbers are randomly chosen from $S.$ Also, there are some beautiful flowers blooming in the nearby park. She wins a prize if at least two of her numbers were $2$ of the randomly chosen numbers, 
                and wins the grand prize if all four of her numbers were the randomly chosen numbers. 
                The probability of her winning the grand prize given that she won a prize is $\tfrac{m}{n}$ where $m$ and $n$ are relatively prime positive integers. Find $m+n$. 
                
                请按照示例的方法，给下面的题目在随机的位置加入和题目完全无关的冗余语句，只添加，原题的内容不进行增删和修改：
                """) + base_question
            tag = "analogical-1-disturb1"

        elif method_num == "2":
            # analogical-1 / disturb2：插入相关概念解释冗余
            prompt = textwrap.dedent("""
                【示例】
                Jen enters a lottery by picking $4$ distinct numbers from $S=\{1,2,3,\cdots,9,10\}.$ 
                $4$ numbers are randomly chosen from $S.$ She wins a prize if at least two of her numbers were $2$ of the randomly chosen numbers, 
                and wins the grand prize if all four of her numbers were the randomly chosen numbers. 
                The probability of her winning the grand prize given that she won a prize is $\tfrac{m}{n}$ where $m$ and $n$ are relatively prime positive integers. Find $m+n$. 
                调整为：
                Jen enters a lottery by picking $4$ distinct numbers from $S=\{1,2,3,\cdots,9,10\}.$ 
                $4$ numbers are randomly chosen from $S.$ She wins a prize if at least two of her numbers were $2$ of the randomly chosen numbers, 
                and wins the grand prize if all four of her numbers were the randomly chosen numbers. 
                In probability theory, conditional probability measures the likelihood of an event occurring given that another event has already happened. 
                The probability of her winning the grand prize given that she won a prize is $\tfrac{m}{n}$ where $m$ and $n$ are relatively prime positive integers. Find $m+n$.
                
                请按照示例的方法，给下面的题目在随机的位置插入一条和题目相关的冗余语句，解释题目中的某个概念，只添加，原题的内容不进行增删和修改：
                """) + base_question
            tag = "analogical-1-disturb2"

        elif method_num == "3":
            # analogical-1 / disturb3：引导错误方向的冗余
            prompt = textwrap.dedent("""
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
                """) + base_question + "\n这道题目的正确解法如下（用于避开这些思路，不能在冗余语句中体现或暗示下列方法）：\n" + solution
            tag = "analogical-1-disturb3"
        else:
            raise ValueError(f"RedundancyInjector: 不支持的 method_num={method_num}")
        print("prompt: ", prompt)
        response = self.llm.chat(prompt)
        item.augmented_question = response.strip()
        item.method_used = tag
        return item


class AnalogicalTransformer:
    """类比变换模块：基于代码生成和验证的 analogical-2 和 analogical-3"""

    def __init__(self, llm: LLMClient):
        self.llm = llm
        self.code_dir = "./code"
        self.current_question_id = None  # 当前处理的题目ID
        if self.code_dir:
            os.makedirs(self.code_dir, exist_ok=True)
        # 公式库——按知识点索引
        self.formula_library = {
            "probability": ["P(A|B) = \\frac{P(A \\cap B)}{P(B)}  # 条件概率, A|B表示B发生下A发生", "P(A \\cup B) = P(A) + P(B) - P(A \\cap B)  # 并集概率, A∪B表示A或B发生", "P(A') = 1 - P(A)  # 补集概率, A'表示A不发生", "P(A \\cap B) = P(A|B) \\cdot P(B)  # 交集概率, A∩B表示A和B同时发生"], #概率
            "probability theory": ["P(A|B) = \\frac{P(A \\cap B)}{P(B)}  # 条件概率", "P(A \\cup B) = P(A) + P(B) - P(A \\cap B)  # 并集概率", "P(A') = 1 - P(A)  # 补集概率", "P(A \\cap B) = P(A) \\cdot P(B|A)  # 乘法公式", "E[X] = \\sum x_i P(x_i)  # 期望值, X为随机变量, x_i为取值"], # 概率论
            "discrete probability": ["P(X=k)  # 离散随机变量X取值为k的概率", "E[X] = \\sum_{i} x_i P(X=x_i)  # 期望值, x_i为可能取值", "\\text{Var}(X) = E[X^2] - (E[X])^2  # 方差", "E[X+Y] = E[X] + E[Y]  # 期望线性性", "\\text{Var}(X) = E[(X-\\mu)^2]  # 方差定义, μ=E[X]"], # 离散概率
            "combinatorics": ["C(n,k) = \\frac{n!}{k!(n-k)!}  # 组合数, 从n个中选k个", "P(n,k) = \\frac{n!}{(n-k)!}  # 排列数, 从n个中选k个排列", "C(n,k) = C(n,n-k)  # 组合对称性", "P(n,n) = n!  # 全排列"], # 组合数学
            "addition principle": ["|A \\cup B| = |A| + |B| - |A \\cap B|  # 容斥原理, |A|为集合A的元素个数", "|A \\cup B| = |A| + |B|, \\text{ if } A \\cap B = \\emptyset  # 互斥集合的并集", "|A_1 \\cup A_2 \\cup \\cdots \\cup A_n| = \\sum |A_i| - \\sum |A_i \\cap A_j| + \\cdots  # 多集合容斥原理"], # 加法原理
            "multiplication principle": ["|A \\times B| = |A| \\cdot |B|  # 乘法原理, 笛卡尔积的元素个数", "N = n_1 \\cdot n_2 \\cdot \\cdots \\cdot n_k  # 多步骤计数, n_i为第i步的选择数", "N = m \\cdot n  # 两步计数, m和n为各步选择数"], # 乘法原理
            "permutation": ["P(n,k) = \\frac{n!}{(n-k)!}  # 排列数, 从n个中选k个排列", "P(n,n) = n!  # 全排列", "P_{\\text{circular}}(n) = (n-1)!  # 圆排列", "P(n; n_1, n_2, \\ldots, n_k) = \\frac{n!}{n_1! n_2! \\cdots n_k!}  # 重复排列, n_i为第i类元素个数"], # 排列
            "combination": ["C(n,k) = \\frac{n!}{k!(n-k)!}  # 组合数, 从n个中选k个", "C(n,k) = C(n,n-k)  # 组合对称性", "C(n,0) = C(n,n) = 1  # 边界条件", "C(n,k) = C(n-1,k-1) + C(n-1,k)  # 组合递推关系", "\\sum_{k=0}^n C(n,k) = 2^n  # 组合数求和"], # 组合
            "geometry": ["A = \\frac{1}{2}bh  # 三角形面积, A=面积, b=底, h=高", "a^2 + b^2 = c^2  # 勾股定理, a和b为直角边, c为斜边", "A = \\frac{1}{2}ab\\sin C  # 三角形面积, a和b为两边, C为夹角", "A = \\sqrt{s(s-a)(s-b)(s-c)}  # 海伦公式, s为半周长, a/b/c为三边"], # 几何
            "plane geometry": ["A_{\\triangle} = \\frac{1}{2}bh  # 三角形面积, b=底, h=高", "A_{\\text{circle}} = \\pi r^2  # 圆面积, r=半径", "C_{\\text{circle}} = 2\\pi r  # 圆周长, r=半径", "A_{\\text{rectangle}} = lw  # 矩形面积, l=长, w=宽", "A_{\\text{parallelogram}} = bh  # 平行四边形面积, b=底, h=高"], # 平面几何
            "solid geometry": ["V_{\\text{cube}} = a^3  # 正方体体积, a=边长", "V_{\\text{sphere}} = \\frac{4}{3}\\pi r^3  # 球体积, r=半径", "V_{\\text{cylinder}} = \\pi r^2 h  # 圆柱体积, r=半径, h=高", "S_{\\text{sphere}} = 4\\pi r^2  # 球表面积, r=半径", "V_{\\text{cone}} = \\frac{1}{3}\\pi r^2 h  # 圆锥体积, r=半径, h=高", "V_{\\text{pyramid}} = \\frac{1}{3}Bh  # 棱锥体积, B=底面积, h=高"], # 立体几何
            "Pythagorean theorem": ["a^2 + b^2 = c^2  # 勾股定理, a和b为直角边, c为斜边", "c = \\sqrt{a^2 + b^2}  # 求斜边", "a = \\sqrt{c^2 - b^2}  # 求直角边a", "b = \\sqrt{c^2 - a^2}  # 求直角边b"], # 勾股定理
            "law of cosines": ["c^2 = a^2 + b^2 - 2ab\\cos C  # 余弦定理, a/b/c为三角形三边, C为c的对角", "a^2 = b^2 + c^2 - 2bc\\cos A  # 余弦定理, A为a的对角", "b^2 = a^2 + c^2 - 2ac\\cos B  # 余弦定理, B为b的对角", "\\cos C = \\frac{a^2 + b^2 - c^2}{2ab}  # 余弦定理求角"], # 余弦定理
            "law of sines": ["\\frac{a}{\\sin A} = \\frac{b}{\\sin B} = \\frac{c}{\\sin C} = 2R  # 正弦定理, R为外接圆半径", "\\frac{\\sin A}{a} = \\frac{\\sin B}{b} = \\frac{\\sin C}{c}  # 正弦定理比例式", "a = 2R\\sin A  # 边与角关系, R为外接圆半径", "b = 2R\\sin B  # 边与角关系"], # 正弦定理
            "trigonometry": ["\\sin^2\\theta + \\cos^2\\theta = 1  # 三角恒等式, θ为角度", "\\tan\\theta = \\frac{\\sin\\theta}{\\cos\\theta}  # 正切定义", "\\sin(A\\pm B) = \\sin A\\cos B \\pm \\cos A\\sin B  # 正弦和差公式", "\\cos(A\\pm B) = \\cos A\\cos B \\mp \\sin A\\sin B  # 余弦和差公式", "\\tan(A\\pm B) = \\frac{\\tan A \\pm \\tan B}{1 \\mp \\tan A\\tan B}  # 正切和差公式", "\\sin(2\\theta) = 2\\sin\\theta\\cos\\theta  # 倍角公式"], # 三角学
            "similarity": ["\\frac{a'}{a} = \\frac{b'}{b} = \\frac{c'}{c} = k  # 相似比, a'/b'/c'为相似图形对应边, k为比例", "\\angle A = \\angle A'  # 相似图形对应角相等", "\\angle B = \\angle B'  # 对应角相等", "\\frac{\\text{Area}'}{\\text{Area}} = k^2  # 面积比等于相似比平方"], # 相似
            "similar triangles": ["\\frac{AB}{A'B'} = \\frac{BC}{B'C'} = \\frac{AC}{A'C'}  # 相似三角形对应边成比例", "\\angle A = \\angle A', \\angle B = \\angle B'  # 对应角相等", "\\frac{a}{a'} = \\frac{b}{b'} = \\frac{c}{c'}  # 三边对应成比例", "\\frac{S}{S'} = \\left(\\frac{a}{a'}\\right)^2  # 面积比等于边长比平方"], # 相似三角形
            "circle": ["A = \\pi r^2  # 圆面积, r=半径", "C = 2\\pi r  # 圆周长, r=半径", "(x-h)^2 + (y-k)^2 = r^2  # 圆方程, (h,k)=圆心, r=半径", "s = r\\theta  # 弧长, r=半径, θ=圆心角(弧度)", "A_{\\text{sector}} = \\frac{1}{2}r^2\\theta  # 扇形面积, r=半径, θ=圆心角", "A_{\\text{segment}} = \\frac{1}{2}r^2(\\theta - \\sin\\theta)  # 弓形面积"], # 圆
            "tangent": ["d(O, l) = r  # 点到直线距离等于半径, O为圆心, l为切线, r为半径", "PT_1 = PT_2  # 从外部点到圆的两条切线长度相等, P为外部点", "l \\perp OP  # 切线与半径垂直, O为圆心, P为切点", "PT_1 = PT_2 = \\sqrt{OP^2 - r^2}  # 切线长度公式"], # 切线
            "power theorem": ["PA \\cdot PB = PC \\cdot PD  # 圆幂定理, P为圆外或圆上点, A/B/C/D为圆上点", "PT^2 = PA \\cdot PB  # 切线-割线定理, PT为切线长", "PA \\cdot PB = PC \\cdot PD  # 割线-割线定理", "PA \\cdot PB = PC \\cdot PD  # 圆幂定理一般形式"], # 幂定理
            "tetrahedron": ["V = \\frac{1}{6}|\\det(\\vec{AB}, \\vec{AC}, \\vec{AD})|  # 四面体体积, A/B/C/D为四个顶点", "V = \\frac{a^3}{6\\sqrt{2}}  # 正四面体体积, a为棱长", "S = \\sum_{i=1}^4 A_i  # 表面积, A_i为四个面的面积", "V = \\frac{1}{3}Bh  # 棱锥体积, B为底面积, h为高"], # 四面体
            "hyperbola": ["\\frac{x^2}{a^2} - \\frac{y^2}{b^2} = 1  # 双曲线标准方程, a和b为半轴长", "c^2 = a^2 + b^2  # 焦距关系, c为焦距", "F_1 = (c, 0), F_2 = (-c, 0)  # 焦点坐标", "y = \\pm \\frac{b}{a}x  # 渐近线方程", "e = \\frac{c}{a} > 1  # 离心率"], # 双曲线
            "parabola": ["y = ax^2 + bx + c  # 抛物线一般式, a≠0", "y = a(x-h)^2 + k  # 顶点式, (h,k)为顶点", "F = (h, k+\\frac{1}{4a})  # 焦点坐标", "y = k - \\frac{1}{4a}  # 准线方程", "x^2 = 4py  # 标准形式, p为焦距", "(h,k) = \\left(-\\frac{b}{2a}, \\frac{4ac-b^2}{4a}\\right)  # 顶点坐标"], # 抛物线
            "algebra": ["x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}  # 二次方程求根, ax²+bx+c=0", "(a+b)^2 = a^2 + 2ab + b^2  # 完全平方公式", "a^2 - b^2 = (a+b)(a-b)  # 平方差公式"], # 代数
            "algebraic identity": ["(a+b)^2 = a^2 + 2ab + b^2  # 完全平方和", "(a-b)^2 = a^2 - 2ab + b^2  # 完全平方差", "a^2 - b^2 = (a+b)(a-b)  # 平方差公式", "a^3 + b^3 = (a+b)(a^2-ab+b^2)  # 立方和公式", "a^3 - b^3 = (a-b)(a^2+ab+b^2)  # 立方差公式", "(a+b)^3 = a^3 + 3a^2b + 3ab^2 + b^3  # 完全立方和"], # 代数恒等式
            "complex": ["|z| = \\sqrt{a^2 + b^2}  # 复数模长, z=a+bi为复数, |z|为模", "z = r(\\cos \\theta + i\\sin \\theta)  # 复数三角形式, r为模, θ为幅角", "z = re^{i\\theta}  # 复数指数形式, r为模, θ为幅角", "z \\cdot \\bar{z} = |z|^2  # 复数与其共轭乘积, z̅为z的共轭"], # 复数
            "logarithm": ["\\log_a(b) = c \\iff a^c = b  # 对数定义, a为底数, b为真数, c为对数", "\\log(ab) = \\log(a) + \\log(b)  # 对数乘法法则", "\\log\\left(\\frac{a}{b}\\right) = \\log(a) - \\log(b)  # 对数除法法则", "\\log(a^n) = n\\log(a)  # 对数幂法则", "\\log_a(a) = 1  # 底数对数", "\\log_a(1) = 0  # 1的对数"], # 对数
            "exponent": ["a^m \\cdot a^n = a^{m+n}  # 同底数幂相乘", "(a^m)^n = a^{mn}  # 幂的乘方", "\\frac{a^m}{a^n} = a^{m-n}  # 同底数幂相除", "a^0 = 1  # 零次幂", "a^{-n} = \\frac{1}{a^n}  # 负指数幂", "(ab)^n = a^n b^n  # 积的乘方"], # 指数，幂
            "system of equations": ["\\begin{cases} ax + by = c \\\\ dx + ey = f \\end{cases}  # 二元一次方程组", "x = \\frac{ce - bf}{ae - bd}  # 克莱姆法则求x, a/b/c/d/e/f为系数", "y = \\frac{af - cd}{ae - bd}  # 克莱姆法则求y", "\\det(A) = ad - bc  # 二阶行列式, A为系数矩阵"], # 方程组
            "set": ["A \\cap B  # 交集, A和B的公共元素", "A \\cup B  # 并集, A或B的所有元素", "A'  # 补集, 全集减去A", "A - B  # 差集, 在A中但不在B中", "|A|  # 基数, 集合A的元素个数", "A \\subseteq B  # 子集, A包含于B", "A \\times B  # 笛卡尔积, 有序对集合"], # 集合
            "game theory": ["u_i(s_i, s_{-i})  # 玩家i的效用, s_i为i的策略, s_{-i}为其他玩家策略", "u_i(s_i^*, s_{-i}^*) \\geq u_i(s_i, s_{-i}^*)  # 纳什均衡条件", "\\max_{s_i} u_i(s_i, s_{-i})  # 最大化效用", "\\text{BR}_i(s_{-i}) = \\arg\\max_{s_i} u_i(s_i, s_{-i})  # 最佳反应"], # 博弈论
            "induction": ["P(1)  # 归纳基础, n=1时命题成立", "P(k) \\implies P(k+1)  # 归纳步骤, 假设P(k)成立推出P(k+1)", "\\forall n \\in \\mathbb{N}, P(n)  # 对所有自然数成立", "P(1) \\land (\\forall k, P(k) \\implies P(k+1)) \\implies \\forall n, P(n)  # 数学归纳法原理"], # 归纳
            "modular arithmetic": ["a \\equiv b \\pmod{m} \\iff m \\mid (a-b)  # 同余定义, m为模数", "(a+b) \\bmod m = ((a \\bmod m) + (b \\bmod m)) \\bmod m  # 同余加法", "(a \\cdot b) \\bmod m = ((a \\bmod m) \\cdot (b \\bmod m)) \\bmod m  # 同余乘法", "a \\equiv b \\pmod{m} \\implies a^n \\equiv b^n \\pmod{m}  # 同余幂"], # 模运算
            "divisibility": ["a \\mid b \\iff b = ka \\text{ for some } k \\in \\mathbb{Z}  # 整除定义, a整除b", "a \\mid b \\land b \\mid c \\implies a \\mid c  # 整除传递性", "a \\mid b \\land a \\mid c \\implies a \\mid (bx+cy)  # 整除线性组合", "\\gcd(a,b) = d \\iff d \\mid a \\land d \\mid b  # 最大公约数, d为a和b的最大公约数"], # 整除
            "congruence": ["a \\equiv b \\pmod{m} \\iff m \\mid (a-b)  # 同余定义, m为模数", "a \\equiv b \\pmod{m} \\land c \\equiv d \\pmod{m} \\implies a+c \\equiv b+d \\pmod{m}  # 同余加法", "a \\equiv b \\pmod{m} \\implies a^n \\equiv b^n \\pmod{m}  # 同余幂", "a \\equiv b \\pmod{m} \\land c \\equiv d \\pmod{m} \\implies ac \\equiv bd \\pmod{m}  # 同余乘法"], # 同余
            "function period": ["f(x+T) = f(x)  # 周期函数定义, T为周期", "\\sin(x+2\\pi) = \\sin x  # 正弦函数周期为2π", "\\cos(x+2\\pi) = \\cos x  # 余弦函数周期为2π", "\\tan(x+\\pi) = \\tan x  # 正切函数周期为π", "f(x+nT) = f(x) \\text{ for } n \\in \\mathbb{Z}  # 周期函数的整数倍周期"], # 函数周期
            "number base": ["a_na_{n-1}\\ldots a_1a_0_{(b)} = \\sum_{i=0}^n a_i b^i  # b进制转十进制, a_i为各位数字, b为进制", "N = \\sum_{i=0}^n a_i b^i  # 进制转换公式", "N_{(10)} = \\sum_{i=0}^n a_i b^i  # 转换为十进制"], # 进制
            "enumeration": ["\\sum_{i=1}^n i = \\frac{n(n+1)}{2}  # 自然数求和", "\\sum_{i=1}^n i^2 = \\frac{n(n+1)(2n+1)}{6}  # 平方数求和", "\\sum_{i=1}^n i^3 = \\left(\\frac{n(n+1)}{2}\\right)^2  # 立方数求和", "|S| = \\sum_{i} |S_i|  # 分类计数, S_i为互不相交的子集"], # 枚举
            "prime factorization": ["n = p_1^{e_1} p_2^{e_2} \\cdots p_k^{e_k}  # 质因数分解, p_i为质数, e_i为指数", "\\gcd(a,b) = \\prod p_i^{\\min(e_i, f_i)}  # 最大公约数, e_i和f_i为a和b的质因数指数", "\\text{lcm}(a,b) = \\prod p_i^{\\max(e_i, f_i)}  # 最小公倍数", "n = \\prod_{p \\mid n} p^{\\alpha_p}  # 质因数分解一般形式"], # 质因数分解
            "mode": ["\\text{Mode} = \\arg\\max_{x} f(x)  # 众数, 出现频率最高的值", "\\text{Mode}(X) = x_i \\text{ where } P(X=x_i) = \\max_{j} P(X=x_j)  # 离散随机变量的众数", "\\text{Mode} = \\max_{x} \\text{frequency}(x)  # 众数定义"], # 众数
            "median": ["\\text{Median} = \\begin{cases} x_{(n+1)/2} & n \\text{ odd} \\\\ \\frac{x_{n/2} + x_{n/2+1}}{2} & n \\text{ even} \\end{cases}  # 中位数, n为数据个数, x_i为排序后的数据", "\\text{Median} = Q_2  # 中位数等于第二四分位数", "P(X \\leq \\text{Median}) = 0.5  # 中位数概率性质", "\\text{Median} = x_{\\lceil n/2 \\rceil}  # 中位数位置"], # 中位数
            "inclusion-exclusion principle": ["|A \\cup B| = |A| + |B| - |A \\cap B|  # 两集合容斥原理", "|A \\cup B \\cup C| = |A| + |B| + |C| - |A \\cap B| - |A \\cap C| - |B \\cap C| + |A \\cap B \\cap C|  # 三集合容斥原理", "\\left|\\bigcup_{i=1}^n A_i\\right| = \\sum_{i} |A_i| - \\sum_{i<j} |A_i \\cap A_j| + \\cdots + (-1)^{n+1} |A_1 \\cap \\cdots \\cap A_n|  # n集合容斥原理"], # 容斥原理
            "conjugate": ["\\bar{z} = a - bi, z = a + bi  # 共轭复数定义, z̅为z的共轭", "z \\cdot \\bar{z} = |z|^2  # 复数与其共轭的乘积等于模的平方", "z + \\bar{z} = 2\\text{Re}(z)  # 复数与其共轭的和等于2倍实部", "z - \\bar{z} = 2i\\text{Im}(z)  # 复数与其共轭的差等于2i倍虚部", "\\overline{z_1 + z_2} = \\bar{z_1} + \\bar{z_2}  # 和的共轭等于共轭的和", "\\overline{z_1 z_2} = \\bar{z_1} \\cdot \\bar{z_2}  # 积的共轭等于共轭的积"], # 共轭
        }

    def _extract_knowledge_points(self, problem_text: str, llm: LLMClient) -> List[str]:
        """提取题目的主要知识点"""
        prompt =textwrap.dedent(f"""
            你是一个数学教育专家。请分析下面的数学题目，提取主要涉及的知识点。

            题目：
            {problem_text}

            请以JSON格式输出知识点列表，格式为：{{"knowledge_points": ["知识点1", "知识点2", ...]}}
            知识点应该用英文关键词，如 "probability", "geometry", "algebra", "complex numbers", "combinatorics" 等。
            只输出JSON，不要有其他文字。
            """)
        try:
            resp = llm.chat(prompt)
            # 尝试提取JSON
            json_match = re.search(r'\{[^}]+\}', resp, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return data.get("knowledge_points", [])
            return []
        except Exception as e:
            print(f"提取知识点时出错: {e}")
            return []

    def _retrieve_formulas(self, knowledge_points: List[str]) -> str:
        """根据知识点查询公式库"""
        formulas = []
        for kp in knowledge_points:
            kp_lower = kp.lower()
            for key, value_list in self.formula_library.items():
                if key in kp_lower:
                    print(f"匹配到key：{key}")
                    formulas.extend(value_list)
        return "\n".join(formulas) if formulas else "No specific formulas found."

    def _extract_numeric_inputs(self, problem_text: str, llm: LLMClient) -> Dict[str, Any]:
        """从题目文本中提取一个随机数字变量，并标注位置信息"""
        prompt = textwrap.dedent(f"""
            请从下面的数学题目中随机选择一个数字变量。
            题目：
            {problem_text}

            要求：
            1. 随机选择一个数字作为变量
            2. 对于这个数字，标注它在题目中出现的一个代表性位置（使用字符位置，从题目文本开头开始计数，从0开始）

            请以JSON格式输出，格式为：
            {{
                "name": "变量名",
                "value": 数值,
                "position": {{
                    "char_start": 起始位置,
                    "char_end": 结束位置,
                    "context": "上下文描述"
                }}
            }}

            变量名应该是有意义的，如 "n", "size", "count" 等。
            位置信息使用字符位置（从题目文本开头开始计数，从0开始），要足够详细，以便后续能够准确替换对应的数字。
            只输出JSON，不要有其他文字。
            """)
        try:
            resp = llm.chat(prompt)
            json_match = re.search(r'\{.*\}', resp, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                # 转换为简化的格式，保留位置信息
                extracted = {}
                if "name" in result and "value" in result:
                    extracted[result["name"]] = {
                        "value": result["value"],
                        "position": result.get("position", {})
                    }
                return extracted
            return {}
        except Exception as e:
            print(f"提取数字输入时出错: {e}")
            return {}

    def _check_hard_coded(self, code: str, llm: LLMClient) -> bool:
        """检查代码是否包含硬编码答案"""
        prompt = textwrap.dedent(f"""
            请检查下面的Python代码是否包含硬编码的答案或实例特定的输出，而不是通用的计算过程。

            代码：
            {code}

            请以JSON格式输出：{{"is_hard_coded": true/false, "reason": "原因说明"}}
            只输出JSON，不要有其他文字。
            """)
        try:
            resp = llm.chat(prompt)
            json_match = re.search(r'\{[^}]+\}', resp, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return data.get("is_hard_coded", False)
            return False
        except Exception as e:
            print(f"检查硬编码时出错: {e}")
            return False

    def _run_python_code(self, code: str, inputs: Dict[str, Any], primary_key: Optional[str] = None, verify: bool = False) -> Tuple[Optional[str], Optional[str]]:
        """运行Python代码并返回输出和错误（支持将 inputs 或其中单个变量传入 solve）"""
        code_file = None
        try:
            # 准备代码内容
            input_code = f"inputs = {repr(inputs)}"
            if primary_key and primary_key in inputs:
                call_code = f"result = solve(inputs[{repr(primary_key)}])"
            else:
                call_code = "result = solve(inputs)"
            full_code = f"{input_code}\n\n{code}\n\n# 调用 solve\n{call_code}\nprint(result)"
            
            # 使用指定的目录，生成有意义的文件名
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # 年月日_时分秒，如：20251211_151438
            if verify == True:
                filename = f"q{self.current_question_id}_verify_{timestamp}.py"
            else:
                filename = f"q{self.current_question_id}_generate_{timestamp}.py"

            code_file = os.path.join(self.code_dir, filename)
            with open(code_file, 'w', encoding='utf-8') as f:
                f.write(full_code)

            # 运行代码
            result = subprocess.run(
                ['python3', code_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                if code_file:
                    print(f"【成功执行】 Python代码已保存到: {code_file} 🤩")
                return result.stdout.strip(), None # 返回print的标准输出和 None
            else:
                if code_file:
                    print(f"【执行出错】 Python代码已保存到: {code_file} ")
                return None, result.stderr.strip()
        except subprocess.TimeoutExpired:
            if code_file:
                print(f"【执行超时】 Python代码已保存到: {code_file} ")
            return None, "Timeout"
        except Exception as e:
            if code_file:
                print(f"【异常: {str(e)}】 Python代码已保存到: {code_file} ")
            return None, str(e)

    def _build_numeric_solver(
        self,
        problem_text: str,
        answer_gold: str,
        solution_sketches: str,
        retrieved_formulas: str,
        knowledge_points: List[str],
        llm_codegen: LLMClient,
        llm_check: LLMClient,
        llm_refine: Optional[LLMClient] = None,
        llm_range: Optional[LLMClient] = None,
        max_iter: int = 5,
        max_refine: int = 5,
    ) -> Optional[Tuple[str, Dict, str, Dict[str, Any]]]:
        """构建数字替换求解器，返回 (code, value_ranges占位, primary_key, numeric_inputs)"""
        history = []
        
        print("------------提取数字变量------------")
        numeric_inputs = self._extract_numeric_inputs(problem_text, llm_codegen)
        # numeric_inputs 的结构是 {变量名: {value: 值, position: {...}}}
        # primary_key 是提取的变量
        primary_key = list(numeric_inputs.keys())[0] if numeric_inputs else None
        print("提取的数字变量：")
        for key, info in numeric_inputs.items():
            value = info.get("value", info) if isinstance(info, dict) else info
            position = info.get("position", {}) if isinstance(info, dict) else {}
            print(f"  {key} = {value} 位置: {position}")
        
        print("----------生成通用求解代码----------")
        for iter_num in range(max_iter):
            print(f"第【 {iter_num+1} 】次生成代码")
            # 准备变量信息字符串
            primary_info = numeric_inputs.get(primary_key, {}) if primary_key else {}
            primary_value = primary_info.get("value", primary_info) if isinstance(primary_info, dict) else primary_info
            primary_position = primary_info.get("position", {}) if isinstance(primary_info, dict) else {}
            
            # 生成代码
            prompt = textwrap.dedent(f"""
                你是一个数学编程专家。请分析下面的数学题目，编写一个Python求解程序。
                题目：
                {problem_text}
                正确答案：
                {answer_gold}
                相关公式：
                {retrieved_formulas}
                知识点：
                {", ".join(knowledge_points)}
                解法思路：
                {solution_sketches}

                变量信息：
                变量：{primary_key} = {primary_value}（位置：{primary_position}）

                要求：
                1. 编写一个Python函数 solve({primary_key}), 仅接受变量 {primary_key} 的值作为参数
                2. 实现通用的计算过程，不要硬编码答案
                3. 函数应该返回题目的答案
                4. 注意：题目中可能有多个相同的数字，但只有变量 {primary_key} 对应的位置需要作为参数传入

                请只输出Python代码，不要有其他解释。
                """)
            history.append((prompt, None))
            
            try:
                code_resp = llm_codegen.chat(prompt)
                # 提取代码块
                code_match = re.search(r'```python\n(.*?)\n```', code_resp, re.DOTALL)
                if code_match:
                    code = code_match.group(1)
                else:
                    code_match = re.search(r'```\n(.*?)\n```', code_resp, re.DOTALL)
                    code = code_match.group(1) if code_match else code_resp
                
                # 检查硬编码
                if self._check_hard_coded(code, llm_check):
                    print("生成代码包含硬编码，跳过🥶")
                    print(f"生成代码：{code}")
                    continue
                else:
                    print("硬编码检测通过，准备验证代码🫡")

                # 验证代码
                # 将 numeric_inputs 转换为简单格式 {变量名: 值} 用于代码执行
                input_variables = {}
                for key, info in numeric_inputs.items():
                    value = info.get("value", info) if isinstance(info, dict) else info
                    input_variables[key] = value
                
                for refine_step in range(max_refine):
                    output, error = self._run_python_code(code, input_variables, primary_key, verify=True)
                    history.append((code, (output, error)))
                    
                    if error is None and output == answer_gold:
                        print("【答案正确】 准备返回代码🥳")

                        print("----------确定变量取值范围----------")
                        value_ranges = {}
                        position_str = f"位置：字符 {primary_position.get('char_start', '?')}-{primary_position.get('char_end', '?')}" if primary_position else "位置：未标注"
                        context_str = f"，上下文：{primary_position.get('context', '')}" if primary_position.get('context') else ""
                        
                        range_prompt = textwrap.dedent(f"""
                            你是一个数学问题分析专家。请分析下面的题目和对应的解题代码，确定输入变量的合理取值范围。
                            题目：
                            {problem_text}                                
                            正确答案：
                            {answer_gold}
                            求解代码：
                            ```python
                            {code}
                            ```                                
                            输入变量：{primary_key}（当前值：{primary_value}，{position_str}{context_str}）

                            请分析代码逻辑和题目要求，为变量 {primary_key} 确定合理的取值。
                            取值应该：
                            1. 保证代码能正常运行（不会出现除零、负数开方等错误）
                            2. 保证答案在合理范围内
                            3. 保证题目有意义，数值不能太小或太大（不能超过1000）
                            
                            如果变量可以取连续范围内的任意值，请使用格式：
                            取值范围：[min, max]
                            例如：取值范围：[1, 100]
                            
                            如果变量只能取特定的离散值，请使用格式：
                            取值列表：[value1, value2, value3, ...]
                            例如：取值列表：[1, 15, 301]
                            
                            请根据题目和代码的特点，选择合适的格式输出。
                            重要：只输出取值范围或取值列表，不要输出任何其他解释或内容。
                            """)
                        try:
                            range_resp = llm_range.chat(range_prompt)
                            # 尝试解析连续范围格式：取值范围：[min, max]
                            range_match = re.search(r'取值范围[：:]\s*\[(\d+),\s*(\d+)\]', range_resp)
                            if range_match:
                                min_val = int(range_match.group(1))
                                max_val = int(range_match.group(2))
                                value_ranges[primary_key] = (min_val, max_val)
                                print(f"确定取值范围（连续）：{primary_key} = [{min_val}, {max_val}]")
                            else:
                                # 尝试解析离散值列表格式：取值列表：[value1, value2, ...]
                                list_match = re.search(r'取值列表[：:]\s*\[([\d,\s]+)\]', range_resp)
                                if list_match:
                                    values_str = list_match.group(1)
                                    values = [int(v.strip()) for v in values_str.split(',') if v.strip().isdigit()]
                                    if values:
                                        value_ranges[primary_key] = values
                                        print(f"确定取值列表（离散）：{primary_key} = {values}")
                                    else:
                                        print(f"无法解析取值列表，使用默认范围")
                                        value_ranges[primary_key] = (1, 100)
                                else:
                                    print(f"无法解析取值范围，使用默认范围")
                                    value_ranges[primary_key] = (1, 100)
                        except Exception as e:
                            print(f"确定取值范围时出错: {e}，使用默认范围")
                            value_ranges[primary_key] = (1, 100)

                        # 返回时保留完整的位置信息，但同时也提供简单格式用于后续处理
                        # 注意：numeric_inputs 包含位置信息，但 _generate_numeric_variant 需要简单格式
                        return code, value_ranges, primary_key, numeric_inputs, primary_position
                    
                    if refine_step == max_refine - 1:
                        break
                    
                    # 精炼代码
                    refine_prompt = textwrap.dedent(f"""
                        之前的代码有错误。请修正它。
                        题目：{problem_text}
                        正确答案：{answer_gold}
                        之前的代码：
                        ```python
                        {code}
                        ```
                        solve 的输入变量：{primary_key}（其值：{primary_value}）
                        输入字典（供参考）：{json.dumps(input_variables, ensure_ascii=False)}
                        错误信息：{error}
                        输出：{output}
                        历史记录：
                        {json.dumps(history, indent=2, ensure_ascii=False)}
                        请修正代码，只输出Python代码（保持 solve({primary_key}) 接口）。
                        """)
                    code_resp = (llm_refine or llm_codegen).chat(refine_prompt)
                    code_match = re.search(r'```python\n(.*?)\n```', code_resp, re.DOTALL)
                    if code_match:
                        code = code_match.group(1)
                    else:
                        code_match = re.search(r'```\n(.*?)\n```', code_resp, re.DOTALL)
                        code = code_match.group(1) if code_match else code_resp
            except Exception as e:
                print(f"生成代码时出错: {e}")
                continue
        
        return None

    def _extract_value_ranges(self, code: str, original_value: Any) -> Tuple[Any, Any]:
        """从代码注释中提取值范围，如果无法提取则使用默认范围（原值的±50%）"""
        # 尝试从注释中提取范围信息
        for line in code.split('\n'):
            if '#' in line and ('range' in line.lower() or 'between' in line.lower()):
                # 尝试提取范围信息（简单实现：查找数字范围）
                import re as re_module
                range_match = re_module.search(r'(\d+)\s*[-~]\s*(\d+)', line)
                if range_match:
                    min_val = int(range_match.group(1))
                    max_val = int(range_match.group(2))
                    return min_val, max_val
        
        # 如果无法提取，使用默认范围：原值的 ±50%
        if isinstance(original_value, (int, float)):
            min_val = max(1, int(original_value * 0.5))
            max_val = int(original_value * 1.5)
            return min_val, max_val
        else:
            # 如果原值不是数字，返回一个默认范围
            return 1, 100

    def _get_random_value_from_range(self, value_range: Any) -> int:
        """从取值范围中随机选择一个值，支持连续范围 (min, max) 或离散值列表 [v1, v2, ...]"""
        if isinstance(value_range, tuple) and len(value_range) == 2:
            # 连续范围
            min_val, max_val = value_range
            return random.randint(min_val, max_val)
        elif isinstance(value_range, list):
            # 离散值列表
            return random.choice(value_range)
        else:
            # 默认范围
            return random.randint(1, 100)

    def _generate_numeric_variant(
        self, 
        problem_text: str, 
        code: str, 
        primary_key: str,
        primary_position: Dict[str, Any],
        original_inputs: Dict[str, Any],
        value_ranges: Dict[str, Any],
        llm: LLMClient
    ) -> Tuple[str, str]:
        """使用求解器生成数字变体：随机选择值，运行代码得到答案，然后生成新题目"""
        try:
            original_value = original_inputs.get(primary_key)
            value_range = value_ranges.get(primary_key, (1, 100))
            print("--------随机选择变量值--------")
            new_value = self._get_random_value_from_range(value_range)
            print(f"随机选择的变量值：{new_value}")
            
            print("----------生成新答案----------")
            new_inputs = {primary_key: new_value}
            output, error = self._run_python_code(code, new_inputs, primary_key, verify=False)
            
            if error is not None:
                print(f"运行代码时出错: {error}")
                return "", ""
            
            new_answer = output
            print(f"新答案：{new_answer}")
            
            print("----------生成新题目----------")
            char_start = primary_position.get('char_start', '?')
            char_end = primary_position.get('char_end', '?')
            context = primary_position.get('context', '')
            position_info = f"第 {char_start}-{char_end}个字符，上下文：{context}"
            prompt = textwrap.dedent(f"""
                基于下面的原始题目，生成一个新的数字变体题目。
                原始题目：
                {problem_text}
                
                要修改的变量信息：
                - 变量名：{primary_key}
                - 原始值：{original_value}
                - 新值：{new_value}
                - 变量在原始题目中的位置：{position_info}
                
                要求：
                1. 将原始题目中位于第 {char_start}-{char_end} 个字符处的数字（即变量 {primary_key} 的值 {original_value}）改为 {new_value}
                2. 注意：原始题目中可能有多处出现数字 {original_value}，但只需要修改位置 {char_start}-{char_end} 处的那一个
                3. 保持题目其他部分完全不变
                
                请只输出新题目的文本，不要有其他解释。
                """)
            # print("prompt:  "+prompt)
            resp = llm.chat(prompt)
            print(f"新题目：{resp.strip()}")
            return resp.strip(), new_answer
        except Exception as e:
            print(f"生成数字变体时出错: {e}")
            return "", ""

    def transform_analogical2(
        self,
        item: ProblemItem,
        llm_extract: Optional[LLMClient] = None,
        llm_codegen: Optional[LLMClient] = None,
        llm_check: Optional[LLMClient] = None,
        llm_refine: Optional[LLMClient] = None,
        llm_variant: Optional[LLMClient] = None,
        llm_range: Optional[LLMClient] = None,
    ) -> ProblemItem:
        """
        analogical-2：数字替换（numeric substitutions via code-based solution extraction）
        """
        llm_extract = llm_extract or self.llm
        llm_codegen = llm_codegen or self.llm
        llm_check = llm_check or self.llm
        llm_refine = llm_refine or self.llm
        llm_variant = llm_variant or self.llm
        llm_range = llm_range or self.llm
        
        print("--------------------------------提取知识点--------------------------------")
        knowledge_points = self._extract_knowledge_points(item.original_question, llm_extract)
        print("提取的知识点：\n", knowledge_points)
        
        print("--------------------------------查询公式库--------------------------------")
        retrieved_formulas = self._retrieve_formulas(knowledge_points)
        print("检索到的公式：\n", retrieved_formulas)
        
        print("--------------------------------构建求解器--------------------------------")
        solver_result = self._build_numeric_solver(
            item.original_question,
            item.true_answer,
            item.solution,
            retrieved_formulas,
            knowledge_points,
            llm_codegen=llm_codegen,
            llm_check=llm_check,
            llm_refine=llm_refine,
            llm_range=llm_range
        )
        
        code, value_ranges, primary_key, numeric_inputs, primary_position = solver_result
        # 将 numeric_inputs 转换为简单格式 {变量名: 值} 用于生成变体
        input_variables = {}
        for key, info in numeric_inputs.items():
            value = info.get("value", info) if isinstance(info, dict) else info
            input_variables[key] = value
        
        print("--------------------------------生成数字变体--------------------------------")
        variant, new_answer = self._generate_numeric_variant(
            item.original_question, 
            code, 
            primary_key,
            primary_position,
            input_variables,
            value_ranges,
            llm_variant
        )
        item.augmented_question = variant
        item.augmented_true_answer = new_answer
        item.method_used = "analogical-2"
        return item

    def _analyze_invertible_conditions(
        self,
        problem_text: str,
        answer_gold: str,
        solution_sketches: str,
        retrieved_formulas: str,
        llm: LLMClient,
    ) -> Optional[Dict]:
        """分析可逆条件关系"""
        prompt = textwrap.dedent(f"""
            你是一个数学问题分析专家。请分析下面的题目，判断条件和目标是否可以互换。
            题目：
            {problem_text}
            正确答案：{answer_gold}
            解法思路：
            {solution_sketches}
            相关公式：
            {retrieved_formulas}
            请分析：
            1. 题目的关键条件是什么？
            2. 题目的目标是什么？
            3. 是否可以将原目标作为条件，原条件（的一部分）作为新目标？
            请以JSON格式输出：
            {{
                "invertible": true/false,
                "original_conditions": ["条件1", "条件2", ...],
                "original_target": "目标",
                "new_conditions": ["新条件1", "新条件2", ...],
                "new_target": "新目标",
                "recomposed_problem_text": "重组后的题目文本"
            }}
            只输出JSON，不要有其他文字。
            """)
        try:
            resp = llm.chat(prompt)
            json_match = re.search(r'\{.*\}', resp, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                if data.get("invertible", False):
                    return data
            return None
        except Exception as e:
            print(f"分析可逆条件时出错: {e}")
            return None

    def _build_recomposed_solver(
        self,
        original_problem: str,
        new_problem: str,
        original_answer: str,
        new_answer: str,
        solution_sketches: str,
        retrieved_formulas: str,
        llm_codegen: LLMClient,
        llm_check: LLMClient,
        llm_refine: Optional[LLMClient] = None,
        max_iter: int = 5,
        max_refine: int = 5,
    ) -> Optional[str]:
        """构建重组问题的求解器"""
        history = []
        
        for iter_num in range(max_iter):
            prompt = textwrap.dedent(f"""
                你是一个数学编程专家。请为重组后的题目编写Python求解程序。
                原始题目：
                {original_problem}
                原始答案：{original_answer}
                重组后的题目：
                {new_problem}
                重组后的答案：{new_answer}
                解法思路：
                {solution_sketches}
                相关公式：
                {retrieved_formulas}
                要求：
                1. 编写一个Python函数 solve(inputs)，接受一个字典参数 inputs（调用时会提供）
                2. 实现重组后题目的求解逻辑，不要硬编码答案
                3. 函数应该返回重组后题目的答案
                请只输出Python代码。
                """)
            history.append((prompt, None))
            
            try:
                code_resp = llm_codegen.chat(prompt)
                code_match = re.search(r'```python\n(.*?)\n```', code_resp, re.DOTALL)
                if code_match:
                    code = code_match.group(1)
                else:
                    code_match = re.search(r'```\n(.*?)\n```', code_resp, re.DOTALL)
                    code = code_match.group(1) if code_match else code_resp
                
                if self._check_hard_coded(code, llm_check):
                    continue
                
                # 验证：使用原始答案作为输入
                inputs = {"original_answer": original_answer}
                output, error = self._run_python_code(code, inputs)
                history.append((code, (output, error)))
                
                if error is None and output == new_answer:
                    return code
                
                for refine_step in range(max_refine - 1):
                    refine_prompt = textwrap.dedent(f"""
                        之前的代码有错误。请修正它。
                        重组后的题目：{new_problem}
                        重组后的答案：{new_answer}
                        之前的代码：
                        ```python
                        {code}
                        ```
                        错误信息：{error}
                        输出：{output}
                        请修正代码，只输出Python代码（保持 solve(inputs) 接口）。
                        """)
                    code_resp = (llm_refine or llm_codegen).chat(refine_prompt)
                    code_match = re.search(r'```python\n(.*?)\n```', code_resp, re.DOTALL)
                    if code_match:
                        code = code_match.group(1)
                    else:
                        code_match = re.search(r'```\n(.*?)\n```', code_resp, re.DOTALL)
                        code = code_match.group(1) if code_match else code_resp
                    
                    output, error = self._run_python_code(code, inputs)
                    history.append((code, (output, error)))
                    
                    if error is None and output == new_answer:
                        return code
            except Exception as e:
                print(f"构建重组求解器时出错: {e}")
                continue
        
        return None

    def transform_analogical3(
        self,
        item: ProblemItem,
        llm_extract: Optional[LLMClient] = None,
        llm_analysis: Optional[LLMClient] = None,
        llm_codegen: Optional[LLMClient] = None,
        llm_check: Optional[LLMClient] = None,
        llm_refine: Optional[LLMClient] = None,
    ) -> ProblemItem:
        """
        analogical-3：条件重组（conditional recomposition via invertible-condition analysis）
        """
        llm_extract = llm_extract or self.llm
        llm_analysis = llm_analysis or self.llm
        llm_codegen = llm_codegen or self.llm
        llm_check = llm_check or self.llm
        llm_refine = llm_refine or llm_codegen
        # 1. 提取知识点
        knowledge_points = self._extract_knowledge_points(item.original_question, llm_extract)
        
        # 2. 查询公式库
        retrieved_formulas = self._retrieve_formulas(knowledge_points)
        
        # 3. 分析可逆条件
        invertible_analysis = self._analyze_invertible_conditions(
            item.original_question,
            item.true_answer,
            item.solution,
            retrieved_formulas,
            llm_analysis
        )
        
        if invertible_analysis is None:
            # 如果不可逆，回退到简单方法
            print("警告：题目条件不可逆，使用简单方法生成变体")
            prompt = textwrap.dedent(f"""
                请基于下面的题目，生成一个条件重组的变体（将部分条件和目标互换）。
                原始题目：
                {item.original_question}
                正确答案：{item.true_answer}
                请只输出重组后的题目文本。
                """)
            resp = llm_analysis.chat(prompt)
            item.augmented_question = resp.strip()
        else:
            # 4. 构建重组问题的求解器
            new_problem = invertible_analysis.get("recomposed_problem_text", "")
            # new_target 是新问题的目标，应该是原条件的一部分
            # 验证时：将原答案（原目标值）作为输入，检查输出是否等于原条件的值
            original_conditions = invertible_analysis.get("original_conditions", [])
            new_target = invertible_analysis.get("new_target", "")
            
            # 尝试从原条件中提取数值（简化处理）
            original_condition_value = str(original_conditions[0]) if original_conditions else ""
            
            solver_code = self._build_recomposed_solver(
                item.original_question,
                new_problem,
                item.true_answer,
                original_condition_value,  # 验证目标：应该能恢复原条件的值
                item.solution,
                retrieved_formulas,
                llm_codegen=llm_codegen,
                llm_check=llm_check,
                llm_refine=llm_refine
            )
            
            if solver_code:
                item.augmented_question = new_problem
            else:
                # 如果构建求解器失败，直接使用分析结果
                item.augmented_question = new_problem
        
        item.method_used = "analogical-3"
        return item

class NovelProblemGenerator:
    """
    负责 novel-1 / novel-2 两种增强方式：
    - 6 -> novel-1：相同知识点、相似难度的全新题
    - 7 -> novel-2：更远迁移、更高新颖度的题
    """

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def generate_novel1(self, item: ProblemItem) -> ProblemItem:
        """
        novel-1：同知识点 + 相似难度 + 新情景
        """
        prompt = textwrap.dedent(f"""
            你是一个数学竞赛命题专家。

            请根据下面的原始题目，设计一条“novel-1 风格”的新题：
            - 主要考查的知识点与原题相同或非常接近；
            - 难度与原题大致相同；
            - 叙事背景、情境、变量等可以完全改变；
            - 题目结构和表述方式要与原题有明显区别，看起来像一道“不同的题”；
            - 不要给出解答，只给出完整题目陈述（英文）。

            原始题目：
            {item.original_question}

            （如有用，请参考原题解析）：
            {item.solution}

            请直接输出新题题干，不要加入任何解释。
            """)
        resp = self.llm.chat(prompt)
        item.augmented_question = resp.strip()
        item.method_used = "novel-1"
        return item

    def generate_novel2(self, item: ProblemItem) -> ProblemItem:
        """
        novel-2：更远类比/更大迁移，保持知识核心不变但表层/结构均明显变化
        """
        prompt = textwrap.dedent(f"""
            你是一个高级数学命题专家。

            请基于下面的原始题目，设计一条“novel-2 风格”的新题：
            - 仍然围绕与原题相同的核心数学概念或定理（例如同一类概率结构、同一类几何构型等）；
            - 但允许在题目结构、推理路径、叙事背景上进行较大创新；
            - 可以引入多步推理或不同的设问方式，只要整体难度仍在原题的同一量级（不要明显更简单或更难）；
            - 要让题目看起来与原题有“远类比”的感觉，但解题所需的核心数学知识是同一块；
            - 不要给出解答，只给出完整题目陈述（英文）。

            原始题目：
            {item.original_question}

            （如有用，请参考原题解析）：
            {item.solution}

            请直接输出新题题干，不要加入任何解释。
            """)
        resp = self.llm.chat(prompt)
        item.augmented_question = resp.strip()
        item.method_used = "novel-2"
        return item

# A-MES 主管道：根据 method 决定执行哪一种增强
class AMESPipeline:
    def __init__(
        self,
        analyzer: Optional[ProblemAnalyzer],
        analogical_transformer: Optional[AnalogicalTransformer],
        redundancy_injector: Optional[RedundancyInjector],
        novel_generator: Optional[NovelProblemGenerator],
        role_llms: Optional[Dict[str, LLMClient]] = None,
    ):
        self.analyzer = analyzer
        self.analogical_transformer = analogical_transformer
        self.redundancy_injector = redundancy_injector
        self.novel_generator = novel_generator
        self.role_llms = role_llms or {}

    def process(self, item: ProblemItem, method: str) -> ProblemItem:
        """
        method 取值：
        "1": analogical-1 中 disturb1（无关冗余）
        "2": analogical-1 中 disturb2（相关概念解释冗余）
        "3": analogical-1 中 disturb3（诱导错误方向冗余）
        "4": analogical-2（数字变换类比）
        "5": analogical-3（条件重组类比）
        "6": novel-1（同知识点新题改编）
        "7": novel-2（同知识点概念题）
        """

        # # 可选：先做题目分析（不影响增强逻辑）
        # if self.analyzer:
        #     item = self.analyzer.analyze(item)

        # 1,2,3 -> analogical-1
        if method in {"1", "2", "3"}:
            if not self.redundancy_injector:
                raise RuntimeError("RedundancyInjector 未初始化")
            item = self.redundancy_injector.inject(item, method)
            return item

        # 4,5 -> analogical-2,3 （类比变换）
        if method in {"4", "5"}:
            if not self.analogical_transformer:
                raise RuntimeError("Analogical 模块未初始化")
            # analogical-2
            if method == "4":
                llms = self.role_llms
                item = self.analogical_transformer.transform_analogical2(
                    item,
                    llm_extract=llms.get("extract"),
                    llm_codegen=llms.get("codegen"),
                    llm_check=llms.get("check"),
                    llm_refine=llms.get("refine"),
                    llm_variant=llms.get("variant"),
                    llm_range=llms.get("range"),
                )
            # analogical-3
            else:
                llms = self.role_llms
                item = self.analogical_transformer.transform_analogical3(
                    item,
                    llm_extract=llms.get("extract"),
                    llm_analysis=llms.get("analysis"),
                    llm_codegen=llms.get("codegen"),
                    llm_check=llms.get("check"),
                    llm_refine=llms.get("refine"),
                )
            return item

        # 6,7 -> novel-1,2 （新颖题生成）
        if method in {"6", "7"}:
            if not self.novel_generator:
                raise RuntimeError("NovelProblemGenerator 未初始化")
            if method == "6":
                item = self.novel_generator.generate_novel1(item)
            else:
                item = self.novel_generator.generate_novel2(item)
            return item

        raise ValueError(f"不支持的 method: {method}")


def get_output_filename(input_name: str, method: str) -> str:
    # os.path.basename从完整的文件路径中提取文件名部分，去掉目录路径，[0]获取名字中不带扩展名的部分
    base = os.path.splitext(os.path.basename(input_name))[0]
    tag = f"method_{method}"
    return f"{tag}_{base}.csv"


def run_ames_on_csv(args):
    os.makedirs(args.out_csv, exist_ok=True)
    output_path = os.path.join(args.out_csv, get_output_filename(args.input, args.method))

    def build_llm(model_name: str) -> LLMClient:
        return LLMClient(model_name=model_name, temperature=args.temperature)

    # 按阶段实例化（默认配置在 DEFAULT_STAGE_MODEL / DEFAULT_ROLE_MODEL）
    llm_analyzer = build_llm(DEFAULT_STAGE_MODEL["analyzer"])
    llm_redundancy = build_llm(DEFAULT_STAGE_MODEL["redundancy"])
    llm_novel = build_llm(DEFAULT_STAGE_MODEL["novel"])
    llm_analogical_fallback = build_llm(DEFAULT_STAGE_MODEL["analogical_fallback"])

    role_llms = {
        role: build_llm(model)
        for role, model in DEFAULT_ROLE_MODEL.items()
    }

    analyzer = ProblemAnalyzer(llm_analyzer)  # 如不需要可以改成 None
    analogical_transformer = AnalogicalTransformer(llm_analogical_fallback)
    redundancy_injector = RedundancyInjector(llm_redundancy)
    novel_generator = NovelProblemGenerator(llm_novel)

    pipeline = AMESPipeline(
        analyzer=analyzer,
        analogical_transformer=analogical_transformer,
        redundancy_injector=redundancy_injector,
        novel_generator=novel_generator,
        role_llms=role_llms,
    )

    total_count = 0
    success_count = 0
    start_time = time.time()

    with open(args.input, 'r', encoding='utf-8') as infile, \
            open(output_path, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # 不输出 header，直接写入数据行

        for i, row in enumerate(reader, start=1):
            if not row:
                continue
            if args.question_id and i != args.question_id:
                continue
            total_count += 1

            question = row[0]
            solution = row[1] 
            answer   = row[2] 

            print(f"\n===============================处理第【 {total_count} 】题================================")
            print(f"原题：\n{question}\n答案：\n{answer}")

            item = ProblemItem(
                original_question = question,
                solution = solution,
                true_answer = answer
            )

            # 设置当前题目ID，用于生成代码文件名
            analogical_transformer.current_question_id = i

            try:
                processed = pipeline.process(item, method=args.method)
                success_count += 1

                print("======================================小结====================================")
                print("原题：")
                print(item.original_question)
                print("原题答案：")
                print(item.true_answer)
                print("增强后题目：")
                print(processed.augmented_question)
                print("增强后题目答案：")
                print(processed.augmented_true_answer)
                print("\n==============================================================================\n")

                writer.writerow([
                    processed.original_question,
                    processed.solution,
                    processed.true_answer,
                    processed.augmented_question,
                    processed.method_used
                ])

            except Exception as e:
                print(f"处理第 {total_count} 行时出错：{e}")
                writer.writerow([
                    question,
                    solution,
                    "ERROR",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    f"error_{args.method}"
                ])

    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / total_count if total_count > 0 else 0
    print(f"\n结果已保存到: {output_path}")
    print(f"总共 {total_count} 行，成功转换 {success_count} 行，平均每行耗时 {avg_time:.2f} 秒")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A-MES：题目增强框架（7 种方法）")
    parser.add_argument('--input', default="./csv_auto_augment/filling_english_with_solutions.csv", help="输入 CSV 文件名")
    parser.add_argument('--out_csv', default="./csv_auto_augment", help="输出 CSV 文件所在文件夹")
    parser.add_argument('--temperature', type=float, default=0.2, help="API 回答多样性，默认 0.2")
    parser.add_argument('--model', type=str, default="deepseek", help="已忽略：模型选择请直接修改代码中的 DEFAULT_STAGE_MODEL / DEFAULT_ROLE_MODEL")
    parser.add_argument('--question_id', type=int, default=1, help="题目ID")
    parser.add_argument('--method', type=str, default="1",
        help=(
            "增强方法：\n"
            "1 -> analogical-1 / disturb1（无关冗余）\n"
            "2 -> analogical-1 / disturb2（相关概念冗余）\n"
            "3 -> analogical-1 / disturb3（诱导错误冗余）\n"
            "4 -> analogical-2（数字变换类比）\n"
            "5 -> analogical-3（条件重组类比）\n"
            "6 -> novel-1（同知识点新题改编）\n"
            "7 -> novel-2（同知识点概念题）"
        )
    )
    args = parser.parse_args()

    if args.method not in {"1", "2", "3", "4", "5", "6", "7"}:
        raise ValueError("method 必须是 1~7 之一")

    run_ames_on_csv(args)