#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
招投标信息爬虫
目标网站：https://www.yfbzb.com/
功能：抓取招标标题、招标公司、预算金额、截止日期、项目详情链接
技术：使用requests和BeautifulSoup
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import logging
from urllib.parse import urljoin

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tender_spider.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TenderSpider:
    """招投标信息爬虫类"""
    
    def __init__(self):
        """初始化爬虫"""
        self.base_url = "https://www.yfbzb.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def get_page(self, url):
        """
        获取页面内容
        参数: url - 页面URL
        返回: 页面HTML内容
        """
        try:
            # 随机延迟，避免被封
            delay = random.uniform(1, 3)
            logger.info(f"等待 {delay:.2f} 秒后请求页面")
            time.sleep(delay)
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()  # 检查响应状态
            response.encoding = response.apparent_encoding  # 自动检测编码
            logger.info(f"成功获取页面: {url}")
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"获取页面失败: {url}, 错误: {str(e)}")
            return None
    
    def parse_list_page(self, html):
        """
        解析列表页面，提取招标信息
        参数: html - 页面HTML内容
        返回: 招标信息列表
        """
        if not html:
            return []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            tender_list = []
            
            # 分析页面结构，找到招标信息列表
            # 注意：网站结构可能会变化，需要根据实际情况调整选择器
            tender_items = soup.find_all('div', class_=['tender-item', 'list-item'])
            
            if not tender_items:
                # 尝试其他可能的选择器
                tender_items = soup.find_all('li', class_=['tender', 'item'])
            
            if not tender_items:
                # 尝试查找包含招标信息的其他元素
                tender_items = soup.find_all('div', class_=lambda x: x and ('tender' in x or 'item' in x))
            
            logger.info(f"找到 {len(tender_items)} 个招标项目")
            
            for item in tender_items:
                try:
                    # 提取标题
                    title_elem = item.find(['h3', 'h4', 'a'], class_=lambda x: x and ('title' in x or 'name' in x))
                    title = title_elem.get_text(strip=True) if title_elem else ""
                    
                    # 提取详情链接
                    link_elem = item.find('a', href=True)
                    if link_elem:
                        link = urljoin(self.base_url, link_elem['href'])
                    else:
                        link = ""
                    
                    # 提取招标公司
                    company_elem = item.find(['div', 'span'], class_=lambda x: x and ('company' in x or 'org' in x))
                    company = company_elem.get_text(strip=True) if company_elem else ""
                    
                    # 提取预算金额
                    budget_elem = item.find(['div', 'span'], class_=lambda x: x and ('budget' in x or 'amount' in x or 'price' in x))
                    budget = budget_elem.get_text(strip=True) if budget_elem else ""
                    
                    # 提取截止日期
                    deadline_elem = item.find(['div', 'span'], class_=lambda x: x and ('deadline' in x or 'end' in x or 'date' in x))
                    deadline = deadline_elem.get_text(strip=True) if deadline_elem else ""
                    
                    # 如果某些字段未找到，尝试从文本中提取
                    if not company or not budget or not deadline:
                        item_text = item.get_text(strip=True)
                        # 这里可以添加正则表达式提取逻辑
                        pass
                    
                    tender_info = {
                        '标题': title,
                        '招标公司': company,
                        '预算金额': budget,
                        '截止日期': deadline,
                        '详情链接': link
                    }
                    
                    tender_list.append(tender_info)
                    logger.info(f"提取招标信息: {title}")
                    
                except Exception as e:
                    logger.error(f"解析单个招标项目失败: {str(e)}")
                    continue
            
            return tender_list
            
        except Exception as e:
            logger.error(f"解析列表页面失败: {str(e)}")
            return []
    
    def save_to_csv(self, tender_list, filename='tender_info.csv'):
        """
        将招标信息保存到CSV文件
        参数: 
            tender_list - 招标信息列表
            filename - 保存文件名
        """
        if not tender_list:
            logger.warning("没有招标信息可保存")
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ['标题', '招标公司', '预算金额', '截止日期', '详情链接']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for tender in tender_list:
                    writer.writerow(tender)
            
            logger.info(f"成功保存 {len(tender_list)} 条招标信息到 {filename}")
        except Exception as e:
            logger.error(f"保存CSV文件失败: {str(e)}")
    
    def crawl(self, start_page=1, end_page=5):
        """
        执行爬虫，抓取多页数据
        参数: 
            start_page - 起始页码
            end_page - 结束页码
        """
        all_tender_list = []
        
        for page in range(start_page, end_page + 1):
            logger.info(f"开始抓取第 {page} 页")
            
            # 构建分页URL
            if page == 1:
                page_url = self.base_url
            else:
                page_url = f"{self.base_url}/list-{page}.html"  # 假设分页URL格式
            
            # 获取页面
            html = self.get_page(page_url)
            if not html:
                logger.warning(f"跳过第 {page} 页")
                continue
            
            # 解析页面
            tender_list = self.parse_list_page(html)
            all_tender_list.extend(tender_list)
            
            # 显示进度
            progress = (page - start_page + 1) / (end_page - start_page + 1) * 100
            logger.info(f"进度: {progress:.1f}%, 已抓取: {len(all_tender_list)} 条")
            
            # 每抓取一页后随机延迟
            time.sleep(random.uniform(2, 4))
        
        # 保存数据
        if all_tender_list:
            self.save_to_csv(all_tender_list)
        else:
            logger.warning("未抓取到任何招标信息")
        
        return all_tender_list

def main():
    """主函数"""
    logger.info("开始执行招投标信息爬虫")
    
    spider = TenderSpider()
    
    # 抓取前5页数据
    tender_list = spider.crawl(start_page=1, end_page=5)
    
    logger.info(f"爬虫执行完成，共抓取 {len(tender_list)} 条招标信息")

if __name__ == "__main__":
    main()
