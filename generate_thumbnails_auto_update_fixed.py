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
    print("请运行: python -m pip install Pillow")
    input("\n按回车退出...")
    sys.exit()

SRC_DIR = "images"
THUMB_DIR = "images/thumbs"
HTML_FILE = "index.html"

MAX_SIZE = (480, 480)


def scan_images():
    for root, dirs, files in os.walk(SRC_DIR):
        dirs[:] = [d for d in dirs if d != "thumbs"]

        for f in files:
            if os.path.splitext(f)[1].lower() in (
                ".jpg",".jpeg",".png",".webp",".bmp"
            ):
                yield os.path.join(root, f)


def thumb_path(src):
    rel = os.path.relpath(src, SRC_DIR)
    rel = os.path.splitext(rel)[0]
    return os.path.join(
        THUMB_DIR,
        rel + ".jpg"
    )


def create_thumb(src, dst):

    os.makedirs(
        os.path.dirname(dst),
        exist_ok=True
    )

    with Image.open(src) as img:

        img = ImageOps.exif_transpose(img)
        img.thumbnail(
            MAX_SIZE,
            Image.LANCZOS
        )

        if img.mode != "RGB":
            img = img.convert("RGB")

        img.save(
            dst,
            "JPEG",
            quality=80
        )


def generate():

    print("\n==========生成缩略图==========")

    num = 0

    for src in scan_images():

        dst = thumb_path(src)

        if (
            not os.path.exists(dst)
            or os.path.getmtime(src) > os.path.getmtime(dst)
        ):

            create_thumb(src, dst)

            print("生成:", dst)
            num += 1

    print("生成完成:", num)


def update_html():

    if not os.path.exists(HTML_FILE):
        print("没有找到 index.html")
        return

    with open(
        HTML_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        html = f.read()


    def replace(m):

        return (
            'src="images/thumbs/' +
            os.path.splitext(m.group(1))[0] +
            '.jpg"'
        )


    html, count = re.subn(
        r'src="images/(?!thumbs/)([^"]+\.(?:jpg|jpeg|png|webp))"',
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

    print("网页更新:", count)


def main():

    print("🚀 作品集缩略图工具")

    generate()
    update_html()

    print("\n✅ 完成")


if __name__ == "__main__":

    try:
        main()
    except Exception as e:
        print("❌ 错误:", e)

    input("\n按回车退出...")
