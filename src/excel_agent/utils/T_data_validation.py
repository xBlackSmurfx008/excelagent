
# Data validation template
from typing import Dict, List, Any, Tuple
import pandas as pd

class DataValidator:
    """Comprehensive data validation for agents."""
    
    def __init__(self, validation_rules: Dict[str, Any]):
        self.validation_rules = validation_rules
    
    def validate_gl_data(self, gl_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate GL data."""
        errors = []
        
        # Validate required fields
        required_fields = self.validation_rules.get("required_fields", [])
        for field in required_fields:
            if field not in gl_data:
                errors.append(f"Missing required field: {field}")
        
        # Validate data types
        # Add specific validation logic
        
        return len(errors) == 0, errors
    
    def validate_bank_data(self, bank_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate bank data."""
        errors = []
        
        # Add bank data validation logic
        
        return len(errors) == 0, errors
