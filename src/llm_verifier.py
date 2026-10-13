from typing import List, Literal
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from src.config import get_llm

class Claims(BaseModel):
    claims: List[str]

class Verdict(BaseModel):
    label: Literal["SUPPORTED", "CONTRADICTED", "NOT_ENOUGH_INFO"]
    evidence: str

class LLMClaimVerifier:
    def __init__(self):
        self.llm = get_llm()

    def extract_claims(self, answer: str) -> List[str]:
        p = ChatPromptTemplate.from_template(
            "Split the answer into short, atomic, self-contained factual claims.\n\nAnswer: {a}")
        return (p | self.llm.with_structured_output(Claims)).invoke({"a": answer}).claims

    def verify(self, claim: str, context: str) -> Verdict:
        p = ChatPromptTemplate.from_template(
            "Context:\n{c}\n\nClaim: {cl}\n\nIs the claim SUPPORTED, CONTRADICTED, or NOT_ENOUGH_INFO "
            "according ONLY to the context? Quote the evidence (or 'none').")
        return (p | self.llm.with_structured_output(Verdict)).invoke({"c": context, "cl": claim})

    def check(self, answer: str, context: str):
        rows = [(c, self.verify(c, context)) for c in self.extract_claims(answer)]
        score = sum(v.label == "SUPPORTED" for _, v in rows) / len(rows) if rows else 1.0
        return rows, round(score, 2)
