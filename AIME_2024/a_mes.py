import os
import csv
import time
from tkinter import N
import openai
import textwrap
import argparse
import re
import subprocess
import tempfile
import json
import random
import datetime
import shutil
import asyncio
import requests
import base64
from datetime import datetime
from fractions import Fraction
from pathlib import Path
from openai import OpenAI
from mistralai import Mistral
from dataclasses import dataclass
from volcenginesdkarkruntime import Ark, AsyncArk
from typing import List, Dict, Optional, Literal, Tuple, Any, Union
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# 尝试导入PDF处理库
try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    try:
        from PyPDF2 import PdfFileReader as PdfReader, PdfFileWriter as PdfWriter
    except ImportError:
        PdfReader = None
        PdfWriter = None
        print("警告：未安装PDF处理库（pypdf或PyPDF2），无法切割大文件。请安装：pip install pypdf")


deepseek_client = OpenAI(api_key="sk-09da13b2c97948628523d042d6a02f06", base_url="https://api.deepseek.com")
qwen_client = OpenAI(api_key="sk-b1c771fc24dd4cb89653163a74bf9e43", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
doubao_client = Ark(api_key="196b33be-8abb-4af3-9fba-6e266b2dd942")
kimi_client = OpenAI(api_key="sk-ODuizMlUC22phanBhvYz6dBjx2yrz7vhKhcjKnoIrYssThQo", base_url="https://api.moonshot.cn/v1")
mistral_client = Mistral(api_key="Wc1s1rVoW5TzceucND85yQoF4urCvO5f")
claude_client = OpenAI(api_key="sk-qjspBDS9b0TvyUuV3hT8EzFFPegGgSA1htNN3MrCJV8iNJuY", base_url="https://yinli.one/v1")
ModelName = Literal["deepseek", "qwen", "doubao", "kimi", "mistral", "gpt"]

# 全局默认模型选择（优先级低于下方细粒度配置）
DEFAULT_STAGE_MODEL = {
    "analogical_fallback": "qwen_max",
    "redundancy": "gpt5",
    "novel": "kimi_k2",
    "textbook_knowledge_base_construction": "kimi_k2",
}

# AnalogicalTransformer 内部不同子步骤可各自指定模型

DEFAULT_ROLE_MODEL = {
    "extract": "doubao_1_5_pro_32k",     # 知识点提取
    "convert": "gpt5",    # 答案格式转换（analogical-3，把m+n变为m/n）
    "analysis": "gpt5",    # 分析题目的条件和结论是否可逆（analogical-3）
    "codegen": "gpt5", # 代码生成
    "check": "gpt5",    # 硬编码检查
    "refine": "gpt5",  # 根据错误历史修正代码
    "range": "gpt5",  # 变量取值范围确定
    "variant": "gpt5",     # 数字变体生成（analogical-2）
    "retrieve": "gpt5",  # 题目检索（novel-1）
    "paraphrase": "doubao_1_5_pro_32k",  # 题目改写（novel-1）
    "generate": "gpt5",  # 概念题生成（novel-2）
    "final_check": "gpt5",  # 最终题目正确性检查
}

METHOD_DESCRIPTION = {
    "1": "analogical-1 / disturb1（无关冗余）",
    "2": "analogical-1 / disturb2（相关概念冗余）",
    "3": "analogical-1 / disturb3（诱导错误冗余）",
    "4": "analogical-2（数字变换类比）",
    "5": "analogical-3（条件重组类比）",
    "6": "novel-1（同知识点新题改编）",
    "7": "novel-2（同知识点概念题）",
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
        print(f"prompt: {prompt}\nmodel: {self.llm.model_name}")
        response = self.llm.chat(prompt)
        item.augmented_question = response.strip()
        item.augmented_true_answer = item.true_answer
        item.method_used = tag
        return item

class AnalogicalTransformer:
    """类比变换模块：基于代码生成和验证的 analogical-2 和 analogical-3"""

    def __init__(self, llm: LLMClient):
        self.llm = llm
        self.code_dir = "./code"
        self.current_question_id = None  # 当前处理的题目ID
        self.knowledge_base_path = Path("knowledge_base/formula_library.json")
        
        if self.code_dir:
            os.makedirs(self.code_dir, exist_ok=True)
        # 公式库——按知识点索引
        with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
            self.formula_library = json.load(f)

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

    def _extract_numeric_inputs(self, problem_text: str, solution_sketches: str, llm: LLMClient) -> Dict[str, Any]:
        """从题目文本中提取一个随机数字变量，并标注位置信息"""
        prompt = textwrap.dedent(f"""
            请从下面的数学题目中选择一个数字变量，这个变量将被用来生成变体题目，题目和题目的正确解法如下。
            题目：
            {problem_text}
            题目正确解法：
            {solution_sketches}

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

    def _check_hard_coded(self, problem_text: str, code: str, llm: LLMClient) -> bool:
        """检查代码是否包含硬编码答案"""

        print("-------------硬编码检查------------")
        prompt = textwrap.dedent(f"""
            请检查下面的Python代码是否包含硬编码的答案或实例特定的输出，而不是通用的计算过程。

            重要说明：
            1. "硬编码"是指代码直接返回一个固定的数值答案，而不依赖题目中的变量值进行计算。
            2. 如果代码使用输入参数进行计算来得到答案，即使代码中包含问题给定的常量（或根据这些常量计算出的常量值），也不应该被认为是硬编码。
            3. 如果代码使用了的常量并非来自题目且无法由题目所给的常量计算得出，则应该被认为是硬编码。
            
            题目：
            {problem_text}
            代码：
            {code}

            请以JSON格式输出：{{"is_hard_coded": true/false, "reason": "原因说明"}}
            只输出JSON，不要有其他文字。
            """)
        try:
            print(f"使用{llm.model_name}检查硬编码")
            resp = llm.chat(prompt)
            print(f"检查硬编码结果：{resp}")
            json_match = re.search(r'\{[^}]+\}', resp, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return data.get("is_hard_coded", False)
            return False
        except Exception as e:
            print(f"检查硬编码时出错: {e}")
            return False
    
    def _is_fraction_string(self, value: Any) -> bool:
        """检测值是否是分数字符串格式（如 "25/8"）"""
        if isinstance(value, str):
            fraction_match = re.match(r'^(\d+)/(\d+)$', value.strip())
            return fraction_match is not None
        return False

    def _run_python_code(self, code: str, inputs: Dict[str, Any], primary_key: Optional[str] = None, verify: bool = False, model_name: Optional[str] = None) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """运行Python代码并返回输出、错误和文件名（支持将 inputs 或其中单个变量传入 solve）"""
        code_file = None
        print(code)
        print(inputs)
        try:
            # 处理分数字符串：将分数字符串转换为 Fraction 对象以便代码执行
            processed_inputs = {}
            has_fraction = False
            for key, value in inputs.items():
                if self._is_fraction_string(value):
                    # 将分数字符串转换为 Fraction 对象
                    parts = value.strip().split('/')
                    if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                        processed_inputs[key] = Fraction(int(parts[0]), int(parts[1]))
                        has_fraction = True
                    else:
                        processed_inputs[key] = value
                elif isinstance(value, Fraction):
                    processed_inputs[key] = value
                    has_fraction = True
                else:
                    processed_inputs[key] = value
            
            # 如果包含 Fraction 对象，添加导入
            import_line = "from fractions import Fraction\n" if has_fraction else ""
            
            # 准备代码内容
            input_code = f"inputs = {repr(processed_inputs)}"
            if primary_key and primary_key in inputs:
                call_code = f"result = solve(inputs[{repr(primary_key)}])"
            else:
                call_code = "result = solve(inputs)"
            full_code = f"{import_line}{input_code}\n\n{code}\n\n# 调用 solve\n{call_code}\nprint(result)"

            # 使用指定的目录，生成有意义的文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # 年月日_时分秒，如：20251211_151438

            model_suffix = f"_{model_name}" if model_name else ""
            if verify == True:
                filename = f"q{self.current_question_id}_verify{model_suffix}_{timestamp}.py"
            else:
                filename = f"q{self.current_question_id}_generate{model_suffix}_{timestamp}.py"
            print(f"文件名: {filename}")
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
                    print(f"【运行成功】 Python代码已保存到: {code_file} 🤩")
                return result.stdout.strip(), None, code_file # 返回print的标准输出、错误和文件名
            else:
                if code_file:
                    print(f"【运行出错】 Python代码已保存到: {code_file} ")
                return None, result.stderr.strip(), code_file
        except subprocess.TimeoutExpired:
            if code_file:
                print(f"【运行超时】 Python代码已保存到: {code_file} ")
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
        print(f"使用{llm_codegen.model_name}提取数字变量")
        numeric_inputs = self._extract_numeric_inputs(problem_text, solution_sketches, llm_codegen)
        
        # numeric_inputs 的结构是 {变量名: {value: 值, position: {...}}}
        # primary_key 是提取的变量
        primary_key = list(numeric_inputs.keys())[0] if numeric_inputs else None
        print("提取的数字变量：")
        for key, info in numeric_inputs.items():
            value = info.get("value", info) if isinstance(info, dict) else info
            position = info.get("position", {}) if isinstance(info, dict) else {}
            print(f"  {key} = {value} 位置: {position}")
        
        # 准备变量信息字符串
        primary_info = numeric_inputs.get(primary_key, {}) if primary_key else {}
        primary_value = primary_info.get("value", primary_info) if isinstance(primary_info, dict) else primary_info
        primary_position = primary_info.get("position", {}) if isinstance(primary_info, dict) else {}
        
        print("----------生成通用求解代码----------")
        for iter_num in range(max_iter):
            print(f"第【 {iter_num+1} 】次使用{llm_codegen.model_name}生成代码")
            # 生成代码
            prompt = textwrap.dedent(f"""
                你是一个数学编程专家。请分析下面的数学题目，编写一个Python求解程序。
                题目：
                {problem_text}
                正确答案：
                {answer_gold}
                解法思路：
                {solution_sketches}
                相关公式：
                {retrieved_formulas}
                知识点：
                {", ".join(knowledge_points)}

                变量信息：
                变量：{primary_key} = {primary_value}（位置：{primary_position}）

                要求：
                1. 编写一个Python函数 solve({primary_key}), 仅接受变量 {primary_key} 的值作为参数
                2. 实现通用的计算过程，对变量 {primary_key} 的取值没有限制，不要硬编码答案
                3. 函数应该返回题目的答案
                4. 注意：题目中可能有多个相同的数字，但只有变量 {primary_key} 对应的位置需要作为参数传入
                5. 只输出函数定义，不要输出 if __name__ == "__main__": 这样的测试代码块，不要输出solve(23)这样的函数调用
                6. 不要输出任何print语句
                7. 只输出Python代码，不要有其他解释。
                """)
            history.append((prompt, None))
         
            try:
                print(f"使用{llm_codegen.model_name}生成代码")
                code_resp = llm_codegen.chat(prompt)
                # 提取代码块
                code_match = re.search(r'```python\n(.*?)\n```', code_resp, re.DOTALL)
                if code_match:
                    code = code_match.group(1)
                else:
                    code_match = re.search(r'```\n(.*?)\n```', code_resp, re.DOTALL)
                    code = code_match.group(1) if code_match else code_resp
                
                # 检查硬编码
                if self._check_hard_coded(problem_text, code, llm_check):
                    print("【硬编码检测未通过】 检测到硬编码，跳过🥶")
                    print(f"包含硬编码的代码：\n{code}")
                    continue
                else:
                    print("【硬编码检测通过】 成功生成通用解题逻辑，准备运行代码🫡")

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
                            
                            请分析题目和代码逻辑，为变量 {primary_key} 确定合理的取值范围，最好找到至少10个取值。
                            要求如下：
                            1. 变量取值能让代码正常运行（不会出现除零、负数开方等错误）
                            2. 变量取值能保证答案在合理范围内
                            3. 变量{primary_key}的新取值在其原值{primary_value}附近, 不能太大或太小, 保证新题目有意义
                            4. 保证我给的求解代码适用于你确定的变量取值
                            5. 保证根据你确定的取值计算得到的答案小于100000
                            6. 保证题目仍然合理，例如：如果变量为三角形的某边，则应满足“三角形两边之和大于第三边”等条件
                            
                            说明：
                            不用考虑变量 {primary_key} 变化后，题目中其他与之关联的变量没有变化会导致题目有误，因为在生成新题目时，我将根据你确定的 {primary_key} 的新值相应地修改所有关联变量的值，确保新题目在数学上仍然正确和有意义。
                            你只需要专注于找出 {primary_key} 本身的合理取值范围。
                            
                            如果变量可以取连续范围内的任意值，请使用格式：
                            取值范围：[min, max]
                            例如：取值范围：[10, 100]
                            min和max必须为正整数
                            
                            如果变量只能取特定的离散值，请使用格式：
                            取值列表：[value1, value2, value3, ...]
                            例如：取值列表：[1, 15, 301]
                            value1, value2, value3...必须为正整数
                            
                            根据题目和代码的特点，选择合适的格式输出。
                            重要：只输出取值范围或取值列表，不要输出任何其他解释或内容。
                            """)
                        
                        # 重试最多 5 次来确定取值范围
                        max_range_retries = 5
                        range_determined = False
                        
                        for range_retry in range(max_range_retries):
                            try:
                                print(f"第 {range_retry + 1} 次尝试使用{llm_range.model_name}确定取值范围...")
                                range_resp = llm_range.chat(range_prompt)
                                print(f"确定取值范围的响应：{range_resp}")
                                # 尝试解析连续范围格式：取值范围：[min, max]
                                range_match = re.search(r'取值范围[：:]\s*\[(\d+),\s*(\d+)\]', range_resp)
                                if range_match:
                                    min_val = int(range_match.group(1))
                                    max_val = int(range_match.group(2))
                                    value_ranges[primary_key] = (min_val, max_val)
                                    print(f"确定取值范围（连续）：{primary_key} = [{min_val}, {max_val}]")
                                    range_determined = True
                                    break
                                else:
                                    # 尝试解析离散值列表格式：取值列表：[value1, value2, ...]
                                    list_match = re.search(r'取值列表[：:]\s*\[([\d,\s]+)\]', range_resp)
                                    if list_match:
                                        values_str = list_match.group(1)
                                        values = [int(v.strip()) for v in values_str.split(',') if v.strip().isdigit()]
                                        if values:
                                            value_ranges[primary_key] = values
                                            print(f"确定取值列表（离散）：{primary_key} = {values}")
                                            range_determined = True
                                            break
                                        else:
                                            print(f"第 {range_retry + 1} 次尝试：无法解析取值列表，继续重试...")
                                    else:
                                        print(f"第 {range_retry + 1} 次尝试：无法解析取值范围，继续重试...")
                            except Exception as e:
                                print(f"第 {range_retry + 1} 次尝试确定取值范围时出错: {e}，继续重试...")
                        
                        # 如果5次重试后仍无法确定取值范围，返回 None 元组表示转换失败
                        if not range_determined:
                            print(f"经过 {max_range_retries} 次尝试，仍无法确定取值范围，转换失败")
                            return None, None, None, None, None

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
        
        return None, None, None, None, None

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
                return None, None, None
            
            # 从可用值中随机选择一个值
            new_value = random.choice(available_values)
            tried_values.add(new_value)
            print(f"尝试第 {attempt} 次，原值：{original_value} → 随机新值：{new_value}")
            
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
                    例如：
                    - 针对这个题目“Consider the paths of length $14$ that follow the lines from the lower left corner to the upper right corner on an $7\times 7$ grid. ”，这里路径长度为14是因为grid边长是7，所以如果修改了grid边长，例如改为5，则路径长度应该相应改为10。
                    - 针对这个题目"Tina enters a lottery by picking $5$ distinct numbers from $S=\\{{1,2,3,\\cdots,9,10\\}}.$ $5$ numbers are randomly chosen from $S.$ She wins a prize if at least two of her numbers were $2$ of the randomly chosen numbers, and wins the grand prize if all five of her numbers were the randomly chosen numbers. "，这里如果把S中的10改为100，则这个集合中其他的数字也要相应修改，改为$S=\\{{1,2,3,\\cdots,99,100\\}}.$，而不能只修改10为100，其他不变，得到$S=\\{{1,2,3,\\cdots,9,100\\}}.$是不合理的
                4. 保持题目其他部分完全不变
                
                请只输出新题目的文本，不要有其他解释。
                """)
            print(f"使用{llm.model_name}生成新答案")
            resp = llm.chat(prompt)
            print(f"新题目：{resp.strip()}")
            return resp.strip(), new_answer, new_value
        
        # 如果达到最大尝试次数仍未成功
        print(f"达到最大尝试次数（{max_attempts}），未能生成有效的变体")
        return None, None, None

    def _check_final_correctness(self, origin_promlem: str, origin_answer: str, solution_sketches: str, new_problem: str, new_answer: str, code: str, primary_key: str, primary_value: str, new_value: str, primary_position: Dict[str, Any], llm: LLMClient) -> bool:
        """检查最终题目正确性"""
        char_start = primary_position.get('char_start', '?')
        char_end = primary_position.get('char_end', '?')
        context = primary_position.get('context', '')
        position_info = f"第 {char_start}-{char_end}个字符，上下文：{context}"
        prompt = textwrap.dedent(f"""
        我在使用大模型对题目数字进行改编，需要你帮我检查改编是否正确。
        
        【原题信息】
        原题目：
        {origin_promlem}
        正确答案：
        {origin_answer}
        解法思路：
        {solution_sketches}
        
        【大模型改编流程】
        1. 首先我让大模型对这道题目设计求解代码，它给出的代码如下：
        {code}
        这段代码将原题中的变量{primary_key}（取值为{primary_value}，位置为{position_info}）作为输入参数
        
        2. 接着，我让大模型为变量{primary_key}选择一个合理的新取值，它选择了{new_value}，我运行代码，得到了新的答案：{new_answer}
        
        3. 最后，我让大模型把原题中的变量{primary_key}的取值{primary_value}改为{new_value}，并修改改变量的相关变量的取值，得到新题目的文本：
        {new_problem}
        
        【具体检查要求】
        1. 检查大模型给出的求解代码是否是“硬编码”，“硬编码”是指直接返回一个固定的数值答案，或不依赖题目中的变量值（或由题目中变量值推导出的值）进行计算。
        2. 检查大模型给出的新值是否让题目保持合理，例如新题目是否满足“三角形两边之和大于第三边”等条件
        3. 检查大模型给出的新题目是否正确改变了变量{primary_key}的关联变量（注意关联变量不一定是用数字表示的，也可能是文字描述的）
           例如：
           - 如果改变了题目中几何图形某一边的长度或者半径等，则几何图形的周长、面积等相关的变量是否改变？
           - 如果已知三角形为直角三角形，改变了某一直角边长度，则斜边长度是否改变？
           - 如果改变了题目中的格点边长，则格点总数、格点路径长度是否改变？
        4. 检查大模型给出的代码和新题目是否适配
           例如：
           如果原题是：设 p 为满足存在正整数 n 使 n⁴ + 1 能被 p² 整除的最小素数。求最小的正整数 m，使得 m⁴ + 1 能被 p² 整除。
           代码是针对两个 p² 的指数同时被修改设计的，即针对“设 p 为满足存在正整数 n 使 n⁴ + 1 能被 pᵉ 整除的最小素数。求最小的正整数 m，使得 m⁴ + 1 能被 pᵉ 整除”设计的，而不是针对“设 p 为满足存在正整数 n 使 n⁴ + 1 能被 pᵉ 整除的最小素数。求最小的正整数 m，使得 m⁴ + 1 能被 p² 整除”设计的。
           但是最后大模型把新题目改成了“设 p 为满足存在正整数 n 使 n⁴ + 1 能被 pᵉ 整除的最小素数。求最小的正整数 m，使得 m⁴ + 1 能被 p² 整除”
           即新题目无法用代码求解，则认为大模型给出的代码和新题目不适配

        【输出要求】
        根据上述具体检查要求，逐点检查这个新题目是否正确，只有所有检查都通过才可以判定为正确，只要有一个检查没有通过，就判定为错误
        请以JSON格式输出：{{"is_correct": true/false, "reason": "原因说明"}}
        只输出JSON，不要输出任何其他解释和信息。
        """)
        try:
            print(f"使用{llm.model_name}检查新题目正确性")
            resp = llm.chat(prompt)
            print(f"检查新题目正确性结果：{resp}")
            # 尝试提取JSON，使用更健壮的方法匹配嵌套的大括号
            json_match = re.search(r'\{.*\}', resp, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                try:
                    data = json.loads(json_str)
                    return data.get("is_correct", False)
                except json.JSONDecodeError as json_err:
                    print(f"JSON 解析失败，尝试修复: {json_err}")
                    # 尝试更精确的JSON提取：匹配嵌套的大括号
                    try:
                        # 从第一个{开始，逐字符匹配，找到匹配的}
                        start_pos = resp.find('{')
                        if start_pos != -1:
                            brace_count = 0
                            for i in range(start_pos, len(resp)):
                                if resp[i] == '{':
                                    brace_count += 1
                                elif resp[i] == '}':
                                    brace_count -= 1
                                    if brace_count == 0:
                                        json_str = resp[start_pos:i+1]
                                        data = json.loads(json_str)
                                        return data.get("is_correct", False)
                        print("无法找到有效的JSON对象")
                    except (json.JSONDecodeError, ValueError) as e2:
                        print(f"修复JSON失败: {e2}")
            return False
        except Exception as e:
            print(f"检查新题目正确性时出错: {e}")
            return False

    def generate_analogical2(
        self,
        item: ProblemItem,
        llm_extract: Optional[LLMClient] = None,
        llm_codegen: Optional[LLMClient] = None,
        llm_check: Optional[LLMClient] = None,
        llm_refine: Optional[LLMClient] = None,
        llm_range: Optional[LLMClient] = None,
        llm_variant: Optional[LLMClient] = None,
        llm_final_check: Optional[LLMClient] = None,
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
        llm_final_check = llm_final_check or self.llm
        
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
        
        # 如果无法确定取值范围，转换失败，返回 None
        if solver_result[0] is None:
            print("无法确定变量取值范围，转换失败")
            item.augmented_question = "x"
            item.augmented_true_answer = "x"
            item.method_used = "analogical-2"
            return item
        
        code, value_ranges, primary_key, numeric_inputs, primary_position = solver_result
        # 将 numeric_inputs 转换为简单格式 {变量名: 值} 用于生成变体
        input_variables = {}
        for key, info in numeric_inputs.items():
            value = info.get("value", info) if isinstance(info, dict) else info
            input_variables[key] = value
        
        print("--------------------------------生成数字变体--------------------------------")
        variant, new_answer, new_value = self._generate_numeric_variant(
            item.original_question, 
            code, 
            primary_key,
            primary_position,
            input_variables,
            value_ranges,
            llm_variant
        )
        
        if variant is None:
            print("生成数字变体题目失败")
            item.augmented_question = "x"
            item.augmented_true_answer = "x"
            item.method_used = "analogical-2"
            return item
        
        print("--------------------------------最终题目正确性检查--------------------------------")
       
        if not self._check_final_correctness(item.original_question, item.true_answer, item.solution, variant, new_answer, code, primary_key, numeric_inputs[primary_key]['value'], new_value, primary_position, llm_final_check):
            print("题目正确性检查结果：错误")
            item.augmented_question = "x"
            item.augmented_true_answer = "x"
        else:
            print("题目正确性检查结果：正确")
            item.augmented_question = variant
            item.augmented_true_answer = new_answer

        item.method_used = "analogical-2"
        return item

    def _convert_answer_format(
        self,
        problem_text: str,
        answer_gold: str,
        solution_sketches: str,
        llm: Optional[LLMClient] = None,
    ) -> Optional[Dict]:
        """转换答案格式：将"Find m+n"类型的题目转换为"Find m/n"，并提取正确的分数答案"""
        llm = llm or self.llm
        prompt = textwrap.dedent(f"""
            你是一个数学问题分析专家。请分析下面的题目，转换题目和答案格式。
            
            题目：
            {problem_text}
            正确答案（原格式）：
            {answer_gold}
            解法思路：
            {solution_sketches}
            
            任务说明：
            如果题目的实际目的是求分数 m/n（或无理数 (m√n)/p)，但为了答案为整数，最后要求"Find m+n"（或"Find m+n+p"等），则：
               - 去掉题目中的"Find m+n"，改为"Find m/n, where m and n are coprime positive integers"（或"Find (m√n)/p,  where m, n, and p are positive integers, m and p are relatively prime, and n is not divisible by the square of any prime."）
            如果不是这种情况，则无需对题目和答案进行任何转化。
            
            示例：
            原题：
            Let $x,y$ and $z$ be positive real numbers that satisfy the following system of equations: 
            \\[\\log_2\\left({{x \\over yz}}\\right) = {{1 \\over 2}}\\]
            \\[\\log_2\\left({{y \\over xz}}\\right) = {{1 \\over 3}}\\]
            \\[\\log_2\\left({{z \\over xy}}\\right) = {{1 \\over 4}}\\]
            Then the value of $\\left|\\log_2(x^4y^3z^2)\\right|$ is $\\tfrac{{m}}{{n}}$ where $m$ and $n$ are relatively prime positive integers. Find $m+n$.
            解法中提到：After absolute value, it is just $\\frac{{25}}{{8}}$. Summing $m$ and $n$, we obtain $\\boxed{{33}}$.
            转换后题目：
            Let $x,y$ and $z$ be positive real numbers that satisfy the following system of equations: 
            \\[\\log_2\\left({{x \\over yz}}\\right) = {{1 \\over 2}}\\]
            \\[\\log_2\\left({{y \\over xz}}\\right) = {{1 \\over 3}}\\]
            \\[\\log_2\\left({{z \\over xy}}\\right) = {{1 \\over 4}}\\]
            Then the value of $\\left|\\log_2(x^4y^3z^2)\\right|$ is $\\tfrac{{m}}{{n}}$ where $m$ and $n$ are relatively prime positive integers. Find $m/n$.
            转换后答案：
            25/8
            
            请以JSON格式输出：
            {{
                "needs_conversion": true/false,  // 是否需要转换（如果题目不是"Find m+n"类型，设为false）
                "converted_problem": "转换后的题目文本（如果needs_conversion为true）",
                "converted_answer": "转换后的答案，使用plain text格式，如 25/2 或 25√7/3",
                "m": m的数值（如果是分数）,
                "n": n的数值（如果是分数）,
                "p": p的数值（如果是无理数，否则省略此字段）
            }}
            
            注意：
            - 只输出JSON，不要有其他文字
            - 如果题目不需要转换（不是"Find m+n"类型），设置 "needs_conversion": false
            """)
        try:
            resp = llm.chat(prompt)
            print(f"答案格式转换响应: {resp}")
            # 提取JSON
            json_match = re.search(r'\{.*\}', resp, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group(0))
                return result
            else:
                print("无法从响应中提取JSON")
                return None
        except Exception as e:
            print(f"答案格式转换出错: {e}")
            return None

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
            Then the value of $-\\log_2(x^4y^3z^2)$ is $\\tfrac{{m}}{{n}}$ where $m$ and $n$ are relatively prime positive integers. Find $m/n$.
            输出JSON格式：
            {{
                "invertible": true,
                "original_condition": "\\[\\\\log_2\\left({{x \\\\over yz}}\\right) = {{1 \\\\over N}}\\], N=2",
                "original_target": "$-\\\\log_2(x^4y^3z^2)$ = ?",
                "new_condition": "$-\\\\log_2(x^4y^3z^2) = N$, N=25/8",
                "new_target": "\\[\\\\log_2\\left({{x \\\\over yz}}\\right) = {{1 \\\\over N}}\\], N=?",
                "recomposed_problem_text": "Let $x,y$ and $z$ be positive real numbers that satisfy the following system of equations: 
                    \\\\[\\\\log_2\\\\left({{y \\\\over xz}}\\\\right) = {{1 \\\\over 3}}\\\\]
                    \\\\[\\\\log_2\\\\left({{z \\\\over xy}}\\\\right) = {{1 \\\\over 4}}\\\\]
                    \\\\[-\\\\log_2(x^4y^3z^2) = {{25 \\\\over 8}}\\\\]
                    Then the value of $\\\\log_2\\\\left({{x \\\\over yz}}\\\\right)$ can be expressed as $\\\\tfrac{{1}}{{N}}$. Find $N$.",
                "new_answer": 2,
                "new_condition_name": "log_x4y3z2r",
                "new_condition_value": 25/8,
                "new_condition_position": {{
                    "char_start": 332,
                    "char_end": 346,
                    "context": "\\\\[-\\\\log_2(x^4y^3z^2) = \\\\tfrac{{25}}{{8}}\\\\]"
                }}
            }}
            要求：
            1. 找到一个条件，这个条件必须能与目标互换
            2. 找到的条件必须是充要条件：即能够由目标（原答案）唯一推导出这个条件，同时这个条件也能唯一推导出目标
            3. 如果无法找到这样的充要条件，请设置 "invertible": false，并在 "reason" 中说明原因
            4. 提取的条件变量值必须是题目中显式出现的数字：变量值必须是题目文本中直接写出的具体数字，不能是题目中隐含的、推导出的、或单位中的变量。
            5. 提取的条件变量值必须是整数：例如，如果题目中有 ${{1 \over 3}}$（三分之一），应该选择整数 $3$ 而不是分数 ${{1 \over 3}}$
            6. 新题目中禁止出现提示新答案的内容，即知道该信息后不需要计算和推理就可以直接得到新答案。
            7. 位置标注要求：
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
            print(f"条件-目标可逆性分析结果: {resp}")
            json_match = re.search(r'\{.*\}', resp, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                try:
                    data = json.loads(json_str)
                except json.JSONDecodeError as json_err:
                    # 如果解析失败，尝试修复常见的转义问题
                    print(f"JSON 解析失败，尝试修复: {json_err}")
                    try:
                        error_msg = str(json_err)
                        if "Invalid \\escape" in error_msg:
                            # 提取错误位置
                            pos_match = re.search(r'\(char (\d+)\)', error_msg)
                            if pos_match:
                                error_pos = int(pos_match.group(1))
                                print(f"错误位置: {error_pos}")
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
            
            # 构建分数处理提示（如果需要）
            fraction_note = ""
            if self._is_fraction_string(variable_value):
                num, den = variable_value.split('/')
                fraction_note = f"""
                重要提示(分数处理)：
                变量 {variable_name} 的值是分数形式({variable_value})。请务必注意以下几点：
                1. 请在代码中使用 fractions.Fraction 来处理分数运算，避免使用浮点数(小数)计算，以保持精确性
                2. 输入参数可能是 Fraction 对象，代码应该直接使用 Fraction 进行运算
                3. 在代码开头必须添加：from fractions import Fraction
                4. 必须使用 Fraction 进行所有分数运算，不要转换为浮点数
                5. 示例：可以使用 Fraction({num}, {den}) 或 Fraction("{variable_value}") 来创建分数对象
                """
            
            fraction_requirement = "7. 必须使用 Fraction 进行分数运算，不要转换为浮点数\n                " if self._is_fraction_string(variable_value) else ""
            
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
                
                {fraction_note}
                
                要求：
                1. 编写一个Python函数 solve({variable_name}), 仅接受变量 {variable_name} 的值作为参数
                2. 实现通用的计算过程，对变量 {variable_name} 的取值没有限制，不要硬编码答案
                3. 函数应该返回题目的答案
                4. 注意：题目中可能有多个相同的数字，但只有变量 {variable_name} 对应的位置需要作为参数传入
                5. 只输出函数定义和函数调用，不要输出 if __name__ == "__main__": 这样的测试代码块
                6. 不要添加任何print语句
                {fraction_requirement}请只输出Python代码，不要有其他解释。
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
                if self._check_hard_coded(recomposed_problem, code, llm_check):
                    print("【硬编码检测未通过】 检测到硬编码，跳过🥶")
                    print(f"包含硬编码的代码：\n{code}")
                    continue
                else:
                    print("【硬编码检测通过】 成功生成通用解题逻辑，准备运行代码🫡")

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
                            print(f"使用{llm_range.model_name}确定取值范围结果：{range_resp}")
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
                    fraction_note = ""
                    if self._is_fraction_string(variable_value):
                        fraction_note = f"""
                        重要提示：变量 {variable_name} 的值是分数形式（{variable_value}）。
                        - 请使用 fractions.Fraction 来处理分数运算，避免使用浮点数（小数）计算
                        - 如果输入参数是字符串形式的分数，请先将其转换为 Fraction 对象
                        - 在代码开头添加：from fractions import Fraction
                        - 必须使用 Fraction 进行分数运算，不要转换为浮点数
                        """
                    refine_prompt = textwrap.dedent(f"""
                        之前的代码有错误。请修正它。
                        重要说明：
                        当前题目是通过"条件"和"目标"交换得到的重组题目。
                        - 原题：{original_problem}
                        - 重组后的题目（当前题目）：{recomposed_problem}
                        - 解法思路是针对原题的，你需要为重组后的题目编写求解代码。
                        {fraction_note}
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
    
    def generate_analogical3(
        self,
        item: ProblemItem,
        llm_extract: Optional[LLMClient] = None,
        llm_convert: Optional[LLMClient] = None,
        llm_analysis: Optional[LLMClient] = None,
        llm_codegen: Optional[LLMClient] = None,
        llm_check: Optional[LLMClient] = None,
        llm_refine: Optional[LLMClient] = None,
        llm_range: Optional[LLMClient] = None,
        llm_variant: Optional[LLMClient] = None,
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
        
        print("--------------------------------答案格式转换--------------------------------")
        answer_format_conversion = self._convert_answer_format(
            item.original_question,
            item.true_answer,
            item.solution,
            llm_convert
        )
        
        # 确定用于分析可逆条件的题目和答案
        if answer_format_conversion and answer_format_conversion.get("needs_conversion", False):
            problem_for_analysis = answer_format_conversion.get("converted_problem", item.original_question)
            answer_for_analysis = answer_format_conversion.get("converted_answer", item.true_answer)
            print(f"使用转换后的题目和答案进行分析")
            print(f"转换后题目: {problem_for_analysis}")
            print(f"转换后答案: {answer_for_analysis}")
        else:
            problem_for_analysis = item.original_question
            answer_for_analysis = item.true_answer
            print(f"使用原始题目和答案进行分析")
        
        print("--------------------------------分析可逆条件--------------------------------")
        invertible_analysis = self._analyze_invertible_conditions(
            problem_for_analysis,
            answer_for_analysis,
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
    - 6 -> novel-1：从网络搜寻的同知识点最新题目改编
    - 7 -> novel-2：从教材的知识点生成的概念题
    """

    def __init__(self, llm: LLMClient):
        self.llm = llm
       
        # novel-1 需要用到的配置
        self.question_bank_url = "https://zujuan.21cnjy.com/question?tree_type=knowledge&xd=3&chid=3"
        self.login_url = "https://passport.21cnjy.com/login?jump_url=https://zujuan.21cnjy.com/u/index"
        self.login_method = "mobile"  # 可选值: "password" 或 "mobile", 代表账号密码登录 or 手机号+验证码登录
        self.username = "18192300180"
        self.password = "xx100806"
        self.mobile = "13240974717"
        self.images_dir = "math_images"
        self.debug_pages_dir = "debug_pages"
        self.doubao_api_key = "196b33be-8abb-4af3-9fba-6e266b2dd942"
        self.driver = None  # Selenium driver，延迟初始化
        self.wait_time = 3

        # novel-2 需要用到的配置
        self.knowledge_base_path = Path("knowledge_base/knowledge_base_math_textbook.json")
        self.knowledge_base = None
        
        # 批量处理时使用的知识点列表
        self._all_knowledge_points = None
        
    def initialize_for_batch_processing(self):
        """
        在处理所有题目之前初始化driver、登录并提取知识点
        这个方法只需要在处理批量题目之前调用一次
        """
        print("-----------------------------初始化driver和登录-------------------------------")
        self._init_driver()
        self._login()
        print("--------------------------------提取题库知识点--------------------------------")
        self._all_knowledge_points = self._get_available_leaf_knowledge_points() # 提取叶子知识点
        # self._all_knowledge_points = self._get_available_level_knowledge_points(3) # 提取第三层知识点
        print(f"提取到 {len(self._all_knowledge_points)} 个知识点")
        
    def _extract_knowledge_points(
        self, 
        problem_text: str, 
        llm: LLMClient, 
        solution: str = None,
        available_knowledge_points: Optional[List[str]] = None
    ) -> List[str]:
        """提取题目的主要知识点"""
        if available_knowledge_points:
            # 如果提供了可用的知识点列表，让模型从中选择
            kb_points_str = "\n".join(available_knowledge_points)
            prompt = textwrap.dedent(f"""
                你是一个数学教育专家。请分析下面的数学题目，从知识库中识别主要涉及的知识点。
                题目：
                {problem_text}
                解答：
                {solution}
                
                知识库中可用的知识点列表：
                {kb_points_str}
                
                请从上述知识点列表中选择与题目最相关的知识点，以JSON格式输出，格式为：{{"knowledge_points": ["知识点1", "知识点2", ...]}}
                如果没有找到相关知识点，就输出一个知识库中和题目微有联系的知识点，不要输出知识库中不存在的知识点或空字符串，必须完全匹配知识库中的知识点名称。
                只输出知识点名称，不要有任何其他文字，禁止在输出中解释或说明你为什么选择这个知识点。
                """)

        try:
            resp = llm.chat(prompt)
            print("使用模型：", llm.model_name)
            # 尝试提取JSON
            json_match = re.search(r'\{[^}]+\}', resp, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return data.get("knowledge_points", [])
            return []
        except Exception as e:
            print(f"提取知识点时出错: {e}")
            return []
        
    def _init_driver(self):
        """ 初始化 Headless Chrome driver """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        # 自动寻找 Chromium 与 chromedriver
        CHROMEDRIVER_PATH = shutil.which("chromedriver") or "/usr/bin/chromedriver"
        service = Service(CHROMEDRIVER_PATH)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def _login(self):
        """ 登录函数 """
        print("🔐 正在打开登录页面...")
        self.driver.get(self.login_url)

        # 等待登录页加载完成
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".login-tabs"))
        )
        time.sleep(1)

        # 根据配置选择登录方式
        if self.login_method == "mobile":
            # ===== 方法1：手机号+验证码登录 =====
            print("📱 使用【手机号+验证码】登录方式...")
            
            # 切换到手机验证码登录选项卡
            try:
                print("🧭 切换到【手机验证码登录】模式...")
                mobile_tab = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-type='m14c']"))
                )
                self.driver.execute_script("arguments[0].click();", mobile_tab)
                time.sleep(1)  # 等待切换完成
            except Exception as e:
                print(f"⚠️ 无法切换至手机验证码登录模式：{e}")

            # 等待手机号输入框变为可见
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located((By.ID, "user-phone"))
            )
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located((By.ID, "resu-m14c"))
            )
            
            # 输入手机号
            print(f"➡️  输入手机号: {self.mobile}")
            mobile_input = self.driver.find_element(By.ID, "user-phone")
            mobile_input.clear()
            mobile_input.send_keys(self.mobile)
            time.sleep(0.5)

            # 点击"获取验证码"按钮
            print("📲 正在点击【获取验证码】按钮...")
            try:
                code_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.J_BtnMsgCode, .btn-code"))
                )
                self.driver.execute_script("arguments[0].click();", code_btn)
                print("🗳 验证码已发送，请查收短信...")
                time.sleep(0.5)  # 等待验证码发送
            except Exception as e:
                print(f"⚠️ 点击获取验证码按钮失败：{e}")

            # 输入验证码
            max_wait_time = 300  # 最大等待时间（秒）
            elapsed_time = 0
            
            code_input = self.driver.find_element(By.ID, "resu-m14c")
            input_code = ""
            
            while not input_code and elapsed_time < max_wait_time:
                try:
                    input_code = input("请输入验证码: ")    
                    code_input.send_keys(input_code)
                    break
                except Exception as e:
                    print(f"⚠️ 输入验证码失败: {e}")
                    time.sleep(1)
                
            if not input_code:
                print("⚠️ 验证码输入超时，请重新运行程序")
                return False

        else:
            # ===== 方法2：账号密码登录 =====
            print("🔑 使用【账号密码】登录方式...")
            
            # 切换到账号密码登录选项卡
            try:
                print("🧭 切换到【账号密码登录】模式...")
                pwd_tab = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-type='pwd']"))
                )
                self.driver.execute_script("arguments[0].click();", pwd_tab)
                time.sleep(1)  # 等待动画或 DOM 切换完成
            except Exception as e:
                print(f"⚠️ 无法切换至账号密码登录模式：{e}")

            # 等待账号输入框变为可见
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located((By.ID, "user-name"))
            )
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located((By.ID, "user-pwd"))
            )
            
            # 输入账号和密码
            print("➡️  输入账号和密码...")
            username_input = self.driver.find_element(By.ID, "user-name")
            password_input = self.driver.find_element(By.ID, "user-pwd")

            username_input.clear()
            username_input.send_keys(self.username)
            time.sleep(0.5)
            password_input.clear()
            password_input.send_keys(self.password)
            time.sleep(0.5)

        # 点击登录按钮（两种方式共用）
        print("🚪 正在点击登录按钮...")
        login_btn = self.driver.find_element(By.CSS_SELECTOR, "button.btn.btn-submit")
        self.driver.execute_script("arguments[0].click();", login_btn)
        
        # 验证是否成功
        try:
            # 等待URL跳转到 zujuan.21cnjy.com 域名（登录成功后会跳转）
            WebDriverWait(self.driver, 20).until(
                lambda d: "zujuan.21cnjy.com" in d.current_url
            )
            print("✅ 登录成功，正在跳转...")
            print(f"\n📥 保存完整页面用于调试...")
            self._save_page_for_debug(question_idx=None, stage="before_click")
        except Exception:
            print("⚠️ 登录失败，请检查账号/密码或验证码！")

        time.sleep(2)
        
    def _get_available_leaf_knowledge_points(self):
        """ 获取题库中的可用知识点 """
        
        # 访问知识点页面
        print("📚 正在访问知识点页面...")
        self.driver.get(self.question_bank_url)
        time.sleep(self.wait_time)
        
        # 等待知识点树加载完成
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".t-checkbox-node"))
            )
            print("✅ 知识点树加载完成")
        except Exception as e:
            print(f"⚠️ 等待知识点树加载失败: {e}")
            return []
        
        # 递归获取所有叶子知识点
        leaf_knowledge_points = []
        
        def _extract_leaf_knowledge_points(element):
            """ 递归提取叶子知识点 """
            try:
                # 查找当前节点的知识点名称（在 t-tit 下的 t-name 中，文本可能在 a 标签内）
                knowledge_point_name = ""
                name_element = element.find_element(By.CSS_SELECTOR, ".t-tit .t-name")
                
                # 尝试从 a 标签获取
                try:
                    a_element = name_element.find_element(By.TAG_NAME, "a")
                    knowledge_point_name = a_element.text.strip()
                    if not knowledge_point_name:
                        knowledge_point_name = a_element.get_attribute("textContent") or a_element.get_attribute("innerText") or ""
                        knowledge_point_name = knowledge_point_name.strip()
                except Exception:
                    pass

                # 检查是否有子知识点（查找并列的 t-bd 下的直接子节点 t-checkbox-node）
                child_container = None
                child_nodes = []
                try:
                    # 查找当前节点下的子节点容器 ul.t-bd
                    child_container = element.find_element(By.CSS_SELECTOR, ".t-bd")
                    # 使用 XPath 查找直接子元素 li.t-checkbox-node（CSS 的 > 在 WebElement.find_elements 中可能不被支持）
                    child_nodes = child_container.find_elements(By.XPATH, "./li[contains(@class, 't-checkbox-node')]")
                    
                    if child_nodes and len(child_nodes) > 0:
                        # 如果有子节点，递归处理每个子节点
                        # print(f"找到{len(child_nodes)}个子节点")
                        for child_node in child_nodes:
                            _extract_leaf_knowledge_points(child_node)
                except Exception as e:
                    # 如果没有找到 t-bd 或子节点，说明这是叶子节点
                    leaf_knowledge_points.append(knowledge_point_name)
                    # print(f"  ✓ 找到叶子知识点: {knowledge_point_name}")
                        
            except Exception as e:
                print(f"  ⚠️ 处理节点时出错: {e}")
        
        # 找到所有顶级知识点节点
        print("🔍 开始遍历知识点树...")

        try:
            treeview_div = self.driver.find_element(By.CSS_SELECTOR, "div.TreeView.t-tree-bd, div.TreeView")
            # 使用 XPath 查找直接子元素 ul.t-bd（CSS 选择器的 > 在 WebElement.find_element 中可能不被支持）
            tree_container = treeview_div.find_element(By.XPATH, "./ul[contains(@class, 't-bd')]")
        except Exception as e:
            print("使用XPath查找tree_container失败")
        
        top_level_nodes = []
        try:
            all_li = tree_container.find_elements(By.TAG_NAME, "li")
            for li in all_li:
                classes = li.get_attribute("class") or ""
                if "t-checkbox-node" in classes:
                    # 检查是否是直接子元素
                    parent = li.find_element(By.XPATH, "./..")
                    if parent == tree_container:
                        top_level_nodes.append(li)
        except Exception as e:
            print(f"没有找到顶级节点: {e}")

        print(f"📊 找到 {len(top_level_nodes)} 个顶级知识点节点")
    
        # 递归处理每个顶级节点
        for node in top_level_nodes:
            _extract_leaf_knowledge_points(node)
        
        print(f"✅ 找到 {len(leaf_knowledge_points)} 个叶子知识点:")
        print(leaf_knowledge_points)
        return leaf_knowledge_points
    
    def _get_available_level_knowledge_points(self, level):
        """ 获取指定层级的知识点 
            level: 层级数，1为顶级知识点，2为顶级知识点的子知识点，3为顶级知识点的孙子知识点，以此类推
        """
        
        if level < 1:
            print("⚠️ 层级必须大于等于1")
            return []
        
        # 访问知识点页面
        print(f"📚 正在访问知识点页面，获取第 {level} 层级的知识点...")
        self.driver.get(self.question_bank_url)
        time.sleep(self.wait_time)
        
        # 等待知识点树加载完成
        self._save_page_for_debug(question_idx=None, stage="知识点树访问")
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".t-checkbox-node"))
            )
            print("✅ 知识点树加载完成")
        except Exception as e:
            print(f"⚠️ 等待知识点树加载失败: {e}")
            return []
        
        # 存储指定层级的知识点
        level_knowledge_points = []
        
        def _extract_knowledge_point_name(element):
            """ 提取知识点的名称 """
            try:
                name_element = element.find_element(By.CSS_SELECTOR, ".t-tit .t-name")
                # 尝试从 a 标签获取
                try:
                    a_element = name_element.find_element(By.TAG_NAME, "a")
                    knowledge_point_name = a_element.text.strip()
                    if not knowledge_point_name:
                        knowledge_point_name = a_element.get_attribute("textContent") or a_element.get_attribute("innerText") or ""
                        knowledge_point_name = knowledge_point_name.strip()
                    return knowledge_point_name
                except Exception:
                    return name_element.text.strip()
            except Exception:
                return ""
        
        def _get_nodes_at_level(nodes, current_level, target_level):
            """ 递归获取指定层级的节点 
            
            Args:
                nodes: 当前层级的节点列表
                current_level: 当前层级（从1开始）
                target_level: 目标层级
            """
            if current_level == target_level:
                # 到达目标层级，收集所有节点的名称
                for node in nodes:
                    name = _extract_knowledge_point_name(node)
                    if name:
                        level_knowledge_points.append(name)
                return
            
            # 如果还没到达目标层级，继续向下遍历
            if current_level < target_level:
                for node in nodes:
                    try:
                        # 查找当前节点的子节点容器
                        child_container = node.find_element(By.CSS_SELECTOR, ".t-bd")
                        # 获取直接子节点
                        child_nodes = child_container.find_elements(By.XPATH, "./li[contains(@class, 't-checkbox-node')]")
                        
                        if child_nodes and len(child_nodes) > 0:
                            _get_nodes_at_level(child_nodes, current_level + 1, target_level)
                    except Exception:
                        # 如果没有子节点，说明已经到达叶子节点，但还没到目标层级
                        # 这种情况不需要处理，直接跳过
                        pass
        
        # 找到所有顶级知识点节点
        print("🔍 开始遍历知识点树...")
        
        try:
            treeview_div = self.driver.find_element(By.CSS_SELECTOR, "div.TreeView.t-tree-bd, div.TreeView")
            tree_container = treeview_div.find_element(By.XPATH, "./ul[contains(@class, 't-bd')]")
        except Exception as e:
            print(f"⚠️ 使用XPath查找tree_container失败: {e}")
            return []
        
        top_level_nodes = []
        try:
            all_li = tree_container.find_elements(By.TAG_NAME, "li")
            for li in all_li:
                classes = li.get_attribute("class") or ""
                if "t-checkbox-node" in classes:
                    # 检查是否是直接子元素
                    parent = li.find_element(By.XPATH, "./..")
                    if parent == tree_container:
                        top_level_nodes.append(li)
        except Exception as e:
            print(f"⚠️ 没有找到顶级节点: {e}")
            return []
        
        print(f"📊 找到 {len(top_level_nodes)} 个顶级知识点节点")
        
        # 从顶级节点开始，递归获取指定层级的节点
        _get_nodes_at_level(top_level_nodes, 1, level)
        
        print(f"✅ 找到 {len(level_knowledge_points)} 个第 {level} 层级的知识点:")
        print(level_knowledge_points)
        return level_knowledge_points
            
    async def _recognize_math_image_doubao(self, image_path):
        """
        使用豆包Vision API异步识别图片中的数学公式
        :param image_path: 图片路径（绝对路径）
        :return: 识别出的数学公式文本（LaTeX格式）
        """
        try:
            # 转换为绝对路径
            abs_image_path = os.path.abspath(image_path)
            
            # 创建异步客户端
            async_client = AsyncArk(
                base_url='https://ark.cn-beijing.volces.com/api/v3',
                api_key=self.doubao_api_key
            )
            
            # 调用豆包Vision API
            response = await async_client.responses.create(
                model="doubao-seed-1-6-251015",
                input=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_image",
                                "image_url": f"file://{abs_image_path}"
                            },
                            {
                                "type": "input_text",
                                "text": "请识别这张图片中的内容。如果是数学公式则使用LaTeX格式输出。如果识别到包含类似“【第1空】”的内容，则删除该内容，并输出剩余内容，例如解析到“【第1空】 -1”则输出“-1”。只输出图片所含内容，不要有任何其他输出。"
                            }
                        ]
                    }
                ]
            )
            
            # 提取识别结果（根据实际响应结构）
            try:
                formula = None
                
                # 尝试 responses.create 的响应结构：response.output 是一个列表
                if hasattr(response, 'output') and response.output:
                    # output 是一个列表，找到 ResponseOutputMessage 类型的项
                    for item in response.output:
                        # 检查是否是消息类型
                        if hasattr(item, 'type') and item.type == 'message':
                            if hasattr(item, 'content') and item.content:
                                # content 也是一个列表，找到 ResponseOutputText 类型的项
                                for content_item in item.content:
                                    if hasattr(content_item, 'type') and content_item.type == 'output_text':
                                        if hasattr(content_item, 'text'):
                                            formula = content_item.text
                                            break
                                if formula:
                                    break
                        # 如果找不到message类型，尝试直接访问text属性
                        if not formula and hasattr(item, 'text'):
                            formula = item.text
                            break
                
                if not formula:
                    formula = "[未能提取到文本内容]"
                else:
                    formula = formula.strip()
                    
            except (AttributeError, IndexError, TypeError) as e:
                print(f"⚠️ 解析响应结构失败: {e}")
                print(f"   响应类型: {type(response)}")
                if hasattr(response, 'output'):
                    print(f"   output类型: {type(response.output)}")
                formula = f"[响应解析失败]"
            
            # 清理可能的markdown代码块标记
            formula = formula.replace('```latex', '').replace('```', '').strip()
            return formula
        except Exception as e:
            print(f"⚠️ 识别图片失败 {image_path}: {e}")
            return f"[公式识别失败]"

    def _recognize_math_image_kimi(self, image_path):
        """
        使用Kimi Vision API同步识别图片中的数学公式
        :param image_path: 图片路径（绝对路径）
        :return: 识别出的数学公式文本（LaTeX格式）
        """
        try:
            # 转换为绝对路径
            abs_image_path = os.path.abspath(image_path)
            
            # 读取图片并转换为base64
            with open(abs_image_path, "rb") as f:
                image_data = f.read()
            
            # 获取图片扩展名（去掉点号）
            image_ext = os.path.splitext(abs_image_path)[1].lstrip('.')
            if not image_ext:
                image_ext = 'png'  # 默认使用png
            
            # 将图片编码成base64格式的image_url
            image_url = f"data:image/{image_ext};base64,{base64.b64encode(image_data).decode('utf-8')}"
            
            # 调用Kimi Vision API
            completion = kimi_client.chat.completions.create(
                model="moonshot-v1-8k-vision-preview",
                messages=[
                    {"role": "system", "content": "你是 Kimi。"},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_url,
                                },
                            },
                            {
                                "type": "text",
                                "text": "请识别这张图片中的内容。如果是数学公式则使用LaTeX格式输出。如果识别到包含类似“【第1空】”的内容，则删除该内容，并输出剩余内容，例如解析到“【第1空】 -1”则输出“-1”。删除冗余内容，例如识别到“D ___”则删除“___”并输出“D”。只输出图片所含内容，不要有任何其他输出。",
                            },
                        ],
                    },
                ],
            )
            
            # 提取识别结果
            try:
                formula = completion.choices[0].message.content
                if not formula:
                    formula = "[未能提取到文本内容]"
                else:
                    formula = formula.strip()
                    
            except (AttributeError, IndexError, TypeError) as e:
                print(f"⚠️ 解析响应结构失败: {e}")
                print(f"   响应类型: {type(completion)}")
                formula = f"[响应解析失败]"
            
            # 清理可能的markdown代码块标记
            formula = formula.replace('```latex', '').replace('```', '').strip()
            return formula
        except Exception as e:
            print(f"⚠️ 识别图片失败 {image_path}: {e}")
            return f"[公式识别失败]"
        
    def _recognize_math_image_simpletex(self, image_path):
        """
        使用SimpleTex API识别图片中的数学公式
        :param image_path: 图片路径（绝对路径）
        :return: 识别出的数学公式文本（LaTeX格式）
        """
        try:
            # 转换为绝对路径
            abs_image_path = os.path.abspath(image_path)
            print(f"🔍 开始识别图片: {abs_image_path}")
            
            # 从环境变量获取UAT token
            simpletex_uat = "Nqvrp8aLItuzjDgudXKItbHOML6dP8y7ogiy6PRpeiUvrn81Z0kPMxm3fPzMlj27"

            # API接口地址
            api_url = "https://server.simpletex.cn/api/latex_ocr"
            
            # 准备请求头
            headers = {"token": simpletex_uat}
            
            # 获取文件名
            filename = os.path.basename(abs_image_path)
            
            # 重复尝试最多5次
            formula = None

            with open(abs_image_path, 'rb') as file_handle:
                files = [("file", (filename, file_handle, "image/png"))]
                data = {}  # 非文件型参数，根据API文档可在此添加
                
                # 发送POST请求（requests会在请求过程中读取文件，文件会在with块结束时自动关闭）
                response = requests.post(api_url, files=files, data=data, headers=headers)
            
            # 检查HTTP状态码
            if response.status_code != 200:
                print(f"⚠️ SimpleTex API请求失败，状态码: {response.status_code}")
                print(f"   响应内容: {response.text[:200]}")
                # HTTP错误不重试，直接返回
                return f"[API请求失败: HTTP {response.status_code}]"
            
            # 解析JSON响应
            result = json.loads(response.text)
            
            # 根据SimpleTex API的响应结构提取LaTeX公式
            # {"res": {"latex": "公式内容"}} 
            formula = None
            if isinstance(result, dict):
                if "res" in result and isinstance(result["res"], dict):
                    if "latex" in result["res"]:
                        formula = result["res"]["latex"]
            
            if not formula:
                print(f"⚠️ 未能从响应中提取公式，res:latex为空")
                formula = "[未能提取到公式内容]"
            else:
                formula = str(formula).strip()
                    
            # 清理可能的markdown代码块标记
            formula = formula.replace('```latex', '').replace('```', '').strip()
            print(f"🔍 识别到的公式: {formula}")
            
            # 使用 doubao_1_5_pro_32k 过滤内容
            try:
                filter_prompt = textwrap.dedent(f"""请过滤以下文本内容：
                    1. 如果文本包含类似"【第1空】"、"【第2空】"等内容，则删除该内容，只输出剩余内容。例如："【第1空】 -1" 应输出 "-1"
                    2. 删除冗余内容，例如识别到"D ___"则删除"___"并输出"D"
                    3. 只输出过滤后的内容，不要有任何其他输出或解释

                    需要过滤的文本：
                    {formula}""")
                
                filter_response = doubao_client.chat.completions.create(
                    model="doubao-1.5-pro-32k-250115",
                    messages=[
                        {"role": "system", "content": "你是一个文本过滤器，只输出过滤后的内容，不要有任何其他输出。"},
                        {"role": "user", "content": filter_prompt},
                    ],
                    temperature=0.0,
                    stream=False
                )
                
                filtered_formula = filter_response.choices[0].message.content.strip()
                print(f"🔍 过滤后的公式: {filtered_formula}")
                return filtered_formula
            except Exception as e:
                print(f"⚠️ 调用 doubao API 过滤内容失败: {e}")
                # 如果过滤失败，返回原始公式
                return formula
            
        except FileNotFoundError:
            print(f"⚠️ 图片文件不存在: {image_path}")
            return f"[文件不存在]"
        except PermissionError:
            print(f"⚠️ 无权限读取文件: {image_path}")
            return f"[文件权限错误]"
        except Exception as e:
            print(f"⚠️ 识别图片失败 {image_path}: {e}")
            import traceback
            traceback.print_exc()
            return f"[公式识别失败: {str(e)}]"

    def _resize_image_if_needed(self, image_path, min_dimension=16, llm_image_recognition="doubao"):
        """
        检查图片尺寸，如果宽或高小于最小尺寸要求，则放大图片
        :param image_path: 图片路径
        :param min_dimension: 最小尺寸（像素），默认16（API要求14，留一些余量）
        :return: 实际使用的图片路径（如果生成了新图片则返回新路径，否则返回原路径）
        """
        import os
        if not PIL_AVAILABLE:
            print("⚠️ 无法调整图片尺寸: PIL/Pillow未安装")
            return image_path
        
        with Image.open(image_path) as img:
            width, height = img.size
            print(f"  📏 图片尺寸: {width}x{height}")
            print(f"  💾 原图路径: {image_path}")
            
            # 如果宽度大于300，裁剪为前150像素（针对simpletex无法识别太"长"的图片）
            if llm_image_recognition == "simpletex":
                if width > 300:
                    # 裁剪图片：保留左侧150像素. crop参数: (left, top, right, bottom)
                    cropped_img = img.crop((0, 0, 150, height))
                    width = 150  # 更新宽度值以便后续检查
                    img = cropped_img  # 更新img对象以便后续处理
                    print(f"  📏 图片裁剪: {width}x{height} -> 150x{height}")
            
                # 在右侧拼接10像素宽度的空白（针对simpletex识别优化）
                padding_width = 10
                target_width = width + padding_width
                # 创建新图片：原宽度+10像素，保持原高度，背景为白色
                new_img = Image.new('RGB', (target_width, height), color='white')
                
                # 粘贴原图到新图的左侧
                new_img.paste(img, (0, 0))
                
                # 保存新图片到不同路径（添加_processed后缀）
                base_path, ext = os.path.splitext(image_path)
                new_image_path = f"{base_path}_processed{ext}"
                new_img.save(new_image_path, 'PNG')
                print(f"  📏 图片右侧拼接空白: {width}x{height} -> {target_width}x{height} (右侧增加{padding_width}像素)")
                print(f"  💾 新图片已保存到: {new_image_path}")
                return new_image_path
            
            # 检查是否需要调整
            if (width <= min_dimension or height <= min_dimension) and llm_image_recognition == "doubao":            
                # 计算缩放比例，确保两个维度都至少达到最小尺寸
                scale_w = min_dimension / width if width < min_dimension else 1
                scale_h = min_dimension / height if height < min_dimension else 1
                scale = max(scale_w, scale_h)
                
                # 计算新尺寸（向上取整，确保至少达到最小尺寸）
                new_width = max(int(width * scale), min_dimension)
                new_height = max(int(height * scale), min_dimension)
                
                # 使用高质量重采样算法（兼容新旧版本Pillow）
                try:
                    # 新版本Pillow使用Image.Resampling.LANCZOS
                    resample = Image.Resampling.LANCZOS
                except AttributeError:
                    # 旧版本使用Image.LANCZOS
                    resample = Image.LANCZOS
                
                resized_img = img.resize((new_width, new_height), resample)
                
                # 保存调整后的图片到不同路径（添加_processed后缀）
                base_path, ext = os.path.splitext(image_path)
                new_image_path = f"{base_path}_processed{ext}"
                resized_img.save(new_image_path, 'PNG')
                print(f"  📏 图片尺寸调整: {width}x{height} -> {new_width}x{new_height}")
                print(f"  💾 新图片已保存到: {new_image_path}")
                return new_image_path
            
        return image_path

    def _download_image(self, img_url, img_path, session=None):
        """
        下载图片到本地，支持SVG格式并自动转换为PNG
        :param img_url: 图片URL（可能是相对路径或绝对路径）
        :param img_path: 保存路径（应该以.png结尾）
        :param session: requests session对象（用于保持cookies）
        :return: 是否下载成功
        """
        try:
            # 处理协议相对URL（以//开头）
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            # 如果是相对路径，转换为绝对路径
            elif not img_url.startswith('http'):
                img_url = urljoin(URL, img_url)
            
            # 确保目录存在
            img_dir = os.path.dirname(img_path)
            if img_dir:
                os.makedirs(img_dir, exist_ok=True)
            
            # 检查URL是否指向SVG（mml2svg表示SVG格式）
            is_svg_url = 'mml2svg' in img_url or 'svg' in img_url.lower()
            
            # 下载内容
            if session:
                response = session.get(img_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            else:
                response = requests.get(img_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            
            # 检查内容类型和内容，判断是否为SVG
            content_type = response.headers.get('Content-Type', '').lower()
            content_preview = response.content[:200] if len(response.content) > 0 else b''
            
            is_svg = is_svg_url or 'svg' in content_type
            if not is_svg:
                try:
                    content_str = content_preview.decode('utf-8', errors='ignore')
                    is_svg = content_str.strip().startswith('<?xml') or content_str.strip().startswith('<svg')
                except:
                    pass
            
            # 如果是SVG格式，使用selenium截图转换为PNG
            if is_svg and self.driver:
                try:
                    # 使用selenium访问SVG URL并截图
                    self.driver.get(img_url)
                    time.sleep(0.5)  # 等待SVG加载
                    svg_element = self.driver.find_element(By.TAG_NAME, 'svg')
                    svg_element.screenshot(img_path)
                    # print(f"  ✅ SVG已转换为PNG: {img_path}")
                    return True
                except Exception as e:
                    print(f"⚠️ SVG截图失败: {e}")
                    # 如果截图失败，尝试保存原始SVG内容
                    try:
                        svg_path = img_path.replace('.png', '.svg')
                        with open(svg_path, 'wb') as f:
                            f.write(response.content)
                        print(f"⚠️ 已保存为SVG文件: {svg_path}")
                    except:
                        pass
                    return False
            elif is_svg:
                print(f"⚠️ 检测到SVG格式，但driver未提供，无法转换")
                # 保存为SVG文件
                svg_path = img_path.replace('.png', '.svg')
                with open(svg_path, 'wb') as f:
                    f.write(response.content)
                # print(f"⚠️ 已保存为SVG文件: {svg_path}")
                return False
            else:
                # 非SVG格式，直接保存
                with open(img_path, 'wb') as f:
                    f.write(response.content)
                return True
                
        except Exception as e:
            print(f"⚠️ 下载图片失败 {img_url}: {e}")
            return False
    
    def _extract_option_content(self, op_item_element, session, question_idx, option_idx, llm_image_recognition):
        """
        提取选项内容（可能是文本或图片，或两者混合）
        :param op_item_element: 选项元素 (span.op-item)
        :param session: requests session
        :param question_idx: 题目索引
        :param option_idx: 选项索引 (0=A, 1=B, 2=C, 3=D)
        :return: 选项内容的文本表示
        """
        option_letter = ['A', 'B', 'C', 'D'][option_idx]
        
        # 查找选项内容部分 (span.op-item-meat)
        meat_span = op_item_element.find('span', class_='op-item-meat')
        if not meat_span:
            return ""
        
        # 创建元素的副本以避免修改原始元素
        element_copy = BeautifulSoup(str(meat_span), 'lxml').find()
        
        # 查找所有mathml图片
        img_tags = element_copy.find_all('img', class_='mathml')
        
        # 如果没有图片，直接返回文本
        if not img_tags:
            return element_copy.get_text(strip=True)
        
        # 创建文本替换映射
        replacements = []
        
        for img_idx, img in enumerate(img_tags):
            img_src = img.get('src', '')
            if not img_src:
                continue
            
            # 构建图片保存路径
            img_filename = f"q{question_idx}_opt{option_letter}_img{img_idx}.png"
            img_path = os.path.join(self.images_dir, img_filename)
            abs_img_path = os.path.abspath(img_path)
            
            # 下载图片
            if self._download_image(img_src, abs_img_path, session):
                # 预处理图片，获取实际使用的图片路径
                actual_img_path = self._resize_image_if_needed(abs_img_path, min_dimension=16, llm_image_recognition=llm_image_recognition)
                
                # 识别图片
                if llm_image_recognition == "doubao":
                    loop = asyncio.get_event_loop()
                    formula = loop.run_until_complete(self._recognize_math_image_doubao(actual_img_path))
                elif llm_image_recognition == "kimi":
                    formula = self._recognize_math_image_kimi(actual_img_path)
                elif llm_image_recognition == "simpletex":
                    formula = self._recognize_math_image_simpletex(actual_img_path)
                else:
                    raise ValueError(f"不支持的图片识别模型: {llm_image_recognition}")
                
                # 记录替换映射（使用唯一占位符）
                placeholder = f"__MATH_FORMULA_{img_idx}__"
                img.replace_with(placeholder)
                replacements.append((placeholder, formula))
            else:
                # 下载失败，使用占位符
                placeholder = f"__MATH_FORMULA_{img_idx}__"
                img.replace_with(placeholder)
                replacements.append((placeholder, "[图片下载失败]"))
        
        # 获取替换后的文本（使用separator=' '以保留文本节点）
        result_text = element_copy.get_text(separator=' ', strip=False)
        
        # 执行替换
        for placeholder, formula in replacements:
            result_text = result_text.replace(placeholder, f"${formula}$")
        
        return result_text.replace(" ", "").strip()

    def _save_page_for_debug(self, question_idx=None, stage="before_click"):
        """
        保存页面HTML和截图到本地，方便调试定位元素
        注意：question_idx 仅用于生成文件名，不影响获取的页面内容。函数会保存完整的页面HTML。
        
        :param question_idx: 题目索引（仅用于生成文件名，可选）
        :param stage: 保存阶段标识（before_click, after_click等）
        :return: 保存的文件路径
        """
        try:
            # 确保调试目录存在
            os.makedirs(self.debug_pages_dir, exist_ok=True)
            
            # 切换到默认内容（确保不在frame中）
            try:
                self.driver.switch_to.default_content()
            except:
                pass
            
            # 等待页面稳定
            time.sleep(0.5)
            
            # 等待页面加载完成（检查document.readyState）
            try:
                WebDriverWait(self.driver, 5).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
            except:
                pass
            
            # 生成文件名（包含时间戳）
            # question_idx 仅用于文件名，不影响获取的页面内容
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if question_idx is not None:
                base_filename = f"q{question_idx}_{stage}_{timestamp}"
            else:
                base_filename = f"page_{stage}_{timestamp}"
            
            # 保存HTML - 获取完整页面的HTML内容
            html_filename = f"{base_filename}.html"
            html_path = os.path.join(self.debug_pages_dir, html_filename)
            
            # 获取完整页面HTML
            page_source = self.driver.page_source
            
            # 检查获取的HTML是否合理（应该包含完整的HTML结构）
            if not page_source or len(page_source) < 500:
                print(f"  ⚠️  警告：获取的页面HTML似乎不完整（大小: {len(page_source)} 字符）")
                print(f"  ⚠️  当前URL: {self.driver.current_url}")
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(page_source)
                
            print(f"  💾 已保存完整页面HTML: {html_path} (大小: {len(page_source)} 字符)")
            
            # 保存截图
            screenshot_filename = f"{base_filename}.png"
            screenshot_path = os.path.join(self.debug_pages_dir, screenshot_filename)
            self.driver.save_screenshot(screenshot_path)
            
            print(f"  📸 已保存页面截图: {screenshot_path}")
            
            return html_path, screenshot_path
        except Exception as e:
            print(f"  ⚠️  保存页面失败: {e}")
            import traceback
            traceback.print_exc()
            return None, None

    def _extract_questions(self, soup_element, session, question_idx, llm_image_recognition):
        """
        提取元素中的图片，识别后替换为LaTeX公式
        """
        # 创建元素的副本以避免修改原始元素
        element_copy = BeautifulSoup(str(soup_element), 'lxml').find()
        
        # 查找所有mathml图片
        img_tags = element_copy.find_all('img', class_='mathml')
        
        # 如果没有图片，直接返回文本
        if not img_tags:
            return element_copy.get_text(strip=True)
        
        # 创建文本替换映射
        replacements = []
        
        for img_idx, img in enumerate(img_tags):
            img_src = img.get('src', '')
            if not img_src:
                continue
            
            # 构建图片保存路径（使用绝对路径）
            img_filename = f"q{question_idx}_img{img_idx}.png"
            img_path = os.path.join(self.images_dir, img_filename)
            abs_img_path = os.path.abspath(img_path)
            
            # 下载图片
            # print(f"  📥 下载图片 {img_idx + 1}/{len(img_tags)}: {img_filename}")
            if self._download_image(img_src, abs_img_path, session):
                # 预处理图片，获取实际使用的图片路径
                actual_img_path = self._resize_image_if_needed(abs_img_path, min_dimension=16, llm_image_recognition=llm_image_recognition)
                # print(f"  🔍 识别图片: {img_filename}")
                if llm_image_recognition == "doubao":
                    loop = asyncio.get_event_loop()
                    formula = loop.run_until_complete(self._recognize_math_image_doubao(actual_img_path))
                elif llm_image_recognition == "kimi":
                    formula = self._recognize_math_image_kimi(actual_img_path)
                elif llm_image_recognition == "simpletex":
                    formula = self._recognize_math_image_simpletex(actual_img_path)
                else:
                    raise ValueError(f"不支持的图片识别模型: {llm_image_recognition}")

                
                # print(f"  ✅ 识别结果: {formula}")
                
                # 记录替换映射（使用唯一占位符）
                placeholder = f"__MATH_FORMULA_{img_idx}__"
                img.replace_with(placeholder)
                replacements.append((placeholder, formula))
            else:
                # 下载失败，使用占位符
                placeholder = f"__MATH_FORMULA_{img_idx}__"
                img.replace_with(placeholder)
                replacements.append((placeholder, "[图片下载失败]"))
        
        # 获取替换后的文本
        result_text = element_copy.get_text(separator=' ', strip=False)
        
        # 执行替换
        for placeholder, formula in replacements:
            result_text = result_text.replace(placeholder, f"${formula}$")

        return result_text.replace(" ", "")
    
    def _extract_options(self, question_element, session, question_idx, llm_image_recognition):
        """
        提取选择题的选项
        :param question_element: 题目元素
        :param session: requests session
        :param question_idx: 题目索引
        :return: 选项字典{A:内容, B:内容, ...}
        """
        options = {}
        
        # 查找选项容器 - 选项在 span.op-item 中
        question_block = question_element.find_parent('div', class_='question-block')
        if question_block:
            # 查找所有选项 (span.op-item)
            op_items = question_block.find_all('span', class_='op-item')
            
            if op_items:
                # 提取每个选项的内容
                for idx, op_item in enumerate(op_items[:4]):  # 最多4个选项
                    option_letter = ['A', 'B', 'C', 'D'][idx]
                    option_content = self._extract_option_content(op_item, session, question_idx, idx, llm_image_recognition)
                    if option_content:  # 只添加非空选项
                        options[option_letter] = option_content
                        print(f"  选项{option_letter}: {option_content}")
        
        return options

    def _extract_answer(self, session, question_idx, llm_image_recognition):
        """
        提取选择题的答案
        :param driver: Selenium driver
        :param session: requests session
        :param question_idx: 题目索引
        :return: 答案内容
        """
        answer_content = ""
        
        # 首先等待 QuestionView 元素加载完成
        try:
            # print(f"  ⏳ 等待题目元素加载...")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "li.QuestionView"))
            )
            # print(f"  ✅ 题目元素已加载")
        except Exception as e:
            print(f"  ⚠️  等待题目元素加载超时: {e}")
        
        q_mc_selenium = None
        try:
            # print(f"  🖱️  尝试通过题目索引定位第 {question_idx} 题...")
            xpath_q_mc = f"(//li[@class='QuestionView'])[{question_idx}]//div[@class='question-block']//div[@class='q-mc']"
            
            # 等待元素出现
            q_mc_selenium = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath_q_mc))
            )
            # print(f"  ✅ 成功定位到 q-mc 元素")
        except Exception as e1:
            print(f"  ⚠️  通过索引定位失败: {e1}")
            # 如果定位失败，尝试使用CSS选择器作为备用方案
            try:
                question_elements = self.driver.find_elements(By.CSS_SELECTOR, "ul li div.q-tit")
                if question_idx <= len(question_elements):
                    # 找到对应的QuestionView
                    target_question = question_elements[question_idx - 1]
                    # 向上查找QuestionView，然后找q-mc
                    question_view = target_question.find_element(By.XPATH, "./ancestor::li[@class='QuestionView']")
                    q_mc_selenium = question_view.find_element(By.CSS_SELECTOR, "div.question-block div.q-mc")
            except Exception as e2:
                print(f"  ⚠️  备用定位方案也失败: {e2}")
                return "（无法定位题目元素）"
        
        if q_mc_selenium is None:
            return "（无法定位题目元素）"
        
        # 滚动到元素可见
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", q_mc_selenium)
        time.sleep(0.5)
        
        # 等待元素可点击
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(q_mc_selenium)
            )
        except:
            pass  # 如果等待超时，继续尝试点击
        
        # 点击 q-mc 区域 
        # print(f"  🖱️  点击题目区域以显示答案...")
        clicked = False
        
        # 使用 Selenium 原生 click（最接近真实鼠标点击）
        try:
            q_mc_selenium.click()
            clicked = True
            # print(f"  ✅ 使用原生 click 成功")
        except Exception as e1:
            print(f"  ⚠️  原生 click 失败: {e1}")
        
        if clicked:
            time.sleep(1)  # 等待答案加载
                
        # 重新解析页面以获取更新后的答案
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, "lxml")
        
        # 重新定位题目元素
        question_element_updated = None
        
        # 通过索引定位
        q_tit_elements = soup.select("ul li div.q-tit")
        if question_idx <= len(q_tit_elements):
            question_element_updated = q_tit_elements[question_idx - 1]

        # 查找答案部分 - 答案在 J_ana_ans 中
        analyze_div = question_element_updated.find_next('div', class_='q-analyize')

        if analyze_div:
            # print(f"  📥 找到答案部分") 
            # 查找答案部分 - 先找 J_ana_ans 容器
            ans_item = analyze_div.find('div', class_='J_ana_ans')
            if ans_item:
                # 查找答案内容 (div.q-analyize-mc)
                ans_mc = ans_item.find('div', class_='q-analyize-mc')
                if ans_mc:
                    # 检查答案中是否有图片
                    img_tags = ans_mc.find_all('img')
                    if img_tags:
                        # 有图片，需要识别
                        for img_idx, img in enumerate(img_tags):
                            img_src = img.get('src', '')
                            if not img_src:
                                continue
                            
                            img_filename = f"q{question_idx}_ans_img{img_idx}.png"
                            # print(f"  📥 下载答案图片: {img_filename}")
                            img_path = os.path.join(self.images_dir, img_filename)
                            abs_img_path = os.path.abspath(img_path)
                            
                            if self._download_image(img_src, abs_img_path, session):
                                # 预处理图片，获取实际使用的图片路径
                                actual_img_path = self._resize_image_if_needed(abs_img_path, min_dimension=16, llm_image_recognition=llm_image_recognition)
                                if llm_image_recognition == "doubao":
                                    loop = asyncio.get_event_loop()
                                    formula = loop.run_until_complete(self._recognize_math_image_doubao(actual_img_path))
                                elif llm_image_recognition == "kimi":
                                    formula = self._recognize_math_image_kimi(actual_img_path)
                                elif llm_image_recognition == "simpletex":
                                    formula = self._recognize_math_image_simpletex(actual_img_path)
                                else:
                                    raise ValueError(f"不支持的图片识别: {llm_image_recognition}")
                                answer_content += formula
                            else:
                                answer_content += "[图片下载失败]"
                    else:
                        # 没有图片，直接获取文本
                        answer_content = ans_mc.get_text(strip=True)
                    
                    # 清理答案内容
                    answer_content = answer_content.strip()
                        
        return answer_content

    def _scrape_questions_and_options(self, knowledge_points, llm_image_recognition):
        """ 搜索并抓取题目 """
        # 确保 knowledge_points 是列表
        if isinstance(knowledge_points, str):
            knowledge_points = [knowledge_points]
        
        print(f"🌐 正在访问：{self.question_bank_url}")
        self.driver.get(self.question_bank_url)

        # 等待页面加载完成，特别是左侧知识树区域
        time.sleep(self.wait_time)
        
        # 等待左侧搜索框出现（根据HTML结构：form#J_ltsrchFrm > input[name='know_txt']）
        print("🔍 正在定位搜索框...")
        search_box = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='know_txt'], #J_ltsrchFrm input[type='text'], .fm-txt"))
        )

        match_count = 0
        # 对每个 keyword 依次处理
        for keyword_idx, keyword in enumerate(knowledge_points, 1):
            print(f"\n📝 【{keyword_idx}/{len(knowledge_points)}】 处理关键词: {keyword}")
            
            # 在搜索框中输入关键词
            # print(f"📝 在搜索框中输入关键词: {keyword}")
            search_box.clear()
            search_box.send_keys(keyword)
            time.sleep(1)
            search_box.send_keys(Keys.ENTER)  
            time.sleep(self.wait_time + 2)

            # 点击左侧对应知识点
            try:
                # 等待搜索结果出现（搜索结果通常在 .list-tree-search-list 或 .list-ts-chbox 区域）
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".list-ts-item, .J_ListTsItem"))
                )
                time.sleep(1)  # 额外等待搜索结果渲染
                
                # 查找所有匹配的条目
                all_matches = []
                try:
                    # 查找所有匹配的条目
                    all_matches = self.driver.find_elements(By.XPATH, f"//span[@class='ts-tit' and contains(., '{keyword}')]/ancestor::li[contains(@class, 'list-ts-item')]")
                    if not all_matches:
                        raise Exception("未找到匹配的知识点条目")
                    match_count += len(all_matches)
                    print(f"📊 找到 {len(all_matches)} 个匹配的知识点")
                    
                    # 遍历所有匹配的知识点并依次点击
                    for idx, item in enumerate(all_matches, 1):
                        try:
                            text_content = item.find_element(By.CSS_SELECTOR, "span.ts-tit").text.strip()
                            
                            # 检查是否已经被点击过（是否有checked类）
                            item_classes = item.get_attribute("class")
                            if item_classes and "checked" in item_classes:
                                print(f"  ⏭️  [{idx}/{len(all_matches)}] 知识点已选中，跳过: {text_content}")
                                continue
                            
                            print(f"  👆 [{idx}/{len(all_matches)}] 正在点击知识点: {text_content}")
                            
                            # 滚动元素到可视区域（这是关键步骤，避免element not interactable错误）
                            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", item)
                            time.sleep(0.5)
                            
                            # 确保元素可见
                            self.driver.execute_script("arguments[0].style.display = 'block';", item)
                            WebDriverWait(self.driver, 10).until(
                                EC.visibility_of(item)
                            )
                            
                            # 使用JavaScript点击
                            self.driver.execute_script("arguments[0].click();", item)
                            # print(f"✅ 成功点击知识点: {text_content}")
                            time.sleep(1)
                            
                        except Exception as e:
                            print(f"⚠️ 点击第 {idx} 个知识点时出错: {e}")
                            continue
                    
                    # print(f"✅ 已完成关键词 '{keyword}' 的所有知识点的点击，共点击 {len(all_matches)} 个知识点")
                    
                except Exception as e:
                    print(f"⚠️ 匹配过程中出现错误: {e}")
                    print(f"⚠️ 关键词 '{keyword}' 未找到匹配的知识点条目，继续处理下一个关键词")
                    continue
            except Exception as e:
                print(f"⚠️ 未找到左侧菜单【{keyword}】，继续处理下一个关键词")
                continue
        
        print(f"\n✅ 已完成所有关键词的处理，共处理 {len(knowledge_points)} 个关键词, 点击 {match_count} 个知识点")
        if match_count == 0:
            return None, None, None, None, None
        
        # 点击完知识点后，设置筛选条件：来源=高考真题，时间=2025
        try:
            time.sleep(1)  # 等待页面更新
            
            # # 1. 选择来源：高考真题 (data-param="question_source=11")
            # try:
            #     source_link = WebDriverWait(self.driver, 10).until(
            #         EC.element_to_be_clickable((By.XPATH, "//a[@data-param='question_source=11' and contains(text(), '高考真题')]"))
            #     )
            #     self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", source_link)
            #     time.sleep(0.5)
            #     self.driver.execute_script("arguments[0].click();", source_link)
            #     print("✅ 成功选择来源：高考真题")
            #     time.sleep(1)
            # except Exception as e:
            #     print(f"⚠️ 选择来源时出错: {e}")
            
            # 2. 选择时间：2025 (data-param="year=2025")     
            year_link = None
            try:
                year_link = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//a[@data-param='year=2025']"))
                )
            except Exception as e1:
                print(f"📌 2025选项不可见：{e1}")
     
            # 如果找到了2025选项，点击它
            if year_link:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", year_link)
                time.sleep(0.5)
                self.driver.execute_script("arguments[0].click();", year_link)
                print("✅ 成功选择年份：2025")
                time.sleep(1)
            else:
                print("⚠️ 未找到2025选项")
                
        except Exception as e:
            print(f"⚠️ 设置筛选条件时出错: {e}")

        # 创建requests session以保持cookies（用于下载图片）
        session = requests.Session()
        for cookie in self.driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])
        
        # 确保图片目录存在
        os.makedirs(self.images_dir, exist_ok=True)
        
        # 收集所有页面的题目，并记录每页的题目索引范围
        all_questions = []
        
        page_num = 1
        while page_num <= 10:
            # print(f"\n📄 正在抓取第 {page_num} 页的题目...")
            
            # 等待页面加载完成
            time.sleep(self.wait_time)
            
            # 解析当前页面的题目内容
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, "lxml")
            page_questions = soup.select("ul li div.q-tit")
            
            # print(f"🧐 第 {page_num} 页发现 {len(page_questions)} 道题。")

            # 将当前页的题目添加到总列表中（记录题目内容、页码和页面索引）
            for page_index, q_tit in enumerate(page_questions):
                question_info = {
                    'content': q_tit,
                    'page_num': page_num,
                    'page_index': page_index
                }
                all_questions.append(question_info)
            
            # 检查是否有"下一页"按钮
            try:
                # 查找"下一页"链接：在pagenum div中查找包含"下一页"文本的a标签
                next_page_link = self.driver.find_element(By.XPATH, "//div[@class='pagenum']//a[contains(text(), '下一页')]")
                
                # 检查链接是否可点击（可能被禁用或隐藏）
                if next_page_link.is_displayed() and next_page_link.is_enabled():
                    # print(f"➡️ 找到'下一页'按钮，准备翻页...")
                    # 滚动到分页区域
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_page_link)
                    time.sleep(0.5)
                    # 点击下一页
                    self.driver.execute_script("arguments[0].click();", next_page_link)
                    page_num += 1
                    # 等待页面加载 - 等待题目元素出现
                    try:
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "ul li div.q-tit"))
                        )
                        time.sleep(self.wait_time)  # 额外等待确保页面完全加载
                    except Exception as e:
                        print(f"⚠️ 等待新页面加载时出错: {e}，继续尝试...")
                        time.sleep(self.wait_time + 1)
                else:
                    # print(f"✅ 已到达最后一页（'下一页'按钮不可用）")
                    break
            except Exception as e:
                # 如果没有找到"下一页"按钮，说明已经是最后一页
                # print(f"✅ 已到达最后一页（未找到'下一页'按钮）")
                break
        
        if page_num > 10:
            print(f"⚠️ 已到达10页限制，提前退出抓取...")
            
        print(f"\n📊 所有页面抓取完成，共发现 {len(all_questions)} 道题。")

        # 过滤掉有小题的题目（q-mc中包含q-bd-list的题目）+ 本身就是小题的题目（q-tit的祖父是q-bd-list）+ 包含"如图"的题目
        questions_without_subquestions = []
        for idx, question_info in enumerate(all_questions):
            q_tit = question_info['content']
            page_num_info = question_info['page_num']
            page_index_info = question_info['page_index']
            
            # 检查1: 如果q-tit的祖父是q-bd-list，说明这是小题，需要过滤
            parent = q_tit.parent
            if parent:
                grandparent = parent.parent
                if grandparent and grandparent.name == "ol" and "q-bd-list" in grandparent.get("class", []):
                    # print(f"  ⚠️ 第 {idx + 1} 题是小题目（祖父是q-bd-list），跳过")
                    continue
            
            # 检查2: q_tit向上查找祖先元素，找到 QuestionView
            question_view = q_tit.find_parent("li", class_="QuestionView")
            # QuestionView向下查找后代元素 q-mc
            q_mc = question_view.find("div", class_="q-mc")
            # 检查q-mc中是否有q-bd-list（代表有小题）
            q_bd_list = q_mc.find("ol", class_="q-bd-list")
            if q_bd_list:
                # print(f"  ⚠️ 第 {idx + 1} 题有小题，跳过")
                continue
                    
            # 检查3: 检查题目文本中是否包含"如图"/"如表"，或者q-tit是否有子节点p
            q_text_raw = q_tit.get_text(strip=False)
            has_figure_text = "如图" in q_text_raw or "如表" in q_text_raw
            has_p_child = q_tit.find("p") is not None
            has_table_child = q_tit.find("table") is not None
            if has_figure_text or has_p_child or has_table_child:
                # print(f"  ⚠️ 第 {idx + 1} 题包含图/表，跳过")
                continue
            
            # 检查4: 检查op-item-meat中的img是否写了class="mathml"，没写的话说明选项中有图
            op_item_meats = q_mc.find_all("span", class_="op-item-meat")
            has_image_in_options = False
            for op_item_meat in op_item_meats:
                img_tags = op_item_meat.find_all("img")
                for img in img_tags:
                    img_class = img.get("class", [])
                    if "mathml" not in img_class:
                        has_image_in_options = True
                        break
                if has_image_in_options:
                    break
            if has_image_in_options:
                # print(f"  ⚠️ 第 {idx + 1} 题选项中有图（img没有class='mathml'），跳过")
                continue
            
            # 没有小题且不包含图表，保留这个题目
            questions_without_subquestions.append((idx, q_tit, page_num_info, page_index_info))

        print(f"🔦 过滤后，共有 {len(questions_without_subquestions)} 道没有小题且不包含图表的题目。")

        # 随机选择一道题
        if len(questions_without_subquestions) == 0:
            print("⚠️ 未找到任何符合条件的题目")
            return None, None, None, None, None
        
        selected_item = random.choice(questions_without_subquestions)
        selected_idx, selected_q, selected_page_num, selected_page_index = selected_item
        actual_idx = selected_idx + 1  # 题目编号从1开始
        print(f"🔍 选择总题号: {actual_idx}的题目，位于第{selected_page_num}页，第{selected_page_index}个题目")
        
        # 提取题目文本，并识别其中的数学公式图片
        q_text = self._extract_questions(selected_q, session, actual_idx, llm_image_recognition)
        print(f"📃 题目: {q_text}")
        # 提取选项
        options = self._extract_options(selected_q, session, actual_idx, llm_image_recognition)
        print(f"📃 选项: {options}")
        # 返回最终使用的关键词、题目索引和选项，以及题目所在的页码
        return actual_idx, options, q_text, selected_page_num, selected_page_index

    def _scrape_answers(self, knowledge_points, question_idx, page_num, page_index, llm_image_recognition):
        """ 
        重复搜索步骤，然后直接提取答案
        :param knowledge_points: 搜索关键词列表
        :param question_idx: 题目索引（从1开始）
        :param page_num: 页面编号
        :param page_index: 页面中的题目index
        :return: 答案文本
        """
        # 确保 knowledge_points 是列表
        if isinstance(knowledge_points, str):
            knowledge_points = [knowledge_points]
        
        # print(f"🌐 正在访问：{self.question_bank_url}")
        self.driver.get(self.question_bank_url)

        # 等待页面加载完成，特别是左侧知识树区域
        time.sleep(self.wait_time)
        
        # 等待左侧搜索框出现（根据HTML结构：form#J_ltsrchFrm > input[name='know_txt']）
        # print("🔍 正在定位搜索框...")
        search_box = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='know_txt'], #J_ltsrchFrm input[type='text'], .fm-txt"))
        )

        # 对每个 keyword 依次处理
        for keyword_idx, keyword in enumerate(knowledge_points, 1):
            # print(f"\n📝 [{keyword_idx}/{len(knowledge_points)}] 处理关键词: {keyword}")
            
            # 在搜索框中输入关键词
            # print(f"📝 在搜索框中输入关键词: {keyword}")
            search_box.clear()
            search_box.send_keys(keyword)
            time.sleep(1)
            search_box.send_keys(Keys.ENTER)  
            time.sleep(self.wait_time + 2)

            # 点击左侧对应知识点
            try:
                # 等待搜索结果出现（搜索结果通常在 .list-tree-search-list 或 .list-ts-chbox 区域）
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".list-ts-item, .J_ListTsItem"))
                )
                time.sleep(1)  # 额外等待搜索结果渲染
                
                # 查找所有匹配的条目
                all_matches = []
                try:
                    # 查找所有匹配的条目
                    all_matches = self.driver.find_elements(By.XPATH, f"//span[@class='ts-tit' and contains(., '{keyword}')]/ancestor::li[contains(@class, 'list-ts-item')]")
                    if not all_matches:
                        raise Exception("未找到匹配的知识点条目")
                    
                    # print(f"📊 找到 {len(all_matches)} 个匹配的知识点")
                    
                    # 遍历所有匹配的知识点并依次点击
                    for idx, item in enumerate(all_matches, 1):
                        try:
                            text_content = item.find_element(By.CSS_SELECTOR, "span.ts-tit").text.strip()
                            
                            # 检查是否已经被点击过（是否有checked类）
                            item_classes = item.get_attribute("class")
                            if item_classes and "checked" in item_classes:
                                # print(f"  ⏭️  [{idx}/{len(all_matches)}] 知识点已选中，跳过: {text_content}")
                                continue
                            
                            # print(f"👆 [{idx}/{len(all_matches)}] 正在点击知识点: {text_content}")
                            
                            # 滚动元素到可视区域（这是关键步骤，避免element not interactable错误）
                            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", item)
                            time.sleep(0.5)
                            
                            # 确保元素可见
                            self.driver.execute_script("arguments[0].style.display = 'block';", item)
                            WebDriverWait(self.driver, 10).until(
                                EC.visibility_of(item)
                            )
                            
                            # 使用JavaScript点击
                            self.driver.execute_script("arguments[0].click();", item)
                            # print(f"✅ 成功点击知识点: {text_content}")
                            time.sleep(1)
                            
                        except Exception as e:
                            # print(f"⚠️ 点击第 {idx} 个知识点时出错: {e}")
                            continue
                    
                    # print(f"✅ 已完成关键词 '{keyword}' 的所有知识点的点击，共点击 {len(all_matches)} 个知识点")
                    
                except Exception as e:
                    # print(f"⚠️ 匹配过程中出现错误: {e}")
                    # print(f"⚠️ 关键词 '{keyword}' 未找到匹配的知识点条目，继续处理下一个关键词")
                    continue
            except Exception as e:
                # print(f"⚠️ 未找到左侧菜单【{keyword}】，继续处理下一个关键词")
                continue
        
        # print(f"\n✅ 已完成所有关键词的处理，共处理 {len(knowledge_points)} 个关键词")

        # 点击完知识点后，设置筛选条件：来源=高考真题，时间=2025
        try:
            time.sleep(1)  # 等待页面更新
            
            # # 1. 选择来源：高考真题 (data-param="question_source=11")
            # try:
            #     source_link = WebDriverWait(self.driver, 10).until(
            #         EC.element_to_be_clickable((By.XPATH, "//a[@data-param='question_source=11' and contains(text(), '高考真题')]"))
            #     )
            #     self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", source_link)
            #     time.sleep(0.5)
            #     self.driver.execute_script("arguments[0].click();", source_link)
            #     print("✅ 成功选择来源：高考真题")
            #     time.sleep(1)
            # except Exception as e:
            #     print(f"⚠️ 选择来源时出错: {e}")
            
            # 2. 选择时间：2025 (data-param="year=2025")     
            year_link = None
            try:
                year_link = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//a[@data-param='year=2025']"))
                )
            except Exception as e1:
                print(f"📌 2025选项不可见：{e1}")
     
            # 如果找到了2025选项，点击它
            if year_link:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", year_link)
                time.sleep(0.5)
                self.driver.execute_script("arguments[0].click();", year_link)
                print("✅ 成功选择年份：2025")
                time.sleep(1)
            else:
                print("⚠️ 未找到2025选项")
                
        except Exception as e:
            print(f"⚠️ 设置筛选条件时出错: {e}")

        # 创建requests session以保持cookies（用于下载图片）
        session = requests.Session()
        for cookie in self.driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])
        
        # 确保图片目录存在
        os.makedirs(self.images_dir, exist_ok=True)

        # 翻页到目标页面
        current_page = 1
        while current_page < page_num:
            try:
                # 等待页面加载完成
                time.sleep(self.wait_time)
                
                # 查找"下一页"按钮
                next_page_link = self.driver.find_element(By.XPATH, "//div[@class='pagenum']//a[contains(text(), '下一页')]")
                
                # 检查链接是否可点击
                if next_page_link.is_displayed() and next_page_link.is_enabled():
                    # 滚动到分页区域
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_page_link)
                    time.sleep(0.5)
                    # 点击下一页
                    self.driver.execute_script("arguments[0].click();", next_page_link)
                    current_page += 1
                    # 等待页面加载 - 等待题目元素出现
                    try:
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "ul li div.q-tit"))
                        )
                        time.sleep(self.wait_time)  # 额外等待确保页面完全加载
                    except Exception as e:
                        print(f"⚠️ 等待新页面加载时出错: {e}，继续尝试...")
                        time.sleep(self.wait_time + 1)
                else:
                    print(f"⚠️ 无法翻到第 {page_num} 页（已到达最后一页）")
                    return "（无法翻到目标页面）"
            except Exception as e:
                print(f"⚠️ 翻页时出错: {e}")
                return "（翻页失败）"
        
        # 等待当前页面加载完成
        time.sleep(self.wait_time)
        print(f"\n📥 保存完整页面用于调试...")
        self._save_page_for_debug(question_idx=None, stage="筛选条件")
                
        # 等待题目元素出现，确保页面已加载
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul li div.q-tit"))
            )
        except Exception as e:
            print(f"⚠️ 等待页面加载时出错: {e}")
            return "（页面加载失败）"
        
        # 直接调用_extract_answer，它已经处理了定位、点击和提取答案的逻辑
        # page_index是从0开始的页面内索引，而_extract_answer期望从1开始的索引，所以需要+1
        answer_content = self._extract_answer(session, page_index + 1, llm_image_recognition)
        print(f"📃 答案: {answer_content}")
        return answer_content

    def _convert_choice_to_fill_blank(self, question_text: str, options: Dict[str, str], correct_answer: str) -> Tuple[str, str]:
        """
        将选择题改编为答案唯一的填空题
        """
        print("------------------------------将选择题改编为填空题-----------------------------")
        # 构建选项文本
        options_text = "\n".join([f"{key}: {value}" for key, value in options.items()])
        
        convert_prompt = textwrap.dedent(f"""
            你是一个数学题目改编专家。请将下面的选择题改编为答案唯一的填空题。
            
            【原题目】
            {question_text}
            
            【选项】
            {options_text}
            
            【正确答案】
            {correct_answer}
            
            【改编要求】
            1. 将选择题改编为填空题，要求答案唯一。
            2. 针对题目中带有“下列选项正确的是”的题目，将正确的选项内容和题目融合，例如：
               原选择题：
               甲、乙两个班级各有6名候选人参加校学生会干部竞选其中, 甲班中男生2名, 乙班中男生3名, 则下列说法正确的有()
               A. 从12人中选出两人担任主持人, 恰好一男一女当选的情况有35种
               B. 从12人中随机选择一人总结会议, 己知选到的是女生, 则她来自甲班的概率是1/3
               C. 5名男生随机抽选3人担任男寝棱长, 其中甲班男生当选人数为X人, 则E(X)=6/5
               D. 某选手得分是9, 9.2, 9.2, 9.3, 9.3, 9.4, 9.4, 9.5, 则该选手得分的第70百分位数是9.3
               正确答案：
               A
                
               改编后的填空题：
               甲、乙两个班级各有6名候选人参加校学生会干部竞选其中, 甲班中男生2名, 乙班中男生3名, 从12人中选出两人担任主持人, 恰好一男一女当选的情况有___种
               正确答案：
               35
            3. 针对多选题，只需选择一个正确选项和题目融合成填空题即可，例如：
               原选择题：
               对于直线:(m-1)x+y-2m+3=0, 下列选项正确的是()
               A. 直线恒过点(2,-1)
               B. 当m=0时,直线1在y轴上的截距为3
               C. 已知点A(3, 1), B(-1,2), 若直线与线段AB相交, 则m的取值范围是[0,3]
               D. 坐标原点到直线的距离的最大值为5
               正确答案：
               A,D
               
               改编后的填空题：
               对于直线:(m-1)x+y-2m+3=0, 直线横过哪个点？
               正确答案：
               (2,-1)
               
               原选择题：
               甲乙两人玩游戏.游戏开局时桌上有n盒动漫卡牌,每个盒子上都标有盒内卡牌的数量,每盒卡牌的数量构成数组(a1,a2,..,an),游戏规则如下:两人轮流抽牌,每人每次只能择其中一盒并抽走至少ー张卡牌,若轮到某人时无卡可抽,则该人输掉游戏.现由甲先抽,则下列开局中,能确保甲有必胜策略的是()
               A. (1,3)
               B. (1,2,3)
               C. (3,3,6)
               D. (3,4,5)
               正确答案：
               A,C,D
               
               改编后的填空题：
               甲乙两人玩游戏.游戏开局时桌上有n盒动漫卡牌,每个盒子上都标有盒内卡牌的数量,每盒卡牌的数量构成数组(a1,a2,..,an),游戏规则如下:两人轮流抽牌,每人每次只能择其中一盒并抽走至少ー张卡牌,若轮到某人时无卡可抽,则该人输掉游戏.现由甲先抽,则开局(1,3)是否能确保甲有必胜策略()
               正确答案：
               是
               
            【输出要求】
            请以JSON格式输出，包含以下字段：
            - "question": 改编后的题目文本
            - "answer": 改编后的答案文本

            示例格式：
            {{
                "question": "改编后的题目内容",
                "answer": "改编后的答案"
            }}

            注意：只输出JSON，不要输出其他任何文字说明。
            """)
        
        try:
            response = self.llm.chat(convert_prompt, system="你是一个专业的数学题目改编专家。").strip()
            if response and response != "❌":
                # 提取JSON
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group(0))
                    converted_question = result.get("question", "").strip()
                    converted_answer = result.get("answer", correct_answer).strip()
                    
                    if converted_question:
                        print(f"✅ 选择题改编完成")
                        print(f"改编后的题目：\n{converted_question}")
                        print(f"改编后的答案：\n{converted_answer}")
                        return converted_question, converted_answer
                    else:
                        print("⚠️ JSON解析成功但题目为空，使用原题目")
                        return question_text, correct_answer
                else:
                    print("⚠️ 无法从响应中提取JSON，使用原题目")
                    return question_text, correct_answer
            else:
                print("⚠️ 大模型改编失败，使用原题目")
                return question_text, correct_answer
        except Exception as e:
            print(f"⚠️ 调用大模型改编题目时出错: {e}，使用原题目")
            return question_text, correct_answer

    def _retrieve_problems_from_web(self, knowledge_points: List[str]) -> tuple:
        """ 从网络检索题目，返回题目文本和答案 """
        # 获得题目和选项
        # 使用第一个知识点作为搜索关键词
        if not knowledge_points:
            print("⚠️ 没有提供知识点，无法检索题目")
            return "", ""
        
        llm_image_recognition = "simpletex" # 可选“doubao”、“kimi”、“simpletex”
        
        question_idx, options, q_text, page_num, page_index = self._scrape_questions_and_options(knowledge_points, llm_image_recognition)
        # 获得答案
        if question_idx and q_text:
            ans_text = self._scrape_answers(knowledge_points, question_idx, page_num, page_index, llm_image_recognition)

            if options:
                print(f"选择题识别完成")
                # 针对选择题做特殊处理：改编为答案唯一的填空题
                q_text, ans_text = self._convert_choice_to_fill_blank(q_text, options, ans_text)
            else:
                print(f"填空题识别完成")
        else:
            print("⚠️ 未能获取题目信息，跳过答案提取")
            return "", ""        
        return q_text, ans_text
    
    def generate_novel1(
        self,
        item: ProblemItem,
        llm_extract: Optional[LLMClient] = None,
        llm_retrieve: Optional[LLMClient] = None,
        llm_paraphrase: Optional[LLMClient] = None,
        all_knowledge_points: Optional[List[str]] = None,
    ) -> ProblemItem:
        """
        novel-1：recent-source adaptation via structured retrieval and paraphrasing
        1. 提取题目的主要知识点
        2. 基于知识点检索/生成匹配的2025年最新考试题目（模拟从题库检索）
        3. 改写检索到的题目
        """
        llm_extract = llm_extract or self.llm
        llm_retrieve = llm_retrieve or self.llm
        llm_paraphrase = llm_paraphrase or self.llm
        
        if all_knowledge_points is None:
            raise ValueError("all_knowledge_points must be provided")
        
        print("--------------------------------提取题目知识点--------------------------------")
        knowledge_points = self._extract_knowledge_points(
            item.original_question, 
            llm_extract, 
            item.solution,
            available_knowledge_points=all_knowledge_points
        )
        print(f"提取到的知识点：{knowledge_points}")
        
        if not knowledge_points:
            print("警告：未能提取到知识点")
            return None
        
        print("---------------------------------网络检索题目---------------------------------")
        retrieved_problem, retrieved_answer = self._retrieve_problems_from_web(knowledge_points)
        
        if not retrieved_problem:
            print("警告：未能检索到题目")
            item.augmented_question = "x"
            item.augmented_true_answer = "x"
            item.method_used = "novel-1"
            return item
        
        print("----------------------------------重述题目----------------------------------")
        # 改写检索到的题目
        example_original = r"1.(2025·开福模拟)已知菱形$ABCD$的边长为$1，∠DAB=60°。E$是$BC$的中点，$AE$与$BD$相交于点$F$。则$$\overrightarrow{AF}\cdot\overrightarrow{AB}=$$（  ）"
        example_modified = r"已知菱形$ABCD$的边长为$1，∠DAB=60°。最近小区里新种了很多绿植，环境变得更优美了。E$是$BC$的中点，$AE$与$BD$相交于点$F$。则$$\overrightarrow{AF}\cdot\overrightarrow{AB}=$$（  ）"
        
        paraphrase_prompt = textwrap.dedent(f"""
            你是一个数学题目改写专家。任务是对题目进行重述，生成一道新的题目。
            
            【示例】
            {example_original}
            调整为：
            {example_modified}
            
            【改写要求】
            1. 去掉题目开头可能存在的题号和题目来源，例如“1.(2025·开福模拟)”、“9.(2025高三上·宁波期末)”等。
            2. 对原题的内容进行重述，保持原题的语义、数字和答案不变，只是换一种说法。
            
            请按照示例的方法改写下面的题目：
            {retrieved_problem}
            """)
        paraphrased_problem = llm_paraphrase.chat(paraphrase_prompt).strip()
        
        print(f"检索到的题目：\n{retrieved_problem}")
        print(f"重述后的题目：\n{paraphrased_problem}")
        item.augmented_question = paraphrased_problem
        item.augmented_true_answer = retrieved_answer  # 记录检索到的答案
        item.method_used = "novel-1"
        return item

    def _load_knowledge_base(self) -> Dict:
        """
        加载从教材构建的知识库
        """
        if self.knowledge_base_path.exists():
            try:
                with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.knowledge_base = data
                    print(f"已加载知识库：{self.knowledge_base_path}")
                    if data.get("_metadata", {}).get("pdf_files"):
                        print(f"知识库目前包含从以下PDF文件提取的知识点：{', '.join(data['_metadata']['pdf_files'])}")
                    return self.knowledge_base
            except Exception as e:
                print(f"加载知识库失败：{e}")
                return None
            
        else:
            # 知识库文件不存在，创建新的空白知识库
            print(f"知识库文件不存在：{self.knowledge_base_path}，正在创建空白知识库...")
            # 确保目录存在
            self.knowledge_base_path.parent.mkdir(parents=True, exist_ok=True)
            # 创建空白知识库
            empty_kb = {"_metadata": {"pdf_files": []}}
            try:
                with open(self.knowledge_base_path, 'w', encoding='utf-8') as f:
                    json.dump(empty_kb, f, ensure_ascii=False, indent=2)
                self.knowledge_base = empty_kb
                print(f"已创建空白知识库：{self.knowledge_base_path}")
                return empty_kb
            except Exception as e:
                print(f"创建知识库失败：{e}")
                return None
    
    def _split_pdf_by_size(self, pdf_path: Path, max_size_mb: int = 90) -> List[Path]:
        """
        将PDF文件切割为多个不超过指定大小的文件
        """
        if PdfReader is None or PdfWriter is None:
            raise ImportError("需要安装PDF处理库：pip install pypdf")
        
        max_size_bytes = max_size_mb * 1024 * 1024
        file_size = pdf_path.stat().st_size

        # 读取PDF
        reader = PdfReader(str(pdf_path))
        total_pages = len(reader.pages)
        
        # 估算每页的平均大小
        avg_page_size = file_size / total_pages
        pages_per_chunk = int(max_size_bytes / avg_page_size * 0.9)  # 留10%余量
        pages_per_chunk = max(1, pages_per_chunk)  # 至少1页
        
        split_files = []
        temp_dir = tempfile.mkdtemp()
        
        try:
            for chunk_start in range(0, total_pages, pages_per_chunk):
                chunk_end = min(chunk_start + pages_per_chunk, total_pages)
                chunk_pages = list(range(chunk_start, chunk_end))
                
                # 创建新的PDF文件
                writer = PdfWriter()
                for page_num in chunk_pages:
                    writer.add_page(reader.pages[page_num])
                
                # 保存切割后的文件
                chunk_filename = f"{pdf_path.stem}_part_{chunk_start//pages_per_chunk + 1}.pdf"
                chunk_path = Path(temp_dir) / chunk_filename
                
                with open(chunk_path, 'wb') as f:
                    writer.write(f)
                
                chunk_size = chunk_path.stat().st_size
                split_files.append(chunk_path)
                print(f"已创建切割文件：{chunk_filename} ({chunk_size / (1024*1024):.2f}MB, 第{chunk_start+1}-{chunk_end}页)")
            
            return split_files
            
        except Exception as e:
            # 清理临时文件
            for f in split_files:
                if f.exists():
                    f.unlink()
            if Path(temp_dir).exists():
                shutil.rmtree(temp_dir)
            raise e

    def build_knowledge_base_from_pdf(self, pdf_path: Optional[Union[str, Path]] = None, merge: bool = True) -> Dict:
        """
        从PDF文件构建知识库
        """
        if isinstance(pdf_path, str):
            pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            print(f"错误：PDF文件不存在：{pdf_path}")
            return {}
        
        pdf_filename = pdf_path.name
        file_size = pdf_path.stat().st_size
        file_size_mb = file_size / (1024 * 1024)
        
        # 加载现有知识库
        existing_kb = self._load_knowledge_base()
        if not merge:
            # 如果不合并，则创建新的知识库，建立空白metadata
            existing_kb = {"_metadata": {"pdf_files": []}}
        
        # 检查PDF是否已经在知识库中
        if pdf_filename in existing_kb.get("_metadata", {}).get("pdf_files", []):
            print(f"警告：PDF文件 {pdf_filename} 已经在知识库中")
            while True:
                choice = input("请选择处理方式：\n  1. 覆盖 - 用新内容替换原有内容\n  2. 保留 - 保留原有内容，跳过处理\n请输入选项 (1/2): ").strip()
                if choice == "1":
                    print("将使用新内容覆盖原有内容")
                    # 删除所有pdf字段等于pdf_filename的知识点条目
                    keys_to_delete = []
                    for key, value in existing_kb.items():
                        if isinstance(value, dict) and value.get("pdf") == pdf_filename:
                            keys_to_delete.append(key)
                    for key in keys_to_delete:
                        del existing_kb[key]
                    print(f"已删除 {len(keys_to_delete)} 个来自该PDF的知识点条目")
                    break
                elif choice == "2":
                    print("保留原有内容，跳过处理")
                    return existing_kb
                else:
                    print("无效选项，请输入 1 或 2")
        
        # 检查文件大小，如果超过100MB则切割
        split_files = []
        temp_dir = None
        try:
            if file_size_mb > 100:
                print(f"PDF文件大小 {file_size_mb:.2f}MB 超过100MB限制，需要切割")
                split_files = self._split_pdf_by_size(pdf_path, max_size_mb=90)
                temp_dir = split_files[0].parent if split_files else None
                print(f"已切割为 {len(split_files)} 个文件")
            else:
                split_files = [pdf_path]
            
            # 依次处理每个PDF文件（可能是原文件或切割后的文件）
            all_new_knowledge = {}
            
            for idx, file_to_process in enumerate(split_files, 1):
                if len(split_files) > 1:
                    print(f"\n处理由{pdf_filename}切割出的第 {idx}/{len(split_files)} 个文件：{file_to_process.name}")
                else:
                    print(f"解析PDF文件：{pdf_path}...")
                
                # 使用kimi_client解析PDF
                try:
                    file_object = kimi_client.files.create(
                        file=file_to_process,
                        purpose="file-extract"
                    )
                    
                    # 获取解析后的文本内容
                    file_content = kimi_client.files.content(file_id=file_object.id).text
                    if len(split_files) > 1:
                        print(f"第 {idx} 个文件解析完成，开始整理知识点...")
                    else:
                        print("PDF解析完成，开始整理知识点...")
                    
                    # 使用LLM整理PDF内容，提取知识点、概念、性质、定理、示例
                    system_prompt = (
                        "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你擅长中文和英文的对话。"
                        "你会为用户提供安全，有帮助，准确的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"
                    )
                    
                    extract_prompt = textwrap.dedent(f"""
                        解析这个pdf中，把所有知识点和其对应的概念/性质/定理/示例整理到一起。

                        请以JSON格式输出，格式如下：
                        {{
                            "知识点1": {{
                                "概念": ["概念1", "概念2", ...],
                                "性质": ["性质1", "性质2", ...],
                                "定理": ["定理1", "定理2", ...],
                                "示例": ["示例1", "示例2", ...]
                            }},
                            "知识点2": {{
                                ...
                            }}
                        }}

                        字段说明：
                        - "概念"：包含所有定义性内容，如"给定两个集合A和B,如果组成它们的元素完全相同,就称这两个集合相等"、"集合可以根据它含有的元素个数分为两类:含有有限个元素的集合称为有限集,含有无限个元素的集合称为无限集"等。所有定义、分类说明、概念描述都应放在这里。
                        - "性质"：包含所有性质描述、运算规律、结论等，如"空集可以看成包含0个元素的集合,所以空集是有限集"、"如果a∈N且b∈N,则a+b∈N"、"集合具有互异性：对于一个给定的集合，集合中的元素一定是不同的．"等。所有性质、规律都应放在这里。
                        - "定理"：包含所有需要证明的定理、命题等。
                        - "示例"：包含所有具体的例子、例题等。

                        注意：
                        1. pdf中每个章节可能包含多个知识点，每个知识点可能包含多个概念、性质、定理、示例，必须详尽整理，不能遗漏。
                        2. 并不是每个知识点都有对应的四者：概念、性质、定理、示例，pdf中有对应内容则添加，没有的话不必强行添加。
                        3. 整理时尽量保持原来的完整描述，例如pdf中内容为："互异性：对于一个给定的集合，集合中的元素一定是不同的。"，则应该完整添加到知识库中，而不是添加为简略形式："互异性：集合中的元素互不相同。"。
                        4. 特别注意：所有定义性内容（包括"称为"、"记作"、"定义为"等表述）都应归入"概念"字段。
                        5. 确保输出是有效的JSON格式，不要包含任何其他解释文字。
                        """)
                    
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "system", "content": file_content},
                        {"role": "user", "content": extract_prompt},
                    ]
                    
                    completion = kimi_client.chat.completions.create(
                        model="kimi-k2-turbo-preview",
                        messages=messages,
                        temperature=0.3,
                    )
                    
                    knowledge_text = completion.choices[0].message.content.strip()
                    
                    # 尝试提取JSON部分（可能包含markdown代码块）
                    json_match = re.search(r'\{[\s\S]*\}', knowledge_text)
                    if json_match:
                        knowledge_text = json_match.group(0)
                    
                    # 解析JSON
                    chunk_knowledge = json.loads(knowledge_text)
                    
                    # 给每个知识点添加"pdf"字段，并合并到本次pdf处理的全部知识库中（排除metadata字段）
                    for key, value in chunk_knowledge.items():
                        # 添加pdf字段
                        value["pdf"] = pdf_filename
                        
                        if key in all_new_knowledge:
                            # 如果知识点已存在，合并内容
                            existing_entry = all_new_knowledge[key]
                            new_entry = value
                            # 合并概念（去重）
                            if "概念" in new_entry:
                                existing_concepts = set(existing_entry.get("概念", []))
                                existing_concepts.update(new_entry["概念"])
                                existing_entry["概念"] = list(existing_concepts)
                            # 合并性质（去重）
                            if "性质" in new_entry:
                                existing_props = set(existing_entry.get("性质", []))
                                existing_props.update(new_entry["性质"])
                                existing_entry["性质"] = list(existing_props)
                            # 合并定理（去重）
                            if "定理" in new_entry:
                                existing_theorems = set(existing_entry.get("定理", []))
                                existing_theorems.update(new_entry["定理"])
                                existing_entry["定理"] = list(existing_theorems)
                            # 合并示例（去重）
                            if "示例" in new_entry:
                                existing_examples = set(existing_entry.get("示例", []))
                                existing_examples.update(new_entry["示例"])
                                existing_entry["示例"] = list(existing_examples)
                        else:
                            all_new_knowledge[key] = value
                    
                except Exception as e:
                    print(f"处理第 {idx} 个文件时出错：{e}")
                    import traceback
                    traceback.print_exc()
                    continue
            
            # 将所有新知识添加到现有知识库（排除metadata字段）
            for key, value in all_new_knowledge.items():
                existing_kb[key] = value
            
            # 更新metadata，添加PDF文件名
            if "_metadata" not in existing_kb:
                existing_kb["_metadata"] = {"pdf_files": []}
            if pdf_filename not in existing_kb["_metadata"]["pdf_files"]:
                existing_kb["_metadata"]["pdf_files"].append(pdf_filename)
            
            # 保存知识库到文件
            with open(self.knowledge_base_path, 'w', encoding='utf-8') as f:
                json.dump(existing_kb, f, ensure_ascii=False, indent=2)
            
            self.knowledge_base = existing_kb
            print(f"知识库构建完成，已保存到：{self.knowledge_base_path}")
            print(f"知识库目前包含的PDF文件：{', '.join(existing_kb['_metadata']['pdf_files'])}")
            return existing_kb
            
        except Exception as e:
            print(f"构建知识库失败：{e}")
            import traceback
            traceback.print_exc()
            return {}
        finally:
            # 清理临时切割文件
            if temp_dir and Path(temp_dir).exists():
                try:
                    shutil.rmtree(temp_dir)
                    print(f"已清理临时文件目录：{temp_dir}")
                except Exception as e:
                    print(f"清理临时文件目录失败：{e}")
    
    def _retrieve_knowledge_from_kb(self, knowledge_base: Dict, knowledge_points: List[str]) -> str:
        """
        从知识库中检索相关知识点内容
        对于同一个knowledge_point，可能知识库中有多个对应的同名条目（来自不同PDF），需要找出所有匹配的条目
        从检索出的内容中随机选择最多三条
        """
        retrieved_content = []
        
        for point in knowledge_points:
            # 遍历知识库中的所有条目，找出所有匹配的条目（排除metadata字段）
            for kb_point, kb_entry in knowledge_base.items():
                # 跳过metadata字段
                if kb_point == "_metadata":
                    continue
                
                # 尝试精确匹配
                if kb_point == point:
                # if kb_point == point or point in kb_point or kb_point in point:
                    # 将每个概念、性质、定理、示例分别作为独立的条目
                    if "概念" in kb_entry and kb_entry["概念"]:
                        for concept in kb_entry["概念"]:
                            retrieved_content.append(concept)
                    
                    if "性质" in kb_entry and kb_entry["性质"]:
                        for prop in kb_entry["性质"]:
                            retrieved_content.append(prop)
                    
                    if "定理" in kb_entry and kb_entry["定理"]:
                        for theorem in kb_entry["定理"]:
                            retrieved_content.append(theorem)
                    
                    if "示例" in kb_entry and kb_entry["示例"]:
                        for example in kb_entry["示例"]:
                            retrieved_content.append(example)
        
        # 从检索出的内容中随机选择最多三条
        print(f"知识库中检索到相关条目数: {len(retrieved_content)}\n")
        if len(retrieved_content) > 3:
            retrieved_content = random.sample(retrieved_content, 3)
        
        return "\n\n".join(retrieved_content) if retrieved_content else ""
    
    def generate_novel2(
        self,
        item: ProblemItem,
        llm_extract: Optional[LLMClient] = None,
        llm_generate: Optional[LLMClient] = None,
    ) -> ProblemItem:
        """
        novel-2：基于教科书知识库的概念题生成
        """
        llm_extract = llm_extract or self.llm
        llm_generate = llm_generate or self.llm
        
        print("--------------------------------加载知识库--------------------------------")
        knowledge_base = self._load_knowledge_base()
        
        # 从知识库中获取所有知识点（去重，排除metadata）
        all_kb_points = [key for key in knowledge_base.keys() if key != "_metadata"]
        print(f"知识库中共有 {len(all_kb_points)} 个知识点")
        
        print("------------------------------提取题目知识点------------------------------")
        knowledge_points = self._extract_knowledge_points(
            item.original_question, 
            llm_extract, 
            item.solution,
            available_knowledge_points=all_kb_points
        )
        print(f"提取到的知识点：{knowledge_points}")
        
        print("------------------------------检索知识库内容------------------------------")
        retrieved_knowledge = self._retrieve_knowledge_from_kb(knowledge_base, knowledge_points)
        
        if not retrieved_knowledge:
            print("警告：未在知识库中找到相关知识点")
            return None
        else:
            print(f"从检索到的知识库内容中随机抽取3条：\n{retrieved_knowledge}")
        
        print("---------------------------------生成概念题-------------------------------")
        prompt = textwrap.dedent(f"""
            你是一个高级数学命题专家。

            请基于下面从教科书中提取的相关知识点，设计一道概念题，并给出正确答案：
            - 根据知识库中检索到的相关内容（包括概念、性质、定理和示例），设计一道新颖的概念性问题及其正确答案
            - 不能自由发挥，比如检索出的内容是：“若ab=0，则a=0或b=0。”，则不能设计出“两个数的乘积为零，则至少有一个为零的原则称为什么？”这样的题目，因为基于的内容中根本没提到这个原则的名称。
            - 例如针对"逻辑用语"的相关内容，可以设计如下题目及其正确答案：
                {{
                    "origin_statement": "可供真假判断的陈述语句称为命题",
                    "question": "可供真假判断的陈述语句称为什么？", 
                    "answer": "命题"
                }}

            从知识库中选择一条能够设计出概念题的内容，保证正确答案简单且唯一。例如：“等式P(A|B)=P(A)P(B|A)/P(B)称为什么？”就没有“等式P(A|B)=P(A)P(B|A)/P(B)称为什么公式”好，因为前者的答案更固定。
            知识库中检索到的相关内容如下：
            {retrieved_knowledge}
            
            给出你基于的内容、题目和正确答案：

            请以JSON格式输出，格式如下：
            {{
                "origin_statement": "基于的内容",
                "question": "基于内容设计的题目题干，保证正确答案简单且唯一",
                "answer": "正确答案"
            }}

            请确保输出是有效的JSON格式，不要包含任何其他解释文字。
            """)
        resp = llm_generate.chat(prompt)
        
        # 解析JSON响应
        try:
            # 尝试提取JSON部分（可能包含markdown代码块）
            json_match = re.search(r'\{[\s\S]*\}', resp)
            if json_match:
                json_text = json_match.group(0)
            else:
                json_text = resp.strip()
            
            result = json.loads(json_text)
            
            # 提取字段
            origin_statement = result.get("origin_statement", "").strip()
            question = result.get("question", "").strip()
            answer = result.get("answer", "").strip()
            
            # 打印生成的结果
            print(f"基于的内容：{origin_statement}")
            print(f"生成的题目：{question}")
            print(f"正确答案：{answer}")
            
            # 填充item
            item.augmented_question = question
            item.augmented_true_answer = answer
            item.method_used = "novel-2"
            
            if not item.augmented_question:
                print("警告：解析到的题目为空")
                return None
                
        except json.JSONDecodeError as e:
            print(f"警告：无法解析JSON响应：{e}")
            print(f"响应内容：{resp[:200]}...")
            return None
        except Exception as e:
            print(f"警告：解析响应时出错：{e}")
            print(f"响应内容：{resp[:200]}...")
            return None
        
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
                item = self.analogical_transformer.generate_analogical2(
                    item,
                    llm_extract=llms.get("extract"), # 提取知识点
                    llm_codegen=llms.get("codegen"), # 代码生成
                    llm_check=llms.get("check"), # 硬编码检查
                    llm_refine=llms.get("refine"), # 代码修改
                    llm_range=llms.get("range"), # 取值范围
                    llm_variant=llms.get("variant"), # 数字变体
                    llm_final_check=llms.get("final_check"), # 最终题目正确性检查
                )
            # analogical-3
            else:
                llms = self.role_llms
                item = self.analogical_transformer.generate_analogical3(
                    item,
                    llm_extract=llms.get("extract"), # 提取知识点
                    llm_convert=llms.get("convert"), # 答案格式转换
                    llm_analysis=llms.get("analysis"), # 可逆条件分析
                    llm_codegen=llms.get("codegen"), # 代码生成
                    llm_check=llms.get("check"), # 硬编码检查
                    llm_refine=llms.get("refine"), # 代码修改
                    llm_range=llms.get("range"), # 取值范围
                    llm_variant=llms.get("variant"), # 数字变体
                    generate_variant=generate_variant,
                )
            return item

        # 6,7 -> novel-1,2 （新颖题生成）
        if method in {"6", "7"}:
            if not self.novel_generator:
                raise RuntimeError("NovelProblemGenerator 未初始化")
            if method == "6":
                llms = self.role_llms
                # all_knowledge_points should be set before calling process
                if not hasattr(self.novel_generator, '_all_knowledge_points') or self.novel_generator._all_knowledge_points is None:
                    raise RuntimeError("all_knowledge_points must be initialized before processing questions")
                item = self.novel_generator.generate_novel1(
                    item,
                    llm_extract=llms.get("extract"),  # 提取知识点
                    llm_retrieve=llms.get("retrieve") or self.novel_generator.llm,  # 检索题目
                    llm_paraphrase=llms.get("paraphrase") or self.novel_generator.llm,  # 改写题目
                    all_knowledge_points=self.novel_generator._all_knowledge_points,
                )
            else:
                llms = self.role_llms
                item = self.novel_generator.generate_novel2(
                    item,
                    llm_extract=llms.get("extract"),  # 提取知识点
                    llm_generate=llms.get("generate"),  # 生成概念题
                )
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
    print(f"从 {args.input} 中读取原始题目\n输出文件将保存在：{output_path}")
    
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

    redundancy_injector = RedundancyInjector(llm_redundancy)
    analogical_transformer = AnalogicalTransformer(llm_analogical_fallback)
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

    # 如果使用novel-1方法，在处理所有题目之前初始化driver、登录并提取知识点
    if args.method == "6":
        novel_generator.initialize_for_batch_processing()

    # 如果设置了mend_question，需要特殊处理：读取输出文件，删除对应行，然后重新插入
    if args.mend_question:
        # 读取输出文件（如果存在）
        existing_rows = []
        if os.path.exists(output_path):
            with open(output_path, 'r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f)
                existing_rows = list(reader)
            print(f"📖 读取到输出文件，共 {len(existing_rows)} 行")
        
        # 确保列表长度足够（如果输出文件行数少于mend_question，需要补充空行）
        while len(existing_rows) < args.mend_question:
            existing_rows.append([])
        
        # 删除对应行（行号从1开始，索引从0开始）
        if args.mend_question <= len(existing_rows):
            deleted_row = existing_rows.pop(args.mend_question - 1)
            print(f"🗑️  删除第 {args.mend_question} 行的旧数据")
        else:
            print(f"⚠️  输出文件中没有第 {args.mend_question} 行，将新增")
        
        # 只处理指定的题目
        mend_success = False
        found_row = False
        with open(args.input, 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            for i, row in enumerate(reader, start=1):
                if i == args.mend_question:
                    found_row = True
                    if not row:
                        print(f"⚠️  输入文件第 {i} 行为空，跳过")
                        break
                    
                    question = row[0]
                    solution = row[1] 
                    answer   = row[2] 

                    print(f"\n===============================处理第【 {i} 】题（修改模式）================================")
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
                        mend_success = True

                        print(f"================================第【 {i} 】题小结=============================")
                        print("原题：")
                        print(item.original_question)
                        print("原题答案：")
                        print(item.true_answer)
                        print("增强后题目：")
                        print(processed.augmented_question)
                        print("增强后题目答案：")
                        print(processed.augmented_true_answer)

                        # 在对应位置插入新生成的内容
                        new_row = [
                            processed.augmented_question,
                            processed.augmented_true_answer,
                        ]
                        existing_rows.insert(args.mend_question - 1, new_row)
                        print(f"✅ 已将新生成的内容插入到第 {args.mend_question} 行")

                    except Exception as e:
                        print(f"处理第 {i} 行时出错：{e}")
                        new_row = [question, solution, "ERROR", "", "", "", "", "", "", f"error_{args.method}"]
                        existing_rows.insert(args.mend_question - 1, new_row)
                        mend_success = False
                    break
        
        if not found_row:
            print(f"⚠️  输入文件中未找到第 {args.mend_question} 行")
        
        # 更新统计信息
        total_count = 1 if found_row else 0
        success_count = 1 if (found_row and mend_success) else 0
        
        # 重新写入整个文件
        with open(output_path, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            for row in existing_rows:
                writer.writerow(row)
        print(f"💾 已保存修改后的文件到：{output_path}")
        
    else:
        # 如果指定了start，使用追加模式；否则使用写入模式（覆盖）
        file_mode = 'a' if args.start else 'w'
        
        with open(args.input, 'r', encoding='utf-8') as infile, \
                open(output_path, file_mode, newline='', encoding='utf-8') as outfile:

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

                    print(f"================================第【 {total_count} 】题小结=============================")
                    print("原题：")
                    print(item.original_question)
                    print("原题答案：")
                    print(item.true_answer)
                    print("增强后题目：")
                    print(processed.augmented_question)
                    print("增强后题目答案：")
                    print(processed.augmented_true_answer)

                    writer.writerow([
                        processed.augmented_question,
                        processed.augmented_true_answer,
                        # processed.original_question,
                        # processed.true_answer,
                    ])

                except Exception as e:
                    print(f"处理第 {total_count} 行时出错：{e}")
                    writer.writerow([question, solution, "ERROR", "", "", "", "", "", "", f"error_{args.method}"])

    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / total_count if total_count > 0 else 0

    print(f"从{args.input}中读取原始题目，经过{METHOD_DESCRIPTION[args.method]}增强方法处理，输出已保存在：{output_path}")
    print(f"总共 {total_count} 行，成功转换 {success_count} 行，平均每行耗时 {avg_time:.2f} 秒")

def add_textbook_knowledge_base(args):        
    print(f"\n===============================开始添加PDF文件到课本知识库===============================")
    print(f"PDF文件路径：{args.add_textbook_knowledge_base}")
    llm_generate_knowledge_base = LLMClient(model_name=DEFAULT_STAGE_MODEL["textbook_knowledge_base_construction"], temperature=args.temperature)
    novel_generator = NovelProblemGenerator(llm_generate_knowledge_base)
    result = novel_generator.build_knowledge_base_from_pdf(pdf_path=args.add_textbook_knowledge_base, merge=True)
    
    # 检查结果：如果返回的字典为空或只有metadata，说明失败
    kb_keys = [k for k in result.keys() if k != "_metadata"]
    if result and kb_keys:
        print(f"成功将PDF文件添加到知识库：{args.add_textbook_knowledge_base}")
        print("知识库添加完成！")
        exit(0)
    else:
        print(f"失败：无法将PDF文件添加到知识库：{args.add_textbook_knowledge_base}")
        print("知识库添加失败！")
        exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A-MES：题目增强框架（7 种方法）")
    parser.add_argument('--input', default="./csv_auto_augment2/filling_english_with_solutions.csv", help="输入 CSV 文件名")
    parser.add_argument('--out_csv', default="./csv_auto_augment2", help="输出 CSV 文件所在文件夹")
    parser.add_argument('--temperature', type=float, default=0.2, help="API 回答多样性，默认 0.2")
    parser.add_argument('--model', type=str, default="deepseek", help="已忽略：模型选择请直接修改代码中的 DEFAULT_STAGE_MODEL / DEFAULT_ROLE_MODEL")
    parser.add_argument('--question_id', type=int, default=None, help="题目ID")
    parser.add_argument('--mend_question', type=int, default=None, help="修改题目")
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
    parser.add_argument('--add_textbook_knowledge_base', type=str, default=None, help="添加PDF文件到知识库，指定PDF文件路径（例如：--add_textbook_knowledge_base xxx.pdf）")
    args = parser.parse_args()

    # 如果指定了--add_knowledge_base，只执行知识库添加操作，不执行题目生成
    if args.add_textbook_knowledge_base:
        add_textbook_knowledge_base(args)
        exit(0)

    if args.method not in {"1", "2", "3", "4", "5", "6", "7"}:
        raise ValueError("method 必须是 1~7 之一")
    else:
        print(f"使用增强方法：{METHOD_DESCRIPTION[args.method]}")

    run_ames_on_csv(args)