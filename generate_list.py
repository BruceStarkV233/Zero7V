import os
import csv

# 定义你的图片文件夹路径
# 假设你的结构是：根目录/images/ 里面放了原图，或者有缩略图
image_dir = 'images'
output_csv = 'image_notes.csv'

# 支持的图片格式
valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')

# 扫描文件夹中的所有图片
image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(valid_extensions)]

# 过滤掉已经是缩略图的文件（比如带有 thumb- 前缀的），只保留原图作为基准
# 或者如果你的命名很规整，可以根据实际情况调整
origin_images = [f for f in image_files if not f.startswith('thumb-')]

# 自动创建 Excel/CSV 清单文件
with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    # 写入表头：原图文件名, 缩略图文件名, 分类, 弹出标题, 描述/地点
    writer.writerow(['原图文件名', '缩略图文件名', '分类(portrait/landscape/urban/nature)', '图片标题', '描述信息'])
    
    for img in origin_images:
        # 尝试猜测缩略图的名字，比如原图是 exhibit-01.jpg，缩略图可能是 thumb-exhibit-01.jpg
        # 如果你没有单独的缩略图，直接让它等于原图即可
        thumb_name = f"thumb-{img}" if os.path.exists(os.path.join(image_dir, f"thumb-{img}")) else img
        
        # 默认标题直接用文件名（去掉后缀）
        default_title = os.path.splitext(img)[0].replace('-', ' ').title()
        
        writer.writerow([img, thumb_name, 'landscape', default_title, 'Captured in 2026'])

print(f"成功！已在当前目录下生成【{output_csv}】。")
print("你可以直接用 Excel 或文本编辑器打开它，修改里面的‘分类’、‘图片标题’和‘描述信息’。")
