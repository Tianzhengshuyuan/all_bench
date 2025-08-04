import re
import gspread
import argparse
import time
from oauth2client.service_account import ServiceAccountCredentials

def extract_filenames(log_path):
    """从log中提取所有文件名（去掉.csv后缀）"""
    pattern = re.compile(r'([a-zA-Z0-9_]+)\.csv测试完毕！')
    filenames = []
    with open(log_path, encoding='utf-8') as f:
        for line in f:
            m = pattern.search(line)
            if m:
                filenames.append(m.group(1))
    return filenames

def subset_names(args, sheet, filenames):
    # 每6行合并A列并填入文件名，从第4行开始
    start_row = 4
    cell_col = 1  # A列
    for idx, name in enumerate(filenames):
        merge_start = start_row + idx * 6
        merge_end = merge_start + 5  # 共6行
        # 合并单元格
        cell_range = f"A{merge_start}:A{merge_end}"
        sheet.merge_cells(cell_range)
        sheet.update_cell(merge_start, cell_col, name)
        print(f"已在A{merge_start}:A{merge_end}合并并写入：{name}")
        time.sleep(args.sleep)    # 每次写入后休眠，降低QPS

    print("子集名称全部填入！")
    
def model_names(args, sheet, filenames):
    # 每组6行分别写入模型名，从B列第4行开始
    start_row = 4
    cell_col = 2  # B列
    model_list = ['deepseek-chat', 'kimi', 'doubao', 'qwen-plus', 'qwen-2.5', 'qwen-loc']
    values = []
    for _ in filenames:
        for model in model_list:
            values.append([model])
    # 计算总行数
    end_row = start_row + len(values) - 1
    cell_range = f"B{start_row}:B{end_row}"
    sheet.update(range_name=cell_range, values=values)
    print(f"模型名称已批量写入 {cell_range}")
            
def adjust_color(args, sheet, filenames):
    start_row = 4
    group_size = 6

    # 动态获取当前表格最大列数
    max_col = sheet.col_count
    print("当前表格最大列数:", max_col)
    blue = {'red': 194/255, 'green': 212/255, 'blue': 229/255}
    white = {'red': 1, 'green': 1, 'blue': 1}

    requests = []
    for idx, _ in enumerate(filenames):
        row_start = start_row + idx * group_size - 1  # 0-based
        row_end = row_start + group_size - 1          # inclusive
        color = blue if idx % 2 == 0 else white

        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sheet.id,
                    "startRowIndex": row_start,
                    "endRowIndex": row_end + 1,
                    "startColumnIndex": 0,           # A列
                    "endColumnIndex": max_col,        # 全部列
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": color
                    }
                },
                "fields": "userEnteredFormat.backgroundColor"
            }
        })

    body = {"requests": requests}
    sheet.spreadsheet.batch_update(body)
    print("颜色调整完成！")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="批量合并并写入Google Sheet文件名")
    parser.add_argument('--log', type=str, default='log/test_origin_kimi.log', help='log文件路径')
    parser.add_argument('--json', type=str, default='civil-lightning-465817-b8-16bb9cce2866.json', help='Google API密钥json文件路径')
    parser.add_argument('--sheet', type=str, default='大模型评估', help='Google Sheet名称')
    parser.add_argument('--worksheet', type=str, default='田郑书媛-CMMLU', help='需要操作的工作表名称')
    parser.add_argument('--sleep', type=float, default=1.5, help='每次写入后的sleep秒数，防止QPS超限')
    args = parser.parse_args()
    
    # 连接Google Sheet
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(args.json, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open(args.sheet)
    sheet = spreadsheet.worksheet(args.worksheet)
    
    # 提取文件名
    filenames = extract_filenames(args.log)
    print("提取到文件名：", filenames)
    
    # subset_names(args, sheet, filenames)
    # model_names(args, sheet, filenames)
    adjust_color(args, sheet, filenames)