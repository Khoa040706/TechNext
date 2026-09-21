# AI-01 – Data & Feature Pipeline

## Stack
- Python 3.12
- pandas
- NumPy
- Jupyter/Colab hoặc script Python tái lập được

## Data collection
- [ ] Quiz event
- [ ] Question result
- [ ] Coding submission
- [ ] Test result
- [ ] Error type
- [ ] Progress event
- [ ] Resource interaction
- [ ] Mastery snapshot

## Cleaning
- [ ] Timestamp normalization
- [ ] Missing values
- [ ] Duplicate attempts
- [ ] Invalid scores
- [ ] Invalid test counts

## Feature engineering
- [ ] Quiz rolling average
- [ ] Quiz trend
- [ ] Coding pass rate
- [ ] Retry count
- [ ] Error rate
- [ ] Mastery
- [ ] Difficulty history
- [ ] Recent activity

## Leakage checks
- [ ] Feature timestamp <= prediction timestamp
- [ ] No future outcome in aggregation
- [ ] Split before sensitive transforms
- [ ] Scaler fit only train

## Reproducibility
- [ ] Dataset snapshot ID
- [ ] Feature version
- [ ] Seed
- [ ] Config


## Coding telemetry caveat
- [ ] execution_source included
- [ ] trust_level included
- [ ] Client Pyodide result không bị nhầm với server-authoritative label
