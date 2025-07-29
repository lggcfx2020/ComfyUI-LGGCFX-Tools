"""
帧数计算器节点 - ComfyUI v0.3.46 兼容版本

该节点用于根据输入的每秒帧数(FPS)和秒数计算总帧数，
支持所有参数的输入连接和输出连接功能。
"""
import torch
import sys
from pathlib import Path

# 添加ComfyUI根目录到Python路径并导入Node类
import sys
from pathlib import Path

class LGGCFX_Tool():
    def __init__(self):
        pass

    """
    帧数计算器节点类
    
    功能: 通过每秒帧数和秒数计算总帧数
    计算公式: 总帧数 = 每秒帧数 × 秒数 (四舍五入取整)
    """
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
    RETURN_NAMES = ("fps","fps_f", "seconds", "total_frames")
    # 指定节点执行的核心函数
    FUNCTION = "calculate_total_frames"
    # 指定节点在ComfyUI菜单中的分类路径 Utilities实用工具
    CATEGORY = "Utilities"
    

    # 计算总帧数
    def calculate_total_frames(self, fps, seconds, formula="(a*b)+1"):
        """
        计算总帧数的核心方法
        
        参数:
            fps (float): 每秒帧数
            seconds (float): 秒数
        
        返回:
            tuple: 包含三个元素的元组
                - fps: 输入的每秒帧数
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
            print(f"公式计算错误: {str(e)}, 将使用默认公式 a*b")
        return (fps, float(fps), seconds, total_frames)

# 节点注册映射
NODE_CLASS_MAPPINGS = {
    "LGGCFX_Tool": LGGCFX_Tool
}

# 节点显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "LGGCFX_Tool": "🧮LGGCFX_帧数计算器"
}