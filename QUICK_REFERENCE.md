# 快速参考手册 🚀

一页纸掌握所有功能！

## 📝 基础命令

```bash
# 基础搜索
python scholar_crawler.py "关键字"

# 指定数量
python scholar_crawler.py "关键字" --max 100

# 使用代理
python scholar_crawler.py "关键字" --proxy
```

## 🔍 高级检索

### 命令行方式

```bash
# 年份范围
python scholar_crawler.py "关键字" --year-start 2020 --year-end 2023

# 作者筛选
python scholar_crawler.py "关键字" --authors "作者1,作者2"

# 会议筛选
python scholar_crawler.py "关键字" --venues "CVPR,NeurIPS"

# 引用量
python scholar_crawler.py "关键字" --min-citations 50

# 排除词
python scholar_crawler.py "关键字" --exclude "survey,review"

# 组合使用
python scholar_crawler.py "关键字" \
  --year-start 2020 \
  --min-citations 50 \
  --venues "CVPR,ICCV" \
  --exclude "survey"
```

### 配置文件方式（推荐）

```bash
# 使用预设配置
python scholar_crawler.py "关键字" --config configs/top_ai_conferences.json

# 使用自定义配置
python scholar_crawler.py "关键字" --config configs/my_config.json
```

## 🛠️ 实用工具

```bash
# 交互式配置生成器
python config_builder.py

# 配置管理工具
python config_manager.py list                          # 列出配置
python config_manager.py validate configs/xxx.json     # 验证配置
python config_manager.py info configs/xxx.json         # 查看详情

# 示例脚本
python advanced_examples.py                            # 10个示例

# 快速开始
python quick_start.py                                  # 交互式向导
```

## 📋 所有参数速查

| 参数 | 说明 | 示例 |
|------|------|------|
| `keyword` | 搜索关键字（必需） | `"deep learning"` |
| `--max` | 最大数量 | `50` |
| `--output` | 输出文件 | `results.csv` |
| `--proxy` | 使用代理 | - |
| `--authors` | 作者筛选 | `"Yann LeCun,..."` |
| `--year-start` | 起始年份 | `2020` |
| `--year-end` | 结束年份 | `2023` |
| `--publishers` | 出版商 | `"IEEE,ACM"` |
| `--venues` | 会议/期刊 | `"CVPR,NeurIPS"` |
| `--min-citations` | 最小引用 | `50` |
| `--max-citations` | 最大引用 | `200` |
| `--exclude` | 排除词 | `"survey,review"` |
| `--additional-keywords` | 额外关键字 | `"neural,..."` |
| `--keyword-mode` | 组合模式 | `OR` / `AND` |
| `--config` | 配置文件 | `configs/xxx.json` |

## 📁 预设配置文件

```bash
configs/
├── top_ai_conferences.json      # AI顶会
├── cv_top_conferences.json      # CV顶会  
├── nlp_top_conferences.json     # NLP顶会
├── ml_top_conferences.json      # ML顶会
├── nature_science.json          # Nature/Science
├── ieee_acm_journals.json       # IEEE/ACM期刊
├── recent_high_impact.json      # 最近高影响力
├── breakthrough_papers.json     # 突破性论文
├── transformers_research.json   # Transformer研究
├── gan_research.json            # GAN研究
└── top_ai_authors.json          # 顶级学者
```

## 🎯 常用场景

### 场景1：最新高影响力文献

```bash
python scholar_crawler.py "deep learning" \
  --year-start 2020 --min-citations 50
```

### 场景2：顶会论文

```bash
python scholar_crawler.py "computer vision" \
  --config configs/cv_top_conferences.json
```

### 场景3：特定作者

```bash
python scholar_crawler.py "neural networks" \
  --authors "Yann LeCun,Geoffrey Hinton"
```

### 场景4：排除综述

```bash
python scholar_crawler.py "machine learning" \
  --exclude "survey,review,tutorial"
```

### 场景5：综合检索

```bash
python scholar_crawler.py "image generation" \
  --config configs/gan_research.json \
  --year-start 2020 --proxy
```

## 💡 最佳实践

1. **使用代理**：加 `--proxy` 避免限制
2. **控制数量**：`--max 50` 以内
3. **保存配置**：复杂条件用配置文件
4. **分批搜索**：不要一次搜太多

## 📊 引用量参考

| 时期 | 中等 | 高影响 | 突破性 |
|------|------|--------|--------|
| 2023+ | 30+ | 100+ | 300+ |
| 2021-2022 | 50+ | 150+ | 500+ |
| 2019-2020 | 80+ | 200+ | 800+ |
| 2017-2018 | 150+ | 400+ | 1500+ |

## 🔧 故障排除

| 问题 | 解决方案 |
|------|----------|
| 搜索失败 | 添加 `--proxy` |
| 结果太少 | 降低 `--min-citations` |
| 结果太多 | 提高 `--min-citations` 或缩小年份 |
| 配置无效 | 运行 `config_manager.py validate` |

## 📚 更多帮助

- 详细文档：`README.md`
- 高级指南：`ADVANCED_GUIDE.md`
- 示例代码：`advanced_examples.py`

---

**记住**：先试简单的，再用复杂的！🎯

