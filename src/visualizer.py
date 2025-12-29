import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class BMWVisualizer:
    def __init__(self, df):
        self.df = df

    def get_plotly_html(self, fig):
        """Converts a plotly figure to an HTML div string."""
        return fig.to_html(full_html=False, include_plotlyjs=False)

    def plot_yearly_trend(self):
        yearly_sales = self.df.groupby('Year')['Sales_Volume'].sum().reset_index()
        fig = px.line(yearly_sales, x='Year', y='Sales_Volume', 
                      title='Global Sales Trend (2020-2024)',
                      markers=True)
        fig.update_layout(xaxis_title='Year', yaxis_title='Sales Volume')
        return self.get_plotly_html(fig)

    def plot_regional_sales(self):
        regional_sales = self.df.groupby('Region')['Sales_Volume'].sum().sort_values(ascending=False).reset_index()
        fig = px.bar(regional_sales, x='Sales_Volume', y='Region', 
                     title='Total Sales by Region',
                     orientation='h', 
                     color='Sales_Volume',
                     color_continuous_scale='Viridis')
        fig.update_layout(xaxis_title='Sales Volume', yaxis_title='Region', yaxis={'categoryorder':'total ascending'})
        return self.get_plotly_html(fig)

    def plot_top_models(self):
        top_models = self.df.groupby('Model')['Sales_Volume'].sum().sort_values(ascending=False).head(10).reset_index()
        fig = px.bar(top_models, x='Sales_Volume', y='Model', 
                     title='Top 10 Performing Models',
                     orientation='h',
                     color='Sales_Volume',
                     color_continuous_scale='Magma')
        fig.update_layout(xaxis_title='Sales Volume', yaxis_title='Model', yaxis={'categoryorder':'total ascending'})
        return self.get_plotly_html(fig)
    
    def plot_price_vs_sales(self):
        # Sampling for performance if data is huge, but 16k rows is fine for plotly
        fig = px.scatter(self.df, x='Price_USD', y='Sales_Volume', 
                         color='Fuel_Type',
                         title='Price vs Sales Volume Correlation',
                         opacity=0.6)
        fig.update_layout(xaxis_title='Price (USD)', yaxis_title='Sales Volume')
        return self.get_plotly_html(fig)

    def plot_fuel_trend(self):
        fuel_trend = self.df.pivot_table(index='Year', columns='Fuel_Type', values='Sales_Volume', aggfunc='sum').fillna(0).reset_index()
        # Melt for plotly express
        fuel_melt = fuel_trend.melt(id_vars='Year', var_name='Fuel Type', value_name='Sales Volume')
        fig = px.area(fuel_melt, x='Year', y='Sales Volume', color='Fuel Type',
                      title='Evolution of Fuel Type Preferences')
        return self.get_plotly_html(fig)

    def plot_transmission(self):
        trans_sales = self.df.groupby('Transmission')['Sales_Volume'].sum().reset_index()
        fig = px.pie(trans_sales, values='Sales_Volume', names='Transmission', 
                     title='Transmission Distribution',
                     hole=0.4)
        return self.get_plotly_html(fig)

    def plot_price_segments(self):
        bins = [0, 40000, 70000, 100000, float('inf')]
        labels = ['Budget (<40k)', 'Mid-Range (40k-70k)', 'Premium (70k-100k)', 'Luxury (>100k)']
        df_copy = self.df.copy()
        df_copy['Price_Segment'] = pd.cut(df_copy['Price_USD'], bins=bins, labels=labels)
        segment_sales = df_copy.groupby('Price_Segment')['Sales_Volume'].sum().reset_index()
        
        fig = px.bar(segment_sales, x='Price_Segment', y='Sales_Volume',
                     title='Sales Volume by Price Segment',
                     color='Sales_Volume',
                     color_continuous_scale='Blues')
        return self.get_plotly_html(fig)

    def plot_color_sales(self):
        color_sales = self.df.groupby('Color')['Sales_Volume'].sum().sort_values(ascending=False).head(10).reset_index()
        fig = px.bar(color_sales, x='Color', y='Sales_Volume',
                     title='Sales Volume by Color',
                     color='Sales_Volume',
                     color_continuous_scale='Turbo')
        return self.get_plotly_html(fig)

    def generate_all_plots(self):
        plots = {}
        plots['yearly_trend'] = self.plot_yearly_trend()
        plots['regional_sales'] = self.plot_regional_sales()
        plots['top_models'] = self.plot_top_models()
        plots['price_vs_sales'] = self.plot_price_vs_sales()
        plots['fuel_trend'] = self.plot_fuel_trend()
        plots['transmission'] = self.plot_transmission()
        plots['price_segments'] = self.plot_price_segments()
        plots['color_sales'] = self.plot_color_sales()
        return plots
