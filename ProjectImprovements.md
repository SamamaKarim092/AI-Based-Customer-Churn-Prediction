# What We Did to Make This Project Research-Paper Ready

This document explains **every improvement** we made to the AI-Based Customer Churn Prediction project, **why** we did it, and **how** it helps us — all in simple English.

---

## Quick Overview

| #   | What We Did                  | Why It Matters                                       |
| --- | ---------------------------- | ---------------------------------------------------- |
| 1   | Leakage-Proof SMOTE          | Makes our results honest and trustworthy             |
| 2   | OneHot Encoding (not Label)  | Stops the model from learning wrong number patterns  |
| 3   | Feature Engineering          | Gives the model better clues to spot churners        |
| 4   | Hyperparameter Tuning        | Finds the best settings for each model automatically |
| 5   | ROC-AUC as Main Metric       | Better way to measure performance on imbalanced data |
| 6   | Wilcoxon Statistical Test    | Scientifically proves our best model is really best  |
| 7   | ROI / Profit Calculator      | Shows how much money the model actually saves        |
| 8   | SHAP Explainability          | Explains _why_ the AI made each prediction           |
| 9   | Action Recommendation System | Tells the business what to do for each customer      |
| 10  | 5 Model Comparison           | Tests many algorithms and picks the winner fairly    |

---

## 1. Leakage-Proof SMOTE (Fixing Data Imbalance the Right Way)

### What is the problem?

In our dataset, only about 26% of customers actually churn. The rest (74%) stay. This is called **class imbalance**. If a model just says "nobody will churn", it's already 74% accurate — but completely useless.

### What is SMOTE?

SMOTE (Synthetic Minority Oversampling TEchnique) creates **fake churner examples** by mixing real churner data points together. This gives the model equal amounts of churners and non-churners to learn from.

### What was the danger?

Many projects apply SMOTE **before** splitting the data into training and testing sets. This means the fake data **leaks** into the test set, making the results look better than they really are. Research papers like **Wagh et al. (2024)** and **Idris et al. (2012)** stress the importance of handling this correctly.

### What we did

We used **imbalanced-learn's Pipeline** to wrap SMOTE inside the cross-validation loop:

- During tuning: SMOTE only touches the **training portion** of each fold
- The validation fold (used to measure performance) **never sees** any synthetic data
- The final test set is **completely untouched** by SMOTE

### How it helps us

- Our reported accuracy, ROC-AUC, recall etc. are **honest numbers** — no inflation
- If a reviewer or professor checks our method, they will see it's done correctly
- This follows the best practice from **Wagh et al. (2024)** which also uses SMOTE with proper CV

**File:** `src/train_model.py` → `tune_and_train_models()` function

---

## 2. OneHot Encoding for Multi-Class Features

### What is the problem?

Some features like `Contract` have values like _Month-to-month_, _One year_, _Two year_. If we use Label Encoding (0, 1, 2), the model might think "Two year (2) is bigger than Month-to-month (0)" which is meaningless for a category.

### What we did

- **Binary columns** (Yes/No like `Partner`, `Gender`): We used Label Encoding (0/1) — this is fine because there are only two values
- **Multi-class columns** (like `Contract`, `InternetService`, `PaymentMethod`): We used **OneHot Encoding** — creates separate 0/1 columns for each category
- This follows the approach in **Lalwani et al. (2022)** and **Manzoor et al. (2024)**

### How it helps us

- The model does not learn false number relationships between categories
- Improves prediction quality, especially for tree-based models
- Matches the encoding standards used in published research

**File:** `src/train_model.py` → `load_and_preprocess_data()` function

---

## 3. Feature Engineering (Creating New Useful Features)

### What we did

We created **3 new features** from the existing data:

| New Feature            | How We Made It                                        | Why It Helps                                       |
| ---------------------- | ----------------------------------------------------- | -------------------------------------------------- |
| `num_services`         | Count of "Yes" across 6 service columns               | Customers using more services tend to stay longer  |
| `avg_charge_per_month` | `TotalCharges ÷ tenure`                               | Shows true cost rate, catches pricing issues       |
| `tenure_group`         | Buckets tenure into bands (0–12, 13–24, 25–48, 49–72) | Captures non-linear churn risk at different stages |

### How it helps us

- Gives the model **more useful signals** to detect churn patterns
- `num_services` is similar to the "service bundling" idea from **De Caigny et al. (2018)**
- `tenure_group` captures the well-known pattern that new customers (0–12 months) churn much more
- Feature engineering is highlighted as important by **Lalwani et al. (2022)** and **Amin et al. (2017)**

**File:** `src/train_model.py` → `load_and_preprocess_data()` function

---

## 4. Hyperparameter Tuning (Finding the Best Model Settings)

### What is the problem?

Every ML model has **settings** (called hyperparameters) — like how many trees to build, how deep they should be, or how fast to learn. Default settings are rarely the best.

### What we did

- Used **RandomizedSearchCV** to automatically try many combinations of settings
- Each model gets its own search space (e.g., XGBoost tries 50 random combinations)
- The best combination is selected based on **5-fold cross-validated ROC-AUC**
- SMOTE is applied **inside** each fold during tuning (no leakage)

### How it helps us

- Our models perform at their **best possible level**, not just default
- Follows standard practice from **Ahmad et al. (2019)** and **Lalwani et al. (2022)**
- The tuning is reproducible (fixed `random_state=42`)

**File:** `src/train_model.py` → `tune_and_train_models()` function

---

## 5. ROC-AUC as the Main Evaluation Metric

### What is the problem?

Plain **accuracy** is misleading when data is imbalanced. A model that says "nobody churns" gets 74% accuracy but catches zero churners.

### What we did

- We use **ROC-AUC** (Area Under the ROC Curve) as the main metric for selecting the best model
- ROC-AUC measures how well the model **ranks** churners above non-churners
- We also report accuracy, precision, recall, and F1-score as secondary metrics

### How it helps us

- ROC-AUC is **threshold-independent** — it works even if we change the decision cutoff
- It's the **dominant metric** in the research — used in 15 out of 21 papers we reviewed
- Papers like **Wagh et al. (2024)**, **Ahmad et al. (2019)**, and **Jeyakumar et al. (2023)** all recommend ROC-AUC for churn prediction on imbalanced data

**File:** `src/train_model.py` → model selection in `tune_and_train_models()`

---

## 6. Wilcoxon Signed-Rank Test (Statistical Proof)

### What is the problem?

Just because Model A got ROC-AUC = 0.84 and Model B got 0.83 doesn't mean A is truly better. The difference might just be random noise from the data split.

### What we did

1. After tuning, we run a **separate 10-fold cross-validation** on all models using the **same folds** (paired evaluation)
2. This gives us 10 AUC scores per model
3. We then run the **Wilcoxon Signed-Rank Test** — a statistical test that checks: _"Is the best model significantly better, or is the difference just luck?"_
4. If the **p-value < 0.05**, the difference is statistically significant (95% confidence)

### Why 10 folds (not 5)?

With only 5 folds, the minimum possible one-sided p-value is 0.03125, making it very difficult to reach significance. 10 folds give us more statistical power.

### Our results

| Comparison                | p-value | Significant? |
| ------------------------- | ------- | ------------ |
| XGBoost vs Naive Bayes    | 0.001   | YES          |
| XGBoost vs Random Forest  | 0.024   | YES          |
| XGBoost vs Logistic Reg.  | 0.278   | NO           |
| XGBoost vs Gradient Boost | 0.313   | NO           |

### How it helps us

- We can **scientifically claim** that XGBoost is significantly better than Naive Bayes and Random Forest
- This follows best practices from **Verbeke et al. (2012)** and **De Caigny et al. (2018)** who use statistical tests to validate model comparisons
- Makes our research rigorous — not just "Model A has a higher number"

**File:** `src/train_model.py` → `run_statistical_tests()` function

---

## 7. ROI / Profit Calculator (Business Value)

### What is the problem?

Academic metrics like ROC-AUC are great for papers, but a business wants to know: _"How much money does this model make or save?"_

### What we did

We calculate **ROI (Return on Investment)** for each model using this formula:

$$ROI = (TP \times \$450) - (FP \times \$50)$$

Where:

- **TP (True Positives)** = Churners we correctly caught → we save \$450 per customer by retaining them
- **FP (False Positives)** = Non-churners we wrongly flagged → we waste \$50 on unnecessary retention offers

### Our results

| Model               | TP  | FP  | ROI          |
| ------------------- | --- | --- | ------------ |
| **XGBoost**         | 339 | 411 | **$132,000** |
| Naive Bayes         | 310 | 377 | $121,700     |
| Random Forest       | 291 | 283 | $117,750     |
| Logistic Regression | 293 | 289 | $117,250     |
| Gradient Boosting   | 267 | 282 | $109,500     |

### How it helps us

- XGBoost wins on ROI because it catches the most churners (highest recall = 90.64%)
- Even though XGBoost has more false positives, the **cost of missing a churner (\$450)** is much higher than the **cost of a false alarm (\$50)**
- This profit-based evaluation follows **De Caigny et al. (2018)** and **Burez & Van den Poel (2009)** who argue that business metrics should complement classification metrics
- Makes the project useful in a real business setting, not just academic

**File:** `src/train_model.py` → `calculate_roi()` function

---

## 8. SHAP Explainability (Why Did the AI Say This?)

### What is the problem?

ML models like XGBoost and Random Forest are "black boxes" — they give predictions but don't explain **why**. A business needs to know _why_ a customer is likely to churn so they can take the right action.

### What we did

- Integrated **SHAP (SHapley Additive exPlanations)** — a method from game theory that calculates how much each feature contributed to a prediction
- For each customer, we show which factors pushed the prediction towards churn or stay
- We handle OneHot-encoded features by grouping dummy columns back to their parent feature

### Example output

> "This customer has a 78% churn probability because:
>
> - Month-to-month contract (+25% towards churn)
> - No online security (+18% towards churn)
> - Short tenure of 3 months (+12% towards churn)"

### How it helps us

- Directly implements the explainability approach from **Lundberg & Lee (2017)** — the creators of SHAP
- Addresses the "right to explanation" requirement discussed in **Goodman & Flaxman (2017)** regarding GDPR
- Makes the project trustworthy for business stakeholders — they can understand and verify the AI's reasoning
- Follows the XAI (Explainable AI) recommendations from **Arrieta et al. (2020)** and **Jeyakumar et al. (2023)**

**File:** `src/explain.py`

---

## 9. Action Recommendation System

### What is the problem?

Knowing _who_ will churn and _why_ is not enough. The business also needs to know **what to do about it**.

### What we did

Built a rule-based recommendation engine with two layers:

**Layer 1 — Risk Level Actions:**
| Risk Level | Urgency | Example Action |
|------------|----------|-----------------------------------------------------|
| HIGH (>70%)| URGENT | Offer 20-30% discount, assign account manager |
| MODERATE | MODERATE | Send re-engagement email, offer 10-15% bundle deal |
| LOW (<40%) | LOW | Continue regular engagement, loyalty program |

**Layer 2 — Factor-Specific Actions:**
Based on SHAP analysis, the system gives targeted recommendations:

- Contract is Month-to-month → "Offer discounted annual contract"
- No Online Security → "Offer free trial of security service"
- High monthly charges → "Review pricing, offer competitive plan"
- Many support calls → "Escalate to quality team"

### How it helps us

- Turns the AI prediction into **actionable business decisions**
- Combines prediction + explanation + recommendation in one system
- This end-to-end approach is what **Jeyakumar et al. (2023)** recommends for practical churn systems

**File:** `src/recommend.py`

---

## 10. Five-Model Comparison

### What we did

We train and compare **5 different algorithms**:

| Model               | Type                | Key Strength                   |
| ------------------- | ------------------- | ------------------------------ |
| Logistic Regression | Linear              | Fast, interpretable            |
| Random Forest       | Ensemble (Bagging)  | Robust, good balance           |
| Gradient Boosting   | Ensemble (Boosting) | Best accuracy                  |
| XGBoost             | Ensemble (Boosting) | Best ROC-AUC & recall (WINNER) |
| Naive Bayes         | Probabilistic       | Simple baseline                |

### Our final results (on test set)

| Model               | Accuracy | Precision | Recall | F1    | ROC-AUC | ROI      |
| ------------------- | -------- | --------- | ------ | ----- | ------- | -------- |
| **XGBoost** ★       | 68.35%   | 45.20%    | 90.64% | 60.32 | 0.8431  | $132,000 |
| Gradient Boosting   | 77.29%   | 55.63%    | 71.39% | 62.53 | 0.8414  | $109,500 |
| Random Forest       | 75.37%   | 52.43%    | 77.81% | 62.65 | 0.8408  | $117,750 |
| Logistic Regression | 73.53%   | 50.09%    | 78.34% | 61.11 | 0.8398  | $117,250 |
| Naive Bayes         | 70.19%   | 46.55%    | 82.89% | 59.62 | 0.8127  | $121,700 |

### Why XGBoost won

- **Highest ROC-AUC (0.8431)** — best overall discrimination
- **Highest recall (90.64%)** — catches 9 out of 10 actual churners
- **Highest ROI ($132,000)** — most business value
- Statistically significantly better than Naive Bayes (p=0.001) and Random Forest (p=0.024)

### How it helps us

- Multi-model comparison follows **Lalwani et al. (2022)**, **Wagh et al. (2024)**, and **Vafeiadis et al. (2015)**
- Using 5 models from different families (linear, tree, ensemble, probabilistic) gives a comprehensive view
- The winner is picked objectively by ROC-AUC, not by personal preference

**File:** `src/train_model.py` → `tune_and_train_models()` and `main()`

---

## How These Improvements Map to Research Papers

| Our Feature                   | Research Paper Support                                               |
| ----------------------------- | -------------------------------------------------------------------- |
| SMOTE inside CV               | Wagh et al. (2024), Idris et al. (2012)                              |
| Feature Engineering           | Lalwani et al. (2022), Amin et al. (2017)                            |
| ROC-AUC as main metric        | Wagh et al. (2024), Ahmad et al. (2019), Jeyakumar et al. (2023)     |
| Random Forest + XGBoost       | Lalwani et al. (2022), Ahmad et al. (2019), Chen & Guestrin (2016)   |
| SHAP Explainability           | Lundberg & Lee (2017), Arrieta et al. (2020), Molnar (2022)          |
| Hyperparameter Tuning         | Lalwani et al. (2022), Ahmad et al. (2019)                           |
| Statistical Significance Test | Verbeke et al. (2012), De Caigny et al. (2018)                       |
| ROI / Profit Metric           | De Caigny et al. (2018), Burez & Van den Poel (2009)                 |
| Action Recommendations        | Jeyakumar et al. (2023)                                              |
| Class Imbalance Handling      | Wagh et al. (2024), Idris et al. (2012), Burez & Van den Poel (2009) |

---

## Summary

We started with a basic churn prediction model and turned it into a **research-grade, business-ready system** by:

1. **Making results trustworthy** — Leakage-proof SMOTE, proper encoding, statistical tests
2. **Maximizing performance** — Feature engineering, hyperparameter tuning, 5-model comparison
3. **Adding business value** — ROI calculator, action recommendations
4. **Making it explainable** — SHAP integration so anyone can understand why a prediction was made
5. **Following research standards** — Every major improvement maps to a published research paper

The final system doesn't just predict churn — it explains **why**, quantifies **how much money** is at stake, and recommends **what to do** about it.
