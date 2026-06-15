#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量生成网站图片缩略图脚本

用法：
  1. 把这个文件放到你的网站仓库根目录（和 images 文件夹同级）
  2. 安装依赖： pip install Pillow
  3. 运行：     python generate_thumbnails.py

效果：
  会遍历 images/ 下所有图片（包括子文件夹，如 images/场景、images/角色 等），
  在 images/thumbs/ 下生成同样目录结构的缩略图，文件统一转为 .jpg 格式
  （体积更小，适合做画廊预览图）。

  例如：
    images/场景/2021芜湖科博会.png
    -> images/thumbs/场景/2021芜湖科博会.jpg

  已经生成过、且原图没有更新过的文件会自动跳过，方便以后增量运行。
"""

import os
from PIL import Image, ImageOps

# ====== 可以根据需要调整的参数 ======
SRC_DIR = "images"           # 原图所在目录
THUMB_DIR = "images/thumbs"  # 缩略图输出目录
MAX_SIZE = (480, 480)         # 缩略图最大宽/高（保持比例缩放）
JPEG_QUALITY = 78             # JPEG 压缩质量 0-100，建议 70~85
SKIP_DIR_NAMES = {"thumbs"}   # 不处理这些子文件夹
IMG_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tif", ".tiff"}
# ====================================


def iter_images(src_dir):
    for root, dirs, files in os.walk(src_dir):
        # 跳过 thumbs 目录本身，避免对缩略图再生成缩略图
        dirs[:] = [d for d in dirs if d not in SKIP_DIR_NAMES]
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext in IMG_EXTS:
                yield os.path.join(root, fname)


def thumb_path_for(src_path):
    """计算某个原图对应的缩略图输出路径（统一改为 .jpg）"""
    rel = os.path.relpath(src_path, SRC_DIR)
    rel_no_ext = os.path.splitext(rel)[0]
    return os.path.join(THUMB_DIR, rel_no_ext + ".jpg")


def needs_update(src_path, dst_path):
    if not os.path.exists(dst_path):
        return True
    return os.path.getmtime(src_path) > os.path.getmtime(dst_path)


def make_thumbnail(src_path, dst_path):
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)

    with Image.open(src_path) as img:
        # 处理 GIF 等多帧图片：只取第一帧
        if getattr(img, "is_animated", False):
            img.seek(0)

        # 根据 EXIF 信息校正旋转方向（手机照片常见问题）
        img = ImageOps.exif_transpose(img)

        # 缩放（保持宽高比，不放大小图）
        img.thumbnail(MAX_SIZE, Image.LANCZOS)

        # 转成 RGB 以便保存为 JPEG（处理带透明通道 / 调色板模式的图片）
        if img.mode in ("RGBA", "LA", "P"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            background.paste(img, mask=img.split()[-1])
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")

        img.save(dst_path, "JPEG", quality=JPEG_QUALITY, optimize=True)


def main():
    total = 0
    generated = 0
    skipped = 0
    failed = []

    for src_path in iter_images(SRC_DIR):
        total += 1
        dst_path = thumb_path_for(src_path)

        if not needs_update(src_path, dst_path):
            skipped += 1
            continue

        try:
            make_thumbnail(src_path, dst_path)
            generated += 1
            print(f"[OK]   {src_path} -> {dst_path}")
        except Exception as e:
            failed.append((src_path, str(e)))
            print(f"[FAIL] {src_path}: {e}")

    print("\n========== 完成 ==========")
    print(f"共扫描图片: {total}")
    print(f"新生成/更新: {generated}")
    print(f"跳过(已存在且未变化): {skipped}")
    if failed:
        print(f"失败: {len(failed)} 个")
        for p, err in failed:
            print(f"  - {p}: {err}")


if __name__ == "__main__":
    main()
