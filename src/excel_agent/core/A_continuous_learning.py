
# Continuous learning template
from training_data_manager import TrainingDataManager
from typing import Dict, Any
from datetime import datetime

class ContinuousLearning:
    """Continuous learning for agents."""
    
    def __init__(self, training_data_manager: TrainingDataManager):
        self.tdm = training_data_manager
        self.learning_history = []
    
    def update_learning(self, execution_result: Dict[str, Any]):
        """Update learning based on execution result."""
        learning_entry = {
            "timestamp": datetime.now().isoformat(),
            "result": execution_result,
            "success_rate": self._calculate_success_rate(execution_result),
            "variance_level": self._calculate_variance_level(execution_result)
        }
        
        self.tdm.add_learning_entry(learning_entry)
        self.learning_history.append(learning_entry)
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """Get learning insights."""
        return self.tdm.get_learning_insights()
