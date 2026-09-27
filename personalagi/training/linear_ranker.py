from __future__ import annotations

import math
import random
import re
from collections import Counter
from dataclasses import dataclass
from typing import Iterable

TOKEN_RE = re.compile(r"[a-z0-9']+")


def _tokens(text: str) -> list[str]:
    toks = TOKEN_RE.findall(text.lower())
    return toks + [f"{a}__{b}" for a, b in zip(toks, toks[1:])]


@dataclass
class RankerMetrics:
    accuracy: float
    mean_margin: float
    n: int


class PairwiseLinearRanker:
    """Tiny auditable pairwise reward/ranking baseline trained with logistic SGD.

    This is intentionally not an LLM reward model. It provides a real learned baseline
    that can be trained/reproduced offline with the Python standard library.
    """

    def __init__(self, *, min_df: int = 2, lr: float = 0.08, l2: float = 1e-4, epochs: int = 25, seed: int = 7):
        self.min_df = min_df
        self.lr = lr
        self.l2 = l2
        self.epochs = epochs
        self.seed = seed
        self.vocab: dict[str, int] = {}
        self.weights: list[float] = []
        self.bias = 0.0

    def fit_vocab(self, rows: Iterable[dict]) -> None:
        df = Counter()
        for row in rows:
            seen = set(_tokens(row['prompt'] + ' ' + row['chosen'] + ' ' + row['rejected']))
            df.update(seen)
        terms = sorted(t for t, c in df.items() if c >= self.min_df)
        self.vocab = {t: i for i, t in enumerate(terms)}
        self.weights = [0.0] * len(terms)

    def _vec(self, prompt: str, response: str) -> dict[int, float]:
        counts = Counter(_tokens(prompt + ' [response] ' + response))
        out: dict[int, float] = {}
        for token, count in counts.items():
            idx = self.vocab.get(token)
            if idx is not None:
                out[idx] = 1.0 + math.log(count)
        norm = math.sqrt(sum(v * v for v in out.values())) or 1.0
        return {i: v / norm for i, v in out.items()}

    @staticmethod
    def _diff(a: dict[int, float], b: dict[int, float]) -> dict[int, float]:
        keys = set(a) | set(b)
        return {i: a.get(i, 0.0) - b.get(i, 0.0) for i in keys}

    def _margin(self, diff: dict[int, float]) -> float:
        return self.bias + sum(self.weights[i] * v for i, v in diff.items())

    def fit(self, rows: list[dict]) -> 'PairwiseLinearRanker':
        if not rows:
            raise ValueError('cannot train on empty data')
        self.fit_vocab(rows)
        rng = random.Random(self.seed)
        order = list(range(len(rows)))
        for epoch in range(self.epochs):
            rng.shuffle(order)
            eta = self.lr / (1.0 + 0.06 * epoch)
            for j in order:
                row = rows[j]
                c = self._vec(row['prompt'], row['chosen'])
                r = self._vec(row['prompt'], row['rejected'])
                diff = self._diff(c, r)
                margin = max(-30.0, min(30.0, self._margin(diff)))
                # d log(1+exp(-m))/dm = sigmoid(m)-1
                grad_factor = 1.0 / (1.0 + math.exp(-margin)) - 1.0
                for i, x in diff.items():
                    grad = grad_factor * x + self.l2 * self.weights[i]
                    self.weights[i] -= eta * grad
                self.bias -= eta * grad_factor
        return self

    def score(self, prompt: str, response: str) -> float:
        v = self._vec(prompt, response)
        return self.bias + sum(self.weights[i] * x for i, x in v.items())

    def evaluate(self, rows: list[dict]) -> RankerMetrics:
        if not rows:
            return RankerMetrics(0.0, 0.0, 0)
        margins = [self.score(r['prompt'], r['chosen']) - self.score(r['prompt'], r['rejected']) for r in rows]
        return RankerMetrics(
            accuracy=sum(m > 0 for m in margins) / len(margins),
            mean_margin=sum(margins) / len(margins),
            n=len(margins),
        )

    def top_features(self, n: int = 20) -> list[tuple[str, float]]:
        inv = {i: t for t, i in self.vocab.items()}
        pairs = [(inv[i], w) for i, w in enumerate(self.weights)]
        return sorted(pairs, key=lambda x: abs(x[1]), reverse=True)[:n]
