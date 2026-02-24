import requests
import time
import json
import os
from typing import Optional, List

class MidjourneyClient:
    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None):
        self.api_key = api_key or os.getenv('MIDJOURNEY_API_KEY')
        self.api_url = api_url or os.getenv('MIDJOURNEY_API_URL', 'https://api.midjourney.com/v1')
        
        if not self.api_key:
            print('⚠️  警告: 未设置 Midjourney API Key')
            print('💡 提示: 请设置环境变量 MIDJOURNEY_API_KEY 或在初始化时传入')
    
    def generate_prompt(self, title: str, keywords: List[str], style: str, color_scheme: str) -> str:
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
    
    def generate_image(self, prompt: str, wait_for_completion: bool = True, timeout: int = 300) -> Optional[str]:
        if not self.api_key:
            print('❌ 错误: 未设置 Midjourney API Key')
            return None
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'prompt': prompt,
                'aspect_ratio': '9:16',
                'quality': 'high'
            }
            
            print('🎨 正在调用 Midjourney 生成图片...')
            print(f'📝 提示词: {prompt[:100]}...')
            
            response = requests.post(
                f'{self.api_url}/imagine',
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                task_id = result.get('task_id')
                
                if task_id and wait_for_completion:
                    return self._wait_for_completion(task_id, timeout)
                elif task_id:
                    print(f'✅ 任务已提交，任务ID: {task_id}')
                    return task_id
                else:
                    print('❌ 错误: 未获取到任务ID')
                    return None
            else:
                print(f'❌ 错误: API 请求失败 (状态码: {response.status_code})')
                print(f'响应: {response.text}')
                return None
                
        except requests.exceptions.Timeout:
            print('❌ 错误: 请求超时')
            return None
        except requests.exceptions.RequestException as e:
            print(f'❌ 错误: 请求异常 - {str(e)}')
            return None
        except Exception as e:
            print(f'❌ 错误: {str(e)}')
            return None
    
    def _wait_for_completion(self, task_id: str, timeout: int) -> Optional[str]:
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                }
                
                response = requests.get(
                    f'{self.api_url}/task/{task_id}',
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    status = result.get('status')
                    
                    if status == 'completed':
                        image_url = result.get('image_url')
                        if image_url:
                            print('✅ 图片生成完成！')
                            return image_url
                        else:
                            print('❌ 错误: 未获取到图片URL')
                            return None
                    elif status == 'failed':
                        print('❌ 错误: 图片生成失败')
                        return None
                    elif status == 'processing':
                        print(f'⏳ 正在生成中... (已等待 {int(time.time() - start_time)} 秒)')
                        time.sleep(5)
                    else:
                        print(f'⏳ 状态: {status}')
                        time.sleep(5)
                else:
                    print(f'❌ 错误: 查询任务失败 (状态码: {response.status_code})')
                    return None
                    
            except requests.exceptions.RequestException as e:
                print(f'❌ 错误: 查询异常 - {str(e)}')
                time.sleep(5)
            except Exception as e:
                print(f'❌ 错误: {str(e)}')
                time.sleep(5)
        
        print(f'⏰ 超时: 等待超过 {timeout} 秒')
        return None
    
    def download_image(self, image_url: str, save_path: str) -> bool:
        try:
            print(f'📥 正在下载图片...')
            
            response = requests.get(image_url, stream=True, timeout=30)
            
            if response.status_code == 200:
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f'✅ 图片已保存: {save_path}')
                return True
            else:
                print(f'❌ 错误: 下载失败 (状态码: {response.status_code})')
                return False
                
        except requests.exceptions.Timeout:
            print('❌ 错误: 下载超时')
            return False
        except requests.exceptions.RequestException as e:
            print(f'❌ 错误: 下载异常 - {str(e)}')
            return False
        except Exception as e:
            print(f'❌ 错误: {str(e)}')
            return False
    
    def generate_and_download(self, title: str, keywords: List[str], style: str, 
                          color_scheme: str, save_path: str) -> bool:
        prompt = self.generate_prompt(title, keywords, style, color_scheme)
        
        image_url = self.generate_image(prompt)
        
        if image_url:
            return self.download_image(image_url, save_path)
        
        return False


def main():
    print('Midjourney 客户端测试')
    print('=' * 60)
    print()
    
    api_key = os.getenv('MIDJOURNEY_API_KEY')
    
    if not api_key:
        print('⚠️  未设置 MIDJOURNEY_API_KEY 环境变量')
        print()
        print('💡 使用方法:')
        print('1. 设置环境变量: export MIDJOURNEY_API_KEY=your_api_key')
        print('2. 或在代码中传入 API Key')
        print()
        return
    
    client = MidjourneyClient(api_key=api_key)
    
    print('测试提示词生成:')
    print('-' * 40)
    
    prompt = client.generate_prompt(
        title='欧啊欧春节粉丝抽奖活动',
        keywords=['抽一个幸运粉丝获得', '拜仁穆勒签名卡砖'],
        style='高饱和度吸睛风',
        color_scheme='橙红渐变'
    )
    
    print(f'生成的提示词:')
    print(prompt)
    print()
    
    print('是否测试图片生成？(y/n, 默认n): ')
    choice = input().strip().lower()
    
    if choice == 'y':
        output_path = 'output/test_midjourney.jpg'
        success = client.generate_and_download(
            title='欧啊欧春节粉丝抽奖活动',
            keywords=['抽一个幸运粉丝获得', '拜仁穆勒签名卡砖'],
            style='高饱和度吸睛风',
            color_scheme='橙红渐变',
            save_path=output_path
        )
        
        if success:
            print(f'✅ 测试成功！图片已保存到: {output_path}')
        else:
            print('❌ 测试失败')


if __name__ == '__main__':
    main()
