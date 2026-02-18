import pandas as pd
import tkinter as tk
from tkinter import filedialog
import warnings
import os

warnings.filterwarnings('ignore')
os.environ['PYDEVD_DISABLE_FILE_VALIDATION'] = '1'

def detect_encoding(file_path):
    encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'big5', 'latin1']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read(1024)
            return encoding
        except:
            continue
    return 'utf-8'

def select_csv_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="选择CSV文件",
        filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")]
    )
    root.destroy()
    return file_path

def read_csv_and_show_first_5_rows(file_path):
    if not file_path:
        print("未选择文件")
        return None
    
    try:
        encoding = detect_encoding(file_path)
        print(f"检测到文件编码: {encoding}")
        df = pd.read_csv(file_path, encoding=encoding)
        print(f"CSV文件: {file_path}")
        print(f"总行数: {len(df)}")
        print(f"总列数: {len(df.columns)}")
        print(f"\n列名: {list(df.columns)}")
        print(f"\n前5行数据:")
        print(df.head())
        return df
    except FileNotFoundError:
        print(f"错误: 文件 '{file_path}' 未找到")
        return None
    except Exception as e:
        print(f"错误: {e}")
        return None

if __name__ == "__main__":
    print("请选择CSV文件...")
    csv_file = select_csv_file()
    read_csv_and_show_first_5_rows(csv_file)
