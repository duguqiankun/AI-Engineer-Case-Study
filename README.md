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

## Setup & Installation

1.  **Clone the repository**:
    ```bash
    git clone <repo-url>
    cd <repo-name>
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Key**:
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
1.  Load the sales data.
2.  Compute trends, top performers, and correlations.
3.  Generate charts in `output/images/`.
4.  Send summary statistics to the LLM to generate a narrative.
5.  Save the final report to `output/Report.md`.

## Deliverables
-   **Codebase**: Modular Python scripts.
-   **Generated Report**: `output/Report.md` (check this file after running).
-   **Executive Summary**: `Executive_Summary.md` (describing the solution design).
