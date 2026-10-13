import re
from dataclasses import dataclass, field
from typing import List

STOP = set("a an the is are was were be been of to in on for and or with by at from that this it as can may must will not no any all per".split())

def tokens(text):
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOP]

def numbers(text):
    return set(re.findall(r"\d+(?:[.,]\d+)?", text))

def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]

@dataclass
class SentenceResult:
    sentence: str
    overlap: float
    unsupported_numbers: List[str] = field(default_factory=list)
    grounded: bool = True

@dataclass
class Report:
    results: List[SentenceResult]
    faithfulness: float

class LexicalGroundingChecker:
    def __init__(self, threshold: float = 0.6):
        self.threshold = threshold

    def check(self, answer: str, context: str) -> Report:
        ctx_tokens, ctx_nums = set(tokens(context)), numbers(context)
        results = []
        for s in sentences(answer):
            toks = tokens(s)
            overlap = (sum(t in ctx_tokens for t in toks) / len(toks)) if toks else 1.0
            bad_nums = sorted(n for n in numbers(s) if n not in ctx_nums)
            results.append(SentenceResult(s, round(overlap, 2), bad_nums,
                                          overlap >= self.threshold and not bad_nums))
        score = sum(r.grounded for r in results) / len(results) if results else 1.0
        return Report(results, round(score, 2))
