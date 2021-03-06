import logging
import torch
import torch.nn as nn


class TransE(nn.Module):
    def __init__(self, params):
        super(TransE, self).__init__()
        self.params = params
        self.ent_embeddings = nn.Embedding(self.params.total_ent, self.params.embedding_dim, max_norm=1)
        self.rel_embeddings = nn.Embedding(self.params.total_rel, self.params.embedding_dim)

        self.criterion = nn.MarginRankingLoss(self.params.margin, reduction='sum')

        self.init_weights()

        logging.info('Initialized the model successfully!')

    def init_weights(self):
        nn.init.xavier_uniform_(self.ent_embeddings.weight.data)
        nn.init.xavier_uniform_(self.rel_embeddings.weight.data)

    def get_score(self, h, t, r):
        return torch.norm(h + r - t, self.params.p_norm, -1)

    def forward(self, batch_h, batch_t, batch_r, batch_y):
        h = self.ent_embeddings(torch.from_numpy(batch_h))
        t = self.ent_embeddings(torch.from_numpy(batch_t))
        r = self.rel_embeddings(torch.from_numpy(batch_r))

        score = self.get_score(h, t, r)

        pos_score = score[0: int(len(score) / 2)]
        neg_score = score[int(len(score) / 2): len(score)]

        loss = self.criterion(pos_score, neg_score, torch.Tensor([-1]))
        return loss, pos_score, neg_score
