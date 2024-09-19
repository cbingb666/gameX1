from abc import abstractmethod
import time
from calc import calculate_point_on_circle, dir_to_angle
from pynput.mouse import Button, Controller
from pynput import keyboard
import pygetwindow as gw
from keyCodes import keyCodes
from keyMapConfigs import getConfigByKey, getTypeByKey, keyMapConfigs

mouse = Controller()

class Action:
    def __init__(self, key, keys: set, baseX, baseY, config):
        self.baseX = baseX
        self.baseY = baseY
        self.config = config
        self.key = key
        self.keys = keys
    
    @abstractmethod
    def press(self, key, x, y, radius):
        pass

    @abstractmethod
    def release(self):
        pass

class ActionRocker(Action):
    def press(self):
        if not self.hasOtherKey(self.config['key'],self.keys, self.key):
            self.release()
        angle = dir_to_angle(self.key, self.keys)
        offset = calculate_point_on_circle(self.config['x'], self.config['y'], self.config['radius'], angle)
        time.sleep(0.01)
        mouse.position = (self.baseX + offset['x'], self.baseY + offset['y'])
        time.sleep(0.01)
        mouse.press(Button.left)
        time.sleep(0.01)
    def release(self):
        mouse.release(Button.left)
        
    def hasOtherKey(self, a = [], c = {}, b = 'up'):
        # 求集合a和集合c的交集
        intersection = set(a) & c - {b}
        # 检查交集是否不为空且不包含b
        exists = intersection and b not in intersection
        return exists

        
class ActionTap(Action):
    def press(self):
        self.release()
        time.sleep(0.01)
        mouse.position = (self.baseX + self.config['x'], self.baseY + self.config['y'])
        time.sleep(0.01)
        mouse.press(Button.left)
        time.sleep(0.01)
    def release(self):
        mouse.release(Button.left)
        
class ActionRoulette(Action):
    def press(self):
        self.release()
        dir = self.config['dirs'][self.config['key'].index(self.key)]
        angle = dir_to_angle(dir)
        offset = calculate_point_on_circle(self.config['x'], self.config['y'], self.config['radius'], angle)
        time.sleep(0.01)
        mouse.position = (self.baseX + offset['x'], self.baseY + offset['y'])
        time.sleep(0.03)
        mouse.press(Button.left)
        time.sleep(0.03)
        offset = calculate_point_on_circle(self.config['x'], self.config['y'], self.config['radius'] + 20, angle)
        mouse.position = (self.baseX + offset['x'], self.baseY + offset['y'])
        time.sleep(0.01)
        
    def release(self):
        mouse.release(Button.left)
        
actionsMaps = {
    'ActionRocker': ActionRocker,
    'ActionTap': ActionTap,
    'ActionRoulette': ActionRoulette
}
        
class ActionControl():
    
    def __init__(self):
        self.baseX = 0
        self.baseY = 0
        self.currentAction = None
        self.previousAction = None
        self.keys = set()
        self.lock = True
        self.keymapWidget = None
    
    def updateBasePosition(self, postion):
        self.baseX = postion[0]
        self.baseY = postion[1]
        
    def addAction(self, key, config):
        Action = actionsMaps[config['type']]
        self.currentAction = Action(key, self.keys, self.baseX, self.baseY, config)
        self.currentAction.press()
        
    def removeAction(self, key):
        self.currentAction.release()
        
    def addPressKey(self, key):
        if(key in self.keys):
            return
        config = getConfigByKey(key)
        if config is None:
            return
            
        self.keys.add(key)
        self.addAction(key, config=config)
        
    def removePressKey(self, key):
        print('release',key)
        if(key not in self.keys):
            return
        config = getConfigByKey(key)
        if config is None:
            return 
        
        self.removeAction(key)
        self.keys.remove(key)
        
        # 释放按键后，检查是否还有其他已经按下的按键，有则再次按下
        if len(self.keys):
            for k in self.keys:
                config = getConfigByKey(k)
                self.addAction(k, config=config)
    
        
    def on_key_press(self, key):
        if self.lock:
            return
        self.updateBasePosition(gw.getWindowGeometry(gw.getActiveWindow()))
        
        key = self.toKeyStr(key)
            
        if key == '.':
            self.debugPosition()
                
        self.addPressKey(key)
      
            
    def on_key_release(self, key):
        if self.lock:
            return
        
        key = self.toKeyStr(key)
        self.removePressKey(key)
        
    def debugPosition(self):
        print(mouse.position[0] - self.last_active_window_geometry[0], mouse.position[1] - self.last_active_window_geometry[1])

        
    def toKeyStr(self, key):
        if isinstance(key, keyboard.Key) and key in keyCodes:
            key = keyCodes[key]

        if isinstance(key, keyboard.KeyCode):
            key = key.char
        return key
