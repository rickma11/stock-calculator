import os
import json
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
from typing import Optional

class XiaohongshuCoverGenerator:
    def __init__(self, use_midjourney: bool = False, midjourney_api_key: Optional[str] = None):
        self.width = 1080
        self.height = 1440
        self.output_dir = os.path.join(os.path.dirname(__file__), 'output')
        self.templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.use_midjourney = use_midjourney
       
        
        if use_midjourney:
            try:
                from midjourney_client import MidjourneyClient
                self.midjourney_client = MidjourneyClient(api_key=midjourney_api_key)
                print('✅ Midjourney 客户端已初始化')
            except Exception as e:
                print(f'⚠️  Midjourney 初始化失败: {str(e)}')
                print('💡 将使用本地生成模式')
                self.use_midjourney = False
                self.midjourney_client = None
        else:
            self.midjourney_client = None
        
        self.color_schemes = {
            '紫色渐变': {
                'primary': '#8B5CF6',
                'secondary': '#A78BFA',
                'accent': '#C4B5FD',
                'text': '#FFFFFF',
                'shadow': '#6D28D9'
            },
            '蓝色渐变': {
                'primary': '#3B82F6',
                'secondary': '#60A5FA',
                'accent': '#93C5FD',
                'text': '#FFFFFF',
                'shadow': '#2563EB'
            },
            '橙红渐变': {
                'primary': '#F97316',
                'secondary': '#FB923C',
                'accent': '#FDBA74',
                'text': '#FFFFFF',
                'shadow': '#EA580C'
            },
            '粉色渐变': {
                'primary': '#EC4899',
                'secondary': '#F472B6',
                'accent': '#F9A8D4',
                'text': '#FFFFFF',
                'shadow': '#DB2777'
            },
            '绿色渐变': {
                'primary': '#10B981',
                'secondary': '#34D399',
                'accent': '#6EE7B7',
                'text': '#FFFFFF',
                'shadow': '#059669'
            },
            '简约黑白': {
                'primary': '#FFFFFF',
                'secondary': '#F3F4F6',
                'accent': '#E5E7EB',
                'text': '#1F2937',
                'shadow': '#9CA3AF'
            },
            '深紫渐变': {
                'primary': '#6B21A8',
                'secondary': '#9333EA',
                'accent': '#A855F7',
                'text': '#FFFFFF',
                'shadow': '#581C87'
            },
            '青色渐变': {
                'primary': '#0891B2',
                'secondary': '#06B6D4',
                'accent': '#22D3EE',
                'text': '#FFFFFF',
                'shadow': '#0E7490'
            },
            '玫瑰渐变': {
                'primary': '#E11D48',
                'secondary': '#F43F5E',
                'accent': '#FB7185',
                'text': '#FFFFFF',
                'shadow': '#BE123C'
            },
            '金色渐变': {
                'primary': '#D97706',
                'secondary': '#F59E0B',
                'accent': '#FBBF24',
                'text': '#FFFFFF',
                'shadow': '#B45309'
            }
        }
        
        self.styles = {
            '简约清新风': self._generate_minimalist_style,
            '高饱和度吸睛风': self._generate_vibrant_style,
            '渐变背景风': self._generate_gradient_style,
            '图文混排风': self._generate_mixed_style
        }
        
        self.fonts = {
            'title': None,
            'subtitle': None,
            'keyword': None
        }
        self._load_fonts()
    
    def _load_fonts(self):
        try:
            font_dir = 'C:/Windows/Fonts'
            self.fonts['title'] = ImageFont.truetype(f'{font_dir}/msyhbd.ttc', 90)
            self.fonts['subtitle'] = ImageFont.truetype(f'{font_dir}/msyh.ttc', 45)
            self.fonts['keyword'] = ImageFont.truetype(f'{font_dir}/msyh.ttc', 35)
        except:
            self.fonts['title'] = ImageFont.load_default()
            self.fonts['subtitle'] = ImageFont.load_default()
            self.fonts['keyword'] = ImageFont.load_default()
    
    def _hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _create_gradient(self, color1, color2, direction='vertical'):
        if direction == 'vertical':
            gradient = Image.new('RGB', (self.width, self.height))
            draw = ImageDraw.Draw(gradient)
            
            for y in range(self.height):
                ratio = y / self.height
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                draw.rectangle([(0, y), (self.width, y + 1)], fill=(r, g, b))
        else:
            gradient = Image.new('RGB', (self.width, self.height))
            draw = ImageDraw.Draw(gradient)
            
            for x in range(self.width):
                ratio = x / self.width
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                draw.rectangle([(x, 0), (x + 1, self.height)], fill=(r, g, b))
        
        return gradient
    
    def _add_decorative_circles(self, draw, color, count=5):
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            radius = random.randint(50, 200)
            
            rgb = self._hex_to_rgb(color)
            r, g, b = rgb
            
            draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], 
                       fill=(r, g, b, 80))
    
    def _add_decorative_squares(self, draw, color, count=5):
        for _ in range(count):
            x = random.randint(0, self.width - 100)
            y = random.randint(0, self.height - 100)
            size = random.randint(50, 150)
            rotation = random.randint(0, 45)
            
            rgb = self._hex_to_rgb(color)
            r, g, b = rgb
            
            draw.rectangle([(x, y), (x + size, y + size)], 
                        fill=(r, g, b, 60))
    
    def _add_geometric_pattern(self, draw, color):
        rgb = self._hex_to_rgb(color)
        r, g, b = rgb
        
        for i in range(0, self.width + self.height, 100):
            draw.line([(i, 0), (0, i)], fill=(r, g, b, 30), width=2)
            draw.line([(self.width - i, self.height), (self.width, self.height - i)], 
                     fill=(r, g, b, 30), width=2)
    
    def _add_wave_pattern(self, draw, color, y_position):
        rgb = self._hex_to_rgb(color)
        r, g, b = rgb
        
        points = []
        for x in range(0, self.width + 50, 50):
            y = y_position + math.sin(x / 100) * 30
            points.append((x, y))
        
        if len(points) > 1:
            draw.line(points, fill=(r, g, b, 100), width=8)
            draw.line(points, fill=(r, g, b, 150), width=4)
    
    def _add_corner_decorations(self, draw, color):
        rgb = self._hex_to_rgb(color)
        r, g, b = rgb
        
        corner_size = 150
        
        draw.polygon([(0, 0), (corner_size, 0), (0, corner_size)], 
                   fill=(r, g, b, 80))
        draw.polygon([(self.width, 0), (self.width - corner_size, 0), 
                    (self.width, corner_size)], fill=(r, g, b, 80))
        draw.polygon([(0, self.height), (corner_size, self.height), 
                    (0, self.height - corner_size)], fill=(r, g, b, 80))
        draw.polygon([(self.width, self.height), (self.width - corner_size, self.height), 
                    (self.width, self.height - corner_size)], fill=(r, g, b, 80))
    
    def _add_text_with_shadow(self, draw, text, position, font, text_color, shadow_color, offset=4):
        x, y = position
        
        shadow_rgb = self._hex_to_rgb(shadow_color)
        text_rgb = self._hex_to_rgb(text_color)
        
        draw.text((x + offset, y + offset), text, fill=shadow_rgb, font=font)
        draw.text((x, y), text, fill=text_rgb, font=font)
    
    def _add_keyword_badge(self, draw, text, position, font, bg_color, text_color):
        x, y = position
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        padding = 20
        badge_width = text_width + padding * 2
        badge_height = text_height + padding * 2
        
        bg_rgb = self._hex_to_rgb(bg_color)
        text_rgb = self._hex_to_rgb(text_color)
        
        draw.rounded_rectangle([(x, y), (x + badge_width, y + badge_height)], 
                           radius=15, fill=bg_rgb)
        draw.text((x + padding, y + padding), text, fill=text_rgb, font=font)
    
    def _generate_minimalist_style(self, title, keywords, color_scheme):
        scheme = self.color_schemes.get(color_scheme, self.color_schemes['简约黑白'])
        bg_color = self._hex_to_rgb(scheme['secondary'])
        
        image = Image.new('RGB', (self.width, self.height), bg_color)
        draw = ImageDraw.Draw(image, 'RGBA')
        
        text_color = scheme['text']
        accent_color = scheme['accent']
        
        self._add_geometric_pattern(draw, accent_color)
        
        y_position = 450
        
        if self.fonts['title']:
            bbox = draw.textbbox((0, 0), title, font=self.fonts['title'])
            text_width = bbox[2] - bbox[0]
            x_position = (self.width - text_width) // 2
            self._add_text_with_shadow(draw, title, (x_position, y_position), 
                                   self.fonts['title'], text_color, scheme['shadow'])
        else:
            draw.text((self.width // 2 - len(title) * 20, y_position), 
                    title, fill=text_color)
        
        y_position += 180
        
        if keywords:
            keyword_text = ' | '.join(keywords[:3])
            if self.fonts['keyword']:
                bbox = draw.textbbox((0, 0), keyword_text, font=self.fonts['keyword'])
                text_width = bbox[2] - bbox[0]
                x_position = (self.width - text_width) // 2
                draw.text((x_position, y_position), keyword_text, 
                         fill=self._hex_to_rgb(scheme['shadow']), 
                         font=self.fonts['keyword'])
            else:
                draw.text((self.width // 2 - len(keyword_text) * 15, y_position), 
                        keyword_text, fill=self._hex_to_rgb(scheme['shadow']))
        
        return image
    
    def _generate_vibrant_style(self, title, keywords, color_scheme):
        scheme = self.color_schemes.get(color_scheme, self.color_schemes['橙红渐变'])
        
        color1 = self._hex_to_rgb(scheme['primary'])
        color2 = self._hex_to_rgb(scheme['secondary'])
        
        image = self._create_gradient(color1, color2, 'diagonal')
        draw = ImageDraw.Draw(image, 'RGBA')
        
        self._add_decorative_circles(draw, scheme['accent'], 8)
        self._add_decorative_squares(draw, scheme['accent'], 6)
        self._add_wave_pattern(draw, scheme['accent'], 350)
        self._add_wave_pattern(draw, scheme['accent'], 1100)
        
        text_color = scheme['text']
        
        y_position = 400
        
        if self.fonts['title']:
            bbox = draw.textbbox((0, 0), title, font=self.fonts['title'])
            text_width = bbox[2] - bbox[0]
            x_position = (self.width - text_width) // 2
            self._add_text_with_shadow(draw, title, (x_position, y_position), 
                                   self.fonts['title'], text_color, scheme['shadow'], offset=6)
        else:
            draw.text((self.width // 2 - len(title) * 20, y_position), 
                    title, fill=text_color)
        
        y_position += 220
        
        if keywords:
            start_x = (self.width - len(keywords[:3]) * 280) // 2
            for i, keyword in enumerate(keywords[:3]):
                x_position = start_x + i * 280
                self._add_keyword_badge(draw, keyword, (x_position, y_position), 
                                     self.fonts['keyword'], scheme['accent'], text_color)
        
        return image
    
    def _generate_gradient_style(self, title, keywords, color_scheme):
        scheme = self.color_schemes.get(color_scheme, self.color_schemes['紫色渐变'])
        
        color1 = self._hex_to_rgb(scheme['primary'])
        color2 = self._hex_to_rgb(scheme['secondary'])
        
        image = self._create_gradient(color1, color2, 'vertical')
        draw = ImageDraw.Draw(image, 'RGBA')
        
        self._add_corner_decorations(draw, scheme['accent'])
        self._add_decorative_circles(draw, scheme['accent'], 4)
        
        text_color = scheme['text']
        
        y_position = 420
        
        if self.fonts['title']:
            bbox = draw.textbbox((0, 0), title, font=self.fonts['title'])
            text_width = bbox[2] - bbox[0]
            x_position = (self.width - text_width) // 2
            self._add_text_with_shadow(draw, title, (x_position, y_position), 
                                   self.fonts['title'], text_color, scheme['shadow'], offset=5)
        else:
            draw.text((self.width // 2 - len(title) * 20, y_position), 
                    title, fill=text_color)
        
        y_position += 200
        
        if keywords:
            keyword_text = ' · '.join(keywords[:3])
            if self.fonts['subtitle']:
                bbox = draw.textbbox((0, 0), keyword_text, font=self.fonts['subtitle'])
                text_width = bbox[2] - bbox[0]
                x_position = (self.width - text_width) // 2
                draw.text((x_position, y_position), keyword_text, 
                         fill=self._hex_to_rgb(scheme['accent']), 
                         font=self.fonts['subtitle'])
            else:
                draw.text((self.width // 2 - len(keyword_text) * 15, y_position), 
                        keyword_text, fill=self._hex_to_rgb(scheme['accent']))
        
        return image
    
    def _generate_mixed_style(self, title, keywords, color_scheme):
        scheme = self.color_schemes.get(color_scheme, self.color_schemes['蓝色渐变'])
        
        color1 = self._hex_to_rgb(scheme['primary'])
        color2 = self._hex_to_rgb(scheme['secondary'])
        
        image = self._create_gradient(color1, color2, 'vertical')
        draw = ImageDraw.Draw(image, 'RGBA')
        
        header_height = 180
        header_bg = (255, 255, 255, 230)
        draw.rectangle([(0, 0), (self.width, header_height)], fill=header_bg)
        
        if self.fonts['subtitle']:
            draw.text((80, 70), '小红书', fill=self._hex_to_rgb(scheme['primary']), 
                    font=self.fonts['subtitle'])
        
        self._add_decorative_circles(draw, scheme['accent'], 6)
        self._add_wave_pattern(draw, scheme['accent'], 1300)
        
        text_color = scheme['text']
        
        y_position = 400
        
        if self.fonts['title']:
            bbox = draw.textbbox((0, 0), title, font=self.fonts['title'])
            text_width = bbox[2] - bbox[0]
            x_position = (self.width - text_width) // 2
            self._add_text_with_shadow(draw, title, (x_position, y_position), 
                                   self.fonts['title'], text_color, scheme['shadow'], offset=5)
        else:
            draw.text((self.width // 2 - len(title) * 20, y_position), 
                    title, fill=text_color)
        
        y_position += 220
        
        if keywords:
            start_x = (self.width - len(keywords[:3]) * 300) // 2
            for i, keyword in enumerate(keywords[:3]):
                x_position = start_x + i * 300
                self._add_keyword_badge(draw, keyword, (x_position, y_position), 
                                     self.fonts['keyword'], scheme['accent'], text_color)
        
        return image
    
    def _generate_midjourney_prompt(self, title: str, keywords: list, style: str, color_scheme: str) -> str:
        style_prompts = {
            '简约清新风': 'minimalist design, clean and fresh, simple layout, elegant typography, white space, modern aesthetic',
            '高饱和度吸睛风': 'vibrant colors, eye-catching design, bold typography, energetic, dynamic composition, high contrast',
            '渐变背景风': 'gradient background, modern tech style, sleek design, smooth transitions, contemporary',
            '图文混排风': 'mixed media layout, creative composition, visual storytelling, artistic arrangement, trendy design'
        }
        
        color_prompts = {
            '紫色渐变': 'purple gradient, mystical purple, elegant violet',
            '蓝色渐变': 'blue gradient, professional blue, fresh cyan',
            '橙红渐变': 'orange-red gradient, warm orange, energetic red',
            '粉色渐变': 'pink gradient, soft pink, rose color',
            '绿色渐变': 'green gradient, fresh green, natural emerald',
            '简约黑白': 'black and white, monochrome, minimalist black white',
            '深紫渐变': 'deep purple gradient, royal purple, mysterious violet',
            '青色渐变': 'cyan gradient, teal, aqua blue',
            '玫瑰渐变': 'rose gradient, crimson, romantic red',
            '金色渐变': 'gold gradient, warm gold, luxury amber'
        }
        
        base_prompt = f"Xiaohongshu cover design, {title}"
        
        if keywords:
            keywords_text = ', '.join(keywords[:3])
            base_prompt += f", {keywords_text}"
        
        style_desc = style_prompts.get(style, 'modern design')
        color_desc = color_prompts.get(color_scheme, 'vibrant colors')
        
        full_prompt = f"{base_prompt}, {style_desc}, {color_desc}"
        full_prompt += ", 1080x1440 aspect ratio, vertical orientation, social media cover, high quality, detailed, 8k"
        
        return full_prompt
    
    def generate(self, title, keywords=None, style='简约清新风', color_scheme='紫色渐变', output_format='JPG', use_midjourney=False):
        if keywords is None:
            keywords = []
        
        if style not in self.styles:
            style = '简约清新风'
        
        if color_scheme not in self.color_schemes:
            color_scheme = '紫色渐变'
        
        if use_midjourney and self.midjourney_client:
            print('🎨 使用 Midjourney 生成图片...')
            prompt = self._generate_midjourney_prompt(title, keywords, style, color_scheme)
            print(f'📝 提示词: {prompt[:150]}...')
            
            safe_title = ''.join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title[:20]
            
            output_format = output_format.upper()
            ext = 'png' if output_format == 'PNG' else 'jpg'
            filename = f'{safe_title}_cover_midjourney.{ext}'
            output_path = os.path.join(self.output_dir, filename)
            
            success = self.midjourney_client.generate_and_download(
                title=title,
                keywords=keywords,
                style=style,
                color_scheme=color_scheme,
                save_path=output_path
            )
            
            if success:
                print(f'✅ Midjourney 图片已保存: {output_path}')
                return output_path
            else:
                print('⚠️  Midjourney 生成失败，切换到本地生成模式')
        
        image = self.styles[style](title, keywords, color_scheme)
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        safe_title = ''.join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title[:20]
        
        output_format = output_format.upper()
        if output_format == 'PNG':
            filename = f'{safe_title}_cover.png'
            output_path = os.path.join(self.output_dir, filename)
            image.save(output_path, 'PNG')
        else:
            filename = f'{safe_title}_cover.jpg'
            output_path = os.path.join(self.output_dir, filename)
            image.save(output_path, 'JPEG', quality=95)
        
        return output_path
    
    def generate_batch(self, titles_list, style='简约清新风', color_scheme='紫色渐变'):
        results = []
        for item in titles_list:
            if isinstance(item, dict):
                title = item.get('title', '')
                keywords = item.get('keywords', [])
                style = item.get('style', style)
                color_scheme = item.get('color_scheme', color_scheme)
            else:
                title = item
                keywords = []
            
            output_path = self.generate(title, keywords, style, color_scheme)
            results.append(output_path)
        
        return results


def main():
    generator = XiaohongshuCoverGenerator()
    
    print('小红书封面图生成器')
    print('=' * 50)
    
    title = input('请输入标题: ')
    keywords_input = input('请输入关键词（用逗号分隔）: ')
    keywords = [k.strip() for k in keywords_input.split(',') if k.strip()]
    
    print('\n可选风格:')
    for i, style in enumerate(generator.styles.keys(), 1):
        print(f'{i}. {style}')
    
    style_choice = input('请选择风格（默认1）: ')
    style_choice = int(style_choice) if style_choice else 1
    style = list(generator.styles.keys())[style_choice - 1]
    
    print('\n可选配色方案:')
    for i, scheme in enumerate(generator.color_schemes.keys(), 1):
        print(f'{i}. {scheme}')
    
    color_choice = input('请选择配色方案（默认1）: ')
    color_choice = int(color_choice) if color_choice else 1
    color_scheme = list(generator.color_schemes.keys())[color_choice - 1]
    
    output_path = generator.generate(title, keywords, style, color_scheme)
    
    print(f'\n✅ 封面图已生成: {output_path}')


if __name__ == '__main__':
    main()
