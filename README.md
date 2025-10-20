# Google Scholar 文献爬取工具

一个功能强大的 Google Scholar 文献搜索和爬取工具，可以根据关键字搜索学术文献，按引用量排序，并导出为 CSV 格式。

## ✨ 功能特点

- 🔍 **关键字搜索**: 支持任意关键字搜索学术文献
- 📊 **引用量排序**: 自动按引用量从高到低排序
- 🎯 **智能筛选**: 支持按最小引用量筛选文献
- 📁 **CSV导出**: 导出结构化的 CSV 表格文件
- 🌐 **代理支持**: 支持使用代理避免访问限制
- 📈 **统计分析**: 自动生成文献统计信息

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

### 完整示例

```bash
# 搜索"deep learning"，获取100篇文献，筛选引用量>=100的，使用代理
python scholar_crawler.py "deep learning" --max 100 --min-citations 100 --proxy --output dl_papers.csv
```

## 📋 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `keyword` | 搜索关键字（必需） | - |
| `--max` | 最大获取文献数量 | 50 |
| `--min-citations` | 最小引用量筛选 | 0 |
| `--output` | 输出CSV文件名 | 自动生成 |
| `--proxy` | 使用代理 | 不使用 |

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

### 在 Python 代码中使用

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

## 📝 更新日志

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

