# Agents.dm 自动更新工具使用指南

## 功能说明

这个工具可以自动监控 skills 目录的变化，并在以下情况自动更新 `F:\skill\agents.dm` 文件：

- ✅ 安装新的全局 skill
- ✅ 创建自定义 skill  
- ✦ 更新现有 skill（修改 SKILL.md）
- ✦ 删除 skill

## 安装依赖

```bash
pip install watchdog
```

## 使用方法

### 方法1：使用批处理文件（推荐）

双击运行 `run_auto_update.bat`，然后选择：

1. **单次更新**：扫描一次所有 skills 并更新 agents.dm，然后退出
2. **持续监控**：自动监控 skills 目录变化，实时更新 agents.dm

### 方法2：直接运行 Python 脚本

**单次更新**：
```bash
python f:\skill\agents-auto-update\auto_update_agents.py once
```

**持续监控**：
```bash
python f:\skill\agents-auto-update\auto_update_agents.py
```

## 工作原理

1. **扫描 skills 目录**：读取 `C:/Users/rickma/.trae-cn/skills/` 下的所有 skill 目录
2. **解析 SKILL.md**：从每个 skill 的 SKILL.md 文件中提取：
   - Skill 名称（目录名）
   - 描述（第一行非注释内容）
   - 触发关键词（从内容中提取）
3. **生成 agents.dm**：将所有 skill 信息格式化为 agents.dm 文件
4. **监控变化**：使用 watchdog 监控目录变化，自动触发更新

## 文件结构

```
f:/skill/
├── auto_update_agents.py    # 主脚本
├── run_auto_update.bat       # 批处理启动文件
├── AUTO_UPDATE_GUIDE.md      # 使用指南（本文件）
└── agents.dm                 # 自动生成的配置文件
```

## 输出示例

生成的 `agents.dm` 文件格式：

```markdown
# Agent 规则配置

本文件由 auto_update_agents.py 自动生成
最后更新: 2025-02-04 10:30:00

---

## 全局 Skills

### imagen
**描述**: Generate images using Google Gemini's image generation capabilities
**触发关键词**: 生成图片, 创建图片, 图片生成

### wechat-article-writer
**描述**: 公众号文章自动化写作流程
**触发关键词**: 写公众号, 微信文章, 自媒体写作

---

## 使用规则

1. **关键词匹配**: 当用户输入包含某个 skill 的触发关键词时，自动调用该 skill
2. **优先级**: 如果多个 skill 匹配，选择关键词匹配度最高的
3. **上下文理解**: 根据对话上下文判断最合适的 skill
4. **用户确认**: 对于模糊的匹配，可以询问用户确认使用哪个 skill
```

## 注意事项

1. **SKILL.md 格式**：确保每个 skill 目录下都有 SKILL.md 文件
2. **关键词提取**：脚本会从 SKILL.md 内容中提取关键词，确保格式正确
3. **权限问题**：确保有写入 `F:\skill\agents.dm` 的权限
4. **监控性能**：持续监控会占用少量系统资源，不需要时可以关闭

## 故障排除

### 问题：找不到 skills 目录

**解决方案**：检查 `C:/Users/rickma/.trae-cn/skills/` 路径是否正确

### 问题：无法写入 agents.dm

**解决方案**：
- 检查文件权限
- 确保 F:\skill 目录存在
- 以管理员身份运行

### 问题：watchdog 未安装

**解决方案**：运行 `pip install watchdog`

## 高级配置

如需修改路径，编辑 `auto_update_agents.py` 中的配置：

```python
SKILLS_DIR = Path("C:/Users/rickma/.trae-cn/skills")  # Skills 源目录
AGENTS_FILE = Path("F:/skill/agents.dm")              # 目标文件
```

## 版本信息

- **版本**: 1.0
- **创建日期**: 2025-02-04
- **维护者**: AI Assistant
