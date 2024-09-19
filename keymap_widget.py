import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QMouseEvent, QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QRectF

from calc import calculate_point_on_circle, dir_to_angle

class KeyMapWidget(QWidget):
    def __init__(self, key_map_configs, rect = (0,0,800,600)):
        super().__init__()
        self.key_map_configs = key_map_configs
        self.rect = rect
        self.initUI()
        # self.mouse_through = True

    def initUI(self):
        self.setGeometry(*self.rect)
        self.setWindowTitle('按键映射')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # 设置窗口无边框
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)  # 点击穿透
        self.setAttribute(Qt.WA_TranslucentBackground)  # 启用窗口的透明背景
        # self.setAttribute(Qt.WA_X11DoNotAcceptFocus)  # 启用窗口的透明背景
        # self.setFocusPolicy(Qt.NoFocus)
        self.setWindowOpacity(1)  # 设置窗口的透明度，1为完全不透明，0为完全透明
        self.show()
        self.clearFocus()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        font = QFont("Arial", 12)
        painter.setFont(font)

        for config in self.key_map_configs:
            x, y = config['x'], config['y']
            radius = config['radius'] - 5
            name = config["name"]
            # key = config["key"] if isinstance(config["key"], str)

            if config['type'] != 'ActionRocker' and config['type'] != 'ActionRoulette':
                # 绘制圆形控件
                painter.setBrush(QColor(255, 255, 255, 255))  # 半透明白色填充
                painter.drawEllipse(QRectF(x + radius + 5, y + radius + 5, 20, 20))
            
            # 设置字体颜色为红色
            painter.setPen(QColor(255, 0, 0))  # 设置画笔颜色为红色
            
            if config['type'] == 'ActionRocker' or config['type'] == 'ActionRoulette':
                for index, k in enumerate(config['key']):
                    key = config['dirs'][index]
                    pos = calculate_point_on_circle(config['x'], config['y'], config['radius'] + 30, dir_to_angle(key))
                    # 绘制文本
                    painter.drawText(QRectF(pos['x'] - 10, pos['y'] - 10, 20, 20), Qt.AlignCenter, k)
                    
            else:
                # 绘制文本
                painter.drawText(QRectF(x + radius + 5, y + radius + 5, 20, 20), Qt.AlignCenter, config['key'])
            
    def mouseReleaseEvent(self, event):
        event

    def mousePressEvent(self, event):
        # self.ignoreEvent()
        event.ignore()
        # QApplication.postEvent(wid, mEvent)
        # 忽略所有鼠标点击事件，因为点击穿透已经开启
        # event.ignore()
        # print(event)
        # if self.mouse_through:
        #     # 如果开启点击穿透，忽略鼠标点击事件
        #     event.ignore()
        # else:
        #     # 如果关闭点击穿透，处理鼠标点击事件
        #     event.accept()
        #     for config in self.key_map_configs:
        #         x, y = config['x'], config['y']
        #         radius = config['radius']
        #         if (event.x() - x) ** 2 + (event.y() - y) ** 2 <= radius ** 2:
        #             print(f"Clicked on {config['name']}")
        #             # 这里可以添加更多的逻辑，比如发送按键事件等
        #             break
        #     else:
        #         event.ignore()  # 如果没有点击任何配置的圆形，忽略事件