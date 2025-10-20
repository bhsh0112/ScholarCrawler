#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Google Scholar 文献爬取工具
功能：根据关键字搜索文献，按引用量排序，导出CSV
"""

import csv
import time
import argparse
from datetime import datetime
from typing import List, Dict
import os

try:
    from scholarly import scholarly, ProxyGenerator
except ImportError:
    print("请先安装 scholarly 库: pip install scholarly")
    exit(1)


class ScholarCrawler:
    """Google Scholar 文献爬取器"""
    
    def __init__(self, use_proxy=False):
        """
        初始化爬取器
        
        Args:
            use_proxy: 是否使用代理（推荐使用以避免被封）
        """
        self.use_proxy = use_proxy
        if use_proxy:
            self._setup_proxy()
    
    def _setup_proxy(self):
        """设置代理"""
        try:
            pg = ProxyGenerator()
            pg.FreeProxies()
            scholarly.use_proxy(pg)
            print("✓ 代理设置成功")
        except Exception as e:
            print(f"⚠ 代理设置失败: {e}")
            print("将使用直连模式，可能会遇到访问限制")
    
    def search_papers(self, keyword: str, max_results: int = 50) -> List[Dict]:
        """
        搜索文献
        
        Args:
            keyword: 搜索关键字
            max_results: 最大结果数量
            
        Returns:
            文献列表
        """
        print(f"\n🔍 正在搜索关键字: '{keyword}'")
        print(f"📊 目标获取数量: {max_results}")
        
        papers = []
        try:
            search_query = scholarly.search_pubs(keyword)
            
            for i, paper in enumerate(search_query):
                if i >= max_results:
                    break
                
                try:
                    # 提取论文信息
                    paper_info = self._extract_paper_info(paper)
                    papers.append(paper_info)
                    
                    # 显示进度
                    if (i + 1) % 10 == 0:
                        print(f"  已获取 {i + 1} 篇文献...")
                    
                    # 添加延迟以避免被封
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"  ⚠ 处理第 {i + 1} 篇文献时出错: {e}")
                    continue
            
            print(f"✓ 成功获取 {len(papers)} 篇文献\n")
            
        except Exception as e:
            print(f"❌ 搜索失败: {e}")
        
        return papers
    
    def _extract_paper_info(self, paper) -> Dict:
        """
        提取论文信息
        
        Args:
            paper: scholarly 返回的论文对象
            
        Returns:
            论文信息字典
        """
        # 安全获取字段的辅助函数
        def safe_get(paper_dict, key, default=''):
            return paper_dict.get(key, default) if paper_dict else default
        
        bib = paper.get('bib', {})
        
        # 提取作者列表
        authors = bib.get('author', [])
        if isinstance(authors, list):
            authors_str = '; '.join(authors)
        else:
            authors_str = str(authors)
        
        # 提取引用数
        num_citations = paper.get('num_citations', 0)
        if num_citations is None:
            num_citations = 0
        
        paper_info = {
            'title': bib.get('title', 'N/A'),
            'authors': authors_str,
            'year': bib.get('pub_year', 'N/A'),
            'venue': bib.get('venue', 'N/A'),
            'publisher': bib.get('publisher', 'N/A'),
            'citations': num_citations,
            'abstract': bib.get('abstract', 'N/A'),
            'url': paper.get('pub_url', 'N/A'),
            'eprint_url': paper.get('eprint_url', 'N/A'),
        }
        
        return paper_info
    
    def sort_by_citations(self, papers: List[Dict], descending=True) -> List[Dict]:
        """
        按引用量排序
        
        Args:
            papers: 文献列表
            descending: 是否降序排列
            
        Returns:
            排序后的文献列表
        """
        return sorted(papers, key=lambda x: x['citations'], reverse=descending)
    
    def filter_by_citations(self, papers: List[Dict], min_citations: int = 0) -> List[Dict]:
        """
        按最小引用量筛选
        
        Args:
            papers: 文献列表
            min_citations: 最小引用量
            
        Returns:
            筛选后的文献列表
        """
        filtered = [p for p in papers if p['citations'] >= min_citations]
        print(f"📌 筛选引用量 >= {min_citations} 的文献: {len(filtered)} 篇")
        return filtered
    
    def export_to_csv(self, papers: List[Dict], filename: str, keyword: str):
        """
        导出为CSV文件
        
        Args:
            papers: 文献列表
            filename: 输出文件名
            keyword: 搜索关键字
        """
        if not papers:
            print("❌ 没有数据可导出")
            return
        
        # 创建输出目录
        output_dir = os.path.dirname(filename)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 写入CSV
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = ['title', 'authors', 'year', 'venue', 'publisher', 
                         'citations', 'abstract', 'url', 'eprint_url']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            for paper in papers:
                writer.writerow(paper)
        
        print(f"✓ 成功导出 {len(papers)} 篇文献到: {filename}")
        
        # 输出统计信息
        self._print_statistics(papers, keyword)
    
    def _print_statistics(self, papers: List[Dict], keyword: str):
        """打印统计信息"""
        if not papers:
            return
        
        total = len(papers)
        citations = [p['citations'] for p in papers]
        
        print("\n" + "="*60)
        print(f"📊 统计信息 - 关键字: '{keyword}'")
        print("="*60)
        print(f"总文献数: {total}")
        print(f"总引用数: {sum(citations)}")
        print(f"平均引用数: {sum(citations)/total:.1f}")
        print(f"最高引用数: {max(citations)}")
        print(f"最低引用数: {min(citations)}")
        
        # Top 5 高引用文献
        print("\n🏆 Top 5 高引用文献:")
        for i, paper in enumerate(papers[:5], 1):
            print(f"{i}. [{paper['citations']}次] {paper['title']}")
            print(f"   作者: {paper['authors'][:100]}...")
            print(f"   年份: {paper['year']}\n")
        
        print("="*60 + "\n")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Google Scholar 文献爬取工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python scholar_crawler.py "deep learning"
  python scholar_crawler.py "machine learning" --max 100 --min-citations 50
  python scholar_crawler.py "computer vision" --output results.csv --proxy
        """
    )
    
    parser.add_argument('keyword', type=str, help='搜索关键字')
    parser.add_argument('--max', type=int, default=50, 
                       help='最大获取文献数量 (默认: 50)')
    parser.add_argument('--min-citations', type=int, default=0,
                       help='最小引用量筛选 (默认: 0)')
    parser.add_argument('--output', type=str, default=None,
                       help='输出CSV文件名 (默认: 自动生成)')
    parser.add_argument('--proxy', action='store_true',
                       help='使用代理 (推荐)')
    
    args = parser.parse_args()
    
    # 生成默认输出文件名
    if args.output is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_keyword = args.keyword.replace(' ', '_').replace('/', '_')
        args.output = f"results/{safe_keyword}_{timestamp}.csv"
    
    # 创建爬虫实例
    crawler = ScholarCrawler(use_proxy=args.proxy)
    
    # 搜索文献
    papers = crawler.search_papers(args.keyword, max_results=args.max)
    
    if not papers:
        print("❌ 未获取到任何文献，请检查网络连接或尝试使用 --proxy 参数")
        return
    
    # 按引用量排序
    papers = crawler.sort_by_citations(papers)
    
    # 筛选最小引用量
    if args.min_citations > 0:
        papers = crawler.filter_by_citations(papers, args.min_citations)
    
    # 导出CSV
    crawler.export_to_csv(papers, args.output, args.keyword)


if __name__ == '__main__':
    main()

