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
claude_client = OpenAI(api_key="sk-qjspBDS9b0TvyUuV3hT8EzFFPegGgSA1htNN3MrCJV8iNJuY", base_url="https://yinli.one/v1")
ModelName = Literal["deepseek", "qwen", "doubao", "kimi", "mistral", "gpt"]

# 全局默认模型选择（优先级低于下方细粒度配置）
DEFAULT_STAGE_MODEL = {
    "analogical_fallback": "qwen",
    "redundancy": "doubao",
    "novel": "kimi",
}

# AnalogicalTransformer 内部不同子步骤可各自指定模型
default_role_model = "gpt5"
DEFAULT_ROLE_MODEL = {
    "extract": "doubao_1_5_pro_32k",     # 知识点提取
    "analysis": "kimi_k2",    # 可逆条件分析（analogical-3）
    "codegen": default_role_model, # 代码生成
    "check": "mistral_medium",    # 硬编码检查
    "refine": default_role_model,  # 代码精炼
    "variant": default_role_model,     # 数字/条件变体生成
    "range": default_role_model,  # 变量取值范围确定
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
        elif self.model_name == "claude_opus_4_1":
            return self._call_claude_opus_4_1(prompt, system)
        elif self.model_name == "claude_opus_4_5":
            return self._call_claude_opus_4_5(prompt, system)
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

    def _call_claude_opus_4_1(self, question: str, system: str) -> str:
        try:
            resp = claude_client.chat.completions.create(
                model="claude-opus-4-1-20250805",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": question},
                ],
                temperature=self.temperature,
                stream=False
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"调用 Claude Opus 4.1 API 时出错: {e}")
            return "❌"
        
    def _call_claude_opus_4_5(self, question: str, system: str) -> str:
        try:
            resp = claude_client.chat.completions.create(
                model="claude-opus-4-5-20251101",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": question},
                ],
                temperature=self.temperature,
                stream=False
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"调用 Claude Opus 4.5 API 时出错: {e}")
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
            "probability": [
                "P(A|B) = \\frac{P(A \\cap B)}{P(B)}  # 条件概率, A|B表示B发生下A发生", 
                "P(A \\cup B) = P(A) + P(B) - P(A \\cap B)  # 并集概率, A∪B表示A或B发生", 
                "P(A') = 1 - P(A)  # 补集概率, A'表示A不发生", 
                "P(A \\cap B) = P(A|B) \\cdot P(B)  # 交集概率, A∩B表示A和B同时发生"
            ], #概率
            "probability theory": [
                "P(A|B) = \\frac{P(A \\cap B)}{P(B)}  # 条件概率", 
                "P(A \\cup B) = P(A) + P(B) - P(A \\cap B)  # 并集概率", 
                "P(A') = 1 - P(A)  # 补集概率", 
                "P(A \\cap B) = P(A) \\cdot P(B|A)  # 乘法公式", 
                "E[X] = \\sum x_i P(x_i)  # 期望值, X为随机变量, x_i为取值"
            ], # 概率论
            "discrete probability": [
                "E[X] = \\sum_{i} x_i P(X=x_i)  # 期望值, x_i为可能取值", 
                "\\text{Var}(X) = E[X^2] - (E[X])^2  # 方差", 
                "E[X+Y] = E[X] + E[Y]  # 期望线性性", 
                "\\text{Var}(X) = E[(X-\\mu)^2]  # 方差定义, μ为期望值, μ=E[X]"
            ], # 离散概率
            "combinatorics": [
                "C(n,k) = \\frac{n!}{k!(n-k)!}  # 组合数, 从n个中选k个", 
                "P(n,k) = \\frac{n!}{(n-k)!}  # 排列数, 从n个中选k个排列", 
                "C(n,k) = C(n,n-k)  # 组合对称性", 
                "P(n,n) = n!  # 全排列", 
                "C(n,0) = C(n,n) = 1  # 边界条件",
                "C(n,k) = C(n-1,k-1) + C(n-1,k)  # 组合递推关系",
                "P_{\\text{circular}}(n) = (n-1)!  # 圆排列, n个不同元素围成圆圈的排列数, 旋转后相同的视为同一种",
                "要解方程x_1 + x_2 + \\cdots + x_k = n, x_i \\ge 0, 可以使用插板法, 想象成n个糖果分给k个人, 相当于用k-1块板子把一排n个糖果分为k段, 一共n+k-1个位置, 组合数为C(n, k-1)",
                "(a+b)^n = \\sum_{k=0}^n C(n,k) a^{n-k} b^k  # 二项式定理, n为非负整数, C(n,k)为组合数",
                "二项式系数: C(n,0) + C(n,1) + \\cdots + C(n,n) = 2^n  # 二项式系数之和",
                "|A \\cup B| = |A| + |B| - |A \\cap B|  # 两集合容斥原理",
                "|A \\cup B \\cup C| = |A| + |B| + |C| - |A \\cap B| - |A \\cap C| - |B \\cap C| + |A \\cap B \\cap C|  # 三集合容斥原理",
                "\\left|\\bigcup_{i=1}^n A_i\\right| = \\sum_{i} |A_i| - \\sum_{i<j} |A_i \\cap A_j| + \\cdots + (-1)^{n+1} |A_1 \\cap \\cdots \\cap A_n|  # n集合容斥原理"
            ], # 组合数学
            "addition principle": [
                "N = n_1 + n_2 + \\cdots + n_k  # 基本加法原理(互斥情形), 一个任务可以通过k种互不重叠的方式完成, 第i种方式有n_i种选择", 
                "如果任务可以通过若干种互不重叠的方式完成, 第i种方式有n_i种选择, 则总完成方式数为各方式选择数之和"
            ], # 加法原理
            "multiplication principle": [
                "|A \\times B| = |A| \\cdot |B|  # 乘法原理, 笛卡尔积的元素个数",
                "N = n_1 \\cdot n_2 \\cdot \\cdots \\cdot n_k  # 多步骤计数, n_i为第i步的选择数",
                "N = m \\cdot n  # 两步计数, m和n为各步选择数"
            ], # 乘法原理
            "inclusion-exclusion principle": [
                "|A \\cup B| = |A| + |B| - |A \\cap B|  # 两集合容斥原理",
                "|A \\cup B \\cup C| = |A| + |B| + |C| - |A \\cap B| - |A \\cap C| - |B \\cap C| + |A \\cap B \\cap C|  # 三集合容斥原理",
                "\\left|\\bigcup_{i=1}^n A_i\\right| = \\sum_{i} |A_i| - \\sum_{i<j} |A_i \\cap A_j| + \\cdots + (-1)^{n+1} |A_1 \\cap \\cdots \\cap A_n|  # n集合容斥原理"
            ], # 容斥原理
            "set": [
                "|A \\cup B| = |A| + |B| - |A \\cap B|  # 两集合容斥原理",
                "|A \\cup B \\cup C| = |A| + |B| + |C| - |A \\cap B| - |A \\cap C| - |B \\cap C| + |A \\cap B \\cap C|  # 三集合容斥原理",
                "\\left|\\bigcup_{i=1}^n A_i\\right| = \\sum_{i} |A_i| - \\sum_{i<j} |A_i \\cap A_j| + \\cdots + (-1)^{n+1} |A_1 \\cap \\cdots \\cap A_n|  # n集合容斥原理"
            ], # 集合
            "permutation": [
                "P(n,k) = \\frac{n!}{(n-k)!}  # 排列数, 从n个中选k个排列",
                "P(n,n) = n!  # 全排列",
                "P_{\\text{circular}}(n) = (n-1)!  # 圆排列, n个不同元素围成圆圈的排列数, 旋转后相同的视为同一种"
            ], # 排列
            "combination": [
                "C(n,k) = \\frac{n!}{k!(n-k)!}  # 组合数, 从n个中选k个",
                "C(n,k) = C(n,n-k)  # 组合对称性",
                "C(n,0) = C(n,n) = 1  # 边界条件",
                "C(n,k) = C(n-1,k-1) + C(n-1,k)  # 组合递推关系",
                "\\sum_{k=0}^n C(n,k) = 2^n  # 组合数求和",
                "要解方程x_1 + x_2 + \\cdots + x_k = n, x_i \\ge 0, 可以使用插板法, 想象成n个糖果分给k个人, 相当于用k-1块板子把一排n个糖果分为k段, 一共n+k-1个位置, 组合数为C(n, k-1)",
                "(a+b)^n = \\sum_{k=0}^n C(n,k) a^{n-k} b^k  # 二项式定理, n为非负整数, C(n,k)为组合数",
                "二项式系数: C(n,0) + C(n,1) + \\cdots + C(n,n) = 2^n  # 二项式系数之和"
            ], # 组合
            "geometry": [
                "A = \\frac{1}{2}bh  # 三角形面积, A=面积, b=底, h=高",
                "a^2 + b^2 = c^2  # 勾股定理, a和b为直角边, c为斜边",
                "A = \\frac{1}{2}ab\\sin C  # 三角形面积, a和b为两边, C为夹角",
                "A = \\sqrt{s(s-a)(s-b)(s-c)}  # 海伦公式, s为半周长, a/b/c为三边",
                "正n边形, n为边数, 所有边相等, 所有内角相等",
                "A_{\\triangle} = \\frac{1}{2}bh  # 三角形面积, b=底, h=高",
                "A_{\\text{circle}} = \\pi r^2  # 圆面积, r=半径",
                "C_{\\text{circle}} = 2\\pi r  # 圆周长, r=半径",
                "A_{\\text{rectangle}} = lw  # 矩形面积, l=长, w=宽",
                "A_{\\text{parallelogram}} = bh  # 平行四边形面积, b=底, h=高",
                "S_{\\text{int}} = (n-2)\\times 180^\\circ  # n边形内角和, 正n边形/任意n边形都适用",
                "r_{\\text{circ}} = \\frac{a}{2\\sin(180^\\circ/n)}  # 外接圆半径",
                "r_{\\text{in}} = \\frac{a}{2\\tan(180^\\circ/n)}  # 内切圆半径",
                "正n边形共有n条轴对称轴",
                "对于正n变形, 若n为偶数, 则有n/2条对称轴连接一对\"对顶点\", 另有n/2条对称轴连接一对对边的中点",
                "对于正n边形, 若n为奇数, 则每条对称轴均连接一个顶点和与其相对的一条边的中点",
                "V_{\\text{cube}} = a^3  # 正方体体积, a=边长",
                "V_{\\text{sphere}} = \\frac{4}{3}\\pi r^3  # 球体积, r=半径",
                "V_{\\text{cylinder}} = \\pi r^2 h  # 圆柱体积, r=半径, h=高",
                "S_{\\text{sphere}} = 4\\pi r^2  # 球表面积, r=半径",
                "V_{\\text{cone}} = \\frac{1}{3}\\pi r^2 h  # 圆锥体积, r=半径, h=高",
                "V_{\\text{pyramid}} = \\frac{1}{3}Bh  # 棱锥体积, B=底面积, h=高",
                "若四面体的三对对边分别相等 (AB=CD, AC=BD, AD=BC), 则该四面体与某一长方体的四个顶点一一重合；反之, 任取长方体中一个顶点及与其相邻的三个顶点组成的四面体, 其三对对边也必然分别相等。",
                "\\frac{a'}{a} = \\frac{b'}{b} = \\frac{c'}{c} = k  # 相似比, a'/a, b'/b, c'/c为相似图形对应边, k为比例",
                "\\angle A = \\angle A'  # 相似图形对应角相等",
                "\\frac{\\text{Area}'}{\\text{Area}} = k^2  # 相似图形面积比等于相似比平方",
                "两个直角三角形中：如果它们各有一个锐角相等，则这两个直角三角形相似",
                "两个三角形有两个角相等，则这两个三角形相似",
                "如果两个三角形三边都相等, 则这两个三角形全等",
                "如果两个三角形两边和夹角都相等, 则这两个三角形全等",
                "如果两个三角形两角和夹边都相等, 则这两个三角形全等",
                "V_{\\text{cube}} = a^3  # 正方体体积, a=边长",
                "V_{\\text{sphere}} = \\frac{4}{3}\\pi r^3  # 球体积, r=半径",
                "V_{\\text{cylinder}} = \\pi r^2 h  # 圆柱体积, r=半径, h=高",
                "S_{\\text{sphere}} = 4\\pi r^2  # 球表面积, r=半径",
                "V_{\\text{cone}} = \\frac{1}{3}\\pi r^2 h  # 圆锥体积, r=半径, h=高",
                "V_{\\text{pyramid}} = \\frac{1}{3}Bh  # 棱锥体积, B=底面积, h=高",
                "若四面体的三对对边分别相等 (AB=CD, AC=BD, AD=BC), 则该四面体与某一长方体的四个顶点一一重合；反之, 任取长方体中一个顶点及与其相邻的三个顶点组成的四面体, 其三对对边也必然分别相等。",
                "A = \\pi r^2  # 圆面积, r=半径",
                "C = 2\\pi r  # 圆周长, r=半径",
                "(x-h)^2 + (y-k)^2 = r^2  # 圆方程, (h,k)=圆心, r=半径",
                "s = r\\theta  # 弧长, r=半径, θ=圆心角(弧度)",
                "A_{\\text{sector}} = \\frac{1}{2}r^2\\theta  # 扇形面积, r=半径, θ=圆心角",
                "A_{\\text{segment}} = \\frac{1}{2}r^2(\\theta - \\sin\\theta)  # 弓形面积",
                "r_{\\text{circ}} = \\frac{a}{2\\sin(180^\\circ/n)}  # 外接圆半径",
                "r_{\\text{in}} = \\frac{a}{2\\tan(180^\\circ/n)}  # 内切圆半径",
                "在三角形的一个角内, 若一个圆与两边相切, 则其圆心落在该角的角平分线上, 且该圆的圆心到与之相切的三角形两边的距离都等于圆的半径",
                "如果两个圆相切，则它们的圆心距等于两个圆的半径之和或差",
                "圆周角定理: 在同一圆中，对同一条弧的圆周角相等, 且等于该弧所对的圆心角的一半",
                "三角形内心和外心之间距离的欧拉公式: OI^2 = R^2 - 2Rr",
                "弦切角定理: 弦切角（圆上的点与弦及切线形成的角）的度数等于它所夹的弧所对的圆心角度数的一半，等于它所夹的弧所对的圆周角度数",
                "从圆外一点P引两条割线与圆分别交于A,B和C,D, 则PA \\cdot PB = PC \\cdot PD  # 割线定理",
                "从圆外一点P引一条割线与圆分别交于A,B和一条切线与圆分别交于C, 则PA \\cdot PB = PC^2  # 割线-切线定理",
                "圆内两条相交弦, 被交点分成的两段的乘积相等  #相交弦定理",
                "托勒密定理: 圆内接四边形的两对对边乘积之和等于其对角线乘积",
                "如果圆心到直线的距离等于圆的半径, 则直线与圆相切",
                "从圆外一点P作圆的两条切线PA和PB, 则PA=PB",
                "切线与半径垂直",
                "弦切角定理: 弦切角（圆上的点与弦及切线形成的角）的度数等于它所夹的弧所对的圆心角度数的一半，等于它所夹的弧所对的圆周角度数",
                "从圆外一点P引两条割线与圆分别交于A,B和C,D, 则PA \\cdot PB = PC \\cdot PD  # 割线定理",
                "从圆外一点P引一条割线与圆分别交于A,B和一条切线与圆分别交于C, 则PA \\cdot PB = PC^2  # 割线-切线定理",
                "圆内两条相交弦, 被交点分成的两段的乘积相等  #相交弦定理",
                "弦切角定理: 弦切角（圆上的点与弦及切线形成的角）的度数等于它所夹的弧所对的圆心角度数的一半，等于它所夹的弧所对的圆周角度数"
                "托勒密定理: 圆内接四边形的两对对边乘积之和等于其对角线乘积",
                "阿波罗尼乌斯定理: 设M是三角形ABC中BC边的中点, 则 AB^2+AC^2 = 2(AM^2+BM^2)"
            ], # 几何
            "plane geometry": [
                "A_{\\triangle} = \\frac{1}{2}bh  # 三角形面积, b=底, h=高",
                "A_{\\text{circle}} = \\pi r^2  # 圆面积, r=半径",
                "C_{\\text{circle}} = 2\\pi r  # 圆周长, r=半径",
                "A_{\\text{rectangle}} = lw  # 矩形面积, l=长, w=宽",
                "A_{\\text{parallelogram}} = bh  # 平行四边形面积, b=底, h=高",
                "S_{\\text{int}} = (n-2)\\times 180^\\circ  # n边形内角和, 正n边形/任意n边形都适用",
                "r_{\\text{circ}} = \\frac{a}{2\\sin(180^\\circ/n)}  # 外接圆半径",
                "r_{\\text{in}} = \\frac{a}{2\\tan(180^\\circ/n)}  # 内切圆半径",
                "正n边形共有n条轴对称轴",
                "对于正n变形, 若n为偶数, 则有n/2条对称轴连接一对\"对顶点\", 另有n/2条对称轴连接一对对边的中点",
                "对于正n边形, 若n为奇数, 则每条对称轴均连接一个顶点和与其相对的一条边的中点"
            ], # 平面几何
            "solid geometry": [
                "V_{\\text{cube}} = a^3  # 正方体体积, a=边长",
                "V_{\\text{sphere}} = \\frac{4}{3}\\pi r^3  # 球体积, r=半径",
                "V_{\\text{cylinder}} = \\pi r^2 h  # 圆柱体积, r=半径, h=高",
                "S_{\\text{sphere}} = 4\\pi r^2  # 球表面积, r=半径",
                "V_{\\text{cone}} = \\frac{1}{3}\\pi r^2 h  # 圆锥体积, r=半径, h=高",
                "V_{\\text{pyramid}} = \\frac{1}{3}Bh  # 棱锥体积, B=底面积, h=高",
                "若四面体的三对对边分别相等 (AB=CD, AC=BD, AD=BC), 则该四面体与某一长方体的四个顶点一一重合；反之, 任取长方体中一个顶点及与其相邻的三个顶点组成的四面体, 其三对对边也必然分别相等。"
            ], # 立体几何
            "3D geometry": [
                "V_{\\text{cube}} = a^3  # 正方体体积, a=边长",
                "V_{\\text{sphere}} = \\frac{4}{3}\\pi r^3  # 球体积, r=半径",
                "V_{\\text{cylinder}} = \\pi r^2 h  # 圆柱体积, r=半径, h=高",
                "S_{\\text{sphere}} = 4\\pi r^2  # 球表面积, r=半径",
                "V_{\\text{cone}} = \\frac{1}{3}\\pi r^2 h  # 圆锥体积, r=半径, h=高",
                "V_{\\text{pyramid}} = \\frac{1}{3}Bh  # 棱锥体积, B=底面积, h=高",
                "若四面体的三对对边分别相等 (AB=CD, AC=BD, AD=BC), 则该四面体与某一长方体的四个顶点一一重合；反之, 任取长方体中一个顶点及与其相邻的三个顶点组成的四面体, 其三对对边也必然分别相等。"
            ], # 立体3D几何
            "tetrahedron": [
                "V = \\frac{1}{6}|\\det(\\vec{AB}, \\vec{AC}, \\vec{AD})|  # 四面体体积, A/B/C/D为四个顶点", 
                "V = \\frac{a^3}{6\\sqrt{2}}  # 正四面体体积, a为棱长", 
                "V = \\frac{1}{3}Bh  # 棱锥体积, B为底面积, h为高",
                "若四面体的三对对边分别相等 (AB=CD, AC=BD, AD=BC), 则该四面体与某一长方体的四个顶点一一重合；反之, 任取长方体中一个顶点及与其相邻的三个顶点组成的四面体, 其三对对边也必然分别相等。"
            ], # 四面体
            "Pythagorean theorem": [
                "a^2 + b^2 = c^2  # 勾股定理, a和b为直角边, c为斜边",
                "c = \\sqrt{a^2 + b^2}  # 求斜边",
                "a = \\sqrt{c^2 - b^2}  # 求直角边a"
            ], # 勾股定理
            "law of cosines": [
                "c^2 = a^2 + b^2 - 2ab\\cos C  # 余弦定理, a/b/c为三角形三边, C为c的对角",
                "\\cos C = \\frac{a^2 + b^2 - c^2}{2ab}  # 余弦定理求角"
            ], # 余弦定理
            "law of sines": [
                "\\frac{a}{\\sin A} = \\frac{b}{\\sin B} = \\frac{c}{\\sin C} = 2R  # 正弦定理, a为角A的对边, b为角B的对边, c为角C的对边, R为外接圆半径",
                "a = 2R\\sin A  # 边与角关系, R为外接圆半径, a为角A的对边",
                "b = 2R\\sin B"
            ], # 正弦定理
            "trigonometric function": [
                "\\sin^2\\theta + \\cos^2\\theta = 1  # 三角恒等式, θ为角度",
                "\\tan\\theta = \\frac{\\sin\\theta}{\\cos\\theta}  # 正切定义",
                "\\sin(A\\pm B) = \\sin A\\cos B \\pm \\cos A\\sin B  # 正弦和差公式",
                "\\cos(A\\pm B) = \\cos A\\cos B \\mp \\sin A\\sin B  # 余弦和差公式",
                "\\tan(A\\pm B) = \\frac{\\tan A \\pm \\tan B}{1 \\mp \\tan A\\tan B}  # 正切和差公式",
                "\\sin(2\\theta) = 2\\sin\\theta\\cos\\theta  # 倍角公式",
                "c^2 = a^2 + b^2 - 2ab\\cos C  # 余弦定理, a/b/c为三角形三边, C为c的对角",
                "\\frac{a}{\\sin A} = \\frac{b}{\\sin B} = \\frac{c}{\\sin C} = 2R  # 正弦定理, a为角A的对边, b为角B的对边, c为角C的对边, R为外接圆半径",
                "三角形内心和外心之间距离的欧拉公式: OI^2 = R^2 - 2Rr",
                "三角形面积公式: A = \\frac{1}{2}ab\\sin C",
                "阿波罗尼乌斯定理: 设M是三角形ABC中BC边的中点, 则 AB^2+AC^2 = 2(AM^2+BM^2)"
            ], # 三角函数
            "trigonometry": [
                "\\sin^2\\theta + \\cos^2\\theta = 1  # 三角恒等式, θ为角度",
                "\\tan\\theta = \\frac{\\sin\\theta}{\\cos\\theta}  # 正切定义",
                "\\sin(A\\pm B) = \\sin A\\cos B \\pm \\cos A\\sin B  # 正弦和差公式",
                "\\cos(A\\pm B) = \\cos A\\cos B \\mp \\sin A\\sin B  # 余弦和差公式",
                "\\tan(A\\pm B) = \\frac{\\tan A \\pm \\tan B}{1 \\mp \\tan A\\tan B}  # 正切和差公式",
                "\\sin(2\\theta) = 2\\sin\\theta\\cos\\theta  # 倍角公式",
                "c^2 = a^2 + b^2 - 2ab\\cos C  # 余弦定理, a/b/c为三角形三边, C为c的对角",
                "\\frac{a}{\\sin A} = \\frac{b}{\\sin B} = \\frac{c}{\\sin C} = 2R  # 正弦定理, a为角A的对边, b为角B的对边, c为角C的对边, R为外接圆半径",
                "三角形内心和外心之间距离的欧拉公式: OI^2 = R^2 - 2Rr",
                "三角形面积公式: A = \\frac{1}{2}ab\\sin C"
            ], # 三角学
            "sinusoidal function": [
                "正弦函数 y = \\sin x 的定义域为全体实数, 值域为[-1, 1], 周期为2π, 为奇函数  # 正弦函数基本性质",
                "\\sin^2\\theta + \\cos^2\\theta = 1  # 三角恒等式, θ为角度",
                "\\tan\\theta = \\frac{\\sin\\theta}{\\cos\\theta}  # 正切定义",
                "\\sin(A\\pm B) = \\sin A\\cos B \\pm \\cos A\\sin B  # 正弦和差公式",
                "\\cos(A\\pm B) = \\cos A\\cos B \\mp \\sin A\\sin B  # 余弦和差公式",
                "\\sin(2\\theta) = 2\\sin\\theta\\cos\\theta  # 倍角公式",
                "\\frac{a}{\\sin A} = \\frac{b}{\\sin B} = \\frac{c}{\\sin C} = 2R  # 正弦定理, a为角A的对边, b为角B的对边, c为角C的对边, R为外接圆半径",
                "三角形面积公式: A = \\frac{1}{2}ab\\sin C",
                "\\sin(x+2\\pi) = \\sin x  # 正弦函数周期为2π",
                "\\sin(x+\\pi) = -\\sin x  # 正弦函数半周期性质",
                "\\sin(x+\\frac{\\pi}{2}) = \\cos x  # 正弦与余弦的相位关系",
                "\\sin(x+2k\\pi) = \\sin x  # 正弦函数整数倍周期, k为整数",
                "sin(ax+b)的周期为\\frac{2\\pi}{a}  # 正弦函数周期"
            ], # 正弦形周期函数
            "sine function": [
                "正弦函数 y = \\sin x 的定义域为全体实数, 值域为[-1, 1], 周期为2π, 为奇函数  # 正弦函数基本性质",
                "\\sin^2\\theta + \\cos^2\\theta = 1  # 三角恒等式, θ为角度",
                "\\tan\\theta = \\frac{\\sin\\theta}{\\cos\\theta}  # 正切定义",
                "\\sin(A\\pm B) = \\sin A\\cos B \\pm \\cos A\\sin B  # 正弦和差公式",
                "\\cos(A\\pm B) = \\cos A\\cos B \\mp \\sin A\\sin B  # 余弦和差公式",
                "\\sin(2\\theta) = 2\\sin\\theta\\cos\\theta  # 倍角公式",
                "\\frac{a}{\\sin A} = \\frac{b}{\\sin B} = \\frac{c}{\\sin C} = 2R  # 正弦定理, a为角A的对边, b为角B的对边, c为角C的对边, R为外接圆半径",
                "三角形面积公式: A = \\frac{1}{2}ab\\sin C",
                "\\sin(x+2\\pi) = \\sin x  # 正弦函数周期为2π",
                "\\sin(x+\\pi) = -\\sin x  # 正弦函数半周期性质",
                "\\sin(x+\\frac{\\pi}{2}) = \\cos x  # 正弦与余弦的相位关系",
                "\\sin(x+2k\\pi) = \\sin x  # 正弦函数整数倍周期, k为整数",
                "sin(ax+b)的周期为\\frac{2\\pi}{a}  # 正弦函数周期"
            ], # 正弦函数
            "cosinusoidal function": [
                "余弦函数 y = \\cos x 的定义域为全体实数, 值域为[-1, 1], 周期为2π, 为偶函数  # 余弦函数基本性质",
                "\\sin^2\\theta + \\cos^2\\theta = 1  # 三角恒等式, θ为角度",
                "\\tan\\theta = \\frac{\\sin\\theta}{\\cos\\theta}  # 正切定义",
                "\\sin(A\\pm B) = \\sin A\\cos B \\pm \\cos A\\sin B  # 正弦和差公式",
                "\\cos(A\\pm B) = \\cos A\\cos B \\mp \\sin A\\sin B  # 余弦和差公式",
                "\\sin(2\\theta) = 2\\sin\\theta\\cos\\theta  # 倍角公式",
                "c^2 = a^2 + b^2 - 2ab\\cos C  # 余弦定理, a/b/c为三角形三边, C为c的对角",
                "\\cos(x+2\\pi) = \\cos x  # 余弦函数周期为2π",
                "\\cos(x+\\pi) = -\\cos x  # 余弦函数半周期性质",
                "\\cos(x+\\frac{\\pi}{2}) = -\\sin x  # 余弦与正弦的相位关系",
                "\\cos(x+2k\\pi) = \\cos x  # 余弦函数整数倍周期, k为整数",
                "cos(ax+b)的周期为\\frac{2\\pi}{a}  # 余弦函数周期"
            ], # 余弦形周期函数
            "cosine function": [
                "余弦函数 y = \\cos x 的定义域为全体实数, 值域为[-1, 1], 周期为2π, 为偶函数  # 余弦函数基本性质",
                "\\sin^2\\theta + \\cos^2\\theta = 1  # 三角恒等式, θ为角度",
                "\\tan\\theta = \\frac{\\sin\\theta}{\\cos\\theta}  # 正切定义",
                "\\sin(A\\pm B) = \\sin A\\cos B \\pm \\cos A\\sin B  # 正弦和差公式",
                "\\cos(A\\pm B) = \\cos A\\cos B \\mp \\sin A\\sin B  # 余弦和差公式",
                "\\sin(2\\theta) = 2\\sin\\theta\\cos\\theta  # 倍角公式",
                "c^2 = a^2 + b^2 - 2ab\\cos C  # 余弦定理, a/b/c为三角形三边, C为c的对角",
                "\\cos(x+2\\pi) = \\cos x  # 余弦函数周期为2π",
                "\\cos(x+\\pi) = -\\cos x  # 余弦函数半周期性质",
                "\\cos(x+\\frac{\\pi}{2}) = -\\sin x  # 余弦与正弦的相位关系",
                "\\cos(x+2k\\pi) = \\cos x  # 余弦函数整数倍周期, k为整数",
                "cos(ax+b)的周期为\\frac{2\\pi}{a}  # 余弦函数周期"
            ], # 余弦函数
            "function period": [
                "f(x+T) = f(x)  # 周期函数定义, T为周期",
                "\\sin(x+2\\pi) = \\sin x  # 正弦函数周期为2π",
                "\\cos(x+2\\pi) = \\cos x  # 余弦函数周期为2π",
                "\\tan(x+\\pi) = \\tan x  # 正切函数周期为π",
                "f(x+nT) = f(x) \\text{ for } n \\in \\mathbb{Z}  # 周期函数的整数倍周期",
                "\\sin(x+\\pi) = -\\sin x  # 正弦函数半周期性质",
                "\\cos(x+\\pi) = -\\cos x  # 余弦函数半周期性质",
                "\\sin(x+\\frac{\\pi}{2}) = \\cos x  # 正弦与余弦的相位关系",
                "\\cos(x+\\frac{\\pi}{2}) = -\\sin x  # 余弦与正弦的相位关系",
                "\\sin(x+2k\\pi) = \\sin x  # 正弦函数整数倍周期, k为整数",
                "\\cos(x+2k\\pi) = \\cos x  # 余弦函数整数倍周期, k为整数",
                "如果函数f(x)有周期T, 则f(ax+b)的周期为\\frac{T}{|a|}  # 周期函数的伸缩变换",
                "sin(ax+b)的周期为\\frac{2\\pi}{a}  # 正弦函数周期",
                "cos(ax+b)的周期为\\frac{2\\pi}{a}  # 余弦函数周期"
            ], # 函数周期
            "similarity": [
                "\\frac{a'}{a} = \\frac{b'}{b} = \\frac{c'}{c} = k  # 相似比, a'/a, b'/b, c'/c为相似图形对应边, k为比例",
                "\\angle A = \\angle A'  # 相似图形对应角相等",
                "\\frac{\\text{Area}'}{\\text{Area}} = k^2  # 相似图形面积比等于相似比平方",
                "两个直角三角形中：如果它们各有一个锐角相等，则这两个直角三角形相似"
            ], # 相似
            "similar triangles": [
                "\\frac{AB}{A'B'} = \\frac{BC}{B'C'} = \\frac{AC}{A'C'}  # 相似三角形对应边成比例",
                "\\angle A = \\angle A', \\angle B = \\angle B'  # 相似三角形对应角相等",
                "\\frac{S}{S'} = \\left(\\frac{a}{a'}\\right)^2  # 相似三角形面积比等于边长比平方",
                "两个直角三角形中：如果它们各有一个锐角相等，则这两个直角三角形相似",
                "两个三角形有两个角相等，则这两个三角形相似",
                "如果两个三角形三边都相等, 则这两个三角形全等",
                "如果两个三角形两边和夹角都相等, 则这两个三角形全等",
                "如果两个三角形两角和夹边都相等, 则这两个三角形全等"
            ], # 相似三角形
            "circle": [
                "A = \\pi r^2  # 圆面积, r=半径",
                "C = 2\\pi r  # 圆周长, r=半径",
                "(x-h)^2 + (y-k)^2 = r^2  # 圆方程, (h,k)=圆心, r=半径",
                "s = r\\theta  # 弧长, r=半径, θ=圆心角(弧度)",
                "A_{\\text{sector}} = \\frac{1}{2}r^2\\theta  # 扇形面积, r=半径, θ=圆心角",
                "A_{\\text{segment}} = \\frac{1}{2}r^2(\\theta - \\sin\\theta)  # 弓形面积",
                "r_{\\text{circ}} = \\frac{a}{2\\sin(180^\\circ/n)}  # 外接圆半径",
                "r_{\\text{in}} = \\frac{a}{2\\tan(180^\\circ/n)}  # 内切圆半径",
                "在三角形的一个角内, 若一个圆与两边相切, 则其圆心落在该角的角平分线上, 且该圆的圆心到与之相切的三角形两边的距离都等于圆的半径",
                "如果两个圆相切，则它们的圆心距等于两个圆的半径之和或差",
                "圆周角定理: 在同一圆中，对同一条弧的圆周角相等, 且等于该弧所对的圆心角的一半",
                "三角形内心和外心之间距离的欧拉公式: OI^2 = R^2 - 2Rr",
                "弦切角定理: 弦切角（圆上的点与弦及切线形成的角）的度数等于它所夹的弧所对的圆心角度数的一半，等于它所夹的弧所对的圆周角度数",
                "从圆外一点P引两条割线与圆分别交于A,B和C,D, 则PA \\cdot PB = PC \\cdot PD  # 割线定理",
                "从圆外一点P引一条割线与圆分别交于A,B和一条切线与圆分别交于C, 则PA \\cdot PB = PC^2  # 割线-切线定理",
                "圆内两条相交弦, 被交点分成的两段的乘积相等  #相交弦定理",
                "托勒密定理: 圆内接四边形的两对对边乘积之和等于其对角线乘积"
            ], # 圆
            "tangent": [
                "如果圆心到直线的距离等于圆的半径, 则直线与圆相切",
                "从圆外一点P作圆的两条切线PA和PB, 则PA=PB",
                "切线与半径垂直",
                "弦切角定理: 弦切角（圆上的点与弦及切线形成的角）的度数等于它所夹的弧所对的圆心角度数的一半，等于它所夹的弧所对的圆周角度数",
            ], # 切线
            "power of a pointtheorem": [
                "从圆外一点P引两条割线与圆分别交于A,B和C,D, 则PA \\cdot PB = PC \\cdot PD  # 割线定理",
                "从圆外一点P引一条割线与圆分别交于A,B和一条切线与圆分别交于C, 则PA \\cdot PB = PC^2  # 割线-切线定理",
                "圆内两条相交弦, 被交点分成的两段的乘积相等  #相交弦定理",
                "弦切角定理: 弦切角（圆上的点与弦及切线形成的角）的度数等于它所夹的弧所对的圆心角度数的一半，等于它所夹的弧所对的圆周角度数"
                "托勒密定理: 圆内接四边形的两对对边乘积之和等于其对角线乘积"
            ], # 圆幂定理
            "hyperbola": [
                "\\frac{x^2}{a^2} - \\frac{y^2}{b^2} = 1  # 双曲线标准方程, a和b为半轴长",
                "c^2 = a^2 + b^2  # 焦距关系, c为焦距, a和b为半轴长",
                "F_1 = (c, 0), F_2 = (-c, 0)  # 双曲线焦点坐标",
                "y = \\pm \\frac{b}{a}x  # 双曲线渐近线方程, a和b为半轴长",
                "e = \\frac{c}{a} > 1  # e为离心率, c为焦距, a为半轴长"
            ], # 双曲线
            "parabola": [
                "y = ax^2 + bx + c  # 抛物线一般式, a≠0", 
                "y = a(x-h)^2 + k  # 顶点式, (h,k)为顶点", 
                "x^2 = 4py  # 标准形式, p为焦距", 
                "抛物线 y = ax^2 + bx + c 的顶点为(h,k) = \\left(-\\frac{b}{2a}, \\frac{4ac-b^2}{4a}\\right)"
            ], # 抛物线
            "algebra": [
                "二次方程 ax²+bx+c=0 的根为 x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}",
                "(a+b)^2 = a^2 + 2ab + b^2  # 完全平方公式",
                "a^2 - b^2 = (a+b)(a-b)  # 平方差公式",
                "有理根定理: 对于多项式 a_n x^n + a_{n-1} x^{n-1} + \\cdots + a_1 x + a_0 = 0, 若有理根为 \\frac{p}{q} (p和q互质), 则 p \\mid a_0 且 q \\mid a_n  # 有理根定理, p整除常数项, q整除首项系数",
                "韦达定理(二次方程): 对于 ax^2+bx+c=0, 若根为 x_1 和 x_2, 则 x_1 + x_2 = -\\frac{b}{a}, x_1 \\cdot x_2 = \\frac{c}{a}  # 二次方程根与系数关系",
                "韦达定理(三次方程): 对于 ax^3+bx^2+cx+d=0, 若根为 x_1, x_2, x_3, 则 x_1+x_2+x_3 = -\\frac{b}{a}, x_1x_2+x_1x_3+x_2x_3 = \\frac{c}{a}, x_1x_2x_3 = -\\frac{d}{a}  # 三次方程根与系数关系",
                "利用单位根进行多项式因式分解: x^n - 1 = (x-1)(x-\\omega)(x-\\omega^2)\\cdots(x-\\omega^{n-1})  # 其中\\omega为n次本原单位根, \\omega^k (k=0,1,\\ldots,n-1)为所有n次单位根",
                "利用单位根进行多项式因式分解(一般形式): 对于复数a, a^n - 1 = \\prod_{k=0}^{n-1} (a - \\omega^k)  # 其中\\omega为n次本原单位根, \\omega^k为所有n次单位根",
                "n次单位根: 满足 z^n = 1 的复数z, 共有n个不同的单位根",
                "n次单位根的形式: \\omega_k = e^{\\frac{2\\pi ik}{n}} = \\cos\\frac{2\\pi k}{n} + i\\sin\\frac{2\\pi k}{n}, k = 0,1,\\ldots,n-1  # 单位根的指数形式和三角形式",
                "本原n次单位根: 若\\omega是n次单位根, 且\\omega^m \\neq 1 对所有 1 \\leq m < n 成立, 则\\omega为本原n次单位根",
                "所有n次单位根的和为0: 1 + \\omega + \\omega^2 + \\cdots + \\omega^{n-1} = 0  # 其中\\omega为任一n次本原单位根"
            ], # 代数
            "algebraic identity": [
                "(a+b)^2 = a^2 + 2ab + b^2  # 完全平方和",
                "(a-b)^2 = a^2 - 2ab + b^2  # 完全平方差",
                "a^2 - b^2 = (a+b)(a-b)  # 平方差公式",
                "a^3 + b^3 = (a+b)(a^2-ab+b^2)  # 立方和公式",
                "a^3 - b^3 = (a-b)(a^2+ab+b^2)  # 立方差公式",
                "(a+b)^3 = a^3 + 3a^2b + 3ab^2 + b^3  # 完全立方和"
            ], # 代数恒等式
            "complex": [
                "对于复数z=a+bi, 它的模长|z|为 \\sqrt{a^2 + b^2}",
                "z = r(\\cos \\theta + i\\sin \\theta)  # 复数三角形式, r为模, θ为幅角",
                "z = re^{i\\theta}  # 复数指数形式, r为模, θ为幅角",
                "z \\cdot \\bar{z} = |z|^2  # 复数与其共轭乘积, \\bar{z}为z的共轭",
                "n次单位根: 满足 z^n = 1 的复数z, 共有n个不同的单位根",
                "利用单位根进行多项式因式分解: x^n - 1 = (x-1)(x-\\omega)(x-\\omega^2)\\cdots(x-\\omega^{n-1})  # 其中\\omega为n次本原单位根, \\omega^k (k=0,1,\\ldots,n-1)为所有n次单位根",
                "n次单位根的形式: \\omega_k = e^{\\frac{2\\pi ik}{n}} = \\cos\\frac{2\\pi k}{n} + i\\sin\\frac{2\\pi k}{n}, k = 0,1,\\ldots,n-1  # 单位根的指数形式和三角形式",
                "本原n次单位根: 若\\omega是n次单位根, 且\\omega^m \\neq 1 对所有 1 \\leq m < n 成立, 则\\omega为本原n次单位根",
                "所有n次单位根的和为0: 1 + \\omega + \\omega^2 + \\cdots + \\omega^{n-1} = 0  # 其中\\omega为任一n次本原单位根",
                "z = a + bi 的共轭为 \\bar{z} = a - bi, 反之亦然",
                "z \\cdot \\bar{z} = |z|^2  # 复数与其共轭的乘积等于模的平方",
                "z + \\bar{z} = 2\\text{Re}(z)  # 复数与其共轭的和等于2倍实部",
                "z - \\bar{z} = 2i\\text{Im}(z)  # 复数与其共轭的差等于2i倍虚部",
                "\\overline{z_1 + z_2} = \\bar{z_1} + \\bar{z_2}  # 和的共轭等于共轭的和",
                "\\overline{z_1 z_2} = \\bar{z_1} \\cdot \\bar{z_2}  # 积的共轭等于共轭的积"
            ], # 复数
            "conjugate": [
                "z = a + bi 的共轭为 \\bar{z} = a - bi, 反之亦然",
                "z \\cdot \\bar{z} = |z|^2  # 复数与其共轭的乘积等于模的平方",
                "z + \\bar{z} = 2\\text{Re}(z)  # 复数与其共轭的和等于2倍实部",
                "z - \\bar{z} = 2i\\text{Im}(z)  # 复数与其共轭的差等于2i倍虚部",
                "\\overline{z_1 + z_2} = \\bar{z_1} + \\bar{z_2}  # 和的共轭等于共轭的和",
                "\\overline{z_1 z_2} = \\bar{z_1} \\cdot \\bar{z_2}  # 积的共轭等于共轭的积"
            ], # 共轭
            "logarithm": [
                "\\log_a(b) = c \\iff a^c = b  # 对数定义, a为底数, b为真数, c为对数",
                "\\log(ab) = \\log(a) + \\log(b)  # 对数乘法法则",
                "\\log\\left(\\frac{a}{b}\\right) = \\log(a) - \\log(b)  # 对数除法法则",
                "\\log(a^n) = n\\log(a)  # 对数幂法则",
                "\\log_a(a) = 1  # 底数对数",
                "\\log_a(1) = 0  # 1的对数",
                "\\log_a(b)\\log_b(c) = \\log_a(c)  # 换底公式",
                "\\log_a(b)\\log_b(a) = 1  # 对数恒等式"
            ], # 对数
            "exponent": [
                "a^m \\cdot a^n = a^{m+n}  # 同底数幂相乘",
                "(a^m)^n = a^{mn}  # 幂的乘方",
                "\\frac{a^m}{a^n} = a^{m-n}  # 同底数幂相除",
                "a^0 = 1  # 零次幂",
                "a^{-n} = \\frac{1}{a^n}  # 负指数幂",
                "(ab)^n = a^n b^n  # 积的乘方"
            ], # 指数，幂
            "modular arithmetic": [
                "a \\equiv b \\pmod{m} \\iff m \\mid (a-b)  # 同余定义, m为模数",
                "(a+b) \\bmod m = ((a \\bmod m) + (b \\bmod m)) \\bmod m  # 同余加法",
                "(a \\cdot b) \\bmod m = ((a \\bmod m) \\cdot (b \\bmod m)) \\bmod m  # 同余乘法",
                "a \\equiv b \\pmod{m} \\implies a^n \\equiv b^n \\pmod{m}  # 同余幂",
                "费马小定理: 对于质数p, 任意整数a, 有a^p \\equiv a \\pmod{p}",
                "费马小定理: 对于质数p, 任意整数a, 有a^(p-1) \\equiv 1 \\pmod{p}",
                "欧拉定理: 对于任意整数a和n互质, 有a^φ(n) \\equiv 1 \\pmod{n}. φ(n)为欧拉函数, 表示小于n且与n互质的正整数个数",
                "威尔逊定理: 对于质数p, 有(p-1)! \\equiv -1 \\pmod{p}"
            ], # 模运算
            "divisibility": [
                "a \\mid b \\iff b = ka \\text{ for some } k \\in \\mathbb{Z}  # 整除定义, a整除b",
                "a \\mid b \\land b \\mid c \\implies a \\mid c  # 整除传递性",
                "a \\mid b \\land a \\mid c \\implies a \\mid (bx+cy)  # 整除线性组合"
            ], # 整除
            "congruence": [
                "a \\equiv b \\pmod{m} \\iff m \\mid (a-b)  # 同余定义, m为模数",
                "a \\equiv b \\pmod{m} \\land c \\equiv d \\pmod{m} \\implies a+c \\equiv b+d \\pmod{m}  # 同余加法",
                "a \\equiv b \\pmod{m} \\implies a^n \\equiv b^n \\pmod{m}  # 同余幂",
                "a \\equiv b \\pmod{m} \\land c \\equiv d \\pmod{m} \\implies ac \\equiv bd \\pmod{m}  # 同余乘法",
                "费马小定理: 对于质数p, 任意整数a, 有a^p \\equiv a \\pmod{p}",
                "费马小定理: 对于质数p, 任意整数a, 有a^(p-1) \\equiv 1 \\pmod{p}",
                "欧拉定理: 对于任意整数a和n互质, 有a^φ(n) \\equiv 1 \\pmod{n}. φ(n)为欧拉函数, 表示小于n且与n互质的正整数个数",
                "威尔逊定理: 对于质数p, 有(p-1)! \\equiv -1 \\pmod{p}"
            ], # 同余
            "derivative": [
                "\\frac{d}{dx}(x^n) = nx^{n-1}  # 幂函数导数, n为常数",
                "\\frac{d}{dx}(e^x) = e^x  # 指数函数e^x的导数",
                "\\frac{d}{dx}(a^x) = a^x \\ln a  # 指数函数a^x的导数, a>0且a≠1",
                "\\frac{d}{dx}(\\ln x) = \\frac{1}{x}  # 自然对数导数, x>0",
                "\\frac{d}{dx}(\\log_a x) = \\frac{1}{x \\ln a}  # 对数函数导数, a>0且a≠1, x>0",
                "\\frac{d}{dx}(\\sin x) = \\cos x  # 正弦函数导数",
                "\\frac{d}{dx}(\\cos x) = -\\sin x  # 余弦函数导数",
                "\\frac{d}{dx}(\\tan x) = \\sec^2 x  # 正切函数导数",
                "\\frac{d}{dx}(\\cot x) = -\\csc^2 x  # 余切函数导数",
                "\\frac{d}{dx}(\\sec x) = \\sec x \\tan x  # 正割函数导数",
                "\\frac{d}{dx}(\\csc x) = -\\csc x \\cot x  # 余割函数导数",
                "\\frac{d}{dx}(\\arcsin x) = \\frac{1}{\\sqrt{1-x^2}}  # 反正弦函数导数, |x|<1",
                "\\frac{d}{dx}(\\arccos x) = -\\frac{1}{\\sqrt{1-x^2}}  # 反余弦函数导数, |x|<1",
                "\\frac{d}{dx}(\\arctan x) = \\frac{1}{1+x^2}  # 反正切函数导数",
                "\\frac{d}{dx}[f(x) + g(x)] = f'(x) + g'(x)  # 和函数导数",
                "\\frac{d}{dx}[f(x) - g(x)] = f'(x) - g'(x)  # 差函数导数",
                "\\frac{d}{dx}[cf(x)] = cf'(x)  # 常数倍函数导数, c为常数",
                "\\frac{d}{dx}[f(x)g(x)] = f'(x)g(x) + f(x)g'(x)  # 乘积法则",
                "\\frac{d}{dx}\\left[\\frac{f(x)}{g(x)}\\right] = \\frac{f'(x)g(x) - f(x)g'(x)}{[g(x)]^2}  # 商法则, g(x)≠0",
                "\\frac{d}{dx}[f(g(x))] = f'(g(x)) \\cdot g'(x)  # 链式法则, 复合函数导数",
                "\\frac{d}{dx}[f(x)]^n = n[f(x)]^{n-1} \\cdot f'(x)  # 幂函数复合导数",
                "若f'(x) > 0, 则f(x)在该区间单调递增  # 导数与单调性",
                "若f'(x) < 0, 则f(x)在该区间单调递减  # 导数与单调性",
                "若f'(x_0) = 0且f''(x_0) > 0, 则x_0为极小值点  # 极值判定",
                "若f'(x_0) = 0且f''(x_0) < 0, 则x_0为极大值点  # 极值判定"
            ], # 导数
            "number base": [
                "a_na_{n-1}\\ldots a_1a_0_{(b)} = \\sum_{i=0}^n a_i b^i  # b进制转十进制, a_i为各位数字, b为进制",
                "十进制转换为b进制: 除以b取余数, 直到商为0, 余数从下到上排列",
            ], # 进制
            "enumeration": [
                "\\sum_{i=1}^n i = \\frac{n(n+1)}{2}  # 自然数求和",
                "\\sum_{i=1}^n i^2 = \\frac{n(n+1)(2n+1)}{6}  # 平方数求和",
                "\\sum_{i=1}^n i^3 = \\left(\\frac{n(n+1)}{2}\\right)^2  # 立方数求和"
            ], # 枚举
            "prime factorization": [
                "n = p_1^{e_1} p_2^{e_2} \\cdots p_k^{e_k}  # 质因数分解, p_i为质数, e_i为指数",
                "唯一分解定理: 任何大于1的整数都可以唯一分解成质因数的乘积。",
                "\\gcd(a,b) = \\prod p_i^{\\min(e_i, f_i)}  # 最大公约数, p_i为质数因子, e_i和f_i为a和b的质因数指数",
                "\\text{lcm}(a,b) = \\prod p_i^{\\max(e_i, f_i)}  # 最小公倍数, p_i为质数因子, e_i和f_i为a和b的质因数指数"
            ], # 质因数分解
            "mode": [
                "在一组数据中，出现次数最多的数值，叫做这组数据的众数。"
            ], # 众数
            "median": [
                "把一组数据按从小到大排好，处在中间位置的那个数，叫做中位数。",
                "如果共有奇数个数据，中位数就是正中间的那个数。如果共有偶数个数据，中位数是中间两个数的平均数。"
            ], # 中位数
        }

    def _extract_knowledge_points(self, problem_text: str, llm: LLMClient, solution: str = None) -> List[str]:
        """提取题目的主要知识点"""
        prompt =textwrap.dedent(f"""
            你是一个数学教育专家。请分析下面的数学题目，提取主要涉及的知识点。
            题目：
            {problem_text}
            解答：
            {solution}
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
        formulas = set()
        for kp in knowledge_points:
            kp_lower = kp.lower()
            for key, value_list in self.formula_library.items():
                if key in kp_lower:
                    print(f"匹配到key：{key}")
                    formulas.update(value_list)
        return "\n".join(formulas) if formulas else "No specific formulas found."

    def _extract_numeric_inputs(self, problem_text: str, llm: LLMClient) -> Dict[str, Any]:
        """从题目文本中提取一个随机数字变量，并标注位置信息"""
        prompt = textwrap.dedent(f"""
            请从下面的数学题目中选择一个数字变量，这个变量将被用来生成变体题目。
            题目：
            {problem_text}

            变量用途说明：
            这个变量将被用来生成新的变体题目。具体流程是：
            1. 将这个变量的值改为其他合理的数值
            2. 根据新的变量值重新计算题目的答案
            3. 生成一个新的题目文本，其中这个变量的值已被替换

            选择变量的标准（重要）：
            请选择一个"好变化"的变量，即改变这个变量的值后：
            1. 代码容易编写：变量在计算过程中容易处理，不会导致复杂的边界情况
            2. 代码能正常运行：改变变量值后不会出现除零、负数开方、对数定义域错误等运行时错误
            3. 答案仍然合理：改变变量值后，答案仍然是正整数，不会变成负数、零或非整数
            4. 题目有意义：变量值改变后，题目仍然有数学意义，不会导致无解或退化情况

            优先选择：
            - 题目中没有关联变量的数字变量，即改变其数字后，不需要改变其他变量的值，就能使得题目仍然有意义
            - 在计算过程中作为输入或主要变量的数字，而不是中间结果或约束条件
            - 改变后能产生合理的答案的数字

            要求：
            1. 选择一个数字作为变量
            2. 对于这个数字变量，标注它在题目中出现的位置（使用字符位置，从题目文本开头开始计数，从0开始）

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

            重要说明：
            1. "硬编码"是指代码直接返回一个固定的数值答案，而不依赖输入参数进行任何计算。
            2. 如果代码使用输入参数进行计算来得到答案，即使代码中包含问题给定的常量（或根据这些常量计算出的常量值），这也不应该被认为是硬编码。
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

    def _run_python_code(self, code: str, inputs: Dict[str, Any], primary_key: Optional[str] = None, verify: bool = False, model_name: Optional[str] = None) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """运行Python代码并返回输出、错误和文件名（支持将 inputs 或其中单个变量传入 solve）"""
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
            model_suffix = f"_{model_name}" if model_name else ""
            if verify == True:
                filename = f"q{self.current_question_id}_verify{model_suffix}_{timestamp}.py"
            else:
                filename = f"q{self.current_question_id}_generate{model_suffix}_{timestamp}.py"

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
                return result.stdout.strip(), None, code_file # 返回print的标准输出、错误和文件名
            else:
                if code_file:
                    print(f"【执行出错】 Python代码已保存到: {code_file} ")
                return None, result.stderr.strip(), code_file
        except subprocess.TimeoutExpired:
            if code_file:
                print(f"【执行超时】 Python代码已保存到: {code_file} ")
            return None, "Timeout", code_file
        except Exception as e:
            if code_file:
                print(f"【异常: {str(e)}】 Python代码已保存到: {code_file} ")
            return None, str(e), code_file

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
            print(f"第【 {iter_num+1} 】次使用{llm_codegen.model_name}生成代码")
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
                2. 实现通用的计算过程，对变量 {primary_key} 的取值没有限制，不要硬编码答案
                3. 函数应该返回题目的答案
                4. 注意：题目中可能有多个相同的数字，但只有变量 {primary_key} 对应的位置需要作为参数传入
                5. 只输出函数定义和函数调用，不要输出 if __name__ == "__main__": 这样的测试代码块
                6. 不要添加任何print语句
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
                
                current_model = llm_codegen.model_name  # 跟踪当前代码的模型
                for refine_step in range(max_refine):
                    output, error, code_file = self._run_python_code(code, input_variables, primary_key, verify=True, model_name=current_model)
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
                            输入变量：
                            {primary_key} = {primary_value}，{position_str}{context_str}
                            求解代码：
                            ```python
                            {code}
                            ```                                
                            
                            请分析题目和代码逻辑，为变量 {primary_key} 确定合理的取值范围, 找出尽量多的取值。
                            要求如下：
                            1. 变量取值能保证代码能正常运行（不会出现除零、负数开方等错误）
                            2. 变量取值能保证答案在合理范围内
                            3. 变量取值不能超过1000或太小, 保证题目有意义
                            4. 保证代码适用于这个变量取值
                            5. 保证根据这个取值计算得到的答案小于100000
                            
                            说明：
                            不用考虑变量 {primary_key} 变化后，题目中其他与它关联的变量没有变化会导致题目有误。
                            因为在生成新题目时，系统会自动根据 {primary_key} 的新值相应地修改所有关联变量的值，
                            确保新题目在数学上仍然正确和有意义。你只需要专注于找出 {primary_key} 本身的合理取值范围即可。
                            
                            如果变量可以取连续范围内的任意值，请使用格式：
                            取值范围：[min, max]
                            例如：取值范围：[10, 100]
                            
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
                    print(f"【答案错误】 开始改进代码🤔")
                    refine_prompt = textwrap.dedent(f"""
                        之前的代码有错误。请修正它。
                        题目：{problem_text}
                        正确答案：{answer_gold}
                        之前的代码：
                        ```python
                        {code}
                        ```
                        solve 的输入变量：{primary_key}（其值：{primary_value}）
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

    def _build_recomposed_solver(
        self,
        original_problem: str,
        original_answer: str,
        recomposed_problem: str,
        recomposed_answer: str,
        solution_sketches: str,
        retrieved_formulas: str,
        knowledge_points: List[str],
        variable_name: str,
        variable_value: Any,
        variable_position: Dict,
        llm_codegen: LLMClient,
        llm_check: LLMClient,
        llm_refine: Optional[LLMClient] = None,
        llm_range: Optional[LLMClient] = None,
        max_iter: int = 5,
        max_refine: int = 5,
        item: Optional[ProblemItem] = None,
        generate_variant: bool = True,
    ) -> Optional[Tuple[str, Dict, str, Dict[str, Any], Dict]]:
        """构建条件重组求解器，专门用于 analogical-3
        
        返回 (code, value_ranges, primary_key, numeric_inputs, primary_position)
        """
        history = []
        
        print("------------构建条件重组求解器------------")
        print(f"原题：{original_problem}")
        print(f"原答案：{original_answer}")
        print(f"重组题：{recomposed_problem}")
        print(f"重组答案：{recomposed_answer}")
        print(f"变量：{variable_name} = {variable_value}")
        
        # 构建 numeric_inputs 格式
        numeric_inputs = {
            variable_name: {
                "value": variable_value,
                "position": variable_position
            }
        }
        
        print("----------生成重组题目求解代码----------")
        for iter_num in range(max_iter):
            print(f"第【 {iter_num+1} 】次使用{llm_codegen.model_name}生成代码")
            
            prompt = textwrap.dedent(f"""
                你是一个数学编程专家。请分析下面的重组后数学题目，编写一个Python求解程序。
                原题：
                {original_problem}
                原题的答案：
                {original_answer}
                重组后的题目（当前题目）：
                {recomposed_problem}
                重组后题目的答案：
                {recomposed_answer}
                
                重要说明：
                重组后题目是通过交换原题的"条件"和"目标"得到的。
                - 下面提供的"解法思路"是针对原题的解题方案，仅供参考，你可以根据这个思路，推导出重组后的题目的求解方案，并编写求解代码。
                - 下面提供的"变量"是重组后题目中的变量, 标注了其在重组后题目中的位置

                相关公式：
                {retrieved_formulas}
                知识点：
                {", ".join(knowledge_points)}
                解法思路：
                {solution_sketches}

                变量信息：
                变量：{variable_name} = {variable_value}（位置：{variable_position}）

                要求：
                1. 编写一个Python函数 solve({variable_name}), 仅接受变量 {variable_name} 的值作为参数
                2. 实现通用的计算过程，对变量 {variable_name} 的取值没有限制，不要硬编码答案
                3. 函数应该返回题目的答案
                4. 注意：题目中可能有多个相同的数字，但只有变量 {variable_name} 对应的位置需要作为参数传入
                5. 只输出函数定义和函数调用，不要输出 if __name__ == "__main__": 这样的测试代码块
                6. 不要添加任何print语句
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
                input_variables = {variable_name: variable_value}
                current_model = llm_codegen.model_name
                for refine_step in range(max_refine):
                    output, error, code_file = self._run_python_code(code, input_variables, variable_name, verify=True, model_name=current_model)
                    history.append((code, (output, error)))
                    
                    if error is None and str(output) == str(recomposed_answer):
                        print("【答案正确】 准备返回代码🥳")
                        
                        # 如果不需要生成变体，直接修改 item 并返回
                        if not generate_variant and item is not None:
                            print("【跳过变体生成】直接使用重组题目")
                            item.augmented_question = recomposed_problem
                            item.augmented_true_answer = recomposed_answer
                            return None  # 返回 None 表示已完成，不需要后续处理

                        print("----------确定变量取值范围----------")
                        value_ranges = {}
                        position_str = f"位置：字符 {variable_position.get('char_start', '?')}-{variable_position.get('char_end', '?')}" if variable_position else "位置：未标注"
                        context_str = f"，上下文：{variable_position.get('context', '')}" if variable_position.get('context') else ""
                        
                        range_prompt = textwrap.dedent(f"""
                            你是一个数学问题分析专家。请分析下面的题目和对应的解题代码，确定输入变量的合理取值范围。
                            题目：
                            {recomposed_problem}                                
                            输入变量：
                            {variable_name} = {variable_value}，{position_str}{context_str}
                            求解代码：
                            ```python
                            {code}
                            ```                                
                            
                            请分析题目和代码逻辑，为变量 {variable_name} 确定合理的取值范围, 找出尽量多的取值。
                            要求如下：
                            1. 变量取值能保证代码能正常运行（不会出现除零、负数开方等错误）
                            2. 变量取值能保证答案在合理范围内
                            3. 变量取值不能超过1000或太小, 保证题目有意义
                            4. 保证代码适用于这个变量取值
                            5. 保证根据这个取值计算得到的答案小于100000
                            
                            说明：
                            不用考虑变量 {variable_name} 变化后，题目中其他与它关联的变量没有变化会导致题目有误。
                            因为在生成新题目时，系统会自动根据 {variable_name} 的新值相应地修改所有关联变量的值，
                            确保新题目在数学上仍然正确和有意义。你只需要专注于找出 {variable_name} 本身的合理取值范围即可。
                            
                            如果变量可以取连续范围内的任意值，请使用格式：
                            取值范围：[min, max]
                            例如：取值范围：[10, 100]
                            
                            如果变量只能取特定的离散值，请使用格式：
                            取值列表：[value1, value2, value3, ...]
                            例如：取值列表：[1, 15, 301]
                            
                            请根据题目和代码的特点，选择合适的格式输出。
                            重要：只输出取值范围或取值列表，不要输出任何其他解释或内容。
                            """)
                        try:
                            range_resp = llm_range.chat(range_prompt) if llm_range else llm_codegen.chat(range_prompt)
                            # 尝试解析连续范围格式：取值范围：[min, max]
                            range_match = re.search(r'取值范围[：:]\s*\[(\d+),\s*(\d+)\]', range_resp)
                            if range_match:
                                min_val = int(range_match.group(1))
                                max_val = int(range_match.group(2))
                                value_ranges[variable_name] = (min_val, max_val)
                                print(f"确定取值范围（连续）：{variable_name} = [{min_val}, {max_val}]")
                            else:
                                # 尝试解析离散值列表格式：取值列表：[value1, value2, ...]
                                list_match = re.search(r'取值列表[：:]\s*\[([\d,\s]+)\]', range_resp)
                                if list_match:
                                    values_str = list_match.group(1)
                                    values = [int(v.strip()) for v in values_str.split(',') if v.strip().isdigit()]
                                    if values:
                                        value_ranges[variable_name] = values
                                        print(f"确定取值列表（离散）：{variable_name} = {values}")
                                    else:
                                        print(f"无法解析取值列表，使用默认范围")
                                        value_ranges[variable_name] = (1, 100)
                                else:
                                    print(f"无法解析取值范围，使用默认范围")
                                    value_ranges[variable_name] = (1, 100)
                        except Exception as e:
                            print(f"确定取值范围时出错: {e}，使用默认范围")
                            value_ranges[variable_name] = (1, 100)

                        return code, value_ranges, variable_name, numeric_inputs, variable_position
                    
                    if refine_step == max_refine - 1:
                        break
                    
                    # 精炼代码
                    print(f"【答案错误】 开始改进代码🤔，正确答案是{recomposed_answer}，当前答案是{output}")
                    refine_prompt = textwrap.dedent(f"""
                        之前的代码有错误。请修正它。
                        重要说明：
                        当前题目是通过"条件"和"目标"交换得到的重组题目。
                        - 原题：{original_problem}
                        - 重组后的题目（当前题目）：{recomposed_problem}
                        - 解法思路是针对原题的，你需要为重组后的题目编写求解代码。
                        
                        题目：{recomposed_problem}
                        正确答案：{recomposed_answer}
                        之前的代码：
                        ```python
                        {code}
                        ```
                        solve 的输入变量：{variable_name}（其值：{variable_value}）
                        错误信息：{error}
                        输出：{output}
                        历史记录：
                        {json.dumps(history, indent=2, ensure_ascii=False)}
                        请修正代码，只输出Python代码（保持 solve({variable_name}) 接口）。
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

    def _get_random_value_from_range(self, value_range: Any, exclude_value: Any = None) -> int:
        """从取值范围中随机选择一个值，支持连续范围 (min, max) 或离散值列表 [v1, v2, ...]
        
        Args:
            value_range: 取值范围，可以是 (min, max) 元组或 [v1, v2, ...] 列表
            exclude_value: 要排除的值，如果指定则不会选择该值
        """
        if isinstance(value_range, tuple) and len(value_range) == 2:
            # 连续范围
            min_val, max_val = value_range
            if exclude_value is not None:
                # 如果排除值在范围内，需要重新选择
                while True:
                    value = random.randint(min_val, max_val)
                    if value != exclude_value:
                        return value
            return random.randint(min_val, max_val)
        elif isinstance(value_range, list):
            # 离散值列表
            if exclude_value is not None:
                # 过滤掉排除值
                available_values = [v for v in value_range if v != exclude_value]
                if not available_values:
                    # 如果所有值都被排除，返回原值（这种情况不应该发生，但作为fallback）
                    return random.choice(value_range)
                return random.choice(available_values)
            return random.choice(value_range)
        else:
            # 默认范围
            if exclude_value is not None:
                while True:
                    value = random.randint(1, 100)
                    if value != exclude_value:
                        return value
            return random.randint(1, 100)

    def _is_positive_integer(self, value: Any) -> bool:
        """检查值是否为正整数"""
        if value is None:
            return False
        try:
            # 尝试转换为字符串，然后解析为整数
            if isinstance(value, str):
                value = value.strip()
                # 尝试解析为浮点数，然后检查是否为整数
                float_value = float(value)
                int_value = int(float_value)
                # 确保是整数且为正，且没有小数部分
                return int_value > 0 and int_value == float_value
            elif isinstance(value, (int, float)):
                int_value = int(value)
                # 确保是整数且为正，且没有小数部分
                return int_value > 0 and int_value == value
            else:
                return False
        except (ValueError, TypeError):
            return False

    def _get_all_possible_values(self, value_range: Any, exclude_values: set) -> list:
        """获取所有可能的值（排除已尝试的值）"""
        if isinstance(value_range, tuple) and len(value_range) == 2:
            # 连续范围
            min_val, max_val = value_range
            return [v for v in range(min_val, max_val + 1) if v not in exclude_values]
        elif isinstance(value_range, list):
            # 离散值列表
            return [v for v in value_range if v not in exclude_values]
        else:
            # 默认范围
            return [v for v in range(1, 101) if v not in exclude_values]

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
            
            # 记录已尝试的值
            tried_values = set()
            if original_value is not None:
                tried_values.add(original_value)
            
            max_attempts = 100  # 最大尝试次数，避免无限循环
            attempt = 0
            
            while attempt < max_attempts:
                attempt += 1
                
                # 检查是否还有可选的值
                available_values = self._get_all_possible_values(value_range, tried_values)
                if not available_values:
                    print(f"没有可选的值了（已尝试 {len(tried_values)} 个值）")
                    return "", ""
                
                # 从可用值中随机选择一个值
                new_value = random.choice(available_values)
                tried_values.add(new_value)
                print(f"尝试第 {attempt} 次，随机选择的变量值：{new_value}（原值：{original_value}）")
                
                print("----------生成新答案----------")
                new_inputs = {primary_key: new_value}
                output, error, code_file = self._run_python_code(code, new_inputs, primary_key, verify=False, model_name=llm.model_name)
                print(f"变量的新值：{new_value}，运行代码得到答案：{output}")
                # 检查是否有错误
                if error is not None:
                    print(f"运行代码时出错: {error}")
                    # 删除生成的Python文件
                    os.remove(code_file)
                    continue  # 重试
                
                # 检查输出是否为None
                if output is None:
                    print(f"函数返回None")
                    # 删除生成的Python文件
                    os.remove(code_file)
                    continue  # 重试
                
                # 检查答案是否为正整数
                if not self._is_positive_integer(output):
                    print(f"答案不是正整数: {output}")
                    # 删除生成的Python文件
                    os.remove(code_file)
                    continue  # 重试
                
                new_answer = output
                print(f"新答案：{new_answer}（正整数，验证通过）")
                
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
                    3. 如果原题中某变量的值和 {primary_key} 的值相关, 则相应地修改该变量的值
                    4. 保持题目其他部分完全不变
                    
                    请只输出新题目的文本，不要有其他解释。
                    """)
                # print("prompt:  "+prompt)
                resp = llm.chat(prompt)
                print(f"新题目：{resp.strip()}")
                return resp.strip(), new_answer
            
            # 如果达到最大尝试次数仍未成功
            print(f"达到最大尝试次数（{max_attempts}），未能生成有效的变体")
            return "", ""
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
        knowledge_points = self._extract_knowledge_points(item.original_question, llm_extract, item.solution)
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
            正确答案：
            {answer_gold}
            解法思路：
            {solution_sketches}
            相关公式：
            {retrieved_formulas}
            
            条件和目标互换的示例：
            原题1：There exist real numbers $x$ and $y$, both greater than 1, such that $\\log_x\\left(y^x\\right)=\\log_y\\left(x^{{4y}}\\right)=10$. Find $xy$.
            输出JSON格式：
            {{
                "invertible": true,
                "original_condition": "$\\\\log_x\\\\left(y^x\\\\right)=\\\\log_y\\\\left(x^{{4y}}\\\\right)=N$, N=10",
                "original_target": "$xy$ = ?",
                "new_condition": "$xy=N$, N=25",
                "new_target": "$\\\\log_x\\\\left(y^x\\\\right)=\\\\log_y\\\\left(x^{{4y}}\\\\right)=N$, N=?",
                "recomposed_problem_text": "There exist real numbers $x$ and $y$, both greater than 1, such that $xy=25$ and $\\\\log_x\\\\left(y^x\\\\right)=\\\\log_y\\\\left(x^{{4y}}\\\\right)=N$. Find $N$.",
                "new_answer": 10,
                "new_condition_name": "xy",
                "new_condition_value": 25,
                "new_condition_position": {{
                    "char_start": 71,
                    "char_end": 73,
                    "context": "such that $xy=25$"
                }}
            }}
            
            原题2：Let $x,y$ and $z$ be positive real numbers that satisfy the following system of equations: 
            \\[\\log_2\\left({{x \\over yz}}\\right) = {{1 \\over 2}}\\]
            \\[\\log_2\\left({{y \\over xz}}\\right) = {{1 \\over 3}}\\]
            \\[\\log_2\\left({{z \\over xy}}\\right) = {{1 \\over 4}}\\]
            Then the value of $-\\log_2(x^4y^3z^2)$ is $\\tfrac{{m}}{{n}}$ where $m$ and $n$ are relatively prime positive integers. Find $m+n$.
            输出JSON格式：
            {{
                "invertible": true,
                "original_condition": "\\[\\\\log_2\\left({{x \\\\over yz}}\\right) = {{1 \\\\over N}}\\], N=2",
                "original_target": "$-\\\\log_2(x^4y^3z^2)$ = ?",
                "new_condition": "$-\\\\log_2(x^4y^3z^2) = 25 \\\\over N$, N=8",
                "new_target": "\\[\\\\log_2\\left({{x \\\\over yz}}\\right) = {{1 \\\\over N}}\\], N=?",
                "recomposed_problem_text": "Let $x,y$ and $z$ be positive real numbers that satisfy the following system of equations: 
                    \\\\[\\\\log_2\\\\left({{y \\\\over xz}}\\\\right) = {{1 \\\\over 3}}\\\\]
                    \\\\[\\\\log_2\\\\left({{z \\\\over xy}}\\\\right) = {{1 \\\\over 4}}\\\\]
                    \\\\[-\\\\log_2(x^4y^3z^2) = {{25 \\\\over 8}}\\\\]
                    Then the value of $\\\\log_2\\\\left({{x \\\\over yz}}\\\\right)$ can be expressed as $\\\\tfrac{{1}}{{N}}$. Find $N$.",
                "new_answer": 2,
                "new_condition_name": "log_x4y3z2_denominator",
                "new_condition_value": 8,
                "new_condition_position": {{
                    "char_start": 345,
                    "char_end": 346,
                    "context": "\\\\[-\\\\log_2(x^4y^3z^2) = \\\\tfrac{{25}}{{8}}\\\\]"
                }}
            }}
            要求：
            1. 找到一个条件，这个条件必须能与目标互换
            2. 找到的条件必须是充要条件：即能够由目标（原答案）唯一推导出这个条件，同时这个条件也能唯一推导出目标
            3. 如果无法找到这样的充要条件，请设置 "invertible": false，并在 "reason" 中说明原因
            4. 提取的条件变量值和目标值必须是整数：例如，如果题目中有 ${{1 \over 3}}$（三分之一），应该选择整数 $3$ 而不是分数 ${{1 \over 3}}$
            5. 关于"m+n"类型题目的处理规则：
               当原题要求"Find m+n"（或 "Find m+n+p"），但题目的实际目的是求分数 m/n（或无理数 (m√n)/p）时，是为了答案判断方便才改为求 m+n（或 m+n+p）。
               在进行条件和目标转换时，必须遵循以下规则：
               - 应该将 m/n 的值（或 (m√n)/p 的值）作为新条件，而不是将 m+n 的值（或 m+n+p 的值）作为条件
               - 具体示例：如果原题是"|log₂(x⁴y³z²)| = m/n，求 m+n"，答案是 33（对应 m/n = 25/8），
                 转换时应将"|log₂(x⁴y³z²)| = 25/8"作为条件，求其他变量（如 log₂(z/xy)）
               - 禁止将 m+n 的值作为条件，同时将 m/n 作为目标，因为：
                 * m+n 完全依赖于 m/n 的值，没有独立的数学意义
                 * 这样的转换无法考察模型的数学推理能力
                 * 例如：不能将题目改为"已知 m+n = 28，求 m/n"，因为从 m+n 无法唯一确定 m/n
               - 核心原则：m/n 是独立的数学量，而 m+n 只是 m/n 的派生值，不能作为条件
            6. 位置标注要求：
               在重组后的题目文本中，需要标注新条件（即原答案）的位置信息：
               - char_start: 新条件在重组后题目文本中的起始字符位置（从0开始计数）
               - char_end: 新条件在重组后题目文本中的结束字符位置
               - context: 新条件的上下文描述，帮助后续准确识别和替换
            
            请以JSON格式输出：
            {{
                "invertible": true/false,
                "original_condition": "找到的那个能与目标互换的条件（如果invertible为true）",
                "original_target": "原目标（即要求求解什么）",
                "new_condition": "新条件（即原答案，如果invertible为true）",
                "new_target": "新目标（原条件的一部分，如果invertible为true）",
                "recomposed_problem_text": "重组后的题目文本（如果invertible为true）",
                "new_answer": "新答案的数值",
                "new_condition_name": "new_condition的变量名",
                "new_condition_value": "new_condition的数值",
                "new_condition_position": {{
                    "char_start": 起始位置,
                    "char_end": 结束位置,
                    "context": "上下文描述"
                }},
                "reason": "如果invertible为false，说明无法找到充要条件的原因；如果invertible为true，可以省略此字段"
            }}
            
            注意：
            - 如果 invertible 为 false，可以只输出 "invertible": false 和 "reason" 字段
            - 如果 invertible 为 true，必须输出所有字段，包括位置信息
            - 只输出JSON，不要有其他文字
            - 重要：JSON 中的字符串值如果包含反斜杠（如 LaTeX 公式），必须正确转义（使用双反斜杠 \\\\）
            - 例如：如果字符串包含 $\\log_x$，在 JSON 中应该写为 "$\\\\log_x$"
            """)
        try:
            resp = llm.chat(prompt)
            print(f"resp: {resp}")
            json_match = re.search(r'\{.*\}', resp, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                try:
                    data = json.loads(json_str)
                except json.JSONDecodeError as json_err:
                    # 如果解析失败，尝试修复常见的转义问题
                    print(f"JSON 解析失败，尝试修复: {json_err}")
                    try:
                        # 尝试修复：在字符串值中，将未转义的反斜杠转义
                        # 但要注意不要破坏已经正确转义的内容
                        # 使用正则表达式找到字符串值并修复其中的反斜杠
                        # 这是一个简化的修复：将 \" 之间的内容中的单个反斜杠转义
                        # 但这种方法可能不够精确，更好的方法是让 LLM 重新生成
                        
                        # 尝试使用更宽松的方式：先找到 JSON 的主要部分
                        # 如果错误信息包含位置信息，可以尝试在该位置附近修复
                        error_msg = str(json_err)
                        if "Invalid \\escape" in error_msg:
                            # 提取错误位置
                            pos_match = re.search(r'\(char (\d+)\)', error_msg)
                            if pos_match:
                                error_pos = int(pos_match.group(1))
                                print(f"错误位置: {error_pos}")
                                # 在错误位置附近，尝试修复反斜杠转义
                                # 但这种方法风险较大，可能破坏正确的内容
                                # 更安全的方法是返回 None，让调用者处理
                                print("无法自动修复 JSON 转义错误，返回 None")
                                return None
                        return None
                    except Exception as fix_err:
                        print(f"修复 JSON 失败: {fix_err}")
                        return None
                
                if data.get("invertible", False):
                    return data
            return None
        except Exception as e:
            print(f"分析可逆条件时出错: {e}")
            import traceback
            traceback.print_exc()
            return None

    def transform_analogical3(
        self,
        item: ProblemItem,
        llm_extract: Optional[LLMClient] = None,
        llm_analysis: Optional[LLMClient] = None,
        llm_codegen: Optional[LLMClient] = None,
        llm_check: Optional[LLMClient] = None,
        llm_refine: Optional[LLMClient] = None,
        llm_variant: Optional[LLMClient] = None,
        llm_range: Optional[LLMClient] = None,
        generate_variant: bool = True
    ) -> ProblemItem:
        """
        analogical-3：条件重组（conditional recomposition via invertible-condition analysis）
        """
        llm_extract = llm_extract or self.llm
        llm_analysis = llm_analysis or self.llm
        llm_codegen = llm_codegen or self.llm
        llm_check = llm_check or self.llm
        llm_refine = llm_refine or llm_codegen
        llm_variant = llm_variant or self.llm
        llm_range = llm_range or self.llm
        
        print("--------------------------------提取知识点--------------------------------")
        knowledge_points = self._extract_knowledge_points(item.original_question, llm_extract, item.solution)
        print("提取的知识点：\n", knowledge_points)
        
        print("--------------------------------查询公式库--------------------------------")
        retrieved_formulas = self._retrieve_formulas(knowledge_points)
        print("检索到的公式：\n", retrieved_formulas)
        
        print("--------------------------------分析可逆条件--------------------------------")
        invertible_analysis = self._analyze_invertible_conditions(
            item.original_question,
            item.true_answer,
            item.solution,
            retrieved_formulas,
            llm_analysis
        )
        
        if invertible_analysis is not None:
            # 获取重组后的题目和新答案
            new_problem = invertible_analysis.get("recomposed_problem_text", "")
            new_answer = invertible_analysis.get("new_answer", "")
            variable_name = invertible_analysis.get("new_condition_name", "")
            variable_value = invertible_analysis.get("new_condition_value", "")
            variable_position = invertible_analysis.get("new_condition_position", {})
            
            if not new_problem or not new_answer:
                print("警告：重组题目或新答案为空，无法继续")
                item.augmented_question = "x"
                item.augmented_true_answer = "x"
            else:
                numeric_inputs = {}
                if variable_name and variable_value is not None:
                    numeric_inputs[variable_name] = {
                        "value": variable_value,
                        "position": variable_position
                    }
                
                print("--------------------------------构建求解器--------------------------------")
                solver_result = self._build_recomposed_solver(
                    original_problem=item.original_question,
                    original_answer=item.true_answer,
                    recomposed_problem=new_problem,
                    recomposed_answer=new_answer,
                    solution_sketches=item.solution,
                    retrieved_formulas=retrieved_formulas,
                    knowledge_points=knowledge_points,
                    variable_name=variable_name,
                    variable_value=variable_value,
                    variable_position=variable_position,
                    llm_codegen=llm_codegen,
                    llm_check=llm_check,
                    llm_refine=llm_refine,
                    llm_range=llm_range,
                    item=item,
                    generate_variant=generate_variant
                )
                
                # 如果 generate_variant=False 且 solver_result 为 None，说明已经在函数内修改了 item，直接返回
                if not generate_variant and solver_result is None:
                    item.method_used = "analogical-3"
                    return item
                
                if solver_result:
                    code, value_ranges, primary_key, extracted_numeric_inputs, primary_position = solver_result  
                    # 将 numeric_inputs 转换为简单格式 {变量名: 值} 用于生成变体
                    input_variables = {}
                    for key, info in extracted_numeric_inputs.items():
                        value = info.get("value", info) if isinstance(info, dict) else info
                        input_variables[key] = value
                    
                    print("--------------------------------生成数字变体--------------------------------")
                    variant, variant_answer = self._generate_numeric_variant(
                        new_problem,  # 使用重组后的题目
                        code,
                        primary_key,
                        primary_position,
                        input_variables,
                        value_ranges,
                        llm_variant
                    )
                    
                    if variant and variant_answer:
                        item.augmented_question = variant
                        item.augmented_true_answer = variant_answer
                    else:
                        # 如果生成变体失败，使用原始重组问题
                        print("警告：生成变体失败，使用原始重组问题")
                        item.augmented_question = new_problem
                        item.augmented_true_answer = new_answer
                else:
                    # 如果构建求解器失败，直接使用分析结果
                    print("警告：构建求解器失败，使用分析结果")
                    item.augmented_question = "x"
                    item.augmented_true_answer = "x"
        else:
            # 条件和目标无法交换的情况
            print("警告：题目条件和目标无法交换，无法生成变体")
            item.augmented_question = "x"
            item.augmented_true_answer = "x"
        
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
        analogical_transformer: Optional[AnalogicalTransformer],
        redundancy_injector: Optional[RedundancyInjector],
        novel_generator: Optional[NovelProblemGenerator],
        role_llms: Optional[Dict[str, LLMClient]] = None,
    ):
        self.analogical_transformer = analogical_transformer
        self.redundancy_injector = redundancy_injector
        self.novel_generator = novel_generator
        self.role_llms = role_llms or {}

    def process(self, item: ProblemItem, method: str, generate_variant: bool = True) -> ProblemItem:
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
                    llm_variant=llms.get("variant"),
                    llm_range=llms.get("range"),
                    generate_variant=generate_variant
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
    llm_redundancy = build_llm(DEFAULT_STAGE_MODEL["redundancy"])
    llm_novel = build_llm(DEFAULT_STAGE_MODEL["novel"])
    llm_analogical_fallback = build_llm(DEFAULT_STAGE_MODEL["analogical_fallback"])

    role_llms = {
        role: build_llm(model)
        for role, model in DEFAULT_ROLE_MODEL.items()
    }

    analogical_transformer = AnalogicalTransformer(llm_analogical_fallback)
    redundancy_injector = RedundancyInjector(llm_redundancy)
    novel_generator = NovelProblemGenerator(llm_novel)

    pipeline = AMESPipeline(
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
            if args.start and i < args.start:
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
                generate_variant = args.generate_variant
                processed = pipeline.process(item, method=args.method, generate_variant=generate_variant)
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
                    processed.true_answer,
                    processed.augmented_question,
                    processed.augmented_true_answer,
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
    parser.add_argument('--question_id', type=int, default=None, help="题目ID")
    parser.add_argument('--start', type=int, default=None, help="开始题目ID")
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
    parser.add_argument('--generate_variant', action='store_true', default=False, help="不生成数字变体（对 analogical-3 有效）。设置此选项时，验证代码正确后直接使用重组题目，不进行后续的数字变换")
    args = parser.parse_args()

    if args.method not in {"1", "2", "3", "4", "5", "6", "7"}:
        raise ValueError("method 必须是 1~7 之一")

    run_ames_on_csv(args)