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

