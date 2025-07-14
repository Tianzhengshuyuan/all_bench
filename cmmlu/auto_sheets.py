import re
import gspread
import argparse
from oauth2client.service_account import ServiceAccountCredentials

def get_matching_rows(sheet, dataset_name):
    """返回A列中等于dataset_name的所有行号（行号从1开始）"""
    a_col = sheet.col_values(1)
    rows = [idx+1 for idx, val in enumerate(a_col) if val.strip() == dataset_name]
    return rows

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="批量写入Google Sheet成绩")
    parser.add_argument('--log', type=str, default='log/test_origin_kimi.log', help='log文件路径')
    parser.add_argument('--sheet', type=str, required=True, help='Google Sheet名称')
    parser.add_argument('--row', type=int, default=1, help='每个数据集写入第几个匹配行（1为第一个，2为第二个...）')
    parser.add_argument('--json', type=str, default='civil-lightning-465817-b8-16bb9cce2866.json', help='Google API密钥json文件路径')
    args = parser.parse_args()

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
    sheet = spreadsheet.sheet1

    # 3. 对每个数据集自动查找A列匹配行，并写入
    for dataset_name, result_data in results.items():
        rows = get_matching_rows(sheet, dataset_name)
        if not rows:
            print(f"A列没有找到 {dataset_name}")
            continue
        if args.row < 1 or args.row > len(rows):
            print(f"{dataset_name} 在A列一共出现 {len(rows)} 次，但你指定的是第 {args.row} 个，已跳过！")
            continue
        match_row = rows[args.row - 1]
        # 写入C、D、E列（3、4、5）
        sheet.update_cell(match_row, 3, result_data['correct'])
        sheet.update_cell(match_row, 4, result_data['total'])
        sheet.update_cell(match_row, 5, result_data['cost'])
        print(f"{dataset_name} 已写入第{match_row}行")

    print("全部写入完成！")