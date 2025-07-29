"""
帧数计算器节点 - ComfyUI v0.3.46 兼容版本

该节点用于根据输入的每秒帧数(FPS)和秒数计算总帧数，
支持所有参数的输入连接和输出连接功能。
"""
# 添加ComfyUI根目录到Python路径并导入Node类
import logging
from pathlib import Path
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

logger = setup_logger()

"""
帧数计算器节点类
功能: 通过每秒帧数和秒数计算总帧数
计算公式: 总帧数 = 每秒帧数 × 秒数 (四舍五入取整)
"""
class LGGCFX_time_frame():
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(cls):
        """
        定义节点的输入参数
        
        返回:
            dict: 包含输入参数配置的字典
                - fps: 每秒帧数，浮点型，范围0.1-120.0，默认30.0
                - seconds: 秒数，浮点型，范围0.1-3600.0，默认10.0
        """
        return {
            "required": {
                "fps": ("INT", {"default": 16, "min": 1, "max": 240, "step": 1}),
                "seconds": ("INT", {"default": 5, "min": 1, "max": 3600, "step": 1}),
            },
            "optional": {
                "formula": ("STRING", {"label": "计算公式", "default": "(a*b)+1", "multiline": True, "placeholder": "使用a代表fps，b代表seconds，支持多行公式\n例如:\n# 这是注释\nresult = a * b\nresult + 1 # 返回结果"}),
            },
        }
    
    # 定义输出参数的数据类型: (fps, seconds, total_frames)
    RETURN_TYPES = ("INT", "FLOAT","INT", "INT")
    # 定义输出参数的名称，将显示在节点输出端口
    RETURN_NAMES = ("fps","fps_float", "seconds", "total_frames")
    # 指定节点执行的核心函数
    FUNCTION = "time_frame"
    # 指定节点在ComfyUI菜单中的分类路径 Utilities实用工具
    CATEGORY = "Utilities"

    # 计算总帧数
    def time_frame(self, fps, seconds, formula="(a*b)+1"):
        """
        计算总帧数的核心方法
        
        参数:
            fps (float): 每秒帧数
            seconds (float): 秒数
        
        返回:
            tuple: 包含三个元素的元组
                - fps: 输入的每秒帧数
                - fps_float: 输入的每秒帧数(浮点数)
                - seconds: 输入的秒数
                - total_frames: 计算得到的总帧数（四舍五入取整）
        """
        try:
            # 使用eval计算自定义公式，a=fps, b=seconds
            # 将公式中的a和b映射到实际参数值
            total_frames = eval(formula, {'__builtins__': None}, {'a': fps, 'b': seconds})
            # 确保结果为整数
            total_frames = int(total_frames)
        except Exception as e:
            # 公式错误时使用默认计算
            total_frames = int(round(fps * seconds))
            #print(f"公式计算错误: {str(e)}, 将使用默认公式 a*b")
        return (fps, float(fps), seconds, total_frames)



"""分辨率选择节点

提供多种预设分辨率和自定义分辨率选项，支持横屏、竖屏、正方形和LatLong格式
"""
class LGGCFX_resolution:
    #logger.debug(f'LGGCFX_resolution')
    # 预设尺寸映射: 键为显示名称，值为(width, height)元组
    # 分类说明:
    # - 横屏格式: 宽>高，适合视频播放
    # - 竖屏格式: 高>宽，适合移动设备
    # - 正方形格式: 宽=高，适合社交媒体
    # - LatLong格式: 2:1比例，适合360度全景视频
    size_map = {
        "768x432 (横屏)": (768, 432),
        "832x480 (横屏)": (832, 480),
        "960x544 (横屏)": (960, 544),
        "1280x720 (横屏HD)": (1280, 720),
        "1920x1080 (横屏FHD)": (1920, 1080),
        "3840x2160 (4K横屏UHD)": (3840, 2160),
        "5760x3240 (6K横屏)": (5760, 3240),
        "7680x4320 (8K横屏)": (7680, 4320),

        "2048x1024 (2K横屏2)": (2048, 1024),
        "4096x2048 (4K横屏2)": (4096, 2048),
        "6144x3072 (6K横屏2)": (6144, 3072),
        "8192x4096 (8K横屏2)": (8192, 4096),

        "1024x1024 (1K正方屏)": (1024, 1024),
        "2048x2048 (2K正方屏)": (2048, 2048),
        "4096x4096 (4K正方屏)": (4096, 4096),
        "6144x6144 (6K正方屏)": (6144, 6144),
        "8192x8192 (8K正方屏)": (8192, 8192),
    }

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "use_custom_size": ("BOOLEAN", {"default": False}),
                "custom_width": ("INT", {"default": 480, "min": 1, "max": 16384, "step": 1}),
                "custom_height": ("INT", {"default": 832, "min": 1, "max": 16384, "step": 1}),
                "preset_size": (
                    list(cls.size_map.keys()),
                    {"default": "480x832 (竖屏)"}
                ),
                "use_vertical_screen": ("BOOLEAN", {"default": False, "label": "转成竖屏"}),
            },
        }
    
    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "resolution"
    CATEGORY = "Utilities"
        
    def resolution(self, use_custom_size, custom_width, custom_height, preset_size,use_vertical_screen):
        #logger.debug(f'执行后重置触发器resolution：\t{use_reversal}\n')
        """根据输入参数返回选定的分辨率

        Args:
            use_custom_size (bool): 是否使用自定义分辨率
            custom_width (int): 自定义宽度值
            custom_height (int): 自定义高度值
            preset_size (str): 预设分辨率选项
            use_vertical_screen (bool): 是否反转宽和高

        Returns:
            tuple: (width, height) - 选定的分辨率宽度和高度
        """

        #是否使用自定义分辨率
        if use_custom_size:
            width, height = custom_width, custom_height
                #return (custom_width, custom_height)
        else:
            # 根据选择的预设尺寸更新宽高
            width, height = self.size_map[preset_size]
        
        # 仅当宽度大于高度时才反转以确保竖屏
        if use_vertical_screen:
            if width > height:
                width, height = height, width
        #横屏
        else:
            if width < height:
                width, height = height,width

        # 返回更新后的宽高值
        return (width, height)


# 节点注册映射
NODE_CLASS_MAPPINGS = {
    "LGGCFX_time_frame": LGGCFX_time_frame,
    "LGGCFX_resolution": LGGCFX_resolution
}

# 节点显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "LGGCFX_time_frame": "🧮LGGCFX_FrameRateCalculator",
    "LGGCFX_resolution": "📹LGGCFX_VideoResolutionWwitching"
}