# Modern Automated LBO

[![GitHub Stars](https://img.shields.io/github/stars/gilhermanns/modern-automated-lbo?style=social)](https://github.com/gilhermanns/modern-automated-lbo/stargazers)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://github.com/gilhermanns/modern-automated-lbo)

`modern-automated-lbo` is a Python-based tool for Leveraged Buyout (LBO) modeling. It pulls financial data via `yfinance`, builds LBO models, and generates Excel reports.

## Features

*   **Data Integration**: Automatic fetching of historical financials, EBITDA, debt, and market cap using `yfinance`.
*   **LBO Mechanics**: Sources & Uses, 5-year projections, debt paydown schedule, and returns waterfall.
*   **Excel Output**: Multi-sheet Excel reports with sensitivity analysis.
*   **Sensitivity Analysis**: IRR matrix for entry vs. exit multiples.
*   **CLI & Library**: Use it as a command-line tool or integrate it into your Python workflows.

## Installation

```bash
git clone https://github.com/gilhermanns/modern-automated-lbo.git
cd modern-automated-lbo
pip install -r requirements.txt
```

## Quickstart

### Command Line Interface (CLI)

Run an LBO analysis for a ticker (e.g., AAPL):

```bash
python main.py AAPL --equity_pct 0.3 --entry_multiple 12.0 --exit_multiple 14.0
```

### Python Usage

```python
from src.models.lbo import LBOModel

# Initialize and run the model
model = LBOModel("MSFT")
returns = model.run(equity_pct=0.3, entry_multiple=10.0, exit_multiple=12.0)

print(f"IRR: {returns['IRR']*100:.2f}%")
print(f"MOIC: {returns['MOIC']:.2f}x")
```

## Methodology

The model follows standard financial workflows:
1.  **Entry Valuation**: Based on a target EV/EBITDA multiple.
2.  **Capital Structure**: Funded via equity contribution and debt.
3.  **Operations**: 5-year projections for Revenue, EBITDA, and FCF.
4.  **Debt Paydown**: FCF is used to pay down debt according to a simplified schedule.
5.  **Exit**: Valuation at a target exit multiple, calculating net proceeds to equity.
6.  **Returns**: IRR and MOIC calculations based on initial equity and exit proceeds.

## Disclaimer

This tool is for educational and analytical purposes only. It is not financial advice. Always conduct your own due diligence.

## License

MIT License
