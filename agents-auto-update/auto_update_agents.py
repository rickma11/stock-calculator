import os
import json
import time
import re
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

GLOBAL_SKILLS_DIR = Path("C:/Users/rickma/.trae-cn/skills")
CUSTOM_SKILLS_DIR = Path("F:/skill/.trae/skills")
AGENTS_FILE = Path("F:/skill/Agents.md")

SKILL_TRANSLATIONS = {
    'article-illustration-generator': {
        'name': '文章插图生成器',
        'description': '为文章生成相关插图',
        'default_keywords': ['文章插图', '生成图片', '文章配图', 'illustration', 'article illustration']
    },
    'frontend-design': {
        'name': '前端设计',
        'description': '创建高质量的网页组件、页面和应用程序界面，避免通用的 AI 生成美学。专注于生产级代码、视觉冲击力和独特的设计风格。',
        'default_keywords': ['构建组件', '创建页面', '设计界面', 'web界面', '前端设计', 'UI设计', '网页设计', 'component', 'page design', 'interface design', 'web design', 'frontend']
    },
    'imagen': {
        'name': 'Imagen 图片生成',
        'description': '使用 Google Gemini 生成图片',
        'default_keywords': ['生成图片', '创建图片', '图片生成', 'UI设计', '图标', '插图', '图表', 'image generation']
    },
    'knowledge-2-web': {
        'name': '知识文章转网页',
        'description': '将知识文章内容转换为精美的交互式网页，自动生成配图，适用于历史、科学、文化等各类知识主题',
        'default_keywords': ['知识文章', '网页生成', '交互式网页', '历史文章', '科学文章', '文化文章']
    },
    'qiuzhi-skill-creator': {
        'name': 'Skill 创建器',
        'description': '创建新的 Skill',
        'default_keywords': ['创建skill', '新建skill', '制作skill', 'help me create a skill', 'make a skill for', 'I want to build a skill']
    },
    'remotion-video': {
        'name': 'Remotion 视频制作',
        'description': '使用 Remotion 框架以编程方式创建视频。支持 React 组件、动画、字幕、音乐可视化等。',
        'default_keywords': ['用代码做视频', '编程视频', 'React 视频', 'Remotion', 'remotion', '程序化视频', '视频生成', '视频制作', 'create video', 'video generation']
    },
    'video-downloader': {
        'name': '视频下载器',
        'description': '从 YouTube 和其他平台下载视频',
        'default_keywords': ['下载视频', 'video download', 'YouTube下载', 'B站下载']
    },
    'wechat-article-writer': {
        'name': '公众号文章写作',
        'description': '公众号文章自动化写作流程',
        'default_keywords': ['写公众号', '微信文章', '自媒体写作', '爆款文章', '内容创作']
    },
    'yt-dlp-downloader': {
        'name': 'yt-dlp 视频下载',
        'description': '使用 yt-dlp 下载视频',
        'default_keywords': ['下载视频', 'download video', 'yt-dlp', 'YouTube', 'B站', '抖音', '提取音频', 'extract audio']
    },
    'xiaohongshu-cover-generator': {
        'name': '小红书封面生成器',
        'description': '生成小红书爆款封面图',
        'default_keywords': ['小红书封面', '封面图生成', '小红书配图', '封面设计', '制作封面', 'xiaohongshu cover', 'cover generator']
    }
}

def parse_skill_md(skill_dir):
    skill_md = skill_dir / "SKILL.md"
    
    if not skill_md.exists():
        return None
    
    try:
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
        
        description = ""
        keywords = []
        use_cases = []
        
        lines = content.split('\n')
        
        if lines[0].strip() == '---':
            in_frontmatter = True
            frontmatter_lines = []
            
            for line in lines[1:]:
                if line.strip() == '---':
                    in_frontmatter = False
                    break
                if in_frontmatter:
                    frontmatter_lines.append(line)
            
            frontmatter_text = '\n'.join(frontmatter_lines)
            
            desc_match = re.search(r'description:\s*"(.+)"', frontmatter_text, re.IGNORECASE | re.DOTALL)
            if desc_match:
                description = desc_match.group(1).strip().replace('\n', ' ')
            else:
                desc_match = re.search(r'description:\s*(.+)', frontmatter_text, re.IGNORECASE)
                if desc_match:
                    description = desc_match.group(1).strip().strip('"\'')
        
        if not description:
            for line in lines:
                if line.strip() and not line.startswith('#') and not line.startswith('---'):
                    description = line.strip()
                    break
        
        for line in lines:
            if '关键词' in line or 'keyword' in line.lower():
                if '：' in line or ':' in line:
                    parts = line.split('：') if '：' in line else line.split(':')
                    if len(parts) > 1:
                        keywords_str = parts[1].strip()
                        keywords = [k.strip() for k in keywords_str.split('、') if k.strip()]
            
            if '使用场景' in line or 'use case' in line.lower() or 'when to use' in line.lower():
                if '：' in line or ':' in line:
                    parts = line.split('：') if '：' in line else line.split(':')
                    if len(parts) > 1:
                        use_case = parts[1].strip()
                        use_cases.append(use_case)
        
        if 'Use this skill when' in content or 'Automatically activate' in content:
            use_case_match = re.search(r'Use this skill when (.+)', content, re.IGNORECASE)
            if use_case_match:
                use_cases.append(use_case_match.group(1).strip())
        
        if '当用户提到' in description:
            keyword_match = re.search(r'当用户提到(.+?)时', description)
            if keyword_match:
                keywords_str = keyword_match.group(1).strip()
                keywords = [k.strip() for k in keywords_str.split('、') if k.strip()]
        
        if 'Triggers on phrases like' in description:
            keyword_match = re.search(r'Triggers on phrases like (.+)', description)
            if keyword_match:
                keywords_str = keyword_match.group(1).strip()
                keywords = [k.strip() for k in keywords_str.split(',') if k.strip()]
        
        if 'Use this skill when' in description:
            keyword_match = re.search(r'Use this skill when (.+)', description)
            if keyword_match:
                keywords_str = keyword_match.group(1).strip()
                extracted_keywords = []
                
                if 'create' in keywords_str.lower():
                    extracted_keywords.append('create')
                if 'generate' in keywords_str.lower():
                    extracted_keywords.append('generate')
                if 'produce' in keywords_str.lower():
                    extracted_keywords.append('produce')
                if 'image' in keywords_str.lower():
                    extracted_keywords.append('image')
                if 'download' in keywords_str.lower():
                    extracted_keywords.append('download')
                if 'video' in keywords_str.lower():
                    extracted_keywords.append('video')
                if 'article' in keywords_str.lower():
                    extracted_keywords.append('article')
                if 'write' in keywords_str.lower():
                    extracted_keywords.append('write')
                
                if extracted_keywords:
                    keywords.extend(extracted_keywords)
        
        skill_name = skill_dir.name
        
        if skill_name in SKILL_TRANSLATIONS:
            translation = SKILL_TRANSLATIONS[skill_name]
            if not description or len(description) < 50:
                description = translation['description']
            if not keywords:
                keywords = translation['default_keywords']
        
        if not description:
            description = "暂无描述"
        
        return {
            'name': skill_name,
            'description': description,
            'keywords': keywords,
            'use_cases': use_cases
        }
    except Exception as e:
        print(f"解析 {skill_dir.name} 失败: {e}")
        return None

def scan_skills_in_directory(directory):
    skills_info = []
    
    if not directory.exists():
        return skills_info
    
    for skill_dir in directory.iterdir():
        if skill_dir.is_dir():
            skill_info = parse_skill_md(skill_dir)
            if skill_info:
                skills_info.append(skill_info)
    
    return skills_info

def scan_all_skills():
    global_skills = scan_skills_in_directory(GLOBAL_SKILLS_DIR)
    custom_skills = scan_skills_in_directory(CUSTOM_SKILLS_DIR)
    
    return {
        'global': global_skills,
        'custom': custom_skills
    }

def generate_agents_md(skills_data):
    content = "# Agent 规则配置\n\n"
    content += "本文件由 auto_update_agents.py 自动生成\n"
    content += f"最后更新: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    content += "---\n\n"
    
    global_skills = skills_data['global']
    custom_skills = skills_data['custom']
    
    if global_skills:
        content += "## 全局 Skills\n\n"
        for skill in global_skills:
            skill_name = skill['name']
            display_name = SKILL_TRANSLATIONS.get(skill_name, {}).get('name', skill_name)
            content += f"### {display_name}\n"
            content += f"**描述**: {skill['description']}\n"
            if skill['keywords']:
                content += f"**触发关键词**: {', '.join(skill['keywords'])}\n"
            if skill['use_cases']:
                content += f"**使用场景**:\n"
                for use_case in skill['use_cases']:
                    content += f"- {use_case}\n"
            content += "\n"
        
        content += "---\n\n"
    
    if custom_skills:
        content += "## 自定义 Skills\n\n"
        for skill in custom_skills:
            skill_name = skill['name']
            display_name = SKILL_TRANSLATIONS.get(skill_name, {}).get('name', skill_name)
            content += f"### {display_name}\n"
            content += f"**描述**: {skill['description']}\n"
            if skill['keywords']:
                content += f"**触发关键词**: {', '.join(skill['keywords'])}\n"
            if skill['use_cases']:
                content += f"**使用场景**:\n"
                for use_case in skill['use_cases']:
                    content += f"- {use_case}\n"
            content += "\n"
        
        content += "---\n\n"
    
    content += "## 使用规则\n\n"
    content += "1. **关键词匹配**: 当用户输入包含某个 skill 的触发关键词时，自动调用该 skill\n"
    content += "2. **优先级**: 如果多个 skill 匹配，选择关键词匹配度最高的\n"
    content += "3. **上下文理解**: 根据对话上下文判断最合适的 skill\n"
    content += "4. **用户确认**: 对于模糊的匹配，可以询问用户确认使用哪个 skill\n"
    content += "5. **自定义优先**: 全局 Skills 和自定义 Skills 具有相同的优先级，根据关键词匹配度决定\n\n"
    
    content += "## 工作流程\n\n"
    content += "1. 用户输入请求\n"
    content += "2. 分析请求内容，提取关键词\n"
    content += "3. 在全局 Skills 和自定义 Skills 中搜索匹配的 skill\n"
    content += "4. 根据匹配度和上下文选择最合适的 skill\n"
    content += "5. 调用选定的 skill 执行任务\n\n"
    
    content += "## 注意事项\n\n"
    content += "- 确保 SKILL.md 文件格式正确，包含 YAML frontmatter\n"
    content += "- 描述和关键词信息应准确反映 skill 的功能\n"
    content += "- 使用场景应详细说明 skill 的适用情况\n"
    content += "- 定期更新此文件以保持配置的准确性\n\n"
    
    content += "---\n\n"
    content += "## 版本信息\n\n"
    content += f"- **生成时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    content += f"- **全局 Skills 数量**: {len(global_skills)}\n"
    content += f"- **自定义 Skills 数量**: {len(custom_skills)}\n"
    content += f"- **总 Skills 数量**: {len(global_skills) + len(custom_skills)}\n"
    
    return content

def update_agents_md():
    print("开始扫描 skills...")
    skills_data = scan_all_skills()
    
    global_skills = skills_data['global']
    custom_skills = skills_data['custom']
    
    if not global_skills and not custom_skills:
        print("未找到任何 skills")
        return False
    
    print(f"找到 {len(global_skills)} 个全局 Skills")
    print(f"找到 {len(custom_skills)} 个自定义 Skills")
    
    content = generate_agents_md(skills_data)
    
    try:
        with open(AGENTS_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 成功更新 {AGENTS_FILE}")
        return True
    except Exception as e:
        print(f"❌ 更新失败: {e}")
        return False

class SkillEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            print(f"📁 检测到新目录: {event.src_path}")
            time.sleep(1)
            update_agents_md()
    
    def on_modified(self, event):
        if event.is_directory:
            print(f"📝 检测到目录修改: {event.src_path}")
            time.sleep(1)
            update_agents_md()
    
    def on_deleted(self, event):
        if event.is_directory:
            print(f"🗑️  检测到目录删除: {event.src_path}")
            time.sleep(1)
            update_agents_md()

def start_monitor():
    print(f"开始监控全局 skills 目录: {GLOBAL_SKILLS_DIR}")
    print(f"开始监控自定义 skills 目录: {CUSTOM_SKILLS_DIR}")
    print(f"目标文件: {AGENTS_FILE}")
    print("按 Ctrl+C 停止监控\n")
    
    update_agents_md()
    
    event_handler = SkillEventHandler()
    observer = Observer()
    
    if GLOBAL_SKILLS_DIR.exists():
        observer.schedule(event_handler, str(GLOBAL_SKILLS_DIR), recursive=True)
    
    if CUSTOM_SKILLS_DIR.exists() and CUSTOM_SKILLS_DIR != GLOBAL_SKILLS_DIR:
        observer.schedule(event_handler, str(CUSTOM_SKILLS_DIR), recursive=True)
    
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n停止监控")
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "once":
        update_agents_md()
    else:
        start_monitor()
