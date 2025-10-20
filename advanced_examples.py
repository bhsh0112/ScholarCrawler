#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
高级检索使用示例
演示如何使用高级检索功能
"""

from scholar_crawler import ScholarCrawler
from config import AdvancedSearchConfig
from config_manager import ConfigManager
import time


def example_1_year_range():
    """示例1: 按年份范围搜索"""
    print("\n" + "="*60)
    print("示例1: 搜索2020-2023年的深度学习文献")
    print("="*60)
    
    config = AdvancedSearchConfig()
    config.year_start = 2020
    config.year_end = 2023
    config.citations_min = 30
    
    crawler = ScholarCrawler(use_proxy=False)
    papers = crawler.search_papers("deep learning", max_results=20, 
                                   advanced_config=config)
    
    if papers:
        papers = crawler.sort_by_citations(papers)
        crawler.export_to_csv(papers, "results/example1_year_range.csv", 
                             "deep learning (2020-2023)")


def example_2_top_authors():
    """示例2: 搜索特定作者的文献"""
    print("\n" + "="*60)
    print("示例2: 搜索图灵奖得主的深度学习文献")
    print("="*60)
    
    config = AdvancedSearchConfig()
    config.authors = ["Yann LeCun", "Geoffrey Hinton", "Yoshua Bengio"]
    config.citations_min = 50
    
    crawler = ScholarCrawler(use_proxy=False)
    papers = crawler.search_papers("deep learning", max_results=20,
                                   advanced_config=config)
    
    if papers:
        papers = crawler.sort_by_citations(papers)
        crawler.export_to_csv(papers, "results/example2_top_authors.csv",
                             "deep learning (顶级作者)")


def example_3_top_venues():
    """示例3: 搜索顶会文献"""
    print("\n" + "="*60)
    print("示例3: 搜索顶级AI会议的计算机视觉文献")
    print("="*60)
    
    config = AdvancedSearchConfig()
    config.venues = ["CVPR", "ICCV", "ECCV"]
    config.year_start = 2021
    config.citations_min = 40
    
    crawler = ScholarCrawler(use_proxy=False)
    papers = crawler.search_papers("computer vision", max_results=25,
                                   advanced_config=config)
    
    if papers:
        papers = crawler.sort_by_citations(papers)
        crawler.export_to_csv(papers, "results/example3_top_venues.csv",
                             "computer vision (顶会)")


def example_4_exclude_reviews():
    """示例4: 排除综述类文章"""
    print("\n" + "="*60)
    print("示例4: 搜索机器学习文献，排除综述类文章")
    print("="*60)
    
    config = AdvancedSearchConfig()
    config.exclude_keywords = ["survey", "review", "tutorial"]
    config.citations_min = 30
    config.year_start = 2020
    
    crawler = ScholarCrawler(use_proxy=False)
    papers = crawler.search_papers("machine learning", max_results=20,
                                   advanced_config=config)
    
    if papers:
        papers = crawler.sort_by_citations(papers)
        crawler.export_to_csv(papers, "results/example4_exclude_reviews.csv",
                             "machine learning (非综述)")


def example_5_high_impact():
    """示例5: 搜索突破性论文"""
    print("\n" + "="*60)
    print("示例5: 搜索高影响力的transformer相关论文（引用>=200）")
    print("="*60)
    
    config = AdvancedSearchConfig()
    config.citations_min = 200
    config.year_start = 2017
    config.additional_keywords = ["transformer", "attention"]
    config.keyword_mode = "OR"
    
    crawler = ScholarCrawler(use_proxy=False)
    papers = crawler.search_papers("neural networks", max_results=15,
                                   advanced_config=config)
    
    if papers:
        papers = crawler.sort_by_citations(papers)
        crawler.export_to_csv(papers, "results/example5_high_impact.csv",
                             "transformer (高影响)")


def example_6_load_config_file():
    """示例6: 从配置文件加载"""
    print("\n" + "="*60)
    print("示例6: 使用配置文件搜索")
    print("="*60)
    
    manager = ConfigManager()
    
    # 检查配置文件是否存在
    config_path = "configs/top_ai_conferences.json"
    try:
        config = manager.load_config(config_path)
        print(f"✓ 已加载配置文件: {config_path}")
        print(config)
        
        crawler = ScholarCrawler(use_proxy=False)
        papers = crawler.search_papers("reinforcement learning", max_results=20,
                                       advanced_config=config)
        
        if papers:
            papers = crawler.sort_by_citations(papers)
            crawler.export_to_csv(papers, "results/example6_config_file.csv",
                                 "reinforcement learning (配置文件)")
    
    except FileNotFoundError:
        print(f"⚠ 配置文件不存在: {config_path}")
        print("请先创建配置文件或使用其他示例")


def example_7_comprehensive():
    """示例7: 综合高级检索"""
    print("\n" + "="*60)
    print("示例7: 综合检索 - 2021-2023年顶会高引用GAN文献")
    print("="*60)
    
    config = AdvancedSearchConfig()
    config.year_start = 2021
    config.year_end = 2023
    config.venues = ["NeurIPS", "ICML", "ICLR", "CVPR", "ICCV"]
    config.citations_min = 50
    config.additional_keywords = ["GAN", "generative"]
    config.exclude_keywords = ["survey", "review"]
    config.keyword_mode = "OR"
    
    crawler = ScholarCrawler(use_proxy=False)
    papers = crawler.search_papers("image generation", max_results=20,
                                   advanced_config=config)
    
    if papers:
        papers = crawler.sort_by_citations(papers)
        crawler.export_to_csv(papers, "results/example7_comprehensive.csv",
                             "image generation (综合检索)")


def example_8_publishers():
    """示例8: 按出版商筛选"""
    print("\n" + "="*60)
    print("示例8: 搜索IEEE和ACM出版的深度学习文献")
    print("="*60)
    
    config = AdvancedSearchConfig()
    config.publishers = ["IEEE", "ACM"]
    config.year_start = 2020
    config.citations_min = 25
    
    crawler = ScholarCrawler(use_proxy=False)
    papers = crawler.search_papers("deep learning", max_results=20,
                                   advanced_config=config)
    
    if papers:
        papers = crawler.sort_by_citations(papers)
        crawler.export_to_csv(papers, "results/example8_publishers.csv",
                             "deep learning (IEEE/ACM)")


def example_9_citation_range():
    """示例9: 按引用量范围筛选"""
    print("\n" + "="*60)
    print("示例9: 搜索中等影响力文献（引用量50-200）")
    print("="*60)
    
    config = AdvancedSearchConfig()
    config.citations_min = 50
    config.citations_max = 200
    config.year_start = 2020
    
    crawler = ScholarCrawler(use_proxy=False)
    papers = crawler.search_papers("neural networks", max_results=20,
                                   advanced_config=config)
    
    if papers:
        papers = crawler.sort_by_citations(papers)
        crawler.export_to_csv(papers, "results/example9_citation_range.csv",
                             "neural networks (中等影响)")


def example_10_keyword_modes():
    """示例10: 关键字AND模式"""
    print("\n" + "="*60)
    print("示例10: 同时包含多个关键字（AND模式）")
    print("="*60)
    
    config = AdvancedSearchConfig()
    config.additional_keywords = ["neural", "optimization", "training"]
    config.keyword_mode = "AND"  # 必须同时包含所有关键字
    config.citations_min = 30
    
    crawler = ScholarCrawler(use_proxy=False)
    papers = crawler.search_papers("deep learning", max_results=15,
                                   advanced_config=config)
    
    if papers:
        papers = crawler.sort_by_citations(papers)
        crawler.export_to_csv(papers, "results/example10_keyword_and.csv",
                             "deep learning (AND模式)")


def run_all_examples():
    """运行所有示例"""
    examples = [
        ("示例1: 年份范围", example_1_year_range),
        ("示例2: 特定作者", example_2_top_authors),
        ("示例3: 顶会筛选", example_3_top_venues),
        ("示例4: 排除综述", example_4_exclude_reviews),
        ("示例5: 高影响力", example_5_high_impact),
        ("示例6: 配置文件", example_6_load_config_file),
        ("示例7: 综合检索", example_7_comprehensive),
        ("示例8: 出版商", example_8_publishers),
        ("示例9: 引用范围", example_9_citation_range),
        ("示例10: AND模式", example_10_keyword_modes),
    ]
    
    print("""
╔══════════════════════════════════════════════════════════╗
║        高级检索示例集 - 运行所有示例                     ║
╚══════════════════════════════════════════════════════════╝

警告：运行所有示例将需要较长时间
建议：首次使用请选择单个示例运行
""")
    
    confirm = input("确认运行所有示例？(y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消")
        return
    
    for i, (name, func) in enumerate(examples, 1):
        print(f"\n[{i}/{len(examples)}] 运行 {name}")
        print("-" * 60)
        
        try:
            func()
            
            # 在示例之间添加延迟
            if i < len(examples):
                print("\n⏳ 等待5秒后继续下一个示例...")
                time.sleep(5)
        
        except KeyboardInterrupt:
            print("\n\n⚠ 用户中断")
            break
        except Exception as e:
            print(f"❌ 示例运行失败: {e}")
            continue
    
    print("\n" + "="*60)
    print("✓ 所有示例运行完成！")
    print("📁 结果已保存到 results/ 目录")
    print("="*60)


def main():
    """主菜单"""
    print("""
╔══════════════════════════════════════════════════════════╗
║            高级检索使用示例 📚                           ║
╚══════════════════════════════════════════════════════════╝

选择要运行的示例:

  1.  示例1: 按年份范围搜索 (2020-2023)
  2.  示例2: 搜索特定作者 (图灵奖得主)
  3.  示例3: 搜索顶会文献 (CVPR/ICCV/ECCV)
  4.  示例4: 排除综述类文章
  5.  示例5: 搜索突破性论文 (引用>=200)
  6.  示例6: 从配置文件加载
  7.  示例7: 综合高级检索
  8.  示例8: 按出版商筛选 (IEEE/ACM)
  9.  示例9: 按引用量范围筛选 (50-200)
  10. 示例10: 关键字AND模式

  0.  运行所有示例
  99. 退出

""")
    
    choice = input("请选择 (0-10, 99): ").strip()
    
    examples = {
        '1': example_1_year_range,
        '2': example_2_top_authors,
        '3': example_3_top_venues,
        '4': example_4_exclude_reviews,
        '5': example_5_high_impact,
        '6': example_6_load_config_file,
        '7': example_7_comprehensive,
        '8': example_8_publishers,
        '9': example_9_citation_range,
        '10': example_10_keyword_modes,
        '0': run_all_examples,
    }
    
    if choice in examples:
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

