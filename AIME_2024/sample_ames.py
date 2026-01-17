import argparse
import pickle
import random
import csv
from pathlib import Path
from typing import Any, Dict, List

def load_augmentation_conditions(csv_path: str) -> List[bool]:
    allow_condition_list: List[bool] = []
    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 2:
                # 不足两列时，默认允许 5
                allow_condition_list.append(True)
                continue

            second_col = row[1].strip()
            # 第二列是 'x'（大小写不敏感）⇒ 不能取 5
            if second_col == "x":
                allow_condition_list.append(False)
            else:
                allow_condition_list.append(True)

    return allow_condition_list


def build_augmentations(num: int = 30) -> Dict[str, int]:
    """
    构建一个层级结构的 augmentations 字典。
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
    # forbidden[row_index][num] = True 表示第 row_index+1 行不能取 num
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
                            # print(f"第 {row_idx + 1} 行在文件夹 {folder_name} 中标记为 x，不能取 {num_value}")
        except Exception as e:
            print(f"警告: 读取文件 {csv_path} 时出错: {e}，跳过")
    
    # 为每一行选择允许的值
    aug_dict: Dict[str, int] = {}
    for i in range(1, num + 1):
        row_idx = i - 1
        # 计算允许的值：所有值减去被禁止的值
        allowed_values = [v for v in all_values if v not in forbidden[row_idx]]
        
        if not allowed_values:
            # 如果所有值都被禁止，则默认取 0
            print(f"警告: augmentation-{i} 所有值都被禁止，默认取 0")
            value = 0
        else:
            value = random.choice(allowed_values)
            forbidden_nums = sorted(forbidden[row_idx])
            # if forbidden_nums:
            #     print(f"augmentation-{i} 不能取 {forbidden_nums}，可选 {allowed_values}，选了 {value}")
            # else:
            #     print(f"augmentation-{i} 可以取所有值 {allowed_values}，选了 {value}")
        
        aug_dict[f"augmentation-{i}"] = value
    
    return aug_dict

def process_pkl(input_path: Path, output_path: Path) -> None:

    with input_path.open("rb") as f:
        data = pickle.load(f)

    for item in data:
        if isinstance(item, dict):
            item["augmentations"] = build_augmentations(30)

    with output_path.open("wb") as f:
        pickle.dump(data, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="给 pkl 文件中的每条记录增加一个层级字段 'augmentations'（内含 30 个 augmentation-*）。")
    parser.add_argument("--input", default="pkl/sample_data_v1.2.pkl", help="输入 pkl 文件路径")
    parser.add_argument("--output", default="pkl/sample_ames_v2.pkl", help="输出 pkl 文件路径")
    args = parser.parse_args()

    process_pkl(Path(args.input), Path(args.output))