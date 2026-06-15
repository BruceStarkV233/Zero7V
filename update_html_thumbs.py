#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 index.html（或其他指定的 html 文件）里 <img src="images/xxx.png" ...>
的 src 自动改写为对应的缩略图路径 images/thumbs/xxx.jpg

不会改动 data-full="images/xxx.png"（保留原图路径，供 Lightbox 大图使用）。

用法：
  python update_html_thumbs.py            # 默认处理 index.html
  python update_html_thumbs.py index.html about.html

建议：
  在运行 generate_thumbnails.py 生成缩略图之后再运行这个脚本。
  会自动生成一份 .bak 备份文件，方便出错时还原。
"""

import re
import sys
import shutil

# 匹配形如 src="images/场景/xxx.png" 的字符串，但不匹配已经是
# images/thumbs/... 的（避免重复处理）
SRC_PATTERN = re.compile(
    r'src="images/(?!thumbs/)([^"]+?)\.(png|jpe?g|gif|bmp|webp|tiff?)"',
    re.IGNORECASE,
)


def convert(html_text):
    def repl(m):
        rel_path_no_ext = m.group(1)
        return 'src="images/thumbs/%s.jpg"' % rel_path_no_ext

    new_text, count = SRC_PATTERN.subn(repl, html_text)
    return new_text, count


def main(files):
    if not files:
        files = ["index.html"]

    for fname in files:
        try:
            with open(fname, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            print(f"[跳过] 找不到文件: {fname}")
            continue

        new_content, count = convert(content)

        if count == 0:
            print(f"[无改动] {fname}: 没有匹配到需要替换的 src")
            continue

        backup_name = fname + ".bak"
        shutil.copyfile(fname, backup_name)

        with open(fname, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"[完成] {fname}: 替换了 {count} 处 img src -> 缩略图路径")
        print(f"        原文件已备份为 {backup_name}")


if __name__ == "__main__":
    main(sys.argv[1:])
