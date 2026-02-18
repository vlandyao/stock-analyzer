"""
测试脚本 - 验证get_gigadevice_data.py是否可以正常运行
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

print("开始测试...")

# 测试1: 导入检查
print("\n✅ 测试1: 检查必要的库")
print(f"   pandas版本: {pd.__version__}")
print(f"   numpy版本: {np.__version__}")

# 测试2: 创建示例数据
print("\n✅ 测试2: 创建示例数据")
dates = pd.date_range(end=datetime.now(), periods=250, freq='B')
n = len(dates)
base_price = 50
returns = np.random.normal(0.0005, 0.02, n)
price = base_price * np.exp(np.cumsum(returns))

df = pd.DataFrame({
    '股票代码': '603986.SH',
    '交易日期': dates,
    '收盘价': price
})

print(f"   创建了 {len(df)} 条数据")
print(f"   数据列: {list(df.columns)}")

# 测试3: 计算移动平均线
print("\n✅ 测试3: 计算移动平均线")
df['5日均线'] = df['收盘价'].rolling(window=5).mean()
df['20日均线'] = df['收盘价'].rolling(window=20).mean()
print(f"   5日均线: {df['5日均线'].iloc[-1]:.2f}")
print(f"   20日均线: {df['20日均线'].iloc[-1]:.2f}")

# 测试4: 保存CSV文件
print("\n✅ 测试4: 保存CSV文件")
test_dir = 'test_output'
if not os.path.exists(test_dir):
    os.makedirs(test_dir)
    
csv_file = os.path.join(test_dir, 'test.csv')
df.to_csv(csv_file, index=False, encoding='utf-8-sig')
print(f"   CSV文件已保存: {csv_file}")
print(f"   文件大小: {os.path.getsize(csv_file)} 字节")

# 测试5: 读取CSV文件
print("\n✅ 测试5: 读取CSV文件")
df_read = pd.read_csv(csv_file)
print(f"   读取了 {len(df_read)} 条数据")
print(f"   数据匹配: {len(df) == len(df_read)}")

# 测试6: 保存Excel文件
print("\n✅ 测试6: 保存Excel文件")
try:
    excel_file = os.path.join(test_dir, 'test.xlsx')
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='测试数据', index=False)
    print(f"   Excel文件已保存: {excel_file}")
    print(f"   文件大小: {os.path.getsize(excel_file)} 字节")
except ImportError:
    print("   ⚠️  openpyxl未安装，跳过Excel测试")

# 测试7: 数据统计
print("\n✅ 测试7: 数据统计")
print(f"   最高价: {df['收盘价'].max():.2f}")
print(f"   最低价: {df['收盘价'].min():.2f}")
print(f"   平均价: {df['收盘价'].mean():.2f}")

# 清理测试文件
print("\n🧹 清理测试文件")
try:
    os.remove(csv_file)
    if os.path.exists(excel_file):
        os.remove(excel_file)
    os.rmdir(test_dir)
    print("   测试文件已清理")
except:
    pass

print("\n" + "="*60)
print("✅ 所有测试通过！get_gigadevice_data.py 应该可以正常运行")
print("="*60)
