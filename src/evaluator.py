import os
import re

class ReportEvaluator:
    def __init__(self, report_path='output/Interactive_Report.html'):
        self.report_path = report_path

    def evaluate(self):
        """
        Evaluates the generated report for completeness and correctness.
        Returns a dictionary of evaluation results.
        """
        results = {
            "file_exists": False,
            "file_size_ok": False,
            "has_h1_title": False,
            "has_sections": False,
            "has_plots": False,
            "score": 0
        }

        if not os.path.exists(self.report_path):
            print(f"Evaluation Failed: Report file not found at {self.report_path}")
            return results

        results["file_exists"] = True
        
        # Check file size (should be > 1KB)
        file_size = os.path.getsize(self.report_path)
        if file_size > 1024:
            results["file_size_ok"] = True

        with open(self.report_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check H1
        if re.search(r'<h1.*?>.*?BMW.*?Report.*?</h1>', content, re.IGNORECASE):
            results["has_h1_title"] = True

        # Check Sections (Executive Summary, Sales Trends, etc.)
        required_sections = [
            "Executive Summary",
            "Sales Trends",
            "Regional",
            "Mobility",
            "Key Drivers",
            "Recommendations"
        ]
        
        sections_found = 0
        for section in required_sections:
            if re.search(rf'<h[23].*?>.*?{section}.*?</h[23]>', content, re.IGNORECASE):
                sections_found += 1
        
        if sections_found >= len(required_sections) - 1: # Allow 1 missing
            results["has_sections"] = True

        # Check Plots
        # We expect at least 5 plots (yearly, regional, models, fuel, transmission, price/correlation, color)
        plot_count = len(re.findall(r'class="plotly-graph-div"', content))
        if plot_count >= 5:
            results["has_plots"] = True

        # Calculate Score (Simple)
        score = 0
        if results["file_exists"]: score += 20
        if results["file_size_ok"]: score += 20
        if results["has_h1_title"]: score += 10
        if results["has_sections"]: score += 25
        if results["has_plots"]: score += 25
        
        results["score"] = score
        
        return results

    def print_report(self):
        results = self.evaluate()
        print("\n" + "="*50)
        print("REPORT EVALUATION RESULTS")
        print("="*50)
        print(f"File Exists:      {'✅' if results['file_exists'] else '❌'}")
        print(f"File Size OK:     {'✅' if results['file_size_ok'] else '❌'}")
        print(f"Title Present:    {'✅' if results['has_h1_title'] else '❌'}")
        print(f"Sections Present: {'✅' if results['has_sections'] else '❌'}")
        print(f"Plots Present:    {'✅' if results['has_plots'] else '❌'}")
        print("-"*50)
        print(f"Quality Score:    {results['score']}/100")
        print("="*50 + "\n")
