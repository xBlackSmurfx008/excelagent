#!/usr/bin/env python3
"""
Enhanced NCB GL Reconciliation Agent with Detailed Audit Trail

This agent provides comprehensive matching reports and audit trails showing
exactly what matched with what, including detailed transaction-level analysis.
"""

import pandas as pd
from pathlib import Path
import os
from datetime import datetime
import json
from difflib import SequenceMatcher
import re

class DetailedAuditReconciliationAgent:
    """
    Enhanced reconciliation agent with comprehensive audit trail and detailed reporting.
    """
    
    def __init__(self):
        self.name = "DetailedAuditReconciliationAgent"
        self.target_match_rate = 80.0
        self.current_match_rate = 0.0
        self.matching_strategies = [
            {"name": "exact_amount", "tolerance": 0.01, "weight": 1.0},
            {"name": "amount_date", "amount_tol": 0.01, "date_tol": 3, "weight": 0.9},
            {"name": "description_similarity", "threshold": 0.6, "weight": 0.8},
            {"name": "partial_amount", "tolerance_pct": 0.05, "min_amount": 1000, "weight": 0.7},
            {"name": "pattern_matching", "patterns": ["ACH", "CHECK", "WIRE", "DEPOSIT", "FEE"], "weight": 0.6}
        ]
        
        # Audit trail storage
        self.audit_trail = []
        self.detailed_matches = []
        self.unmatched_analysis = []
        self.strategy_performance = {}
    
    def load_gl_activity(self, gl_file):
        """Load and consolidate GL activity from all sheets with detailed tracking"""
        print(f"📊 Loading GL Activity from all sheets...")
        
        gl_data = pd.read_excel(gl_file, sheet_name=None)
        consolidated_data = []
        
        for sheet_name, df in gl_data.items():
            if sheet_name.startswith('74'):  # GL account sheets
                # Calculate net amount
                df['Net_Amount'] = (
                    pd.to_numeric(df['Debit'], errors='coerce').fillna(0) + 
                    pd.to_numeric(df['Credit'], errors='coerce').fillna(0)
                )
                
                # Add GL account
                df['GL_Account'] = int(sheet_name)
                df['GL_Sheet'] = sheet_name
                
                # Enhance description for matching
                if 'Description' in df.columns:
                    df['Enhanced_Description'] = df['Description'].fillna('').astype(str).str.upper()
                
                # Add transaction type
                df['Transaction_Type'] = df['Description'].fillna('').astype(str).apply(self._identify_transaction_type)
                
                # Add unique transaction ID
                df['GL_Transaction_ID'] = df.index.astype(str) + '_' + sheet_name
                
                consolidated_data.append(df)
                
                net_total = df['Net_Amount'].sum()
                print(f"   ✅ GL {sheet_name}: {len(df)} transactions, Net: ${net_total:,.2f}")
        
        if consolidated_data:
            result = pd.concat(consolidated_data, ignore_index=True)
            print(f"   📊 Total GL transactions: {len(result)}")
            return result
        return pd.DataFrame()
    
    def _identify_transaction_type(self, description):
        """Identify transaction type from description"""
        desc_upper = description.upper()
        
        if re.search(r'ACH|ACH_ADV|ACH_FILE', desc_upper):
            return 'ACH'
        elif re.search(r'CHECK|CHK|DRAFT', desc_upper):
            return 'CHECK'
        elif re.search(r'WIRE|WIR', desc_upper):
            return 'WIRE'
        elif re.search(r'DEP|DEPOSIT', desc_upper):
            return 'DEPOSIT'
        elif re.search(r'FEE|CHARGE|SERVICE', desc_upper):
            return 'FEE'
        else:
            return 'OTHER'
    
    def load_bank_statement(self, bank_file):
        """Load bank statement data with detailed tracking"""
        print(f"📊 Loading NCB Bank Statement...")
        
        bank_df = pd.read_excel(bank_file)
        
        # Calculate net amount
        bank_df['Net_Amount'] = (
            pd.to_numeric(bank_df['Credit'], errors='coerce').fillna(0) + 
            pd.to_numeric(bank_df['Debit'], errors='coerce').fillna(0)
        )
        
        # Enhance description for matching
        if 'Description' in bank_df.columns:
            bank_df['Enhanced_Description'] = bank_df['Description'].fillna('').astype(str).str.upper()
        
        # Add transaction type
        bank_df['Transaction_Type'] = bank_df['Description'].fillna('').astype(str).apply(self._identify_transaction_type)
        
        # Add unique transaction ID
        bank_df['Bank_Transaction_ID'] = bank_df.index.astype(str) + '_BANK'
        
        # Get date range
        if 'Post Date' in bank_df.columns:
            bank_df['Post Date'] = pd.to_datetime(bank_df['Post Date'], errors='coerce')
            start_date = bank_df['Post Date'].min().strftime('%Y-%m-%d')
            end_date = bank_df['Post Date'].max().strftime('%Y-%m-%d')
            print(f"   📅 Date range: {start_date} to {end_date}")
        
        total_amount = bank_df['Net_Amount'].sum()
        print(f"   💰 Total net amount: ${total_amount:,.2f}")
        print(f"   📊 NCB Statement: {len(bank_df)} transactions")
        
        return bank_df
    
    def iterative_match_transactions(self, gl_data, bank_data):
        """Iteratively match transactions with detailed audit trail"""
        print(f"\n🔄 Starting iterative matching to achieve {self.target_match_rate}% match rate...")
        
        matches = []
        unmatched_gl = gl_data.copy()
        unmatched_bank = bank_data.copy()
        
        iteration = 0
        max_iterations = 5
        
        # Initialize strategy performance tracking
        for strategy in self.matching_strategies:
            self.strategy_performance[strategy['name']] = {
                'matches_found': 0,
                'execution_time': 0,
                'success_rate': 0
            }
        
        while (self.current_match_rate < self.target_match_rate and 
               iteration < max_iterations and 
               len(unmatched_gl) > 0 and len(unmatched_bank) > 0):
            
            iteration += 1
            print(f"\n🧠 Iteration {iteration}: Attempting to improve match rate...")
            
            iteration_start_time = datetime.now()
            
            # Strategy 1: Exact amount matching
            exact_matches = self._exact_amount_match_with_audit(unmatched_gl, unmatched_bank)
            if exact_matches:
                matches.extend(exact_matches)
                unmatched_gl, unmatched_bank = self._remove_matched_transactions(
                    unmatched_gl, unmatched_bank, exact_matches
                )
                self.strategy_performance['exact_amount']['matches_found'] += len(exact_matches)
                print(f"   ✅ Exact amount: Found {len(exact_matches)} matches")
            
            # Strategy 2: Amount + Date matching
            amount_date_matches = self._amount_date_match_with_audit(unmatched_gl, unmatched_bank)
            if amount_date_matches:
                matches.extend(amount_date_matches)
                unmatched_gl, unmatched_bank = self._remove_matched_transactions(
                    unmatched_gl, unmatched_bank, amount_date_matches
                )
                self.strategy_performance['amount_date']['matches_found'] += len(amount_date_matches)
                print(f"   ✅ Amount+Date: Found {len(amount_date_matches)} matches")
            
            # Strategy 3: Description similarity
            desc_matches = self._description_similarity_match_with_audit(unmatched_gl, unmatched_bank)
            if desc_matches:
                matches.extend(desc_matches)
                unmatched_gl, unmatched_bank = self._remove_matched_transactions(
                    unmatched_gl, unmatched_bank, desc_matches
                )
                self.strategy_performance['description_similarity']['matches_found'] += len(desc_matches)
                print(f"   ✅ Description similarity: Found {len(desc_matches)} matches")
            
            # Strategy 4: Partial amount matching
            partial_matches = self._partial_amount_match_with_audit(unmatched_gl, unmatched_bank)
            if partial_matches:
                matches.extend(partial_matches)
                unmatched_gl, unmatched_bank = self._remove_matched_transactions(
                    unmatched_gl, unmatched_bank, partial_matches
                )
                self.strategy_performance['partial_amount']['matches_found'] += len(partial_matches)
                print(f"   ✅ Partial amount: Found {len(partial_matches)} matches")
            
            # Strategy 5: Pattern matching
            pattern_matches = self._pattern_matching_with_audit(unmatched_gl, unmatched_bank)
            if pattern_matches:
                matches.extend(pattern_matches)
                unmatched_gl, unmatched_bank = self._remove_matched_transactions(
                    unmatched_gl, unmatched_bank, pattern_matches
                )
                self.strategy_performance['pattern_matching']['matches_found'] += len(pattern_matches)
                print(f"   ✅ Pattern matching: Found {len(pattern_matches)} matches")
            
            # Calculate current match rate
            total_gl_transactions = len(gl_data)
            matched_count = len(matches)
            self.current_match_rate = (matched_count / total_gl_transactions) * 100
            
            iteration_end_time = datetime.now()
            iteration_duration = (iteration_end_time - iteration_start_time).total_seconds()
            
            print(f"   📊 Current match rate: {self.current_match_rate:.1f}% ({matched_count}/{total_gl_transactions})")
            print(f"   ⏱️ Iteration duration: {iteration_duration:.2f} seconds")
            
            # Record audit trail for this iteration
            self.audit_trail.append({
                'iteration': iteration,
                'timestamp': iteration_start_time.isoformat(),
                'duration_seconds': iteration_duration,
                'matches_found': len(matches) - (len(matches) - sum(len(m) for m in [exact_matches, amount_date_matches, desc_matches, partial_matches, pattern_matches])),
                'match_rate': self.current_match_rate,
                'unmatched_gl_count': len(unmatched_gl),
                'unmatched_bank_count': len(unmatched_bank),
                'strategy_results': {
                    'exact_amount': len(exact_matches),
                    'amount_date': len(amount_date_matches),
                    'description_similarity': len(desc_matches),
                    'partial_amount': len(partial_matches),
                    'pattern_matching': len(pattern_matches)
                }
            })
            
            # Break if no new matches found
            if len(matches) == 0:
                print(f"   ⚠️ No new matches found in iteration {iteration}")
                break
        
        # Store detailed matches for audit trail
        self.detailed_matches = matches
        
        print(f"\n✅ Iterative matching completed:")
        print(f"   🎯 Target: {self.target_match_rate}%")
        print(f"   📊 Achieved: {self.current_match_rate:.1f}%")
        print(f"   ✅ Matches: {len(matches)}")
        print(f"   ❌ Unmatched GL: {len(unmatched_gl)}")
        print(f"   ❌ Unmatched Bank: {len(unmatched_bank)}")
        print(f"   🔄 Iterations: {iteration}")
        
        return matches, unmatched_gl.to_dict('records'), unmatched_bank.to_dict('records')
    
    def _exact_amount_match_with_audit(self, gl_data, bank_data):
        """Exact amount matching with detailed audit trail"""
        matches = []
        tolerance = 0.01
        
        for gl_idx, gl_row in gl_data.iterrows():
            gl_amount = gl_row['Net_Amount']
            
            for bank_idx, bank_row in bank_data.iterrows():
                bank_amount = bank_row['Net_Amount']
                
                if abs(gl_amount - bank_amount) <= tolerance:
                    match_detail = {
                        'gl_transaction': gl_row.to_dict(),
                        'bank_transaction': bank_row.to_dict(),
                        'match_type': 'exact_amount',
                        'gl_index': gl_idx,
                        'bank_index': bank_idx,
                        'amount_difference': abs(gl_amount - bank_amount),
                        'match_confidence': 1.0,
                        'matching_criteria': {
                            'amount_tolerance': tolerance,
                            'gl_amount': gl_amount,
                            'bank_amount': bank_amount,
                            'amount_match': True
                        },
                        'audit_trail': {
                            'strategy': 'exact_amount',
                            'timestamp': datetime.now().isoformat(),
                            'match_reason': f'Amounts match within ${tolerance} tolerance',
                            'gl_description': str(gl_row.get('Description', '')),
                            'bank_description': str(bank_row.get('Description', ''))
                        }
                    }
                    matches.append(match_detail)
                    break
        
        return matches
    
    def _amount_date_match_with_audit(self, gl_data, bank_data):
        """Amount + date proximity matching with detailed audit trail"""
        matches = []
        amount_tolerance = 0.01
        date_tolerance_days = 3
        
        for gl_idx, gl_row in gl_data.iterrows():
            gl_amount = gl_row['Net_Amount']
            gl_date = gl_row.get('Effective Date') or gl_row.get('Actual Date')
            
            if pd.isna(gl_date):
                continue
            
            for bank_idx, bank_row in bank_data.iterrows():
                bank_amount = bank_row['Net_Amount']
                bank_date = bank_row.get('Post Date')
                
                if pd.isna(bank_date):
                    continue
                
                # Check amount match
                amount_diff = abs(gl_amount - bank_amount)
                if amount_diff <= amount_tolerance:
                    # Check date match
                    date_diff = abs((gl_date - bank_date).days)
                    if date_diff <= date_tolerance_days:
                        # Calculate combined score
                        amount_score = 1 - (amount_diff / max(abs(gl_amount), abs(bank_amount), 1))
                        date_score = 1 - (date_diff / date_tolerance_days)
                        combined_score = (amount_score + date_score) / 2
                        
                        match_detail = {
                            'gl_transaction': gl_row.to_dict(),
                            'bank_transaction': bank_row.to_dict(),
                            'match_type': 'amount_date',
                            'gl_index': gl_idx,
                            'bank_index': bank_idx,
                            'amount_difference': amount_diff,
                            'date_difference_days': date_diff,
                            'match_confidence': combined_score,
                            'matching_criteria': {
                                'amount_tolerance': amount_tolerance,
                                'date_tolerance_days': date_tolerance_days,
                                'gl_amount': gl_amount,
                                'bank_amount': bank_amount,
                                'gl_date': gl_date.isoformat() if pd.notna(gl_date) else None,
                                'bank_date': bank_date.isoformat() if pd.notna(bank_date) else None,
                                'amount_match': True,
                                'date_match': True
                            },
                            'audit_trail': {
                                'strategy': 'amount_date',
                                'timestamp': datetime.now().isoformat(),
                                'match_reason': f'Amounts match within ${amount_tolerance} and dates within {date_tolerance_days} days',
                                'gl_description': str(gl_row.get('Description', '')),
                                'bank_description': str(bank_row.get('Description', ''))
                            }
                        }
                        matches.append(match_detail)
                        break
        
        return matches
    
    def _description_similarity_match_with_audit(self, gl_data, bank_data):
        """Description similarity matching with detailed audit trail"""
        matches = []
        similarity_threshold = 0.6
        
        for gl_idx, gl_row in gl_data.iterrows():
            gl_desc = str(gl_row.get('Description', '')).lower()
            gl_amount = gl_row['Net_Amount']
            
            if not gl_desc or gl_amount == 0:
                continue
            
            for bank_idx, bank_row in bank_data.iterrows():
                bank_desc = str(bank_row.get('Description', '')).lower()
                bank_amount = bank_row['Net_Amount']
                
                if not bank_desc:
                    continue
                
                # Calculate description similarity
                desc_similarity = SequenceMatcher(None, gl_desc, bank_desc).ratio()
                
                # Check if amounts are close (within 10%)
                amount_diff = abs(gl_amount - bank_amount)
                amount_tolerance = max(abs(gl_amount), abs(bank_amount)) * 0.1
                
                if amount_diff <= amount_tolerance and desc_similarity > similarity_threshold:
                    # Calculate combined score
                    amount_score = 1 - (amount_diff / amount_tolerance)
                    combined_score = (desc_similarity + amount_score) / 2
                    
                    match_detail = {
                        'gl_transaction': gl_row.to_dict(),
                        'bank_transaction': bank_row.to_dict(),
                        'match_type': 'description_similarity',
                        'gl_index': gl_idx,
                        'bank_index': bank_idx,
                        'description_similarity': desc_similarity,
                        'amount_difference': amount_diff,
                        'match_confidence': combined_score,
                        'matching_criteria': {
                            'similarity_threshold': similarity_threshold,
                            'amount_tolerance_percentage': 0.1,
                            'gl_description': gl_desc,
                            'bank_description': bank_desc,
                            'gl_amount': gl_amount,
                            'bank_amount': bank_amount,
                            'description_match': True,
                            'amount_match': True
                        },
                        'audit_trail': {
                            'strategy': 'description_similarity',
                            'timestamp': datetime.now().isoformat(),
                            'match_reason': f'Description similarity {desc_similarity:.2f} > {similarity_threshold} and amounts within 10%',
                            'gl_description': str(gl_row.get('Description', '')),
                            'bank_description': str(bank_row.get('Description', ''))
                        }
                    }
                    matches.append(match_detail)
                    break
        
        return matches
    
    def _partial_amount_match_with_audit(self, gl_data, bank_data):
        """Partial amount matching for large transactions with detailed audit trail"""
        matches = []
        tolerance_percentage = 0.05  # 5% tolerance
        min_amount = 1000  # Only for transactions > $1000
        
        for gl_idx, gl_row in gl_data.iterrows():
            gl_amount = gl_row['Net_Amount']
            
            # Only apply to large transactions
            if abs(gl_amount) < min_amount:
                continue
            
            for bank_idx, bank_row in bank_data.iterrows():
                bank_amount = bank_row['Net_Amount']
                
                # Check if amounts are within percentage tolerance
                amount_diff = abs(gl_amount - bank_amount)
                tolerance_amount = abs(gl_amount) * tolerance_percentage
                
                if amount_diff <= tolerance_amount:
                    # Calculate match score based on amount difference
                    match_score = 1 - (amount_diff / tolerance_amount)
                    
                    match_detail = {
                        'gl_transaction': gl_row.to_dict(),
                        'bank_transaction': bank_row.to_dict(),
                        'match_type': 'partial_amount',
                        'gl_index': gl_idx,
                        'bank_index': bank_idx,
                        'amount_difference': amount_diff,
                        'tolerance_percentage': tolerance_percentage,
                        'match_confidence': match_score,
                        'matching_criteria': {
                            'tolerance_percentage': tolerance_percentage,
                            'min_amount': min_amount,
                            'gl_amount': gl_amount,
                            'bank_amount': bank_amount,
                            'tolerance_amount': tolerance_amount,
                            'amount_match': True
                        },
                        'audit_trail': {
                            'strategy': 'partial_amount',
                            'timestamp': datetime.now().isoformat(),
                            'match_reason': f'Large transaction amounts within {tolerance_percentage*100}% tolerance',
                            'gl_description': str(gl_row.get('Description', '')),
                            'bank_description': str(bank_row.get('Description', ''))
                        }
                    }
                    matches.append(match_detail)
                    break
        
        return matches
    
    def _pattern_matching_with_audit(self, gl_data, bank_data):
        """Pattern-based matching for common transaction types with detailed audit trail"""
        matches = []
        
        for gl_idx, gl_row in gl_data.iterrows():
            gl_amount = gl_row['Net_Amount']
            gl_type = gl_row.get('Transaction_Type', 'OTHER')
            
            for bank_idx, bank_row in bank_data.iterrows():
                bank_amount = bank_row['Net_Amount']
                bank_type = bank_row.get('Transaction_Type', 'OTHER')
                
                # Check if transaction types match
                if gl_type == bank_type and gl_type != 'OTHER':
                    # Check if amounts are close (within 20% for pattern matching)
                    amount_diff = abs(gl_amount - bank_amount)
                    amount_tolerance = max(abs(gl_amount), abs(bank_amount)) * 0.2
                    
                    if amount_diff <= amount_tolerance:
                        # Calculate pattern match score
                        pattern_score = 0.8  # Base score for type match
                        amount_score = 1 - (amount_diff / amount_tolerance)
                        combined_score = (pattern_score + amount_score) / 2
                        
                        match_detail = {
                            'gl_transaction': gl_row.to_dict(),
                            'bank_transaction': bank_row.to_dict(),
                            'match_type': 'pattern_matching',
                            'gl_index': gl_idx,
                            'bank_index': bank_idx,
                            'transaction_type': gl_type,
                            'amount_difference': amount_diff,
                            'match_confidence': combined_score,
                            'matching_criteria': {
                                'transaction_type': gl_type,
                                'amount_tolerance_percentage': 0.2,
                                'gl_amount': gl_amount,
                                'bank_amount': bank_amount,
                                'type_match': True,
                                'amount_match': True
                            },
                            'audit_trail': {
                                'strategy': 'pattern_matching',
                                'timestamp': datetime.now().isoformat(),
                                'match_reason': f'Transaction type {gl_type} matches and amounts within 20% tolerance',
                                'gl_description': str(gl_row.get('Description', '')),
                                'bank_description': str(bank_row.get('Description', ''))
                            }
                        }
                        matches.append(match_detail)
                        break
        
        return matches
    
    def _remove_matched_transactions(self, gl_data, bank_data, matches):
        """Remove matched transactions from unmatched lists"""
        matched_gl_indices = [m['gl_index'] for m in matches]
        matched_bank_indices = [m['bank_index'] for m in matches]
        
        unmatched_gl = gl_data.drop(matched_gl_indices)
        unmatched_bank = bank_data.drop(matched_bank_indices)
        
        return unmatched_gl, unmatched_bank
    
    def generate_detailed_audit_report(self, gl_data, bank_data, matches, unmatched_gl, unmatched_bank):
        """Generate comprehensive audit report with transaction-level details"""
        print(f"\n📄 Generating detailed audit report...")
        
        # Calculate reconciliation summary
        gl_balance = gl_data['Net_Amount'].sum()
        bank_total = bank_data['Net_Amount'].sum()
        variance = gl_balance - bank_total
        variance_percentage = (variance / abs(gl_balance)) * 100 if gl_balance != 0 else 0
        
        # Analyze match strategies
        strategy_analysis = {}
        for match in matches:
            match_type = match['match_type']
            if match_type not in strategy_analysis:
                strategy_analysis[match_type] = {
                    'count': 0,
                    'total_amount': 0,
                    'avg_confidence': 0,
                    'confidence_scores': []
                }
            strategy_analysis[match_type]['count'] += 1
            strategy_analysis[match_type]['total_amount'] += match['gl_transaction']['Net_Amount']
            strategy_analysis[match_type]['confidence_scores'].append(match['match_confidence'])
        
        # Calculate average confidence for each strategy
        for strategy in strategy_analysis:
            scores = strategy_analysis[strategy]['confidence_scores']
            strategy_analysis[strategy]['avg_confidence'] = sum(scores) / len(scores) if scores else 0
        
        # Generate detailed match report
        detailed_match_report = []
        for i, match in enumerate(matches, 1):
            match_detail = {
                'match_number': i,
                'match_type': match['match_type'],
                'match_confidence': match['match_confidence'],
                'gl_transaction': {
                    'id': match['gl_transaction']['GL_Transaction_ID'],
                    'gl_account': match['gl_transaction']['GL_Account'],
                    'description': match['gl_transaction']['Description'],
                    'amount': match['gl_transaction']['Net_Amount'],
                    'date': match['gl_transaction'].get('Effective Date', ''),
                    'transaction_type': match['gl_transaction']['Transaction_Type']
                },
                'bank_transaction': {
                    'id': match['bank_transaction']['Bank_Transaction_ID'],
                    'description': match['bank_transaction']['Description'],
                    'amount': match['bank_transaction']['Net_Amount'],
                    'date': match['bank_transaction'].get('Post Date', ''),
                    'transaction_type': match['bank_transaction']['Transaction_Type']
                },
                'matching_criteria': match['matching_criteria'],
                'audit_trail': match['audit_trail']
            }
            detailed_match_report.append(match_detail)
        
        # Generate unmatched analysis
        unmatched_gl_analysis = []
        for i, transaction in enumerate(unmatched_gl, 1):
            unmatched_detail = {
                'transaction_number': i,
                'id': transaction['GL_Transaction_ID'],
                'gl_account': transaction['GL_Account'],
                'description': transaction['Description'],
                'amount': transaction['Net_Amount'],
                'date': transaction.get('Effective Date', ''),
                'transaction_type': transaction['Transaction_Type'],
                'analysis': {
                    'amount_range': 'Large' if abs(transaction['Net_Amount']) > 1000 else 'Small',
                    'has_description': bool(str(transaction.get('Description', '')).strip()),
                    'transaction_type': transaction['Transaction_Type']
                }
            }
            unmatched_gl_analysis.append(unmatched_detail)
        
        unmatched_bank_analysis = []
        for i, transaction in enumerate(unmatched_bank, 1):
            unmatched_detail = {
                'transaction_number': i,
                'id': transaction['Bank_Transaction_ID'],
                'description': transaction['Description'],
                'amount': transaction['Net_Amount'],
                'date': transaction.get('Post Date', ''),
                'transaction_type': transaction['Transaction_Type'],
                'analysis': {
                    'amount_range': 'Large' if abs(transaction['Net_Amount']) > 1000 else 'Small',
                    'has_description': bool(str(transaction.get('Description', '')).strip()),
                    'transaction_type': transaction['Transaction_Type']
                }
            }
            unmatched_bank_analysis.append(unmatched_detail)
        
        # Compile comprehensive report
        comprehensive_report = {
            'report_metadata': {
                'generated_at': datetime.now().isoformat(),
                'agent_name': self.name,
                'target_match_rate': self.target_match_rate,
                'achieved_match_rate': self.current_match_rate,
                'total_gl_transactions': len(gl_data),
                'total_bank_transactions': len(bank_data),
                'total_matches': len(matches),
                'unmatched_gl_count': len(unmatched_gl),
                'unmatched_bank_count': len(unmatched_bank)
            },
            'reconciliation_summary': {
                'gl_balance': gl_balance,
                'bank_total': bank_total,
                'variance': variance,
                'variance_percentage': variance_percentage,
                'is_balanced': abs(variance) < 1000
            },
            'strategy_performance': self.strategy_performance,
            'strategy_analysis': strategy_analysis,
            'audit_trail': self.audit_trail,
            'detailed_matches': detailed_match_report,
            'unmatched_gl_analysis': unmatched_gl_analysis,
            'unmatched_bank_analysis': unmatched_bank_analysis,
            'recommendations': self._generate_recommendations(strategy_analysis, unmatched_gl_analysis, unmatched_bank_analysis)
        }
        
        return comprehensive_report
    
    def _generate_recommendations(self, strategy_analysis, unmatched_gl, unmatched_bank):
        """Generate recommendations based on analysis"""
        recommendations = []
        
        # Strategy performance recommendations
        if strategy_analysis.get('exact_amount', {}).get('count', 0) > 0:
            recommendations.append({
                'type': 'strategy_performance',
                'priority': 'high',
                'recommendation': f"Exact amount matching found {strategy_analysis['exact_amount']['count']} matches - continue using this strategy",
                'action': 'Maintain exact amount matching with current tolerance'
            })
        
        if strategy_analysis.get('description_similarity', {}).get('count', 0) == 0:
            recommendations.append({
                'type': 'strategy_improvement',
                'priority': 'medium',
                'recommendation': 'Description similarity matching found no matches - consider adjusting similarity threshold',
                'action': 'Lower similarity threshold from 0.6 to 0.4 or implement fuzzy matching'
            })
        
        # Unmatched transaction recommendations
        large_unmatched_gl = [t for t in unmatched_gl if abs(t['amount']) > 1000]
        if large_unmatched_gl:
            recommendations.append({
                'type': 'unmatched_analysis',
                'priority': 'high',
                'recommendation': f"Found {len(large_unmatched_gl)} large unmatched GL transactions - investigate manually",
                'action': 'Review large unmatched transactions for potential aggregation or timing differences'
            })
        
        return recommendations
    
    def run_detailed_reconciliation(self, gl_file, bank_file):
        """Run detailed reconciliation with comprehensive audit trail"""
        print("🤖 Excel Agent - Detailed Audit NCB Statement vs GL Activity Reconciliation")
        print("=" * 80)
        print(f"🎯 Target Match Rate: {self.target_match_rate}%")
        print(f"📋 Audit Trail: Comprehensive transaction-level matching details")
        print()
        
        # Load data
        gl_data = self.load_gl_activity(gl_file)
        if gl_data.empty:
            return {"status": "error", "message": "No GL data found"}
        
        bank_data = self.load_bank_statement(bank_file)
        if bank_data.empty:
            return {"status": "error", "message": "No bank data found"}
        
        print()
        
        # Perform iterative matching
        matches, unmatched_gl, unmatched_bank = self.iterative_match_transactions(gl_data, bank_data)
        
        print()
        
        # Generate detailed audit report
        comprehensive_report = self.generate_detailed_audit_report(gl_data, bank_data, matches, unmatched_gl, unmatched_bank)
        
        # Save comprehensive report
        reports_dir = Path("data/reports")
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Save JSON report
        json_report_filename = f"detailed_audit_reconciliation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        json_report_path = reports_dir / json_report_filename
        
        with open(json_report_path, 'w') as f:
            json.dump(comprehensive_report, f, indent=4, default=str)
        
        # Save CSV match report
        csv_report_filename = f"detailed_matches_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        csv_report_path = reports_dir / csv_report_filename
        
        match_df = pd.DataFrame([
            {
                'Match_Number': match['match_number'],
                'Match_Type': match['match_type'],
                'Match_Confidence': match['match_confidence'],
                'GL_ID': match['gl_transaction']['id'],
                'GL_Account': match['gl_transaction']['gl_account'],
                'GL_Description': match['gl_transaction']['description'],
                'GL_Amount': match['gl_transaction']['amount'],
                'GL_Date': match['gl_transaction']['date'],
                'GL_Type': match['gl_transaction']['transaction_type'],
                'Bank_ID': match['bank_transaction']['id'],
                'Bank_Description': match['bank_transaction']['description'],
                'Bank_Amount': match['bank_transaction']['amount'],
                'Bank_Date': match['bank_transaction']['date'],
                'Bank_Type': match['bank_transaction']['transaction_type'],
                'Match_Reason': match['audit_trail']['match_reason']
            }
            for match in comprehensive_report['detailed_matches']
        ])
        
        match_df.to_csv(csv_report_path, index=False)
        
        print(f"\n📄 Detailed audit reports saved!")
        print(f"📁 JSON Report: {json_report_path}")
        print(f"📁 CSV Report: {csv_report_path}")
        
        # Display summary
        recon_summary = comprehensive_report['reconciliation_summary']
        
        print("\n📋 DETAILED AUDIT RECONCILIATION SUMMARY:")
        print("=" * 50)
        print(f"Status: {'✅ BALANCED' if recon_summary['is_balanced'] else '❌ IMBALANCED'}")
        print(f"GL Balance: ${recon_summary['gl_balance']:,.2f}")
        print(f"Bank Total: ${recon_summary['bank_total']:,.2f}")
        print(f"Variance: ${recon_summary['variance']:,.2f} ({recon_summary['variance_percentage']:.2f}%)")
        print(f"Match Rate: {comprehensive_report['report_metadata']['achieved_match_rate']:.1f}% (Target: {self.target_match_rate}%)")
        print(f"Matches Found: {comprehensive_report['report_metadata']['total_matches']}")
        print(f"Unmatched GL: {comprehensive_report['report_metadata']['unmatched_gl_count']}")
        print(f"Unmatched Bank: {comprehensive_report['report_metadata']['unmatched_bank_count']}")
        
        print(f"\n🎯 Strategy Analysis:")
        for strategy, analysis in comprehensive_report['strategy_analysis'].items():
            print(f"   {strategy}: {analysis['count']} matches, Avg Confidence: {analysis['avg_confidence']:.2f}")
        
        print(f"\n💡 Recommendations:")
        for rec in comprehensive_report['recommendations']:
            print(f"   {rec['priority'].upper()}: {rec['recommendation']}")
        
        print(f"\n🎉 Detailed audit reconciliation completed!")
        
        return comprehensive_report

def main():
    """Main function to run detailed reconciliation with audit trail"""
    print("🚀 Running Detailed Audit NCB GL Reconciliation Agent...")
    
    # Find files
    upload_dir = Path("uploads")
    gl_file = None
    bank_file = None
    
    for f in upload_dir.iterdir():
        if "Flex GL Activity" in f.name and f.suffix in ['.xlsx', '.xls']:
            gl_file = f
        if "NCB Bank Activity" in f.name and f.suffix in ['.xlsx', '.xls']:
            bank_file = f
    
    if not gl_file:
        print("❌ GL Activity file not found")
        return
    
    if not bank_file:
        print("❌ Bank Statement file not found")
        return
    
    print(f"📁 GL Activity File: {gl_file}")
    print(f"📁 Bank Statement File: {bank_file}")
    print("\n✅ Both files found!\n")
    
    # Run detailed reconciliation
    agent = DetailedAuditReconciliationAgent()
    result = agent.run_detailed_reconciliation(gl_file, bank_file)
    
    if result.get('report_metadata', {}).get('achieved_match_rate', 0) >= agent.target_match_rate:
        print(f"\n🎯 SUCCESS: Target match rate of {agent.target_match_rate}% achieved!")
    else:
        print(f"\n⚠️ PARTIAL SUCCESS: Achieved {agent.current_match_rate:.1f}% match rate (Target: {agent.target_match_rate}%)")

if __name__ == "__main__":
    main()
