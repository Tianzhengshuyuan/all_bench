import argparse
import os
import pandas as pd

def sample_csv(input_file, output_file, n=10):
    """从一个 CSV 文件中随机抽取 n 行，保存到新的文件"""
    try:
        df = pd.read_csv(input_file, header=None)
        if len(df) < n:
            sampled = df.sample(len(df))  # 如果行数不足 n，就全取
        else:
            sampled = df.sample(n)
        sampled.to_csv(output_file, index=False, header=False)
        print(f"✅ 已保存: {output_file}")
    except Exception as e:
        print(f"❌ 处理文件 {input_file} 时出错: {e}")

def get_subset():
    # 确保输出文件夹存在
    os.makedirs(args.output_dir, exist_ok=True)

    # 遍历输入文件夹中的所有 CSV 文件
    for filename in os.listdir(args.input_dir):
        if filename.lower().endswith(".csv"):
            input_file = os.path.join(args.input_dir, filename)
            output_file = os.path.join(args.output_dir, filename)
            sample_csv(input_file, output_file, n=10)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从文件夹中读取 CSV 并随机抽取 10 行保存到新文件夹")
    parser.add_argument("--input_dir", help="输入文件夹路径，包含 CSV 文件")
    parser.add_argument("--output_dir", help="输出文件夹路径，用于保存抽样后的 CSV 文件")
    args = parser.parse_args()
    get_subset()