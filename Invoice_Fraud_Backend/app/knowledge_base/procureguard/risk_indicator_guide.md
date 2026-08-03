# ProcureGuard AI --- Risk Indicator Guide

> Internal RAG knowledge source. This document translates model features
> into neutral risk concepts that can be used for retrieval against
> authoritative procurement and control documents.

# Amount Anomaly

**Risk concept:** Invoice amount anomaly

**Mapped features:** - `invoice_amount_zscore` - `invoice_amount` -
`supplier_avg_amount_90d` - `avg_invoice_amount`

**Meaning:**\
The current invoice amount may differ from historical or statistical
amount patterns represented in the model inputs.

**Retrieval concepts:** - unusual invoice amount - abnormal invoice
value - invoice amount anomaly - payment amount review - invoice
verification - transaction value review

**Authoritative topics to retrieve:** - invoice verification - payment
controls - payment authorization - transaction review

**Explanation language:**\
"The model identified invoice-amount characteristics that contributed to
the risk prediction."

**Do not say:**\
"The unusual amount proves that the invoice is fraudulent."

**Review focus:** - verify the invoice amount against supporting
records - compare the amount with relevant supplier history when
available - review applicable payment and invoice controls

------------------------------------------------------------------------

# Unusual Supplier Invoice Activity

**Risk concept:** Supplier transaction behaviour

**Mapped features:** - `supplier_invoice_count_30d` -
`supplier_avg_amount_90d` - `avg_invoice_amount`

**Meaning:**\
The model considers recent and historical supplier transaction patterns
when evaluating the invoice.

**Retrieval concepts:** - supplier invoice activity - vendor transaction
monitoring - supplier payment history - repeated invoice activity -
supplier invoice pattern - vendor payment review

**Authoritative topics to retrieve:** - supplier monitoring - vendor
payment controls - invoice review - transaction monitoring

**Explanation language:**\
"Recent or historical supplier transaction behaviour contributed to the
model's risk assessment."

**Do not say:**\
"A high number of supplier invoices means the supplier is committing
fraud."

**Review focus:** - compare recent invoice activity with the supplier's
normal pattern - review relevant invoice and payment records -
investigate material deviations where appropriate

------------------------------------------------------------------------

# Supplier Risk

**Risk concept:** Supplier or vendor risk

**Mapped features:** - `supplier_risk_score` - `supplier_age_days` -
`blacklisted_flag`

**Meaning:**\
The model uses supplier-level risk and history information as part of
the fraud-risk assessment.

**Retrieval concepts:** - supplier risk - vendor risk - supplier due
diligence - vendor assessment - supplier monitoring - supplier
eligibility - vendor integrity

**Authoritative topics to retrieve:** - procurement risk management -
supplier due diligence - supplier eligibility - vendor assessment -
supplier monitoring

**Explanation language:**\
"Supplier-level risk information contributed to the model prediction."

**Do not say:**\
"The supplier is fraudulent because its risk score is high."

**Review focus:** - verify supplier status and available supplier
records - review applicable due-diligence information - investigate
relevant risk indicators in combination with invoice evidence

------------------------------------------------------------------------

# Supplier Blacklist Status

**Risk concept:** Supplier blacklisting, debarment, and eligibility

**Mapped feature:** - `blacklisted_flag`

**Meaning:**\
The dataset records a binary supplier blacklist status that can
contribute to the model's prediction.

**Retrieval concepts:** - supplier blacklisting - vendor blacklist -
debarment - supplier eligibility - vendor eligibility - supplier due
diligence - supplier integrity

**Authoritative topics to retrieve:** - debarment - supplier
eligibility - procurement restrictions - vendor due diligence

**Explanation language:**\
"The supplier's recorded blacklist status contributed to the model
assessment."

**Do not say:**\
"The supplier is legally debarred under a specific authority" unless the
retrieved authoritative evidence and underlying supplier data explicitly
support that statement.

**Review focus:** - verify the supplier's recorded status - check
applicable supplier eligibility or debarment requirements - confirm the
status against the relevant authoritative or organizational records

------------------------------------------------------------------------

# Unusual Submission Timing

**Risk concept:** Invoice submission timing

**Mapped features:** - `submission_hour` -
`late_night_submission_flag` - `is_weekend` - `invoice_weekday`

**Meaning:**\
The model uses time-of-day and day-of-week information as behavioural
context.

**Retrieval concepts:** - unusual transaction timing - late-night
invoice submission - after-hours transaction - weekend invoice
activity - transaction monitoring - invoice review

**Authoritative topics to retrieve:** - transaction monitoring -
internal controls - invoice review - payment processing controls

**Explanation language:**\
"Submission-timing characteristics contributed to the model's risk
prediction."

**Do not say:**\
"Late-night or weekend submission is officially classified as fraud."

**Review focus:** - verify whether the timing is consistent with
expected operational activity - review the invoice together with
supporting transaction records - treat timing as contextual evidence
rather than proof of wrongdoing

------------------------------------------------------------------------

# Temporal Pattern Context

**Risk concept:** Temporal or seasonal transaction context

**Mapped features:** - `invoice_month` - `invoice_weekday` -
`invoice_quarter` - `is_weekend`

**Meaning:**\
Calendar-derived features provide temporal context that the model may
use when identifying patterns in invoice activity.

**Retrieval concepts:** - transaction timing - temporal transaction
pattern - seasonal invoice pattern - monthly invoice activity -
quarterly invoice activity - weekend transaction activity

**Authoritative topics to retrieve:** - transaction monitoring - risk
monitoring - invoice review

**Explanation language:**\
"Temporal transaction patterns contributed to the model assessment."

**Do not say:**\
"A particular month, weekday, or quarter is inherently fraudulent."

**Review focus:** - compare the timing with relevant historical or
operational patterns - use temporal information only in combination with
stronger transaction or supplier evidence

------------------------------------------------------------------------

# Payment and Invoice Context

**Risk concept:** Invoice and payment conditions

**Mapped features:** - `payment_terms` - `invoice_type` -
`invoice_amount`

**Meaning:**\
The model considers basic invoice characteristics and payment-related
context when evaluating risk.

**Retrieval concepts:** - payment terms - invoice processing - invoice
verification - payment authorization - payment controls - invoice
documentation

**Authoritative topics to retrieve:** - payment procedures - invoice
verification - payment authorization - supporting documentation -
internal controls

**Explanation language:**\
"Invoice and payment characteristics contributed to the model
prediction."

**Do not say:**\
"A specific payment term or invoice type is fraudulent by definition."

**Review focus:** - verify invoice details against supporting
documentation - review applicable payment conditions and authorization
controls - confirm consistency between invoice information and
procurement/payment records

------------------------------------------------------------------------

# Supplier Profile Context

**Risk concept:** Supplier profile information

**Mapped features:** - `supplier_country` - `supplier_age_days`

**Meaning:**\
The model uses basic supplier profile information as contextual input.

**Retrieval concepts:** - supplier profile - supplier history - supplier
tenure - vendor information - supplier due diligence

**Authoritative topics to retrieve:** - supplier due diligence -
supplier assessment - vendor information verification

**Explanation language:**\
"Supplier profile information formed part of the model's assessment."

**Do not say:**\
"A supplier is risky or fraudulent because of its country."

**Review focus:** - use supplier profile data as contextual
information - rely on transaction evidence and documented supplier-risk
information for stronger conclusions

------------------------------------------------------------------------

# Combined Risk Indicators

**Risk concept:** Multi-signal fraud-risk assessment

**Mapped features:**\
Any combination of invoice, behavioural, supplier-risk, and temporal
features identified as important by model explainability.

**Meaning:**\
ProcureGuard should interpret risk primarily from combinations of model
signals rather than treating a single feature as deterministic proof of
fraud.

**Retrieval concepts:** - procurement risk assessment - invoice risk
review - vendor payment controls - supplier risk management -
transaction monitoring - internal controls

**Authoritative topics to retrieve:** - procurement risk management -
invoice and payment controls - supplier due diligence - transaction
review - internal control procedures

**Explanation language:**\
"The model's prediction was influenced by multiple invoice and supplier
risk indicators. Relevant procurement and control guidance should be
reviewed together with the underlying transaction evidence."

**Do not say:**\
"The retrieved documents prove that the model prediction is correct."

**Review focus:** - prioritize the strongest model contributors -
retrieve guidance relevant to those contributors - review the underlying
invoice and supplier evidence - keep the final decision subject to human
investigation

------------------------------------------------------------------------

# Retrieval Priority Rules

When generating a RAG query from model explainability:

1.  Use the strongest contributing features first.
2.  Translate internal feature names into business concepts before
    searching authoritative documents.
3.  Prefer specific concepts such as `invoice amount anomaly`,
    `supplier due diligence`, `debarment`, or `payment controls` over
    raw variable names.
4.  Retrieve ProcureGuard feature definitions when the question concerns
    what a model feature means.
5.  Retrieve authoritative documents when the question concerns
    procurement practice, payment controls, supplier eligibility, due
    diligence, or risk management.
6.  If no authoritative source directly supports a model-specific
    indicator, describe it only as a model or behavioural signal.
7.  Never convert a risk indicator into a confirmed fraud statement
    solely because it contributed strongly to the prediction.
