import argparse
import pickle
import random
import csv
from pathlib import Path
from typing import Any, Dict, List

def compute_allowed_values(num: int = 30) -> List[List[int]]:
    """
    计算每一行允许的值（只计算一次，所有item共享）。
    从 csv_auto_augment 文件夹下的 8 个子文件夹中读取 filling_english.csv，
    如果第 i 行第一列为 "x"，则表明该行不能取该文件夹对应的数字。
    
    文件夹到数字的映射：
    - origin -> 0
    - disturb1 -> 1
    - disturb2 -> 2
    - disturb3 -> 3
    - numeric -> 4
    - condition -> 5
    - adaptation -> 6
    - concept -> 7
    
    返回: List[List[int]]，其中 allowed_values[i] 是第 i+1 行允许的值列表
    """
    
    # 定义文件夹到数字的映射
    folder_to_num = {
        "origin": 0,
        "disturb1": 1,
        "disturb2": 2,
        "disturb3": 3,
        "numeric": 4,
        "condition": 5,
        "adaptation": 6,
        "concept": 7,
    }
    
    # 所有可能的数字（0-7）
    all_values = list(range(8))
    
    # 读取每个文件夹的 CSV 文件，记录哪些行不能取哪些数字
    # forbidden[row_index] 是一个集合，包含第 row_index+1 行不能取的数字
    forbidden = [set() for _ in range(num)]
    
    base_path = Path("csv_auto_augment")
    for folder_name, num_value in folder_to_num.items():
        csv_path = base_path / folder_name / "filling_english.csv"
        
        if not csv_path.exists():
            print(f"警告: 文件 {csv_path} 不存在，跳过")
            continue
        
        try:
            with open(csv_path, "r", encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                for row_idx, row in enumerate(reader):
                    if row_idx >= num:
                        break
                    
                    # 检查第一列是否为 "x"
                    if row and len(row) > 0:
                        first_col = row[0].strip()
                        if first_col.lower() == "x":
                            forbidden[row_idx].add(num_value)
        except Exception as e:
            print(f"警告: 读取文件 {csv_path} 时出错: {e}，跳过")
    
    # 为每一行计算允许的值
    allowed_values_list: List[List[int]] = []
    for i in range(num):
        # 计算允许的值：所有值减去被禁止的值
        allowed_values = [v for v in all_values if v not in forbidden[i]]        
        allowed_values_list.append(allowed_values)
        print(f"第 {i + 1} 行允许的值: {allowed_values}，被禁止的值: {forbidden[i]}")
    
    return allowed_values_list


def build_augmentations(allowed_values_list: List[List[int]]) -> Dict[str, int]:
    """
    为每一行选择一个增强方法。
    选择逻辑：
    - 50% 概率从组1 {0, (1,2,3), 4, 5} 中选
    - 50% 概率从组2 {6, 7} 中选
    - (1,2,3) 作为一个整体，如果选中则再从其中等概率选择
    """
    aug_dict: Dict[str, int] = {}
    num = len(allowed_values_list)
    
    for i in range(1, num + 1):
        row_idx = i - 1
        allowed_values = set(allowed_values_list[row_idx])
        
        # 决定从哪个组选（50% 概率），random.random() 返回 [0.0, 1.0) 的随机浮点数
        if random.random() < 0.5:
            # 组1: {0, (1,2,3), 4, 5}
            group1_candidates = []
            
            # 0 单独作为一个选项
            if 0 in allowed_values:
                group1_candidates.append(0)
            
            # (1,2,3) 作为一个整体选项
            disturb_available = [v for v in [1, 2, 3] if v in allowed_values]
            if disturb_available:
                group1_candidates.append("disturb_group")
            
            # 4 单独作为一个选项
            if 4 in allowed_values:
                group1_candidates.append(4)
            
            # 5 单独作为一个选项
            if 5 in allowed_values:
                group1_candidates.append(5)
            
            if group1_candidates:
                selected = random.choice(group1_candidates)
                if selected == "disturb_group":
                    # 如果选中了 (1,2,3) 组，再从其中等概率选择
                    value = random.choice(disturb_available)
                else:
                    value = selected
            else:
                # 如果组1没有可用值，回退到从所有allowed_values中随机选
                value = random.choice(list(allowed_values))
        else:
            # 组2: {6, 7}
            group2_candidates = [v for v in [6, 7] if v in allowed_values]
            
            if group2_candidates:
                value = random.choice(group2_candidates)
            else:
                # 如果组2没有可用值，回退到从所有allowed_values中随机选
                value = random.choice(list(allowed_values))
        
        aug_dict[f"augmentation-{i}"] = value
    
    return aug_dict

def process_pkl(input_path: Path, output_path: Path) -> None:

    with input_path.open("rb") as f:
        data = pickle.load(f)

    # 只计算一次 allowed_values（所有item共享）
    allowed_values_list = compute_allowed_values(30)
    
    # 为每个item随机选择值
    for item in data:
        if isinstance(item, dict):
            item["augmentations"] = build_augmentations(allowed_values_list)

    with output_path.open("wb") as f:
        pickle.dump(data, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="给 pkl 文件中的每条记录增加一个层级字段 'augmentations'（内含 30 个 augmentation-*）。")
    parser.add_argument("--input", default="pkl/sample_data_v1.2.pkl", help="输入 pkl 文件路径")
    parser.add_argument("--output", default="pkl/sample_ames_v2.pkl", help="输出 pkl 文件路径")
    args = parser.parse_args()

    process_pkl(Path(args.input), Path(args.output))