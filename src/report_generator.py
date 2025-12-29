import os

class ReportGenerator:
    def __init__(self, output_dir='output'):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_report(self, narrative_text, plot_paths):
        """
        Combines narrative text and plot paths into a Markdown report.
        """
        report_path = os.path.join(self.output_dir, 'Report.md')
        
        # We need relative paths for the markdown images to render correctly if the markdown is opened in the output folder or root
        # Assuming report is in output/Report.md and images are in output/images/
        # Relative path from Report.md to images is "images/filename"
        
        # Helper to get relative path
        def get_rel_path(full_path):
            return os.path.join('images', os.path.basename(full_path))

        # Insert images into relevant sections if possible, or append them.
        # Since the LLM text structure is somewhat dynamic, appending them or inserting them at known markers is safer.
        # But a simple approach is to append them at the end or intersperse them.
        # Let's try to append them after specific headers if they exist, or just at the bottom.
        
        # Better yet, let's just append the Visual Appendix at the bottom.
        
        content = f"{narrative_text}\n\n"
        content += "## Visual Appendix\n\n"
        
        content += "### 1. Yearly Sales Trend\n"
        content += f"![Yearly Trend]({get_rel_path(plot_paths['yearly_trend'])})\n\n"
        
        content += "### 2. Regional Performance\n"
        content += f"![Regional Sales]({get_rel_path(plot_paths['regional_sales'])})\n\n"
        
        content += "### 3. Top Performing Models\n"
        content += f"![Top Models]({get_rel_path(plot_paths['top_models'])})\n\n"
        
        content += "### 4. Price vs Sales Analysis\n"
        content += f"![Price vs Sales]({get_rel_path(plot_paths['price_vs_sales'])})\n\n"

        with open(report_path, 'w') as f:
            f.write(content)
            
        return report_path
