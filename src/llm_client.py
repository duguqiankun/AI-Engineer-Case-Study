import os
import google.generativeai as genai
from dotenv import load_dotenv

class LLMClient:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def generate_report_content(self, summary_stats):
        """
        Generates a narrative report based on the provided summary statistics.
        """
        prompt = self._construct_prompt(summary_stats)
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return "Error: Could not generate AI report content. Please check API key and quota."

    def _construct_prompt(self, stats):
        return f"""
        You are a senior data analyst at BMW. Write a comprehensive executive report based on the following sales data analysis.
        
        ### Data Summary:
        - **Total Sales Volume**: {stats['total_sales']}
        - **Yearly Trend**: {stats['yearly_trend']}
        - **Top Performing Region**: {stats['top_region']} with {stats['top_region_sales']} sales
        - **Top 5 Models**: {stats['top_models']}
        - **Fuel Type Trends**: {stats['fuel_trends']}
        - **Transmission Split**: {stats['transmission_split']}
        - **Price Segments (Volume by Range)**: {stats['price_segments']}
        - **Color Preferences**: {stats['color_sales']}
        - **Correlations**: {stats['correlations']}

        ### Requirements:
        1. **Executive Summary**: Brief overview of the key findings.
        2. **Sales Trends**: Analyze the performance over the years.
        3. **Regional & Model Performance**: Highlight top markets and models.
        4. **Mobility Trends (Fuel & Transmission)**: Analyze the shift in fuel preferences (e.g., EV/Hybrid growth) and transmission types.
        5. **Key Drivers of Sales**:
            -   Analyze **Price Sensitivity**: Which price segments (Budget, Mid, Premium, Luxury) drive the most volume?
            -   Analyze **Aesthetic Preferences**: Which colors are most popular?
            -   Mention the statistical correlations as supporting evidence.
        6. **Strategic Recommendations**: Provide actionable business advice based on the data.
        7. **Additional Insight**: Add one creative insight or prediction about the future of mobility.

        Format the output in clear Markdown with headers. Do not include any code blocks or raw JSON. Focus on business value.
        """
