# Modern Automated LBO 🚀

[![GitHub Stars](https://img.shields.io/github/stars/gilhermanns/modern-automated-lbo?style=social)](https://github.com/gilhermanns/modern-automated-lbo/stargazers)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/modern-automated-lbo)](https://pypi.org/project/modern-automated-lbo/)

`modern-automated-lbo` is a robust Python library for automated Leveraged Buyout (LBO) modeling. It pulls real-time financial data via `yfinance`, builds comprehensive LBO models, and generates professional, client-ready Excel reports.

## Features

*   **Real-time Data**: Automatic fetching of historical financials, EBITDA, debt, and market cap using `yfinance`.
*   **Full LBO Mechanics**: Sources & Uses, 5-year projections, debt paydown schedule, and returns waterfall.
*   **Professional Excel Output**: Multi-sheet Excel reports with corporate styling and sensitivity analysis.
*   **Sensitivity Analysis**: 5x5 IRR matrix for entry vs. exit multiples.
*   **CLI & Library**: Use it as a command-line tool or integrate it into your Python workflows.

## Installation

```bash
pip install git+https://github.com/gilhermanns/modern-automated-lbo.git
```

## Quickstart

### Command Line Interface (CLI)

Run a full LBO analysis for a ticker (e.g., AAPL) with default assumptions:

```bash
lbo AAPL --equity_pct 0.3 --entry_multiple 12.0 --exit_multiple 14.0
```

### Python Library

```python
from automated_lbo import LBOModel, ExcelWriter

# Initialize and run the model
model = LBOModel("MSFT")
returns = model.run(equity_pct=0.3, entry_multiple=10.0, exit_multiple=12.0)

print(f"IRR: {returns['IRR']*100:.2f}%")
print(f"MOIC: {returns['MOIC']:.2f}x")

# Export to Excel
writer = ExcelWriter(model)
writer.save("MSFT_LBO_Analysis.xlsx")
```

## Project Structure

```
modern-automated-lbo/
├── src/automated_lbo/
│   ├── data_fetch.py    # yfinance integration
│   ├── lbo_model.py     # Core LBO logic
│   ├── excel_writer.py  # Professional Excel reports
│   └── cli.py           # Command-line interface
├── examples/            # Jupyter notebooks and demo scripts
├── tests/               # Unit tests
└── README.md
```

## Methodology

The model follows standard Private Equity (PE) and Investment Banking (IB) workflows:
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
