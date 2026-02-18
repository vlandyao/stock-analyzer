"""
股票分析脚本
功能：
1. 从Tushare获取兆易创新股票的历史数据
2. 计算5日、10日、20日移动平均线
3. 当5日线上穿20日线时，标记为"买入信号"
4. 当5日线下穿20日线时，标记为"卖出信号"
5. 将结果保存到Excel文件
6. 用matplotlib绘制股价和均线图

作者：AI助手
日期：2026-02-17
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tushare as ts
from datetime import datetime, timedelta
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

class StockAnalyzer:
    """股票分析类"""
    
    def __init__(self, token):
        """
        初始化函数
        
        参数:
            token: Tushare API token
        """
        # 设置Tushare token
        ts.set_token(token)
        # 初始化Tushare API
        self.pro = ts.pro_api()
        print("✅ Tushare API 初始化成功")
    
    def get_stock_data(self, stock_code='603986.SH', years=3):
        """
        从Tushare获取股票历史数据
        
        参数:
            stock_code: 股票代码，默认为兆易创新(603986.SH)
            years: 获取数据的年数，默认为3年
            
        返回:
            DataFrame: 股票历史数据
        """
        print(f"\n📈 正在获取 {stock_code} 的历史数据...")
        
        # 计算日期范围
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=years*365)).strftime('%Y%m%d')
        
        print(f"📅 时间范围: {start_date} 至 {end_date}")
        
        try:
            # 调用Tushare API获取日线数据
            # ts_code: 股票代码
            # start_date: 开始日期
            # end_date: 结束日期
            df = self.pro.daily(ts_code=stock_code, start_date=start_date, end_date=end_date)
            
            if df.empty:
                print("❌ 未获取到数据，请检查股票代码是否正确")
                return None
            
            # 数据排序（按日期升序）
            df = df.sort_values('trade_date')
            
            # 转换日期格式
            df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d')
            
            # 重命名列，使其更直观
            df = df.rename(columns={
                'ts_code': '股票代码',
                'trade_date': '交易日期',
                'open': '开盘价',
                'high': '最高价',
                'low': '最低价',
                'close': '收盘价',
                'pre_close': '前收盘价',
                'change': '涨跌额',
                'pct_chg': '涨跌幅(%)',
                'vol': '成交量(手)',
                'amount': '成交额(千元)'
            })
            
            print(f"✅ 成功获取 {len(df)} 条记录")
            return df
            
        except Exception as e:
            print(f"❌ 获取数据时出错: {e}")
            return None
    
    def calculate_moving_averages(self, df):
        """
        计算移动平均线
        
        参数:
            df: 股票数据DataFrame
            
        返回:
            DataFrame: 包含移动平均线的股票数据
        """
        print("\n📊 正在计算移动平均线...")
        
        try:
            # 计算5日移动平均线
            # rolling(window=5) 表示以5天为窗口
            # mean() 计算窗口内的平均值
            df['MA5'] = df['收盘价'].rolling(window=5).mean()
            
            # 计算10日移动平均线
            df['MA10'] = df['收盘价'].rolling(window=10).mean()
            
            # 计算20日移动平均线
            df['MA20'] = df['收盘价'].rolling(window=20).mean()
            
            print("✅ 移动平均线计算完成")
            return df
            
        except Exception as e:
            print(f"❌ 计算移动平均线时出错: {e}")
            return df
    
    def detect_signals(self, df):
        """
        检测买卖信号
        
        参数:
            df: 包含移动平均线的股票数据
            
        返回:
            DataFrame: 包含买卖信号的股票数据
        """
        print("\n🔍 正在检测买卖信号...")
        
        try:
            # 初始化信号列
            df['信号'] = ''
            
            # 遍历数据，检测信号
            for i in range(1, len(df)):
                # 当前5日线和20日线
                current_ma5 = df['MA5'].iloc[i]
                current_ma20 = df['MA20'].iloc[i]
                
                # 前一天的5日线和20日线
                prev_ma5 = df['MA5'].iloc[i-1]
                prev_ma20 = df['MA20'].iloc[i-1]
                
                # 检测买入信号：5日线上穿20日线
                # 条件1：当前5日线 > 当前20日线
                # 条件2：前一天5日线 <= 前一天20日线
                if current_ma5 > current_ma20 and prev_ma5 <= prev_ma20:
                    df.loc[df.index[i], '信号'] = '买入信号'
                
                # 检测卖出信号：5日线下穿20日线
                # 条件1：当前5日线 < 当前20日线
                # 条件2：前一天5日线 >= 前一天20日线
                elif current_ma5 < current_ma20 and prev_ma5 >= prev_ma20:
                    df.loc[df.index[i], '信号'] = '卖出信号'
            
            # 统计信号数量
            buy_signals = (df['信号'] == '买入信号').sum()
            sell_signals = (df['信号'] == '卖出信号').sum()
            
            print(f"✅ 信号检测完成")
            print(f"📋 买入信号: {buy_signals} 个")
            print(f"📋 卖出信号: {sell_signals} 个")
            
            return df
            
        except Exception as e:
            print(f"❌ 检测信号时出错: {e}")
            return df
    
    def save_to_excel(self, df, stock_code='603986'):
        """
        将结果保存到Excel文件
        
        参数:
            df: 包含信号的股票数据
            stock_code: 股票代码，用于文件名
            
        返回:
            str: Excel文件路径
        """
        print("\n💾 正在保存数据到Excel文件...")
        
        try:
            # 创建数据目录
            data_dir = 'stock_analysis'
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
                print(f"📁 创建目录: {data_dir}")
            
            # 生成文件名
            today = datetime.now().strftime('%Y%m%d')
            filename = f"{stock_code}_analysis_{today}.xlsx"
            file_path = os.path.join(data_dir, filename)
            
            # 创建Excel写入器
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # 写入完整数据
                df.to_excel(writer, sheet_name='完整数据', index=False)
                
                # 写入只包含信号的行
                signals_df = df[df['信号'] != '']
                if not signals_df.empty:
                    signals_df.to_excel(writer, sheet_name='买卖信号', index=False)
                
            print(f"✅ Excel文件已保存: {file_path}")
            return file_path
            
        except Exception as e:
            print(f"❌ 保存Excel文件时出错: {e}")
            return None
    
    def plot_chart(self, df, stock_code='603986'):
        """
        绘制股价和均线图
        
        参数:
            df: 包含移动平均线的股票数据
            stock_code: 股票代码，用于文件名
            
        返回:
            str: 图表文件路径
        """
        print("\n📈 正在绘制股价和均线图...")
        
        try:
            # 创建图表目录
            chart_dir = 'stock_charts'
            if not os.path.exists(chart_dir):
                os.makedirs(chart_dir)
                print(f"📁 创建目录: {chart_dir}")
            
            # 创建图表
            plt.figure(figsize=(15, 8))
            
            # 绘制收盘价
            plt.plot(df['交易日期'], df['收盘价'], label='收盘价', color='blue', linewidth=2)
            
            # 绘制5日均线
            plt.plot(df['交易日期'], df['MA5'], label='5日均线', color='red', linewidth=1.5)
            
            # 绘制10日均线
            plt.plot(df['交易日期'], df['MA10'], label='10日均线', color='green', linewidth=1.5)
            
            # 绘制20日均线
            plt.plot(df['交易日期'], df['MA20'], label='20日均线', color='orange', linewidth=1.5)
            
            # 标记买入信号
            buy_signals = df[df['信号'] == '买入信号']
            if not buy_signals.empty:
                plt.scatter(buy_signals['交易日期'], buy_signals['收盘价'], 
                          marker='^', color='lime', s=100, label='买入信号')
            
            # 标记卖出信号
            sell_signals = df[df['信号'] == '卖出信号']
            if not sell_signals.empty:
                plt.scatter(sell_signals['交易日期'], sell_signals['收盘价'], 
                          marker='v', color='red', s=100, label='卖出信号')
            
            # 设置图表标题和标签
            plt.title(f'{stock_code} 股价与移动平均线分析', fontsize=16)
            plt.xlabel('日期', fontsize=12)
            plt.ylabel('价格', fontsize=12)
            
            # 添加图例
            plt.legend(loc='best', fontsize=10)
            
            # 添加网格
            plt.grid(True, linestyle='--', alpha=0.7)
            
            # 自动调整日期标签
            plt.gcf().autofmt_xdate()
            
            # 生成文件名
            today = datetime.now().strftime('%Y%m%d')
            filename = f"{stock_code}_chart_{today}.png"
            file_path = os.path.join(chart_dir, filename)
            
            # 保存图表
            plt.tight_layout()
            plt.savefig(file_path, dpi=150)
            plt.close()
            
            print(f"✅ 图表已保存: {file_path}")
            return file_path
            
        except Exception as e:
            print(f"❌ 绘制图表时出错: {e}")
            return None

def main():
    """
    主函数
    """
    print("=" * 80)
    print("📊 股票分析系统")
    print("=" * 80)
    print("功能：分析兆易创新股票数据，计算移动平均线，检测买卖信号")
    print("=" * 80)
    
    # 请替换为你的Tushare token
    # 注册地址：https://tushare.pro
    TUSHARE_TOKEN = '2d116fcacd0294c740024fee58bfdce494ad6ace4e2ec5e125b8a1f5'  # 请替换为你的实际token
    
    if TUSHARE_TOKEN == 'your_token_here':
        print("=" * 60)
        print("⚠️  请先注册Tushare获取Token：")
        print("1. 访问 https://tushare.pro")
        print("2. 注册账号（免费）")
        print("3. 在个人中心获取Token")
        print("4. 将Token替换到代码中")
        print("=" * 60)
        return
    
    # 初始化分析器
    analyzer = StockAnalyzer(TUSHARE_TOKEN)
    
    # 获取股票数据
    df = analyzer.get_stock_data('603986.SH', years=3)
    
    if df is not None:
        # 计算移动平均线
        df = analyzer.calculate_moving_averages(df)
        
        # 检测买卖信号
        df = analyzer.detect_signals(df)
        
        # 保存到Excel
        excel_path = analyzer.save_to_excel(df, '603986')
        
        # 绘制图表
        chart_path = analyzer.plot_chart(df, '603986')
        
        print("\n" + "=" * 80)
        print("✅ 股票分析完成！")
        print("=" * 80)
        if excel_path:
            print(f"📄 分析结果已保存到: {excel_path}")
        if chart_path:
            print(f"📊 图表已保存到: {chart_path}")
        print("=" * 80)
    
if __name__ == "__main__":
    main()
