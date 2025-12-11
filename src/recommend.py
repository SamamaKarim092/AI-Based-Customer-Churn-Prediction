"""
Action Recommendation Module
Provides business actions based on churn prediction and contributing factors.
"""


# Recommendation rules based on churn probability levels
CHURN_RECOMMENDATIONS = {
    'HIGH': {
        'threshold': 0.7,
        'urgency': 'URGENT',
        'base_action': 'Immediate retention intervention required',
        'actions': [
            'Offer personalized discount (20-30% off)',
            'Assign dedicated account manager',
            'Send personalized re-engagement email',
            'Offer free premium features trial'
        ]
    },
    'MODERATE': {
        'threshold': 0.4,
        'urgency': 'MODERATE',
        'base_action': 'Proactive engagement recommended',
        'actions': [
            'Send re-engagement notification',
            'Offer limited-time discount (10-15% off)',
            'Highlight new features via email',
            'Invite to customer feedback survey'
        ]
    },
    'LOW': {
        'threshold': 0.0,
        'urgency': 'LOW',
        'base_action': 'Standard customer maintenance',
        'actions': [
            'Continue regular engagement',
            'Include in loyalty rewards program',
            'Send monthly newsletter',
            'No immediate action required'
        ]
    }
}

# Factor-specific recommendations
FACTOR_RECOMMENDATIONS = {
    'last_login_days': {
        'condition': lambda x: x > 14,
        'action': 'Send "We miss you" email with exclusive content',
        'reason': 'Customer has not logged in recently'
    },
    'login_frequency': {
        'condition': lambda x: x < 5,
        'action': 'Recommend personalized content based on past preferences',
        'reason': 'Low engagement - customer rarely logs in'
    },
    'watch_time': {
        'condition': lambda x: x < 10,
        'action': 'Send curated content recommendations to boost engagement',
        'reason': 'Low content consumption'
    },
    'payment_failures': {
        'condition': lambda x: x > 0,
        'action': 'Reach out to resolve payment issues and offer alternative payment methods',
        'reason': 'Payment problems detected'
    },
    'customer_support_calls': {
        'condition': lambda x: x > 3,
        'action': 'Proactive outreach to resolve ongoing issues',
        'reason': 'Multiple support interactions indicate frustration'
    },
    'tenure_in_months': {
        'condition': lambda x: x < 6,
        'action': 'Onboarding follow-up to ensure customer is getting value',
        'reason': 'New customer - critical retention period'
    },
    'monthly_charges': {
        'condition': lambda x: x > 25,
        'action': 'Highlight value proposition and premium benefits',
        'reason': 'High subscription cost may affect retention'
    }
}


def get_risk_level(churn_probability):
    """Determine risk level based on churn probability."""
    if churn_probability >= 0.7:
        return 'HIGH'
    elif churn_probability >= 0.4:
        return 'MODERATE'
    else:
        return 'LOW'


def get_base_recommendation(churn_probability):
    """Get the base recommendation based on churn probability."""
    risk_level = get_risk_level(churn_probability)
    rec = CHURN_RECOMMENDATIONS[risk_level]
    
    return {
        'risk_level': risk_level,
        'urgency': rec['urgency'],
        'primary_action': rec['base_action'],
        'suggested_actions': rec['actions'].copy(),
        'churn_probability': churn_probability
    }


def get_factor_specific_recommendations(customer_data, top_factors=None):
    """
    Get recommendations based on specific customer factors.
    
    Args:
        customer_data: Dictionary of customer features
        top_factors: List of top SHAP factors (optional)
        
    Returns:
        List of factor-specific recommendations
    """
    recommendations = []
    
    for feature, rec_info in FACTOR_RECOMMENDATIONS.items():
        if feature in customer_data:
            value = customer_data[feature]
            if rec_info['condition'](value):
                recommendations.append({
                    'feature': feature,
                    'value': value,
                    'reason': rec_info['reason'],
                    'action': rec_info['action'],
                    'is_top_factor': top_factors is not None and feature in [f.get('feature') for f in top_factors]
                })
    
    # Sort by whether it's a top factor
    recommendations.sort(key=lambda x: (not x['is_top_factor'], -x.get('value', 0)))
    
    return recommendations


def generate_full_recommendation(churn_probability, customer_data, top_factors=None):
    """
    Generate a complete recommendation report.
    
    Args:
        churn_probability: Predicted churn probability
        customer_data: Dictionary of customer features
        top_factors: List of top SHAP factors from explainability module
        
    Returns:
        Complete recommendation dictionary
    """
    # Get base recommendation
    base_rec = get_base_recommendation(churn_probability)
    
    # Get factor-specific recommendations
    factor_recs = get_factor_specific_recommendations(customer_data, top_factors)
    
    # Prioritize actions based on top factors
    prioritized_actions = []
    for factor_rec in factor_recs:
        if factor_rec['is_top_factor']:
            prioritized_actions.insert(0, factor_rec['action'])
        else:
            prioritized_actions.append(factor_rec['action'])
    
    # Combine and deduplicate actions
    all_actions = prioritized_actions + base_rec['suggested_actions']
    unique_actions = list(dict.fromkeys(all_actions))  # Remove duplicates while preserving order
    
    # Generate summary message
    risk_level = base_rec['risk_level']
    if risk_level == 'HIGH':
        summary = f"ALERT: This customer has a {churn_probability*100:.0f}% probability of churning. Immediate action required!"
    elif risk_level == 'MODERATE':
        summary = f"CAUTION: This customer has a {churn_probability*100:.0f}% probability of churning. Proactive engagement recommended."
    else:
        summary = f"OK: This customer has a low churn risk ({churn_probability*100:.0f}%). Continue standard engagement."
    
    return {
        'summary': summary,
        'risk_level': risk_level,
        'urgency': base_rec['urgency'],
        'churn_probability': churn_probability,
        'primary_action': base_rec['primary_action'],
        'recommended_actions': unique_actions[:5],  # Top 5 actions
        'factor_insights': factor_recs,
        'all_suggested_actions': unique_actions
    }


def format_recommendation_report(recommendation):
    """Format recommendation as a readable text report."""
    lines = []
    lines.append("=" * 60)
    lines.append("ACTION RECOMMENDATION REPORT")
    lines.append("=" * 60)
    
    lines.append(f"\n{recommendation['summary']}")
    lines.append(f"\nRisk Level: {recommendation['risk_level']}")
    lines.append(f"Urgency: {recommendation['urgency']}")
    lines.append(f"Churn Probability: {recommendation['churn_probability']*100:.1f}%")
    
    lines.append(f"\n{'-' * 60}")
    lines.append("PRIMARY ACTION:")
    lines.append(f"  >> {recommendation['primary_action']}")
    
    lines.append(f"\n{'-' * 60}")
    lines.append("RECOMMENDED ACTIONS:")
    for i, action in enumerate(recommendation['recommended_actions'], 1):
        lines.append(f"  {i}. {action}")
    
    if recommendation['factor_insights']:
        lines.append(f"\n{'-' * 60}")
        lines.append("FACTOR-SPECIFIC INSIGHTS:")
        for insight in recommendation['factor_insights']:
            marker = "[TOP FACTOR]" if insight['is_top_factor'] else ""
            lines.append(f"\n  {insight['feature'].upper()} {marker}")
            lines.append(f"    Reason: {insight['reason']}")
            lines.append(f"    Action: {insight['action']}")
    
    lines.append("\n" + "=" * 60)
    
    return "\n".join(lines)


def main():
    """Test recommendation system."""
    print("=" * 50)
    print("ACTION RECOMMENDATION TEST")
    print("=" * 50)
    
    # Simulate a high-risk customer
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
    
    # Simulate top factors from SHAP
    top_factors = [
        {'feature': 'last_login_days', 'shap_value': 0.25},
        {'feature': 'payment_failures', 'shap_value': 0.18},
        {'feature': 'login_frequency', 'shap_value': 0.12}
    ]
    
    print("\n[TEST 1] High-Risk Customer (78% churn probability)")
    print("-" * 50)
    
    rec = generate_full_recommendation(0.78, high_risk_customer, top_factors)
    print(format_recommendation_report(rec))
    
    # Simulate a low-risk customer
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
    
    print("\n[TEST 2] Low-Risk Customer (12% churn probability)")
    print("-" * 50)
    
    rec2 = generate_full_recommendation(0.12, low_risk_customer, [])
    print(format_recommendation_report(rec2))
    
    print("\n[OK] Recommendation test complete!")


if __name__ == "__main__":
    main()
