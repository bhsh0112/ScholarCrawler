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
from typing import List, Dict, Optional
import os
import json

try:
    from scholarly import scholarly, ProxyGenerator
except ImportError:
    print("请先安装 scholarly 库: pip install scholarly")
    exit(1)

try:
    from config import AdvancedSearchConfig
except ImportError:
    # 如果无法导入，定义一个简单版本
    AdvancedSearchConfig = None


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
    
    def search_papers(self, keyword: str, max_results: int = 50, 
                     advanced_config: Optional['AdvancedSearchConfig'] = None) -> List[Dict]:
        """
        搜索文献（支持高级检索）
        
        Args:
            keyword: 搜索关键字
            max_results: 最大结果数量
            advanced_config: 高级检索配置（可选）
            
        Returns:
            文献列表
        """
        # 构建查询字符串
        if advanced_config:
            search_keyword = advanced_config.to_query_string(keyword)
            print(f"\n🔍 高级搜索模式")
            print(f"📝 基础关键字: '{keyword}'")
            print(f"🔎 构建的查询: '{search_keyword}'")
            print(advanced_config)
        else:
            search_keyword = keyword
            print(f"\n🔍 正在搜索关键字: '{keyword}'")
        
        print(f"📊 目标获取数量: {max_results}")
        
        papers = []
        filtered_count = 0
        
        try:
            search_query = scholarly.search_pubs(search_keyword)
            
            for i, paper in enumerate(search_query):
                # 如果已经获取足够的符合条件的文献，则停止
                if len(papers) >= max_results:
                    break
                
                # 防止无限循环（搜索的总数不超过max_results的3倍）
                if i >= max_results * 3:
                    print(f"⚠ 已搜索 {i} 篇，但只找到 {len(papers)} 篇符合条件的文献")
                    break
                
                try:
                    # 提取论文信息
                    paper_info = self._extract_paper_info(paper)
                    
                    # 应用高级筛选
                    if advanced_config and not advanced_config.matches_filters(paper_info):
                        filtered_count += 1
                        continue
                    
                    papers.append(paper_info)
                    
                    # 显示进度
                    if len(papers) % 10 == 0:
                        print(f"  已获取 {len(papers)} 篇文献（已筛掉 {filtered_count} 篇）...")
                    
                    # 添加延迟以避免被封
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"  ⚠ 处理第 {i + 1} 篇文献时出错: {e}")
                    continue
            
            print(f"✓ 成功获取 {len(papers)} 篇文献", end='')
            if filtered_count > 0:
                print(f"（筛选掉 {filtered_count} 篇不符合条件的文献）")
            else:
                print()
            print()
            
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
        description='Google Scholar 文献爬取工具 - 支持高级检索',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  基础搜索:
    python scholar_crawler.py "deep learning"
    python scholar_crawler.py "machine learning" --max 100 --min-citations 50
  
  高级检索:
    python scholar_crawler.py "deep learning" --year-start 2020 --year-end 2023
    python scholar_crawler.py "computer vision" --authors "Yann LeCun" --venues "CVPR,ICCV"
    python scholar_crawler.py "NLP" --publishers "ACL" --exclude "survey,review"
    python scholar_crawler.py "AI" --config advanced_search.json
        """
    )
    
    # 基础参数
    parser.add_argument('keyword', type=str, help='搜索关键字')
    parser.add_argument('--max', type=int, default=50, 
                       help='最大获取文献数量 (默认: 50)')
    parser.add_argument('--output', type=str, default=None,
                       help='输出CSV文件名 (默认: 自动生成)')
    parser.add_argument('--proxy', action='store_true',
                       help='使用代理 (推荐)')
    
    # 高级检索参数
    advanced_group = parser.add_argument_group('高级检索选项')
    advanced_group.add_argument('--authors', type=str, default=None,
                               help='作者筛选 (多个用逗号分隔，例如: "Andrew Ng,Yann LeCun")')
    advanced_group.add_argument('--year-start', type=int, default=None,
                               help='起始年份 (例如: 2020)')
    advanced_group.add_argument('--year-end', type=int, default=None,
                               help='结束年份 (例如: 2023)')
    advanced_group.add_argument('--publishers', type=str, default=None,
                               help='出版商筛选 (多个用逗号分隔，例如: "IEEE,ACM")')
    advanced_group.add_argument('--venues', type=str, default=None,
                               help='会议/期刊筛选 (多个用逗号分隔，例如: "CVPR,NeurIPS")')
    advanced_group.add_argument('--min-citations', type=int, default=0,
                               help='最小引用量 (默认: 0)')
    advanced_group.add_argument('--max-citations', type=int, default=None,
                               help='最大引用量 (默认: 不限)')
    advanced_group.add_argument('--exclude', type=str, default=None,
                               help='排除关键字 (多个用逗号分隔，例如: "survey,review")')
    advanced_group.add_argument('--additional-keywords', type=str, default=None,
                               help='额外关键字 (多个用逗号分隔)')
    advanced_group.add_argument('--keyword-mode', type=str, default='OR',
                               choices=['OR', 'AND'],
                               help='关键字组合模式 (默认: OR)')
    advanced_group.add_argument('--config', type=str, default=None,
                               help='从JSON配置文件加载高级检索配置')
    
    args = parser.parse_args()
    
    # 生成默认输出文件名
    if args.output is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_keyword = args.keyword.replace(' ', '_').replace('/', '_')
        args.output = f"results/{safe_keyword}_{timestamp}.csv"
    
    # 构建高级检索配置
    advanced_config = None
    
    # 如果指定了配置文件，从JSON加载
    if args.config:
        try:
            with open(args.config, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            if AdvancedSearchConfig:
                advanced_config = AdvancedSearchConfig()
                # 从字典加载配置
                for key, value in config_data.items():
                    if hasattr(advanced_config, key):
                        setattr(advanced_config, key, value)
                print(f"✓ 已从配置文件加载: {args.config}")
        except Exception as e:
            print(f"⚠ 加载配置文件失败: {e}")
    
    # 如果命令行提供了高级检索参数，创建或更新配置
    has_advanced_params = any([
        args.authors, args.year_start, args.year_end,
        args.publishers, args.venues, args.exclude,
        args.additional_keywords, args.min_citations > 0,
        args.max_citations
    ])
    
    if has_advanced_params:
        if not AdvancedSearchConfig:
            print("⚠ 无法使用高级检索功能，请确保 config.py 可访问")
        else:
            if not advanced_config:
                advanced_config = AdvancedSearchConfig()
            
            # 设置高级检索参数
            if args.authors:
                advanced_config.authors = [a.strip() for a in args.authors.split(',')]
            if args.year_start:
                advanced_config.year_start = args.year_start
            if args.year_end:
                advanced_config.year_end = args.year_end
            if args.publishers:
                advanced_config.publishers = [p.strip() for p in args.publishers.split(',')]
            if args.venues:
                advanced_config.venues = [v.strip() for v in args.venues.split(',')]
            if args.min_citations > 0:
                advanced_config.citations_min = args.min_citations
            if args.max_citations:
                advanced_config.citations_max = args.max_citations
            if args.exclude:
                advanced_config.exclude_keywords = [e.strip() for e in args.exclude.split(',')]
            if args.additional_keywords:
                advanced_config.additional_keywords = [k.strip() for k in args.additional_keywords.split(',')]
            advanced_config.keyword_mode = args.keyword_mode
    
    # 创建爬虫实例
    crawler = ScholarCrawler(use_proxy=args.proxy)
    
    # 搜索文献（使用高级检索配置）
    papers = crawler.search_papers(args.keyword, max_results=args.max, 
                                   advanced_config=advanced_config)
    
    if not papers:
        print("❌ 未获取到任何文献，请检查网络连接或尝试使用 --proxy 参数")
        return
    
    # 按引用量排序
    papers = crawler.sort_by_citations(papers)
    
    # 导出CSV
    crawler.export_to_csv(papers, args.output, args.keyword)


if __name__ == '__main__':
    main()

