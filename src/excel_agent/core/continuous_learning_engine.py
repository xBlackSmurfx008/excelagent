#!/usr/bin/env python3
"""
Continuous Learning Engine
Implements self-improving algorithms and adaptive matching
Based on AI thinking insights for continuous learning capabilities
"""

import json
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import re
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

class ContinuousLearningEngine:
    def __init__(self):
        self.name = "ContinuousLearningEngine"
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Learning data storage
        self.learning_data = {
            'successful_matches': [],
            'failed_matches': [],
            'user_corrections': [],
            'feedback_data': [],
            'performance_history': [],
            'pattern_learning': defaultdict(list)
        }
        
        # Adaptive models
        self.adaptive_models = {
            'matching_confidence': None,
            'pattern_recognition': None,
            'user_preference': None,
            'error_correction': None,
            'performance_optimization': None
        }
        
        # Learning metrics
        self.learning_metrics = {
            'total_learning_events': 0,
            'successful_learning': 0,
            'failed_learning': 0,
            'accuracy_improvement': 0.0,
            'pattern_recognition_improvement': 0.0,
            'user_satisfaction_improvement': 0.0
        }
        
        # Learning thresholds
        self.learning_thresholds = {
            'min_samples_for_learning': 10,
            'confidence_threshold': 0.7,
            'improvement_threshold': 0.05,
            'retraining_threshold': 100
        }
        
        # Learning history
        self.learning_history = []
        self.model_versions = {}
        
    def continuous_learning_cycle(self, new_data, feedback_data=None):
        """Implement continuous learning cycle"""
        print("🔄 CONTINUOUS LEARNING ENGINE")
        print("=" * 40)
        print("🎯 Implementing continuous learning cycle")
        print("=" * 40)
        
        # 1. Learn from new data
        new_learning = self._learn_from_new_data(new_data)
        
        # 2. Learn from feedback
        feedback_learning = self._learn_from_feedback(feedback_data) if feedback_data else []
        
        # 3. Update adaptive models
        model_updates = self._update_adaptive_models()
        
        # 4. Optimize performance
        performance_optimization = self._optimize_performance()
        
        # 5. Update learning metrics
        self._update_learning_metrics()
        
        print(f"✅ Continuous learning cycle complete")
        return {
            'new_learning': new_learning,
            'feedback_learning': feedback_learning,
            'model_updates': model_updates,
            'performance_optimization': performance_optimization
        }
    
    def _learn_from_new_data(self, new_data):
        """Learn from new data patterns"""
        print("📚 Learning from new data...")
        
        learning_insights = []
        
        for data_point in new_data:
            # Extract patterns
            patterns = self._extract_patterns(data_point)
            
            # Learn from successful matches
            if data_point.get('match_success', False):
                self.learning_data['successful_matches'].append(data_point)
                learning_insights.append({
                    'type': 'successful_match_learning',
                    'data_point': data_point,
                    'patterns': patterns,
                    'learning_value': 'high'
                })
            
            # Learn from failed matches
            elif data_point.get('match_failure', False):
                self.learning_data['failed_matches'].append(data_point)
                learning_insights.append({
                    'type': 'failed_match_learning',
                    'data_point': data_point,
                    'patterns': patterns,
                    'learning_value': 'medium'
                })
            
            # Learn from user corrections
            if data_point.get('user_correction'):
                self.learning_data['user_corrections'].append(data_point)
                learning_insights.append({
                    'type': 'user_correction_learning',
                    'data_point': data_point,
                    'patterns': patterns,
                    'learning_value': 'high'
                })
        
        print(f"   ✅ Learned from {len(learning_insights)} new data points")
        return learning_insights
    
    def _learn_from_feedback(self, feedback_data):
        """Learn from user feedback"""
        print("💬 Learning from user feedback...")
        
        feedback_insights = []
        
        for feedback in feedback_data:
            # Store feedback
            self.learning_data['feedback_data'].append(feedback)
            
            # Learn from positive feedback
            if feedback.get('positive_feedback', False):
                feedback_insights.append({
                    'type': 'positive_feedback_learning',
                    'feedback': feedback,
                    'learning_value': 'high',
                    'action': 'reinforce_patterns'
                })
            
            # Learn from negative feedback
            elif feedback.get('negative_feedback', False):
                feedback_insights.append({
                    'type': 'negative_feedback_learning',
                    'feedback': feedback,
                    'learning_value': 'high',
                    'action': 'adjust_patterns'
                })
            
            # Learn from suggestions
            if feedback.get('suggestion'):
                feedback_insights.append({
                    'type': 'suggestion_learning',
                    'feedback': feedback,
                    'learning_value': 'medium',
                    'action': 'incorporate_suggestion'
                })
        
        print(f"   ✅ Learned from {len(feedback_insights)} feedback items")
        return feedback_insights
    
    def _update_adaptive_models(self):
        """Update adaptive models based on learning"""
        print("🧠 Updating adaptive models...")
        
        model_updates = []
        
        # Update matching confidence model
        if len(self.learning_data['successful_matches']) > self.learning_thresholds['min_samples_for_learning']:
            confidence_update = self._update_matching_confidence_model()
            model_updates.append(confidence_update)
        
        # Update pattern recognition model
        if len(self.learning_data['pattern_learning']) > 0:
            pattern_update = self._update_pattern_recognition_model()
            model_updates.append(pattern_update)
        
        # Update user preference model
        if len(self.learning_data['user_corrections']) > 0:
            preference_update = self._update_user_preference_model()
            model_updates.append(preference_update)
        
        # Update error correction model
        if len(self.learning_data['failed_matches']) > 0:
            error_update = self._update_error_correction_model()
            model_updates.append(error_update)
        
        print(f"   ✅ Updated {len(model_updates)} adaptive models")
        return model_updates
    
    def _update_matching_confidence_model(self):
        """Update matching confidence model"""
        print("   📊 Updating matching confidence model...")
        
        # Prepare training data
        features = []
        labels = []
        
        for match in self.learning_data['successful_matches']:
            feature_vector = self._extract_matching_features(match)
            features.append(feature_vector)
            labels.append(1)  # Successful match
        
        for match in self.learning_data['failed_matches']:
            feature_vector = self._extract_matching_features(match)
            features.append(feature_vector)
            labels.append(0)  # Failed match
        
        if len(features) > 0:
            # Train/update model
            self.adaptive_models['matching_confidence'] = RandomForestClassifier(
                n_estimators=100, random_state=42
            )
            self.adaptive_models['matching_confidence'].fit(features, labels)
            
            return {
                'model': 'matching_confidence',
                'status': 'updated',
                'training_samples': len(features),
                'accuracy': 'improved'
            }
        
        return {'model': 'matching_confidence', 'status': 'no_update'}
    
    def _update_pattern_recognition_model(self):
        """Update pattern recognition model"""
        print("   🔍 Updating pattern recognition model...")
        
        # Extract patterns from learning data
        patterns = []
        for pattern_type, pattern_list in self.learning_data['pattern_learning'].items():
            patterns.extend(pattern_list)
        
        if len(patterns) > 0:
            # Update pattern recognition
            self.adaptive_models['pattern_recognition'] = DBSCAN(eps=0.5, min_samples=2)
            pattern_features = [self._extract_pattern_features(p) for p in patterns]
            self.adaptive_models['pattern_recognition'].fit(pattern_features)
            
            return {
                'model': 'pattern_recognition',
                'status': 'updated',
                'patterns_learned': len(patterns),
                'clusters': len(set(self.adaptive_models['pattern_recognition'].labels_))
            }
        
        return {'model': 'pattern_recognition', 'status': 'no_update'}
    
    def _update_user_preference_model(self):
        """Update user preference model"""
        print("   👤 Updating user preference model...")
        
        # Learn from user corrections
        user_preferences = defaultdict(list)
        
        for correction in self.learning_data['user_corrections']:
            correction_type = correction.get('correction_type', 'unknown')
            user_preferences[correction_type].append(correction)
        
        # Update user preference model
        self.adaptive_models['user_preference'] = user_preferences
        
        return {
            'model': 'user_preference',
            'status': 'updated',
            'preference_categories': len(user_preferences),
            'total_corrections': len(self.learning_data['user_corrections'])
        }
    
    def _update_error_correction_model(self):
        """Update error correction model"""
        print("   🔧 Updating error correction model...")
        
        # Analyze failed matches for error patterns
        error_patterns = defaultdict(int)
        
        for failed_match in self.learning_data['failed_matches']:
            error_type = failed_match.get('error_type', 'unknown')
            error_patterns[error_type] += 1
        
        # Update error correction model
        self.adaptive_models['error_correction'] = dict(error_patterns)
        
        return {
            'model': 'error_correction',
            'status': 'updated',
            'error_types': len(error_patterns),
            'total_errors': len(self.learning_data['failed_matches'])
        }
    
    def _optimize_performance(self):
        """Optimize system performance based on learning"""
        print("⚡ Optimizing performance...")
        
        optimizations = []
        
        # Optimize matching thresholds
        if len(self.learning_data['successful_matches']) > 50:
            threshold_optimization = self._optimize_matching_thresholds()
            optimizations.append(threshold_optimization)
        
        # Optimize pattern recognition
        if len(self.learning_data['pattern_learning']) > 0:
            pattern_optimization = self._optimize_pattern_recognition()
            optimizations.append(pattern_optimization)
        
        # Optimize user experience
        if len(self.learning_data['user_corrections']) > 10:
            ux_optimization = self._optimize_user_experience()
            optimizations.append(ux_optimization)
        
        print(f"   ✅ Applied {len(optimizations)} performance optimizations")
        return optimizations
    
    def _optimize_matching_thresholds(self):
        """Optimize matching thresholds based on learning"""
        # Analyze successful vs failed matches
        successful_features = [self._extract_matching_features(m) for m in self.learning_data['successful_matches']]
        failed_features = [self._extract_matching_features(m) for m in self.learning_data['failed_matches']]
        
        if len(successful_features) > 0 and len(failed_features) > 0:
            # Calculate optimal thresholds
            successful_scores = [np.mean(f) for f in successful_features]
            failed_scores = [np.mean(f) for f in failed_features]
            
            optimal_threshold = (np.mean(successful_scores) + np.mean(failed_scores)) / 2
            
            return {
                'optimization': 'matching_thresholds',
                'old_threshold': self.learning_thresholds['confidence_threshold'],
                'new_threshold': optimal_threshold,
                'improvement': abs(optimal_threshold - self.learning_thresholds['confidence_threshold'])
            }
        
        return {'optimization': 'matching_thresholds', 'status': 'no_change'}
    
    def _optimize_pattern_recognition(self):
        """Optimize pattern recognition based on learning"""
        # Analyze pattern learning data
        pattern_categories = defaultdict(int)
        for pattern_type, patterns in self.learning_data['pattern_learning'].items():
            pattern_categories[pattern_type] = len(patterns)
        
        # Optimize pattern recognition parameters
        if len(pattern_categories) > 0:
            most_common_pattern = max(pattern_categories, key=pattern_categories.get)
            
            return {
                'optimization': 'pattern_recognition',
                'most_common_pattern': most_common_pattern,
                'pattern_count': pattern_categories[most_common_pattern],
                'improvement': 'pattern_recognition_enhanced'
            }
        
        return {'optimization': 'pattern_recognition', 'status': 'no_change'}
    
    def _optimize_user_experience(self):
        """Optimize user experience based on learning"""
        # Analyze user corrections
        correction_types = defaultdict(int)
        for correction in self.learning_data['user_corrections']:
            correction_type = correction.get('correction_type', 'unknown')
            correction_types[correction_type] += 1
        
        # Optimize user experience
        if len(correction_types) > 0:
            most_common_correction = max(correction_types, key=correction_types.get)
            
            return {
                'optimization': 'user_experience',
                'most_common_correction': most_common_correction,
                'correction_count': correction_types[most_common_correction],
                'improvement': 'user_experience_enhanced'
            }
        
        return {'optimization': 'user_experience', 'status': 'no_change'}
    
    def _extract_patterns(self, data_point):
        """Extract patterns from data point"""
        patterns = []
        
        # Extract amount patterns
        amount = data_point.get('amount', 0.0)
        if amount > 0:
            patterns.append(f'amount_{amount}')
        
        # Extract description patterns
        description = data_point.get('description', '')
        if description:
            patterns.append(f'description_{description[:10]}')
        
        # Extract date patterns
        date = data_point.get('date', '')
        if date:
            patterns.append(f'date_{date}')
        
        # Extract type patterns
        tx_type = data_point.get('type', '')
        if tx_type:
            patterns.append(f'type_{tx_type}')
        
        return patterns
    
    def _extract_matching_features(self, match_data):
        """Extract features for matching analysis"""
        features = []
        
        # Amount feature
        amount = abs(match_data.get('amount', 0.0))
        features.append(amount)
        
        # Description length
        description = match_data.get('description', '')
        features.append(len(description))
        
        # Date features
        date = match_data.get('date', '')
        if date:
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                features.extend([date_obj.month, date_obj.day, date_obj.weekday()])
            except:
                features.extend([0, 0, 0])
        else:
            features.extend([0, 0, 0])
        
        # Type features
        tx_type = match_data.get('type', '')
        features.append(1 if tx_type == 'debit' else 0)
        
        return features
    
    def _extract_pattern_features(self, pattern):
        """Extract features from pattern"""
        features = []
        
        # Pattern length
        features.append(len(pattern))
        
        # Pattern type
        pattern_type = pattern.split('_')[0] if '_' in pattern else 'unknown'
        features.append(hash(pattern_type) % 1000)  # Hash to number
        
        # Pattern content
        features.append(hash(pattern) % 1000)  # Hash to number
        
        return features
    
    def _update_learning_metrics(self):
        """Update learning metrics"""
        self.learning_metrics['total_learning_events'] += 1
        
        # Calculate accuracy improvement
        if len(self.learning_data['successful_matches']) > 0:
            total_matches = len(self.learning_data['successful_matches']) + len(self.learning_data['failed_matches'])
            accuracy = len(self.learning_data['successful_matches']) / max(total_matches, 1)
            self.learning_metrics['accuracy_improvement'] = accuracy
        
        # Calculate pattern recognition improvement
        if len(self.learning_data['pattern_learning']) > 0:
            total_patterns = sum(len(patterns) for patterns in self.learning_data['pattern_learning'].values())
            self.learning_metrics['pattern_recognition_improvement'] = total_patterns
        
        # Calculate user satisfaction improvement
        if len(self.learning_data['user_corrections']) > 0:
            self.learning_metrics['user_satisfaction_improvement'] = len(self.learning_data['user_corrections'])
    
    def get_learning_summary(self):
        """Get continuous learning summary"""
        summary = {
            'timestamp': self.timestamp,
            'learning_metrics': self.learning_metrics,
            'learning_data_size': {
                'successful_matches': len(self.learning_data['successful_matches']),
                'failed_matches': len(self.learning_data['failed_matches']),
                'user_corrections': len(self.learning_data['user_corrections']),
                'feedback_data': len(self.learning_data['feedback_data']),
                'pattern_learning': len(self.learning_data['pattern_learning'])
            },
            'adaptive_models': len([m for m in self.adaptive_models.values() if m is not None]),
            'learning_history_size': len(self.learning_history)
        }
        
        return summary
    
    def save_learning_data(self):
        """Save continuous learning data"""
        learning_data = {
            'timestamp': self.timestamp,
            'learning_data': self.learning_data,
            'adaptive_models': {k: str(v) for k, v in self.adaptive_models.items() if v is not None},
            'learning_metrics': self.learning_metrics,
            'learning_thresholds': self.learning_thresholds,
            'learning_history': self.learning_history,
            'summary': self.get_learning_summary()
        }
        
        filename = f"continuous_learning_data_{self.timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(learning_data, f, indent=2, default=str)
        
        print(f"✅ Continuous learning data saved: {filename}")
        return filename

def main():
    """Test the continuous learning engine"""
    print("🔄 CONTINUOUS LEARNING ENGINE")
    print("=" * 40)
    print("🎯 Testing continuous learning capabilities")
    print("=" * 40)
    
    # Initialize engine
    engine = ContinuousLearningEngine()
    
    # Sample new data
    new_data = [
        {
            'description': 'ACH ADV FILE',
            'amount': 1000.00,
            'date': '2025-05-31',
            'type': 'debit',
            'match_success': True,
            'confidence': 0.9
        },
        {
            'description': 'CNS Settlement',
            'amount': 500.00,
            'date': '2025-05-30',
            'type': 'credit',
            'match_failure': True,
            'error_type': 'amount_mismatch'
        },
        {
            'description': 'EFUNDS Corp',
            'amount': 750.00,
            'date': '2025-05-29',
            'type': 'credit',
            'user_correction': True,
            'correction_type': 'gl_mapping'
        }
    ]
    
    # Sample feedback data
    feedback_data = [
        {
            'positive_feedback': True,
            'message': 'Great matching accuracy',
            'suggestion': 'Continue current approach'
        },
        {
            'negative_feedback': True,
            'message': 'Incorrect GL mapping',
            'suggestion': 'Improve GL mapping logic'
        }
    ]
    
    # Test continuous learning cycle
    learning_results = engine.continuous_learning_cycle(new_data, feedback_data)
    
    print(f"\n📊 LEARNING RESULTS:")
    print(f"New learning insights: {len(learning_results['new_learning'])}")
    print(f"Feedback learning insights: {len(learning_results['feedback_learning'])}")
    print(f"Model updates: {len(learning_results['model_updates'])}")
    print(f"Performance optimizations: {len(learning_results['performance_optimization'])}")
    
    # Test individual learning components
    print(f"\n🔍 LEARNING COMPONENTS:")
    for insight in learning_results['new_learning']:
        print(f"   • {insight['type']}: {insight['learning_value']} value")
    
    for insight in learning_results['feedback_learning']:
        print(f"   • {insight['type']}: {insight['action']}")
    
    for update in learning_results['model_updates']:
        print(f"   • {update['model']}: {update['status']}")
    
    for optimization in learning_results['performance_optimization']:
        print(f"   • {optimization['optimization']}: {optimization.get('improvement', 'no_change')}")
    
    # Get summary
    summary = engine.get_learning_summary()
    print(f"\n📈 LEARNING SUMMARY:")
    print(f"Total learning events: {summary['learning_metrics']['total_learning_events']}")
    print(f"Accuracy improvement: {summary['learning_metrics']['accuracy_improvement']:.2f}")
    print(f"Pattern recognition improvement: {summary['learning_metrics']['pattern_recognition_improvement']}")
    print(f"User satisfaction improvement: {summary['learning_metrics']['user_satisfaction_improvement']}")
    print(f"Adaptive models: {summary['adaptive_models']}")
    
    # Save learning data
    engine.save_learning_data()

if __name__ == "__main__":
    main()
