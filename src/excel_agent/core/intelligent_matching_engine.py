#!/usr/bin/env python3
"""
Intelligent Matching Engine
Implements fuzzy matching, pattern recognition, and confidence scoring
Based on AI thinking insights for enhanced transaction matching
"""

import re
import json
from difflib import SequenceMatcher
from datetime import datetime
from collections import defaultdict
import numpy as np

class IntelligentMatchingEngine:
    def __init__(self):
        self.name = "IntelligentMatchingEngine"
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Matching thresholds
        self.exact_match_threshold = 0.95
        self.fuzzy_match_threshold = 0.8
        self.pattern_match_threshold = 0.7
        
        # Pattern recognition rules
        self.transaction_patterns = {
            "ACH": ["ACH ADV FILE", "ACH CREDIT", "ACH DEBIT"],
            "CNS": ["CNS Settlement", "ATM Settlement"],
            "EFUNDS": ["EFUNDS Corp", "Shared Branching"],
            "RBC": ["RBC Activity", "VISA", "Wire Transfer"],
            "IMAGE": ["Image CL Presentment", "Image CL Deposit", "Return Image CL"],
            "COOPERATIVE": ["Cooperative Business", "ICUL ServCorp"],
            "CRIF": ["CRIF", "CRIF Loans"],
            "CASH": ["Cash Letter", "Check Deposits"]
        }
        
        # Confidence scoring weights
        self.weights = {
            "description_similarity": 0.4,
            "amount_match": 0.3,
            "date_proximity": 0.2,
            "pattern_match": 0.1
        }
        
        # Learning data
        self.successful_matches = []
        self.failed_matches = []
        self.learning_patterns = defaultdict(list)
        
    def intelligent_match(self, bank_transaction, gl_transactions):
        """Perform intelligent matching using multiple strategies"""
        print(f"🔍 Intelligent matching for: {bank_transaction.get('description', 'Unknown')}")
        
        matches = []
        
        # Strategy 1: Exact Match
        exact_matches = self._exact_match(bank_transaction, gl_transactions)
        matches.extend(exact_matches)
        
        # Strategy 2: Fuzzy Match
        fuzzy_matches = self._fuzzy_match(bank_transaction, gl_transactions)
        matches.extend(fuzzy_matches)
        
        # Strategy 3: Pattern Match
        pattern_matches = self._pattern_match(bank_transaction, gl_transactions)
        matches.extend(pattern_matches)
        
        # Strategy 4: Historical Match
        historical_matches = self._historical_match(bank_transaction, gl_transactions)
        matches.extend(historical_matches)
        
        # Sort by confidence score
        matches.sort(key=lambda x: x['confidence'], reverse=True)
        
        print(f"   ✅ Found {len(matches)} potential matches")
        return matches
    
    def _exact_match(self, bank_tx, gl_transactions):
        """Exact matching strategy"""
        matches = []
        
        for gl_tx in gl_transactions:
            # Check exact amount match
            amount_match = abs(bank_tx.get('amount', 0) - gl_tx.get('amount', 0)) < 0.01
            
            # Check exact description match
            desc_match = self._calculate_similarity(
                bank_tx.get('description', ''), 
                gl_tx.get('description', '')
            ) >= self.exact_match_threshold
            
            if amount_match and desc_match:
                matches.append({
                    'type': 'exact_match',
                    'bank_transaction': bank_tx,
                    'gl_transaction': gl_tx,
                    'confidence': 1.0,
                    'strategy': 'exact_match',
                    'reason': 'Exact amount and description match'
                })
        
        return matches
    
    def _fuzzy_match(self, bank_tx, gl_transactions):
        """Fuzzy matching strategy"""
        matches = []
        
        for gl_tx in gl_transactions:
            # Calculate description similarity
            desc_similarity = self._calculate_similarity(
                bank_tx.get('description', ''), 
                gl_tx.get('description', '')
            )
            
            # Calculate amount similarity
            amount_diff = abs(bank_tx.get('amount', 0) - gl_tx.get('amount', 0))
            amount_similarity = max(0, 1 - (amount_diff / max(bank_tx.get('amount', 1), gl_tx.get('amount', 1))))
            
            # Calculate date proximity
            date_similarity = self._calculate_date_similarity(
                bank_tx.get('date', ''), 
                gl_tx.get('date', '')
            )
            
            # Calculate pattern match
            pattern_similarity = self._calculate_pattern_similarity(
                bank_tx.get('description', ''), 
                gl_tx.get('description', '')
            )
            
            # Calculate overall confidence
            confidence = (
                desc_similarity * self.weights['description_similarity'] +
                amount_similarity * self.weights['amount_match'] +
                date_similarity * self.weights['date_proximity'] +
                pattern_similarity * self.weights['pattern_match']
            )
            
            if confidence >= self.fuzzy_match_threshold:
                matches.append({
                    'type': 'fuzzy_match',
                    'bank_transaction': bank_tx,
                    'gl_transaction': gl_tx,
                    'confidence': confidence,
                    'strategy': 'fuzzy_match',
                    'reason': f'Fuzzy match with {confidence:.2f} confidence',
                    'details': {
                        'description_similarity': desc_similarity,
                        'amount_similarity': amount_similarity,
                        'date_similarity': date_similarity,
                        'pattern_similarity': pattern_similarity
                    }
                })
        
        return matches
    
    def _pattern_match(self, bank_tx, gl_transactions):
        """Pattern matching strategy"""
        matches = []
        
        bank_desc = bank_tx.get('description', '').upper()
        
        for gl_tx in gl_transactions:
            gl_desc = gl_tx.get('description', '').upper()
            
            # Check for pattern matches
            pattern_score = 0
            matched_patterns = []
            
            for pattern_name, patterns in self.transaction_patterns.items():
                for pattern in patterns:
                    if pattern.upper() in bank_desc and pattern.upper() in gl_desc:
                        pattern_score += 0.3
                        matched_patterns.append(pattern_name)
            
            # Check for amount similarity
            amount_similarity = max(0, 1 - abs(bank_tx.get('amount', 0) - gl_tx.get('amount', 0)) / max(bank_tx.get('amount', 1), gl_tx.get('amount', 1)))
            
            confidence = (pattern_score + amount_similarity) / 2
            
            if confidence >= self.pattern_match_threshold:
                matches.append({
                    'type': 'pattern_match',
                    'bank_transaction': bank_tx,
                    'gl_transaction': gl_tx,
                    'confidence': confidence,
                    'strategy': 'pattern_match',
                    'reason': f'Pattern match with {confidence:.2f} confidence',
                    'matched_patterns': matched_patterns
                })
        
        return matches
    
    def _historical_match(self, bank_tx, gl_transactions):
        """Historical matching strategy using learning data"""
        matches = []
        
        # Use learning patterns from successful matches
        bank_desc = bank_tx.get('description', '').upper()
        
        for gl_tx in gl_transactions:
            gl_desc = gl_tx.get('description', '').upper()
            
            # Check against learned patterns
            historical_score = 0
            for pattern in self.learning_patterns.get('successful_patterns', []):
                if pattern in bank_desc and pattern in gl_desc:
                    historical_score += 0.5
            
            # Check amount similarity
            amount_similarity = max(0, 1 - abs(bank_tx.get('amount', 0) - gl_tx.get('amount', 0)) / max(bank_tx.get('amount', 1), gl_tx.get('amount', 1)))
            
            confidence = (historical_score + amount_similarity) / 2
            
            if confidence >= self.pattern_match_threshold:
                matches.append({
                    'type': 'historical_match',
                    'bank_transaction': bank_tx,
                    'gl_transaction': gl_tx,
                    'confidence': confidence,
                    'strategy': 'historical_match',
                    'reason': f'Historical match with {confidence:.2f} confidence'
                })
        
        return matches
    
    def _calculate_similarity(self, desc1, desc2):
        """Calculate similarity between two descriptions"""
        if not desc1 or not desc2:
            return 0.0
        
        # Clean descriptions
        desc1_clean = re.sub(r'[^\w\s]', '', desc1.upper())
        desc2_clean = re.sub(r'[^\w\s]', '', desc2.upper())
        
        # Calculate sequence similarity
        similarity = SequenceMatcher(None, desc1_clean, desc2_clean).ratio()
        
        return similarity
    
    def _calculate_date_similarity(self, date1, date2):
        """Calculate date proximity similarity"""
        if not date1 or not date2:
            return 0.0
        
        try:
            # Simple date comparison (can be enhanced)
            if date1 == date2:
                return 1.0
            else:
                return 0.5  # Partial similarity for different dates
        except:
            return 0.0
    
    def _calculate_pattern_similarity(self, desc1, desc2):
        """Calculate pattern similarity"""
        desc1_upper = desc1.upper()
        desc2_upper = desc2.upper()
        
        pattern_score = 0
        total_patterns = 0
        
        for pattern_name, patterns in self.transaction_patterns.items():
            for pattern in patterns:
                total_patterns += 1
                if pattern.upper() in desc1_upper and pattern.upper() in desc2_upper:
                    pattern_score += 1
        
        return pattern_score / max(total_patterns, 1)
    
    def learn_from_match(self, match_result, was_successful):
        """Learn from matching results"""
        if was_successful:
            self.successful_matches.append(match_result)
            # Extract patterns for learning
            bank_desc = match_result.get('bank_transaction', {}).get('description', '')
            gl_desc = match_result.get('gl_transaction', {}).get('description', '')
            
            # Learn common words and patterns
            common_words = set(bank_desc.upper().split()) & set(gl_desc.upper().split())
            for word in common_words:
                if len(word) > 3:  # Only learn meaningful words
                    self.learning_patterns['successful_patterns'].append(word)
        else:
            self.failed_matches.append(match_result)
    
    def get_matching_statistics(self):
        """Get matching statistics"""
        total_attempts = len(self.successful_matches) + len(self.failed_matches)
        success_rate = len(self.successful_matches) / max(total_attempts, 1)
        
        return {
            'total_attempts': total_attempts,
            'successful_matches': len(self.successful_matches),
            'failed_matches': len(self.failed_matches),
            'success_rate': success_rate,
            'learned_patterns': len(self.learning_patterns['successful_patterns'])
        }
    
    def save_learning_data(self):
        """Save learning data for future use"""
        learning_data = {
            'timestamp': self.timestamp,
            'successful_matches': self.successful_matches,
            'failed_matches': self.failed_matches,
            'learning_patterns': dict(self.learning_patterns),
            'statistics': self.get_matching_statistics()
        }
        
        filename = f"intelligent_matching_learning_{self.timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(learning_data, f, indent=2, default=str)
        
        print(f"✅ Learning data saved: {filename}")
        return filename

def main():
    """Test the intelligent matching engine"""
    print("🧠 INTELLIGENT MATCHING ENGINE")
    print("=" * 40)
    print("🎯 Testing fuzzy matching and pattern recognition")
    print("=" * 40)
    
    # Initialize engine
    engine = IntelligentMatchingEngine()
    
    # Sample data for testing
    bank_transaction = {
        'description': 'ACH ADV FILE - Rcvd DB',
        'amount': 1000.00,
        'date': '2025-05-31',
        'type': 'debit'
    }
    
    gl_transactions = [
        {
            'description': 'ACH ADV FILE - Received Debit',
            'amount': 1000.00,
            'date': '2025-05-31',
            'type': 'debit',
            'gl_account': '74530'
        },
        {
            'description': 'CNS Settlement',
            'amount': 500.00,
            'date': '2025-05-30',
            'type': 'credit',
            'gl_account': '74505'
        },
        {
            'description': 'EFUNDS Corp Daily Settlement',
            'amount': 750.00,
            'date': '2025-05-31',
            'type': 'credit',
            'gl_account': '74510'
        }
    ]
    
    # Test intelligent matching
    matches = engine.intelligent_match(bank_transaction, gl_transactions)
    
    print(f"\n📊 MATCHING RESULTS:")
    print(f"Found {len(matches)} potential matches")
    
    for i, match in enumerate(matches, 1):
        print(f"\n{i}. {match['type'].upper()} - Confidence: {match['confidence']:.2f}")
        print(f"   Bank: {match['bank_transaction']['description']}")
        print(f"   GL: {match['gl_transaction']['description']}")
        print(f"   Reason: {match['reason']}")
    
    # Test learning
    if matches:
        engine.learn_from_match(matches[0], True)
        print(f"\n✅ Learned from successful match")
    
    # Get statistics
    stats = engine.get_matching_statistics()
    print(f"\n📈 MATCHING STATISTICS:")
    print(f"Total attempts: {stats['total_attempts']}")
    print(f"Success rate: {stats['success_rate']:.2%}")
    print(f"Learned patterns: {stats['learned_patterns']}")
    
    # Save learning data
    engine.save_learning_data()

if __name__ == "__main__":
    main()
