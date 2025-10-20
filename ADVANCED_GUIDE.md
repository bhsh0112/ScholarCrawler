# 高级检索使用指南 📚

本指南详细介绍如何使用 Scholar Crawler 的高级检索功能。

## 目录

- [快速开始](#快速开始)
- [高级检索参数详解](#高级检索参数详解)
- [配置文件系统](#配置文件系统)
- [实用工具](#实用工具)
- [使用示例](#使用示例)
- [最佳实践](#最佳实践)

---

## 快速开始

### 三种使用方式

#### 1. 命令行参数（适合简单检索）

```bash
python scholar_crawler.py "deep learning" --year-start 2020 --min-citations 50
```

#### 2. 配置文件（推荐，适合复杂检索）

```bash
python scholar_crawler.py "deep learning" --config configs/top_ai_conferences.json
```

#### 3. 交互式工具（最友好）

```bash
python config_builder.py
```

---

## 高级检索参数详解

### 👤 作者筛选 `--authors`

搜索特定作者的文献。支持多个作者，用逗号分隔。

```bash
# 单个作者
python scholar_crawler.py "neural networks" --authors "Yann LeCun"

# 多个作者（OR关系）
python scholar_crawler.py "deep learning" --authors "Yann LeCun,Geoffrey Hinton,Yoshua Bengio"
```

**适用场景**：
- 追踪特定研究者的工作
- 研究某个研究团队的成果
- 了解领域大牛的最新进展

### 📅 日期范围 `--year-start` `--year-end`

限定文献发表年份范围。

```bash
# 只搜索2020年之后的文献
python scholar_crawler.py "transformer" --year-start 2020

# 搜索2018-2022年间的文献
python scholar_crawler.py "GAN" --year-start 2018 --year-end 2022

# 搜索最近3年的文献
python scholar_crawler.py "reinforcement learning" --year-start 2021
```

**适用场景**：
- 了解最新研究进展
- 研究某个时期的技术发展
- 排除过时的研究

### 🏛️ 会议/期刊筛选 `--venues`

限定在特定会议或期刊发表的文献。

```bash
# AI顶会
python scholar_crawler.py "deep learning" --venues "NeurIPS,ICML,ICLR"

# CV顶会
python scholar_crawler.py "object detection" --venues "CVPR,ICCV,ECCV"

# NLP顶会
python scholar_crawler.py "language model" --venues "ACL,EMNLP,NAACL"

# 顶刊
python scholar_crawler.py "machine learning" --venues "Nature,Science,TPAMI"
```

**预设会议/期刊列表**：
- **AI**: NeurIPS, ICML, ICLR, AAAI, IJCAI
- **CV**: CVPR, ICCV, ECCV
- **NLP**: ACL, EMNLP, NAACL, COLING
- **DM**: KDD, WWW, SIGIR, WSDM
- **期刊**: Nature, Science, TPAMI, IJCV, JMLR

### 🏢 出版商筛选 `--publishers`

按出版商筛选文献。

```bash
# IEEE出版物
python scholar_crawler.py "computer vision" --publishers "IEEE"

# ACM出版物
python scholar_crawler.py "machine learning" --publishers "ACM"

# IEEE和ACM
python scholar_crawler.py "AI" --publishers "IEEE,ACM"
```

**常见出版商**：
- IEEE
- ACM
- Springer
- Elsevier
- Nature Publishing Group

### 📊 引用量范围

#### `--min-citations` 最小引用量

筛选高影响力文献。

```bash
# 引用量>=50
python scholar_crawler.py "deep learning" --min-citations 50

# 引用量>=100（高影响力）
python scholar_crawler.py "transformer" --min-citations 100

# 引用量>=500（突破性论文）
python scholar_crawler.py "neural networks" --min-citations 500
```

#### `--max-citations` 最大引用量

筛选中等影响力或新兴研究。

```bash
# 引用量在50-200之间（中等影响）
python scholar_crawler.py "federated learning" --min-citations 50 --max-citations 200

# 引用量<100（新兴研究）
python scholar_crawler.py "prompt learning" --max-citations 100
```

### 🚫 排除关键字 `--exclude`

排除不想要的文献类型。

```bash
# 排除综述类文章
python scholar_crawler.py "deep learning" --exclude "survey,review,tutorial"

# 排除综述和教程
python scholar_crawler.py "GAN" --exclude "survey,review,tutorial,overview"

# 排除特定主题
python scholar_crawler.py "neural networks" --exclude "medical,healthcare"
```

**常用排除词**：
- `survey` - 综述
- `review` - 回顾
- `tutorial` - 教程
- `overview` - 概述
- `introduction` - 介绍

### ➕ 额外关键字 `--additional-keywords`

在基础关键字上添加额外限定。

```bash
# OR模式（默认）：包含任一关键字即可
python scholar_crawler.py "deep learning" --additional-keywords "neural,optimization" --keyword-mode OR

# AND模式：必须同时包含所有关键字
python scholar_crawler.py "deep learning" --additional-keywords "neural,optimization,training" --keyword-mode AND
```

**使用技巧**：
- OR模式：扩大搜索范围
- AND模式：精确限定主题

---

## 配置文件系统

### 为什么使用配置文件？

配置文件适合以下场景：
1. **复杂检索条件**：多个参数组合
2. **重复使用**：保存常用的检索条件
3. **团队协作**：共享检索配置
4. **批量任务**：对多个关键字使用相同配置

### 配置文件格式

JSON格式，包含所有高级检索参数：

```json
{
  "description": "配置描述",
  "year_start": 2020,
  "year_end": 2023,
  "citations_min": 50,
  "citations_max": null,
  "authors": ["Author 1", "Author 2"],
  "publishers": ["IEEE", "ACM"],
  "venues": ["CVPR", "NeurIPS"],
  "additional_keywords": ["neural", "network"],
  "exclude_keywords": ["survey", "review"],
  "keyword_mode": "OR"
}
```

### 预设配置文件

项目包含多个预设配置文件（位于 `configs/` 目录）：

#### 1. 顶级会议/期刊

- `top_ai_conferences.json` - AI顶会（NeurIPS, ICML, ICLR等）
- `cv_top_conferences.json` - CV顶会（CVPR, ICCV, ECCV）
- `nlp_top_conferences.json` - NLP顶会（ACL, EMNLP等）
- `ml_top_conferences.json` - ML顶会
- `nature_science.json` - Nature/Science期刊
- `ieee_acm_journals.json` - IEEE/ACM期刊

#### 2. 按影响力

- `recent_high_impact.json` - 最近高影响力（2020+，引用>=50）
- `breakthrough_papers.json` - 突破性论文（引用>=500）

#### 3. 按主题

- `transformers_research.json` - Transformer相关研究
- `gan_research.json` - GAN相关研究

#### 4. 按作者

- `top_ai_authors.json` - 顶级AI学者

### 创建自定义配置

#### 方式一：手动创建JSON文件

```json
{
  "description": "我的自定义配置",
  "year_start": 2021,
  "year_end": 2023,
  "citations_min": 30,
  "venues": ["CVPR", "ICCV"],
  "exclude_keywords": ["survey"]
}
```

保存为 `configs/my_config.json`

#### 方式二：使用交互式生成器（推荐）

```bash
python config_builder.py
```

按照提示一步步创建配置，支持：
- 自定义参数设置
- 快速模板选择
- 预设列表选择
- 自动保存

#### 方式三：使用配置管理工具

```bash
# 创建配置
python config_manager.py create recent --output my_config.json --year-start 2020

# 验证配置
python config_manager.py validate configs/my_config.json

# 查看配置详情
python config_manager.py info configs/my_config.json

# 列出所有配置
python config_manager.py list
```

---

## 实用工具

### 1. 配置生成器 `config_builder.py`

交互式配置文件生成工具。

```bash
python config_builder.py
```

**功能**：
- 🆕 创建自定义配置（分步引导）
- 🚀 使用快速模板（预设9种常用配置）
- 📁 查看现有配置
- 📖 查看帮助文档

### 2. 配置管理器 `config_manager.py`

命令行配置文件管理工具。

```bash
# 列出所有配置
python config_manager.py list

# 验证配置文件
python config_manager.py validate configs/my_config.json

# 查看配置详情
python config_manager.py info configs/top_ai_conferences.json

# 创建模板配置
python config_manager.py create high_impact --output my_high_impact.json --min-citations 100
```

### 3. 高级示例脚本 `advanced_examples.py`

10个实用示例，展示各种高级检索场景。

```bash
python advanced_examples.py
```

**包含示例**：
1. 按年份范围搜索
2. 搜索特定作者
3. 搜索顶会文献
4. 排除综述类文章
5. 搜索突破性论文
6. 从配置文件加载
7. 综合高级检索
8. 按出版商筛选
9. 按引用量范围筛选
10. 关键字AND模式

### 4. 快速开始向导 `quick_start.py`

友好的交互式界面，适合新手。

```bash
python quick_start.py
```

---

## 使用示例

### 示例1：搜索最近的高影响力文献

**需求**：搜索2020年后发表、引用量>=50的深度学习文献

```bash
python scholar_crawler.py "deep learning" \
  --year-start 2020 \
  --min-citations 50 \
  --max 50
```

### 示例2：搜索顶会的CV文献

**需求**：搜索CVPR/ICCV/ECCV上的目标检测文献

```bash
python scholar_crawler.py "object detection" \
  --venues "CVPR,ICCV,ECCV" \
  --year-start 2020 \
  --min-citations 30
```

### 示例3：追踪特定作者

**需求**：搜索Kaiming He在CV领域的工作

```bash
python scholar_crawler.py "computer vision" \
  --authors "Kaiming He" \
  --min-citations 50
```

### 示例4：排除综述，只要原创研究

**需求**：搜索Transformer相关原创研究

```bash
python scholar_crawler.py "transformer" \
  --year-start 2017 \
  --exclude "survey,review,tutorial" \
  --min-citations 100
```

### 示例5：综合检索

**需求**：搜索2021-2023年顶会发表的GAN高引用论文

创建配置文件 `configs/gan_top.json`:

```json
{
  "description": "GAN顶会高引用",
  "year_start": 2021,
  "year_end": 2023,
  "citations_min": 50,
  "venues": ["NeurIPS", "ICML", "CVPR", "ICCV"],
  "additional_keywords": ["GAN", "generative"],
  "exclude_keywords": ["survey"],
  "keyword_mode": "OR"
}
```

使用配置：

```bash
python scholar_crawler.py "image generation" --config configs/gan_top.json
```

### 示例6：批量搜索

使用配置文件对多个关键字进行相同的检索：

```bash
# 对多个关键字使用相同配置
for keyword in "object detection" "semantic segmentation" "instance segmentation"
do
  python scholar_crawler.py "$keyword" --config configs/cv_top_conferences.json
  sleep 10  # 添加延迟
done
```

---

## 最佳实践

### 1. 检索策略

#### 🎯 从宽到窄

1. **第一步**：使用基础关键字，不加限制条件
2. **第二步**：查看结果，确定需要的筛选条件
3. **第三步**：添加年份、引用量等限制
4. **第四步**：精确到特定会议/作者

#### 📊 分层筛选

```bash
# 第一层：基础筛选（年份+引用量）
python scholar_crawler.py "deep learning" --year-start 2020 --min-citations 30

# 第二层：添加会议筛选
python scholar_crawler.py "deep learning" --year-start 2020 --min-citations 30 --venues "NeurIPS,ICML"

# 第三层：排除不需要的
python scholar_crawler.py "deep learning" --year-start 2020 --min-citations 30 --venues "NeurIPS,ICML" --exclude "survey"
```

### 2. 引用量设置建议

根据研究领域和发表时间选择合适的引用量阈值：

| 发表年份 | 低影响 | 中等影响 | 高影响 | 突破性 |
|---------|--------|----------|--------|--------|
| 2023-2024 | 10+ | 30+ | 100+ | 300+ |
| 2021-2022 | 20+ | 50+ | 150+ | 500+ |
| 2019-2020 | 30+ | 80+ | 200+ | 800+ |
| 2017-2018 | 50+ | 150+ | 400+ | 1500+ |
| 2015之前 | 100+ | 300+ | 1000+ | 5000+ |

### 3. 避免被限制

Google Scholar 会限制频繁访问，建议：

1. **使用代理**：添加 `--proxy` 参数
2. **控制数量**：`--max` 设置为 50 以内
3. **添加延迟**：代码已内置2秒延迟
4. **分批进行**：不要一次搜索太多

### 4. 配置文件管理

#### 命名规范

```
{用途}_{条件}_{日期}.json

示例:
- cv_topconf_2023.json
- ml_recent_highcite.json
- nlp_specific_authors.json
```

#### 组织结构

```
configs/
├── by_venue/          # 按会议/期刊
│   ├── cvpr_papers.json
│   └── neurips_papers.json
├── by_topic/          # 按主题
│   ├── transformer.json
│   └── gan.json
├── by_author/         # 按作者
│   └── top_scholars.json
└── templates/         # 通用模板
    ├── recent.json
    └── high_impact.json
```

### 5. 结果分析

导出CSV后，可以进行：

1. **Excel分析**：打开CSV文件，使用筛选和排序
2. **Python处理**：
```python
import pandas as pd

df = pd.read_csv('results.csv')

# 按年份分组统计
print(df.groupby('year')['citations'].agg(['count', 'mean', 'sum']))

# Top 10 高引用
print(df.nlargest(10, 'citations')[['title', 'citations', 'year']])

# 作者分布
authors = df['authors'].str.split(';').explode()
print(authors.value_counts().head(10))
```

### 6. 常见问题

#### Q: 搜索结果太少？

- 放宽筛选条件（降低引用量要求）
- 扩大年份范围
- 减少venue限制
- 使用OR模式而不是AND模式

#### Q: 搜索结果太多？

- 提高引用量要求
- 缩小年份范围
- 添加venue限制
- 使用AND模式
- 添加排除词

#### Q: 搜索速度慢？

- 减少 `--max` 值
- 使用代理
- 检查网络连接

#### Q: 配置文件不生效？

- 验证JSON格式：`python config_manager.py validate your_config.json`
- 检查字段名拼写
- 确保值的类型正确（数字、字符串、数组）

---

## 进阶技巧

### 1. 组合多个配置

```python
from config_manager import ConfigManager

manager = ConfigManager()

# 合并多个配置
config = manager.merge_configs(
    'configs/recent_high_impact.json',
    'configs/top_ai_conferences.json'
)
```

### 2. 编程方式使用

```python
from scholar_crawler import ScholarCrawler
from config import AdvancedSearchConfig

# 创建配置
config = AdvancedSearchConfig()
config.year_start = 2020
config.citations_min = 50
config.venues = ['CVPR', 'ICCV']

# 执行搜索
crawler = ScholarCrawler(use_proxy=True)
papers = crawler.search_papers('object detection', max_results=30, 
                              advanced_config=config)

# 处理结果
for paper in papers:
    print(f"{paper['title']} - {paper['citations']} citations")
```

### 3. 自定义后处理

```python
# 按作者筛选（二次筛选）
def filter_by_first_author(papers, author_name):
    return [p for p in papers 
            if p['authors'].split(';')[0].strip() == author_name]

# 按关键字密度筛选
def filter_by_keyword_density(papers, keywords, min_count=2):
    filtered = []
    for paper in papers:
        text = (paper['title'] + ' ' + paper['abstract']).lower()
        count = sum(1 for kw in keywords if kw.lower() in text)
        if count >= min_count:
            filtered.append(paper)
    return filtered
```

---

## 获取帮助

- 📖 查看主文档：`README.md`
- 💬 查看示例：运行 `python advanced_examples.py`
- 🛠️ 使用工具：运行 `python config_builder.py`
- ❓ 遇到问题：检查 [常见问题](#常见问题) 部分

---

**祝你的文献调研顺利！** 📚✨

