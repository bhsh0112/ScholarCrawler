#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置文件管理工具
用于加载、验证和管理高级检索配置文件
"""

import json
import os
from typing import Dict, List, Optional
from config import AdvancedSearchConfig


class ConfigManager:
    """配置文件管理器"""
    
    def __init__(self, configs_dir="configs"):
        """
        初始化配置管理器
        
        Args:
            configs_dir: 配置文件目录
        """
        self.configs_dir = configs_dir
        if not os.path.exists(configs_dir):
            os.makedirs(configs_dir)
    
    def load_config(self, config_path: str) -> AdvancedSearchConfig:
        """
        从JSON文件加载配置
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            AdvancedSearchConfig对象
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        config = AdvancedSearchConfig()
        
        # 从字典加载配置
        for key, value in config_data.items():
            # 跳过注释和元数据字段
            if key.startswith('_') or key == 'description':
                continue
            if hasattr(config, key):
                setattr(config, key, value)
        
        return config
    
    def save_config(self, config: AdvancedSearchConfig, filename: str, 
                    description: str = "") -> str:
        """
        保存配置到JSON文件
        
        Args:
            config: AdvancedSearchConfig对象
            filename: 文件名
            description: 配置描述
            
        Returns:
            保存的文件路径
        """
        config_dict = {
            "description": description,
            "year_start": config.year_start,
            "year_end": config.year_end,
            "citations_min": config.citations_min,
            "citations_max": config.citations_max,
            "authors": config.authors,
            "publishers": config.publishers,
            "venues": config.venues,
            "additional_keywords": config.additional_keywords,
            "exclude_keywords": config.exclude_keywords,
            "keyword_mode": config.keyword_mode,
            "sort_by": getattr(config, 'sort_by', 'citations'),
            "sort_order": getattr(config, 'sort_order', 'desc'),
        }
        
        filepath = os.path.join(self.configs_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def list_configs(self) -> List[Dict]:
        """
        列出所有可用的配置文件
        
        Returns:
            配置文件信息列表
        """
        configs = []
        
        if not os.path.exists(self.configs_dir):
            return configs
        
        for filename in os.listdir(self.configs_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.configs_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        config_data = json.load(f)
                    
                    configs.append({
                        'filename': filename,
                        'filepath': filepath,
                        'description': config_data.get('description', '无描述'),
                    })
                except Exception as e:
                    print(f"⚠ 读取配置文件 {filename} 失败: {e}")
        
        return configs
    
    def validate_config(self, config_path: str) -> tuple:
        """
        验证配置文件是否有效
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            (是否有效, 错误信息)
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # 检查必需字段
            valid_fields = {
                'year_start', 'year_end', 'citations_min', 'citations_max',
                'authors', 'publishers', 'venues', 'additional_keywords',
                'exclude_keywords', 'keyword_mode', 'description'
            }
            
            for key in config_data.keys():
                if not key.startswith('_') and key not in valid_fields:
                    return False, f"未知字段: {key}"
            
            # 检查年份范围
            if config_data.get('year_start') and config_data.get('year_end'):
                if config_data['year_start'] > config_data['year_end']:
                    return False, "起始年份不能大于结束年份"
            
            # 检查引用量范围
            if config_data.get('citations_min') and config_data.get('citations_max'):
                if config_data['citations_min'] > config_data['citations_max']:
                    return False, "最小引用量不能大于最大引用量"
            
            # 检查keyword_mode
            if config_data.get('keyword_mode') and config_data['keyword_mode'] not in ['OR', 'AND']:
                return False, "keyword_mode 必须是 'OR' 或 'AND'"
            
            return True, "配置文件有效"
            
        except json.JSONDecodeError as e:
            return False, f"JSON格式错误: {e}"
        except Exception as e:
            return False, f"验证失败: {e}"
    
    def create_template(self, template_type: str, **kwargs) -> AdvancedSearchConfig:
        """
        创建预设模板配置
        
        Args:
            template_type: 模板类型 ('recent', 'top_venues', 'author', 'high_impact', 'exclude_reviews')
            **kwargs: 模板参数
            
        Returns:
            AdvancedSearchConfig对象
        """
        config = AdvancedSearchConfig()
        
        if template_type == 'recent':
            # 最近文献模板
            config.year_start = kwargs.get('year_start', 2020)
            config.citations_min = kwargs.get('min_citations', 0)
        
        elif template_type == 'top_venues':
            # 顶级会议/期刊模板
            config.venues = kwargs.get('venues', [])
            config.citations_min = kwargs.get('min_citations', 20)
        
        elif template_type == 'author':
            # 特定作者模板
            config.authors = kwargs.get('authors', [])
        
        elif template_type == 'high_impact':
            # 高影响力文献模板
            config.citations_min = kwargs.get('min_citations', 100)
            config.year_start = kwargs.get('year_start', 2015)
        
        elif template_type == 'exclude_reviews':
            # 排除综述类文章模板
            config.exclude_keywords = ['survey', 'review', 'tutorial', 'overview']
        
        return config
    
    def merge_configs(self, *config_paths) -> AdvancedSearchConfig:
        """
        合并多个配置文件
        
        Args:
            *config_paths: 配置文件路径列表
            
        Returns:
            合并后的AdvancedSearchConfig对象
        """
        merged_config = AdvancedSearchConfig()
        
        for config_path in config_paths:
            config = self.load_config(config_path)
            
            # 合并列表类型的字段
            merged_config.authors.extend(config.authors)
            merged_config.publishers.extend(config.publishers)
            merged_config.venues.extend(config.venues)
            merged_config.additional_keywords.extend(config.additional_keywords)
            merged_config.exclude_keywords.extend(config.exclude_keywords)
            
            # 对于范围类型的字段，取更严格的条件
            if config.year_start:
                merged_config.year_start = max(
                    merged_config.year_start or 0, 
                    config.year_start
                )
            if config.year_end:
                merged_config.year_end = min(
                    merged_config.year_end or 9999, 
                    config.year_end
                )
            if config.citations_min:
                merged_config.citations_min = max(
                    merged_config.citations_min, 
                    config.citations_min
                )
            if config.citations_max:
                merged_config.citations_max = min(
                    merged_config.citations_max or float('inf'), 
                    config.citations_max
                )
        
        # 去重
        merged_config.authors = list(set(merged_config.authors))
        merged_config.publishers = list(set(merged_config.publishers))
        merged_config.venues = list(set(merged_config.venues))
        merged_config.additional_keywords = list(set(merged_config.additional_keywords))
        merged_config.exclude_keywords = list(set(merged_config.exclude_keywords))
        
        return merged_config
    
    def print_config_info(self, config_path: str):
        """打印配置文件详细信息"""
        config = self.load_config(config_path)
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        print("\n" + "="*60)
        print(f"配置文件: {os.path.basename(config_path)}")
        print("="*60)
        print(f"描述: {config_data.get('description', '无')}")
        print("\n" + str(config))
        print("="*60)


def main():
    """主函数 - 配置管理工具"""
    import argparse
    
    parser = argparse.ArgumentParser(description='配置文件管理工具')
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # list 命令
    list_parser = subparsers.add_parser('list', help='列出所有配置文件')
    
    # validate 命令
    validate_parser = subparsers.add_parser('validate', help='验证配置文件')
    validate_parser.add_argument('config', help='配置文件路径')
    
    # info 命令
    info_parser = subparsers.add_parser('info', help='显示配置文件详细信息')
    info_parser.add_argument('config', help='配置文件路径')
    
    # create 命令
    create_parser = subparsers.add_parser('create', help='创建模板配置')
    create_parser.add_argument('template_type', 
                              choices=['recent', 'top_venues', 'author', 'high_impact', 'exclude_reviews'],
                              help='模板类型')
    create_parser.add_argument('--output', required=True, help='输出文件名')
    create_parser.add_argument('--year-start', type=int, help='起始年份')
    create_parser.add_argument('--min-citations', type=int, help='最小引用量')
    create_parser.add_argument('--venues', help='会议/期刊列表（逗号分隔）')
    create_parser.add_argument('--authors', help='作者列表（逗号分隔）')
    
    args = parser.parse_args()
    
    manager = ConfigManager()
    
    if args.command == 'list':
        configs = manager.list_configs()
        if not configs:
            print("📁 没有找到配置文件")
        else:
            print(f"\n📁 找到 {len(configs)} 个配置文件:\n")
            for i, cfg in enumerate(configs, 1):
                print(f"{i}. {cfg['filename']}")
                print(f"   描述: {cfg['description']}")
                print(f"   路径: {cfg['filepath']}\n")
    
    elif args.command == 'validate':
        is_valid, message = manager.validate_config(args.config)
        if is_valid:
            print(f"✓ {message}")
        else:
            print(f"❌ {message}")
    
    elif args.command == 'info':
        manager.print_config_info(args.config)
    
    elif args.command == 'create':
        kwargs = {}
        if args.year_start:
            kwargs['year_start'] = args.year_start
        if args.min_citations:
            kwargs['min_citations'] = args.min_citations
        if args.venues:
            kwargs['venues'] = [v.strip() for v in args.venues.split(',')]
        if args.authors:
            kwargs['authors'] = [a.strip() for a in args.authors.split(',')]
        
        config = manager.create_template(args.template_type, **kwargs)
        filepath = manager.save_config(config, args.output, 
                                      f"{args.template_type} 模板配置")
        print(f"✓ 配置文件已创建: {filepath}")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

