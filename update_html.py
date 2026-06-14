import csv
import os

csv_file = 'image_notes.csv'
html_file = 'index.html'

if not os.path.exists(csv_file):
    print(f"错误：找不到 {csv_file}，请先运行第一个脚本生成清单！")
    exit()

# 1. 读取 CSV 中的图片数据
gallery_items_html = []
with open(csv_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # 拼装单个图片块的 HTML 模版
        item = f"""    <div class="gallery__item" data-category="{row['分类(portrait/landscape/urban/nature)']}"
         data-full="images/{row['原图文件名']}"
         data-title="{row['图片标题']}"
         data-meta="{row['描述信息']}">

      <img
        src="images/{row['缩略图文件名']}"
        width="600"
        height="450"
        alt="{row['图片标题']}"
        class="gallery__image"
        loading="lazy"
      />

      <div class="gallery__caption">
        <span class="gallery__caption-title">{row['图片标题']}</span>
        <span class="gallery__caption-meta">{row['描述信息']}</span>
      </div>

      <div class="gallery__expand-icon" aria-hidden="true">
        <svg viewBox="0 0 12 12" stroke-width="1.5"><path d="M1 4V1h3M8 1h3v3M11 8v3H8M4 11H1V8"/></svg>
      </div>

    </div>
"""
        gallery_items_html.append(item)

all_images_html = "\n".join(gallery_items_html)

# 2. 读取现有的 index.html 并替换
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 利用特征标记定位你要替换的画廊区域
start_tag = '<main class="gallery" id="js-gallery" aria-label="Photo gallery">'
end_tag = '</main>'

if start_tag in html_content and end_tag in html_content:
    parts = html_content.split(start_tag)
    before_gallery = parts[0] + start_tag + "\n"
    after_gallery = end_tag + parts[1].split(end_tag)[1]
    
    # 重新组合完整的 HTML
    new_html_content = before_gallery + all_images_html + "\n  " + after_gallery
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_html_content)
    print("成功！index.html 中的画廊图片已根据清单全部自动更新！")
else:
    print("错误：在 index.html 中没有找到指定的 <main class=\"gallery\"...> 标记，请检查 HTML 结构是否被破坏。")
