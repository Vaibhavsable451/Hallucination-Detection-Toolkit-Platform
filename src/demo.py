import sys
from src.lexical import LexicalGroundingChecker

CONTEXT = open("data/handbook.txt", encoding="utf-8").read()
ANSWERS = {
    "faithful": "Employees receive 20 days of paid vacation per year. Unused days carry over up to 5 days.",
    "hallucinated": "Employees receive 25 days of paid vacation per year. Unused days carry over without limit. "
                    "The company also provides a free gym membership.",
}

for name, ans in ANSWERS.items():
    rep = LexicalGroundingChecker().check(ans, CONTEXT)
    print(f"\n=== {name} | faithfulness={rep.faithfulness} ===")
    for r in rep.results:
        flag = "OK " if r.grounded else "BAD"
        print(f"[{flag}] overlap={r.overlap} bad_numbers={r.unsupported_numbers} :: {r.sentence}")

if "--llm" in sys.argv:
    from src.llm_verifier import LLMClaimVerifier
    v = LLMClaimVerifier()
    rows, score = v.check(ANSWERS["hallucinated"], CONTEXT)
    print(f"\nLLM verifier faithfulness={score}")
    for claim, verdict in rows:
        print(f"  {verdict.label:16} {claim}")
