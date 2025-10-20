#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
快速开始脚本
交互式引导用户使用 Scholar Crawler
"""

from scholar_crawler import ScholarCrawler
import config


def quick_start():
    """快速开始向导"""
    print("""
╔══════════════════════════════════════════════════════════╗
║     欢迎使用 Google Scholar 文献爬取工具 🎓              ║
╚══════════════════════════════════════════════════════════╝
""")
    
    # 1. 选择关键字来源
    print("第一步: 选择搜索关键字来源")
    print("  1. 手动输入关键字")
    print("  2. 从预设列表选择 (AI/CV/NLP/推荐系统/数据挖掘/大数据)")
    
    choice = input("\n请选择 (1-2): ").strip()
    
    keyword = ""
    if choice == '1':
        keyword = input("\n请输入搜索关键字: ").strip()
    elif choice == '2':
        print("\n预设类别:")
        print("  1. 人工智能 (AI)")
        print("  2. 计算机视觉 (CV)")
        print("  3. 自然语言处理 (NLP)")
        print("  4. 推荐系统 (RecSys)")
        print("  5. 数据挖掘 (DM)")
        print("  6. 大数据 (BigData)")
        
        cat_choice = input("\n请选择类别 (1-6): ").strip()
        cat_map = {
            '1': 'ai', '2': 'cv', '3': 'nlp',
            '4': 'recsys', '5': 'dm', '6': 'bigdata'
        }
        
        if cat_choice in cat_map:
            keywords = config.get_keywords_by_category(cat_map[cat_choice])
            print(f"\n该类别包含以下关键字:")
            for i, kw in enumerate(keywords, 1):
                print(f"  {i}. {kw}")
            
            kw_choice = input(f"\n请选择关键字 (1-{len(keywords)}): ").strip()
            try:
                keyword = keywords[int(kw_choice) - 1]
            except:
                print("❌ 无效选择，使用第一个关键字")
                keyword = keywords[0]
    
    if not keyword:
        print("❌ 未选择关键字，退出")
        return
    
    print(f"\n✓ 已选择关键字: '{keyword}'")
    
    # 2. 设置参数
    print("\n" + "-"*60)
    print("第二步: 设置搜索参数")
    
    max_results = input(f"最大获取文献数量 (默认: {config.DEFAULT_MAX_RESULTS}): ").strip()
    max_results = int(max_results) if max_results.isdigit() else config.DEFAULT_MAX_RESULTS
    
    use_proxy = input("是否使用代理? (y/n, 默认: n): ").strip().lower() == 'y'
    
    output_file = input("输出文件名 (默认: 自动生成): ").strip()
    if not output_file:
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_keyword = keyword.replace(' ', '_').replace('/', '_')
        output_file = f"{config.OUTPUT_DIR}/{safe_keyword}_{timestamp}.csv"
    
    # 2.5 高级检索选项
    print("\n" + "-"*60)
    print("第三步: 高级检索选项（可选）")
    print("  1. 使用预设配置（推荐）")
    print("  2. 自定义高级检索")
    print("  3. 跳过（使用基础搜索）")
    
    advanced_choice = input("\n请选择 (1-3, 默认: 3): ").strip() or '3'
    
    advanced_config = None
    
    if advanced_choice == '1':
        # 使用预设配置
        print("\n预设配置:")
        print("  1. 最近高影响力文献 (2020年后, 引用>=50)")
        print("  2. 顶级AI会议 (NeurIPS, ICML, CVPR等)")
        print("  3. Nature/Science 顶级期刊")
        
        preset_choice = input("\n选择预设配置 (1-3): ").strip()
        
        if preset_choice == '1':
            advanced_config = config.create_recent_high_impact_config(2020, 50)
        elif preset_choice == '2':
            advanced_config = config.create_top_venue_config(config.TOP_AI_CONFERENCES)
        elif preset_choice == '3':
            advanced_config = config.create_top_venue_config(config.TOP_AI_JOURNALS)
        
        if advanced_config:
            print(f"\n✓ 已选择预设配置")
    
    elif advanced_choice == '2':
        # 自定义高级检索
        advanced_config = config.AdvancedSearchConfig()
        
        print("\n自定义高级检索参数（直接回车跳过）:")
        
        # 年份范围
        year_start = input("  起始年份 (如: 2020): ").strip()
        if year_start.isdigit():
            advanced_config.year_start = int(year_start)
        
        year_end = input("  结束年份 (如: 2023): ").strip()
        if year_end.isdigit():
            advanced_config.year_end = int(year_end)
        
        # 引用量
        min_cit = input("  最小引用量 (如: 50): ").strip()
        if min_cit.isdigit():
            advanced_config.citations_min = int(min_cit)
        
        max_cit = input("  最大引用量 (留空不限): ").strip()
        if max_cit.isdigit():
            advanced_config.citations_max = int(max_cit)
        
        # 作者
        authors = input("  作者 (多个用逗号分隔): ").strip()
        if authors:
            advanced_config.authors = [a.strip() for a in authors.split(',')]
        
        # 会议/期刊
        venues = input("  会议/期刊 (如: CVPR,NeurIPS): ").strip()
        if venues:
            advanced_config.venues = [v.strip() for v in venues.split(',')]
        
        # 出版商
        publishers = input("  出版商 (如: IEEE,ACM): ").strip()
        if publishers:
            advanced_config.publishers = [p.strip() for p in publishers.split(',')]
        
        # 排除词
        exclude = input("  排除关键字 (如: survey,review): ").strip()
        if exclude:
            advanced_config.exclude_keywords = [e.strip() for e in exclude.split(',')]
        
        print("\n✓ 已配置高级检索")
    
    # 3. 确认信息
    print("\n" + "="*60)
    print("搜索配置确认:")
    print("="*60)
    print(f"  关键字: {keyword}")
    print(f"  最大数量: {max_results}")
    print(f"  使用代理: {'是' if use_proxy else '否'}")
    print(f"  输出文件: {output_file}")
    
    if advanced_config:
        print("\n  高级检索:")
        print(advanced_config)
    
    print("="*60)
    
    confirm = input("\n确认开始搜索? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ 已取消")
        return
    
    # 4. 执行搜索
    print("\n" + "="*60)
    print("开始搜索...")
    print("="*60)
    
    try:
        crawler = ScholarCrawler(use_proxy=use_proxy)
        papers = crawler.search_papers(keyword, max_results=max_results, 
                                       advanced_config=advanced_config)
        
        if not papers:
            print("❌ 未获取到任何文献")
            return
        
        # 排序
        papers = crawler.sort_by_citations(papers)
        
        # 导出
        crawler.export_to_csv(papers, output_file, keyword)
        
        print("\n" + "="*60)
        print("✓ 搜索完成！")
        print("="*60)
        print(f"📁 结果已保存到: {output_file}")
        print("\n您可以使用 Excel 或其他工具打开 CSV 文件查看结果")
        
    except KeyboardInterrupt:
        print("\n\n⚠ 用户中断")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        print("请检查网络连接或尝试使用代理")


def batch_search():
    """批量搜索模式"""
    print("""
╔══════════════════════════════════════════════════════════╗
║            批量搜索模式 📚                               ║
╚══════════════════════════════════════════════════════════╝
""")
    
    print("请选择批量搜索类别:")
    print("  1. 人工智能 (6个关键字)")
    print("  2. 计算机视觉 (6个关键字)")
    print("  3. 自然语言处理 (6个关键字)")
    print("  4. 推荐系统 (5个关键字)")
    print("  5. 数据挖掘 (6个关键字)")
    print("  6. 大数据 (5个关键字)")
    print("  7. 全部 (所有预设关键字)")
    
    choice = input("\n请选择 (1-7): ").strip()
    
    cat_map = {
        '1': ('ai', config.AI_KEYWORDS),
        '2': ('cv', config.CV_KEYWORDS),
        '3': ('nlp', config.NLP_KEYWORDS),
        '4': ('recsys', config.RECSYS_KEYWORDS),
        '5': ('dm', config.DM_KEYWORDS),
        '6': ('bigdata', config.BIGDATA_KEYWORDS),
        '7': ('all', config.get_all_keywords()),
    }
    
    if choice not in cat_map:
        print("❌ 无效选择")
        return
    
    cat_name, keywords = cat_map[choice]
    
    print(f"\n将搜索以下 {len(keywords)} 个关键字:")
    for i, kw in enumerate(keywords, 1):
        print(f"  {i}. {kw}")
    
    max_results = input(f"\n每个关键字的最大文献数 (默认: 20): ").strip()
    max_results = int(max_results) if max_results.isdigit() else 20
    
    use_proxy = input("是否使用代理? (y/n, 默认: n): ").strip().lower() == 'y'
    
    confirm = input(f"\n确认批量搜索 {len(keywords)} 个关键字? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ 已取消")
        return
    
    # 执行批量搜索
    print("\n" + "="*60)
    print("开始批量搜索...")
    print("="*60)
    
    crawler = ScholarCrawler(use_proxy=use_proxy)
    
    from datetime import datetime
    import time
    
    for i, keyword in enumerate(keywords, 1):
        print(f"\n[{i}/{len(keywords)}] 搜索: {keyword}")
        print("-"*60)
        
        try:
            papers = crawler.search_papers(keyword, max_results=max_results)
            
            if papers:
                papers = crawler.sort_by_citations(papers)
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                safe_keyword = keyword.replace(' ', '_').replace('/', '_')
                output_file = f"{config.OUTPUT_DIR}/{cat_name}_{safe_keyword}_{timestamp}.csv"
                
                crawler.export_to_csv(papers, output_file, keyword)
            
            # 在关键字之间添加延迟
            if i < len(keywords):
                print("\n⏳ 等待5秒后继续...")
                time.sleep(5)
        
        except KeyboardInterrupt:
            print("\n\n⚠ 用户中断批量搜索")
            break
        except Exception as e:
            print(f"❌ 搜索 '{keyword}' 时出错: {e}")
            continue
    
    print("\n" + "="*60)
    print("✓ 批量搜索完成！")
    print("="*60)
    print(f"📁 所有结果已保存到: {config.OUTPUT_DIR}/ 目录")


def advanced_search_wizard():
    """高级检索向导"""
    print("""
╔══════════════════════════════════════════════════════════╗
║            高级检索向导 🔬                               ║
╚══════════════════════════════════════════════════════════╝
""")
    
    # 从配置文件加载
    print("使用预设配置文件或自定义？")
    print("  1. 加载预设配置文件")
    print("  2. 自定义配置（保存为文件）")
    
    choice = input("\n请选择 (1-2): ").strip()
    
    if choice == '1':
        import os
        config_dir = "configs"
        if os.path.exists(config_dir):
            import glob
            json_files = glob.glob(f"{config_dir}/*.json")
            if json_files:
                print("\n可用的配置文件:")
                for i, f in enumerate(json_files, 1):
                    print(f"  {i}. {os.path.basename(f)}")
                
                file_choice = input(f"\n选择配置文件 (1-{len(json_files)}): ").strip()
                try:
                    config_file = json_files[int(file_choice) - 1]
                    keyword = input("\n请输入搜索关键字: ").strip()
                    
                    # 调用命令行工具
                    import subprocess
                    cmd = f'python scholar_crawler.py "{keyword}" --config "{config_file}"'
                    print(f"\n执行命令: {cmd}\n")
                    subprocess.call(cmd, shell=True)
                    return
                except:
                    print("❌ 无效选择")
                    return
        
        print("⚠ 未找到配置文件")
    
    elif choice == '2':
        print("\n自定义高级检索配置")
        print("请按提示输入参数（直接回车跳过）\n")
        
        config_dict = {}
        
        keyword = input("搜索关键字: ").strip()
        if not keyword:
            print("❌ 必须提供关键字")
            return
        
        # 收集参数
        year_start = input("起始年份 (如: 2020): ").strip()
        if year_start.isdigit():
            config_dict['year_start'] = int(year_start)
        
        year_end = input("结束年份 (如: 2023): ").strip()
        if year_end.isdigit():
            config_dict['year_end'] = int(year_end)
        
        min_cit = input("最小引用量: ").strip()
        if min_cit.isdigit():
            config_dict['citations_min'] = int(min_cit)
        
        authors = input("作者 (逗号分隔): ").strip()
        if authors:
            config_dict['authors'] = [a.strip() for a in authors.split(',')]
        
        venues = input("会议/期刊 (逗号分隔): ").strip()
        if venues:
            config_dict['venues'] = [v.strip() for v in venues.split(',')]
        
        # 保存配置
        save = input("\n是否保存配置到文件? (y/n): ").strip().lower()
        if save == 'y':
            import json
            from datetime import datetime
            config_name = input("配置文件名 (无需后缀): ").strip() or f"custom_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            config_file = f"configs/{config_name}.json"
            
            import os
            os.makedirs("configs", exist_ok=True)
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, ensure_ascii=False, indent=2)
            
            print(f"✓ 配置已保存: {config_file}")
            
            # 使用配置搜索
            execute = input("是否立即使用此配置搜索? (y/n): ").strip().lower()
            if execute == 'y':
                import subprocess
                cmd = f'python scholar_crawler.py "{keyword}" --config "{config_file}"'
                print(f"\n执行命令: {cmd}\n")
                subprocess.call(cmd, shell=True)


def main():
    """主菜单"""
    while True:
        print("""
╔══════════════════════════════════════════════════════════╗
║     Google Scholar 文献爬取工具 - 快速开始              ║
╚══════════════════════════════════════════════════════════╝

请选择模式:
  1. 快速开始 (单个关键字搜索)
  2. 批量搜索 (多个关键字)
  3. 高级检索向导 (配置文件管理)
  4. 查看配置
  5. 退出

""")
        
        choice = input("请选择 (1-5): ").strip()
        
        if choice == '1':
            quick_start()
        elif choice == '2':
            batch_search()
        elif choice == '3':
            advanced_search_wizard()
        elif choice == '4':
            print(f"\n当前配置:")
            print(f"  默认搜索数量: {config.DEFAULT_MAX_RESULTS}")
            print(f"  默认最小引用: {config.DEFAULT_MIN_CITATIONS}")
            print(f"  输出目录: {config.OUTPUT_DIR}")
            print(f"  预设关键字总数: {len(config.get_all_keywords())}")
            print(f"  顶级AI会议: {len(config.TOP_AI_CONFERENCES)} 个")
            print(f"  顶级AI期刊: {len(config.TOP_AI_JOURNALS)} 个")
            input("\n按回车继续...")
        elif choice == '5':
            print("\n再见! 👋")
            break
        else:
            print("❌ 无效选择\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n再见! 👋")

