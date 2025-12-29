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
    
    def get_fuel_type_trends(self):
        """Aggregates sales volume by Year and Fuel_Type."""
        return self.df.pivot_table(index='Year', columns='Fuel_Type', values='Sales_Volume', aggfunc='sum').fillna(0)

    def get_transmission_sales(self):
        """Aggregates sales volume by Transmission."""
        return self.df.groupby('Transmission')['Sales_Volume'].sum().sort_values(ascending=False)

    def get_correlations(self):
        """Calculates correlation matrix for numerical features vs Sales_Volume."""
        numeric_cols = ['Engine_Size_L', 'Mileage_KM', 'Price_USD', 'Sales_Volume']
        # Filter only existing numeric columns to be safe
        cols_to_use = [col for col in numeric_cols if col in self.df.columns]
        return self.df[cols_to_use].corr()['Sales_Volume'].sort_values(ascending=False)

    def get_price_segments(self):
        """Bins Price_USD into segments and aggregates sales."""
        bins = [0, 40000, 70000, 100000, float('inf')]
        labels = ['Budget (<40k)', 'Mid-Range (40k-70k)', 'Premium (70k-100k)', 'Luxury (>100k)']
        
        # Avoid SettingWithCopyWarning
        df_copy = self.df.copy()
        df_copy['Price_Segment'] = pd.cut(df_copy['Price_USD'], bins=bins, labels=labels)
        return df_copy.groupby('Price_Segment')['Sales_Volume'].sum()

    def get_color_sales(self):
        """Aggregates sales by Color."""
        return self.df.groupby('Color')['Sales_Volume'].sum().sort_values(ascending=False)
    
    def get_summary_stats(self):
        """Returns a dictionary of summary statistics for the LLM prompt."""
        yearly = self.get_yearly_sales()
        regional = self.get_regional_sales()
        top_models = self.get_top_models()
        fuel_trends = self.get_fuel_type_trends()
        transmission = self.get_transmission_sales()
        correlations = self.get_correlations()
        price_segments = self.get_price_segments()
        color_sales = self.get_color_sales()
        
        return {
            "total_sales": int(self.df['Sales_Volume'].sum()),
            "yearly_trend": yearly.to_dict(),
            "top_region": regional.index[0],
            "top_region_sales": int(regional.iloc[0]),
            "top_models": top_models.to_dict(),
            "fuel_trends": fuel_trends.to_dict(),
            "transmission_split": transmission.to_dict(),
            "price_segments": price_segments.to_dict(),
            "color_sales": color_sales.head(5).to_dict(),
            "correlations": correlations.drop('Sales_Volume').to_dict() # Exclude self-correlation
        }
