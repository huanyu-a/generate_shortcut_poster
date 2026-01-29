from PIL import Image, ImageDraw, ImageFont
import textwrap

# 创建1920x1300的基础图像（增加高度以适应8个板块）
width, height = 1920, 1080
img = Image.new('RGB', (width, height), '#0A0E27')
draw = ImageDraw.Draw(img)

# 加载背景纹理（可选，降低透明度避免冲突）
try:
    bg = Image.open('output/blob.png')
    bg = bg.resize((width, height), Image.Resampling.LANCZOS)
    # 降低背景强度，避免与主内容竞争
    bg = bg.convert('RGBA')
    # 创建一个半透明层
    alpha = Image.new('L', (width, height), 56)  # 30% 透明度
    bg.putalpha(alpha)
    img.paste(bg, (0, 0), bg)
except:
    # 如果背景加载失败，使用纯色背景
    pass

# 定义颜色
WHITE = '#FFFFFF'
CYAN = '#00D4FF'
BLUE = '#0099FF'
PURPLE = '#9966FF'
GREEN = '#00FF99'
YELLOW = '#FFCC00'
PINK = '#FF66CC'
ORANGE = '#FF9900'
GRAY = '#808080'  # 添加灰色定义

# 加载字体 - 简化字体加载
chinese_fonts = [
    'C:\\Windows\\Fonts\\msyhbd.ttc',  # 微软雅黑粗体
    'C:\\Windows\\Fonts\\msyh.ttc',   # 微软雅黑
    'C:\\Windows\\Fonts\\simhei.ttf',  # 黑体
]

# 加载基础字体
font_chinese = None
for font_path in chinese_fonts:
    try:
        font_chinese = ImageFont.truetype(font_path, 16)
        break
    except:
        continue

if not font_chinese:
    font_chinese = ImageFont.load_default()

# 设置标题和快捷键字体
try:
    font_title = ImageFont.truetype('C:\\Windows\\Fonts\\msyhbd.ttc', 32)  # 标题字体
    font_key = ImageFont.truetype('C:\\Windows\\Fonts\\msyhbd.ttc', 16)   # 快捷键字体
except:
    font_title = font_chinese
    font_key = font_chinese

# 加载emoji专用字体
try:
    font_emoji = ImageFont.truetype('C:\\Windows\\Fonts\\seguiemj.ttf', 32)  # Segoe UI Emoji
except:
    try:
        font_emoji = ImageFont.truetype('C:\\Windows\\Fonts\\seguisym.ttf', 32)  # Segoe UI Symbol
    except:
        font_emoji = font_title  # 备用方案

# 快捷键数据
sections = [
    {
        'emoji': '🏠',
        'title': '通用快捷键',
        'color': CYAN,
        'x': 50, 'y': 80,
        'shortcuts': [
            ('Win', '打开或关闭开始菜单'),
            ('Win + A', '打开操作中心(通知栏)'),
            ('Win + I', '打开设置'),
            ('Win + L', '锁定电脑'),
            ('Win + P', '切换投影模式'),
            ('Win + S', '打开搜索'),
            ('Win + V', '剪贴板历史'),
            ('Win + X', '快速链接菜单'),
            ('Win + 1~9', '任务栏程序'),
            ('Alt + F4', '关闭窗口'),
            ('Ctrl + Alt + Del', '打开安全选项'),
            ('Ctrl+Shift+Esc', '任务管理器'),
        ]
    },
    {
        'emoji': '🖥️',
        'title': '窗口与桌面管理',
        'color': BLUE,
        'x': 480, 'y': 80,
        'shortcuts': [
            ('Win + Tab', '打开任务视图'),
            ('Win + Ctrl + D', '新建虚拟桌面'),
            ('Win + Ctrl + ←/→', '切换虚拟桌面'),
            ('Win + Ctrl + F4', '关闭虚拟桌面'),
            ('Win + D', '显示/隐藏桌面'),
            ('Win + Shift + ←/→', '移动显示器'),
            ('Alt + Tab', '切换窗口'),
            ('Win + ←', '左半屏'),
            ('Win + →', '右半屏'),
            ('Win + ↑', '最大化'),
            ('Win + ↓', '最小化'),
            ('Win + Home', '最小化其他'),
        ]
    },
    {
        'emoji': '✏️',
        'title': '文本编辑',
        'color': ORANGE,
        'x': 905, 'y': 80,
        'shortcuts': [
            ('Ctrl + C', '复制'),
            ('Ctrl + X', '剪切'),
            ('Ctrl + V', '粘贴'),
            ('Ctrl + Z', '撤销'),
            ('Ctrl + Y', '恢复'),
            ('Ctrl + A', '全选'),
            ('Ctrl + F', '查找'),
            ('Ctrl + H', '替换'),
            ('Ctrl + ←/→', '按单词移动光标'),
            ('Ctrl + Shift + ←/→', '按单词选择文本'),
            ('Shift + Home/End', '选择到行首/行尾'),
            ('Ctrl + Home/End', '跳转到文档开头/结尾'),
        ]
    },
    {
        'emoji': '🎮',
        'title': '游戏与截图',
        'color': GREEN,
        'x': 1335, 'y': 80,
        'shortcuts': [
            ('Win + G', 'Xbox Game Bar'),
            ('Win + Alt + R', '录制'),
            ('PrtSc', '截屏到剪贴板'),
            ('Win + PrtSc', '截屏并保存'),
            ('Win + Shift + S', '区域截图'),
            ('Alt + PrtSc', '窗口截图'),
        ]
    },
    {
        'emoji': '⚙️',
        'title': '系统命令',
        'color': PURPLE,
        'x': 50, 'y': 580,
        'shortcuts': [
            ('WIN+R', '启动运行'),
            ('cmd', '命令提示符'),
            ('powershell', 'PowerShell'),
            ('msconfig', '系统配置'),
            ('mstsc', '远程桌面'),
            ('devmgmt.msc', '设备管理器'),
            ('diskmgmt.msc', '磁盘管理'),
            ('services.msc', '服务管理'),
            ('control', '控制面板'),
            ('regedit', '注册表编辑器'),
            ('taskmgr', '任务管理器'),
            ('sysdm.cpl', '系统属性'),
        ]
    },
    {
        'emoji': '📁',
        'title': '文件资源管理器',
        'color': YELLOW,
        'x': 480, 'y': 580,
        'shortcuts': [
            ('Win + E', '打开文件资源管理器'),
            ('Ctrl + N/W', '打开新/关闭窗口'),
            ('Ctrl + E/F', '搜索框'),
            ('Ctrl + Shift + N', '新建文件夹'),
            ('Alt + Enter', '显示属性'),
            ('Alt + →/←', '前进/后退'),
            ('Alt + ↑', '打开上一级文件夹'),
            ('F2', '重命名选中项目'),
            ('F5', '刷新窗口'),
            ('Delete', '删除到回收站'),
            ('Shift + Delete', '永久删除'),
            ('Ctrl + 鼠标滚轮', '调整图标大小'),
        ]
    },
    {
        'emoji': '🌐',
        'title': '浏览器',
        'color': GREEN,
        'x': 905, 'y': 580,
        'shortcuts': [
            ('Ctrl + T', '新建标签页'),
            ('Ctrl + W', '关闭当前标签页'),
            ('Ctrl + Shift + T', '恢复刚关闭的标签页'),
            ('Ctrl + Tab', '切换到下一个标签页'),
            ('Ctrl + Shift + Tab', '切换到上一个标签页'),
            ('Ctrl + 数字键', '跳转到对应顺序的标签页'),
            ('Ctrl + L 或 F6', '定位到地址栏'),
            ('Ctrl + R 或 F5', '刷新页面'),
            ('Ctrl + F5', '强制刷新（忽略缓存）'),
            ('Ctrl + D', '收藏当前页面'),
            ('Ctrl + H', '打开历史记录'),
            ('Ctrl + J', '打开下载列表'),
        ]
    },
    {
        'emoji': '♿',
        'title': '辅助功能',
        'color': PINK,
        'x': 1335, 'y': 580,
        'shortcuts': [
            ('Win + +', '放大'),
            ('Win + -', '缩小'),
            ('Win + Esc', '关闭放大镜'),
            ('Ctrl + Alt + I', '反色'),
            ('Win + Ctrl + O', '屏幕键盘'),
            ('Win + Ctrl + N', '讲述人设置'),
        ]
    },
]

# 绘制标题
title_font = ImageFont.truetype('C:\\Windows\\Fonts\\msyhbd.ttc', 48)  # 使用微软雅黑粗体
draw.text((width // 2, 30), 'Windows 快捷键大全', font=title_font, fill=WHITE, anchor='mt')

# 绘制每个区域
for section in sections:
    x, y = section['x'], section['y']
    color = section['color']

    # 绘制卡片背景（半透明）
    card_width, card_height = 390, 440
    if section['title'] in ['游戏与截图', '辅助功能']:
        card_height = 260  # 内容较少的板块用小高度

    # 绘制圆角矩形背景
    overlay = Image.new('RGBA', (card_width, card_height), (10, 20, 50, 180))
    img.paste(overlay, (x, y), overlay)

    # 绘制边框
    draw.rectangle([x, y, x + card_width, y + card_height], outline=color, width=2)

    # 绘制标题背景 - 增加高度以适应更大的字体
    draw.rectangle([x, y, x + card_width, y + 60], fill=color)

    # 绘制标题 - 使用专门字体分别绘制emoji和文字
    emoji_text = section.get('emoji', '')
    title_text = section['title']
    
    # 计算总宽度
    emoji_bbox = draw.textbbox((0, 0), emoji_text, font=font_emoji) if emoji_text else (0, 0, 0, 0)
    title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
    
    emoji_width = emoji_bbox[2] - emoji_bbox[0] if emoji_text else 0
    title_width = title_bbox[2] - title_bbox[0]
    total_width = emoji_width + title_width + (10 if emoji_text else 0)  # emoji和文字之间的间距
    
    # 计算起始位置（居中）
    start_x = x + (card_width - total_width) // 2
    text_y = y + 15
    
    # 绘制emoji（如果存在）
    if emoji_text:
        draw.text((start_x, text_y), emoji_text, font=font_emoji, fill='white')
        start_x += emoji_width + 10
    
    # 绘制文字
    draw.text((start_x, text_y), title_text, font=font_title, fill='white')

    # 绘制快捷键 - 优化布局和间距
    start_y = y + 80
    for i, (key, desc) in enumerate(section['shortcuts']):
        row_y = start_y + i * 30  # 适当行间距

        # 绘制按键背景
        key_bbox = draw.textbbox((0, 0), key, font=font_key)
        key_width = key_bbox[2] - key_bbox[0]
        draw.rectangle([x + 15, row_y - 2, x + 15 + key_width + 20, row_y + 22], fill=(30, 40, 80), outline=color,
                       width=1)

        # 绘制按键文字（去掉描边效果）
        draw.text((x + 25, row_y), key, font=font_key, fill=color)

        # 绘制描述（增加左边距）
        draw.text((x + 200, row_y), desc, font=font_chinese, fill=WHITE)

# 添加底部装饰线
draw.line([(100, height - 40), (width - 100, height - 40)], fill=CYAN, width=2)
draw.text((width // 2, height - 25), 'Windows Shortcuts Reference', font=font_chinese, fill=GRAY, anchor='mt')

# 保存
img.save('output/windows_shortcuts_poster_final.png')
print("Poster saved successfully!")
img
