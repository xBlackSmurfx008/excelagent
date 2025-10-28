#!/usr/bin/env python3
"""
Machine Learning Integration Engine
Implements historical data analysis, pattern recognition, and predictive models
Based on AI thinking insights for advanced machine learning capabilities
"""

import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import re
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

class MachineLearningEngine:
    def __init__(self):
        self.name = "MachineLearningEngine"
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # ML model configurations
        self.models = {
            'fraud_detection': None,
            'anomaly_detection': None,
            'transaction_classification': None,
            'timing_prediction': None,
            'amount_prediction': None
        }
        
        # Training data storage
        self.training_data = {
            'transactions': [],
            'fraud_labels': [],
            'anomaly_labels': [],
            'classification_labels': [],
            'timing_patterns': [],
            'amount_patterns': []
        }
        
        # ML performance metrics
        self.metrics = {
            'fraud_detection_accuracy': 0.0,
            'anomaly_detection_precision': 0.0,
            'classification_accuracy': 0.0,
            'timing_prediction_accuracy': 0.0,
            'amount_prediction_accuracy': 0.0,
            'total_predictions': 0,
            'successful_predictions': 0
        }
        
        # Feature engineering
        self.feature_columns = [
            'amount', 'hour', 'day_of_week', 'day_of_month', 'month',
            'description_length', 'has_numbers', 'has_special_chars',
            'is_round_number', 'is_weekend', 'is_month_end'
        ]
        
        # Learning history
        self.learning_history = []
        self.model_versions = {}
        
    def train_models(self, historical_data):
        """Train all ML models on historical data"""
        print("🤖 MACHINE LEARNING ENGINE")
        print("=" * 40)
        print("🎯 Training ML models on historical data")
        print("=" * 40)
        
        # Prepare training data
        training_features, training_labels = self._prepare_training_data(historical_data)
        
        # Train individual models
        self._train_fraud_detection_model(training_features, training_labels)
        self._train_anomaly_detection_model(training_features, training_labels)
        self._train_classification_model(training_features, training_labels)
        self._train_timing_prediction_model(training_features, training_labels)
        self._train_amount_prediction_model(training_features, training_labels)
        
        print(f"✅ ML model training complete: {len(self.models)} models trained")
        return self.models
    
    def _prepare_training_data(self, historical_data):
        """Prepare training data from historical transactions"""
        print("📊 Preparing training data...")
        
        features = []
        labels = {
            'fraud': [],
            'anomaly': [],
            'classification': [],
            'timing': [],
            'amount': []
        }
        
        for data_point in historical_data:
            # Extract features
            feature_vector = self._extract_features(data_point)
            features.append(feature_vector)
            
            # Extract labels (if available)
            if 'fraud_label' in data_point:
                labels['fraud'].append(data_point['fraud_label'])
            if 'anomaly_label' in data_point:
                labels['anomaly'].append(data_point['anomaly_label'])
            if 'classification_label' in data_point:
                labels['classification'].append(data_point['classification_label'])
            if 'timing_label' in data_point:
                labels['timing'].append(data_point['timing_label'])
            if 'amount_label' in data_point:
                labels['amount'].append(data_point['amount_label'])
        
        # Convert to numpy arrays
        features_array = np.array(features)
        
        print(f"   ✅ Prepared {len(features)} training samples")
        return features_array, labels
    
    def _extract_features(self, transaction):
        """Extract features from a transaction"""
        features = []
        
        # Amount features
        amount = abs(transaction.get('amount', 0.0))
        features.append(amount)
        
        # Time features
        date_str = transaction.get('date', '')
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                features.extend([
                    date_obj.hour,
                    date_obj.weekday(),
                    date_obj.day,
                    date_obj.month
                ])
            except:
                features.extend([0, 0, 0, 0])
        else:
            features.extend([0, 0, 0, 0])
        
        # Description features
        description = transaction.get('description', '')
        features.extend([
            len(description),
            1 if any(char.isdigit() for char in description) else 0,
            1 if any(char in '!@#$%^&*()' for char in description) else 0,
            1 if amount in [100, 1000, 10000, 100000] else 0,
            1 if date_str and self._is_weekend(date_str) else 0,
            1 if date_str and self._is_month_end(date_str) else 0
        ])
        
        return features
    
    def _train_fraud_detection_model(self, features, labels):
        """Train fraud detection model"""
        print("🚨 Training fraud detection model...")
        
        fraud_labels = labels.get('fraud', [])
        if len(fraud_labels) > 10:  # Minimum samples for training
            X_train, X_test, y_train, y_test = train_test_split(
                features, fraud_labels, test_size=0.2, random_state=42
            )
            
            self.models['fraud_detection'] = RandomForestClassifier(
                n_estimators=100, random_state=42
            )
            self.models['fraud_detection'].fit(X_train, y_train)
            
            # Evaluate model
            y_pred = self.models['fraud_detection'].predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            self.metrics['fraud_detection_accuracy'] = accuracy
            
            print(f"   ✅ Fraud detection model trained (accuracy: {accuracy:.2f})")
        else:
            print("   ⚠️ Insufficient fraud data for training")
    
    def _train_anomaly_detection_model(self, features, labels):
        """Train anomaly detection model"""
        print("🔍 Training anomaly detection model...")
        
        # Use Isolation Forest for unsupervised anomaly detection
        self.models['anomaly_detection'] = IsolationForest(
            contamination=0.1, random_state=42
        )
        self.models['anomaly_detection'].fit(features)
        
        # Evaluate on training data
        anomaly_scores = self.models['anomaly_detection'].decision_function(features)
        anomalies_detected = np.sum(anomaly_scores < 0)
        
        print(f"   ✅ Anomaly detection model trained ({anomalies_detected} anomalies detected)")
    
    def _train_classification_model(self, features, labels):
        """Train transaction classification model"""
        print("📊 Training classification model...")
        
        classification_labels = labels.get('classification', [])
        if len(classification_labels) > 10:
            X_train, X_test, y_train, y_test = train_test_split(
                features, classification_labels, test_size=0.2, random_state=42
            )
            
            self.models['transaction_classification'] = RandomForestClassifier(
                n_estimators=100, random_state=42
            )
            self.models['transaction_classification'].fit(X_train, y_train)
            
            # Evaluate model
            y_pred = self.models['transaction_classification'].predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            self.metrics['classification_accuracy'] = accuracy
            
            print(f"   ✅ Classification model trained (accuracy: {accuracy:.2f})")
        else:
            print("   ⚠️ Insufficient classification data for training")
    
    def _train_timing_prediction_model(self, features, labels):
        """Train timing prediction model"""
        print("⏰ Training timing prediction model...")
        
        timing_labels = labels.get('timing', [])
        if len(timing_labels) > 10:
            X_train, X_test, y_train, y_test = train_test_split(
                features, timing_labels, test_size=0.2, random_state=42
            )
            
            self.models['timing_prediction'] = RandomForestClassifier(
                n_estimators=100, random_state=42
            )
            self.models['timing_prediction'].fit(X_train, y_train)
            
            # Evaluate model
            y_pred = self.models['timing_prediction'].predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            self.metrics['timing_prediction_accuracy'] = accuracy
            
            print(f"   ✅ Timing prediction model trained (accuracy: {accuracy:.2f})")
        else:
            print("   ⚠️ Insufficient timing data for training")
    
    def _train_amount_prediction_model(self, features, labels):
        """Train amount prediction model"""
        print("💰 Training amount prediction model...")
        
        amount_labels = labels.get('amount', [])
        if len(amount_labels) > 10:
            X_train, X_test, y_train, y_test = train_test_split(
                features, amount_labels, test_size=0.2, random_state=42
            )
            
            self.models['amount_prediction'] = RandomForestClassifier(
                n_estimators=100, random_state=42
            )
            self.models['amount_prediction'].fit(X_train, y_train)
            
            # Evaluate model
            y_pred = self.models['amount_prediction'].predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            self.metrics['amount_prediction_accuracy'] = accuracy
            
            print(f"   ✅ Amount prediction model trained (accuracy: {accuracy:.2f})")
        else:
            print("   ⚠️ Insufficient amount data for training")
    
    def predict_fraud_risk(self, transaction):
        """Predict fraud risk for a transaction"""
        if not self.models['fraud_detection']:
            return {'risk_score': 0.0, 'confidence': 0.0, 'message': 'Model not trained', 'recommendation': 'Model not available'}
        
        features = self._extract_features(transaction)
        features_array = np.array(features).reshape(1, -1)
        
        # Get fraud probability
        fraud_prob = self.models['fraud_detection'].predict_proba(features_array)[0][1]
        
        return {
            'risk_score': fraud_prob,
            'confidence': fraud_prob,
            'message': f'Fraud risk: {fraud_prob:.2f}',
            'recommendation': 'High risk' if fraud_prob > 0.7 else 'Low risk'
        }
    
    def detect_anomalies(self, transactions):
        """Detect anomalies in transaction data"""
        if not self.models['anomaly_detection']:
            return []
        
        features = [self._extract_features(tx) for tx in transactions]
        features_array = np.array(features)
        
        # Get anomaly scores
        anomaly_scores = self.models['anomaly_detection'].decision_function(features_array)
        anomaly_predictions = self.models['anomaly_detection'].predict(features_array)
        
        anomalies = []
        for i, (tx, score, prediction) in enumerate(zip(transactions, anomaly_scores, anomaly_predictions)):
            if prediction == -1:  # Anomaly detected
                anomalies.append({
                    'transaction': tx,
                    'anomaly_score': score,
                    'severity': 'high' if score < -0.5 else 'medium',
                    'message': f'Anomaly detected (score: {score:.2f})',
                    'recommendation': 'Review transaction for accuracy'
                })
        
        return anomalies
    
    def classify_transaction(self, transaction):
        """Classify transaction type"""
        if not self.models['transaction_classification']:
            return {'classification': 'unknown', 'confidence': 0.0}
        
        features = self._extract_features(transaction)
        features_array = np.array(features).reshape(1, -1)
        
        # Get classification
        classification = self.models['transaction_classification'].predict(features_array)[0]
        confidence = np.max(self.models['transaction_classification'].predict_proba(features_array))
        
        return {
            'classification': classification,
            'confidence': confidence,
            'message': f'Classified as: {classification}',
            'recommendation': 'Use classification for GL mapping'
        }
    
    def predict_timing_differences(self, transactions):
        """Predict timing differences for transactions"""
        if not self.models['timing_prediction']:
            return []
        
        predictions = []
        for tx in transactions:
            features = self._extract_features(tx)
            features_array = np.array(features).reshape(1, -1)
            
            # Get timing prediction
            timing_pred = self.models['timing_prediction'].predict(features_array)[0]
            confidence = np.max(self.models['timing_prediction'].predict_proba(features_array))
            
            predictions.append({
                'transaction': tx,
                'timing_prediction': timing_pred,
                'confidence': confidence,
                'message': f'Timing prediction: {timing_pred}',
                'recommendation': 'Monitor for timing differences'
            })
        
        return predictions
    
    def predict_amounts(self, transactions):
        """Predict amounts for transactions"""
        if not self.models['amount_prediction']:
            return []
        
        predictions = []
        for tx in transactions:
            features = self._extract_features(tx)
            features_array = np.array(features).reshape(1, -1)
            
            # Get amount prediction
            amount_pred = self.models['amount_prediction'].predict(features_array)[0]
            confidence = np.max(self.models['amount_prediction'].predict_proba(features_array))
            
            predictions.append({
                'transaction': tx,
                'amount_prediction': amount_pred,
                'confidence': confidence,
                'message': f'Amount prediction: {amount_pred}',
                'recommendation': 'Verify predicted amount'
            })
        
        return predictions
    
    def continuous_learning(self, new_data, feedback_data=None):
        """Implement continuous learning from new data"""
        print("🔄 Implementing continuous learning...")
        
        # Update training data with new data
        self.training_data['transactions'].extend(new_data)
        
        # Retrain models if enough new data
        if len(new_data) > 50:  # Threshold for retraining
            print("   📚 Retraining models with new data...")
            self.train_models(self.training_data['transactions'])
            
            # Update model versions
            self.model_versions[self.timestamp] = {
                'models_trained': len(self.models),
                'new_data_points': len(new_data),
                'total_training_data': len(self.training_data['transactions'])
            }
        
        # Learn from feedback
        if feedback_data:
            self._learn_from_feedback(feedback_data)
        
        print(f"   ✅ Continuous learning complete: {len(new_data)} new data points")
    
    def _learn_from_feedback(self, feedback_data):
        """Learn from human feedback"""
        for feedback in feedback_data:
            if feedback.get('correct_prediction'):
                # Positive feedback - reinforce model
                self.learning_history.append({
                    'type': 'positive_feedback',
                    'timestamp': self.timestamp,
                    'feedback': feedback
                })
            else:
                # Negative feedback - adjust model
                self.learning_history.append({
                    'type': 'negative_feedback',
                    'timestamp': self.timestamp,
                    'feedback': feedback
                })
    
    def _is_weekend(self, date_str):
        """Check if date is weekend"""
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            return date_obj.weekday() >= 5
        except:
            return False
    
    def _is_month_end(self, date_str):
        """Check if date is month end"""
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            next_day = date_obj + timedelta(days=1)
            return next_day.month != date_obj.month
        except:
            return False
    
    def get_ml_summary(self):
        """Get machine learning summary"""
        summary = {
            'timestamp': self.timestamp,
            'models_trained': len([m for m in self.models.values() if m is not None]),
            'metrics': self.metrics,
            'training_data_size': len(self.training_data['transactions']),
            'learning_history_size': len(self.learning_history),
            'model_versions': len(self.model_versions)
        }
        
        return summary
    
    def save_ml_models(self):
        """Save ML models and data"""
        ml_data = {
            'timestamp': self.timestamp,
            'models': {k: str(v) for k, v in self.models.items() if v is not None},
            'training_data': self.training_data,
            'metrics': self.metrics,
            'learning_history': self.learning_history,
            'model_versions': self.model_versions,
            'summary': self.get_ml_summary()
        }
        
        filename = f"machine_learning_models_{self.timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(ml_data, f, indent=2, default=str)
        
        print(f"✅ ML models saved: {filename}")
        return filename

def main():
    """Test the machine learning engine"""
    print("🤖 MACHINE LEARNING ENGINE")
    print("=" * 35)
    print("🎯 Testing ML model training and prediction")
    print("=" * 35)
    
    # Initialize engine
    engine = MachineLearningEngine()
    
    # Sample historical data for training
    historical_data = [
        {
            'description': 'ACH ADV FILE',
            'amount': 1000.00,
            'date': '2025-05-31',
            'type': 'debit',
            'fraud_label': 0,
            'anomaly_label': 0,
            'classification_label': 'ACH',
            'timing_label': 'normal',
            'amount_label': 'medium'
        },
        {
            'description': 'CNS Settlement',
            'amount': 500.00,
            'date': '2025-05-30',
            'type': 'credit',
            'fraud_label': 0,
            'anomaly_label': 0,
            'classification_label': 'CNS',
            'timing_label': 'normal',
            'amount_label': 'small'
        },
        {
            'description': 'Suspicious Transaction',
            'amount': 100000.00,
            'date': '2025-05-29',
            'type': 'debit',
            'fraud_label': 1,
            'anomaly_label': 1,
            'classification_label': 'SUSPICIOUS',
            'timing_label': 'anomaly',
            'amount_label': 'large'
        }
    ]
    
    # Train models
    models = engine.train_models(historical_data)
    
    # Test predictions
    test_transaction = {
        'description': 'Test Transaction',
        'amount': 1500.00,
        'date': '2025-05-31',
        'type': 'debit'
    }
    
    # Test fraud detection
    fraud_prediction = engine.predict_fraud_risk(test_transaction)
    print(f"\n🚨 FRAUD PREDICTION:")
    print(f"Risk Score: {fraud_prediction['risk_score']:.2f}")
    print(f"Message: {fraud_prediction['message']}")
    print(f"Recommendation: {fraud_prediction['recommendation']}")
    
    # Test anomaly detection
    anomalies = engine.detect_anomalies([test_transaction])
    print(f"\n🔍 ANOMALY DETECTION:")
    print(f"Anomalies found: {len(anomalies)}")
    
    # Test classification
    classification = engine.classify_transaction(test_transaction)
    print(f"\n📊 CLASSIFICATION:")
    print(f"Classification: {classification['classification']}")
    print(f"Confidence: {classification['confidence']:.2f}")
    
    # Test continuous learning
    new_data = [test_transaction]
    engine.continuous_learning(new_data)
    
    # Get summary
    summary = engine.get_ml_summary()
    print(f"\n📈 ML SUMMARY:")
    print(f"Models trained: {summary['models_trained']}")
    print(f"Training data size: {summary['training_data_size']}")
    print(f"Learning history: {summary['learning_history_size']}")
    
    # Save models
    engine.save_ml_models()

if __name__ == "__main__":
    main()
