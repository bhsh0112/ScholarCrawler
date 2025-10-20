# Scholar Crawler 项目概览 📚

## 项目介绍

Google Scholar 文献爬取工具，支持基础搜索和高级检索功能，可通过多种方式（命令行参数、配置文件、交互式界面）进行文献搜索，并导出为CSV格式。

---

## 📁 项目结构

```
scholar_crawler/
│
├── 📘 文档
│   ├── README.md                    # 主要文档（入门必读）
│   ├── ADVANCED_GUIDE.md            # 高级检索详细指南
│   ├── QUICK_REFERENCE.md           # 快速参考手册
│   └── PROJECT_OVERVIEW.md          # 本文档
│
├── 🔧 核心脚本
│   ├── scholar_crawler.py           # 主程序（文献爬取核心）
│   ├── config.py                    # 配置类和预设值
│   ├── config_manager.py            # 配置文件管理工具
│   └── config_builder.py            # 交互式配置生成器
│
├── 📝 示例脚本
│   ├── quick_start.py               # 快速开始向导（交互式）
│   ├── example.py                   # 基础使用示例
│   └── advanced_examples.py         # 高级检索示例（10个）
│
├── ⚙️ 配置文件
│   ├── configs/                     # 配置文件目录
│   │   ├── top_ai_conferences.json  # AI顶会配置
│   │   ├── cv_top_conferences.json  # CV顶会配置
│   │   ├── nlp_top_conferences.json # NLP顶会配置
│   │   ├── ml_top_conferences.json  # ML顶会配置
│   │   ├── nature_science.json      # Nature/Science配置
│   │   ├── ieee_acm_journals.json   # IEEE/ACM期刊配置
│   │   ├── recent_high_impact.json  # 最近高影响力配置
│   │   ├── breakthrough_papers.json # 突破性论文配置
│   │   ├── transformers_research.json # Transformer研究配置
│   │   ├── gan_research.json        # GAN研究配置
│   │   └── top_ai_authors.json      # 顶级学者配置
│   └── advanced_search_examples.json # 配置示例文件
│
├── 📊 输出
│   └── results/                     # CSV结果保存目录
│
└── 📦 依赖
    └── requirements.txt             # Python依赖包
```

---

## 🚀 核心功能

### 1. 基础搜索功能
- ✅ 关键字搜索
- ✅ 引用量排序
- ✅ CSV导出
- ✅ 统计分析
- ✅ 代理支持

### 2. 高级检索功能
- ✅ 作者筛选
- ✅ 日期范围限定
- ✅ 会议/期刊筛选
- ✅ 出版商筛选
- ✅ 引用量范围设置
- ✅ 关键字组合（AND/OR）
- ✅ 排除特定类型文章
- ✅ 配置文件支持

### 3. 辅助工具
- ✅ 交互式配置生成器
- ✅ 配置文件管理器
- ✅ 快速开始向导
- ✅ 多个实用示例

---

## 📖 使用方式

### 方式一：命令行直接使用

**适合**：快速搜索、简单条件

```bash
# 基础搜索
python scholar_crawler.py "deep learning"

# 高级检索
python scholar_crawler.py "deep learning" \
  --year-start 2020 \
  --min-citations 50 \
  --venues "NeurIPS,ICML"
```

### 方式二：配置文件（推荐）

**适合**：复杂检索、重复使用、团队协作

```bash
# 使用预设配置
python scholar_crawler.py "deep learning" --config configs/top_ai_conferences.json

# 使用自定义配置
python scholar_crawler.py "computer vision" --config configs/my_config.json
```

### 方式三：交互式工具

**适合**：新手、不确定参数、探索功能

```bash
# 快速开始向导
python quick_start.py

# 配置生成器
python config_builder.py

# 查看示例
python advanced_examples.py
```

### 方式四：Python代码

**适合**：自动化、批量处理、定制化

```python
from scholar_crawler import ScholarCrawler
from config import AdvancedSearchConfig

config = AdvancedSearchConfig()
config.year_start = 2020
config.min_citations = 50

crawler = ScholarCrawler(use_proxy=True)
papers = crawler.search_papers("deep learning", max_results=50, 
                              advanced_config=config)
```

---

## 🛠️ 工具详解

### 1. scholar_crawler.py - 主程序

核心爬取程序，支持所有检索功能。

**基本用法**：
```bash
python scholar_crawler.py "关键字" [参数]
```

**主要参数**：
- `--max`: 最大数量
- `--output`: 输出文件名
- `--proxy`: 使用代理
- `--config`: 加载配置文件
- 更多高级参数见 `QUICK_REFERENCE.md`

### 2. config_builder.py - 配置生成器

交互式创建配置文件，友好的问答式界面。

**功能**：
- 🆕 创建自定义配置（分步引导）
- 🚀 使用快速模板（9种预设）
- 📁 查看现有配置
- 📖 帮助文档

**使用**：
```bash
python config_builder.py
```

### 3. config_manager.py - 配置管理器

命令行配置文件管理工具。

**功能**：
- `list`: 列出所有配置
- `validate`: 验证配置文件
- `info`: 查看配置详情
- `create`: 创建模板配置

**使用**：
```bash
# 列出配置
python config_manager.py list

# 验证配置
python config_manager.py validate configs/my_config.json

# 查看详情
python config_manager.py info configs/top_ai_conferences.json
```

### 4. quick_start.py - 快速开始向导

友好的交互式界面，适合新手入门。

**功能**：
- 单个关键字搜索（向导式）
- 批量搜索多个关键字
- 从预设列表选择
- 查看配置

**使用**：
```bash
python quick_start.py
```

### 5. advanced_examples.py - 示例脚本

10个实用示例，涵盖各种检索场景。

**示例列表**：
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

**使用**：
```bash
python advanced_examples.py
```

---

## 📝 配置文件说明

### 配置文件格式

JSON格式，包含以下字段：

```json
{
  "description": "配置描述",
  "year_start": 2020,              // 起始年份
  "year_end": 2023,                // 结束年份
  "citations_min": 50,             // 最小引用量
  "citations_max": null,           // 最大引用量
  "authors": ["作者1", "作者2"],    // 作者列表
  "publishers": ["IEEE", "ACM"],   // 出版商列表
  "venues": ["CVPR", "NeurIPS"],   // 会议/期刊列表
  "additional_keywords": ["kw1"],  // 额外关键字
  "exclude_keywords": ["survey"],  // 排除词
  "keyword_mode": "OR"             // OR 或 AND
}
```

### 预设配置分类

#### 按会议/期刊
- `top_ai_conferences.json` - AI顶会
- `cv_top_conferences.json` - CV顶会
- `nlp_top_conferences.json` - NLP顶会
- `ml_top_conferences.json` - ML顶会
- `nature_science.json` - Nature/Science
- `ieee_acm_journals.json` - IEEE/ACM期刊

#### 按影响力
- `recent_high_impact.json` - 最近高影响力
- `breakthrough_papers.json` - 突破性论文

#### 按主题
- `transformers_research.json` - Transformer研究
- `gan_research.json` - GAN研究

#### 按作者
- `top_ai_authors.json` - 顶级AI学者

---

## 📊 输出格式

CSV文件包含以下字段：

| 字段 | 说明 |
|------|------|
| title | 论文标题 |
| authors | 作者列表（分号分隔） |
| year | 发表年份 |
| venue | 会议/期刊 |
| publisher | 出版商 |
| citations | 引用次数 |
| abstract | 摘要 |
| url | 论文链接 |
| eprint_url | 预印本链接 |

---

## 🎯 典型使用流程

### 流程A：新手入门

1. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

2. **运行向导**：
   ```bash
   python quick_start.py
   ```

3. **按提示操作**，完成第一次搜索

### 流程B：快速搜索

1. **命令行搜索**：
   ```bash
   python scholar_crawler.py "deep learning" --min-citations 50
   ```

2. **查看结果**：
   打开 `results/` 目录下的CSV文件

### 流程C：高级检索

1. **创建或选择配置**：
   ```bash
   python config_builder.py
   ```

2. **使用配置搜索**：
   ```bash
   python scholar_crawler.py "关键字" --config configs/my_config.json
   ```

3. **分析结果**：
   使用Excel或Python处理CSV

### 流程D：批量任务

1. **准备配置文件**

2. **编写批处理脚本**：
   ```bash
   for keyword in "kw1" "kw2" "kw3"
   do
     python scholar_crawler.py "$keyword" --config configs/my_config.json
     sleep 10
   done
   ```

3. **运行并收集结果**

---

## 💡 最佳实践

### 1. 检索策略
- 从宽到窄：先基础搜索，再加限制
- 分层筛选：逐步添加条件
- 组合使用：命令行 + 配置文件

### 2. 性能优化
- 使用代理（`--proxy`）
- 控制数量（`--max 50`）
- 添加延迟（已内置）
- 分批进行

### 3. 配置管理
- 使用描述性文件名
- 按类别组织配置
- 定期更新和维护
- 团队共享配置

### 4. 结果处理
- Excel分析
- Python处理
- 数据可视化
- 导出报告

---

## 📚 学习路径

### 第一阶段：基础使用
1. 阅读 `README.md`
2. 运行 `quick_start.py`
3. 尝试基础搜索
4. 了解CSV输出格式

### 第二阶段：高级检索
1. 阅读 `QUICK_REFERENCE.md`
2. 学习命令行参数
3. 尝试不同筛选条件
4. 运行 `advanced_examples.py`

### 第三阶段：配置文件
1. 阅读 `ADVANCED_GUIDE.md`
2. 查看预设配置文件
3. 使用 `config_builder.py` 创建配置
4. 将常用检索保存为配置

### 第四阶段：深度定制
1. 学习配置文件格式
2. 编写批处理脚本
3. Python代码集成
4. 结果后处理

---

## ❓ 常见问题

### Q1: 如何开始？
**A**: 运行 `python quick_start.py`，按向导操作。

### Q2: 搜索结果太少？
**A**: 降低 `--min-citations` 或扩大年份范围。

### Q3: 搜索失败？
**A**: 添加 `--proxy` 参数，或检查网络连接。

### Q4: 如何重复使用检索条件？
**A**: 使用配置文件（推荐）或 `config_builder.py` 创建。

### Q5: 配置文件格式错误？
**A**: 运行 `python config_manager.py validate your_config.json`

更多问题见 `ADVANCED_GUIDE.md` 的常见问题部分。

---

## 📞 获取帮助

| 文档 | 用途 |
|------|------|
| `README.md` | 项目介绍和基础用法 |
| `QUICK_REFERENCE.md` | 快速查询所有参数 |
| `ADVANCED_GUIDE.md` | 详细的高级检索指南 |
| `PROJECT_OVERVIEW.md` | 本文档，项目全貌 |

| 工具 | 用途 |
|------|------|
| `quick_start.py` | 新手入门向导 |
| `config_builder.py` | 创建配置文件 |
| `config_manager.py` | 管理配置文件 |
| `advanced_examples.py` | 学习示例代码 |

---

## 🔄 更新日志

### v2.0.0 (2025-10-20) - 高级检索版本
- ✅ 添加高级检索功能
- ✅ 支持配置文件系统
- ✅ 创建配置生成器和管理工具
- ✅ 添加11个预设配置模板
- ✅ 创建完整文档系统
- ✅ 提供10个使用示例

### v1.0.0 (2025-10-20) - 初始版本
- ✅ 基础搜索功能
- ✅ 引用量排序
- ✅ CSV导出
- ✅ 基础筛选

---

**祝你的文献调研顺利！** 📚✨

如有问题，请查阅相关文档或运行交互式工具获取帮助。

