from typing import Any as any_type
from comfy import model_management
from ..tool.logger import logger

# 自定义字符串代理类，用于在ComfyUI节点中表示'接受任何类型'的输入
class AnyTypeProxy(str):
    # 重写相等比较方法，始终返回True
    def __eq__(self, _):
        return True
    # 重写不等比较方法，始终返回False
    def __ne__(self, _):
        return False
# 创建一个特殊的类型标记，表示接受任何类型的输入
any_type = AnyTypeProxy("*")

# VRAM 预留设置器节点类，用于配置ComfyUI中的额外显存预留
class VRAMReserver:
    @classmethod
    def INPUT_TYPES(s):
        # 定义节点的输入参数
        return {
            "required": {
                # 接受任何类型的输入，用于连接到其他节点
                "anything": (any_type, {}),
                # 显存预留量（GB），范围0.6-...，步长0.1
                "reserved": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.5,
                    "step": 0.1,
                    "display": "reserved (GB)"
                }),
            },
            # 隐藏参数，由ComfyUI内部使用
            "hidden": {"unique_id": "UNIQUE_ID", "extra_pnginfo": "EXTRA_PNGINFO"}
        }

    # 定义节点的输出类型
    RETURN_TYPES = (any_type,)
    # 定义输出端口的名称
    RETURN_NAMES = ("output",)
    # 标记为输出节点
    OUTPUT_NODE = True
    # 指定要调用的方法名称
    FUNCTION = "set_reserved_vram"

    # 节点分类
    CATEGORY = "Utilities"

    def set_reserved_vram(self, anything, reserved, unique_id=None, extra_pnginfo=None):
        # 将预留显存设置为指定的值（转换为字节）
        model_management.EXTRA_RESERVED_VRAM = int(reserved * 1024 * 1024 * 1024)
        # 打印设置信息到控制台
        logger.info(f'额外保留的显存={reserved}GB')
        # 返回输入的anything，保持节点链的连续性
        return (anything,)

# 节点类映射，用于ComfyUI注册节点
NODE_CLASS_MAPPINGS = {
    "VRAMReserver": VRAMReserver
}
# 节点显示名称映射，定义在UI中显示的名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "VRAMReserver": "⚙️LGGCFX_SetReservedVRAM(GB)"
}
