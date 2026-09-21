# BE-06 – Prediction & XAI Integration

## Prediction service – in-process V1
- [ ] Load joblib model artifact in FastAPI
- [ ] Validate model metadata/feature version
- [ ] Build feature vector
- [ ] Call loaded model
- [ ] Validate model output
- [ ] Save prediction
- [ ] Save model version
- [ ] Save target reference

## XAI
- [ ] Compute local explanation bằng SHAP hoặc method đã chốt
- [ ] Save top factors
- [ ] Map technical feature → readable label
- [ ] Generate safe wording
- [ ] Store method/version

## Failure handling
- [ ] Model unavailable
- [ ] Feature missing
- [ ] Model load/inference failure
- [ ] Unsupported model version

## API
- [ ] GET /predictions/latest
- [ ] GET /predictions/{id}
- [ ] GET /predictions/{id}/explanation

## Tests
- [ ] Valid model response
- [ ] Invalid response rejected
- [ ] Model load/inference failure fallback
- [ ] Explanation linked to prediction
- [ ] No prediction when insufficient data


## V1 Constraint
- [ ] Không tạo AI microservice riêng
- [ ] Model artifact/version path lấy từ config
