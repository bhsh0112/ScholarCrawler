# Google Scholar 文献爬取工具

一个功能强大的 Google Scholar 文献搜索和爬取工具，可以根据关键字搜索学术文献，按引用量排序，并导出为 CSV 格式。**现已支持高级检索功能！**

## ✨ 功能特点

### 基础功能
- 🔍 **关键字搜索**: 支持任意关键字搜索学术文献
- 📊 **引用量排序**: 自动按引用量从高到低排序
- 🎯 **智能筛选**: 支持按最小引用量筛选文献
- 📁 **CSV导出**: 导出结构化的 CSV 表格文件
- 🌐 **代理支持**: 支持使用代理避免访问限制
- 📈 **统计分析**: 自动生成文献统计信息

### 🆕 高级检索功能
- 👤 **作者筛选**: 搜索特定作者的文献
- 📅 **日期范围**: 限定文献发表年份范围
- 🏛️ **会议/期刊筛选**: 筛选特定会议或期刊的文献
- 🏢 **出版商筛选**: 按出版商筛选（如 IEEE, ACM）
- 📊 **引用量范围**: 设置引用量的上下限
- 🚫 **排除关键字**: 排除不想要的文献类型
- ➕ **额外关键字**: 组合多个关键字搜索
- 📄 **配置文件**: 保存和复用搜索配置

## 📦 安装依赖

```bash
cd scholar_crawler
pip install -r requirements.txt
```

## 🚀 快速开始

### 基础用法

```bash
# 搜索"deep learning"相关文献
python scholar_crawler.py "deep learning"

# 搜索100篇文献
python scholar_crawler.py "machine learning" --max 100

# 只保留引用量>=50的文献
python scholar_crawler.py "computer vision" --min-citations 50

# 指定输出文件名
python scholar_crawler.py "neural networks" --output my_results.csv

# 使用代理（推荐，避免被限制）
python scholar_crawler.py "artificial intelligence" --proxy
```

### 🆕 高级检索用法

```bash
# 搜索2020-2023年间的文献
python scholar_crawler.py "deep learning" --year-start 2020 --year-end 2023

# 搜索特定作者的文献
python scholar_crawler.py "computer vision" --authors "Yann LeCun,Kaiming He"

# 搜索顶会文献（CVPR, ICCV, ECCV）
python scholar_crawler.py "object detection" --venues "CVPR,ICCV,ECCV" --min-citations 50

# 排除综述类文章
python scholar_crawler.py "transformer" --exclude "survey,review,tutorial"

# 使用配置文件进行复杂检索
python scholar_crawler.py "deep learning" --config configs/recent_high_impact.json
```

### 📝 使用配置文件（推荐）

对于复杂的检索需求，建议使用配置文件：

```bash
# 使用预设的配置文件
python scholar_crawler.py "deep learning" --config configs/top_ai_conferences.json
python scholar_crawler.py "computer vision" --config configs/recent_high_impact.json
python scholar_crawler.py "NLP" --config configs/nature_science.json
```

配置文件示例 (`my_config.json`):
```json
{
  "year_start": 2020,
  "year_end": 2023,
  "citations_min": 100,
  "venues": ["NeurIPS", "ICML", "ICLR"],
  "exclude_keywords": ["survey", "review"]
}
```

### 完整示例

```bash
# 基础搜索：获取100篇文献，筛选引用量>=100的，使用代理
python scholar_crawler.py "deep learning" --max 100 --min-citations 100 --proxy

# 高级检索：搜索2021-2023年顶会的高引用深度学习文献
python scholar_crawler.py "deep learning" \
  --year-start 2021 --year-end 2023 \
  --venues "NeurIPS,ICML,CVPR" \
  --min-citations 50 \
  --exclude "survey,review" \
  --proxy
```

## 📋 命令行参数

### 基础参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `keyword` | 搜索关键字（必需） | - |
| `--max` | 最大获取文献数量 | 50 |
| `--output` | 输出CSV文件名 | 自动生成 |
| `--proxy` | 使用代理 | 不使用 |

### 🆕 高级检索参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--authors` | 作者筛选（逗号分隔） | `"Andrew Ng,Yann LeCun"` |
| `--year-start` | 起始年份 | `2020` |
| `--year-end` | 结束年份 | `2023` |
| `--publishers` | 出版商筛选（逗号分隔） | `"IEEE,ACM,Springer"` |
| `--venues` | 会议/期刊筛选（逗号分隔） | `"CVPR,NeurIPS,Nature"` |
| `--min-citations` | 最小引用量 | `50` |
| `--max-citations` | 最大引用量 | `1000` |
| `--exclude` | 排除关键字（逗号分隔） | `"survey,review"` |
| `--additional-keywords` | 额外关键字（逗号分隔） | `"neural,network"` |
| `--keyword-mode` | 关键字组合模式 | `OR` 或 `AND` |
| `--config` | 配置文件路径 | `configs/my_config.json` |

## 📊 输出格式

CSV文件包含以下字段：

| 字段 | 说明 |
|------|------|
| title | 论文标题 |
| authors | 作者列表（分号分隔） |
| year | 发表年份 |
| venue | 发表会议/期刊 |
| publisher | 出版商 |
| citations | 引用次数 |
| abstract | 摘要 |
| url | 论文链接 |
| eprint_url | 预印本链接 |

## 📁 输出示例

```
results/
├── deep_learning_20251020_143052.csv
├── machine_learning_20251020_144201.csv
└── computer_vision_20251020_145327.csv
```

## ⚠️ 注意事项

1. **访问限制**: Google Scholar 可能会限制频繁访问，建议：
   - 使用 `--proxy` 参数启用代理
   - 在请求之间添加了2秒延迟
   - 不要一次性爬取过多数据

2. **网络问题**: 如果遇到网络错误：
   - 检查网络连接
   - 尝试使用代理
   - 减少 `--max` 参数值

3. **数据准确性**: 
   - 引用数可能不是实时更新
   - 部分字段可能为空（如摘要、链接等）

## 🛠️ 高级用法

### 🆕 高级检索详细说明

#### 1. 预设配置文件

工具提供了多个预设配置文件，可直接使用：

| 配置文件 | 说明 | 适用场景 |
|---------|------|----------|
| `configs/recent_high_impact.json` | 2020年后，引用≥50 | 查找最新高影响力研究 |
| `configs/top_ai_conferences.json` | 顶级AI会议（10个） | 查找顶会发表的论文 |
| `configs/nature_science.json` | Nature/Science系列 | 查找顶刊突破性研究 |

**使用示例:**
```bash
# 在顶级会议中搜索计算机视觉文献
python scholar_crawler.py "computer vision" --config configs/top_ai_conferences.json

# 搜索Nature/Science上的深度学习文献
python scholar_crawler.py "deep learning" --config configs/nature_science.json
```

#### 2. 自定义配置文件

创建自己的配置文件 `my_search.json`:
```json
{
  "description": "我的自定义检索配置",
  "year_start": 2021,
  "year_end": 2023,
  "citations_min": 100,
  "venues": ["CVPR", "ICCV", "ECCV", "NeurIPS"],
  "authors": ["Kaiming He", "Ross Girshick"],
  "exclude_keywords": ["survey", "review", "dataset"],
  "keyword_mode": "AND"
}
```

使用：
```bash
python scholar_crawler.py "ResNet" --config my_search.json
```

#### 3. 实际应用场景

**场景1: 追踪最新研究进展**
```bash
# 搜索2023年后的Transformer相关高引用文献
python scholar_crawler.py "transformer" \
  --year-start 2023 \
  --min-citations 20 \
  --exclude "survey,review"
```

**场景2: 文献综述准备**
```bash
# 搜索2018-2022年计算机视觉领域的经典文献
python scholar_crawler.py "computer vision" \
  --year-start 2018 --year-end 2022 \
  --min-citations 200 \
  --venues "CVPR,ICCV,ECCV,TPAMI"
```

**场景3: 关注特定研究团队**
```bash
# 搜索Hinton团队的深度学习工作
python scholar_crawler.py "deep learning" \
  --authors "Geoffrey Hinton,Yann LeCun,Yoshua Bengio" \
  --year-start 2015 \
  --min-citations 50
```

**场景4: 顶会论文调研**
```bash
# 使用配置文件批量搜索多个主题
for topic in "GAN" "VAE" "Transformer" "Diffusion"; do
  python scholar_crawler.py "$topic" \
    --config configs/top_ai_conferences.json \
    --max 50
done
```

#### 4. 交互式高级检索

使用交互式向导进行高级检索：
```bash
python quick_start.py
# 选择 "3. 高级检索向导"
```

向导功能：
- 选择预设配置文件
- 创建并保存自定义配置
- 可视化配置管理

### 在 Python 代码中使用

#### 基础用法
```python
from scholar_crawler import ScholarCrawler

# 创建爬虫实例
crawler = ScholarCrawler(use_proxy=True)

# 搜索文献
papers = crawler.search_papers("deep learning", max_results=50)

# 按引用量排序
papers = crawler.sort_by_citations(papers)

# 筛选高引用文献
papers = crawler.filter_by_citations(papers, min_citations=100)

# 导出CSV
crawler.export_to_csv(papers, "results.csv", "deep learning")
```

#### 🆕 使用高级检索
```python
from scholar_crawler import ScholarCrawler
from config import AdvancedSearchConfig

# 创建高级检索配置
advanced_config = AdvancedSearchConfig()
advanced_config.year_start = 2020
advanced_config.year_end = 2023
advanced_config.citations_min = 50
advanced_config.venues = ["CVPR", "ICCV", "ECCV"]
advanced_config.exclude_keywords = ["survey", "review"]

# 使用高级配置搜索
crawler = ScholarCrawler(use_proxy=True)
papers = crawler.search_papers(
    "object detection", 
    max_results=50,
    advanced_config=advanced_config
)

# 排序并导出
papers = crawler.sort_by_citations(papers)
crawler.export_to_csv(papers, "object_detection_cvpr.csv", "object detection")
```

#### 使用预设配置函数
```python
from config import (
    create_recent_high_impact_config,
    create_top_venue_config,
    TOP_AI_CONFERENCES
)

# 使用预设配置
config1 = create_recent_high_impact_config(2020, 50)
config2 = create_top_venue_config(TOP_AI_CONFERENCES)

# 搜索
papers1 = crawler.search_papers("deep learning", max_results=50, advanced_config=config1)
papers2 = crawler.search_papers("NLP", max_results=50, advanced_config=config2)
```

## 🔧 故障排除

### 问题1: 安装 scholarly 失败

```bash
# 尝试升级 pip
pip install --upgrade pip

# 重新安装
pip install scholarly
```

### 问题2: 无法获取数据

- 检查网络连接
- 使用 `--proxy` 参数
- 等待一段时间后重试

### 问题3: 代理设置失败

如果免费代理不稳定，可以：
- 不使用代理，直接访问
- 配置自己的代理服务器（需要修改代码）

## 📚 更多资源

- **配置文件文档**: 查看 `configs/README_CONFIGS.md` 了解配置文件的详细说明
- **示例脚本**: 运行 `python example.py` 查看5个实用示例
- **交互式向导**: 运行 `python quick_start.py` 使用友好的交互界面

## 📝 更新日志

### v1.1.0 (2025-10-20) - 高级检索版本 🆕
- ✨ 新增高级检索功能
  - 支持作者筛选
  - 支持日期范围限定
  - 支持会议/期刊筛选
  - 支持出版商筛选
  - 支持引用量范围设置
  - 支持排除关键字
  - 支持额外关键字组合
- 📄 新增配置文件支持
  - 提供3个预设配置文件
  - 支持JSON格式自定义配置
  - 配置文件可保存和复用
- 🔧 改进交互式向导
  - 新增高级检索向导
  - 支持配置文件管理
  - 更友好的用户界面
- 📚 完善文档
  - 新增高级检索使用说明
  - 提供多个实际应用场景
  - 新增配置文件详细文档

### v1.0.0 (2025-10-20)
- 初始版本
- 支持基础搜索和CSV导出
- 支持引用量筛选和排序
- 支持代理功能

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

如有问题或建议，请联系项目维护者。

