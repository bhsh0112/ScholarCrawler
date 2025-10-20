#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
使用示例脚本
演示如何在代码中使用 ScholarCrawler
"""

from scholar_crawler import ScholarCrawler


def example_basic_search():
    """示例1: 基础搜索"""
    print("\n" + "="*60)
    print("示例1: 基础搜索 - 搜索'machine learning'")
    print("="*60)
    
    crawler = ScholarCrawler(use_proxy=False)
    papers = crawler.search_papers("machine learning", max_results=10)
    
    if papers:
        # 按引用量排序
        papers = crawler.sort_by_citations(papers)
        
        # 导出CSV
        crawler.export_to_csv(papers, "results/example1_basic.csv", "machine learning")
    

def example_with_filter():
    """示例2: 带筛选的搜索"""
    print("\n" + "="*60)
    print("示例2: 高引用文献搜索 - 搜索'deep learning'并筛选引用量>=100")
    print("="*60)
    
    crawler = ScholarCrawler(use_proxy=False)
    papers = crawler.search_papers("deep learning", max_results=30)
    
    if papers:
        # 按引用量排序
        papers = crawler.sort_by_citations(papers)
        
        # 筛选高引用文献
        papers = crawler.filter_by_citations(papers, min_citations=100)
        
        if papers:
            # 导出CSV
            crawler.export_to_csv(papers, "results/example2_filtered.csv", "deep learning")
        else:
            print("⚠ 没有符合条件的文献")


def example_with_proxy():
    """示例3: 使用代理"""
    print("\n" + "="*60)
    print("示例3: 使用代理搜索 - 搜索'computer vision'")
    print("="*60)
    
    crawler = ScholarCrawler(use_proxy=True)  # 启用代理
    papers = crawler.search_papers("computer vision", max_results=20)
    
    if papers:
        # 按引用量排序
        papers = crawler.sort_by_citations(papers)
        
        # 导出CSV
        crawler.export_to_csv(papers, "results/example3_proxy.csv", "computer vision")


def example_multiple_keywords():
    """示例4: 批量搜索多个关键字"""
    print("\n" + "="*60)
    print("示例4: 批量搜索多个关键字")
    print("="*60)
    
    keywords = [
        "neural networks",
        "reinforcement learning",
        "natural language processing"
    ]
    
    crawler = ScholarCrawler(use_proxy=False)
    
    for keyword in keywords:
        print(f"\n>>> 正在处理关键字: {keyword}")
        papers = crawler.search_papers(keyword, max_results=15)
        
        if papers:
            papers = crawler.sort_by_citations(papers)
            safe_keyword = keyword.replace(' ', '_')
            crawler.export_to_csv(
                papers, 
                f"results/example4_{safe_keyword}.csv", 
                keyword
            )
        
        # 在关键字之间添加延迟
        print("等待5秒后继续...")
        import time
        time.sleep(5)


def example_custom_analysis():
    """示例5: 自定义分析"""
    print("\n" + "="*60)
    print("示例5: 自定义分析 - 分析不同年份的文献分布")
    print("="*60)
    
    crawler = ScholarCrawler(use_proxy=False)
    papers = crawler.search_papers("artificial intelligence", max_results=50)
    
    if papers:
        # 按年份分组统计
        year_stats = {}
        for paper in papers:
            year = paper['year']
            if year != 'N/A':
                year_stats[year] = year_stats.get(year, 0) + 1
        
        print("\n📊 年份分布:")
        for year in sorted(year_stats.keys(), reverse=True):
            print(f"  {year}: {year_stats[year]} 篇")
        
        # 计算平均引用数 by year
        year_citations = {}
        for paper in papers:
            year = paper['year']
            if year != 'N/A':
                if year not in year_citations:
                    year_citations[year] = []
                year_citations[year].append(paper['citations'])
        
        print("\n📈 年份平均引用数:")
        for year in sorted(year_citations.keys(), reverse=True):
            avg = sum(year_citations[year]) / len(year_citations[year])
            print(f"  {year}: {avg:.1f} 次")
        
        # 导出结果
        papers = crawler.sort_by_citations(papers)
        crawler.export_to_csv(papers, "results/example5_analysis.csv", "artificial intelligence")


def main():
    """主函数 - 运行所有示例"""
    print("""
╔══════════════════════════════════════════════════════════╗
║       Google Scholar 文献爬取工具 - 使用示例             ║
╚══════════════════════════════════════════════════════════╝

请选择要运行的示例:
  1. 基础搜索
  2. 带筛选的搜索 (高引用文献)
  3. 使用代理搜索
  4. 批量搜索多个关键字
  5. 自定义分析
  0. 运行所有示例

输入选项 (0-5): """, end='')
    
    choice = input().strip()
    
    examples = {
        '1': example_basic_search,
        '2': example_with_filter,
        '3': example_with_proxy,
        '4': example_multiple_keywords,
        '5': example_custom_analysis,
    }
    
    if choice == '0':
        print("\n>>> 运行所有示例...")
        for func in examples.values():
            func()
            print("\n" + "-"*60)
    elif choice in examples:
        examples[choice]()
    else:
        print("❌ 无效的选项")
    
    print("\n✓ 所有示例运行完成！")
    print("📁 结果已保存到 results/ 目录")


if __name__ == '__main__':
    main()

