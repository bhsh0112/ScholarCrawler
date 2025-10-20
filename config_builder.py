#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置文件生成器
交互式界面帮助用户创建自定义配置文件
"""

from config import AdvancedSearchConfig, TOP_AI_CONFERENCES, TOP_AI_JOURNALS
from config_manager import ConfigManager


def build_config_interactive():
    """交互式构建配置"""
    print("""
╔══════════════════════════════════════════════════════════╗
║         高级检索配置生成器 🛠️                            ║
╚══════════════════════════════════════════════════════════╝

欢迎使用配置生成器！我将引导您一步步创建自定义配置。
按 Enter 键跳过可选项。

""")
    
    config = AdvancedSearchConfig()
    
    # 1. 配置描述
    print("=" * 60)
    print("第一步：配置描述")
    print("=" * 60)
    description = input("请输入配置描述（可选）: ").strip()
    if not description:
        description = "自定义配置"
    
    # 2. 年份范围
    print("\n" + "=" * 60)
    print("第二步：设置年份范围")
    print("=" * 60)
    print("提示：可以限制文献的发表年份")
    
    year_start = input("起始年份（例如: 2020，留空表示不限）: ").strip()
    if year_start.isdigit():
        config.year_start = int(year_start)
    
    year_end = input("结束年份（例如: 2023，留空表示不限）: ").strip()
    if year_end.isdigit():
        config.year_end = int(year_end)
    
    # 3. 引用量范围
    print("\n" + "=" * 60)
    print("第三步：设置引用量范围")
    print("=" * 60)
    print("提示：可以筛选高影响力文献")
    
    citations_min = input("最小引用量（例如: 50，留空表示0）: ").strip()
    if citations_min.isdigit():
        config.citations_min = int(citations_min)
    
    citations_max = input("最大引用量（留空表示不限）: ").strip()
    if citations_max.isdigit():
        config.citations_max = int(citations_max)
    
    # 4. 作者筛选
    print("\n" + "=" * 60)
    print("第四步：设置作者筛选")
    print("=" * 60)
    print("提示：可以搜索特定作者的文献")
    print("示例：Yann LeCun, Geoffrey Hinton")
    
    authors_input = input("作者列表（多个用逗号分隔，留空表示不限）: ").strip()
    if authors_input:
        config.authors = [a.strip() for a in authors_input.split(',')]
    
    # 5. 会议/期刊筛选
    print("\n" + "=" * 60)
    print("第五步：设置会议/期刊筛选")
    print("=" * 60)
    print("提示：可以限定在特定会议或期刊")
    print("  1. 手动输入")
    print("  2. 从预设列表选择（AI顶会）")
    print("  3. 从预设列表选择（AI顶刊）")
    print("  4. 跳过")
    
    venue_choice = input("\n请选择 (1-4): ").strip()
    
    if venue_choice == '1':
        venues_input = input("会议/期刊列表（多个用逗号分隔）: ").strip()
        if venues_input:
            config.venues = [v.strip() for v in venues_input.split(',')]
    
    elif venue_choice == '2':
        print("\n预设AI顶会:")
        for i, conf in enumerate(TOP_AI_CONFERENCES, 1):
            print(f"  {i}. {conf}")
        selected = input("\n选择会议编号（多个用逗号分隔，留空表示全选）: ").strip()
        
        if selected:
            indices = [int(i.strip()) - 1 for i in selected.split(',') if i.strip().isdigit()]
            config.venues = [TOP_AI_CONFERENCES[i] for i in indices if 0 <= i < len(TOP_AI_CONFERENCES)]
        else:
            config.venues = TOP_AI_CONFERENCES.copy()
    
    elif venue_choice == '3':
        print("\n预设AI顶刊:")
        for i, journal in enumerate(TOP_AI_JOURNALS, 1):
            print(f"  {i}. {journal}")
        selected = input("\n选择期刊编号（多个用逗号分隔，留空表示全选）: ").strip()
        
        if selected:
            indices = [int(i.strip()) - 1 for i in selected.split(',') if i.strip().isdigit()]
            config.venues = [TOP_AI_JOURNALS[i] for i in indices if 0 <= i < len(TOP_AI_JOURNALS)]
        else:
            config.venues = TOP_AI_JOURNALS.copy()
    
    # 6. 出版商筛选
    print("\n" + "=" * 60)
    print("第六步：设置出版商筛选")
    print("=" * 60)
    print("提示：可以限定特定出版商（如IEEE, ACM, Springer等）")
    
    publishers_input = input("出版商列表（多个用逗号分隔，留空表示不限）: ").strip()
    if publishers_input:
        config.publishers = [p.strip() for p in publishers_input.split(',')]
    
    # 7. 额外关键字
    print("\n" + "=" * 60)
    print("第七步：设置额外关键字")
    print("=" * 60)
    print("提示：在主关键字基础上添加额外的限定词")
    print("示例：neural, network, deep")
    
    additional_keywords = input("额外关键字（多个用逗号分隔）: ").strip()
    if additional_keywords:
        config.additional_keywords = [k.strip() for k in additional_keywords.split(',')]
    
    if config.additional_keywords:
        keyword_mode = input("关键字组合模式 (OR/AND，默认OR): ").strip().upper()
        if keyword_mode in ['AND', 'OR']:
            config.keyword_mode = keyword_mode
    
    # 8. 排除词
    print("\n" + "=" * 60)
    print("第八步：设置排除词")
    print("=" * 60)
    print("提示：排除包含特定词的文献（如综述类文章）")
    print("  1. 排除综述类（survey, review, tutorial）")
    print("  2. 自定义排除词")
    print("  3. 不排除")
    
    exclude_choice = input("\n请选择 (1-3): ").strip()
    
    if exclude_choice == '1':
        config.exclude_keywords = ['survey', 'review', 'tutorial', 'overview']
    elif exclude_choice == '2':
        exclude_input = input("排除词列表（多个用逗号分隔）: ").strip()
        if exclude_input:
            config.exclude_keywords = [e.strip() for e in exclude_input.split(',')]
    
    # 9. 保存配置
    print("\n" + "=" * 60)
    print("配置完成！")
    print("=" * 60)
    print("\n当前配置:")
    print(config)
    
    save = input("\n是否保存配置？(y/n): ").strip().lower()
    
    if save == 'y':
        filename = input("请输入文件名（例如: my_config.json）: ").strip()
        if not filename.endswith('.json'):
            filename += '.json'
        
        manager = ConfigManager()
        filepath = manager.save_config(config, filename, description)
        
        print(f"\n✓ 配置已保存到: {filepath}")
        print("\n使用方式:")
        print(f'  python scholar_crawler.py "your_keyword" --config {filepath}')
    else:
        print("\n配置未保存")
    
    return config


def quick_templates():
    """快速模板选择"""
    print("""
╔══════════════════════════════════════════════════════════╗
║            快速配置模板 🚀                               ║
╚══════════════════════════════════════════════════════════╝

选择一个预设模板快速创建配置：

  1. 最近高影响力文献（2020年后，引用>=50）
  2. 顶级AI会议（NeurIPS, ICML, ICLR等）
  3. 顶级CV会议（CVPR, ICCV, ECCV）
  4. 顶级NLP会议（ACL, EMNLP, NAACL）
  5. 顶级期刊（Nature, Science, TPAMI等）
  6. 突破性论文（引用>=500）
  7. 排除综述类文章
  8. Transformer相关研究
  9. GAN相关研究
  0. 返回自定义配置

""")
    
    choice = input("请选择 (0-9): ").strip()
    
    manager = ConfigManager()
    config = None
    description = ""
    default_filename = ""
    
    if choice == '1':
        config = manager.create_template('recent', year_start=2020, min_citations=50)
        description = "最近高影响力文献配置"
        default_filename = "recent_high_impact.json"
    
    elif choice == '2':
        config = manager.create_template('top_venues', 
                                        venues=['NeurIPS', 'ICML', 'ICLR', 'AAAI', 'IJCAI'],
                                        min_citations=20)
        description = "顶级AI会议配置"
        default_filename = "top_ai_conferences.json"
    
    elif choice == '3':
        config = manager.create_template('top_venues',
                                        venues=['CVPR', 'ICCV', 'ECCV'],
                                        min_citations=30)
        description = "顶级CV会议配置"
        default_filename = "cv_top_conferences.json"
    
    elif choice == '4':
        config = manager.create_template('top_venues',
                                        venues=['ACL', 'EMNLP', 'NAACL'],
                                        min_citations=25)
        description = "顶级NLP会议配置"
        default_filename = "nlp_top_conferences.json"
    
    elif choice == '5':
        config = manager.create_template('top_venues',
                                        venues=['Nature', 'Science', 'TPAMI', 'IJCV'],
                                        min_citations=30)
        description = "顶级期刊配置"
        default_filename = "top_journals.json"
    
    elif choice == '6':
        config = manager.create_template('high_impact', min_citations=500, year_start=2015)
        description = "突破性论文配置"
        default_filename = "breakthrough_papers.json"
    
    elif choice == '7':
        config = manager.create_template('exclude_reviews')
        description = "排除综述类文章配置"
        default_filename = "exclude_reviews.json"
    
    elif choice == '8':
        config = AdvancedSearchConfig()
        config.year_start = 2017
        config.citations_min = 100
        config.additional_keywords = ['transformer', 'attention mechanism']
        description = "Transformer相关研究配置"
        default_filename = "transformers_research.json"
    
    elif choice == '9':
        config = AdvancedSearchConfig()
        config.year_start = 2014
        config.citations_min = 80
        config.additional_keywords = ['GAN', 'generative adversarial']
        config.exclude_keywords = ['survey', 'review']
        description = "GAN相关研究配置"
        default_filename = "gan_research.json"
    
    elif choice == '0':
        return build_config_interactive()
    
    else:
        print("❌ 无效选择")
        return None
    
    if config:
        print("\n" + "=" * 60)
        print("模板配置:")
        print("=" * 60)
        print(config)
        
        save = input("\n是否保存此配置？(y/n): ").strip().lower()
        
        if save == 'y':
            filename = input(f"请输入文件名（默认: {default_filename}）: ").strip()
            if not filename:
                filename = default_filename
            elif not filename.endswith('.json'):
                filename += '.json'
            
            filepath = manager.save_config(config, filename, description)
            
            print(f"\n✓ 配置已保存到: {filepath}")
            print("\n使用方式:")
            print(f'  python scholar_crawler.py "your_keyword" --config {filepath}')
    
    return config


def list_existing_configs():
    """列出现有配置"""
    manager = ConfigManager()
    configs = manager.list_configs()
    
    if not configs:
        print("\n📁 没有找到配置文件")
        print("提示：可以使用配置生成器创建新配置")
        return
    
    print("\n" + "=" * 60)
    print(f"现有配置文件（共 {len(configs)} 个）")
    print("=" * 60)
    
    for i, cfg in enumerate(configs, 1):
        print(f"\n{i}. {cfg['filename']}")
        print(f"   描述: {cfg['description']}")
        print(f"   路径: {cfg['filepath']}")
    
    print("\n" + "=" * 60)
    
    action = input("\n查看详情？输入配置编号，或按Enter返回: ").strip()
    
    if action.isdigit():
        idx = int(action) - 1
        if 0 <= idx < len(configs):
            manager.print_config_info(configs[idx]['filepath'])
        else:
            print("❌ 无效编号")


def main():
    """主菜单"""
    while True:
        print("""
╔══════════════════════════════════════════════════════════╗
║         高级检索配置工具 🛠️                              ║
╚══════════════════════════════════════════════════════════╝

请选择操作:

  1. 🆕 创建自定义配置（交互式）
  2. 🚀 使用快速模板
  3. 📁 查看现有配置
  4. 📖 帮助文档
  5. 🚪 退出

""")
        
        choice = input("请选择 (1-5): ").strip()
        
        if choice == '1':
            build_config_interactive()
        
        elif choice == '2':
            quick_templates()
        
        elif choice == '3':
            list_existing_configs()
        
        elif choice == '4':
            print("""
╔══════════════════════════════════════════════════════════╗
║                    帮助文档                              ║
╚══════════════════════════════════════════════════════════╝

配置文件说明:
-------------
配置文件是JSON格式，包含以下字段：

1. description: 配置描述
2. year_start/year_end: 年份范围
3. citations_min/citations_max: 引用量范围
4. authors: 作者列表
5. publishers: 出版商列表
6. venues: 会议/期刊列表
7. additional_keywords: 额外关键字
8. exclude_keywords: 排除词
9. keyword_mode: 关键字组合模式 (OR/AND)

使用示例:
---------
1. 使用配置文件搜索:
   python scholar_crawler.py "deep learning" --config configs/my_config.json

2. 命令行参数搜索:
   python scholar_crawler.py "ML" --year-start 2020 --min-citations 50

3. 组合使用:
   python scholar_crawler.py "AI" --config configs/base.json --year-start 2022

配置文件位置:
-------------
所有配置文件保存在 configs/ 目录下

更多信息请查看 README.md
""")
            input("\n按Enter继续...")
        
        elif choice == '5':
            print("\n再见! 👋\n")
            break
        
        else:
            print("❌ 无效选择\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n再见! 👋\n")

