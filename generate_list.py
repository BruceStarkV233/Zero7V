import os
import csv

current_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(current_dir, 'images')
output_csv = os.path.join(current_dir, 'image_notes.csv')

if not os.path.exists(image_dir):
    print(f"❌ 错误：在当前目录下没有找到【images】文件夹！")
    input("\n按下回车键退出...")
    exit()

valid_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp')
all_found_images = []

print(f"🔍 开始深度扫描【{image_dir}】层级结构...\n")

for root, dirs, files in os.walk(image_dir):
    for file in files:
        if os.path.splitext(file)[1].lower() in valid_extensions:
            if file.lower().startswith('thumb-'):
                continue
                
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, image_dir).replace('\\', '/')
            
            # 获取相对目录层级（例如：角色/卡通角色/名侦探柯南）
            rel_dir = os.path.relpath(root, image_dir).replace('\\', '/')
            
            # 🌟【核心修复】：如果图片在子文件夹中，确保“分类层级”保留完整的路径
            category = 'all' if rel_dir == '.' else rel_dir
            
            # 自动生成默认标题（拿文件名当标题）
            default_title = os.path.splitext(file)[0].replace('-', ' ').replace('_', ' ').title()
            
            # 检查同级目录下有没有对应的缩略图 (thumb-文件名)
            thumb_file = f"thumb-{file}"
            if thumb_file in files:
                thumb_relative_path = os.path.relpath(os.path.join(root, thumb_file), image_dir).replace('\\', '/')
            else:
                thumb_relative_path = relative_path
                
            all_found_images.append({
                'origin': relative_path,
                'thumb': thumb_relative_path,
                'category': category,
                'title': default_title
            })

with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['原图路径', '缩略图路径', '分类层级', '图片标题', '描述信息'])
    for img in all_found_images:
        # 将最后一列“描述信息”直接赋值为图片的“原图路径”以供前端使用
        writer.writerow([img['origin'], img['thumb'], img['category'], img['title'], img['origin']])

print(f"🎉 成功！已扫描到 {len(all_found_images)} 张有效图片，清单已更新至 image_notes.csv")
input("\n按下回车键退出...")