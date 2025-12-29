import os
import sys
from src.data_loader import DataLoader
from src.analyzer import BMWAnalyzer
from src.visualizer import BMWVisualizer
from src.llm_client import LLMClient
from src.report_generator import ReportGenerator
from src.evaluator import ReportEvaluator

def main():
    print("Starting BMW Sales Report Generation Workflow...")

    # Configuration
    DATA_PATH = 'data/BMW sales data (2020-2024).xlsx'
    
    # 1. Load Data
    print("Loading data...")
    try:
        loader = DataLoader(DATA_PATH)
        df = loader.load_data()
        print(f"Data loaded successfully. Shape: {df.shape}")
    except Exception as e:
        print(f"Failed to load data: {e}")
        sys.exit(1)

    # 2. Analyze Data
    print("Analyzing data...")
    analyzer = BMWAnalyzer(df)
    summary_stats = analyzer.get_summary_stats()
    print("Summary stats calculated.")

    # 3. Generate Visualizations
    print("Generating visualizations...")
    visualizer = BMWVisualizer(df)
    # This now returns a dictionary of HTML strings
    plot_htmls = visualizer.generate_all_plots()
    print("Interactive plots generated.")

    # 4. Generate AI Narrative
    print("Generating AI narrative...")
    try:
        llm = LLMClient()
        narrative = llm.generate_report_content(summary_stats)
        print("AI Narrative generated.")
    except ValueError as ve:
        print(f"Warning: {ve}")
        narrative = "## AI Generation Skipped\n\nNo API Key provided. Please check .env file."
    except Exception as e:
        print(f"Warning: AI generation failed: {e}")
        narrative = f"## AI Generation Failed\n\nError: {e}"

    # 5. Compile Report
    print("Compiling final interactive report...")
    generator = ReportGenerator()
    report_path = generator.generate_interactive_report(narrative, plot_htmls)
    
    print("="*50)
    print(f"SUCCESS! Interactive Report generated at: {report_path}")
    print("="*50)

    # 6. Evaluate Report
    print("Evaluating report quality...")
    evaluator = ReportEvaluator(report_path)
    evaluator.print_report()

if __name__ == "__main__":
    main()
