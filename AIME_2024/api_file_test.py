from pathlib import Path
from openai import OpenAI

# 初始化客户端
client = OpenAI(
    api_key="sk-ODuizMlUC22phanBhvYz6dBjx2yrz7vhKhcjKnoIrYssThQo",
    base_url="https://api.moonshot.cn/v1",
)

def main():
    # 1. 上传文件并提取内容（只做一次）
    pdf_path = Path("phy2.pdf")
    if not pdf_path.exists():
        print(f"文件 {pdf_path} 不存在，请确认路径。")
        return

    print("正在上传并解析 phy2.pdf，请稍候...")
    file_object = client.files.create(
        file=pdf_path,
        purpose="file-extract"
    )

    # 获取解析后的文本内容
    file_content = client.files.content(file_id=file_object.id).text
    print("解析完成，可以开始提问了。\n")

    # 固定的角色设定 system 消息
    system_prompt = (
        "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。"
        "你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，"
        "种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"
    )

    print("输入你的问题（输入 exit / quit / q 退出）：")
    while True:
        user_input = input("你：").strip()

        # 退出条件
        if user_input.lower() in ["exit", "quit", "q"]:
            print("已退出对话。")
            break
        if not user_input:
            continue  # 空输入就跳过

        # 2. 每一轮单独构造 messages，只包含 system + pdf 内容 + 当前用户问题
        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "system",
                "content": file_content,
            },
            {
                "role": "user",
                "content": user_input,
            },
        ]

        # 3. 调用 chat.completions
        try:
            completion = client.chat.completions.create(
                model="kimi-k2-turbo-preview",
                messages=messages,
                temperature=0.6,
            )
        except Exception as e:
            print(f"调用接口出错：{e}")
            continue

        # 4. 输出回答（不再把对话加入历史）
        assistant_msg = completion.choices[0].message
        answer = assistant_msg.content
        print("Kimi：", answer, "\n")


if __name__ == "__main__":
    main()