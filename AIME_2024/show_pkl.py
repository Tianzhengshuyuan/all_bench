import pickle
import argparse

def show_pkl():    
    with open(args.pkl_path, 'rb') as f:
        data = pickle.load(f)
    
    if args.number is not None:
        # 设置了 number，只展示那一项
        print(f"第{args.number}项内容：")
        if 0 <= args.number < len(data):
            print(data[args.number])
        else:
            print(f"错误：索引 {args.number} 超出范围（共 {len(data)} 项）")
    else:
        # 没设置 number，展示全部
        print(f"PKL文件共有 {len(data)} 项，全部内容如下：")
        for i, item in enumerate(data):
            print(f"\n第 {i} 项：")
            print(item)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="显示PKL文件内容")
    parser.add_argument("--pkl_path", type=str, help="PKL文件路径")
    parser.add_argument("--number", type=int, help="显示第几项")
    args = parser.parse_args()
    show_pkl()