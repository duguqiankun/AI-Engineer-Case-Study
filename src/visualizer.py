import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd

class BMWVisualizer:
    def __init__(self, df, output_dir='output/images'):
        self.df = df
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Set style
        sns.set_theme(style="whitegrid")

    def plot_yearly_trend(self):
        plt.figure(figsize=(10, 6))
        yearly_sales = self.df.groupby('Year')['Sales_Volume'].sum().reset_index()
        sns.lineplot(data=yearly_sales, x='Year', y='Sales_Volume', marker='o')
        plt.title('BMW Global Sales Trend (2020-2024)')
        plt.ylabel('Total Sales Volume')
        plt.tight_layout()
        path = os.path.join(self.output_dir, 'yearly_trend.png')
        plt.savefig(path)
        plt.close()
        return path

    def plot_regional_sales(self):
        plt.figure(figsize=(12, 6))
        regional_sales = self.df.groupby('Region')['Sales_Volume'].sum().sort_values(ascending=False).reset_index()
        sns.barplot(data=regional_sales, x='Sales_Volume', y='Region', palette='viridis')
        plt.title('Total Sales by Region')
        plt.xlabel('Sales Volume')
        plt.tight_layout()
        path = os.path.join(self.output_dir, 'regional_sales.png')
        plt.savefig(path)
        plt.close()
        return path

    def plot_top_models(self):
        plt.figure(figsize=(12, 6))
        top_models = self.df.groupby('Model')['Sales_Volume'].sum().sort_values(ascending=False).head(10).reset_index()
        sns.barplot(data=top_models, x='Sales_Volume', y='Model', palette='magma')
        plt.title('Top 10 Performing Models')
        plt.xlabel('Sales Volume')
        plt.tight_layout()
        path = os.path.join(self.output_dir, 'top_models.png')
        plt.savefig(path)
        plt.close()
        return path
    
    def plot_price_vs_sales(self):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=self.df, x='Price_USD', y='Sales_Volume', alpha=0.5)
        plt.title('Price vs Sales Volume')
        plt.xlabel('Price (USD)')
        plt.ylabel('Sales Volume')
        plt.tight_layout()
        path = os.path.join(self.output_dir, 'price_vs_sales.png')
        plt.savefig(path)
        plt.close()
        return path

    def generate_all_plots(self):
        paths = {}
        paths['yearly_trend'] = self.plot_yearly_trend()
        paths['regional_sales'] = self.plot_regional_sales()
        paths['top_models'] = self.plot_top_models()
        paths['price_vs_sales'] = self.plot_price_vs_sales()
        return paths
