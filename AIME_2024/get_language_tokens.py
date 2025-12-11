import os
from volcenginesdkarkruntime import Ark

# 初始化客户端
doubao_client = Ark(api_key="196b33be-8abb-4af3-9fba-6e266b2dd942")

# 多语言问题定义：让模型在各自语言中回答
questions = {
    "中文": "请用中文简单介绍一下人工智能。",
    "英文": "Please briefly introduce artificial intelligence in English.",
    "阿拉伯语": "من فضلك قدم مقدمة موجزة عن الذكاء الاصطناعي باللغة العربية.",
    "俄语": "Пожалуйста, кратко расскажите об искусственном интеллекте на русском языке.",
    "法语": "Veuillez présenter brièvement l'intelligence artificielle en français.",
    "日语": "日本語で人工知能について簡単に紹介してください。"
}

results = []

for lang, question in questions.items():
    print(f"\n=== 正在处理：{lang} ===")
    completion = doubao_client.chat.completions.create(
        model="doubao-1-5-pro-32k-250115",
        messages=[
            {"role": "user", "content": question}
        ]
    )

    answer = completion.choices[0].message.content
    print(f"回答内容：{answer}")
    usage = completion.usage

    result = {
        "语言": lang,
        "字符数": len(answer),
        "提示token": usage.prompt_tokens,
        "回答token": usage.completion_tokens,
        "总token": usage.total_tokens,
        "字符/回答token比": round(len(answer) / usage.completion_tokens, 2) if usage.completion_tokens else 0
    }
    results.append(result)


# 打印统计表
print("\n" + "=" * 100)
print(f"{'语言':<8} {'字符数':<8} {'提示token':<10} {'回答token':<10} {'总token':<10} {'字符/回答token比':<12}")
print("-" * 100)
for r in results:
    print(f"{r['语言']:<8} {r['字符数']:<8} {r['提示token']:<10} {r['回答token']:<10} {r['总token']:<10} {r['字符/回答token比']:<12}")