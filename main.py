import os
import sys
from src.data_loader import DataLoader
from src.analyzer import BMWAnalyzer
from src.visualizer import BMWVisualizer
from src.llm_client import LLMClient
from src.report_generator import ReportGenerator

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
    plot_paths = visualizer.generate_all_plots()
    print(f"Plots saved to {visualizer.output_dir}")

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
    print("Compiling final report...")
    generator = ReportGenerator()
    report_path = generator.generate_report(narrative, plot_paths)
    
    print("="*50)
    print(f"SUCCESS! Report generated at: {report_path}")
    print("="*50)

if __name__ == "__main__":
    main()
