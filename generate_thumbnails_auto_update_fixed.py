#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

try:
    from PIL import Image, ImageOps
except ImportError:
    print("❌ 缺少 Pillow")
    print("请运行：")
    print("python -m pip install Pillow")
    input("\n按回车退出...")
    sys.exit()

# ===========================
# 配置
# ===========================

SRC_DIR = "images"
THUMB_DIR = "images/thumbs"
HTML_FILE = "index.html"

# 缩略图尺寸（原来480，现放大两倍）
MAX_SIZE = (960, 960)

# JPEG质量
JPEG_QUALITY = 92


# ===========================
# 扫描图片
# ===========================

def scan_images():
    for root, dirs, files in os.walk(SRC_DIR):

        # 不扫描thumbs目录
        dirs[:] = [d for d in dirs if d != "thumbs"]

        for f in files:
            if os.path.splitext(f)[1].lower() in (
                ".jpg",
                ".jpeg",
                ".png",
                ".webp",
                ".bmp"
            ):
                yield os.path.join(root, f)


# ===========================
# 计算缩略图路径
# ===========================

def thumb_path(src):
    rel = os.path.relpath(src, SRC_DIR)
    rel = os.path.splitext(rel)[0]

    return os.path.join(
        THUMB_DIR,
        rel + ".jpg"
    )


# ===========================
# 生成缩略图
# ===========================

def create_thumb(src, dst):

    os.makedirs(
        os.path.dirname(dst),
        exist_ok=True
    )

    with Image.open(src) as img:

        # 自动旋转
        img = ImageOps.exif_transpose(img)

        # 保持比例缩放
        img.thumbnail(
            MAX_SIZE,
            Image.LANCZOS
        )

        if img.mode != "RGB":
            img = img.convert("RGB")

        img.save(
            dst,
            "JPEG",
            quality=JPEG_QUALITY,
            optimize=True
        )


# ===========================
# 批量生成（每次覆盖）
# ===========================

def generate():

    print("\n================================")
    print("开始重新生成缩略图")
    print("================================")

    total = 0

    for src in scan_images():

        dst = thumb_path(src)

        create_thumb(src, dst)

        print("✔", dst)

        total += 1

    print("\n================================")
    print("缩略图生成完成")
    print("共生成：", total)
    print("================================")


# ===========================
# 更新HTML
# ===========================

def update_html():

    if not os.path.exists(HTML_FILE):
        print("⚠ 未找到 index.html")
        return

    with open(
        HTML_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        html = f.read()

    def replace(m):

        return (
            'src="images/thumbs/'
            + os.path.splitext(m.group(1))[0]
            + '.jpg"'
        )

    html, count = re.subn(
        r'src="images/(?!thumbs/)([^"]+\.(?:jpg|jpeg|png|webp|bmp))"',
        replace,
        html,
        flags=re.I
    )

    with open(
        HTML_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(html)

    print("\nHTML更新完成，共替换", count, "处图片链接")


# ===========================
# 主程序
# ===========================

def main():

    print("================================")
    print("🚀 作品集缩略图自动生成工具")
    print("================================")

    generate()

    update_html()

    print("\n✅ 全部完成！")


# ===========================

if __name__ == "__main__":

    try:
        main()

    except Exception as e:
        print("\n❌ 发生错误：")
        print(e)

    input("\n按回车退出...")