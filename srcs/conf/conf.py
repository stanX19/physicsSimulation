import ast
import os
import configparser


class _Effects:
    def __init__(self):
        self.GRAVITY = 0
        self.AIR_RESISTANCE = 0
        self.COLLISION = True
        self.MATTER_REPEL = True
        self.VECTOR = 0
        self.TRAIL = False


class _Status:
    def __init__(self):
        self.SCREEN_SIZE = (1200, 700)
        self.WINDOW = None
        self.RUNNING = True
        self.OBJS = []
        self.BLACKHOLE = []
        self.BARRIERS = []
        self.object_kwargs = {}

    @property
    def CENTER(self):
        return self.SCREEN_SIZE[0] / 2, self.SCREEN_SIZE[1] / 2


Effects = _Effects()
colors = {
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "YELLOW": (255, 255, 0),
    "RED": (255, 0, 0),
    "CYAN": (0, 255, 255),
    "LIME": (0, 255, 0),
    "BLUE": (0, 0, 255),

    "BACKGROUND": (0, 0, 0)
}
Status = _Status()


def read_config(path: str):
    config_parser = configparser.RawConfigParser()
    config_file_path = path
    config_parser.read(config_file_path)
    return config_parser._sections


def init_configs():
    global Effects, colors, Status
    settings = read_config(r'assets\base_settings.cfg')
    config_path = settings["base_settings"]["default_cfg"]

    confdict = read_config(os.path.join("assets", config_path))

    Status.object_kwargs = {}
    Status.OBJS = []
    Status.BLACKHOLE = []
    Status.BARRIERS = []

    for key in confdict:
        if key in ["color", "effects", "status"]:
            if "color" == key:
                for color, data in confdict["color"].items():
                    colors[color.upper()] = ast.literal_eval(data)
            elif "effects" == key:
                for effect, data in confdict["effects"].items():
                    setattr(Effects, effect.upper(), ast.literal_eval(data))
            elif "status" == key:
                for _key, data in confdict["status"].items():
                    setattr(Status, _key.upper(), ast.literal_eval(data))
        else:
            Status.object_kwargs[key] = confdict[key]


if __name__ == '__main__':
    init_configs()
    print(colors)
