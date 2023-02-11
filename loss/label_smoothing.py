from pdb import set_trace as bp

import torch
import torch.nn as nn
import torch.nn.functional as F

class LabelSmoothing(nn.Module):
    
    def __init__(self, smoothing, pad_idx, cls_idx):
        super(LabelSmoothing, self).__init__()
        self.smoothing = smoothing
        self.pad_idx = pad_idx
        self.cls_idx = cls_idx
        
    def forward(self, pred, target):  # pred (B, S, V), target (B, S)
        # Note: preds are expected to be after log
        B, S, V = pred.shape
        # (B, S, V) -> (B * S, V); (B, S) -> (B * S)
        pred = pred.contiguous().view(-1, V)
        target = target.contiguous().view(-1)
        
        # prior (uniform)
        dist = self.smoothing * torch.ones_like(pred) / (V - 2)
        # add smoothed ground-truth to prior (args: dim, index, src (value))
        dist.scatter_(1, target.unsqueeze(-1).long(), 1-self.smoothing)
        # make the padding token to have zero probability
        dist[:, self.pad_idx] = 0
        # ?? mask: 1 if target == pad_idx; 0 otherwise
<<<<<<< HEAD
=======
        # bp()
>>>>>>> 77e77b40aeeb3b1923d7fbad3ca64895d5e70e6c
        mask = torch.nonzero((target == self.pad_idx) | (target == self.cls_idx))
        
        if mask.sum() > 0 and len(mask) > 0:
            # dim, index, val
            dist.index_fill_(0, mask.squeeze(), 0)
<<<<<<< HEAD
        
        n_tokens = ((target != self.pad_idx) & (target != self.cls_idx)).sum()

=======

        n_tokens = ((target != self.pad_idx) & (target != self.cls_idx)).sum()
            
>>>>>>> 77e77b40aeeb3b1923d7fbad3ca64895d5e70e6c
        return F.kl_div(pred, dist, reduction='sum') / n_tokens
