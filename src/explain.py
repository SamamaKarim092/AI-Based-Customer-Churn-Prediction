"""
Explainability Module
Uses SHAP to explain individual churn predictions.
"""

import os
import joblib
import numpy as np
import shap


# Feature descriptions for human-readable explanations
FEATURE_DESCRIPTIONS = {
    'age': {
        'name': 'Age',
        'high_impact': 'Customer age affects engagement patterns',
        'unit': 'years'
    },
    'gender': {
        'name': 'Gender',
        'high_impact': 'Gender influences subscription preferences'
    },
    'subscription_type': {
        'name': 'Subscription Type',
        'high_impact': 'Subscription tier correlates with commitment level'
    },
    'monthly_charges': {
        'name': 'Monthly Charges',
        'high_impact': 'Higher charges may affect retention',
        'unit': '$'
    },
    'tenure_in_months': {
        'name': 'Account Tenure',
        'high_impact': 'Longer tenure indicates customer loyalty',
        'unit': 'months'
    },
    'login_frequency': {
        'name': 'Login Frequency',
        'high_impact': 'Low login frequency suggests disengagement',
        'unit': 'logins/month'
    },
    'last_login_days': {
        'name': 'Days Since Last Login',
        'high_impact': 'Many days since last login indicates potential churn',
        'unit': 'days'
    },
    'watch_time': {
        'name': 'Watch Time',
        'high_impact': 'Low watch time indicates reduced engagement',
        'unit': 'hours/month'
    },
    'payment_failures': {
        'name': 'Payment Failures',
        'high_impact': 'Payment issues strongly predict churn',
        'unit': 'failures'
    },
    'customer_support_calls': {
        'name': 'Support Calls',
        'high_impact': 'Many support calls may indicate frustration',
        'unit': 'calls'
    }
}


def load_model_and_data():
    """Load the trained model and encoders."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    model_dir = os.path.join(project_dir, 'model')
    
    model = joblib.load(os.path.join(model_dir, 'churn_model.pkl'))
    encoders = joblib.load(os.path.join(model_dir, 'encoder.pkl'))
    feature_names = joblib.load(os.path.join(model_dir, 'feature_names.pkl'))
    
    return model, encoders, feature_names


def create_explainer(model, X_background=None):
    """
    Create a SHAP explainer for the model.
    
    Args:
        model: Trained model
        X_background: Background data for SHAP (optional)
        
    Returns:
        SHAP explainer or None for coefficient-based models
    """
    model_type = type(model).__name__
    
    if model_type == 'RandomForestClassifier':
        return shap.TreeExplainer(model)
    else:
        # For Logistic Regression and other models, return None
        # We'll use coefficient-based explanation instead
        return None


def explain_prediction(customer_features, model, feature_names, original_values=None):
    """
    Explain a churn prediction using SHAP values or model coefficients.
    
    Args:
        customer_features: Preprocessed feature array (scaled)
        model: Trained model
        feature_names: List of feature names
        original_values: Original (unscaled) feature values for display
        
    Returns:
        Dictionary with explanation data
    """
    model_type = type(model).__name__
    
    # For Logistic Regression, use coefficients as feature importance
    if model_type == 'LogisticRegression':
        # Get model coefficients
        coefficients = model.coef_[0]
        
        # Calculate feature contributions (coefficient * feature value)
        feature_contributions = coefficients * customer_features[0]
        shap_values_churn = feature_contributions
        base_value = model.intercept_[0]
        
    elif model_type == 'RandomForestClassifier':
        # Use TreeExplainer for Random Forest
        explainer = shap.TreeExplainer(model)
        shap_result = explainer(customer_features)
        
        # Get SHAP values for class 1 (churn)
        if len(shap_result.values.shape) == 3:
            shap_values_churn = shap_result.values[0, :, 1]
        else:
            shap_values_churn = shap_result.values[0]
        
        if hasattr(shap_result, 'base_values'):
            if isinstance(shap_result.base_values, np.ndarray):
                base_value = float(shap_result.base_values[0][1]) if len(shap_result.base_values.shape) > 1 else float(shap_result.base_values[0])
            else:
                base_value = float(shap_result.base_values)
        else:
            base_value = 0.5
    else:
        # Fallback: use feature values as importance (less accurate)
        shap_values_churn = customer_features[0]
        base_value = 0.5
    
    # Create feature importance list
    feature_importance = []
    for i, (fname, shap_val) in enumerate(zip(feature_names, shap_values_churn)):
        feature_info = FEATURE_DESCRIPTIONS.get(fname, {'name': fname})
        
        # Get original value if available
        if original_values and fname in original_values:
            orig_val = original_values[fname]
        else:
            orig_val = customer_features[0][i]
        
        # Determine impact direction and create explanation
        if shap_val > 0:
            impact = "increases"
            impact_direction = "+"
        else:
            impact = "decreases"
            impact_direction = "-"
        
        # Create human-readable explanation
        unit = feature_info.get('unit', '')
        if unit:
            value_str = f"{orig_val} {unit}"
        else:
            value_str = str(orig_val)
        
        explanation = f"{feature_info['name']} ({value_str}) {impact} churn risk"
        
        feature_importance.append({
            'feature': fname,
            'display_name': feature_info['name'],
            'shap_value': float(shap_val),
            'abs_shap_value': abs(float(shap_val)),
            'impact_direction': impact_direction,
            'value': orig_val,
            'explanation': explanation
        })
    
    # Sort by absolute SHAP value (most important first)
    feature_importance.sort(key=lambda x: x['abs_shap_value'], reverse=True)
    
    # Get top 3 factors
    top_factors = feature_importance[:3]
    
    # Create summary explanations
    explanations = []
    for factor in top_factors:
        impact_pct = abs(factor['shap_value']) * 100
        if factor['impact_direction'] == '+':
            explanations.append(f"{factor['explanation']} (+{impact_pct:.1f}%)")
        else:
            explanations.append(f"{factor['explanation']} ({impact_pct:.1f}%)")
    
    return {
        'all_features': feature_importance,
        'top_factors': top_factors,
        'explanations': explanations,
        'base_value': float(base_value)
    }


def main():
    """Test explainability with sample data."""
    print("=" * 50)
    print("SHAP EXPLAINABILITY TEST")
    print("=" * 50)
    
    from predict import predict_churn, load_model_and_encoders, preprocess_customer_data
    
    # Sample high-risk customer
    customer = {
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
    
    print("\n[*] Loading model...")
    model, encoders, feature_names = load_model_and_encoders()
    
    print("\n[*] Getting prediction...")
    prediction = predict_churn(customer, model, encoders, feature_names)
    print(f"   Churn Probability: {prediction['churn_probability']*100:.1f}%")
    print(f"   Risk Level: {prediction['risk_level']}")
    
    print("\n[*] Generating SHAP explanations...")
    features = preprocess_customer_data(customer, encoders, feature_names)
    explanation = explain_prediction(features, model, feature_names, customer)
    
    print("\n" + "-" * 50)
    print("TOP FACTORS INFLUENCING CHURN:")
    print("-" * 50)
    for i, factor in enumerate(explanation['top_factors'], 1):
        print(f"\n   {i}. {factor['explanation']}")
        print(f"      SHAP Impact: {factor['impact_direction']}{abs(factor['shap_value']):.4f}")
    
    print("\n" + "-" * 50)
    print("ALL FEATURE IMPORTANCE:")
    print("-" * 50)
    for factor in explanation['all_features']:
        bar = "+" * int(abs(factor['shap_value']) * 50) if factor['shap_value'] > 0 else "-" * int(abs(factor['shap_value']) * 50)
        print(f"   {factor['display_name']:25s} {factor['impact_direction']}{abs(factor['shap_value']):.4f} {bar}")
    
    print("\n" + "=" * 50)
    print("[OK] Explainability test complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
