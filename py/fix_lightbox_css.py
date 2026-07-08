import os

def fix_lightbox_logic(file_path="index.html"):
    if not os.path.exists(file_path):
        print(f"❌ 错误：未找到文件 '{file_path}'")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. 检查并注入精准的内联兼容样式，强制让 lightbox--active 生效
    # 我们把这段样式直接挂在 </body> 标签前，确保拥有最高优先级
    compat_style = """
  <style>
    .lightbox.lightbox--active {
      opacity: 1 !important;
      pointer-events: all !important;
      background: rgba(10, 11, 12, 0.98) !important;
    }
    /* 确保大图居中且正常缩放 */
    .lightbox__container {
      position: fixed; inset: 0; display: flex; flex-direction: column; z-index: 9999;
    }
    #js-lb-image {
      max-width: 90% !important;
      max-height: 80vh !important;
      object-fit: contain !important;
      box-shadow: 0 20px 60px rgba(0,0,0,0.7) !important;
    }
  </style>
"""

    if "lightbox.lightbox--active" in content:
        print("ℹ️ 提示：兼容性样式似乎已经存在，跳过注入。")
    else:
        content = content.replace("</body>", compat_style + "</body>")
        print("✔ 成功：已注入 .lightbox--active 状态兼容样式。")

    # 2. 检查脚本中需要的计数器 ID 是否在页面中缺失
    # 如果缺失，我们在 js-lb-close 按钮附近安全地补上它们，防止 JS 报 Null 错误瘫痪
    if "js-lb-current" not in content:
        # 寻找常见的关闭按钮或灯箱内部结构作为锚点
        if 'id="js-lb-close"' in content:
            missing_dom = '<div style="display:none;"><span id="js-lb-current">1</span><span id="js-lb-total">1</span></div>'
            content = content.replace('id="js-lb-close"', f'id="js-lb-close"{missing_dom}')
            print("✔ 成功：已隐式补全 js-lb-current / js-lb-total 计数器锚点，阻止脚本崩溃。")

    # 写回修改
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("🚀 修复完成！请刷新浏览器测试点击放大效果。")

if __name__ == "__main__":
    fix_lightbox_logic()