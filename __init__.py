"""
ComfyUI-LGGCFX-Tools 插件初始化文件

该文件负责导出节点映射关系，使ComfyUI能够发现并加载插件中的自定义节点。
"""
#from .LGGCFX_Tool import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
import importlib

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
module_list = [
    "LGGCFX_Video_Tools",
]
for module_name in module_list:
    imported_module = importlib.import_module(".modules.{}".format(module_name), __name__)

    NODE_CLASS_MAPPINGS = {**NODE_CLASS_MAPPINGS, **imported_module.NODE_CLASS_MAPPINGS}
    NODE_DISPLAY_NAME_MAPPINGS = {**NODE_DISPLAY_NAME_MAPPINGS, **imported_module.NODE_DISPLAY_NAME_MAPPINGS}



# 导出节点映射供ComfyUI使用
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']