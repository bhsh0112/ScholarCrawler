# 高级检索配置文件说明

这个目录包含预设的高级检索配置文件，可直接使用或作为模板修改。

## 📁 预设配置文件

### 1. `recent_high_impact.json`
**最近高影响力文献**
- 年份：2020年至今
- 最小引用量：50
- 排除：综述、评论类文章
- 适用场景：查找近期有影响力的原创研究

### 2. `top_ai_conferences.json`
**顶级AI会议文献**
- 包含会议：NeurIPS, ICML, ICLR, AAAI, IJCAI, CVPR, ICCV, ECCV, ACL, EMNLP
- 年份：2020年至今
- 最小引用量：20
- 适用场景：查找顶会发表的高质量论文

### 3. `nature_science.json`
**Nature/Science 顶级期刊**
- 包含期刊：Nature, Science, Nature Machine Intelligence, Nature Communications
- 年份：2018年至今
- 最小引用量：30
- 适用场景：查找顶刊发表的突破性研究

## 🚀 使用方法

### 方式1: 直接使用预设配置
```bash
# 使用最近高影响力配置搜索深度学习文献
python scholar_crawler.py "deep learning" --config configs/recent_high_impact.json

# 使用顶会配置搜索计算机视觉文献
python scholar_crawler.py "computer vision" --config configs/top_ai_conferences.json

# 使用顶刊配置搜索AI文献
python scholar_crawler.py "artificial intelligence" --config configs/nature_science.json
```

### 方式2: 自定义配置文件
1. 复制一个预设配置文件
2. 修改参数
3. 使用你的配置文件

```bash
cp configs/recent_high_impact.json configs/my_custom.json
# 编辑 my_custom.json
python scholar_crawler.py "your keyword" --config configs/my_custom.json
```

## 📝 配置文件格式

```json
{
  "description": "配置说明",
  "year_start": 2020,              // 起始年份（null表示不限）
  "year_end": 2023,                // 结束年份（null表示不限）
  "citations_min": 50,             // 最小引用量
  "citations_max": null,           // 最大引用量（null表示不限）
  "authors": ["作者1", "作者2"],   // 作者筛选（空数组表示不限）
  "publishers": ["IEEE", "ACM"],   // 出版商筛选
  "venues": ["CVPR", "NeurIPS"],   // 会议/期刊筛选
  "additional_keywords": [],       // 额外关键字
  "exclude_keywords": ["survey"],  // 排除关键字
  "keyword_mode": "OR"             // 关键字组合模式："OR" 或 "AND"
}
```

## 🎯 常见应用场景

### 场景1: 追踪最新研究进展
```json
{
  "year_start": 2023,
  "citations_min": 10,
  "exclude_keywords": ["survey", "review"]
}
```

### 场景2: 找特定领域的经典文献
```json
{
  "year_start": 2015,
  "year_end": 2020,
  "citations_min": 200,
  "venues": ["CVPR", "ICCV", "ECCV"]
}
```

### 场景3: 关注特定作者的工作
```json
{
  "authors": ["Yann LeCun", "Yoshua Bengio"],
  "year_start": 2018,
  "citations_min": 50
}
```

### 场景4: 排除特定类型的文章
```json
{
  "exclude_keywords": ["survey", "review", "tutorial", "dataset"],
  "citations_min": 30
}
```

## 💡 提示

1. **组合使用**: 可以同时设置多个筛选条件，条件之间是"与"的关系
2. **合理设置**: 条件太严格可能导致结果很少，建议逐步调整
3. **年份范围**: 近期文献引用量可能较低，注意调整 `citations_min`
4. **会议/期刊名**: 尽量使用缩写（如 CVPR 而非 IEEE Conference on...）
5. **作者名**: 使用作者的常用署名形式

## 🔧 高级技巧

### 技巧1: 组合命令行参数和配置文件
```bash
# 配置文件提供基础设置，命令行参数可覆盖
python scholar_crawler.py "deep learning" \
  --config configs/top_ai_conferences.json \
  --year-start 2023 \
  --max 100
```

### 技巧2: 批量使用不同配置
```bash
# 使用相同关键字但不同配置搜索
for config in configs/*.json; do
  python scholar_crawler.py "transformer" --config "$config"
done
```

### 技巧3: 创建专题配置
为特定研究主题创建配置文件：
- `configs/transformers_nlp.json` - Transformer在NLP的应用
- `configs/gan_cv.json` - GAN在计算机视觉的应用
- `configs/rl_robotics.json` - 强化学习在机器人的应用

## 📚 参考

更多信息请参考主 README.md 文档。

