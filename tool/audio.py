from typing import TypedDict
from torch import Tensor


class AUDIO(TypedDict):
    """
    必填字段：
        waveform（torch.Tensor）：包含音频数据的张量。形状：[批次，声道，帧]。
        sample_rate（int）：音频数据的采样率。
    """

    waveform: Tensor
    sample_rate: int
