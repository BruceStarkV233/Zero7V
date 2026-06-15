import csv
import os
from bs4 import BeautifulSoup

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(current_dir, 'image_notes.csv')
html_file = os.path.join(current_dir, 'index.html')

if not os.path.exists(csv_file):
    print(f"❌ 错误：找不到 {csv_file}，请先运行第一个脚本生成清单！")
    input("\n按下回车键退出...")
    exit()

# 1. 读取 CSV 数据并处理
gallery_items_html = []
category_tree = {}

def add_to_tree(tree, path_parts, current_prefix=""):
    if not path_parts:
        return
    part = path_parts[0]
    this_node_path = f"{current_prefix}/{part}" if current_prefix else part
    
    if part not in tree:
        tree[part] = {"_full_path": this_node_path, "_children": {}}
    else:
        tree[part]["_full_path"] = this_node_path
        
    add_to_tree(tree[part]["_children"], path_parts[1:], this_node_path)

with open(csv_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cat_path = row['分类层级'].strip()
        if cat_path and cat_path != 'all':
            parts = cat_path.split('/')
            add_to_tree(category_tree, parts)
            
        # 🌟【最核心的修改】：为图片生成多级联动样式类
        # 如果 cat_path 是 "角色/卡通角色"，这里会生成 "all 角色 角色/卡通角色"
        if cat_path and cat_path != 'all':
            levels = cat_path.split('/')
            cat_classes = " ".join(["/".join(levels[:i+1]) for i in range(len(levels))])
        else:
            cat_classes = "all"

        item = f"""
    <div class="gallery__item" data-category="{cat_classes}"
         data-full="images/{row['原图路径']}"
         data-title="{row['图片标题']}"
         data-meta="{row['描述信息']}">
      <img src="images/{row['缩略图路径']}" width="600" height="450" alt="{row['图片标题']}" class="gallery__image" loading="lazy" />
      <div class="gallery__caption">
        <span class="gallery__caption-title">{row['图片标题']}</span>
        <span class="gallery__caption-meta">{row['描述信息']}</span>
      </div>
      <div class="gallery__expand-icon" aria-hidden="true">
        <svg viewBox="0 0 12 12" stroke-width="1.5"><path d="M1 4V1h3M8 1h3v3M11 8v3H8M4 11H1V8"/></svg>
      </div>
    </div>"""
        gallery_items_html.append(item)

# 2. 递归生成嵌套的 HTML 下拉菜单
def generate_menu_html(tree_node):
    if not tree_node:
        return ""
    html = '<ul class="filter__dropdown">\n'
    for name, data in sorted(tree_node.items()):
        display_name = name.title()
        full_cat = data["_full_path"]
        children = data["_children"]
        
        if children:
            html += f'  <li class="filter__menu-item has-children">\n'
            html += f'    <button class="filter__btn" data-filter="{full_cat}">{display_name} ▾</button>\n'
            html += generate_menu_html(children)
            html += f'  </li>\n'
        else:
            html += f'  <li class="filter__menu-item"><button class="filter__btn" data-filter="{full_cat}">{display_name}</button></li>\n'
    html += '</ul>\n'
    return html

# 拼装顶层导航
top_filter_html = ['<ul class="filter__main-nav">', '    <li class="filter__menu-item"><button class="filter__btn is-active" data-filter="all">All</button></li>']
for name, data in sorted(category_tree.items()):
    display_name = name.title()
    full_cat = data["_full_path"]
    children = data["_children"]
    if children:
        top_filter_html.append(f'    <li class="filter__menu-item has-children">\n      <button class="filter__btn" data-filter="{full_cat}">{display_name} ▾</button>\n' + generate_menu_html(children) + '    </li>')
    else:
        top_filter_html.append(f'    <li class="filter__menu-item"><button class="filter__btn" data-filter="{full_cat}">{display_name}</button></li>')
top_filter_html.append('  </ul>')

# 3. 替换内容
with open(html_file, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

gallery_target = soup.find('main', id='js-gallery') or soup.find('main', class_='gallery')
filter_target = soup.find('div', class_='gallery-filter')

if gallery_target and filter_target:
    gallery_target.clear()
    gallery_target.append(BeautifulSoup("\n".join(gallery_items_html), 'html.parser'))
    
    filter_target.clear()
    filter_target.append(BeautifulSoup("\n".join(top_filter_html), 'html.parser'))
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("🎉 【图片属性同步成功】图片现在的 data-category 已经拥有多级识别能力了！")
else:
    print("❌ 未能成功替换，请确认 index.html 中的容器标签是否存在。")

input("\n按下回车键退出...")