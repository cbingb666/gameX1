

keyMapConfigs = [
    {
        'key': ['up', 'down', 'left', 'right'],
        'dirs': ['up', 'down', 'left', 'right'],
        'type': 'ActionRocker',
        "name": '遥杆',
        'x': 169.30859375,
        'y': 300.5390625,
        'radius': 45
    },
    {
        'key': 'c',
        'type': 'ActionTap',
        "name": '跳跃',
        'x': 755.76171875,
        'y': 336.07421875,
        'radius': 20
    },
    {
        'key': 'space',
        'type': 'ActionTap',
        "name": '闪避',
        'x': 698.7734375,
        'y': 374.57421875,
        'radius': 10
    },
    {
        'key': 'x',
        'type': 'ActionTap',
        "name": '攻击',
        'x': 700.15625,
        'y': 306.1953125,
        'radius': 10
    },
    {
        'key': ['1','2','3','4'],
        'dirs': ['up', 'down', 'left', 'right'],
        'type': 'ActionRoulette',
        "name": '技能盘',
        'x': 641.72265625, 
        'y': 250.26953125,
        'radius': 20
    },
    {
        'key': 'a',
        'type': 'ActionTap',
        "name": '底部1',
        'x': 526.0390625, 
        'y': 366.296875,
        'radius': 10
    },
    {
        'key': 's',
        'type': 'ActionTap',
        "name": '底部1',
        'x': 587.21484375, 
        'y': 365.53515625,
        'radius': 10
    },
    {
        'key': 'd',
        'type': 'ActionTap',
        "name": '回环1',
        'x': 642.94921875, 
        'y': 353.38671875,
        'radius': 10
    },
    {
        'key': 'f',
        'type': 'ActionTap',
        "name": '回环2',
        'x': 621.19921875, 
        'y': 302.05078125,
        'radius': 10
    },
    {
        'key': 'g',
        'type': 'ActionTap',
        "name": '回环3',
        'x': 701.65625, 
        'y': 230.98046875,
        'radius': 10
    },
    {
        'key': 'v',
        'type': 'ActionTap',
        "name": '回环4',
        'x': 754.94140625, 
        'y': 263.04296875,
        'radius': 10
    },
    {
        'key': 'q',
        'type': 'ActionTap',
        "name": '顶栏1',
        'x': 625.59375, 
        'y': 152.734375,
        'radius': 10
    },
    {
        'key': 'w',
        'type': 'ActionTap',
        "name": '顶栏2',
        'x': 665.52734375, 
        'y': 152.37109375,
        'radius': 10
    },
    {
        'key': 'e',
        'type': 'ActionTap',
        "name": '顶栏3',
        'x': 700.34765625, 
        'y': 152.234375,
        'radius': 10
    },
    {
        'key': 'r',
        'type': 'ActionTap',
        "name": '顶栏4',
        'x': 739.46875, 
        'y': 152.30078125,
        'radius': 10
    },
    {
        'key': 't',
        'type': 'ActionTap',
        "name": '右上',
        'x': 756.01953125, 
        'y': 205.0625,
        'radius': 10
    },
]

    

def getConfigByKey(key: str):
    for config_item in keyMapConfigs:
            if isinstance(config_item['key'], list):
                for k in config_item['key']:
                    if key == k:
                        return config_item
            elif key == config_item['key']:
                return config_item
            
            
def getTypeByKey(key: str):
    config = getConfigByKey(key)
    if config:
        return config['type']