# 在使用 PIL 之前，需要 pip install pillow
from PIL import Image

# 设置下降的高度
Z_DOWN = 2  # 毫米
Z_UP = 0  # 毫米

XY_FEEDRATE = 4000  # X 和 Y 移动的速度
Z_FEEDRATE = 2500  # Z 轴移动的速度
SCALE_FACTOR = 0.3  # 毫米/点


def bitmap_to_gcode(image_path, output_path):
    image = Image.open(image_path)
    image = image.convert('1')  # 将图像转换为黑白模式
    width, height = image.size

    with open(output_path, 'w') as f:
        # 初始化 G-code 文件
        f.write("G21 ; 使用毫米单位\n")
        f.write("G90 ; 使用绝对坐标模式\n")
        f.write("G1 Z{} F{} ; 提起 Z 轴\n".format(Z_UP, Z_FEEDRATE))

        for y in range(height):
            if y % 2 == 0:
                x_range = range(width)  # 从左到右
            else:
                x_range = range(width - 1, -1, -1)  # 从右到左

            for x in x_range:
                pixel = image.getpixel((x, y))
                if pixel == 0:  # 如果像素是黑色
                    f.write("G1 X{} Y{} F{} ; 移动到 ({}, {})\n".format(x * SCALE_FACTOR, y * SCALE_FACTOR, XY_FEEDRATE,
                                                                        x * SCALE_FACTOR, y * SCALE_FACTOR))
                    f.write("G1 Z{} F{} ; 下降到 Z = {}\n".format(Z_DOWN, Z_FEEDRATE, Z_DOWN))
                    f.write("G1 Z{} F{} ; 提起 Z 轴\n".format(Z_UP, Z_FEEDRATE))

        # 结束 G-code
        f.write("G1 Z{} F{} ; 提起 Z 轴\n".format(Z_UP, Z_FEEDRATE))
        f.write("M2 ; 程序结束\n")


# 使用示例
bitmap_to_gcode('input.bmp', 'output.gcode')
