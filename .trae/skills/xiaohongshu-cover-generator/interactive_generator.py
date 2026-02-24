import os
import sys
from generator import XiaohongshuCoverGenerator

class InteractiveCoverGenerator:
    def __init__(self):
        self.generator = XiaohongshuCoverGenerator()
        self.user_inputs = {}
        self.use_midjourney = False
    
    def print_header(self):
        print('\n' + '=' * 60)
        print('🎨 小红书爆款封面图生成器')
        print('=' * 60)
        print()
    
    def print_step(self, step_num, title):
        print(f'\n【步骤 {step_num}】{title}')
        print('-' * 40)
    
    def get_title(self):
        self.print_step(1, '输入文章标题')
        print('请输入您想要制作封面的文章标题：')
        print('💡 提示：标题建议控制在 20 字以内，简洁有力')
        print()
        
        while True:
            title = input('标题: ').strip()
            if title:
                if len(title) > 20:
                    print(f'⚠️  标题较长（{len(title)} 字），建议缩短，但也可以继续')
                    confirm = input('是否继续？(y/n, 默认y): ').strip().lower()
                    if confirm == 'n':
                        continue
                self.user_inputs['title'] = title
                print(f'✅ 标题: {title}')
                break
            else:
                print('❌ 标题不能为空，请重新输入')
    
    def get_keywords(self):
        self.print_step(2, '输入关键词')
        print('请输入文章的关键词（用逗号或空格分隔）：')
        print('💡 提示：关键词建议 3-5 个，有助于封面设计')
        print()
        
        while True:
            keywords_input = input('关键词: ').strip()
            if keywords_input:
                keywords = [k.strip() for k in keywords_input.replace(',', ' ').split() if k.strip()]
                if keywords:
                    if len(keywords) > 5:
                        print(f'⚠️  关键词较多（{len(keywords)} 个），建议保留 3-5 个')
                        confirm = input('是否继续？(y/n, 默认y): ').strip().lower()
                        if confirm == 'n':
                            continue
                    self.user_inputs['keywords'] = keywords
                    print(f'✅ 关键词: {", ".join(keywords)}')
                    break
                else:
                    print('❌ 请输入有效的关键词')
            else:
                print('⚠️  关键词可以为空，直接回车跳过')
                self.user_inputs['keywords'] = []
                break
    
    def get_style(self):
        self.print_step(3, '选择封面风格')
        print('请选择您喜欢的封面风格：')
        print()
        
        styles = list(self.generator.styles.keys())
        for i, style in enumerate(styles, 1):
            print(f'  {i}. {style}')
        
        print()
        print('💡 提示：不同风格适合不同类型的内容')
        print('   - 简约清新风：适合知识分享、教程类')
        print('   - 高饱和度吸睛风：适合产品推广、热点话题')
        print('   - 渐变背景风：适合科技、时尚类')
        print('   - 图文混排风：适合综合内容、品牌展示')
        print()
        
        while True:
            choice = input('请选择风格（输入数字，默认1）: ').strip()
            if not choice:
                choice = '1'
            
            try:
                style_index = int(choice) - 1
                if 0 <= style_index < len(styles):
                    self.user_inputs['style'] = styles[style_index]
                    print(f'✅ 已选择: {styles[style_index]}')
                    break
                else:
                    print(f'❌ 请输入 1-{len(styles)} 之间的数字')
            except ValueError:
                print('❌ 请输入有效的数字')
    
    def get_color_scheme(self):
        self.print_step(4, '选择配色方案')
        print('请选择您喜欢的配色方案：')
        print()
        
        schemes = list(self.generator.color_schemes.keys())
        for i, scheme in enumerate(schemes, 1):
            scheme_info = self.generator.color_schemes[scheme]
            print(f'  {i}. {scheme} - {scheme_info.get("description", "")}')
        
        print()
        print('💡 提示：配色方案会根据风格自动推荐最佳搭配')
        print()
        
        while True:
            choice = input('请选择配色（输入数字，默认1）: ').strip()
            if not choice:
                choice = '1'
            
            try:
                scheme_index = int(choice) - 1
                if 0 <= scheme_index < len(schemes):
                    self.user_inputs['color_scheme'] = schemes[scheme_index]
                    print(f'✅ 已选择: {schemes[scheme_index]}')
                    break
                else:
                    print(f'❌ 请输入 1-{len(schemes)} 之间的数字')
            except ValueError:
                print('❌ 请输入有效的数字')
    
    def get_output_format(self):
        self.print_step(5, '选择输出格式')
        print('请选择输出格式：')
        print('  1. JPG - 通用格式，文件较小')
        print('  2. PNG - 高质量格式，支持透明背景')
        print()
        
        while True:
            choice = input('请选择格式（输入数字，默认1）: ').strip()
            if not choice:
                choice = '1'
            
            if choice == '1':
                self.user_inputs['output_formatting'] = 'JPG'
                print('✅ 已选择: JPG')
                break
            elif choice == '2':
                self.user_inputs['output_formatting'] = 'PNG'
                print('✅ 已选择: PNG')
                break
            else:
                print('❌ 请输入 1 或 2')
    
    def get_midjourney_option(self):
        self.print_step(6, '选择生成方式')
        print('请选择封面图生成方式：')
        print('  1. 本地生成 - 使用 Pillow 库快速生成')
        print('  2. Midjourney - 使用 AI 生成更精美的图片')
        print()
        print('💡 提示：')
        print('   - 本地生成：速度快，无需 API Key，适合快速预览')
        print('   - Midjourney：效果更精美，需要 API Key，适合最终制作')
        print()
        
        while True:
            choice = input('请选择生成方式（输入数字，默认1）: ').strip()
            if not choice:
                choice = '1'
            
            if choice == '1':
                self.use_midjourney = False
                print('✅ 已选择: 本地生成')
                break
            elif choice == '2':
                self.use_midjourney = True
                print('✅ 已选择: Midjourney')
                
                api_key = input('请输入 Midjourney API Key (可选，直接回车使用环境变量): ').strip()
                if api_key:
                    self.user_inputs['midjourney_api_key'] = api_key
                    print('✅ API Key 已设置')
                else:
                    print('💡 将使用环境变量 MIDJOURNEY_API_KEY')
                
                break
            else:
                print('❌ 请输入 1 或 2')
    
    def confirm_and_generate(self):
        step_num = 7 if self.use_midjourney else 6
        self.print_step(step_num, '确认信息')
        print('请确认以下信息：')
        print()
        print(f'  📝 标题: {self.user_inputs["title"]}')
        if self.user_inputs['keywords']:
            print(f'  🏷️  关键词: {", ".join(self.user_inputs["keywords"])}')
        else:
            print(f'  🏷️  关键词: 无')
        print(f'  🎨 风格: {self.user_inputs["style"]}')
        print(f'  🌈 配色: {self.user_inputs["color_scheme"]}')
        print(f'  📁 格式: {self.user_inputs["output_formatting"]}')
        if self.use_midjourney:
            print(f'  🎨 生成方式: Midjourney')
        else:
            print(f'  🎨 生成方式: 本地生成')
        print()
        
        while True:
            confirm = input('确认无误？(y/n, 默认y): ').strip().lower()
            if not confirm or confirm == 'y':
                return True
            elif confirm == 'n':
                return False
            else:
                print('❌ 请输入 y 或 n')
    
    def generate_cover(self):
        print('\n' + '=' * 60)
        print('🚀 开始生成封面图...')
        print('=' * 60)
        print()
        
        if self.use_midjourney:
            api_key = self.user_inputs.get('midjourney_api_key')
            self.generator = XiaohongshuCoverGenerator(
                use_midjourney=True,
                midjourney_api_key=api_key
            )
        
        try:
            output_path = self.generator.generate(
                title=self.user_inputs['title'],
                keywords=self.user_inputs.get('keywords', []),
                style=self.user_inputs['style'],
                color_scheme=self.user_inputs['color_scheme'],
                output_format=self.user_inputs['output_formatting'],
                use_midjourney=self.use_midjourney
            )
            
            print('\n' + '=' * 60)
            print('✅ 封面图生成成功！')
            print('=' * 60)
            print()
            print(f'📁 保存路径: {output_path}')
            print()
            print('💡 提示：您可以直接在文件管理器中打开该文件夹')
            print()
            
            return output_path
        except Exception as e:
            print('\n' + '=' * 60)
            print('❌ 封面图生成失败')
            print('=' * 60)
            print()
            print(f'错误信息: {str(e)}')
            print()
            return None
    
    def run(self):
        self.print_header()
        
        print('欢迎使用小红书封面图生成器！')
        print('我将引导您一步步完成封面图的制作')
        print()
        
        input('按回车键开始...')
        
        while True:
            self.user_inputs = {}
            
            try:
                self.get_title()
                self.get_keywords()
                self.get_style()
                self.get_color_scheme()
                self.get_output_format()
                self.get_midjourney_option()
                
                if self.confirm_and_generate():
                    output_path = self.generate_cover()
                    
                    if output_path:
                        print('是否继续制作新的封面图？(y/n, 默认n): ')
                        continue_choice = input().strip().lower()
                        if continue_choice == 'y':
                            print('\n' + '=' * 60)
                            continue
                        else:
                            break
                    else:
                        print('是否重试？(y/n, 默认y): ')
                        retry_choice = input().strip().lower()
                        if retry_choice == 'n':
                            break
                else:
                    print('是否重新输入？(y/n, 默认y): ')
                    retry_choice = input().strip().lower()
                    if retry_choice == 'n':
                        break
            except KeyboardInterrupt:
                print('\n\n⚠️  用户中断操作')
                break
            except Exception as e:
                print(f'\n❌ 发生错误: {str(e)}')
                print('是否重试？(y/n, 默认y): ')
                retry_choice = input().strip().lower()
                if retry_choice == 'n':
                    break
        
        print('\n' + '=' * 60)
        print('👋 感谢使用小红书封面图生成器！')
        print('=' * 60)
        print()


def main():
    generator = InteractiveCoverGenerator()
    generator.run()


if __name__ == '__main__':
    main()
