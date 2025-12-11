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
    若 csv_condition/filling_english.csv 第 i 行第二列为 "x"，
    则 augmentation-i 的取值只能在 {0,1,2,3,4,6,7} 中随机选，不允许为 5；
    否则在 {0,1,2,3,4,5,6,7} 中随机选。
    """
    # 读取条件
    conditions = load_augmentation_conditions("csv_condition/filling_english.csv")

    # 如果 CSV 行数不足 num 个，缺的部分默认允许取 5
    if len(conditions) < num:
        conditions.extend([True] * (num - len(conditions)))

    aug_dict: Dict[str, int] = {}
    for i in range(1, num + 1):
        allow_five = conditions[i - 1]

        if allow_five:
            # 可以取 0-7 任意值，0 代表原题
            value = random.randint(0, 7)
            print(f"augmentation-{i} 可以取 5，选了 {value}")
        else:
            # 不能取 5，只能在 0,1,2,3,4,6,7 中选
            allowed_values = [0, 1, 2, 3, 4, 6, 7]
            value = random.choice(allowed_values)
            print(f"augmentation-{i} 不能取 5，选了 {value}")

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
    parser.add_argument("--output", default="pkl/sample_ames.pkl", help="输出 pkl 文件路径")
    args = parser.parse_args()

    process_pkl(Path(args.input), Path(args.output))