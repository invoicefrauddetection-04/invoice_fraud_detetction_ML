# ProcureGuard AI --- Model Interpretation Guide

> Internal RAG knowledge source. This document defines how ProcureGuard
> model outputs and explainability signals should be interpreted and
> communicated.

# Fraud Prediction

**Concept:** Binary fraud-risk classification

**Definition:**\
The ProcureGuard classifier produces a prediction for whether an invoice
resembles patterns learned for the fraud class or the non-fraud class.

**Preferred language:** - "The model classified this invoice as high
risk." - "The model prediction indicates elevated fraud risk." - "The
invoice was classified into the fraud-risk class by the model."

**Avoid:** - "This invoice is proven fraudulent." - "Fraud definitely
occurred." - "The model confirmed a crime."

**Interpretation rule:**\
A model prediction is an analytical risk assessment. It is not legal
proof of fraud and should be reviewed together with the underlying
invoice, supplier information, and relevant procurement controls.

------------------------------------------------------------------------

# Fraud Probability

**Concept:** Model confidence / fraud-class probability

**Definition:**\
A numerical model output representing the model's estimated probability
or confidence for the fraud class, according to the trained classifier.

**Preferred language:**\
"The model assigned a fraud-risk probability of X."

**Avoid:**\
"There is an X% factual probability that fraud occurred."

**Interpretation rule:**\
The probability describes the model's output under its learned patterns.
It must not be interpreted as a legally verified probability that fraud
actually occurred.

------------------------------------------------------------------------

# Risk Level

**Concept:** Human-readable presentation of model risk

**Definition:**\
A label such as Low, Medium, or High used by the application to
communicate model output more clearly.

**Interpretation rule:**\
Risk levels are application-level interpretations of model output and
must follow the thresholds configured by ProcureGuard.

**Preferred language:** - "Low model risk" - "Medium model risk" - "High
model risk"

**Avoid:** - "Safe supplier" - "Confirmed fraudulent supplier" -
"Legally fraudulent invoice"

**Threshold rule:**\
The RAG system must not invent Low/Medium/High probability thresholds.
It should use only thresholds explicitly configured by the application.

------------------------------------------------------------------------

# Explainability Signal

**Concept:** Feature contribution to a model prediction

**Definition:**\
An explainability method may identify which input features contributed
most strongly to an individual prediction.

**Interpretation:**\
A strong feature contribution means that the feature influenced the
model output for that prediction. It does not mean that the feature
independently proves fraud.

**Preferred language:**\
"`invoice_amount_zscore` was one of the stronger contributors to the
model prediction."

**Avoid:**\
"`invoice_amount_zscore` proves the invoice is fraudulent."

------------------------------------------------------------------------

# Positive Feature Contribution

**Concept:** Feature contribution toward the fraud-risk prediction

**Definition:**\
An explainability value may indicate that a feature pushed the model
output more strongly toward the fraud-risk class.

**Preferred language:**\
"This feature increased the model's fraud-risk assessment for this
invoice."

**Avoid:**\
"This feature is a fraud rule."

**Interpretation rule:**\
Contribution direction describes model behaviour, not an authoritative
procurement rule.

------------------------------------------------------------------------

# Negative Feature Contribution

**Concept:** Feature contribution away from the fraud-risk prediction

**Definition:**\
An explainability value may indicate that a feature pushed the model
output away from the fraud-risk class.

**Preferred language:**\
"This feature reduced the model's fraud-risk assessment for this
invoice."

**Avoid:**\
"This feature proves the invoice is legitimate."

**Interpretation rule:**\
A negative contribution does not guarantee that an invoice is legitimate
or risk-free.

------------------------------------------------------------------------

# Top Contributing Features

**Concept:** Prioritised explanation signals

**Definition:**\
The strongest model contributors for an individual prediction should be
prioritised when constructing the RAG retrieval query.

**Retrieval procedure:** 1. Identify the strongest contributing model
features. 2. Retrieve their definitions from `feature_dictionary.md`
when feature meaning is needed. 3. Translate the features into business
risk concepts using `risk_indicator_guide.md`. 4. Retrieve relevant
authoritative procurement or control guidance. 5. Generate an
explanation that separates model evidence from authoritative guidance.

**Interpretation rule:**\
Do not retrieve authoritative material for every model feature
indiscriminately. Prioritise the features that materially influenced the
prediction.

------------------------------------------------------------------------

# Model Evidence vs Authoritative Guidance

**Concept:** Separation of evidence sources

**Model evidence answers:**\
"What caused the model to produce this prediction?"

Examples: - amount anomaly contributed strongly - supplier risk score
contributed strongly - blacklist status influenced the prediction -
submission timing contributed to the prediction

**Authoritative guidance answers:**\
"What procurement, payment, supplier, or control practices are relevant
to reviewing this risk?"

Examples: - invoice verification - payment controls - supplier due
diligence - supplier eligibility or debarment - procurement risk
management

**Interpretation rule:**\
Authoritative documents must not be presented as if they caused the ML
prediction. The model and the external guidance are separate evidence
layers.

------------------------------------------------------------------------

# Risk Indicator

**Concept:** Signal requiring review

**Definition:**\
A risk indicator is a model feature, pattern, or combination of signals
that contributes to an elevated model-risk assessment.

**Preferred language:** - "risk indicator" - "review signal" -
"anomalous pattern" - "model contributor" - "potential concern"

**Avoid:** - "proof of fraud" - "confirmed fraud evidence" - "criminal
activity" unless independently established outside the model

**Interpretation rule:**\
Risk indicators should trigger investigation or review, not automatic
conclusions.

------------------------------------------------------------------------

# Multiple Risk Indicators

**Concept:** Combined model evidence

**Definition:**\
Several model features may jointly contribute to an elevated fraud-risk
prediction.

**Preferred language:**\
"The prediction was influenced by multiple signals, including
invoice-amount behaviour and supplier-risk information."

**Avoid:**\
"Because several indicators were present, fraud is confirmed."

**Interpretation rule:**\
Multiple signals may strengthen the model's risk assessment, but they
remain model evidence requiring review.

------------------------------------------------------------------------

# Statistical Anomaly

**Concept:** Unusual numerical pattern

**Mapped examples:** - `invoice_amount_zscore` - current amount compared
with historical amount features

**Preferred language:**\
"The model identified an unusual invoice-amount pattern."

**Avoid:**\
"The amount is fraudulent because it is statistically unusual."

**Interpretation rule:**\
Statistical abnormality and fraud are different concepts. An anomaly can
have legitimate explanations.

------------------------------------------------------------------------

# Supplier Risk Information

**Concept:** Supplier-level model evidence

**Mapped examples:** - `supplier_risk_score` - `blacklisted_flag` -
`supplier_age_days`

**Preferred language:**\
"Supplier-level risk information contributed to the model assessment."

**Avoid:**\
"The supplier is fraudulent."

**Interpretation rule:**\
Supplier risk information should be combined with invoice-level evidence
and applicable due-diligence guidance.

------------------------------------------------------------------------

# Timing Information

**Concept:** Temporal model evidence

**Mapped examples:** - `submission_hour` -
`late_night_submission_flag` - `is_weekend` - `invoice_weekday` -
`invoice_month` - `invoice_quarter`

**Preferred language:**\
"Transaction timing formed part of the model assessment."

**Avoid:**\
"Late-night, weekend, or a particular calendar period is proof of
fraud."

**Interpretation rule:**\
Timing information is contextual unless stronger evidence supports
additional conclusions.

------------------------------------------------------------------------

# Human Review

**Concept:** Final investigation responsibility

**Definition:**\
ProcureGuard supports risk detection and investigation. Final
conclusions should be made through appropriate human review of the
transaction and supporting evidence.

**Recommended review language:**\
"This result should be reviewed together with the invoice, supplier
records, supporting procurement documentation, and applicable payment
controls."

**Interpretation rule:**\
The LLM should recommend relevant review steps when useful, but should
not claim that its generated explanation is a final audit, legal, or
disciplinary determination.

------------------------------------------------------------------------

# RAG Response Structure

When explaining a prediction, the generated response should preferably
separate the following components.

**1. Model assessment**\
State the model prediction and available probability/risk level.

**2. Key model contributors**\
Summarise the strongest explainability signals in understandable
language.

**3. Risk interpretation**\
Translate those features into neutral risk concepts such as amount
anomaly, supplier risk, or unusual timing.

**4. Relevant authoritative guidance**\
Present retrieved procurement, payment-control, supplier, or
risk-management guidance and identify its source.

**5. Recommended review**\
Suggest evidence or controls that should be checked.

**6. Limitation**\
Clarify that the model result and retrieved guidance support risk
assessment and investigation; they do not independently prove fraud.

------------------------------------------------------------------------

# Example Response Pattern

**Model assessment:**\
The invoice was classified as high risk by the fraud-detection model.

**Key contributors:**\
The strongest model signals were an unusual invoice-amount pattern and
supplier-level risk information.

**Relevant guidance:**\
Retrieved procurement and payment-control guidance recommends
appropriate invoice verification, supplier review, and payment controls
relevant to these signals.

**Recommended review:**\
Verify the invoice amount against supporting records, review relevant
supplier information, and confirm applicable payment and procurement
controls.

**Limitation:**\
These indicators support further review and do not independently
establish that fraud occurred.

------------------------------------------------------------------------

# Grounding Rules

1.  Do not state that an authoritative document supports a claim unless
    that claim is present in the retrieved context.
2.  Do not invent model thresholds, feature formulas, supplier facts, or
    procurement rules.
3.  Do not convert model confidence into legal certainty.
4.  Do not describe a feature as an official fraud indicator merely
    because it is important to the ML model.
5.  Clearly distinguish model-derived observations from externally
    retrieved guidance.
6.  Prefer neutral terms such as `risk`, `indicator`, `anomaly`,
    `contributor`, and `review`.
7.  Use the authoritative source name when presenting retrieved
    guidance.
8.  If relevant authoritative guidance is not retrieved, say that the
    model signal is based on ProcureGuard's learned patterns and avoid
    fabricating external support.
