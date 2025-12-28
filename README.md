# 🤖 AI-Based Customer Churn Prediction & Action Recommendation System

A complete machine learning system that predicts customer churn, explains why customers are leaving using SHAP (Explainable AI), and recommends business actions to retain them.

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [How It Works](#-how-it-works)
3. [Project Architecture](#-project-architecture)
4. [Dataset Description](#-dataset-description)
5. [Machine Learning Models](#-machine-learning-models)
6. [SHAP Explainability](#-shap-explainability)
7. [Action Recommendation System](#-action-recommendation-system)
8. [Installation Guide](#-installation-guide)
9. [How to Run](#-how-to-run)
10. [Sample Output](#-sample-output)
11. [Future Enhancements](#-future-enhancements)
12. [Technologies Used](#-technologies-used)

---

## 🎯 Project Overview

### What is Customer Churn?

Customer churn refers to when customers stop using a company's product or service. For subscription-based businesses like Netflix, Spotify, Amazon Prime, or telecom operators, churn directly impacts revenue.

### What Does This System Do?

This AI system provides three core capabilities:

| Feature | Description |
|---------|-------------|
| **1. Churn Prediction** | Predicts whether a customer will leave (churn) or stay |
| **2. Explainability** | Explains WHY the AI made that prediction using SHAP values |
| **3. Action Recommendations** | Suggests specific business actions to retain at-risk customers |

### Why This Project Matters

- Companies lose millions due to customer churn
- Early identification of at-risk customers enables proactive retention
- Understanding WHY customers leave helps improve business strategies
- Automated recommendations enable fast, data-driven decisions

---


## ⚙️ How It Works

### Step-by-Step Process

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        SYSTEM WORKFLOW                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   1. DATA INPUT                                                          │
│   ┌──────────────────┐                                                  │
│   │ Customer Data    │  age, gender, subscription, login frequency,     │
│   │ (10 features)    │  last login days, watch time, payment failures, │
│   │                  │  support calls, tenure, monthly charges          │
│   └────────┬─────────┘                                                  │
│            │                                                             │
│            ▼                                                             │
│   2. PREPROCESSING                                                       │
│   ┌──────────────────┐                                                  │
│   │ Encode & Scale   │  Convert text to numbers, normalize values       │
│   └────────┬─────────┘                                                  │
│            │                                                             │
│            ▼                                                             │
│   3. ML PREDICTION                                                       │
│   ┌──────────────────┐                                                  │
│   │ Trained Model    │  Predicts churn probability (0-100%)             │
│   │ (Logistic Reg)   │  Risk Level: HIGH / MODERATE / LOW               │
│   └────────┬─────────┘                                                  │
│            │                                                             │
│            ▼                                                             │
│   4. SHAP EXPLANATION                                                    │
│   ┌──────────────────┐                                                  │
│   │ Feature Impact   │  "Low login frequency increased churn by 25%"   │
│   │ Analysis         │  "Payment failures increased churn by 18%"       │
│   └────────┬─────────┘                                                  │
│            │                                                             │
│            ▼                                                             │
│   5. ACTION RECOMMENDATION                                               │
│   ┌──────────────────┐                                                  │
│   │ Business Rules   │  "Offer 20% discount"                            │
│   │ Engine           │  "Send re-engagement email"                       │
│   └──────────────────┘                                                  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Architecture

```
customer_churn_project/
│
├── 📂 data/
│   ├── generate_data.py      # Creates synthetic customer dataset
│   └── customers.csv         # Generated dataset (1000 customers)
│
├── 📂 model/
│   ├── churn_model.pkl       # Trained machine learning model
│   ├── encoder.pkl           # Feature encoders (gender, subscription)
│   └── feature_names.pkl     # List of feature column names
│
├── 📂 src/
│   ├── train_model.py        # Trains and compares 3 ML algorithms
│   ├── predict.py            # Makes churn predictions
│   ├── explain.py            # SHAP-based explainability
│   └── recommend.py          # Action recommendation engine
│
├── 📂 ui/
│   └── app.py                # Tkinter desktop application
│
└── README.md                 # This documentation file
```

### File Descriptions

| File | Purpose |
|------|---------|
| `data/generate_data.py` | Generates 1000 synthetic customers with realistic churn patterns. Uses probability-based logic where low engagement, payment failures, and high support calls correlate with higher churn. |
| `data/customers.csv` | The training dataset with 10 features and 1 target variable (churn). Contains ~32% churned customers. |
| `src/train_model.py` | Loads data, preprocesses features, trains Logistic Regression, Naive Bayes, and Random Forest. Compares accuracy and saves the best model. |
| `src/predict.py` | Loads the saved model and makes predictions on new customer data. Returns probability and risk level. |
| `src/explain.py` | Uses SHAP (SHapley Additive exPlanations) to calculate feature importance for each prediction. |
| `src/recommend.py` | Rule-based engine that suggests actions based on churn probability and specific customer factors. |
| `ui/app.py` | Desktop GUI built with Tkinter. Allows entering customer data and displays prediction + explanation + recommendations. |

---

## 📊 Dataset Description

### Features (Input Variables)

| Feature | Type | Description | Range |
|---------|------|-------------|-------|
| `age` | Numeric | Customer's age | 18-70 years |
| `gender` | Categorical | Male or Female | Male/Female |
| `subscription_type` | Categorical | Subscription tier | Basic/Standard/Premium |
| `monthly_charges` | Numeric | Monthly subscription cost | $9.99-$39.99 |
| `tenure_in_months` | Numeric | How long they've been a customer | 1-72 months |
| `login_frequency` | Numeric | Number of logins per month | 0-60 logins |
| `last_login_days` | Numeric | Days since last login | 0-90 days |
| `watch_time` | Numeric | Hours of content watched per month | 0-100 hours |
| `payment_failures` | Numeric | Number of failed payment attempts | 0-5 failures |
| `customer_support_calls` | Numeric | Support tickets raised | 0-10 calls |

### Target Variable (Output)

| Variable | Values | Meaning |
|----------|--------|---------|
| `churn` | 0 | Customer will STAY |
| `churn` | 1 | Customer will LEAVE (churn) |

### Realistic Churn Patterns in Data

The synthetic data generator creates realistic correlations:

- **Low login frequency** → Higher churn probability
- **Many days since last login** → Higher churn probability  
- **Low watch time** → Higher churn probability
- **Payment failures** → Strongly increases churn probability
- **Many support calls** → Indicates frustration, higher churn
- **Short tenure** → New customers churn more
- **Premium subscription** → Lower churn (more committed)

---

## 🤖 Machine Learning Models

### Algorithms Compared

| Algorithm | Description | Strengths |
|-----------|-------------|-----------|
| **Logistic Regression** | Linear model for binary classification | Fast, interpretable, good baseline |
| **Naive Bayes** | Probabilistic classifier | Fast training, works with small data |
| **Random Forest** | Ensemble of decision trees | High accuracy, handles non-linear patterns |

### Model Training Process

1. **Load Data**: Read `customers.csv`
2. **Encode Categoricals**: Convert gender and subscription_type to numbers
3. **Scale Features**: Normalize all values to same range (StandardScaler)
4. **Split Data**: 80% training, 20% testing
5. **Train Models**: Fit all 3 algorithms
6. **Evaluate**: Calculate accuracy, precision, recall, F1-score
7. **Save Best**: Store the best performing model as `.pkl` file

### Current Model Performance

```
Model                       Accuracy  Precision  Recall   F1-Score
-----------------------------------------------------------------
Logistic Regression           72.5%     63.9%    35.4%     45.5%  [SELECTED]
Naive Bayes                   72.0%     60.5%    40.0%     48.2%
Random Forest                 72.5%     65.6%    32.3%     43.3%
```

---

## 🔍 SHAP Explainability

### What is SHAP?

SHAP (SHapley Additive exPlanations) is an explainable AI technique that:
- Calculates the contribution of each feature to the prediction
- Shows which features pushed the prediction toward churn or stay
- Provides both global (overall) and local (individual) explanations

### How We Use SHAP

For each customer prediction, SHAP tells us:
- **Positive SHAP value**: This feature INCREASES churn probability
- **Negative SHAP value**: This feature DECREASES churn probability

### Example Output

```
Customer: John, 25 years old, Basic subscription, 2 months tenure

Top Factors Influencing Churn:
1. Last Login Days: 45 days → INCREASES churn risk by 25%
2. Payment Failures: 2 failures → INCREASES churn risk by 18%
3. Login Frequency: 3 logins/month → INCREASES churn risk by 12%
4. Watch Time: 2.5 hours → INCREASES churn risk by 10%
5. Tenure: 2 months → INCREASES churn risk by 8%
```

---

## 💡 Action Recommendation System

### Rule-Based Logic

The system uses probability thresholds to categorize risk and suggest actions:

| Churn Probability | Risk Level | Urgency | Actions |
|-------------------|------------|---------|---------|
| **≥ 70%** | HIGH | URGENT | Offer 20-30% discount, assign account manager, send personalized retention message |
| **40-70%** | MODERATE | MODERATE | Send re-engagement notification, offer 10-15% discount, highlight new features |
| **< 40%** | LOW | LOW | Continue regular engagement, include in loyalty program |

### Factor-Specific Recommendations

The system also provides targeted actions based on specific issues:

| Factor Issue | Recommended Action |
|--------------|-------------------|
| Many days since login | Send "We miss you" email with exclusive content |
| Low login frequency | Recommend personalized content |
| Low watch time | Send curated content recommendations |
| Payment failures | Reach out to resolve payment issues |
| Many support calls | Proactive outreach to resolve ongoing issues |
| Short tenure | Onboarding follow-up |

---

## 🛠️ Installation Guide

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project

```bash
git clone https://github.com/your-username/customer-churn-prediction.git
cd customer-churn-prediction
```

### Step 2: Install Dependencies

```bash
pip install pandas numpy scikit-learn shap matplotlib joblib
```

### Required Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| pandas | ≥1.3.0 | Data manipulation |
| numpy | ≥1.21.0 | Numerical operations |
| scikit-learn | ≥1.0.0 | Machine learning |
| shap | ≥0.40.0 | Explainability |
| matplotlib | ≥3.4.0 | Visualizations |
| joblib | ≥1.1.0 | Model saving/loading |
| tkinter | (built-in) | Desktop UI |

---

## 🚀 How to Run

### Option 1: Run Full Pipeline

```bash
# Step 1: Generate the dataset
python data/generate_data.py

# Step 2: Train the model
python src/train_model.py

# Step 3: Launch the UI
python ui/app.py
```

### Option 2: Test Individual Components

```bash
# Test prediction module
python src/predict.py

# Test recommendation module
python src/recommend.py

# Test explainability module
python src/explain.py
```

### Using the UI Application

1. Launch with `python ui/app.py`
2. Enter customer data in the input fields
3. OR click "Load High-Risk Sample" / "Load Low-Risk Sample"
4. Click "Predict Churn"
5. View results: probability, risk level, explanations, and recommendations

---

## 📝 Sample Output

### High-Risk Customer Example

**Input:**
- Age: 25, Gender: Male, Subscription: Basic
- Monthly Charges: $12.99, Tenure: 2 months
- Login Frequency: 3/month, Last Login: 45 days ago
- Watch Time: 2.5 hours, Payment Failures: 2
- Support Calls: 4

**Output:**
```
======================================================================
                    CHURN PREDICTION RESULTS
======================================================================

  CHURN PROBABILITY:  94.0%
  PREDICTION:         Churn
  RISK LEVEL:         HIGH

  Risk Meter: [###############################################---] 94%

----------------------------------------------------------------------
  TOP FACTORS INFLUENCING CHURN:
----------------------------------------------------------------------
  1. Days Since Last Login: 45 days
     -> INCREASES churn risk by 25.0%
  2. Payment Failures: 2
     -> INCREASES churn risk by 18.0%
  3. Login Frequency: 3
     -> INCREASES churn risk by 12.0%

----------------------------------------------------------------------
  RECOMMENDED ACTIONS:
----------------------------------------------------------------------
  Status: ALERT - 94% probability of churning. Immediate action required!

  Primary Action: Immediate retention intervention required

  Specific Actions:
    1. Reach out to resolve payment issues
    2. Send "We miss you" email with exclusive content
    3. Offer personalized discount (20-30% off)
    4. Recommend personalized content based on past preferences
    5. Assign dedicated account manager

======================================================================
```

---

## 🔮 Future Enhancements

The following features are planned for future development:

### 1. 🎨 Enhanced UI Design

| Feature | Description |
|---------|-------------|
| Modern Theme | Dark mode, glassmorphism effects, modern color palette |
| Responsive Layout | Better resizing and mobile-friendly design |
| Progress Indicators | Loading animations during predictions |
| Tabbed Interface | Separate tabs for Predict, Train, Reports, Settings |

### 2. 📈 Interactive Charts & Graphs

| Visualization | Purpose |
|---------------|---------|
| SHAP Waterfall Plot | Visual breakdown of feature contributions |
| SHAP Summary Plot | Global feature importance across all customers |
| Churn Distribution Pie Chart | Churned vs Stayed percentages |
| Risk Level Gauge | Visual meter showing churn probability |
| Feature Correlation Heatmap | Shows relationships between features |
| ROC Curve | Model performance visualization |
| Confusion Matrix | Prediction accuracy breakdown |

### 3. 📂 Excel/CSV File Upload

| Feature | Description |
|---------|-------------|
| Batch Upload | Upload CSV/Excel file with multiple customers |
| Bulk Prediction | Predict churn for all customers at once |
| Data Validation | Check for missing or invalid values |
| Preview Window | See uploaded data before processing |
| Export Results | Download predictions as CSV/Excel |

### 4. 📄 PDF Report Generation

| Report Section | Contents |
|----------------|----------|
| Executive Summary | Overall churn statistics, risk distribution |
| Individual Customer Reports | Detailed prediction for each customer |
| SHAP Visualizations | Embedded charts explaining predictions |
| Recommendation Summary | All suggested actions compiled |
| Model Performance | Accuracy metrics and confusion matrix |
| Timestamp & Metadata | When report was generated, model version |

### 5. 📊 Dashboard Features

| Feature | Description |
|---------|-------------|
| Real-time Statistics | Live count of high/moderate/low risk customers |
| Trend Analysis | Track churn predictions over time |
| Alert System | Notifications for high-risk customers |
| Model Retraining | Option to retrain model with new data |
| A/B Testing | Compare different model versions |

### 6. 🔄 Model Improvements

| Enhancement | Description |
|-------------|-------------|
| More Algorithms | XGBoost, LightGBM, Neural Networks |
| Hyperparameter Tuning | Optimize model parameters automatically |
| Cross-Validation | More robust model evaluation |
| Feature Engineering | Create new features from existing data |
| Class Balancing | Handle imbalanced churn/stay ratios |

### 7. 📧 Automated Actions

| Feature | Description |
|---------|-------------|
| Email Templates | Pre-written retention emails |
| Gemini Integration | AI-generated personalized messages |
| Notification System | Automated alerts for high-risk customers |
| CRM Integration | Connect with Salesforce, HubSpot, etc. |

---

## 🛠️ Technologies Used

| Category | Technology |
|----------|------------|
| Programming Language | Python 3.x |
| Data Processing | pandas, numpy |
| Machine Learning | scikit-learn |
| Explainability | SHAP |
| Visualization | matplotlib, seaborn |
| Model Persistence | joblib |
| Desktop UI | Tkinter |
| Future UI | CustomTkinter / PyQt |

---

## 📄 License

This project is developed for educational and academic purposes.

---

## 👨‍💻 Author

Customer Churn AI Prediction System

---

## 🙏 Acknowledgments

- SHAP library for explainable AI
- scikit-learn for machine learning algorithms
- The open-source Python community

---

**Last Updated:** December 2025
