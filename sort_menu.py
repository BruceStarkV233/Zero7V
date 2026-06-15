import os
from bs4 import BeautifulSoup

# 获取当前脚本所在目录及文件路径
current_dir = os.path.dirname(os.path.abspath(__file__))
html_file = os.path.join(current_dir, 'index.html')

# ═══════════════════════════════════════════════════════════════
#  🌟 自定义排序配置区（完全由你编辑）
# ═══════════════════════════════════════════════════════════════
# 规则说明：
# 1. 填入你在网页按钮上看到的 data-filter 属性值。
# 2. 这里的先后顺序，就是网页上菜单显示的绝对顺序。
# 3. 如果某个菜单没写在这里，它会被自动排在最后面，确保不会丢失菜单。
# ═══════════════════════════════════════════════════════════════

# 1. 一级主菜单的顺序
ORDER_MAIN = [
    "角色", 
    "道具", 
    "场景",
    "生物", 
    "all", 
    "学生时代作品"
]

# 2. 二级子菜单的顺序（例如“角色”和“道具”内部的下拉子项）
ORDER_SUB = [
    # 角色子项排序
    "角色/卡通角色",
    "角色/metahuman_数字人",
    "角色/服装",
    
    # 道具子项排序
    "道具/文物"
    "道具/食物",
    "道具/硬表面",
]

# ═══════════════════════════════════════════════════════════════

def sort_menu_nodes(menu_list_node, order_rules):
    """根据给定的顺序规则，对列表节点下的 <li> 元素进行重新排序"""
    if not menu_list_node:
        return
    
    # 提取当前层级所有的直接子 <li> 节点
    items = menu_list_node.find_all('li', recursive=False)
    if not items:
        return

    def get_sort_key(li_node):
        # 寻找 <li> 内部的 <button> 标签获取它的 data-filter 属性值
        btn = li_node.find('button', class_='filter__btn')
        filter_val = btn.get('data-filter', '') if btn else ''
        
        # 如果在用户定义的排序规则里，返回其索引位置；找不到则排在最后面(赋予无穷大)
        if filter_val in order_rules:
            return order_rules.index(filter_val)
        return float('inf')

    # 按计算出的权重进行升序排序
    sorted_items = sorted(items, key=get_sort_key)

    # 从 HTML 树中清空原有的顺序，按新顺序重新附加
    menu_list_node.clear()
    for item in sorted_items:
        menu_list_node.append(item)
        
        # 🟢 深度递归：如果当前菜单项包含子菜单（下拉列表），同步对其进行子项排序
        sub_ul = item.find('ul', class_='filter__dropdown')
        if sub_ul:
            sort_menu_nodes(sub_ul, ORDER_SUB)

def main():
    if not os.path.exists(html_file):
        print(f"❌ 错误：在当前目录下没有找到【index.html】文件！")
        input("\n按下回车键退出...")
        return

    print("🔍 正在读取 index.html 并解析导航菜单...")
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # 定位最外层的一级菜单容器 <ul>
    main_nav = soup.find('ul', class_='filter__main-nav')

    if not main_nav:
        print("❌ 错误：未能在网页中定位到 <ul class=\"filter__main-nav\"> 容器。")
        print("请确认你已经运行过一次 update_html.py 生成了初始菜单。")
        input("\n按下回车键退出...")
        return

    # 开始执行排序
    print("⚡ 正在根据你的自定义规则重新排列菜单顺序...")
    sort_menu_nodes(main_nav, ORDER_MAIN)

    # 写回文件
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print("\n🎉 成功！index.html 中的菜单顺序已按照你的配置完美更新！")
    print("👉 现在刷新浏览器即可看到全新的菜单顺序。")
    input("\n按下回车键退出...")

if __name__ == '__main__':
    main()