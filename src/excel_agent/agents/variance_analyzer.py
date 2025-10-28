import pandas as pd
import logging
from datetime import datetime
from typing import Tuple

# Set up logging
logging.basicConfig(filename='variance_analyzer.log', level=logging.INFO)

class VarianceAnalyzer:
    def __init__(self, gl_file: str, threshold: float):
        self.gl_file = gl_file
        self.threshold = threshold
        self.gl_data = None
        self.reconciled_data = None

    def load_gl_data(self):
        try:
            self.gl_data = pd.read_excel(self.gl_file)
            logging.info(f'GL data loaded successfully from {self.gl_file}')
        except Exception as e:
            logging.error(f'Error loading GL data: {e}')
            raise

    def daily_reconciliation(self):
        try:
            self.reconciled_data = self.gl_data.groupby(['Branch', 'Date']).sum()
            logging.info('Daily reconciliation completed successfully')
        except Exception as e:
            logging.error(f'Error during daily reconciliation: {e}')
            raise

    def month_end_balance(self):
        try:
            self.gl_data['MonthEndBalance'] = self.gl_data['Balance'].shift(-1)
            logging.info('Month-end balance calculated successfully')
        except Exception as e:
            logging.error(f'Error calculating month-end balance: {e}')
            raise

    def transaction_reconciliation(self):
        try:
            self.gl_data['Reconciled'] = self.gl_data['Debit'] - self.gl_data['Credit']
            logging.info('Transaction reconciliation completed successfully')
        except Exception as e:
            logging.error(f'Error during transaction reconciliation: {e}')
            raise

    def variance_analysis(self):
        try:
            self.gl_data['Variance'] = self.gl_data['Reconciled'] - self.gl_data['MonthEndBalance']
            self.gl_data['VarianceFlag'] = self.gl_data['Variance'].apply(lambda x: 1 if abs(x) > self.threshold else 0)
            logging.info('Variance analysis completed successfully')
        except Exception as e:
            logging.error(f'Error during variance analysis: {e}')
            raise

    def data_validation(self):
        try:
            assert self.gl_data.isnull().sum().sum() == 0, 'Missing data detected'
            logging.info('Data validation completed successfully')
        except Exception as e:
            logging.error(f'Error during data validation: {e}')
            raise

    def run(self):
        self.load_gl_data()
        self.data_validation()
        self.daily_reconciliation()
        self.month_end_balance()
        self.transaction_reconciliation()
        self.variance_analysis()

if __name__ == '__main__':
    analyzer = VarianceAnalyzer('gl_data.xlsx', 0.01)
    analyzer.run()