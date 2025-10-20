#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
排序功能示例
演示各种排序方式的使用
"""

from scholar_crawler import ScholarCrawler
from config import AdvancedSearchConfig


def example_sort_by_citations():
    """示例1: 按引用量排序（默认）"""
    print("\n" + "="*60)
    print("示例1: 按引用量排序 - 查找高影响力论文")
    print("="*60)
    
    config = AdvancedSearchConfig()
    config.year_start = 2018
    config.sort_by = "citations"
    config.sort_order = "desc"
    
    crawler = ScholarCrawler(use_proxy=False)
    papers = crawler.search_papers("deep learning", max_results=10, 
                                   advanced_config=config)
    
    if papers:
        crawler.export_to_csv(papers, "results/sorted_by_citations.csv", 
                             "deep learning")
        
        print("\nTop 5 高引用论文:")
        for i, paper in enumerate(papers[:5], 1):
            print(f"{i}. [{paper['citations']}引用] {paper['title'][:80]}...")


def example_sort_by_year_newest():
    """示例2: 按年份排序（最新优先）"""
    print("\n" + "="*60)
    print("示例2: 按年份排序 - 最新文献优先")
    print("="*60)
    
    config = AdvancedSearchConfig()
    config.year_start = 2020
    config.sort_by = "year"
    config.sort_order = "desc"  # 降序：从新到旧
    
    crawler = ScholarCrawler(use_proxy=False)
    papers = crawler.search_papers("transformer", max_results=10,
                                   advanced_config=config)
    
    if papers:
        crawler.export_to_csv(papers, "results/sorted_by_year_newest.csv",
                             "transformer")
        
        print("\n最新5篇论文:")
        for i, paper in enumerate(papers[:5], 1):
            print(f"{i}. [{paper['year']}年] {paper['title'][:80]}...")


def example_sort_by_year_oldest():
    """示例3: 按年份排序（最早优先）"""
    print("\n" + "="*60)
    print("示例3: 按年份排序 - 早期经典论文")
    print("="*60)
    
    config = AdvancedSearchConfig()
    config.year_start = 2010
    config.year_end = 2015
    config.citations_min = 100
    config.sort_by = "year"
    config.sort_order = "asc"  # 升序：从旧到新
    
    crawler = ScholarCrawler(use_proxy=False)
    papers = crawler.search_papers("deep learning", max_results=10,
                                   advanced_config=config)
    
    if papers:
        crawler.export_to_csv(papers, "results/sorted_by_year_oldest.csv",
                             "deep learning")
        
        print("\n早期5篇论文:")
        for i, paper in enumerate(papers[:5], 1):
            print(f"{i}. [{paper['year']}年] {paper['title'][:80]}...")


def example_sort_by_relevance():
    """示例4: 按相关性排序"""
    print("\n" + "="*60)
    print("示例4: 按相关性排序 - 保持Google Scholar排序")
    print("="*60)
    
    config = AdvancedSearchConfig()
    config.sort_by = "relevance"
    config.sort_order = "desc"
    
    crawler = ScholarCrawler(use_proxy=False)
    papers = crawler.search_papers("attention mechanism", max_results=10,
                                   advanced_config=config)
    
    if papers:
        crawler.export_to_csv(papers, "results/sorted_by_relevance.csv",
                             "attention mechanism")
        
        print("\n按相关性排序的前5篇:")
        for i, paper in enumerate(papers[:5], 1):
            print(f"{i}. {paper['title'][:80]}...")


def example_sort_by_title():
    """示例5: 按标题排序"""
    print("\n" + "="*60)
    print("示例5: 按标题字母顺序排序")
    print("="*60)
    
    config = AdvancedSearchConfig()
    config.year_start = 2020
    config.sort_by = "title"
    config.sort_order = "asc"  # 升序：A-Z
    
    crawler = ScholarCrawler(use_proxy=False)
    papers = crawler.search_papers("neural network", max_results=10,
                                   advanced_config=config)
    
    if papers:
        crawler.export_to_csv(papers, "results/sorted_by_title.csv",
                             "neural network")
        
        print("\n按标题排序的前5篇:")
        for i, paper in enumerate(papers[:5], 1):
            print(f"{i}. {paper['title'][:80]}...")


def example_combined_strategy():
    """示例6: 组合策略 - 先筛选后排序"""
    print("\n" + "="*60)
    print("示例6: 组合策略 - 高引用文献按年份排序")
    print("="*60)
    
    config = AdvancedSearchConfig()
    config.year_start = 2018
    config.citations_min = 100
    config.venues = ["NeurIPS", "ICML", "CVPR"]
    config.sort_by = "year"       # 按年份排序
    config.sort_order = "desc"    # 最新优先
    
    crawler = ScholarCrawler(use_proxy=False)
    papers = crawler.search_papers("computer vision", max_results=15,
                                   advanced_config=config)
    
    if papers:
        crawler.export_to_csv(papers, "results/combined_strategy.csv",
                             "computer vision")
        
        print("\n结果统计:")
        print(f"总文献数: {len(papers)}")
        if papers:
            print(f"年份范围: {papers[-1]['year']} - {papers[0]['year']}")
            print(f"引用量范围: {min(p['citations'] for p in papers)} - {max(p['citations'] for p in papers)}")


def example_load_from_config():
    """示例7: 从配置文件加载排序设置"""
    print("\n" + "="*60)
    print("示例7: 从配置文件加载排序设置")
    print("="*60)
    
    from config_manager import ConfigManager
    
    manager = ConfigManager()
    
    try:
        # 使用预设的按年份排序配置
        config = manager.load_config("configs/sort_by_year_newest.json")
        print(f"✓ 已加载配置")
        print(config)
        
        crawler = ScholarCrawler(use_proxy=False)
        papers = crawler.search_papers("machine learning", max_results=10,
                                       advanced_config=config)
        
        if papers:
            crawler.export_to_csv(papers, "results/from_config_sorted.csv",
                                 "machine learning")
    
    except FileNotFoundError:
        print("⚠ 配置文件不存在，请先创建")


def main():
    """主菜单"""
    print("""
╔══════════════════════════════════════════════════════════╗
║            排序功能示例 📊                               ║
╚══════════════════════════════════════════════════════════╝

选择要运行的示例:

  1. 按引用量排序 (高→低)
  2. 按年份排序 (新→旧)
  3. 按年份排序 (旧→新)
  4. 按相关性排序
  5. 按标题排序
  6. 组合策略（筛选+排序）
  7. 从配置文件加载

  0. 运行所有示例
  99. 退出

""")
    
    choice = input("请选择 (0-7, 99): ").strip()
    
    examples = {
        '1': example_sort_by_citations,
        '2': example_sort_by_year_newest,
        '3': example_sort_by_year_oldest,
        '4': example_sort_by_relevance,
        '5': example_sort_by_title,
        '6': example_combined_strategy,
        '7': example_load_from_config,
    }
    
    if choice == '0':
        print("\n>>> 运行所有示例...\n")
        for i, func in enumerate(examples.values(), 1):
            func()
            if i < len(examples):
                print("\n⏳ 等待5秒...")
                import time
                time.sleep(5)
    elif choice in examples:
        examples[choice]()
    elif choice == '99':
        print("再见!")
    else:
        print("❌ 无效选择")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n再见! 👋")

