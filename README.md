# BMW Sales Analysis & Automated Reporting

This project automates the analysis of BMW sales data, generating key insights and visualizations, and producing a cohesive executive report using LLM (Google Gemini).

## Project Structure

```
.
├── src/
│   ├── data_loader.py      # Handles data ingestion and validation
│   ├── analyzer.py         # Performs statistical analysis
│   ├── visualizer.py       # Generates plots using matplotlib/seaborn
│   ├── llm_client.py       # Interfaces with Google Gemini API
│   └── report_generator.py # Assembles final Markdown report
├── output/                 # Generated artifacts (images, report)
├── data/                   # Input data
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
└── .env                    # API Keys configuration
```

## Prerequisites

-   Python 3.8 or higher
-   A Google Gemini API Key

## Setup & Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/duguqiankun/AI-Engineer-Case-Study.git
    cd AI-Engineer-Case-Study
    ```

2.  **Create and activate a virtual environment** (recommended):
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure API Key**:
    -   Copy `.env.example` to `.env`:
        ```bash
        cp .env.example .env
        ```
    -   Open `.env` and replace `your_api_key_here` with your Google Gemini API Key.
    -   *Note: Using Gemini Flash model which is efficient and cost-effective.*

## Usage

Run the main script:
```bash
python main.py
```

The script will:
1.  Load the sales data from `data/BMW sales data (2020-2024).xlsx`.
2.  Compute trends (including Fuel/Transmission), top performers, and correlations.
3.  Generate interactive Plotly charts.
4.  Send summary statistics to the LLM to generate a narrative.
5.  Save the final report to `output/Interactive_Report.html`.

## Deliverables
-   **Codebase**: Modular Python scripts.
-   **Generated Report**: `output/Interactive_Report.html` (open in browser).
-   **Executive Summary**: `Executive_Summary.md` (describing the solution design).
