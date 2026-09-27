# Data Dictionary -- retail_campaign_data.csv

| Column          | Meaning                                    | Role       |
|------------------|---------------------------------------------|------------|
| customer_id     | Unique ID per customer                      | id         |
| age             | Customer age (18-80)                        | covariate  |
| income          | Income in $ thousands (15-200)              | confounder |
| loyalty_score   | Loyalty, 0 (new) to 1 (very loyal)           | confounder |
| discount_given  | Discount offered: $0, $10, or $20           | treatment  |
| purchased       | 1 = bought, 0 = did not buy                 | outcome    |
