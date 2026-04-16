# AI Real Estate Agent — Project 2 Brief Walkthrough

## Overview

A two-stage LLM prompt chain connected by an ML model, served via FastAPI in Docker. Natural language query in, structured price prediction + interpretation out.

---

## ML Pipeline

- Three-way train/validation/test split with no leakage
- Select 8–12 features from the Ames Housing dataset during EDA
- Distinguish ordinal from nominal categoricals for encoding
- Scaling is needed if using linear models (linear models are sensitive to feature magnitude); tree-based models don't require it, but including a scaler keeps the pipeline model-agnostic
- Use a scikit-learn `Pipeline` wrapping a `ColumnTransformer` (with `SimpleImputer`, `OrdinalEncoder`, `OneHotEncoder`, `StandardScaler`) plus the model — this enforces fit-on-train-only structurally
- Compare at least two model types, serialize the winner with `joblib`
- Evaluate on test exactly once

---

## LLM Prompt Chain

- **Stage 1** — extracts feature values from natural language and reports which features were found vs. missing (completeness signal). Does not predict.
- **Stage 2** — receives extracted features + ML prediction + training summary stats, produces a narrative interpretation (not just a restatement of the number)
- Test two prompt variants for Stage 1 across 3+ queries, log results, pick the winner with evidence

---

## Pydantic Schemas

### Schema 1 — Extracted Features

| Field | Type | Description |
|---|---|---|
| *(12 feature fields)* | `Optional[...]` | Typed feature values, nullable if not found |
| `extracted_features` | `list[str]` | Features successfully extracted |
| `missing_features` | `list[str]` | Features still needed from user |
| `completeness` | `float` | e.g. `0.75` for 9/12 found |

### Schema 2 — Combined Response

| Field | Type | Description |
|---|---|---|
| `extracted_features` | `ExtractedFeatures` | The full Schema 1 object |
| `predicted_price` | `float` | ML model output |
| `interpretation` | `str` | Stage 2 narrative |

---

## Error Handling

- Catch API errors, schema validation failures, and malformed LLM output at **both** stages
- Demonstrate one failure case (e.g. intentionally bad input or mocked bad LLM response)

---

## Deployment

- FastAPI POST route: query in, validated JSON out, model loads at startup
- UI (Streamlit/Gradio) runs separately and calls the FastAPI endpoint
- UI shows extracted features, lets user fill gaps before prediction runs, displays prediction + interpretation
- Docker contains the FastAPI app + serialized model + all chain code

---

## Proving No Data Leakage

- Train/validation/test split happens **before** any fitting
- All transformers are inside the `Pipeline` — confirm with `print(pipeline)` or `pipeline.named_steps`
- scikit-learn structurally prevents `fit` being called on validation or test data

---

## Outliers

- Remove outliers from **training data only**
- Leave validation and test sets untouched — they represent real-world data your model will encounter
