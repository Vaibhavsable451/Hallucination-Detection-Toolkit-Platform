# 04 - Hallucination Detection Toolkit

Two complementary detectors that check whether an answer is **grounded** in its source context:

| Detector | Needs API key | How it works |
|---|---|---|
| `LexicalGroundingChecker` | No | Sentence-level content-word overlap + number/entity checks |
| `LLMClaimVerifier` | Yes | Extracts atomic claims, verifies each as SUPPORTED / CONTRADICTED / NOT_ENOUGH_INFO |

```bash
pip install -r requirements.txt
python -m src.demo            # offline lexical demo
python -m src.demo --llm      # adds LLM claim verification
python -m unittest discover tests
```
The report gives per-sentence scores, flagged unsupported claims, and an overall **faithfulness score** you can use as a release gate (e.g. block answers < 0.8).
