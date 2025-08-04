import gspread
import argparse
import time
from oauth2client.service_account import ServiceAccountCredentials

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

def do_sum():
    # 1. 连接Google Sheet
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(args.json, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open(args.sheet)
    sheet = spreadsheet.worksheet(args.worksheet)
    
    # 2. 列号和起始行号
    col_index = colname_to_index(args.col)
    start_row = args.row + 3
    # 结果要写入的行
    target_row = args.row + 405

    # 3. 批量读取该列1~target_row行
    col_values = sheet.col_values(col_index)
    # col_values: 下标0是第1行, 1是第2行...
    total = 0.0
    rows_used = []
    for row in range(start_row, 406, 6):
        idx = row - 1
        if idx < len(col_values):
            try:
                val = float(col_values[idx])
                total += val
                # print(f"第{row}行的值: {val}")
                rows_used.append((row, val))
            except Exception:
                pass  # 非数字直接跳过

    # 4. 写入结果
    cell_label = f"{args.col.upper()}{target_row}"
    sheet.update_acell(cell_label, total)
    print(f"已将 {args.col} 列第{start_row}、{start_row+6}...行的和 {total} 写入到 {cell_label}")
    print("参与求和的行：", [x[0] for x in rows_used])
    time.sleep(args.sleep)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="统计Google Sheet某列多行求和并写回")
    parser.add_argument('--json', type=str, default='civil-lightning-465817-b8-16bb9cce2866.json', help='Google API密钥json文件路径')
    parser.add_argument('--sheet', type=str, default='大模型评估', help='Google Sheet名称')
    parser.add_argument('--worksheet', type=str, default='田郑书媛-CMMLU', help='需要操作的工作表名称')
    parser.add_argument('--row', type=int, default=1, help='起始行号')
    parser.add_argument('--col', type=str, default='F', help='操作的列，比如F或AA')
    parser.add_argument('--sleep', type=float, default=1.0, help='每次操作后的sleep秒数')
    args = parser.parse_args()
    do_sum()