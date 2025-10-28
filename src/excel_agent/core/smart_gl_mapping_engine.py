#!/usr/bin/env python3
"""
Smart GL Account Mapping Engine
Implements AI-powered GL account assignment and transaction classification
Based on AI thinking insights for intelligent GL mapping
"""

import json
import re
from datetime import datetime
from collections import defaultdict
import numpy as np

class SmartGLMappingEngine:
    def __init__(self):
        self.name = "SmartGLMappingEngine"
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # GL account mappings from AI insights
        self.gl_mappings = {
            "ACH ADV FILE": "74530",
            "CNS Settlement": "74505",
            "EFUNDS Corp": "74510",
            "RBC Activity": "74400",
            "PULSE FEES": "74505",
            "Image CL Presentment": "74520",
            "Image CL Deposit": "74560",
            "Return Image CL": "74525",
            "Cooperative Business": "74550",
            "ICUL ServCorp": "74535",
            "CRIF": "74540",
            "Cash Letter": "74515",
            "Wire Transfer": "74400",
            "VISA": "74400",
            "Analysis Service": "74400",
            "Interest": "74400"
        }
        
        # Enhanced pattern matching rules
        self.pattern_rules = {
            "ACH": {
                "keywords": ["ACH", "ADV FILE", "AUTOMATED CLEARING HOUSE"],
                "gl_account": "74530",
                "confidence": 0.9
            },
            "CNS": {
                "keywords": ["CNS", "ATM", "SETTLEMENT"],
                "gl_account": "74505",
                "confidence": 0.85
            },
            "EFUNDS": {
                "keywords": ["EFUNDS", "SHARED BRANCHING", "DAILY SETTLE"],
                "gl_account": "74510",
                "confidence": 0.8
            },
            "RBC": {
                "keywords": ["RBC", "VISA", "WIRE", "ANALYSIS"],
                "gl_account": "74400",
                "confidence": 0.75
            },
            "IMAGE": {
                "keywords": ["IMAGE", "CHECK", "PRESENTMENT", "DEPOSIT"],
                "gl_account": "74520",
                "confidence": 0.8
            },
            "COOPERATIVE": {
                "keywords": ["COOPERATIVE", "ICUL", "SERV CORP"],
                "gl_account": "74550",
                "confidence": 0.7
            },
            "CRIF": {
                "keywords": ["CRIF", "LOAN", "INDIRECT"],
                "gl_account": "74540",
                "confidence": 0.75
            },
            "CASH": {
                "keywords": ["CASH LETTER", "CHECK DEPOSIT"],
                "gl_account": "74515",
                "confidence": 0.8
            }
        }
        
        # Learning data
        self.mapping_history = []
        self.successful_mappings = []
        self.failed_mappings = []
        self.confidence_scores = defaultdict(list)
        
        # Performance metrics
        self.metrics = {
            "total_mappings": 0,
            "successful_mappings": 0,
            "failed_mappings": 0,
            "average_confidence": 0.0,
            "accuracy_rate": 0.0
        }
        
    def smart_map_transaction(self, transaction_description, transaction_amount=None, transaction_date=None):
        """Intelligently map transaction to GL account"""
        print(f"🧠 Smart mapping: {transaction_description}")
        
        # Clean and normalize description
        clean_desc = self._clean_description(transaction_description)
        
        # Apply multiple mapping strategies
        mappings = []
        
        # Strategy 1: Exact match
        exact_match = self._exact_match_mapping(clean_desc)
        if exact_match:
            mappings.append(exact_match)
        
        # Strategy 2: Pattern matching
        pattern_matches = self._pattern_match_mapping(clean_desc)
        mappings.extend(pattern_matches)
        
        # Strategy 3: Fuzzy matching
        fuzzy_matches = self._fuzzy_match_mapping(clean_desc)
        mappings.extend(fuzzy_matches)
        
        # Strategy 4: Machine learning prediction
        ml_matches = self._ml_prediction_mapping(clean_desc, transaction_amount, transaction_date)
        mappings.extend(ml_matches)
        
        # Sort by confidence score
        mappings.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Select best mapping
        best_mapping = mappings[0] if mappings else None
        
        if best_mapping:
            print(f"   ✅ Mapped to GL {best_mapping['gl_account']} (confidence: {best_mapping['confidence']:.2f})")
            self._record_mapping(transaction_description, best_mapping, True)
        else:
            print(f"   ❌ No mapping found")
            self._record_mapping(transaction_description, None, False)
        
        return best_mapping
    
    def _clean_description(self, description):
        """Clean and normalize transaction description"""
        if not description:
            return ""
        
        # Convert to uppercase
        clean = description.upper()
        
        # Remove special characters and extra spaces
        clean = re.sub(r'[^\w\s]', ' ', clean)
        clean = re.sub(r'\s+', ' ', clean)
        clean = clean.strip()
        
        return clean
    
    def _exact_match_mapping(self, description):
        """Exact match mapping strategy"""
        for pattern, gl_account in self.gl_mappings.items():
            if pattern.upper() in description:
                return {
                    'gl_account': gl_account,
                    'confidence': 1.0,
                    'strategy': 'exact_match',
                    'reason': f'Exact match for "{pattern}"',
                    'pattern_matched': pattern
                }
        return None
    
    def _pattern_match_mapping(self, description):
        """Pattern matching strategy"""
        matches = []
        
        for pattern_name, pattern_data in self.pattern_rules.items():
            keywords = pattern_data['keywords']
            gl_account = pattern_data['gl_account']
            base_confidence = pattern_data['confidence']
            
            # Count matching keywords
            matching_keywords = 0
            for keyword in keywords:
                if keyword in description:
                    matching_keywords += 1
            
            if matching_keywords > 0:
                # Calculate confidence based on keyword matches
                keyword_ratio = matching_keywords / len(keywords)
                confidence = base_confidence * keyword_ratio
                
                matches.append({
                    'gl_account': gl_account,
                    'confidence': confidence,
                    'strategy': 'pattern_match',
                    'reason': f'Pattern match for {pattern_name} ({matching_keywords}/{len(keywords)} keywords)',
                    'pattern_matched': pattern_name,
                    'matching_keywords': matching_keywords
                })
        
        return matches
    
    def _fuzzy_match_mapping(self, description):
        """Fuzzy matching strategy"""
        matches = []
        
        # Split description into words
        desc_words = set(description.split())
        
        for pattern_name, pattern_data in self.pattern_rules.items():
            keywords = pattern_data['keywords']
            gl_account = pattern_data['gl_account']
            
            # Calculate fuzzy similarity
            similarity_scores = []
            for keyword in keywords:
                max_similarity = 0
                for desc_word in desc_words:
                    similarity = self._calculate_word_similarity(keyword, desc_word)
                    max_similarity = max(max_similarity, similarity)
                similarity_scores.append(max_similarity)
            
            avg_similarity = np.mean(similarity_scores)
            
            if avg_similarity > 0.6:  # Threshold for fuzzy matching
                confidence = avg_similarity * 0.8  # Lower confidence for fuzzy matches
                matches.append({
                    'gl_account': gl_account,
                    'confidence': confidence,
                    'strategy': 'fuzzy_match',
                    'reason': f'Fuzzy match for {pattern_name} (similarity: {avg_similarity:.2f})',
                    'pattern_matched': pattern_name,
                    'similarity_score': avg_similarity
                })
        
        return matches
    
    def _ml_prediction_mapping(self, description, amount=None, date=None):
        """Machine learning prediction mapping"""
        matches = []
        
        # Simple ML-like prediction based on historical data
        if len(self.successful_mappings) > 0:
            # Analyze successful mappings for patterns
            successful_patterns = defaultdict(int)
            for mapping in self.successful_mappings:
                pattern = mapping.get('pattern_matched', '')
                if pattern:
                    successful_patterns[pattern] += 1
            
            # Find most successful pattern
            if successful_patterns:
                most_successful = max(successful_patterns, key=successful_patterns.get)
                pattern_data = self.pattern_rules.get(most_successful)
                
                if pattern_data:
                    # Check if description matches this successful pattern
                    keywords = pattern_data['keywords']
                    matching_keywords = sum(1 for keyword in keywords if keyword in description)
                    
                    if matching_keywords > 0:
                        confidence = 0.6 + (matching_keywords / len(keywords)) * 0.3
                        matches.append({
                            'gl_account': pattern_data['gl_account'],
                            'confidence': confidence,
                            'strategy': 'ml_prediction',
                            'reason': f'ML prediction based on successful pattern {most_successful}',
                            'pattern_matched': most_successful,
                            'historical_success': successful_patterns[most_successful]
                        })
        
        return matches
    
    def _calculate_word_similarity(self, word1, word2):
        """Calculate similarity between two words"""
        if not word1 or not word2:
            return 0.0
        
        # Simple character-based similarity
        common_chars = set(word1) & set(word2)
        total_chars = set(word1) | set(word2)
        
        if not total_chars:
            return 0.0
        
        return len(common_chars) / len(total_chars)
    
    def _record_mapping(self, description, mapping_result, was_successful):
        """Record mapping result for learning"""
        mapping_record = {
            'timestamp': self.timestamp,
            'description': description,
            'mapping_result': mapping_result,
            'was_successful': was_successful
        }
        
        self.mapping_history.append(mapping_record)
        
        if was_successful and mapping_result:
            self.successful_mappings.append(mapping_result)
        else:
            self.failed_mappings.append(mapping_record)
        
        # Update metrics
        self.metrics['total_mappings'] += 1
        if was_successful:
            self.metrics['successful_mappings'] += 1
        else:
            self.metrics['failed_mappings'] += 1
        
        self.metrics['accuracy_rate'] = self.metrics['successful_mappings'] / max(self.metrics['total_mappings'], 1)
        
        if mapping_result:
            self.confidence_scores[mapping_result['gl_account']].append(mapping_result['confidence'])
            self.metrics['average_confidence'] = np.mean([
                score for scores in self.confidence_scores.values() for score in scores
            ])
    
    def batch_map_transactions(self, transactions):
        """Map multiple transactions in batch"""
        print(f"🧠 BATCH MAPPING {len(transactions)} TRANSACTIONS")
        print("-" * 40)
        
        results = []
        for i, transaction in enumerate(transactions, 1):
            print(f"\n{i}. Mapping: {transaction.get('description', 'Unknown')}")
            
            mapping = self.smart_map_transaction(
                transaction.get('description', ''),
                transaction.get('amount'),
                transaction.get('date')
            )
            
            results.append({
                'transaction': transaction,
                'mapping': mapping
            })
        
        print(f"\n✅ Batch mapping complete: {len(results)} transactions processed")
        return results
    
    def get_mapping_statistics(self):
        """Get mapping statistics and insights"""
        stats = {
            'metrics': self.metrics,
            'total_mappings': len(self.mapping_history),
            'successful_mappings': len(self.successful_mappings),
            'failed_mappings': len(self.failed_mappings),
            'accuracy_rate': self.metrics['accuracy_rate'],
            'average_confidence': self.metrics['average_confidence'],
            'confidence_by_gl': dict(self.confidence_scores)
        }
        
        return stats
    
    def learn_from_feedback(self, description, correct_gl_account, feedback_confidence=1.0):
        """Learn from human feedback"""
        print(f"📚 Learning from feedback: {description} -> GL {correct_gl_account}")
        
        # Update pattern rules based on feedback
        for pattern_name, pattern_data in self.pattern_rules.items():
            if pattern_data['gl_account'] == correct_gl_account:
                # Increase confidence for this pattern
                pattern_data['confidence'] = min(1.0, pattern_data['confidence'] + 0.1)
        
        # Record successful learning
        learning_record = {
            'timestamp': self.timestamp,
            'description': description,
            'correct_gl_account': correct_gl_account,
            'feedback_confidence': feedback_confidence,
            'type': 'human_feedback'
        }
        
        self.successful_mappings.append(learning_record)
        print(f"   ✅ Updated pattern confidence for GL {correct_gl_account}")
    
    def save_mapping_data(self):
        """Save mapping data for future use"""
        mapping_data = {
            'timestamp': self.timestamp,
            'mapping_history': self.mapping_history,
            'successful_mappings': self.successful_mappings,
            'failed_mappings': self.failed_mappings,
            'metrics': self.metrics,
            'pattern_rules': self.pattern_rules,
            'confidence_scores': dict(self.confidence_scores)
        }
        
        filename = f"smart_gl_mapping_data_{self.timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(mapping_data, f, indent=2, default=str)
        
        print(f"✅ Mapping data saved: {filename}")
        return filename

def main():
    """Test the smart GL mapping engine"""
    print("🧠 SMART GL ACCOUNT MAPPING ENGINE")
    print("=" * 40)
    print("🎯 Testing intelligent GL mapping")
    print("=" * 40)
    
    # Initialize engine
    engine = SmartGLMappingEngine()
    
    # Sample transactions for testing
    test_transactions = [
        {
            'description': 'ACH ADV FILE - Rcvd DB',
            'amount': 1000.00,
            'date': '2025-05-31'
        },
        {
            'description': 'CNS Settlement',
            'amount': 500.00,
            'date': '2025-05-30'
        },
        {
            'description': 'EFUNDS Corp Daily Settlement',
            'amount': 750.00,
            'date': '2025-05-31'
        },
        {
            'description': 'Image CL Presentment',
            'amount': 2000.00,
            'date': '2025-05-29'
        },
        {
            'description': 'Unknown Transaction Type',
            'amount': 100.00,
            'date': '2025-05-31'
        }
    ]
    
    # Test individual mapping
    print("\n🔍 INDIVIDUAL MAPPING TESTS:")
    for transaction in test_transactions[:3]:
        mapping = engine.smart_map_transaction(
            transaction['description'],
            transaction['amount'],
            transaction['date']
        )
        if mapping:
            print(f"   Result: GL {mapping['gl_account']} (confidence: {mapping['confidence']:.2f})")
    
    # Test batch mapping
    print(f"\n🔄 BATCH MAPPING TEST:")
    batch_results = engine.batch_map_transactions(test_transactions)
    
    # Test learning from feedback
    print(f"\n📚 LEARNING FROM FEEDBACK:")
    engine.learn_from_feedback("Unknown Transaction Type", "74400", 0.8)
    
    # Get statistics
    stats = engine.get_mapping_statistics()
    print(f"\n📊 MAPPING STATISTICS:")
    print(f"Total mappings: {stats['total_mappings']}")
    print(f"Successful mappings: {stats['successful_mappings']}")
    print(f"Accuracy rate: {stats['accuracy_rate']:.2%}")
    print(f"Average confidence: {stats['average_confidence']:.2f}")
    
    # Save mapping data
    engine.save_mapping_data()

if __name__ == "__main__":
    main()
