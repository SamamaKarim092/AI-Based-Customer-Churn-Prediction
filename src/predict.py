"""
Prediction Module
Loads the trained model and makes churn predictions for new customers.
"""

import os
import joblib
import numpy as np
import pandas as pd


def load_model_and_encoders():
    """Load the trained model and encoders from disk."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    model_dir = os.path.join(project_dir, 'model')
    
    # Load model
    model_path = os.path.join(model_dir, 'churn_model.pkl')
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}. Please run train_model.py first.")
    model = joblib.load(model_path)
    
    # Load encoders
    encoder_path = os.path.join(model_dir, 'encoder.pkl')
    encoders = joblib.load(encoder_path)
    
    # Load feature names
    feature_path = os.path.join(model_dir, 'feature_names.pkl')
    feature_names = joblib.load(feature_path)
    
    return model, encoders, feature_names


def preprocess_customer_data(customer_data, encoders, feature_names):
    """
    Preprocess a single customer's data for prediction.
    
    Args:
        customer_data: Dictionary with customer features
        encoders: Dictionary of fitted encoders
        feature_names: List of feature names in correct order
        
    Returns:
        Preprocessed feature array ready for prediction
    """
    # Create a copy to avoid modifying original
    data = customer_data.copy()
    
    # Encode categorical features
    if 'gender' in data:
        data['gender'] = encoders['gender'].transform([data['gender']])[0]
    
    if 'subscription_type' in data:
        data['subscription_type'] = encoders['subscription_type'].transform([data['subscription_type']])[0]
    
    # Create feature array in correct order
    features = np.array([[data[fname] for fname in feature_names]])
    
    # Scale features
    features_scaled = encoders['scaler'].transform(features)
    
    return features_scaled


def predict_churn(customer_data, model=None, encoders=None, feature_names=None):
    """
    Predict churn probability for a customer.
    
    Args:
        customer_data: Dictionary with customer features
        model: Trained model (optional, will load if not provided)
        encoders: Fitted encoders (optional, will load if not provided)
        feature_names: Feature names (optional, will load if not provided)
        
    Returns:
        Dictionary with prediction results
    """
    # Load model and encoders if not provided
    if model is None or encoders is None or feature_names is None:
        model, encoders, feature_names = load_model_and_encoders()
    
    # Preprocess the customer data
    features = preprocess_customer_data(customer_data, encoders, feature_names)
    
    # Get prediction and probability
    prediction = model.predict(features)[0]
    
    # Get probability if model supports it
    if hasattr(model, 'predict_proba'):
        probabilities = model.predict_proba(features)[0]
        churn_probability = probabilities[1]  # Probability of churn (class 1)
    else:
        churn_probability = float(prediction)
    
    # Determine risk level
    if churn_probability >= 0.7:
        risk_level = "HIGH"
    elif churn_probability >= 0.4:
        risk_level = "MODERATE"
    else:
        risk_level = "LOW"
    
    return {
        'prediction': int(prediction),
        'prediction_label': 'Churn' if prediction == 1 else 'Stay',
        'churn_probability': float(churn_probability),
        'stay_probability': float(1 - churn_probability),
        'risk_level': risk_level
    }


def main():
    """Test prediction with sample customer data."""
    print("=" * 50)
    print("CUSTOMER CHURN PREDICTION TEST")
    print("=" * 50)
    
    # Sample customer data (high risk)
    high_risk_customer = {
        'age': 25,
        'gender': 'Male',
        'subscription_type': 'Basic',
        'monthly_charges': 12.99,
        'tenure_in_months': 2,
        'login_frequency': 3,
        'last_login_days': 45,
        'watch_time': 2.5,
        'payment_failures': 2,
        'customer_support_calls': 4
    }
    
    # Sample customer data (low risk)
    low_risk_customer = {
        'age': 45,
        'gender': 'Female',
        'subscription_type': 'Premium',
        'monthly_charges': 29.99,
        'tenure_in_months': 48,
        'login_frequency': 25,
        'last_login_days': 1,
        'watch_time': 45.0,
        'payment_failures': 0,
        'customer_support_calls': 1
    }
    
    # Load model once
    model, encoders, feature_names = load_model_and_encoders()
    
    print("\n[TEST 1] High-Risk Customer Profile:")
    print("-" * 40)
    for key, value in high_risk_customer.items():
        print(f"   {key}: {value}")
    
    result1 = predict_churn(high_risk_customer, model, encoders, feature_names)
    print(f"\n   RESULT:")
    print(f"   - Churn Probability: {result1['churn_probability']*100:.1f}%")
    print(f"   - Prediction: {result1['prediction_label']}")
    print(f"   - Risk Level: {result1['risk_level']}")
    
    print("\n[TEST 2] Low-Risk Customer Profile:")
    print("-" * 40)
    for key, value in low_risk_customer.items():
        print(f"   {key}: {value}")
    
    result2 = predict_churn(low_risk_customer, model, encoders, feature_names)
    print(f"\n   RESULT:")
    print(f"   - Churn Probability: {result2['churn_probability']*100:.1f}%")
    print(f"   - Prediction: {result2['prediction_label']}")
    print(f"   - Risk Level: {result2['risk_level']}")
    
    print("\n" + "=" * 50)
    print("[OK] Prediction test complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
