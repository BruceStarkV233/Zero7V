import os
import re

# ================= 配置区域 =================
# 1. 你的图片相对于 index.html 的文件夹路径
IMAGE_DIR = "images/gallery" 

# 2. 你的网页文件名
HTML_FILE = "index.html"
# ============================================

def natural_sort_key(s):
    """ 对文件名进行自然排序（防止 10.jpg 排在 2.jpg 前面） """
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def generate_gallery_html(img_dir):
    if not os.path.exists(img_dir):
        print(f"错误：找不到图片文件夹 '{img_dir}'，请检查路径是否正确。")
        return None

    # 支持的图片格式
    valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
    
    # 获取并排序所有图片文件名
    files = [f for f in os.listdir(img_dir) if f.lower().endswith(valid_extensions)]
    files.sort(key=natural_sort_key)
    
    if not files:
        print(f"提示：在 '{img_dir}' 文件夹中没有找到任何图片。")
        return None

    print(f"成功找到并排序了 {len(files)} 张图片：", files)

    # 动态生成符合你网页结构的 HTML 字符串
    gallery_html_parts = []
    for file in files:
        # 拼接图片在网页中的相对路径
        web_img_path = f"{img_dir}/{file}"
        # 去掉后缀作为默认标题（例如 "01.jpg" 变成 "01"）
        title = os.path.splitext(file)[0]
        
        item_html = f"""
                <div class="gallery__item" data-full="{web_img_path}" data-title="作品 {title}">
                    <div class="gallery__item-image-wrapper">
                        <img src="{web_img_path}" alt="作品 {title}" class="gallery__item-image" loading="lazy">
                    </div>
                    <div class="gallery__item-info">
                        <h3 class="gallery__item-title">作品 {title}</h3>
                        <p class="gallery__item-category">Photography</p>
                    </div>
                </div>"""
        gallery_html_parts.append(item_html)
        
    return "\n".join(gallery_html_parts)

def main():
    if not os.path.exists(HTML_FILE):
        print(f"错误：未能在当前目录下找到 {HTML_FILE}")
        return

    # 1. 生成按文件名排好序的图片 HTML
    new_gallery_content = generate_gallery_html(IMAGE_DIR)
    if not new_gallery_content:
        return

    # 2. 读取现有的 HTML
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html_content = f.read()

    # 3. 寻找网页中存放图片的容器标签
    # 你的网页中使用的是 <div class="gallery__grid" ...> 
    start_tag = '<div class="gallery__grid"'
    end_tag = '</div>'
    
    # 如果找不到精确的结尾注释，尝试通用的闭合标签定位
    if start_tag in html_content and end_tag in html_content:
        pattern = re.compile(r'('<div class="gallery__grid".*?'>)(.*?)(</div>)', re.DOTALL)
        if pattern.search(html_content):
            # 替换容器内部的旧图片，保留容器外壳
            fixed_html = pattern.sub(rf'\1\n{new_gallery_content}\n\3', html_content)
            
            with open(HTML_FILE, "w", encoding="utf-8") as f:
                f.write(fixed_html)
            print(f"\n🎉 成功！{HTML_FILE} 中的图片已完全按照文件名顺序重新排列！")
            return

    # 如果正则匹配由于格式微调失败了，提供备用方案
    print("⚠️ 自动定位容器失败，请确认你的图片网格容器 class 是否为 'gallery__grid'。")

if __name__ == "__main__":
    main()