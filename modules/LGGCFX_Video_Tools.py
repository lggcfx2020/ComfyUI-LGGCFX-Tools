"""
帧数计算器节点 - ComfyUI v0.3.46 兼容版本

该节点用于根据输入的每秒帧数(FPS)和秒数计算总帧数，
支持所有参数的输入连接和输出连接功能。
"""
# 添加ComfyUI根目录到Python路径并导入Node类
#from pathlib import Path
#import folder_paths,torch,os
import torch
#from ..tool.utils import get_audio,validate_path,strip_path,hash_path
from ..tool.logger import logger
from typing import Tuple
from ..tool.audio import AUDIO
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
    #logger.info(f'LGGCFX_resolution')
    # 预设尺寸映射: 键为显示名称，值为(width, height)元组
    # 分类说明:
    # - 横屏格式: 宽>高，适合视频播放
    # - 竖屏格式: 高>宽，适合移动设备
    # - 正方形格式: 宽=高，适合社交媒体
    # - LatLong格式: 2:1比例，适合360度全景视频
    size_map = {
        "768x432 33w(横屏)": (768, 432),
        "832x480 39w(横屏)": (832, 480),
        "960x544 52w(横屏)": (960, 544),
        "1024x768 78w(横屏HD)": (1024, 768),

        "1067x600 64w(横屏HD)": (1067, 600),
        "1138x640 72w(横屏HD)": (1138, 640),
        "1173x660 77w(横屏HD)": (1173, 660),
        "1209x680 82w(横屏HD)": (1209, 680),
        "1244x700 87w(横屏HD)": (1244, 700),
        
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
                "custom_width": ("INT", {"default": 832, "min": 1, "max": 16384, "step": 1}),
                "custom_height": ("INT", {"default": 480, "min": 1, "max": 16384, "step": 1}),
                "preset_size": (
                    list(cls.size_map.keys()),
                    {"default": "768x432 (横屏)"}
                ),
                "use_vertical_screen": ("BOOLEAN", {"default": False, "label": "转成竖屏"}),
            },
        }
    
    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "resolution"
    CATEGORY = "Utilities"
        
    def resolution(self, use_custom_size, custom_width, custom_height, preset_size,use_vertical_screen):
        #logger.info(f'执行后重置触发器resolution：\t{use_reversal}\n')
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


"""
音频加载和处理类，用于ComfyUI节点系统
提供音频文件选择、加载和验证功能
"""
class LGGCFX_audio:   
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "audio": ("AUDIO",),
                # 开始时间参数，默认为0
                "start_time": (
                    "STRING",
                    {
                        "default": "0:00",
                    },
                ),
                # 持续时间参数，默认为0（表示加载整个音频）
                "end_time": (
                    "STRING",
                    {
                        "default": "0:00",
                    },
                ),
                # 每秒帧数参数，默认为16
                "fps": (
                    "INT",
                    {
                        "default": 25,
                        "min": 1,
                        "max": 240,
                        "step": 1
                    },
                ),
            },
            "optional": {
                "formula": ("STRING", {"label": "帧数计算公式", "default": "(a*b)", "multiline": True, "placeholder": "使用a代表音频采样点数，支持多行公式\n例如:\n# 这是注释\nresult = a\nresult // 2 # 返回结果"}),
            },
        }

    # 节点分类
    CATEGORY = "Utilities"

    # 返回类型定义
    RETURN_TYPES = ("AUDIO", "INT", "INT", "INT", "FLOAT", "INT")
    # 返回值名称
    RETURN_NAMES = ("audio", "duration_seconds", "duration_ms", "fps", "fps_float", "total_frames")
    # 要调用的主要函数
    FUNCTION = "load_audio"

    def load_audio(self, audio: AUDIO, start_time: str = "0:00", end_time: str = "0:00", fps: int = 16, formula: str = "(a*b)") -> Tuple[AUDIO, int, int, int, int, float]:
        """
        加载音频文件并返回处理后的音频数据和音频持续时间
        
        参数:
            audio: 输入音频数据
            start_time: 开始时间，格式为"分:秒"
            end_time: 结束时间，格式为"分:秒"
            fps: 每秒帧数
            formula: 自定义帧数计算公式，使用a代表采样点数，b代表fps
            
        返回:
            tuple: (处理后的音频数据, 音频持续时间(秒，整数), 音频持续时间(毫秒，整数), 总帧数(整数), fps(整数), fps(浮点数))
        """

        waveform: torch.Tensor = audio["waveform"]
        sample_rate: int = audio["sample_rate"]

        # Assume that no ":" in input means that the user is trying to specify seconds
        if ":" not in start_time:
            start_time = f"00:{start_time}"
        if ":" not in end_time:
            end_time = f"00:{end_time}"

        start_seconds_time = 60 * int(start_time.split(":")[0]) + int(
            start_time.split(":")[1]
        )
        start_frame = start_seconds_time * sample_rate
        if start_frame >= waveform.shape[-1]:
            start_frame = waveform.shape[-1] - 1

        end_seconds_time = 60 * int(end_time.split(":")[0]) + int(
            end_time.split(":")[1]
        )
        end_frame = end_seconds_time * sample_rate
        if end_frame >= waveform.shape[-1]:
            end_frame = waveform.shape[-1] - 1
        if start_frame < 0:
            start_frame = 0
        if end_frame < 0:
            end_frame = 0

        if start_frame > end_frame:
            raise ValueError(
                "AudioCrop：开始时间必须小于结束时间，且需在音频时长范围内。"
            )

        # 计算加载的音频持续时间（以秒为单位，保留整数）
        duration_seconds = int((end_frame - start_frame) / sample_rate)
        # 计算加载的音频持续时间（以毫秒为单位，保留整数）
        duration_ms = int((end_frame - start_frame) / sample_rate * 1000)
        
        # 计算总帧数，支持自定义公式
        try:
            # 使用eval计算自定义公式，a=sample_count, b=fps
            total_frames = eval(formula, {'__builtins__': None}, {'a': duration_seconds, 'b': fps})
            # 确保结果为整数
            total_frames = int(total_frames)
        except Exception as e:
            # 公式错误时使用默认计算
            total_frames = int(round(fps * duration_seconds))

        return (
            {
                "waveform": waveform[..., start_frame:end_frame],
                "sample_rate": sample_rate,
            },
            duration_seconds,
            duration_ms,
            fps,
            float(fps),
            total_frames
        )


# 节点注册映射
NODE_CLASS_MAPPINGS = {
    "LGGCFX_time_frame": LGGCFX_time_frame,
    "LGGCFX_resolution": LGGCFX_resolution,
    "LGGCFX_audio":LGGCFX_audio
}

# 节点显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "LGGCFX_time_frame": "🧮LGGCFX_FrameRateCalculator",
    "LGGCFX_resolution": "📹LGGCFX_VideoResolutionWwitching",
    "LGGCFX_audio": "🎵LGGCFX_audio"
}