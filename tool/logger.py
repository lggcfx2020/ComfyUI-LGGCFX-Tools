import sys
import copy
import logging


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[0;36m",  # CYAN
        "INFO": "\033[0;32m",  # GREEN
        "WARNING": "\033[0;33m",  # YELLOW
        "ERROR": "\033[0;31m",  # RED
        "CRITICAL": "\033[0;37;41m",  # WHITE ON RED
        "RESET": "\033[0m",  # RESET COLOR
    }

    def format(self, record):
        colored_record = copy.copy(record)
        levelname = colored_record.levelname
        seq = self.COLORS.get(levelname, self.COLORS["RESET"])
        colored_record.levelname = f"{seq}{levelname}{self.COLORS['RESET']}"
        return super().format(colored_record)


#创建一个新的日志记录器
logger = logging.getLogger("VideoHelperSuite")
logger.propagate = False

#如果我们没有处理程序，则添加一个。
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(ColoredFormatter("[%(name)s] - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

#配置日志记录器
loglevel = logging.INFO
logger.setLevel(loglevel)


# 配置日志记录到文件（在插件顶部添加）
def setup_logger():
    logger = logging.getLogger("ComfyUIPlugin")
    logger.setLevel(logging.DEBUG)
    
    # 创建文件处理器
    file_handler = logging.FileHandler("plugin_debug.log")
    file_handler.setLevel(logging.DEBUG)
    
    # 创建格式化器并添加到处理器
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    # 添加处理器到logger
    if not logger.handlers:
        logger.addHandler(file_handler)
    
    return logger
