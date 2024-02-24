import chess.engine
from lc_tools._leela_board import LeelaBoard
import numpy as np
import torch.nn as nn
import torch


class LeelaEngine():
    def __init__(self, name, model, k=None, seed=0):
        self.model = model
        self.device = list(model.parameters())[0].device
        self.rng = np.random.default_rng(seed)
        self.k = k
        self.name = name

    def play(self, board):
        lc_board = LeelaBoard(board)
        deserialised = lc_board.deserialize_features(lc_board.serialize_features())

        out = self.model(
            torch.tensor(deserialised).float().unsqueeze(0).to(self.device)
        )
        logits = out[0]
        legal_logit_idxs, legal_uci_moves = lc_board.generate_legal_indices()
        legal_logits = logits[:, legal_logit_idxs]
        probs = nn.Softmax(dim=-1)(legal_logits).squeeze(0)
        probs = probs.cpu().detach().numpy()
        sorted_probs_idxs = np.argsort(probs)[::-1]
        probs = probs[sorted_probs_idxs]
        if self.k is not None:
            sorted_probs_idxs = sorted_probs_idxs[: self.k]
            probs = probs[: self.k]
            probs = probs / np.sum(probs)
        move_logit_idx = self.rng.choice(len(probs), p=probs)
        return legal_uci_moves[sorted_probs_idxs[move_logit_idx]]

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    def __hash__(self) -> int:
        return hash(self.name)
