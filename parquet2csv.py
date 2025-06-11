import pandas as pd
import argparse
import os

def convert(input_file, output_file):
    # 读取parquet并保存为csv
    df = pd.read_parquet(input_file)
    df.to_csv(output_file, index=False)
    print(f"Converted '{input_file}' to '{output_file}' successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a Parquet file to CSV with the same filename.")
    parser.add_argument("--filename", help="The name of the Parquet file to convert (e.g. data.parquet)")
    args = parser.parse_args()

    input_file = args.filename + '.parquet'

    # 检查文件是否存在
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' does not exist.")
        sys.exit(1)

    # 生成输出文件名
    output_file = args.filename + '.csv'  # 去掉.parquet，加上.csv
    convert(input_file, output_file)