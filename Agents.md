# Agent 规则配置

本文件由 auto_update_agents.py 自动生成
最后更新: 2026-02-06 21:47:30

---

## 全局 Skills

### 文章插图生成器
**描述**: 为文章生成相关插图
**触发关键词**: 文章插图, 生成图片, 文章配图, illustration, article illustration

### 前端设计
**描述**: 创建高质量的网页组件、页面和应用程序界面，避免通用的 AI 生成美学。专注于生产级代码、视觉冲击力和独特的设计风格。
**触发关键词**: 构建组件, 创建页面, 设计界面, web界面, 前端设计, UI设计, 网页设计, component, page design, interface design, web design, frontend

### Imagen 图片生成
**描述**: Generate images using Google Gemini's image generation capabilities. Use this skill when the user needs to create, generate, or produce images for any purpose including UI mockups, icons, illustrations, diagrams, concept art, placeholder images, or visual representations.
**触发关键词**: create, generate, produce, image
**使用场景**:
- the user needs to create, generate, or produce images

### 知识文章转网页
**描述**: 将知识文章内容转换为精美的交互式网页，自动生成配图，适用于历史、科学、文化等各类知识主题
**触发关键词**: 知识文章, 网页生成, 交互式网页, 历史文章, 科学文章, 文化文章

### Skill 创建器
**描述**: 创建新的 Skill。当用户提到创建skill、新建skill、制作skill、help me create a skill、make a skill for、I want to build a skill时使用此 skill。
**触发关键词**: 创建skill, 新建skill, 制作skill, help me create a skill, make a skill for, I want to build a skill
**使用场景**:
- 最典型的使用场景

### Remotion 视频制作
**描述**: 使用 Remotion 框架以编程方式创建视频。支持 React 组件、动画、字幕、音乐可视化等。
**触发关键词**: 用代码做视频, 编程视频, React 视频, Remotion, remotion, 程序化视频, 视频生成, 视频制作, create video, video generation

### 视频下载器
**描述**: Downloads videos from YouTube and other platforms for offline viewing, editing, or archival. Handles various formats and quality options.
**触发关键词**: 下载视频, video download, YouTube下载, B站下载

### 公众号文章写作
**描述**: 公众号文章自动化写作流程。支持资料搜索、文章撰写、爆款标题生成、排版优化。当用户提到写公众号、微信文章、自媒体写作、爆款文章、内容创作时使用此 skill。
**触发关键词**: 写公众号, 微信文章, 自媒体写作, 爆款文章, 内容创作

### yt-dlp 视频下载
**描述**: Download videos from YouTube, Bilibili, Twitter, and thousands of other sites using yt-dlp. Use when the user provides a video URL and wants to download it, extract audio (MP3), download subtitles, or select video quality. Triggers on phrases like \"下载视频\", \"download video\", \"yt-dlp\", \"YouTube\", \"B站\", \"抖音\", \"提取音频\", \"extract audio\".
**触发关键词**: \"下载视频\", \"download video\", \"yt-dlp\", \"YouTube\", \"B站\", \"抖音\", \"提取音频\", \"extract audio\".

---

## 自定义 Skills

### 小红书封面生成器
**描述**: 生成小红书爆款封面图。当用户提到小红书封面、封面图生成、小红书配图、封面设计、制作封面时使用此 skill。
**触发关键词**: 小红书封面, 封面图生成, 小红书配图, 封面设计, 制作封面

---

## 使用规则

1. **关键词匹配**: 当用户输入包含某个 skill 的触发关键词时，自动调用该 skill
2. **优先级**: 如果多个 skill 匹配，选择关键词匹配度最高的
3. **上下文理解**: 根据对话上下文判断最合适的 skill
4. **用户确认**: 对于模糊的匹配，可以询问用户确认使用哪个 skill
5. **自定义优先**: 全局 Skills 和自定义 Skills 具有相同的优先级，根据关键词匹配度决定

## 工作流程

1. 用户输入请求
2. 分析请求内容，提取关键词
3. 在全局 Skills 和自定义 Skills 中搜索匹配的 skill
4. 根据匹配度和上下文选择最合适的 skill
5. 调用选定的 skill 执行任务

## 注意事项

- 确保 SKILL.md 文件格式正确，包含 YAML frontmatter
- 描述和关键词信息应准确反映 skill 的功能
- 使用场景应详细说明 skill 的适用情况
- 定期更新此文件以保持配置的准确性

---

## 版本信息

- **生成时间**: 2026-02-06 21:47:30
- **全局 Skills 数量**: 9
- **自定义 Skills 数量**: 1
- **总 Skills 数量**: 10
