"""
Model Training Script
Trains and compares multiple ML models for customer churn prediction.
Saves the best performing model and encoder.
"""

import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix


def load_and_preprocess_data(data_path):
    """
    Load and preprocess the customer data.
    
    Args:
        data_path: Path to the CSV file
        
    Returns:
        X: Feature matrix
        y: Target variable
        encoders: Dictionary of fitted encoders
        feature_names: List of feature names
    """
    print("\n[1/5] Loading data...")
    df = pd.read_csv(data_path)
    print(f"   Loaded {len(df)} records")
    
    # Drop customer_id as it's not a feature
    df = df.drop('customer_id', axis=1)
    
    print("\n[2/5] Encoding categorical features...")
    encoders = {}
    
    # Encode gender
    le_gender = LabelEncoder()
    df['gender'] = le_gender.fit_transform(df['gender'])
    encoders['gender'] = le_gender
    print(f"   Gender mapping: {dict(zip(le_gender.classes_, le_gender.transform(le_gender.classes_)))}")
    
    # Encode subscription_type
    le_subscription = LabelEncoder()
    df['subscription_type'] = le_subscription.fit_transform(df['subscription_type'])
    encoders['subscription_type'] = le_subscription
    print(f"   Subscription mapping: {dict(zip(le_subscription.classes_, le_subscription.transform(le_subscription.classes_)))}")
    
    # Separate features and target
    X = df.drop('churn', axis=1)
    y = df['churn']
    
    feature_names = X.columns.tolist()
    
    print("\n[3/5] Scaling numerical features...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    encoders['scaler'] = scaler
    
    return X_scaled, y, encoders, feature_names


def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    """
    Train multiple models and compare their performance.
    
    Returns:
        best_model: The best performing model
        results: Dictionary of results for all models
    """
    print("\n[4/5] Training models...")
    
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Naive Bayes': GaussianNB(),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    }
    
    results = {}
    best_accuracy = 0
    best_model_name = None
    best_model = None
    
    for name, model in models.items():
        print(f"\n   Training {name}...")
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        results[name] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'model': model
        }
        
        print(f"   {name} Results:")
        print(f"      Accuracy:  {accuracy:.4f}")
        print(f"      Precision: {precision:.4f}")
        print(f"      Recall:    {recall:.4f}")
        print(f"      F1-Score:  {f1:.4f}")
        
        # Track best model
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model_name = name
            best_model = model
    
    print(f"\n   [BEST] {best_model_name} with {best_accuracy:.4f} accuracy")
    
    return best_model, best_model_name, results


def save_model_and_encoder(model, encoders, feature_names, model_dir):
    """Save the trained model and encoders."""
    print("\n[5/5] Saving model and encoders...")
    
    # Create model directory if it doesn't exist
    os.makedirs(model_dir, exist_ok=True)
    
    # Save the model
    model_path = os.path.join(model_dir, 'churn_model.pkl')
    joblib.dump(model, model_path)
    print(f"   Model saved to: {model_path}")
    
    # Save encoders
    encoder_path = os.path.join(model_dir, 'encoder.pkl')
    joblib.dump(encoders, encoder_path)
    print(f"   Encoders saved to: {encoder_path}")
    
    # Save feature names for later use
    feature_path = os.path.join(model_dir, 'feature_names.pkl')
    joblib.dump(feature_names, feature_path)
    print(f"   Feature names saved to: {feature_path}")


def print_detailed_report(model, X_test, y_test, model_name):
    """Print detailed classification report and confusion matrix."""
    y_pred = model.predict(X_test)
    
    print("\n" + "=" * 50)
    print(f"DETAILED REPORT - {model_name}")
    print("=" * 50)
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Stay', 'Churn']))
    
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"                  Predicted")
    print(f"                  Stay  Churn")
    print(f"   Actual Stay    {cm[0][0]:4d}  {cm[0][1]:4d}")
    print(f"   Actual Churn   {cm[1][0]:4d}  {cm[1][1]:4d}")


def main():
    """Main function to run the training pipeline."""
    print("=" * 50)
    print("CUSTOMER CHURN MODEL TRAINING")
    print("=" * 50)
    
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    data_path = os.path.join(project_dir, 'data', 'customers.csv')
    model_dir = os.path.join(project_dir, 'model')
    
    # Check if data exists
    if not os.path.exists(data_path):
        print(f"\n[ERROR] Dataset not found at: {data_path}")
        print("Please run data/generate_data.py first to create the dataset.")
        return
    
    # Load and preprocess data
    X, y, encoders, feature_names = load_and_preprocess_data(data_path)
    
    # Split data
    print("\n   Splitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   Training samples: {len(X_train)}")
    print(f"   Testing samples: {len(X_test)}")
    
    # Train and evaluate models
    best_model, best_model_name, results = train_and_evaluate_models(X_train, X_test, y_train, y_test)
    
    # Print detailed report for the best model
    print_detailed_report(best_model, X_test, y_test, best_model_name)
    
    # Save model and encoders
    save_model_and_encoder(best_model, encoders, feature_names, model_dir)
    
    # Summary
    print("\n" + "=" * 50)
    print("MODEL COMPARISON SUMMARY")
    print("=" * 50)
    print("\n{:<25} {:>10} {:>10} {:>10} {:>10}".format(
        "Model", "Accuracy", "Precision", "Recall", "F1-Score"
    ))
    print("-" * 65)
    for name, metrics in results.items():
        marker = " [BEST]" if name == best_model_name else ""
        print("{:<25} {:>10.4f} {:>10.4f} {:>10.4f} {:>10.4f}{}".format(
            name,
            metrics['accuracy'],
            metrics['precision'],
            metrics['recall'],
            metrics['f1_score'],
            marker
        ))
    
    print("\n" + "=" * 50)
    print("[OK] Training complete! Model saved successfully.")
    print("=" * 50)


if __name__ == "__main__":
    main()
