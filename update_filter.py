#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

def update_gallery_filter():
    # ==========================================================
    # 核心修复：自动获取当前 Python 脚本所在的绝对路径，确保一定能找到 index.html
    # ==========================================================
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "index.html")

    if not os.path.exists(file_path):
        print(f"❌ 错误：在以下路径未找到文件：\n   {file_path}")
        print("\n💡 请检查：")
        print("1. 这个 Python 脚本是否确实和 'index.html' 放在【同一个文件夹】下？")
        print("2. 你的网页文件名是不是叫 'index.html'？如果是大写 'Index.html' 请改成小写。")
        return False

    print(f"🔍 成功定位文件！正在读取:\n   {file_path} ...")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 读取文件失败：{e}")
        return False

    # ==========================================
    # 精确层级隔离算法 JavaScript 核心代码
    # ==========================================
    new_filter_logic = """    filterButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            // 1. 切换按钮激活状态样式
            document.querySelector('.filter__btn.is-active')?.classList.remove('is-active');
            this.classList.add('is-active');

            // 2. 获取当前点击按钮的过滤值（例如: "all", "场景", "角色", "角色/卡通角色"）
            const filterValue = this.getAttribute('data-filter');

            galleryItems.forEach(item => {
                const itemMeta = item.getAttribute('data-meta') || '';

                if (filterValue === 'all') {
                    item.style.display = 'block'; // 'all' 显示所有图片
                } else {
                    // 判断图片的 data-meta 路径是否以当前过滤的目录名开头
                    if (itemMeta.startsWith(filterValue)) {
                        
                        // 【严格层级隔离算法】
                        // 1. 截取掉当前过滤前缀部分
                        const remainingPath = itemMeta.substring(filterValue.length);
                        // 2. 去除可能残余的头部斜杠，得到相对当前目录的文件/目录路径
                        const cleanPath = remainingPath.startsWith('/') ? remainingPath.substring(1) : remainingPath;
                        
                        // 3. 核心判断：如果 cleanPath 中还包含斜杠 '/'，说明它位于更深层的子目录中。
                        // 为了大类别下只显示当前目录内的图片，此时必须将其隐藏。
                        if (!cleanPath.includes('/')) {
                            item.style.display = 'block';   // 直属当前目录的文件，显示
                        } else {
                            item.style.display = 'none';    // 属于子目录的文件，隐藏
                        }
                    } else {
                        item.style.display = 'none';        // 路径完全不匹配，隐藏
                    }
                }
            });

            // 3. 动态更新照片总数及刷新 Lightbox 的可见图片池（确保前后翻页正常）
            updateGalleryState();
        });
    });"""

    # 正则表达式：精准匹配原本的 filterButtons.forEach(...) 块结构
    filter_pattern = re.compile(
        r"filterButtons\.forEach\(btn\s*=>\s*\{.*?"
        r"\}\);\s*\}\);\s*\}\);", 
        re.DOTALL
    )

    # 兜底方案：如果上述严格匹配未成功，使用兼容性更广的循环块匹配
    if not filter_pattern.search(content):
        filter_pattern = re.compile(
            r"filterButtons\.forEach\(btn\s*=>\s*\{.*?"
            r"updateGalleryState\(\);\s*\}\);\s*\}\);", 
            re.DOTALL
        )

    if filter_pattern.search(content):
        try:
            # 执行就地替换
            updated_content = filter_pattern.sub(new_filter_logic, content)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"\n✨ 成功！大类别【只显示当前目录、隐藏子目录图片】的过滤逻辑已成功写入！")
            print("💡 提示：你可以直接刷新网页查看隔离后的正确过滤效果了。")
            return True
        except Exception as e:
            print(f"❌ 写入文件失败：{e}")
            return False
    else:
        print("\n❌ 错误：未能精准匹配到 index.html 中原有的 filterButtons 过滤逻辑块。")
        print("💡 原因：这通常是因为您在此之前已经手动对该 JS 脚本块做过修改。")
        print("   如果您之前手动改动过，请直接在 index.html 底部手动替换对应的 filterButtons 逻辑。")
        return False

if __name__ == "__main__":
    try:
        update_gallery_filter()
    except Exception as main_err:
        print(f"❌ 运行过程中发生未知错误: {main_err}")
    
    print("\n-------------------------------------------")
    input("按 【Enter (回车键)】 退出程序...")
    sys.exit()