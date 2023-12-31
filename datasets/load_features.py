import os
import pickle

import numpy as np
import torch
import torch.nn.functional as F


def load_pickle(load_path):
    with open(load_path, 'rb') as f:
        message_dict = pickle.load(f)
    return message_dict


def fill_missing_features(method, feature_size):
    if method == 'random':
        return torch.rand(1, feature_size)
    elif method == 'zero':
        return torch.zeros(1, feature_size).float()


def crop_a_segment(feature, start, end, duration):
    S, D = feature.shape
    start_quantile = start / duration
    end_quantile = end / duration
    start_idx = int(S * start_quantile)
    end_idx = int(S * end_quantile)
    # handles the case when a segment is too small
    if start_idx == end_idx:
        # if the small segment occurs in the end of a video
        # [S:S] -> [S-1:S]
        if start_idx == S:
            start_idx -= 1
        # [S:S] -> [S:S+1]
        else:
            end_idx += 1
    feature = feature[start_idx:end_idx, :]

    if len(feature) == 0:
        return None
    else:
        return feature


def pad_segment(feature, max_feature_len, pad_idx):
    S, D = feature.shape
    assert S <= max_feature_len
    # pad
    l, r, t, b = 0, 0, 0, max_feature_len - S
    feature = F.pad(feature, [l, r, t, b], value=pad_idx)
    return feature


def load_features_from_npy(feature_pkl, cfg, video_id, start, end, duration,
                           pad_idx, get_full_feat=False):

    stacks = {}
    if get_full_feat:
        stacks['orig_feat_length'] = {}

    # get audio feature
    try:
        stack_vggish = feature_pkl[video_id]['audio']
        stack_vggish = torch.tensor(stack_vggish.tolist()).float()

        if get_full_feat:
            stacks['orig_feat_length']['audio'] = stack_vggish.shape[0]
            stack_vggish = pad_segment(stack_vggish, cfg.pad_feats_up_to['audio'], pad_idx)
        else:
            stack_vggish = crop_a_segment(stack_vggish, start, end, duration)
    except FileNotFoundError:
        stack_vggish = None
    stacks['audio'] = stack_vggish
    # not elif
    # get video feature
    try:
        stack_rgb = feature_pkl[video_id]['rgb']
        stack_flow = feature_pkl[video_id]['flow']
        a=np.shape(stack_flow)
        b=np.shape(stack_rgb)
        if a[0] !=b[0]:
            z=np.zeros([int(abs(a[0]-b[0])),2048]).astype(np.float32)
            if a[0] < b[0]:
                stack_flow = np.concatenate((stack_flow,z),axis=0)
            else:
                stack_rgb = np.concatenate((stack_rgb,z),axis=0)
        stack_rgb = torch.tensor(stack_rgb.tolist()).float()
        stack_flow = torch.tensor(stack_flow.tolist()).float()
        if get_full_feat:
            stacks['orig_feat_length']['rgb'] = stack_rgb.shape[0]
            stacks['orig_feat_length']['flow'] = stack_flow.shape[0]
            stack_rgb = pad_segment(stack_rgb, cfg.pad_feats_up_to['video'], pad_idx)
            stack_flow = pad_segment(stack_flow, cfg.pad_feats_up_to['video'], pad_idx=0)
        else:
            stack_rgb = crop_a_segment(stack_rgb, start, end, duration)
            stack_flow = crop_a_segment(stack_flow, start, end, duration)
            nframes = min(stack_rgb.shape[0], stack_flow.shape[0])
            stack_rgb = stack_rgb[:nframes]
            stack_flow = stack_flow[:nframes]
    except FileNotFoundError:
        stack_rgb = None
        stack_flow = None
    assert stack_rgb.shape == stack_flow.shape
    stacks['rgb'] = stack_rgb
    stacks['flow'] = stack_flow

    return stacks

