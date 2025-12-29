import pandas as pd
import os

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        """Loads the BMW sales data from the Excel file."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found at {self.file_path}")
        
        try:
            df = pd.read_excel(self.file_path)
            # Basic validation
            required_columns = ['Model', 'Year', 'Region', 'Price_USD', 'Sales_Volume']
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"Missing one or more required columns: {required_columns}")
            
            return df
        except Exception as e:
            raise Exception(f"Error loading data: {e}")
