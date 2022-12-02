from pdb import set_trace as bp
from functools import lru_cache

import torch
import numpy as np


def compute_iou(interval_1, interval_2):
        start_i, end_i = interval_1[0], interval_1[1]
        start, end = interval_2[0], interval_2[1]
        intersection = max(0, min(end, end_i) - max(start, start_i))
        union = min(max(end, end_i) - min(start, start_i), end-start + end_i-start_i)
        iou = float(intersection) / (union + 1e-8)
        return iou


def get_pooling_counts(N=64):
    assert N >= 16 and (N & (N-1) == 0)
    pooling_counts = [15]
    while N > 16:
        N /= 2
        pooling_counts.append(8)
    return pooling_counts 
    

@lru_cache(None)
def get_2d_position(N=64):
    """
    output:
        poolers_range: range of each poolers
        mask2d: mask of valid position
    """
    pooling_counts = get_pooling_counts(N)

    stride, offset = 1, 0
    mask2d = torch.zeros(N, N, dtype=torch.bool)
    mask2d[range(N), range(N)] = 1

    poolers_range = []
    for c in pooling_counts:
        for _ in range(c): 
            # fill a diagonal line 
            offset += stride
            i, j = range(0, N - offset, stride), range(offset, N, stride)
            
            mask2d[i, j] = 1
            poolers_range.append((i, j))
        stride *= 2
    return poolers_range, mask2d

@lru_cache(None)
def get_valid_position(N=64):
    poolers_range, _ = get_2d_position(N)
    valid_position = [(i,i) for i in range(N)]
    for i_range, j_range in poolers_range:
        for i, j in zip(i_range, j_range):
            valid_position.append((i, j))
    valid_position = np.array(valid_position)
    return valid_position


def get_valid_position_norm(N=64):
    vp = get_valid_position(N).copy()
    vp[:, 1] += 1
    vp = vp / float(N)
    return vp 


if __name__ == '__main__':
    get_valid_position(64)