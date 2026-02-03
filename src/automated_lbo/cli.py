import click
from .lbo_model import LBOModel
from .excel_writer import ExcelWriter

@click.command()
@click.argument('ticker')
@click.option('--equity_pct', default=0.3, help='Equity contribution percentage (0.0 to 1.0)')
@click.option('--entry_multiple', default=10.0, help='Entry EV/EBITDA multiple')
@click.option('--exit_multiple', default=10.0, help='Exit EV/EBITDA multiple')
@click.option('--years', default=5, help='Investment horizon in years')
@click.option('--output', default=None, help='Output Excel filename')
def main(ticker, equity_pct, entry_multiple, exit_multiple, years, output):
    """Automated LBO Modeling CLI."""
    click.echo(f"Running LBO model for {ticker}...")
    
    try:
        model = LBOModel(ticker)
        returns = model.run(
            equity_pct=equity_pct,
            entry_multiple=entry_multiple,
            exit_multiple=exit_multiple,
            years=years
        )
        
        click.echo("\n--- LBO Returns ---")
        click.echo(f"IRR: {returns['IRR']*100:.2f}%")
        click.echo(f"MOIC: {returns['MOIC']:.2f}x")
        
        if output is None:
            output = f"{ticker}_LBO_Model.xlsx"
            
        writer = ExcelWriter(model)
        writer.save(output)
        click.echo(f"\nExcel report saved to {output}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

if __name__ == "__main__":
    main()
