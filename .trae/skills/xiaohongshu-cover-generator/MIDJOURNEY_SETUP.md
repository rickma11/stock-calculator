# Midjourney 集成配置指南

## 概述

小红书封面图生成器现已支持 Midjourney AI 图片生成功能，可以根据标题、关键词、风格和配色方案自动生成精美的封面图。

## 功能对比

| 特性 | 本地生成 | Midjourney 生成 |
|------|---------|----------------|
| 速度 | 快速（秒级） | 较慢（分钟级） |
| 效果 | 基础设计 | AI 精美设计 |
| 成本 | 免费 | 需要付费 API |
| 灵活性 | 有限 | 高度灵活 |
| 适用场景 | 快速预览 | 最终制作 |

## 配置方法

### 方法 1：使用环境变量（推荐）

在系统环境变量中设置 Midjourney API Key：

**Windows (PowerShell)**：
```powershell
$env:MIDJOURNEY_API_KEY="your_api_key_here"
```

**Windows (CMD)**：
```cmd
set MIDJOURNEY_API_KEY=your_api_key_here
```

**Linux/Mac**：
```bash
export MIDJOURNEY_API_KEY=your_api_key_here
```

### 方法 2：交互式输入

运行交互式生成器时，选择 Midjourney 生成方式，系统会提示输入 API Key：

```bash
python interactive_generator.py
```

选择 `2. Midjourney` 后，输入您的 API Key。

### 方法 3：代码中传入

在 Python 代码中直接传入 API Key：

```python
from generator import XiaohongshuCoverGenerator

generator = XiaohongshuCoverGenerator(
    use_midjourney=True,
    midjourney_api_key='your_api_key_here'
)

output_path = generator.generate(
    title='欧啊欧春节粉丝抽奖活动',
    keywords=['抽一个幸运粉丝获得', '拜仁穆勒签名卡砖'],
    style='高饱和度吸睛风',
    color_scheme='橙红渐变',
    use_midjourney=True
)
```

## 获取 Midjourney API Key

1. 访问 [Midjourney 官网](https://www.midjourney.com/)
2. 注册账号并登录
3. 在账户设置中找到 API Key
4. 复制 API Key 并保存

## 使用示例

### 交互式使用

```bash
python interactive_generator.py
```

按照提示操作：
1. 输入标题
2. 输入关键词
3. 选择风格
4. 选择配色方案
5. 选择输出格式
6. **选择生成方式（本地生成 或 Midjourney）**
7. 如果选择 Midjourney，输入 API Key
8. 确认并生成

### Python API 使用

```python
from generator import XiaohongshuCoverGenerator

# 使用 Midjourney 生成
generator = XiaohongshuCoverGenerator(
    use_midjourney=True,
    midjourney_api_key='your_api_key_here'
)

output_path = generator.generate(
    title='10个提升效率的Python技巧',
    keywords=['Python', '效率', '编程'],
    style='简约清新风',
    color_scheme='紫色渐变',
    output_format='PNG',
    use_midjourney=True
)

print(f'封面图已生成: {output_path}')
```

### 批量生成

```python
from generator import XiaohongshuCoverGenerator

generator = XiaohongshuCoverGenerator(
    use_midjourney=True,
    midjourney_api_key='your_api_key_here'
)

titles = [
    {
        'title': '标题1',
        'keywords': ['关键词1'],
        'style': '简约清新风',
        'color_scheme': '紫色渐变'
    },
    {
        'title': '标题2',
        'keywords': ['关键词2'],
        'style': '高饱和度吸睛风',
        'color_scheme': '粉色渐变'
    }
]

for item in titles:
    output_path = generator.generate(
        title=item['title'],
        keywords=item['keywords'],
        style=item['style'],
        color_scheme=item['color_scheme'],
        use_midjourney=True
    )
    print(f'生成成功: {output_path}')
```

## Midjourney 提示词生成逻辑

系统会根据以下信息自动生成 Midjourney 提示词：

### 基础结构

```
Xiaohongshu cover design, {标题}, {关键词}, {风格描述}, {配色描述}, 1080x1440 aspect ratio, vertical orientation, social media cover, high quality, detailed, 8k
```

### 风格描述映射

| 风格 | Midjourney 描述 |
|--------|----------------|
| 简约清新风 | minimalist design, clean and fresh, simple layout, elegant typography, white space, modern aesthetic |
| 高饱和度吸睛风 | vibrant colors, eye-catching design, bold typography, energetic, dynamic composition, high contrast |
| 渐变背景风 | gradient background, modern tech style, sleek design, smooth transitions, contemporary |
| 图文混排风 | mixed media layout, creative composition, visual storytelling, artistic arrangement, trendy design |

### 配色方案映射

| 配色方案 | Midjourney 描述 |
|---------|----------------|
| 紫色渐变 | purple gradient, mystical purple, elegant violet |
| 蓝色渐变 | blue gradient, professional blue, fresh cyan |
| 橙红渐变 | orange-red gradient, warm orange, energetic red |
| 粉色渐变 | pink gradient, soft pink, rose color |
| 绿色渐变 | green gradient, fresh green, natural emerald |
| 简约黑白 | black and white, monochrome, minimalist black white |
| 深紫渐变 | deep purple gradient, royal purple, mysterious violet |
| 青色渐变 | cyan gradient, teal, aqua blue |
| 玫瑰渐变 | rose gradient, crimson, romantic red |
| 金色渐变 | gold gradient, warm gold, luxury amber |

## 错误处理

### API Key 未设置

如果未设置 API Key，系统会：
1. 显示警告信息
2. 自动切换到本地生成模式
3. 继续生成封面图

### API 请求失败

如果 Midjourney API 请求失败，系统会：
1. 显示错误信息
2. 自动切换到本地生成模式
3. 继续生成封面图

### 网络超时

如果网络请求超时，系统会：
1. 显示超时错误
2. 自动切换到本地生成模式
3. 继续生成封面图

## 注意事项

1. **API Key 安全**
   - 不要将 API Key 提交到代码仓库
   - 使用环境变量或配置文件存储
   - 定期更换 API Key

2. **生成时间**
   - Midjourney 生成需要较长时间（通常 1-3 分钟）
   - 请耐心等待
   - 可以使用本地生成进行快速预览

3. **API 配额**
   - 注意 Midjourney API 的调用限制
   - 避免短时间内大量调用
   - 合理规划批量生成任务

4. **图片质量**
   - Midjourney 生成的图片质量更高
   - 适合最终发布使用
   - 本地生成适合快速预览和测试

## 故障排除

### 问题：无法连接到 Midjourney API

**解决方案**：
1. 检查网络连接
2. 确认 API Key 正确
3. 检查 API 服务状态
4. 尝试使用本地生成模式

### 问题：生成的图片不符合预期

**解决方案**：
1. 调整标题和关键词
2. 尝试不同的风格和配色
3. 使用更具体的描述
4. 查看生成的提示词并手动优化

### 问题：生成速度太慢

**解决方案**：
1. 使用本地生成模式进行快速预览
2. 确认满意后再使用 Midjourney 生成
3. 减少同时生成的任务数量

## 更新日志

### v2.1 (2026-02-06)
- ✅ 新增 Midjourney API 集成
- ✅ 自动生成 Midjourney 提示词
- ✅ 支持交互式选择生成方式
- ✅ 智能错误处理和降级
- ✅ 完整的配置文档

### v2.0 (2026-02-06)
- ✅ 交互式引导功能
- ✅ 丰富的视觉装饰元素
- ✅ 多种风格和配色方案

### v1.0 (2026-02-06)
- ✅ 基础封面图生成功能
