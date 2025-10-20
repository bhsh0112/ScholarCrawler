#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置文件
包含常用的配置项和关键字列表
"""

# ==================== 搜索配置 ====================

# 默认搜索结果数量
DEFAULT_MAX_RESULTS = 50

# 默认最小引用量
DEFAULT_MIN_CITATIONS = 0

# 请求之间的延迟（秒）
REQUEST_DELAY = 2

# 是否默认使用代理
USE_PROXY_BY_DEFAULT = False


# ==================== 输出配置 ====================

# 输出目录
OUTPUT_DIR = "results"

# CSV文件编码
CSV_ENCODING = "utf-8-sig"  # 使用 utf-8-sig 以便 Excel 正确识别中文


# ==================== 预设关键字列表 ====================

# 人工智能相关
AI_KEYWORDS = [
    "machine learning",
    "deep learning",
    "neural networks",
    "artificial intelligence",
    "reinforcement learning",
    "transfer learning",
]

# 计算机视觉相关
CV_KEYWORDS = [
    "computer vision",
    "image recognition",
    "object detection",
    "semantic segmentation",
    "image classification",
    "face recognition",
]

# 自然语言处理相关
NLP_KEYWORDS = [
    "natural language processing",
    "machine translation",
    "sentiment analysis",
    "text classification",
    "named entity recognition",
    "question answering",
]

# 推荐系统相关
RECSYS_KEYWORDS = [
    "recommendation system",
    "collaborative filtering",
    "content-based filtering",
    "matrix factorization",
    "deep learning recommendation",
]

# 数据挖掘相关
DM_KEYWORDS = [
    "data mining",
    "knowledge discovery",
    "clustering",
    "classification",
    "association rules",
    "anomaly detection",
]

# 大数据相关
BIGDATA_KEYWORDS = [
    "big data",
    "distributed computing",
    "spark",
    "hadoop",
    "data stream mining",
]


# ==================== 高级配置 ====================

# 需要提取的字段列表
FIELDS_TO_EXTRACT = [
    'title',
    'authors',
    'year',
    'venue',
    'publisher',
    'citations',
    'abstract',
    'url',
    'eprint_url',
]

# 代理配置（如果使用自定义代理）
CUSTOM_PROXY = {
    'http': None,   # 例如: 'http://127.0.0.1:7890'
    'https': None,  # 例如: 'http://127.0.0.1:7890'
}


# ==================== 高级检索配置 ====================

class AdvancedSearchConfig:
    """
    高级检索配置类
    用于配置更精细的搜索条件
    """
    
    def __init__(self):
        # 作者筛选
        self.authors = []  # 作者列表，例如: ["Andrew Ng", "Yann LeCun"]
        
        # 日期范围
        self.year_start = None  # 起始年份，例如: 2020
        self.year_end = None    # 结束年份，例如: 2023
        
        # 发表机构/出版商
        self.publishers = []  # 出版商列表，例如: ["IEEE", "ACM", "Springer"]
        self.venues = []      # 会议/期刊列表，例如: ["CVPR", "NeurIPS", "Nature"]
        
        # 引用量范围
        self.citations_min = 0    # 最小引用量
        self.citations_max = None # 最大引用量（None表示不限）
        
        # 关键字组合模式
        self.keyword_mode = "OR"  # "OR" 或 "AND"
        self.additional_keywords = []  # 额外的关键字
        
        # 排除词
        self.exclude_keywords = []  # 要排除的关键字
        
        # 文献类型
        self.paper_types = []  # 例如: ["journal", "conference", "book"]
    
    def to_query_string(self, base_keyword):
        """
        将配置转换为Google Scholar查询字符串
        
        Args:
            base_keyword: 基础关键字
            
        Returns:
            构建的查询字符串
        """
        query_parts = [base_keyword]
        
        # 添加作者筛选
        if self.authors:
            author_queries = [f'author:"{author}"' for author in self.authors]
            query_parts.append(f"({' OR '.join(author_queries)})")
        
        # 添加额外关键字
        if self.additional_keywords:
            if self.keyword_mode == "AND":
                query_parts.extend(self.additional_keywords)
            else:
                query_parts.append(f"({' OR '.join(self.additional_keywords)})")
        
        # 添加排除词
        for exclude in self.exclude_keywords:
            query_parts.append(f"-{exclude}")
        
        return " ".join(query_parts)
    
    def matches_filters(self, paper_info):
        """
        检查论文是否符合筛选条件
        
        Args:
            paper_info: 论文信息字典
            
        Returns:
            是否符合条件
        """
        # 检查年份范围
        if self.year_start or self.year_end:
            year = paper_info.get('year', 'N/A')
            if year != 'N/A':
                try:
                    year_int = int(year)
                    if self.year_start and year_int < self.year_start:
                        return False
                    if self.year_end and year_int > self.year_end:
                        return False
                except (ValueError, TypeError):
                    pass
        
        # 检查引用量范围
        citations = paper_info.get('citations', 0)
        if self.citations_min and citations < self.citations_min:
            return False
        if self.citations_max and citations > self.citations_max:
            return False
        
        # 检查发表机构
        if self.publishers:
            publisher = paper_info.get('publisher', '').lower()
            if not any(pub.lower() in publisher for pub in self.publishers):
                return False
        
        # 检查会议/期刊
        if self.venues:
            venue = paper_info.get('venue', '').lower()
            if not any(v.lower() in venue for v in self.venues):
                return False
        
        # 检查作者（在结果中二次筛选）
        if self.authors:
            authors_str = paper_info.get('authors', '').lower()
            if not any(author.lower() in authors_str for author in self.authors):
                return False
        
        return True
    
    def __str__(self):
        """返回配置的字符串表示"""
        config_str = "高级搜索配置:\n"
        
        if self.authors:
            config_str += f"  作者: {', '.join(self.authors)}\n"
        
        if self.year_start or self.year_end:
            year_range = f"{self.year_start or '不限'} - {self.year_end or '不限'}"
            config_str += f"  年份范围: {year_range}\n"
        
        if self.citations_min > 0 or self.citations_max:
            cit_range = f"{self.citations_min} - {self.citations_max or '不限'}"
            config_str += f"  引用量范围: {cit_range}\n"
        
        if self.publishers:
            config_str += f"  出版商: {', '.join(self.publishers)}\n"
        
        if self.venues:
            config_str += f"  会议/期刊: {', '.join(self.venues)}\n"
        
        if self.additional_keywords:
            config_str += f"  额外关键字 ({self.keyword_mode}): {', '.join(self.additional_keywords)}\n"
        
        if self.exclude_keywords:
            config_str += f"  排除词: {', '.join(self.exclude_keywords)}\n"
        
        return config_str if len(config_str) > len("高级搜索配置:\n") else "高级搜索配置: 无"


# ==================== 预设高级搜索配置示例 ====================

def create_recent_high_impact_config(year_start=2020, min_citations=50):
    """创建最近高影响力文献配置"""
    config = AdvancedSearchConfig()
    config.year_start = year_start
    config.citations_min = min_citations
    return config


def create_top_venue_config(venues):
    """创建顶会顶刊配置"""
    config = AdvancedSearchConfig()
    config.venues = venues
    return config


def create_author_config(authors):
    """创建特定作者配置"""
    config = AdvancedSearchConfig()
    config.authors = authors
    return config


# 顶级会议列表
TOP_AI_CONFERENCES = [
    "NeurIPS", "ICML", "ICLR", "AAAI", "IJCAI",
    "CVPR", "ICCV", "ECCV",
    "ACL", "EMNLP", "NAACL",
    "KDD", "WWW", "SIGIR",
]

# 顶级期刊列表
TOP_AI_JOURNALS = [
    "Nature", "Science", "TPAMI", "IJCV",
    "JMLR", "Nature Machine Intelligence",
    "IEEE Transactions", "ACM Transactions",
]


# ==================== 实用函数 ====================

def get_all_keywords():
    """获取所有预设关键字"""
    return (
        AI_KEYWORDS + 
        CV_KEYWORDS + 
        NLP_KEYWORDS + 
        RECSYS_KEYWORDS + 
        DM_KEYWORDS + 
        BIGDATA_KEYWORDS
    )


def get_keywords_by_category(category):
    """
    根据类别获取关键字
    
    Args:
        category: 类别名称 ('ai', 'cv', 'nlp', 'recsys', 'dm', 'bigdata')
    
    Returns:
        关键字列表
    """
    categories = {
        'ai': AI_KEYWORDS,
        'cv': CV_KEYWORDS,
        'nlp': NLP_KEYWORDS,
        'recsys': RECSYS_KEYWORDS,
        'dm': DM_KEYWORDS,
        'bigdata': BIGDATA_KEYWORDS,
    }
    
    return categories.get(category.lower(), [])


if __name__ == '__main__':
    # 测试配置
    print("=== 配置测试 ===\n")
    print(f"默认搜索数量: {DEFAULT_MAX_RESULTS}")
    print(f"默认最小引用: {DEFAULT_MIN_CITATIONS}")
    print(f"输出目录: {OUTPUT_DIR}")
    
    print("\n=== 预设关键字 ===")
    print(f"\n人工智能 ({len(AI_KEYWORDS)}个):")
    for kw in AI_KEYWORDS:
        print(f"  - {kw}")
    
    print(f"\n计算机视觉 ({len(CV_KEYWORDS)}个):")
    for kw in CV_KEYWORDS:
        print(f"  - {kw}")
    
    print(f"\n自然语言处理 ({len(NLP_KEYWORDS)}个):")
    for kw in NLP_KEYWORDS:
        print(f"  - {kw}")
    
    print(f"\n总计关键字数量: {len(get_all_keywords())}")

