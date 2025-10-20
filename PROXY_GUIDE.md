# 代理设置指南 🌐

## 为什么需要代理？

Google Scholar 会限制频繁访问，使用代理可以：
- ✅ 避免IP被封禁
- ✅ 提高搜索成功率
- ✅ 绕过访问限制
- ✅ 更稳定的连接

---

## 方式一：使用内置免费代理（最简单）

### 使用方法

只需在命令后添加 `--proxy` 参数：

```bash
python scholar_crawler.py "deep learning" --proxy
```

或者与其他参数组合：

```bash
python scholar_crawler.py "deep learning" \
  --config configs/cv_top_conferences.json \
  --proxy
```

### 内置代理说明

- 使用 scholarly 库的免费代理功能
- 自动轮换代理IP
- 无需额外配置
- 可能不太稳定（免费代理的通病）

### 示例

```bash
# 基础搜索 + 代理
python scholar_crawler.py "computer vision" --proxy --max 30

# 高级检索 + 代理
python scholar_crawler.py "deep learning" \
  --year-start 2020 \
  --min-citations 50 \
  --proxy
```

---

## 方式二：使用自定义HTTP代理

如果你有自己的代理服务器（如Clash、V2Ray、Shadowsocks等），可以配置自定义代理。

### 步骤1：修改 config.py

打开 `/Users/shanhao/Desktop/script/scholar_crawler/config.py`，找到 `CUSTOM_PROXY` 部分：

```python
# 代理配置（如果使用自定义代理）
CUSTOM_PROXY = {
    'http': None,   # 例如: 'http://127.0.0.1:7890'
    'https': None,  # 例如: 'http://127.0.0.1:7890'
}
```

修改为你的代理地址：

```python
# 代理配置
CUSTOM_PROXY = {
    'http': 'http://127.0.0.1:7890',    # 你的HTTP代理地址
    'https': 'http://127.0.0.1:7890',   # 你的HTTPS代理地址
}
```

**常见代理端口**：
- Clash：`7890`
- V2Ray：`10809` 或 `1080`
- Shadowsocks：`1080`
- 其他：查看你的代理软件设置

### 步骤2：修改 scholar_crawler.py

目前代码使用的是 scholarly 内置代理。如果要使用系统代理，需要稍微修改代码。

创建一个增强版本 `scholar_crawler_enhanced.py`：

```python
import os

# 在文件开头添加环境变量设置
def setup_system_proxy():
    """设置系统代理环境变量"""
    proxy_url = "http://127.0.0.1:7890"  # 修改为你的代理地址
    
    os.environ['HTTP_PROXY'] = proxy_url
    os.environ['HTTPS_PROXY'] = proxy_url
    os.environ['http_proxy'] = proxy_url
    os.environ['https_proxy'] = proxy_url
    
    print(f"✓ 系统代理已设置: {proxy_url}")

# 在 main() 函数开始处调用
def main():
    # 如果需要使用系统代理，取消下面的注释
    # setup_system_proxy()
    
    # ... 其余代码保持不变
```

---

## 方式三：使用环境变量（推荐）

这是最灵活的方式，不需要修改代码。

### macOS/Linux

```bash
# 临时设置（仅当前终端有效）
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890

# 然后运行爬虫
python scholar_crawler.py "deep learning" --config configs/cv_top_conferences.json

# 或者一行命令
HTTP_PROXY=http://127.0.0.1:7890 HTTPS_PROXY=http://127.0.0.1:7890 \
python scholar_crawler.py "deep learning" --proxy
```

### 永久设置（可选）

编辑 `~/.zshrc` 或 `~/.bash_profile`：

```bash
# 添加以下行
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890

# 保存后执行
source ~/.zshrc
```

### Windows

```cmd
# CMD
set HTTP_PROXY=http://127.0.0.1:7890
set HTTPS_PROXY=http://127.0.0.1:7890

# PowerShell
$env:HTTP_PROXY="http://127.0.0.1:7890"
$env:HTTPS_PROXY="http://127.0.0.1:7890"

# 然后运行
python scholar_crawler.py "deep learning" --proxy
```

---

## 方式四：检查并使用系统代理

### 查看当前代理设置

```bash
# macOS/Linux
echo $HTTP_PROXY
echo $HTTPS_PROXY

# 或者
env | grep -i proxy
```

### 如果已配置系统代理

直接运行即可，Python会自动使用系统代理：

```bash
python scholar_crawler.py "deep learning" --config configs/cv_top_conferences.json
```

---

## 🔧 针对你当前问题的解决方案

根据你的错误信息，问题不仅是代理，还有**筛选条件太严格**。

### 问题分析

```
⚠ 已搜索 150 篇，但只找到 0 篇符合条件的文献
✓ 成功获取 0 篇文献（筛选掉 150 篇不符合条件的文献）
```

这说明：
1. **搜索成功**了（找到150篇）
2. **全部被筛选条件过滤掉**了

### 解决方案1：放宽筛选条件

查看你的配置 `cv_top_conferences.json`：

```json
{
  "year_start": 2020,
  "citations_min": 30,
  "venues": ["CVPR", "ICCV", "ECCV"],
  "exclude_keywords": ["survey", "review"]
}
```

问题可能是：
- ✗ venues 筛选太严格（必须包含这些会议名）
- ✗ citations_min 可能太高（新文献引用少）

**修改建议**：

创建新配置 `cv_top_conferences_relaxed.json`：

```json
{
  "description": "CV顶会配置（放宽版）",
  "year_start": 2020,
  "year_end": null,
  "citations_min": 10,  // 降低到10
  "citations_max": null,
  "authors": [],
  "publishers": [],
  "venues": [],  // 先不限制venue，看看结果
  "additional_keywords": ["CVPR", "ICCV", "ECCV"],  // 改为额外关键字
  "exclude_keywords": [],  // 先不排除
  "keyword_mode": "OR"
}
```

### 解决方案2：逐步添加条件

```bash
# 第一步：基础搜索，不加限制
python scholar_crawler.py "deep learning computer vision" --max 20

# 第二步：添加年份限制
python scholar_crawler.py "deep learning computer vision" \
  --year-start 2020 --max 20

# 第三步：添加引用量（从低开始）
python scholar_crawler.py "deep learning computer vision" \
  --year-start 2020 --min-citations 10 --max 20

# 第四步：如果结果合适，再添加其他条件
```

### 解决方案3：使用代理 + 放宽条件

```bash
# 推荐方式
python scholar_crawler.py "deep learning computer vision" \
  --year-start 2020 \
  --min-citations 10 \
  --max 30 \
  --proxy
```

---

## 📋 完整示例：从零开始

### 步骤1：设置代理（选择一种方式）

**方式A：使用内置代理（最简单）**
```bash
# 只需加 --proxy 参数，无需其他设置
```

**方式B：使用Clash等代理软件**
```bash
# 1. 确保代理软件运行中
# 2. 查看代理端口（通常是7890）
# 3. 设置环境变量
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890
```

### 步骤2：测试网络

```bash
# 测试代理是否工作
curl -x http://127.0.0.1:7890 https://www.google.com

# 或者测试Python
python -c "import requests; print(requests.get('https://scholar.google.com', proxies={'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}).status_code)"
```

### 步骤3：运行爬虫（放宽条件）

```bash
# 基础搜索 + 代理
python scholar_crawler.py "deep learning computer vision" \
  --max 20 \
  --proxy

# 如果成功，再添加条件
python scholar_crawler.py "deep learning computer vision" \
  --year-start 2020 \
  --min-citations 10 \
  --max 30 \
  --proxy
```

---

## ⚠️ 常见问题

### Q1: 使用 --proxy 后仍然失败

**可能原因**：
- 免费代理不稳定
- Google Scholar 封禁了代理IP
- 网络问题

**解决方案**：
1. 使用自己的代理（Clash/V2Ray）
2. 减少请求频率（`--max 20`）
3. 多试几次

### Q2: 所有文献都被筛掉

**原因**：筛选条件太严格

**解决方案**：
1. 降低 `citations_min`（从50降到10）
2. 移除 `venues` 限制
3. 清空 `exclude_keywords`
4. 扩大年份范围

### Q3: 代理设置后无效

**检查清单**：
```bash
# 1. 检查代理软件是否运行
ps aux | grep -i clash  # 或你的代理软件名

# 2. 检查端口是否正确
netstat -an | grep 7890  # 或你的代理端口

# 3. 检查环境变量
echo $HTTP_PROXY
echo $HTTPS_PROXY

# 4. 测试代理连接
curl -x http://127.0.0.1:7890 https://www.google.com
```

### Q4: urllib3 警告信息

```
NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+
```

**这是警告，不是错误**，不影响使用。如果想消除：

```bash
pip install urllib3==1.26.15
```

---

## 🎯 针对你的情况的具体建议

基于你的错误信息，我建议：

### 方案A：放宽条件 + 内置代理（推荐）

```bash
python scholar_crawler.py "deep learning computer vision" \
  --year-start 2020 \
  --min-citations 10 \
  --max 30 \
  --proxy
```

### 方案B：使用系统代理（如果有Clash等）

```bash
# 1. 确保Clash运行中，端口通常是7890
# 2. 设置环境变量
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890

# 3. 运行（放宽条件）
python scholar_crawler.py "deep learning computer vision" \
  --year-start 2020 \
  --min-citations 10 \
  --max 30
```

### 方案C：分步测试

```bash
# 步骤1：最简单的搜索
python scholar_crawler.py "deep learning" --max 10 --proxy

# 步骤2：如果成功，添加年份
python scholar_crawler.py "deep learning" --year-start 2020 --max 10 --proxy

# 步骤3：逐步添加其他条件
python scholar_crawler.py "deep learning" \
  --year-start 2020 \
  --min-citations 10 \
  --max 20 \
  --proxy
```

---

## 📝 推荐的配置文件

创建 `configs/cv_relaxed.json`：

```json
{
  "description": "CV相关文献（放宽版）",
  "year_start": 2020,
  "year_end": null,
  "citations_min": 10,
  "citations_max": null,
  "authors": [],
  "publishers": [],
  "venues": [],
  "additional_keywords": [],
  "exclude_keywords": [],
  "keyword_mode": "OR"
}
```

使用：

```bash
python scholar_crawler.py "deep learning computer vision" \
  --config configs/cv_relaxed.json \
  --proxy
```

---

## 💡 最佳实践

1. **总是使用代理**：添加 `--proxy` 参数
2. **从宽到窄**：先放宽条件，看到结果后再收紧
3. **控制数量**：`--max 20-30` 即可，不要太多
4. **耐心等待**：每篇文献之间有2秒延迟
5. **多次尝试**：网络问题可能导致偶尔失败

---

## 🔍 调试技巧

```bash
# 1. 测试最简单的搜索
python scholar_crawler.py "deep learning" --max 5

# 2. 如果失败，加代理
python scholar_crawler.py "deep learning" --max 5 --proxy

# 3. 如果还失败，检查网络
ping scholar.google.com

# 4. 检查是否被限制
curl https://scholar.google.com
```

---

希望这能帮到你！如果还有问题，请告诉我具体的错误信息。🚀

