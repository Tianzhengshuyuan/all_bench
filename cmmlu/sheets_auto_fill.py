import re
import gspread
import argparse
import time
from oauth2client.service_account import ServiceAccountCredentials
from gspread.utils import rowcol_to_a1

def get_matching_rows(a_col, dataset_name):
    """直接用缓存的A列列表查找行号。如果没找到，去掉常见语言后缀再试。"""
    # 先尝试直接查找
    rows = [idx+1 for idx, val in enumerate(a_col) if val.strip() == dataset_name]
    if rows:
        return rows

    # 定义可能的语言后缀
    lang_suffixes = ["_english", "_arabic", "_chinese", "_russian", "_japanese", "_french"]
    for suffix in lang_suffixes:
        if dataset_name.endswith(suffix):
            # 去掉后缀再查找
            base_name = dataset_name[:-len(suffix)]
            rows = [idx+1 for idx, val in enumerate(a_col) if val.strip() == base_name]
            if rows:
                return rows
    # 最终找不到就返回空
    return []

def colname_to_index(col):
    """支持 A, B, Z, AA, AB... 转为数字，也支持直接数字字符串"""
    col = str(col).strip()
    if col.isdigit():
        return int(col)
    col = col.upper()
    num = 0
    for c in col:
        if not ('A' <= c <= 'Z'):
            raise ValueError(f"列参数 {col} 非法！")
        num = num * 26 + (ord(c) - ord('A') + 1)
    return num

def write_spreadsheet():

    # 1. 解析 log 文件，提取所有统计行
    pattern = re.compile(
        r'([a-zA-Z0-9_]+)\.csv测试完毕！总题数: (\d+), 正确答案数: (\d+), 正确率: ([\d.]+)%, 耗时: ([\d.]+)秒'
    )
    results = {}  # {dataset_name: {'total':..., 'correct':..., 'cost':...}}
    with open(args.log, encoding='utf-8') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                name, total, correct, accuracy, cost = match.groups()
                results[name] = {
                    'total': int(total),
                    'correct': int(correct),
                    'cost': float(cost)
                }

    # 2. 连接Google Sheet
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(args.json, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open(args.sheet)
    sheet = spreadsheet.worksheet(args.worksheet)
    
    # 只调用一次API，缓存A列内容
    a_col = sheet.col_values(1)
    
    # 解析列号
    col_index = colname_to_index(args.col)

    # 3. 对每个数据集自动查找A列匹配行，并写入
    for dataset_name, result_data in results.items():
        rows = get_matching_rows(a_col, dataset_name)
        
        if not rows:
            print(f"A列没有找到 {dataset_name}")
            continue

        match_row = rows[0] + args.row - 1 
        # 写入C、D、E列（3、4、5）
        # sheet.update_cell(match_row, col_index, result_data['correct'])
        # sheet.update_cell(match_row, col_index+1, result_data['total'])
        # sheet.update_cell(match_row, col_index+2, result_data['cost'])
        # 得到区域名
        range_name = f"{rowcol_to_a1(match_row, col_index)}:{rowcol_to_a1(match_row, col_index + 2)}"
        # 或手工拼写： range_name = f"C{match_row}:E{match_row}"

        values = [[result_data['correct'], result_data['total'], result_data['cost']]]

        sheet.update(range_name=range_name, values=values)
        
        print(f"{dataset_name} 已写入第{match_row}行，从{args.col}列开始")
        time.sleep(args.sleep)    # 每次写入后休眠，降低QPS

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="批量写入Google Sheet成绩")
    parser.add_argument('--log', type=str, default='log/test_origin_kimi.log', help='log文件路径')
    parser.add_argument('--json', type=str, default='civil-lightning-465817-b8-16bb9cce2866.json', help='Google API密钥json文件路径')
    parser.add_argument('--sheet', type=str, default='大模型评估', help='Google Sheet名称')
    parser.add_argument('--worksheet', type=str, default='田郑书媛-CMMLU', help='需要操作的工作表名称')
    parser.add_argument('--row', type=int, default=1, help='每个数据集写入第几个匹配行（1为第一个，2为第二个...）')
    parser.add_argument('--col', type=str, default='C', help='要写入的起始列，比如C或3，AA等')
    parser.add_argument('--sleep', type=float, default=1.0, help='每次写入后的sleep秒数，防止QPS超限')
    args = parser.parse_args()
    
    write_spreadsheet()
    print("全部写入完成！")
