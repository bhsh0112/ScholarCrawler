# 排序功能使用指南 📊

## 概述

现在你可以根据多种维度对检索结果进行排序，不再局限于引用量排序！

## 支持的排序方式

| 排序字段 | 说明 | 适用场景 |
|---------|------|---------|
| `citations` | 按引用量排序 | 查找高影响力文献（默认） |
| `year` | 按年份排序 | 查找最新或最早的研究 |
| `title` | 按标题字母顺序排序 | 按标题组织文献 |
| `relevance` | 按相关性排序 | 保持Google Scholar原始排序 |

## 排序顺序

- `desc` - 降序（从大到小，从新到旧）**默认**
- `asc` - 升序（从小到大，从旧到新）

---

## 使用方式

### 方式一：命令行参数

```bash
# 按引用量降序（默认）
python scholar_crawler.py "deep learning"

# 按年份降序（最新优先）
python scholar_crawler.py "deep learning" --sort-by year --sort-order desc

# 按年份升序（最早优先）
python scholar_crawler.py "deep learning" --sort-by year --sort-order asc

# 按相关性排序
python scholar_crawler.py "deep learning" --sort-by relevance

# 按标题字母顺序
python scholar_crawler.py "deep learning" --sort-by title --sort-order asc
```

### 方式二：配置文件（推荐）

在JSON配置文件中添加排序字段：

```json
{
  "description": "你的配置",
  "year_start": 2020,
  "citations_min": 10,
  "sort_by": "year",
  "sort_order": "desc"
}
```

使用：
```bash
python scholar_crawler.py "deep learning" --config configs/your_config.json
```

---

## 实用示例

### 示例1：查找最新文献

**需求**：查找2020年后的最新深度学习研究

```bash
python scholar_crawler.py "deep learning" \
  --year-start 2020 \
  --sort-by year \
  --sort-order desc \
  --max 30
```

或使用配置文件 `configs/sort_by_year_newest.json`：

```bash
python scholar_crawler.py "deep learning" --config configs/sort_by_year_newest.json
```

### 示例2：查找早期经典文献

**需求**：查找深度学习早期的经典论文

```bash
python scholar_crawler.py "deep learning" \
  --year-start 2006 \
  --year-end 2015 \
  --min-citations 500 \
  --sort-by year \
  --sort-order asc
```

### 示例3：按相关性排序

**需求**：保持Google Scholar的相关性排序

```bash
python scholar_crawler.py "transformer attention mechanism" \
  --sort-by relevance \
  --max 50
```

或使用配置：

```bash
python scholar_crawler.py "transformer" --config configs/sort_by_relevance.json
```

### 示例4：高引用文献按年份排序

**需求**：查找高影响力文献，但按年份排序看趋势

```bash
python scholar_crawler.py "computer vision" \
  --min-citations 100 \
  --year-start 2018 \
  --sort-by year \
  --sort-order desc
```

### 示例5：组合排序策略

**需求**：先按年份筛选，再按引用量排序

配置文件 `configs/recent_high_impact_sorted.json`:

```json
{
  "description": "最近高影响力文献，按引用量排序",
  "year_start": 2020,
  "citations_min": 50,
  "sort_by": "citations",
  "sort_order": "desc"
}
```

```bash
python scholar_crawler.py "machine learning" --config configs/recent_high_impact_sorted.json
```

---

## 预设配置文件

我已经为你创建了几个排序相关的配置文件：

### 1. 按年份排序（最新优先）
```bash
python scholar_crawler.py "deep learning" --config configs/sort_by_year_newest.json
```

### 2. 按相关性排序
```bash
python scholar_crawler.py "deep learning" --config configs/sort_by_relevance.json
```

### 3. 按标题排序
```bash
python scholar_crawler.py "deep learning" --config configs/sort_by_title.json
```

---

## 配置文件完整示例

### 配置1：最新AI研究（按年份）

`configs/ai_latest_research.json`:

```json
{
  "description": "最新AI研究 - 按年份降序",
  "year_start": 2022,
  "year_end": null,
  "citations_min": 5,
  "citations_max": null,
  "authors": [],
  "publishers": [],
  "venues": ["NeurIPS", "ICML", "ICLR"],
  "additional_keywords": [],
  "exclude_keywords": ["survey", "review"],
  "keyword_mode": "OR",
  "sort_by": "year",
  "sort_order": "desc"
}
```

### 配置2：经典论文（按引用量）

`configs/classic_papers_high_citations.json`:

```json
{
  "description": "经典论文 - 按引用量降序",
  "year_start": 2010,
  "year_end": 2020,
  "citations_min": 500,
  "citations_max": null,
  "authors": [],
  "publishers": [],
  "venues": [],
  "additional_keywords": [],
  "exclude_keywords": [],
  "keyword_mode": "OR",
  "sort_by": "citations",
  "sort_order": "desc"
}
```

### 配置3：按相关性搜索（探索性研究）

`configs/exploratory_research.json`:

```json
{
  "description": "探索性研究 - 按相关性排序",
  "year_start": null,
  "year_end": null,
  "citations_min": 0,
  "citations_max": null,
  "authors": [],
  "publishers": [],
  "venues": [],
  "additional_keywords": [],
  "exclude_keywords": [],
  "keyword_mode": "OR",
  "sort_by": "relevance",
  "sort_order": "desc"
}
```

---

## 排序字段详解

### 1. citations（引用量）

**用途**：查找高影响力文献

**排序逻辑**：
- `desc`：引用量从高到低
- `asc`：引用量从低到高

**适用场景**：
- ✅ 查找领域经典论文
- ✅ 了解高影响力研究
- ✅ 寻找突破性工作

**示例**：
```bash
# 查找引用量最高的论文
python scholar_crawler.py "GAN" --sort-by citations --sort-order desc
```

### 2. year（年份）

**用途**：按时间顺序组织文献

**排序逻辑**：
- `desc`：从新到旧（2023 → 2020）
- `asc`：从旧到新（2020 → 2023）

**适用场景**：
- ✅ 追踪最新研究进展
- ✅ 研究技术发展历史
- ✅ 按时间线组织文献综述

**示例**：
```bash
# 最新的transformer研究
python scholar_crawler.py "transformer" \
  --year-start 2020 \
  --sort-by year \
  --sort-order desc

# 深度学习的早期研究
python scholar_crawler.py "deep learning" \
  --year-start 2006 \
  --year-end 2012 \
  --sort-by year \
  --sort-order asc
```

### 3. relevance（相关性）

**用途**：保持Google Scholar的智能排序

**排序逻辑**：
- 保持Google Scholar的原始排序
- Google Scholar根据多个因素综合排序：
  - 关键字匹配度
  - 引用量
  - 发表时间
  - 作者权威性
  - 等等

**适用场景**：
- ✅ 探索性研究
- ✅ 不确定如何排序时
- ✅ 相信Google Scholar的智能算法

**示例**：
```bash
# 让Google Scholar决定最相关的文献
python scholar_crawler.py "attention mechanism transformer" \
  --sort-by relevance
```

### 4. title（标题）

**用途**：按字母顺序组织

**排序逻辑**：
- `asc`：A → Z
- `desc`：Z → A

**适用场景**：
- ✅ 整理文献列表
- ✅ 查找特定标题
- ✅ 按名称分组

**示例**：
```bash
# 按标题字母顺序排列
python scholar_crawler.py "neural network" \
  --sort-by title \
  --sort-order asc
```

---

## 常见使用场景

### 场景1：文献综述（按年份）

**目标**：撰写文献综述，需要按时间顺序组织

```bash
python scholar_crawler.py "federated learning" \
  --year-start 2016 \
  --sort-by year \
  --sort-order asc \
  --max 100
```

### 场景2：追踪最新进展（按年份降序）

**目标**：了解某领域最新研究

```bash
python scholar_crawler.py "large language model" \
  --year-start 2022 \
  --sort-by year \
  --sort-order desc \
  --max 50
```

### 场景3：查找经典论文（按引用量）

**目标**：学习领域基础，从经典论文开始

```bash
python scholar_crawler.py "convolutional neural network" \
  --year-start 2012 \
  --year-end 2018 \
  --min-citations 1000 \
  --sort-by citations \
  --sort-order desc
```

### 场景4：探索新主题（按相关性）

**目标**：探索不熟悉的新领域

```bash
python scholar_crawler.py "neuromorphic computing" \
  --sort-by relevance \
  --max 30
```

### 场景5：组合策略

**目标**：查找2020年后的高引用文献，先看最新的

```bash
python scholar_crawler.py "self-supervised learning" \
  --year-start 2020 \
  --min-citations 50 \
  --sort-by year \
  --sort-order desc
```

---

## 在Python代码中使用

```python
from scholar_crawler import ScholarCrawler
from config import AdvancedSearchConfig

# 创建配置
config = AdvancedSearchConfig()
config.year_start = 2020
config.sort_by = "year"      # 按年份排序
config.sort_order = "desc"   # 降序（最新优先）

# 执行搜索
crawler = ScholarCrawler(use_proxy=True)
papers = crawler.search_papers("deep learning", max_results=30, 
                              advanced_config=config)

# 排序已在内部完成
for paper in papers:
    print(f"{paper['year']} - {paper['title']} - {paper['citations']} citations")
```

---

## 更新现有配置文件

如果你已经有配置文件，只需添加两个字段即可：

```json
{
  "description": "你的配置",
  // ... 其他配置 ...
  "sort_by": "year",        // 添加这行
  "sort_order": "desc"      // 添加这行
}
```

如果不添加这两个字段，默认会按引用量降序排序（保持向后兼容）。

---

## 快速参考

```bash
# 按引用量（默认）
python scholar_crawler.py "keyword" --sort-by citations --sort-order desc

# 按年份（最新优先）
python scholar_crawler.py "keyword" --sort-by year --sort-order desc

# 按年份（最早优先）
python scholar_crawler.py "keyword" --sort-by year --sort-order asc

# 按相关性
python scholar_crawler.py "keyword" --sort-by relevance

# 按标题
python scholar_crawler.py "keyword" --sort-by title --sort-order asc
```

---

## 注意事项

1. **相关性排序**：选择 `relevance` 时，会保持Google Scholar的原始排序，其他参数不会改变这个顺序

2. **年份字段缺失**：如果某些文献没有年份信息，按年份排序时会将它们放在最后（降序）或最前（升序）

3. **配置文件优先级**：如果同时使用配置文件和命令行参数，命令行参数会覆盖配置文件

4. **向后兼容**：如果配置文件中没有 `sort_by` 字段，默认按引用量降序排序

---

## 更多帮助

- 查看所有参数：`python scholar_crawler.py --help`
- 查看配置示例：`configs/` 目录
- 详细文档：`ADVANCED_GUIDE.md`

**开始使用吧！** 🎯📚

