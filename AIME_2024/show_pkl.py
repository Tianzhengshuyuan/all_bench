import pickle
import argparse

def show_pkl():    
    with open(args.pkl_path, 'rb') as f:
        data = pickle.load(f)
    
    if args.number is not None:
        # 设置了 number，只展示那一项
        print(f"第{args.number}项内容：")
        if 0 <= args.number < len(data):
            item = data[args.number]
            # 格式化打印item，augmentations字段每个键值对单独一行
            if isinstance(item, dict):
                for key, value in item.items():
                    if key == "augmentations" and isinstance(value, dict):
                        print(f"{key}:")
                        # 按顺序打印augmentation-1到augmentation-30
                        for i in range(1, 31):
                            aug_key = f"augmentation-{i}"
                            if aug_key in value:
                                print(f"  {aug_key}: {value[aug_key]}")
                    else:
                        print(f"{key}: {value}")
            else:
                print(item)
            
            # 统计30个数字的分布
            if isinstance(item, dict) and "augmentations" in item:
                aug_dict = item["augmentations"]
                # 初始化计数器
                count_0 = 0
                count_123 = 0  # 1、2、3合起来
                count_4 = 0
                count_5 = 0
                count_6 = 0
                count_7 = 0
                
                # 遍历30个augmentation值
                for i in range(1, 31):
                    key = f"augmentation-{i}"
                    if key in aug_dict:
                        value = aug_dict[key]
                        if value == 0:
                            count_0 += 1
                        elif value in [1, 2, 3]:
                            count_123 += 1
                        elif value == 4:
                            count_4 += 1
                        elif value == 5:
                            count_5 += 1
                        elif value == 6:
                            count_6 += 1
                        elif value == 7:
                            count_7 += 1
                
                # 打印统计结果
                print(f"\n统计结果（30个数字的分布）：")
                print(f"  0: {count_0} 个")
                print(f"  123: {count_123} 个")
                print(f"  4: {count_4} 个")
                print(f"  5: {count_5} 个")
                print(f"  6: {count_6} 个")
                print(f"  7: {count_7} 个")
        else:
            print(f"错误：索引 {args.number} 超出范围（共 {len(data)} 项）")
    else:
        # 没设置 number，展示全部
        print(f"PKL文件共有 {len(data)} 项，全部内容如下：")
        
        # 初始化累加计数器
        total_count_0 = 0
        total_count_123 = 0  # 1、2、3合起来
        total_count_4 = 0
        total_count_5 = 0
        total_count_6 = 0
        total_count_7 = 0
        
        for i, item in enumerate(data):
            # print(f"\n第 {i} 项：")
            # print(item)
            
            # 累加统计每个item的augmentations
            if isinstance(item, dict) and "augmentations" in item:
                aug_dict = item["augmentations"]
                # 遍历30个augmentation值
                for j in range(1, 31):
                    key = f"augmentation-{j}"
                    if key in aug_dict:
                        value = aug_dict[key]
                        if value == 0:
                            total_count_0 += 1
                        elif value in [1, 2, 3]:
                            total_count_123 += 1
                        elif value == 4:
                            total_count_4 += 1
                        elif value == 5:
                            total_count_5 += 1
                        elif value == 6:
                            total_count_6 += 1
                        elif value == 7:
                            total_count_7 += 1
        
        # 打印累加统计结果
        total_items = len(data)
        total_augmentations = total_count_0 + total_count_123 + total_count_4 + total_count_5 + total_count_6 + total_count_7
        print(f"\n\n累加统计结果（共 {total_items} 项，{total_augmentations} 个数字的分布）：")
        print(f"  0: {total_count_0} 个， 占比 {total_count_0/total_augmentations}")
        print(f"  123: {total_count_123} 个， 占比 {total_count_123/total_augmentations}")
        print(f"  4: {total_count_4} 个， 占比 {total_count_4/total_augmentations}")
        print(f"  5: {total_count_5} 个， 占比 {total_count_5/total_augmentations}")
        print(f"  6: {total_count_6} 个， 占比 {total_count_6/total_augmentations}")
        print(f"  7: {total_count_7} 个， 占比 {total_count_7/total_augmentations}")
        print(f"  012345: {total_count_0+total_count_123+total_count_4+total_count_5}, 占比 {(total_count_0+total_count_123+total_count_4+total_count_5)/total_augmentations}")
        print(f"  67: {total_count_6+total_count_7}, 占比 {(total_count_6+total_count_7)/total_augmentations}")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="显示PKL文件内容")
    parser.add_argument("--pkl_path", type=str, help="PKL文件路径")
    parser.add_argument("--number", type=int, help="显示第几项")
    args = parser.parse_args()
    show_pkl()