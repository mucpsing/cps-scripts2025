from PIL import Image
import os
from typing import Optional


def couver_img(img_path: str, info_template: str, output_path: str) -> None:
    """
    将目标图片按照模板图片的尺寸和元数据进行处理并输出

    Args:
        img_path: 目标图片路径
        info_template: 模板图片路径（用于获取尺寸、DPI等元数据）
        output_path: 输出图片路径
    """
    # 验证文件存在性
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"目标图片不存在: {img_path}")
    if not os.path.exists(info_template):
        raise FileNotFoundError(f"模板图片不存在: {info_template}")

    # 打开模板图片
    with Image.open(info_template) as template_img:
        # 获取模板图片尺寸
        template_width, template_height = template_img.size

        # 直接在模板图片上清除内容
        if template_img.mode == "RGBA":
            # 对于RGBA模式，使用透明色填充
            clear_color = (0, 0, 0, 0)
        else:
            # 对于其他模式，使用白色填充
            if template_img.mode == "RGB":
                clear_color = (255, 255, 255)
            elif template_img.mode == "L":  # 灰度模式
                clear_color = 255
            else:
                # 其他模式转换为RGB处理
                template_img = template_img.convert("RGB")
                clear_color = (255, 255, 255)

        # 使用填充色清除模板内容
        template_img.paste(clear_color, [0, 0, template_width, template_height])

        # 打开目标图片
        with Image.open(img_path) as source_img:
            # 计算目标图片的新尺寸（保持宽高比）
            source_width, source_height = source_img.size
            new_width = template_width
            new_height = int((template_width / source_width) * source_height)

            # 调整目标图片大小
            resized_source = source_img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # 计算垂直居中位置
            y_position = (template_height - new_height) // 2

            # 如果目标图片是RGBA模式，需要确保模板也是RGBA以支持透明度
            if resized_source.mode == "RGBA" and template_img.mode != "RGBA":
                template_img = template_img.convert("RGBA")

            # 将目标图片转换为与模板相同的模式
            if resized_source.mode != template_img.mode:
                resized_source = resized_source.convert(template_img.mode)

            # 粘贴目标图片到模板上
            if resized_source.mode == "RGBA":
                # 使用alpha通道作为掩码粘贴
                template_img.paste(resized_source, (0, y_position), resized_source)
            else:
                template_img.paste(resized_source, (0, y_position))

        # 保存输出图片，保留模板的元数据
        save_kwargs = {}

        # 保留DPI信息
        if hasattr(template_img, "info") and "dpi" in template_img.info:
            save_kwargs["dpi"] = template_img.info["dpi"]

        # 根据输出格式设置保存参数
        output_ext = os.path.splitext(output_path)[1].lower()

        if output_ext in [".jpg", ".jpeg"]:
            save_kwargs["quality"] = 95
            # JPEG不支持透明度，转换为RGB
            if template_img.mode == "RGBA":
                template_img = template_img.convert("RGB")

        # 保存图片
        template_img.save(output_path, **save_kwargs)


# 使用示例
if __name__ == "__main__":
    # 示例用法
    try:
        couver_img(img_path="input.jpg", info_template="template.png", output_path="output.jpg")
        print("图片处理完成！")
    except Exception as e:
        print(f"处理失败: {e}")
