import pandas as pd

class BMWAnalyzer:
    def __init__(self, df):
        self.df = df

    def get_yearly_sales(self):
        """Aggregates sales volume by year."""
        return self.df.groupby('Year')['Sales_Volume'].sum().sort_index()

    def get_regional_sales(self):
        """Aggregates sales volume by region."""
        return self.df.groupby('Region')['Sales_Volume'].sum().sort_values(ascending=False)

    def get_top_models(self, n=5):
        """Returns top n performing models."""
        return self.df.groupby('Model')['Sales_Volume'].sum().sort_values(ascending=False).head(n)

    def get_bottom_models(self, n=5):
        """Returns bottom n performing models."""
        return self.df.groupby('Model')['Sales_Volume'].sum().sort_values(ascending=True).head(n)

    def get_correlations(self):
        """Calculates correlation matrix for numerical features vs Sales_Volume."""
        numeric_cols = ['Engine_Size_L', 'Mileage_KM', 'Price_USD', 'Sales_Volume']
        # Filter only existing numeric columns to be safe
        cols_to_use = [col for col in numeric_cols if col in self.df.columns]
        return self.df[cols_to_use].corr()['Sales_Volume'].sort_values(ascending=False)
    
    def get_summary_stats(self):
        """Returns a dictionary of summary statistics for the LLM prompt."""
        yearly = self.get_yearly_sales()
        regional = self.get_regional_sales()
        top_models = self.get_top_models()
        correlations = self.get_correlations()
        
        return {
            "total_sales": int(self.df['Sales_Volume'].sum()),
            "yearly_trend": yearly.to_dict(),
            "top_region": regional.index[0],
            "top_region_sales": int(regional.iloc[0]),
            "top_models": top_models.to_dict(),
            "correlations": correlations.drop('Sales_Volume').to_dict() # Exclude self-correlation
        }
