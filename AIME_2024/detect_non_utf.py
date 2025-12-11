import sys
import os
import chardet

def detect_encoding(file_path, sample_size=4096):
    """ 检测文件整体编码（仅供参考） """
    with open(file_path, "rb") as f:
        raw = f.read(sample_size)
    result = chardet.detect(raw)
    print(f"\n[INFO] 检测到 {file_path} 可能使用编码: {result.get('encoding')} (置信度: {result.get('confidence')})")
    return result

def check_utf8_issues(file_path):
    """ 一行行检查 UTF-8 解码错误，并报告位置 """
    if not os.path.exists(file_path):
        print(f"[ERROR] 文件不存在: {file_path}")
        return

    print(f"\n[CHECK] 正在检查文件：{file_path}\n")

    error_found = False
    with open(file_path, "rb") as f:
        for i, raw_line in enumerate(f, start=1):
            try:
                raw_line.decode("utf-8")
            except UnicodeDecodeError as e:
                error_found = True
                bad_bytes = raw_line[e.start:e.end]
                hex_repr = " ".join(f"0x{b:02x}" for b in bad_bytes)
                print(f"[ERROR] 第 {i} 行 UTF-8 解码失败:")
                print(f"        错误字节范围: {e.start}–{e.end}")
                print(f"        有问题字节: {hex_repr}")
                # 显示该行的可视前后文（使用 repr 避免再次解码错误）
                preview = repr(raw_line[:100])
                print(f"        行预览: {preview}\n")

    if not error_found:
        print("[OK] 文件中未发现 UTF-8 解码问题 ✅")
    else:
        print("\n[REPORT] 已检测到以上非 UTF-8 内容。可尝试用 'gbk' 或 'latin1' 打开。")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python check_log_encoding.py <filename>")
        sys.exit(1)

    file_path = sys.argv[1]
    detect_encoding(file_path)
    check_utf8_issues(file_path)