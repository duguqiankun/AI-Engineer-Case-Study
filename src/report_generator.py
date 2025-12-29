import os
import markdown
import re

class ReportGenerator:
    def __init__(self, output_dir='output'):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_interactive_report(self, narrative_text, plot_htmls):
        """
        Generates an interactive HTML report with Plotly charts embedded.
        """
        report_path = os.path.join(self.output_dir, 'Interactive_Report.html')
        
        # Convert Markdown narrative to HTML
        narrative_html = markdown.markdown(narrative_text, extensions=['extra'])
        
        # Define injection points
        # Map simpler keywords to plot keys
        injections = [
            (r'(<h[23]>.*?Sales Trends.*?</h[23]>)', 'yearly_trend'),
            (r'(<h[23]>.*?Regional.*?Performance.*?</h[23]>)', 'regional_sales'),
            (r'(<h[23]>.*?Regional.*?Performance.*?</h[23]>)', 'top_models'), # Inject both here? Or split? Let's inject top_models after regional
            (r'(<h[23]>.*?Mobility Trends.*?</h[23]>)', 'fuel_trend'),
            (r'(<h[23]>.*?Mobility Trends.*?</h[23]>)', 'transmission'),
            (r'(<h[23]>.*?Key Drivers.*?</h[23]>)', 'price_vs_sales')
        ]
        
        # We need to handle multiple injections carefully. 
        # Easier strategy: Split the text by headers?
        # Or just use replace with a marker?
        
        # Let's simple append plots after the matched header. 
        # Since we might match the same header multiple times (e.g. for Regional and Top Models), 
        # we should do it sequentially or use specific markers.
        
        # Simplified approach: Append the plot DIV after the header tag.
        
        for pattern, plot_key in injections:
            if plot_key in plot_htmls:
                plot_div = f'<div class="chart-container">{plot_htmls[plot_key]}</div>'
                # Use sub to insert after the match. count=1 to only do it once per plot per header type logic
                # But wait, if we have multiple plots for one header, we need to be careful.
                # Let's just create a combined string of plots if multiple map to one header?
                # No, the loop runs for each plot.
                # Regex replace: replace the header with "header + plot".
                
                # Check if we already inserted this plot?
                # No need, we iterate through injections list.
                
                # However, if we replace the header, the next injection looking for the same header pattern will find it again?
                # Yes. So we should probably iterate the narrative once or be careful.
                
                # Let's try to just insert them.
                # But if we modify `narrative_html` in place, the offsets change.
                # Regex replace is safe regarding offsets if we just replace string content.
                
                # Problem: If I replace "<h2>Header</h2>" with "<h2>Header</h2><div>Plot</div>", the next regex finding "<h2>Header</h2>" will match the same thing and insert another plot.
                # Result: "<h2>Header</h2><div>Plot2</div><div>Plot1</div>". This is actually fine! They will stack.
                
                # So I will just loop and replace.
                # To avoid re-matching the already modified string loop forever, I will trust that standard python re.sub doesn't do recursive replacement in that way unless called repeatedly.
                
                # Actually, I should use a unique marker if I want to be precise, but let's try this.
                # I'll use a specific regex that matches the header tag.
                
                # Important: Remove the plot from plot_htmls so we know which ones are used, 
                # to append unused ones at the end.
                pass

        # Better logic:
        # 1. Create a dictionary of Header Key -> List of Plots
        header_plots = {}
        unused_plots = set(plot_htmls.keys())
        
        keywords = {
            'Sales Trends': ['yearly_trend'],
            'Regional': ['regional_sales', 'top_models'],
            'Mobility': ['fuel_trend', 'transmission'],
            'Fuel': ['fuel_trend', 'transmission'], # Fallback
            'Drivers': ['price_segments', 'color_sales', 'price_vs_sales']
        }
        
        # We iterate through the HTML to find headers, and if they match a keyword, we prepare the injection
        # But iterating HTML with regex is brittle.
        # Let's just do a blind search/replace for the headers we expect from the prompt.
        
        for key, plot_list in keywords.items():
            # Find the header in HTML
            # Case insensitive search for header containing key
            pattern = re.compile(f'(<h[23][^>]*>.*{key}.*?</h[23]>)', re.IGNORECASE)
            match = pattern.search(narrative_html)
            if match:
                # We found a header. We will append the plots after it.
                plots_to_insert = []
                for pk in plot_list:
                    if pk in unused_plots:
                        plots_to_insert.append(plot_htmls[pk])
                        unused_plots.remove(pk)
                
                if plots_to_insert:
                    injection = "\n".join([f'<div class="chart-container">{p}</div>' for p in plots_to_insert])
                    # Replace the header with Header + Injection
                    # We use a lambda to ensure we replace the exact match
                    narrative_html = pattern.sub(lambda m: m.group(1) + injection, narrative_html, count=1)

        # Append remaining unused plots at the end
        if unused_plots:
            narrative_html += "<h2>Visual Appendix</h2>"
            for pk in unused_plots:
                narrative_html += f'<div class="chart-container">{plot_htmls[pk]}</div>'

        # Full HTML Template
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>BMW Sales Analysis Report</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 1000px;
                    margin: 0 auto;
                    padding: 40px;
                    background-color: #f9f9f9;
                }}
                h1, h2, h3 {{
                    color: #003366; /* BMW Blue-ish */
                }}
                h1 {{
                    border-bottom: 2px solid #003366;
                    padding-bottom: 10px;
                }}
                .chart-container {{
                    background: white;
                    padding: 20px;
                    margin: 30px 0;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }}
                /* Responsive plots */
                .plotly-graph-div {{
                    width: 100% !important;
                }}
            </style>
        </head>
        <body>
            {narrative_html}
        </body>
        </html>
        """
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return report_path
