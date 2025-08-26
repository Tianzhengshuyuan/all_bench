import pickle
import argparse
def show_pkl():    
    with open(args.pkl_path, 'rb') as f:
        data = pickle.load(f)
    # print("PKL内容如下：")
    # print(data)
    print(f"第{args.number}项内容：")
    if 0 <= args.number < len(data):
        print(data[args.number])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="显示PKL文件内容")
    parser.add_argument("--pkl_path", type=str, help="PKL文件路径")
    parser.add_argument("--number", type=int, help="显示第几项")
    args = parser.parse_args()
    show_pkl()