#!/usr/bin/env python3
"""
Predictive Analytics Engine
Implements forecasting, risk assessment, and trend analysis
Based on AI thinking insights for advanced predictive capabilities
"""

import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import re
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

class PredictiveAnalyticsEngine:
    def __init__(self):
        self.name = "PredictiveAnalyticsEngine"
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Predictive models
        self.models = {
            'discrepancy_forecast': None,
            'timing_difference_prediction': None,
            'fraud_risk_assessment': None,
            'transaction_volume_forecast': None,
            'balance_trend_analysis': None
        }
        
        # Historical data for analysis
        self.historical_data = {
            'transactions': [],
            'discrepancies': [],
            'timing_differences': [],
            'fraud_incidents': [],
            'balance_history': []
        }
        
        # Predictive analytics metrics
        self.metrics = {
            'forecast_accuracy': 0.0,
            'risk_assessment_accuracy': 0.0,
            'trend_analysis_accuracy': 0.0,
            'total_predictions': 0,
            'successful_predictions': 0,
            'prediction_confidence': 0.0
        }
        
        # Risk assessment thresholds
        self.risk_thresholds = {
            'low_risk': 0.3,
            'medium_risk': 0.6,
            'high_risk': 0.8,
            'critical_risk': 0.9
        }
        
        # Forecasting parameters
        self.forecast_horizon = 30  # days
        self.trend_analysis_window = 90  # days
        
    def train_predictive_models(self, historical_data):
        """Train predictive models on historical data"""
        print("🔮 PREDICTIVE ANALYTICS ENGINE")
        print("=" * 40)
        print("🎯 Training predictive models for forecasting")
        print("=" * 40)
        
        # Store historical data
        self.historical_data.update(historical_data)
        
        # Train individual predictive models
        self._train_discrepancy_forecast_model()
        self._train_timing_difference_prediction_model()
        self._train_fraud_risk_assessment_model()
        self._train_transaction_volume_forecast_model()
        self._train_balance_trend_analysis_model()
        
        print(f"✅ Predictive models training complete: {len(self.models)} models trained")
        return self.models
    
    def _train_discrepancy_forecast_model(self):
        """Train model to forecast discrepancies"""
        print("📊 Training discrepancy forecast model...")
        
        if len(self.historical_data['discrepancies']) > 10:
            # Prepare features and targets
            features, targets = self._prepare_discrepancy_features()
            
            if len(features) > 0:
                # Train regression model
                self.models['discrepancy_forecast'] = RandomForestRegressor(
                    n_estimators=100, random_state=42
                )
                self.models['discrepancy_forecast'].fit(features, targets)
                
                # Evaluate model
                predictions = self.models['discrepancy_forecast'].predict(features)
                mse = mean_squared_error(targets, predictions)
                r2 = r2_score(targets, predictions)
                
                print(f"   ✅ Discrepancy forecast model trained (R²: {r2:.2f})")
            else:
                print("   ⚠️ Insufficient discrepancy data for training")
        else:
            print("   ⚠️ Insufficient discrepancy data for training")
    
    def _train_timing_difference_prediction_model(self):
        """Train model to predict timing differences"""
        print("⏰ Training timing difference prediction model...")
        
        if len(self.historical_data['timing_differences']) > 10:
            # Prepare features and targets
            features, targets = self._prepare_timing_features()
            
            if len(features) > 0:
                # Train regression model
                self.models['timing_difference_prediction'] = RandomForestRegressor(
                    n_estimators=100, random_state=42
                )
                self.models['timing_difference_prediction'].fit(features, targets)
                
                # Evaluate model
                predictions = self.models['timing_difference_prediction'].predict(features)
                mse = mean_squared_error(targets, predictions)
                r2 = r2_score(targets, predictions)
                
                print(f"   ✅ Timing difference prediction model trained (R²: {r2:.2f})")
            else:
                print("   ⚠️ Insufficient timing data for training")
        else:
            print("   ⚠️ Insufficient timing data for training")
    
    def _train_fraud_risk_assessment_model(self):
        """Train model for fraud risk assessment"""
        print("🚨 Training fraud risk assessment model...")
        
        if len(self.historical_data['fraud_incidents']) > 10:
            # Prepare features and targets
            features, targets = self._prepare_fraud_features()
            
            if len(features) > 0:
                # Train regression model
                self.models['fraud_risk_assessment'] = RandomForestRegressor(
                    n_estimators=100, random_state=42
                )
                self.models['fraud_risk_assessment'].fit(features, targets)
                
                # Evaluate model
                predictions = self.models['fraud_risk_assessment'].predict(features)
                mse = mean_squared_error(targets, predictions)
                r2 = r2_score(targets, predictions)
                
                print(f"   ✅ Fraud risk assessment model trained (R²: {r2:.2f})")
            else:
                print("   ⚠️ Insufficient fraud data for training")
        else:
            print("   ⚠️ Insufficient fraud data for training")
    
    def _train_transaction_volume_forecast_model(self):
        """Train model to forecast transaction volumes"""
        print("📈 Training transaction volume forecast model...")
        
        if len(self.historical_data['transactions']) > 50:
            # Prepare features and targets
            features, targets = self._prepare_volume_features()
            
            if len(features) > 0:
                # Train regression model
                self.models['transaction_volume_forecast'] = RandomForestRegressor(
                    n_estimators=100, random_state=42
                )
                self.models['transaction_volume_forecast'].fit(features, targets)
                
                # Evaluate model
                predictions = self.models['transaction_volume_forecast'].predict(features)
                mse = mean_squared_error(targets, predictions)
                r2 = r2_score(targets, predictions)
                
                print(f"   ✅ Transaction volume forecast model trained (R²: {r2:.2f})")
            else:
                print("   ⚠️ Insufficient transaction data for training")
        else:
            print("   ⚠️ Insufficient transaction data for training")
    
    def _train_balance_trend_analysis_model(self):
        """Train model for balance trend analysis"""
        print("💰 Training balance trend analysis model...")
        
        if len(self.historical_data['balance_history']) > 30:
            # Prepare features and targets
            features, targets = self._prepare_balance_features()
            
            if len(features) > 0:
                # Train regression model
                self.models['balance_trend_analysis'] = RandomForestRegressor(
                    n_estimators=100, random_state=42
                )
                self.models['balance_trend_analysis'].fit(features, targets)
                
                # Evaluate model
                predictions = self.models['balance_trend_analysis'].predict(features)
                mse = mean_squared_error(targets, predictions)
                r2 = r2_score(targets, predictions)
                
                print(f"   ✅ Balance trend analysis model trained (R²: {r2:.2f})")
            else:
                print("   ⚠️ Insufficient balance data for training")
        else:
            print("   ⚠️ Insufficient balance data for training")
    
    def _prepare_discrepancy_features(self):
        """Prepare features for discrepancy forecasting"""
        features = []
        targets = []
        
        for discrepancy in self.historical_data['discrepancies']:
            # Extract features
            feature_vector = [
                discrepancy.get('amount', 0.0),
                discrepancy.get('gl_account', 0),
                discrepancy.get('month', 0),
                discrepancy.get('day_of_week', 0),
                discrepancy.get('is_month_end', 0)
            ]
            features.append(feature_vector)
            
            # Target is the discrepancy amount
            targets.append(discrepancy.get('amount', 0.0))
        
        return np.array(features), np.array(targets)
    
    def _prepare_timing_features(self):
        """Prepare features for timing difference prediction"""
        features = []
        targets = []
        
        for timing_diff in self.historical_data['timing_differences']:
            # Extract features
            feature_vector = [
                timing_diff.get('amount', 0.0),
                timing_diff.get('gl_account', 0),
                timing_diff.get('month', 0),
                timing_diff.get('day_of_week', 0),
                timing_diff.get('is_month_end', 0)
            ]
            features.append(feature_vector)
            
            # Target is the timing difference amount
            targets.append(timing_diff.get('amount', 0.0))
        
        return np.array(features), np.array(targets)
    
    def _prepare_fraud_features(self):
        """Prepare features for fraud risk assessment"""
        features = []
        targets = []
        
        for fraud_incident in self.historical_data['fraud_incidents']:
            # Extract features
            feature_vector = [
                fraud_incident.get('amount', 0.0),
                fraud_incident.get('hour', 0),
                fraud_incident.get('day_of_week', 0),
                fraud_incident.get('is_weekend', 0),
                fraud_incident.get('description_length', 0)
            ]
            features.append(feature_vector)
            
            # Target is the fraud risk score
            targets.append(fraud_incident.get('risk_score', 0.0))
        
        return np.array(features), np.array(targets)
    
    def _prepare_volume_features(self):
        """Prepare features for transaction volume forecasting"""
        features = []
        targets = []
        
        # Group transactions by date
        daily_volumes = defaultdict(int)
        for tx in self.historical_data['transactions']:
            date = tx.get('date', '')
            if date:
                daily_volumes[date] += 1
        
        # Create features for each day
        for date, volume in daily_volumes.items():
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                feature_vector = [
                    date_obj.month,
                    date_obj.day,
                    date_obj.weekday(),
                    date_obj.day <= 7,  # First week of month
                    date_obj.day >= 25,  # Last week of month
                    date_obj.weekday() >= 5  # Weekend
                ]
                features.append(feature_vector)
                targets.append(volume)
            except:
                continue
        
        return np.array(features), np.array(targets)
    
    def _prepare_balance_features(self):
        """Prepare features for balance trend analysis"""
        features = []
        targets = []
        
        for balance_record in self.historical_data['balance_history']:
            # Extract features
            feature_vector = [
                balance_record.get('month', 0),
                balance_record.get('day', 0),
                balance_record.get('day_of_week', 0),
                balance_record.get('is_month_end', 0),
                balance_record.get('transaction_count', 0)
            ]
            features.append(feature_vector)
            
            # Target is the balance amount
            targets.append(balance_record.get('balance', 0.0))
        
        return np.array(features), np.array(targets)
    
    def forecast_discrepancies(self, forecast_period=30):
        """Forecast discrepancies for the next period"""
        if not self.models['discrepancy_forecast']:
            return {'forecast': [], 'confidence': 0.0, 'message': 'Model not trained'}
        
        # Generate forecast features
        forecast_features = self._generate_forecast_features(forecast_period)
        
        # Make predictions
        predictions = self.models['discrepancy_forecast'].predict(forecast_features)
        
        # Calculate confidence
        confidence = np.mean(predictions) / max(np.std(predictions), 1.0)
        
        return {
            'forecast': predictions.tolist(),
            'confidence': min(1.0, confidence),
            'message': f'Discrepancy forecast for {forecast_period} days',
            'recommendation': 'Monitor for predicted discrepancies'
        }
    
    def predict_timing_differences(self, gl_accounts):
        """Predict timing differences for GL accounts"""
        if not self.models['timing_difference_prediction']:
            return []
        
        predictions = []
        for gl_account in gl_accounts:
            # Generate features for GL account
            features = self._generate_gl_account_features(gl_account)
            
            # Make prediction
            prediction = self.models['timing_difference_prediction'].predict([features])[0]
            
            predictions.append({
                'gl_account': gl_account,
                'predicted_timing_difference': prediction,
                'confidence': min(1.0, prediction / 1000),  # Normalize confidence
                'message': f'Predicted timing difference: ${prediction:.2f}',
                'recommendation': 'Monitor for timing differences'
            })
        
        return predictions
    
    def assess_fraud_risk(self, transactions):
        """Assess fraud risk for transactions"""
        if not self.models['fraud_risk_assessment']:
            return []
        
        risk_assessments = []
        for tx in transactions:
            # Generate features for transaction
            features = self._generate_transaction_features(tx)
            
            # Make risk assessment
            risk_score = self.models['fraud_risk_assessment'].predict([features])[0]
            
            # Determine risk level
            risk_level = self._determine_risk_level(risk_score)
            
            risk_assessments.append({
                'transaction': tx,
                'risk_score': risk_score,
                'risk_level': risk_level,
                'confidence': min(1.0, risk_score),
                'message': f'Fraud risk: {risk_score:.2f} ({risk_level})',
                'recommendation': self._get_risk_recommendation(risk_level)
            })
        
        return risk_assessments
    
    def forecast_transaction_volumes(self, forecast_period=30):
        """Forecast transaction volumes for the next period"""
        if not self.models['transaction_volume_forecast']:
            return {'forecast': [], 'confidence': 0.0, 'message': 'Model not trained'}
        
        # Generate forecast features
        forecast_features = self._generate_forecast_features(forecast_period)
        
        # Make predictions
        predictions = self.models['transaction_volume_forecast'].predict(forecast_features)
        
        # Calculate confidence
        confidence = np.mean(predictions) / max(np.std(predictions), 1.0)
        
        return {
            'forecast': predictions.tolist(),
            'confidence': min(1.0, confidence),
            'message': f'Transaction volume forecast for {forecast_period} days',
            'recommendation': 'Plan resources based on forecast'
        }
    
    def analyze_balance_trends(self, current_balance):
        """Analyze balance trends and predict future balance"""
        if not self.models['balance_trend_analysis']:
            return {
                'current_balance': current_balance,
                'predicted_balance': current_balance,
                'trend': 'unknown',
                'confidence': 0.0,
                'message': 'Model not trained',
                'recommendation': 'Model not available'
            }
        
        # Generate features for current balance
        current_date = datetime.now()
        features = [
            current_date.month,
            current_date.day,
            current_date.weekday(),
            current_date.day >= 25,  # Last week of month
            current_date.weekday() >= 5  # Weekend
        ]
        
        # Make prediction
        predicted_balance = self.models['balance_trend_analysis'].predict([features])[0]
        
        # Determine trend
        trend = 'increasing' if predicted_balance > current_balance else 'decreasing'
        
        return {
            'current_balance': current_balance,
            'predicted_balance': predicted_balance,
            'trend': trend,
            'confidence': min(1.0, abs(predicted_balance - current_balance) / max(current_balance, 1.0)),
            'message': f'Balance trend: {trend} (predicted: ${predicted_balance:.2f})',
            'recommendation': 'Monitor balance changes'
        }
    
    def _generate_forecast_features(self, forecast_period):
        """Generate features for forecasting"""
        features = []
        current_date = datetime.now()
        
        for i in range(forecast_period):
            forecast_date = current_date + timedelta(days=i)
            feature_vector = [
                forecast_date.month,
                forecast_date.day,
                forecast_date.weekday(),
                forecast_date.day <= 7,  # First week
                forecast_date.day >= 25,  # Last week
                forecast_date.weekday() >= 5  # Weekend
            ]
            features.append(feature_vector)
        
        return np.array(features)
    
    def _generate_gl_account_features(self, gl_account):
        """Generate features for GL account"""
        return [
            int(gl_account) if gl_account.isdigit() else 0,
            datetime.now().month,
            datetime.now().day,
            datetime.now().weekday(),
            datetime.now().day >= 25  # Month end
        ]
    
    def _generate_transaction_features(self, transaction):
        """Generate features for transaction"""
        amount = abs(transaction.get('amount', 0.0))
        date_str = transaction.get('date', '')
        
        # Parse date
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            hour = date_obj.hour
            day_of_week = date_obj.weekday()
            is_weekend = day_of_week >= 5
        except:
            hour = 0
            day_of_week = 0
            is_weekend = False
        
        description = transaction.get('description', '')
        
        return [
            amount,
            hour,
            day_of_week,
            is_weekend,
            len(description)
        ]
    
    def _determine_risk_level(self, risk_score):
        """Determine risk level based on score"""
        if risk_score < self.risk_thresholds['low_risk']:
            return 'low'
        elif risk_score < self.risk_thresholds['medium_risk']:
            return 'medium'
        elif risk_score < self.risk_thresholds['high_risk']:
            return 'high'
        else:
            return 'critical'
    
    def _get_risk_recommendation(self, risk_level):
        """Get recommendation based on risk level"""
        recommendations = {
            'low': 'Continue monitoring',
            'medium': 'Review transaction details',
            'high': 'Investigate immediately',
            'critical': 'Escalate to fraud team'
        }
        return recommendations.get(risk_level, 'Review transaction')
    
    def get_analytics_summary(self):
        """Get predictive analytics summary"""
        summary = {
            'timestamp': self.timestamp,
            'models_trained': len([m for m in self.models.values() if m is not None]),
            'metrics': self.metrics,
            'historical_data_size': len(self.historical_data['transactions']),
            'forecast_horizon': self.forecast_horizon,
            'trend_analysis_window': self.trend_analysis_window
        }
        
        return summary
    
    def save_analytics_models(self):
        """Save predictive analytics models"""
        analytics_data = {
            'timestamp': self.timestamp,
            'models': {k: str(v) for k, v in self.models.items() if v is not None},
            'historical_data': self.historical_data,
            'metrics': self.metrics,
            'risk_thresholds': self.risk_thresholds,
            'summary': self.get_analytics_summary()
        }
        
        filename = f"predictive_analytics_models_{self.timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(analytics_data, f, indent=2, default=str)
        
        print(f"✅ Predictive analytics models saved: {filename}")
        return filename

def main():
    """Test the predictive analytics engine"""
    print("🔮 PREDICTIVE ANALYTICS ENGINE")
    print("=" * 40)
    print("🎯 Testing predictive analytics and forecasting")
    print("=" * 40)
    
    # Initialize engine
    engine = PredictiveAnalyticsEngine()
    
    # Sample historical data
    historical_data = {
        'transactions': [
            {'description': 'ACH ADV FILE', 'amount': 1000.00, 'date': '2025-05-31', 'type': 'debit'},
            {'description': 'CNS Settlement', 'amount': 500.00, 'date': '2025-05-30', 'type': 'credit'},
            {'description': 'EFUNDS Corp', 'amount': 750.00, 'date': '2025-05-29', 'type': 'credit'}
        ],
        'discrepancies': [
            {'amount': 100.00, 'gl_account': '74400', 'month': 5, 'day_of_week': 0, 'is_month_end': True},
            {'amount': 200.00, 'gl_account': '74505', 'month': 5, 'day_of_week': 1, 'is_month_end': False}
        ],
        'timing_differences': [
            {'amount': 150.00, 'gl_account': '74510', 'month': 5, 'day_of_week': 0, 'is_month_end': True},
            {'amount': 300.00, 'gl_account': '74560', 'month': 5, 'day_of_week': 1, 'is_month_end': False}
        ],
        'fraud_incidents': [
            {'amount': 1000.00, 'hour': 14, 'day_of_week': 0, 'is_weekend': False, 'description_length': 10, 'risk_score': 0.3},
            {'amount': 5000.00, 'hour': 2, 'day_of_week': 6, 'is_weekend': True, 'description_length': 5, 'risk_score': 0.8}
        ],
        'balance_history': [
            {'month': 5, 'day': 31, 'day_of_week': 0, 'is_month_end': True, 'transaction_count': 10, 'balance': 1000.00},
            {'month': 5, 'day': 30, 'day_of_week': 6, 'is_month_end': False, 'transaction_count': 5, 'balance': 500.00}
        ]
    }
    
    # Train models
    models = engine.train_predictive_models(historical_data)
    
    # Test forecasting
    discrepancy_forecast = engine.forecast_discrepancies(30)
    print(f"\n📊 DISCREPANCY FORECAST:")
    print(f"Forecast period: 30 days")
    print(f"Confidence: {discrepancy_forecast['confidence']:.2f}")
    print(f"Message: {discrepancy_forecast['message']}")
    
    # Test timing difference prediction
    timing_predictions = engine.predict_timing_differences(['74400', '74505'])
    print(f"\n⏰ TIMING DIFFERENCE PREDICTIONS:")
    for prediction in timing_predictions:
        print(f"GL {prediction['gl_account']}: ${prediction['predicted_timing_difference']:.2f}")
        print(f"Confidence: {prediction['confidence']:.2f}")
    
    # Test fraud risk assessment
    test_transactions = [
        {'description': 'Test Transaction', 'amount': 1000.00, 'date': '2025-05-31', 'type': 'debit'}
    ]
    fraud_assessments = engine.assess_fraud_risk(test_transactions)
    print(f"\n🚨 FRAUD RISK ASSESSMENTS:")
    for assessment in fraud_assessments:
        print(f"Risk Score: {assessment['risk_score']:.2f}")
        print(f"Risk Level: {assessment['risk_level']}")
        print(f"Recommendation: {assessment['recommendation']}")
    
    # Test balance trend analysis
    balance_trend = engine.analyze_balance_trends(1000.00)
    print(f"\n💰 BALANCE TREND ANALYSIS:")
    print(f"Current Balance: ${balance_trend['current_balance']:.2f}")
    print(f"Predicted Balance: ${balance_trend['predicted_balance']:.2f}")
    print(f"Trend: {balance_trend['trend']}")
    print(f"Confidence: {balance_trend['confidence']:.2f}")
    
    # Get summary
    summary = engine.get_analytics_summary()
    print(f"\n📈 ANALYTICS SUMMARY:")
    print(f"Models trained: {summary['models_trained']}")
    print(f"Historical data size: {summary['historical_data_size']}")
    print(f"Forecast horizon: {summary['forecast_horizon']} days")
    
    # Save models
    engine.save_analytics_models()

if __name__ == "__main__":
    main()
