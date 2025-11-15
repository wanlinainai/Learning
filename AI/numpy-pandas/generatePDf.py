"""
快速生成 20MB PDF 文件的程序
使用 PyPDF2 和 reportlab 库生成包含文本和图形的大文件PDF
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import io

def generate_20mb_pdf(filename="output_20mb.pdf", target_size_mb=20, output_dir=None):
    """
    生成指定大小的PDF文件

    参数:
        filename: 输出文件名
        target_size_mb: 目标文件大小(MB)
        output_dir: 输出目录路径(可选)
    """
    # 如果指定了输出目录,则组合完整路径
    if output_dir:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        filepath = os.path.join(output_dir, filename)
    else:
        filepath = filename

    target_size = target_size_mb * 1024 * 1024  # 转换为字节

    # 注册中文字体（使用系统自带的中文字体）
    try:
        pdfmetrics.registerFont(TTFont('SimSun', 'C:/Windows/Fonts/simsun.ttc'))
        chinese_font = 'SimSun'
        print("✓ 成功加载宋体字体")
    except:
        try:
            pdfmetrics.registerFont(TTFont('SimHei', 'C:/Windows/Fonts/simhei.ttf'))
            chinese_font = 'SimHei'
            print("✓ 成功加载黑体字体")
        except:
            chinese_font = 'Helvetica'
            print("⚠ 警告: 无法加载中文字体，中文可能无法正常显示")

    # 创建PDF
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    # 丰富的中文内容
    chinese_paragraphs = [
        "人工智能技术的发展正在深刻改变着我们的生活方式和工作模式。从语音识别到图像处理，从自动驾驶到智能推荐系统，AI的应用无处不在。",
        "大数据时代的到来使得信息的收集、存储和分析变得前所未有的重要。企业通过数据分析来优化决策，提高效率，创造更大的商业价值。",
        "云计算技术为企业提供了灵活、可扩展的IT基础设施。通过云服务，企业可以降低成本，提高运营效率，快速响应市场变化。",
        "物联网将各种设备连接到互联网，实现设备之间的数据交换和智能控制。智能家居、智慧城市等应用场景正在逐步实现。",
        "区块链技术以其去中心化、不可篡改的特性，在金融、供应链、版权保护等领域展现出巨大的应用潜力。",
        "5G网络的普及为移动互联网带来了革命性的变化。更快的速度、更低的延迟使得更多创新应用成为可能。",
        "网络安全在数字化时代变得越来越重要。保护数据隐私、防范网络攻击是每个组织都必须重视的问题。",
        "软件工程的最佳实践包括代码审查、自动化测试、持续集成等。这些实践能够提高软件质量，减少bug。",
        "敏捷开发方法强调快速迭代、持续交付和团队协作。这种方法能够更好地适应需求变化，提高开发效率。",
        "开源软件促进了技术的共享和创新。许多优秀的开源项目为开发者提供了强大的工具和框架。"
    ]

    print(f"\n开始生成 {target_size_mb}MB 的PDF文件...")
    print(f"保存路径: {filepath}\n")

    page_count = 0
    lines_per_page = 55  # 增加每页行数

    # 预估需要的页数 (调整为每页约4-5KB，需要更多页)
    estimated_pages = int(target_size / 4500)  # 增加页数

    print(f"预计需要生成约 {estimated_pages} 页")
    print("正在生成中，请稍候...\n")

    for page_num in range(estimated_pages):
        page_count += 1

        # 页面标题
        c.setFont(chinese_font, 20)
        c.drawString(1*inch, height - 0.7*inch, f"测试文档 - 第 {page_count} 页")

        # 副标题
        c.setFont(chinese_font, 12)
        c.drawString(1*inch, height - 1.0*inch, f"本文档用于测试PDF文件生成功能 | 目标大小: {target_size_mb}MB")

        # 分隔线
        c.setStrokeColorRGB(0.3, 0.3, 0.3)
        c.line(0.5*inch, height - 1.15*inch, width - 0.5*inch, height - 1.15*inch)

        # 添加文本内容 - 使用更小的字体和行距以增加内容密度
        c.setFont(chinese_font, 9)
        y_position = height - 1.5*inch

        for i in range(lines_per_page):
            if y_position < 1.2*inch:
                break

            # 循环使用不同段落，并添加更多文字
            paragraph = chinese_paragraphs[i % len(chinese_paragraphs)]
            line_text = f"[行{i+1:03d}] {paragraph} (重复内容以增加文件大小) {paragraph[:30]}"

            c.drawString(0.5*inch, y_position, line_text)
            y_position -= 0.25*inch  # 减小行距以容纳更多内容

        # 添加装饰性图形元素 - 增加更多图形
        c.setStrokeColorRGB(0.2, 0.4, 0.8)
        c.setFillColorRGB(0.7, 0.85, 1.0)

        # 底部装饰条 - 增加数量
        for j in range(30):
            x_pos = 0.3*inch + j * 0.27*inch
            c.rect(x_pos, 0.5*inch, 0.2*inch, 0.15*inch, fill=1)

        # 顶部装饰
        for j in range(30):
            x_pos = 0.3*inch + j * 0.27*inch
            c.rect(x_pos, height - 0.4*inch, 0.2*inch, 0.1*inch, fill=1)

        # 侧边装饰 - 增加更多
        c.setFillColorRGB(0.9, 0.95, 1.0)
        c.rect(0.2*inch, height - 2*inch, 0.15*inch, 1.5*inch, fill=1)
        c.rect(width - 0.35*inch, height - 2*inch, 0.15*inch, 1.5*inch, fill=1)

        # 页脚信息
        c.setFont(chinese_font, 9)
        c.setFillColorRGB(0.4, 0.4, 0.4)
        footer_text = f"文档生成工具 | 页码: {page_count}/{estimated_pages} | 进度: {(page_count/estimated_pages*100):.1f}%"
        c.drawString(width/2 - 2*inch, 0.4*inch, footer_text)

        c.showPage()

        # 每200页显示一次进度
        if page_count % 200 == 0:
            print(f"已生成 {page_count} 页... (约 {page_count * 4.5 / 1024:.1f} MB)")

    # 保存PDF
    print(f"\n正在保存文件...")
    c.save()

    # 检查最终文件大小
    final_size = os.path.getsize(filepath)
    final_size_mb = final_size / 1024 / 1024

    print(f"\n{'='*50}")
    print(f"✓ PDF文件生成完成!")
    print(f"{'='*50}")
    print(f"文件路径: {filepath}")
    print(f"总页数: {page_count}")
    print(f"文件大小: {final_size_mb:.2f} MB")
    print(f"目标大小: {target_size_mb} MB")

    if final_size_mb < target_size_mb * 0.9:
        print(f"\n⚠ 注意: 文件大小未达到目标，可能需要增加页数")
    elif final_size_mb > target_size_mb * 1.1:
        print(f"\n⚠ 注意: 文件大小超出目标较多")
    else:
        print(f"\n✓ 文件大小符合预期!")

if __name__ == "__main__":
    # 指定输出目录
    output_directory = r"E:\work\hulianwangyiyuanhoutai\hospital_mbxfkj\src\main\resources\static"

    # 生成 20MB 的 PDF 文件到指定目录
    generate_20mb_pdf("output_20mb.pdf", target_size_mb=20, output_dir=output_directory)

    print(f"\n{'='*50}")
    print("✓ 所有操作完成!")
    print(f"{'='*50}\n")