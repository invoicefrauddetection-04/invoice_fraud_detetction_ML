# ProcureGuard AI --- Feature Dictionary

> Internal RAG knowledge source. Each feature section is designed to
> function as a self-contained retrieval unit.

# invoice_amount

**Type:** Numerical\
**Category:** Invoice characteristics\
**Source:** invoices dataset

**Definition:**\
Monetary amount associated with the invoice.

**Interpretation:**\
Provides transaction-value context to the model. It can be evaluated
together with supplier history, historical invoice amounts, and
behavioural features.

**Retrieval concepts:** - invoice amount - transaction value - invoice
value - payment amount

**Related authoritative topics:** - invoice verification - payment
controls - transaction review

**Caution:**\
A high or low invoice amount does not independently establish fraud.

------------------------------------------------------------------------

# payment_terms

**Type:** Categorical\
**Category:** Invoice characteristics\
**Source:** invoices dataset

**Definition:**\
Payment-term category associated with the invoice.

**Model handling:**\
Treated as a categorical variable and encoded during model
preprocessing.

**Retrieval concepts:** - payment terms - payment conditions - invoice
payment - payment arrangements

**Related authoritative topics:** - payment procedures - invoice
processing - payment controls

**Caution:**\
No individual payment-term category should be described as fraudulent
solely because of its category.

------------------------------------------------------------------------

# invoice_type

**Type:** Categorical\
**Category:** Invoice characteristics\
**Source:** invoices dataset

**Definition:**\
Type or category assigned to the invoice.

**Model handling:**\
Treated as a categorical variable and encoded during model
preprocessing.

**Retrieval concepts:** - invoice type - invoice category - invoice
classification

**Related authoritative topics:** - invoice processing - invoice
verification - payment documentation

**Caution:**\
Invoice type provides transaction context and does not independently
establish fraud.

------------------------------------------------------------------------

# submission_hour

**Type:** Numerical\
**Category:** Submission timing\
**Source:** invoices dataset

**Definition:**\
Hour associated with submission of the invoice.

**Interpretation:**\
Provides time-of-day context to the model.

**Retrieval concepts:** - invoice submission time - transaction timing -
unusual submission timing - time-of-day activity

**Related authoritative topics:** - transaction monitoring - invoice
review - internal controls

**Caution:**\
Submission at a particular hour does not independently establish
suspicious or fraudulent activity.

------------------------------------------------------------------------

# supplier_invoice_count_30d

**Type:** Numerical\
**Category:** Supplier transaction behaviour\
**Source:** behavioural_features dataset

**Definition:**\
Dataset-provided behavioural feature representing supplier invoice
activity over a 30-day period.

**Interpretation:**\
Provides recent supplier-activity context to the model.

**Retrieval concepts:** - supplier invoice frequency - recent supplier
activity - vendor transaction volume - repeated invoice activity

**Related authoritative topics:** - supplier monitoring - transaction
monitoring - vendor payment review

**Formula note:**\
The exact feature-generation formula is not defined in the uploaded
model-development notebook. No additional calculation details should be
assumed.

**Caution:**\
High supplier activity alone does not establish fraud.

------------------------------------------------------------------------

# supplier_avg_amount_90d

**Type:** Numerical\
**Category:** Supplier transaction behaviour\
**Source:** behavioural_features dataset

**Definition:**\
Dataset-provided behavioural feature representing a supplier
invoice-amount average over a 90-day period.

**Interpretation:**\
Provides a recent historical amount reference for supplier behaviour.

**Retrieval concepts:** - supplier historical amount - recent supplier
spending pattern - vendor invoice baseline - historical invoice value

**Related authoritative topics:** - invoice amount review - supplier
monitoring - transaction analysis

**Formula note:**\
The precise aggregation logic and inclusion rules are not defined in the
uploaded model-development notebook.

**Caution:**\
Deviation from a historical amount reference is analytical context, not
proof of wrongdoing.

------------------------------------------------------------------------

# invoice_amount_zscore

**Type:** Numerical\
**Category:** Amount anomaly\
**Source:** behavioural_features dataset

**Definition:**\
Dataset-provided standardized anomaly feature associated with invoice
amount.

**Interpretation:**\
Represents how statistically unusual an invoice amount is according to
the dataset's feature-generation process.

**Retrieval concepts:** - invoice amount anomaly - unusual invoice
amount - abnormal transaction value - amount deviation - statistical
amount anomaly

**Related authoritative topics:** - invoice verification - payment
controls - transaction review - anomalous payment review

**Formula note:**\
The model-development notebook does not define the original reference
population or formula used to generate this feature. The RAG system must
not invent a supplier-specific or global Z-score calculation.

**Caution:**\
Statistical abnormality is a risk signal and does not independently
establish fraud.

------------------------------------------------------------------------

# late_night_submission_flag

**Type:** Binary\
**Category:** Submission timing behaviour\
**Source:** behavioural_features dataset

**Definition:**\
Indicates that the dataset's feature-generation process classified the
invoice submission as late-night.

**Interpretation:**\
Provides an engineered timing signal in addition to the raw
`submission_hour`.

**Retrieval concepts:** - late-night invoice submission - unusual
submission timing - after-hours transaction - timing anomaly

**Related authoritative topics:** - transaction monitoring - invoice
review - internal controls

**Threshold note:**\
The exact hour threshold used to generate this flag is not defined in
the uploaded model-development notebook.

**Caution:**\
The RAG system must not claim that late-night submission is officially
defined as fraud unless an authoritative source explicitly supports that
statement.

------------------------------------------------------------------------

# supplier_country

**Type:** Categorical\
**Category:** Supplier profile\
**Source:** suppliers dataset

**Definition:**\
Country associated with the supplier record.

**Model handling:**\
Treated as a categorical variable and encoded during model
preprocessing.

**Retrieval concepts:** - supplier geography - vendor location -
supplier profile

**Related authoritative topics:** - supplier information - supplier due
diligence

**Caution:**\
Supplier country is contextual model input. Country must not be
presented as evidence that a supplier is fraudulent.

------------------------------------------------------------------------

# supplier_age_days

**Type:** Numerical\
**Category:** Supplier profile\
**Source:** suppliers dataset

**Definition:**\
Dataset-provided supplier-age measure expressed in days.

**Interpretation:**\
Provides context about the length of the supplier's recorded history.

**Retrieval concepts:** - supplier tenure - supplier history - vendor
age - supplier experience

**Related authoritative topics:** - supplier due diligence - vendor
assessment - supplier monitoring

**Formula note:**\
The source dates and calculation used to derive the number of days are
not defined in the uploaded model-development notebook.

**Caution:**\
A newer or older supplier is not inherently fraudulent.

------------------------------------------------------------------------

# supplier_risk_score

**Type:** Numerical\
**Category:** Supplier risk\
**Source:** suppliers dataset

**Definition:**\
Numeric supplier-risk score provided by the supplier dataset.

**Interpretation:**\
Provides a pre-existing supplier-risk signal to the ML model.

**Retrieval concepts:** - supplier risk - vendor risk - supplier risk
assessment - vendor risk assessment

**Related authoritative topics:** - supplier due diligence - procurement
risk management - supplier monitoring - vendor assessment

**Formula note:**\
The model-development notebook does not define how this score was
originally calculated. The RAG system must not invent its formula or
thresholds.

**Caution:**\
The score is a model input and should not by itself be presented as
proof of fraud.

------------------------------------------------------------------------

# blacklisted_flag

**Type:** Binary\
**Category:** Supplier risk and due diligence\
**Source:** suppliers dataset

**Definition:**\
Indicates the supplier's recorded blacklist status in the dataset.

**Interpretation:**\
Provides supplier-status context to the model.

**Retrieval concepts:** - supplier blacklisting - vendor blacklist -
supplier debarment - supplier eligibility - vendor due diligence

**Related authoritative topics:** - debarment - supplier eligibility -
supplier due diligence - vendor integrity

**Caution:**\
The RAG system should report the recorded status and retrieve relevant
guidance without making additional legal conclusions.

------------------------------------------------------------------------

# avg_invoice_amount

**Type:** Numerical\
**Category:** Supplier historical transaction context\
**Source:** suppliers dataset

**Definition:**\
Average invoice amount stored in the supplier dataset.

**Interpretation:**\
Provides a supplier-level historical amount reference that can be
considered alongside the current invoice amount and behavioural amount
features.

**Retrieval concepts:** - supplier average invoice - supplier historical
amount - vendor transaction baseline - historical invoice value

**Related authoritative topics:** - invoice amount review - supplier
monitoring - transaction analysis

**Formula note:**\
The model-development notebook does not define the original averaging
period or generation formula.

**Caution:**\
Deviation from a historical average is an analytical signal, not proof
of fraud.

------------------------------------------------------------------------

# invoice_month

**Type:** Numerical / temporal\
**Category:** Temporal context\
**Source:** Derived from `invoice_date`

**Definition:**\
Calendar month of the invoice date.

**Verified derivation:**\
`invoice_date.dt.month`

**Values:**\
1 through 12.

**Retrieval concepts:** - invoice month - monthly transaction timing -
seasonal transaction context

**Related authoritative topics:** - transaction monitoring - temporal
pattern review

**Caution:**\
A particular month is not inherently suspicious.

------------------------------------------------------------------------

# invoice_weekday

**Type:** Numerical / temporal\
**Category:** Temporal context\
**Source:** Derived from `invoice_date`

**Definition:**\
Day of week associated with the invoice date.

**Verified derivation:**\
`invoice_date.dt.dayofweek`

**Values:**\
Monday = 0 through Sunday = 6.

**Retrieval concepts:** - invoice weekday - day-of-week activity -
transaction timing

**Related authoritative topics:** - transaction monitoring - temporal
pattern review

**Caution:**\
A particular weekday is not inherently suspicious.

------------------------------------------------------------------------

# invoice_quarter

**Type:** Numerical / temporal\
**Category:** Temporal context\
**Source:** Derived from `invoice_date`

**Definition:**\
Calendar quarter associated with the invoice date.

**Verified derivation:**\
`invoice_date.dt.quarter`

**Values:**\
1 through 4.

**Retrieval concepts:** - invoice quarter - quarterly transaction
timing - seasonal transaction context

**Related authoritative topics:** - transaction monitoring - temporal
pattern review

**Caution:**\
A particular quarter is not inherently suspicious.

------------------------------------------------------------------------

# is_weekend

**Type:** Binary\
**Category:** Temporal context\
**Source:** Derived from `invoice_weekday`

**Definition:**\
Indicates whether the invoice date falls on Saturday or Sunday.

**Verified derivation:**\
`(invoice_weekday >= 5).astype(int)`

**Values:**\
0 = weekday\
1 = weekend

**Retrieval concepts:** - weekend invoice - weekend transaction -
unusual timing context - non-business-day activity

**Related authoritative topics:** - transaction monitoring - invoice
review - internal controls

**Caution:**\
Weekend activity is timing context and does not automatically indicate
fraud.
