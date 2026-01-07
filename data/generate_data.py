"""
Synthetic Customer Dataset Generator
Generates realistic customer data with churn patterns for ML training.
"""

import pandas as pd
import numpy as np
import os

# Set random seed for reproducibility
np.random.seed(42)

def generate_customer_data(n_customers=1000):
    """
    Generate synthetic customer data with realistic churn patterns.
    
    Features:
    - customer_id: Unique identifier
    - age: Customer age (18-70)
    - gender: Male/Female
    - subscription_type: Basic/Standard/Premium
    - monthly_charges: Monthly subscription cost
    - tenure_in_months: How long they've been a customer
    - login_frequency: Logins per month
    - last_login_days: Days since last login
    - watch_time: Hours of content watched per month
    - payment_failures: Number of failed payments
    - customer_support_calls: Support tickets raised
    - churn: Target variable (0=stay, 1=leave)
    """
    
    # Generate base features
    customer_ids = range(1001, 1001 + n_customers)
    ages = np.random.randint(18, 71, n_customers)
    genders = np.random.choice(['Male', 'Female'], n_customers)
    subscription_types = np.random.choice(
        ['Basic', 'Standard', 'Premium'], 
        n_customers, 
        p=[0.4, 0.35, 0.25]  # More basic subscribers
    )
    
    # Monthly charges based on subscription type
    monthly_charges = []
    for sub_type in subscription_types:
        if sub_type == 'Basic':
            monthly_charges.append(round(np.random.uniform(9.99, 14.99), 2))
        elif sub_type == 'Standard':
            monthly_charges.append(round(np.random.uniform(15.99, 24.99), 2))
        else:  # Premium
            monthly_charges.append(round(np.random.uniform(25.99, 39.99), 2))
    
    # Tenure (months as customer)
    tenure_in_months = np.random.exponential(scale=24, size=n_customers).astype(int)
    tenure_in_months = np.clip(tenure_in_months, 1, 72)  # 1 month to 6 years
    
    # Login frequency (logins per month)
    login_frequency = np.random.poisson(lam=15, size=n_customers)
    login_frequency = np.clip(login_frequency, 0, 60)
    
    # Days since last login
    last_login_days = np.random.exponential(scale=7, size=n_customers).astype(int)
    last_login_days = np.clip(last_login_days, 0, 90)
    
    # Watch time (hours per month)
    watch_time = np.random.exponential(scale=20, size=n_customers)
    watch_time = np.clip(watch_time, 0, 100).round(1)
    
    # Payment failures
    payment_failures = np.random.poisson(lam=0.5, size=n_customers)
    payment_failures = np.clip(payment_failures, 0, 5)
    
    # Customer support calls
    customer_support_calls = np.random.poisson(lam=1.5, size=n_customers)
    customer_support_calls = np.clip(customer_support_calls, 0, 10)
    
    # Calculate churn probability based on realistic patterns
    # Very clear patterns for ~73% model accuracy
    churn_probability = np.zeros(n_customers)
    
    for i in range(n_customers):
        prob = 0.10  # Base churn rate of 10%
        
        # Low engagement - STRONG predictor
        if login_frequency[i] < 5:
            prob += 0.45
        elif login_frequency[i] < 8:
            prob += 0.20
        elif login_frequency[i] > 20:
            prob -= 0.08
        
        # Haven't logged in recently - STRONGEST predictor
        if last_login_days[i] > 25:
            prob += 0.50
        elif last_login_days[i] > 12:
            prob += 0.25
        elif last_login_days[i] < 3:
            prob -= 0.10
        
        # Low watch time - Strong predictor
        if watch_time[i] < 4:
            prob += 0.35
        elif watch_time[i] < 8:
            prob += 0.15
        elif watch_time[i] > 30:
            prob -= 0.10
        
        # Payment failures - Very strong predictor
        if payment_failures[i] >= 2:
            prob += 0.40
        elif payment_failures[i] == 1:
            prob += 0.20
        
        # Support calls
        if customer_support_calls[i] > 5:
            prob += 0.25
        elif customer_support_calls[i] > 3:
            prob += 0.10
        
        # Short tenure - New customers churn more
        if tenure_in_months[i] < 3:
            prob += 0.25
        elif tenure_in_months[i] < 6:
            prob += 0.12
        elif tenure_in_months[i] > 40:
            prob -= 0.15
        
        # Premium subscribers are more loyal
        if subscription_types[i] == 'Premium':
            prob -= 0.18
        elif subscription_types[i] == 'Basic':
            prob += 0.10
        
        churn_probability[i] = np.clip(prob, 0.02, 0.98)
    
    # Generate churn labels based on probabilities
    churn = (np.random.random(n_customers) < churn_probability).astype(int)
    
    # Create DataFrame
    df = pd.DataFrame({
        'customer_id': customer_ids,
        'age': ages,
        'gender': genders,
        'subscription_type': subscription_types,
        'monthly_charges': monthly_charges,
        'tenure_in_months': tenure_in_months,
        'login_frequency': login_frequency,
        'last_login_days': last_login_days,
        'watch_time': watch_time,
        'payment_failures': payment_failures,
        'customer_support_calls': customer_support_calls,
        'churn': churn
    })
    
    return df


def main():
    """Generate and save the customer dataset."""
    print("=" * 50)
    print("[*] Generating Synthetic Customer Dataset...")
    print("=" * 50)
    
    # Generate data
    df = generate_customer_data(n_customers=5000)
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'customers.csv')
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    
    # Print summary statistics
    print(f"\n[OK] Dataset generated successfully!")
    print(f"[FILE] Saved to: {output_path}")
    print(f"\n[STATS] Dataset Summary:")
    print(f"   - Total customers: {len(df)}")
    print(f"   - Churn rate: {df['churn'].mean()*100:.1f}%")
    print(f"   - Customers who churned: {df['churn'].sum()}")
    print(f"   - Customers who stayed: {len(df) - df['churn'].sum()}")
    
    print(f"\n[INFO] Feature Statistics:")
    print(df.describe().round(2).to_string())
    
    print("\n[INFO] Subscription Distribution:")
    print(df['subscription_type'].value_counts().to_string())
    
    print("\n" + "=" * 50)
    print("[OK] Dataset generation complete!")
    print("=" * 50)
    
    return df


if __name__ == "__main__":
    main()
