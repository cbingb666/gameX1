import sys
import threading
import time
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QEvent, QCoreApplication
import pygetwindow as gw
from pynput import keyboard
from action import ActionControl
from keyMapConfigs import keyMapConfigs
from keymap_widget import KeyMapWidget

# 定义自定义事件类型
class ActiveWindowChangeEvent(QEvent):
    def __init__(self, title):
        super().__init__(QEvent.Type(QEvent.registerEventType()))
        self.title = title
        
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Window Monitor Example')
        self.windowTitleName = 'Iphone镜像 Iphone镜像'
        self.actionControl = ActionControl()
        self.keyboardListen = keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release)
        self.keyboardListen.start()
        self.keymapWidget = None 

    def event(self, event):
        if isinstance(event, ActiveWindowChangeEvent):
            print(f"Active window changed: {event.title}")
            if event.title == self.windowTitleName:
                self.onFocusMirror()
            else:
                self.onBlurMirror()
            # 这里可以添加更多的逻辑，比如更新UI等
            return True
        return super().event(event)
    
    def on_key_press(self, key):
        self.actionControl.on_key_press(key)
        
    def on_key_release(self, key):
        self.actionControl.on_key_release(key)

    def onFocusMirror(self):
        
        self.actionControl.lock = False
        time.sleep(0.4)
        active_window = gw.getActiveWindow()
        active_geometry = gw.getWindowGeometry(active_window)
        self.actionControl.updateBasePosition(active_geometry)
        self.keymapWidget = KeyMapWidget(keyMapConfigs,active_geometry)
        self.keymapWidget.show()
        print('focus')

    def onBlurMirror(self):
        if self.keymapWidget is not None:
            self.keymapWidget.close()
        self.actionControl.lock = True

def monitor_active_window(main_window):
    last_active_title = None
    while True:
        active_window = gw.getActiveWindow()
        active_title = active_window.title() if active_window else None
        if last_active_title == active_title:
            continue
        event = ActiveWindowChangeEvent(active_title)
        QCoreApplication.postEvent(main_window, event)
        last_active_title = active_title
        sys.stdout.flush()
        time.sleep(0.1)

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    # 启动监控线程
    monitor_thread = threading.Thread(target=monitor_active_window, args=(main_window,))
    monitor_thread.daemon = True
    monitor_thread.start()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()