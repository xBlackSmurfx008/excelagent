
# OP Manual integration template
from training_data_manager import TrainingDataManager

class OPManualIntegration:
    """Integration of OP manual data into agents."""
    
    def __init__(self, training_data_manager: TrainingDataManager):
        self.tdm = training_data_manager
        self.op_manual = self.tdm.get_training_data("op_manual")
    
    def get_gl_account_info(self, gl_account: str) -> Dict[str, Any]:
        """Get GL account information from OP manual."""
        return self.op_manual.get("gl_accounts", {}).get(gl_account, {})
    
    def get_matching_keywords(self, gl_account: str) -> List[str]:
        """Get matching keywords for GL account."""
        account_info = self.get_gl_account_info(gl_account)
        return account_info.get("matching_keywords", [])
    
    def get_variance_threshold(self, gl_account: str) -> float:
        """Get variance threshold for GL account."""
        account_info = self.get_gl_account_info(gl_account)
        return account_info.get("variance_threshold", 1000.0)
