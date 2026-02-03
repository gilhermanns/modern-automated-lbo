import pytest
from automated_lbo.lbo_model import LBOModel

def test_lbo_run():
    # Use a well-known ticker for testing
    model = LBOModel("AAPL")
    # We don't need to fetch real data for a simple logic test if we mock or just check structure
    # But since we have internet, let's do a quick real run
    returns = model.run(equity_pct=0.3, entry_multiple=10.0, exit_multiple=10.0, years=5)
    
    assert 'IRR' in returns
    assert 'MOIC' in returns
    assert returns['MOIC'] > 0
    assert len(model.projections) == 5

def test_sensitivity():
    model = LBOModel("MSFT")
    sens = model.sensitivity_analysis(entry_range=[8, 10], exit_range=[8, 10])
    assert sens.shape == (2, 2)
    assert "8.0x" in sens.index
    assert "10.0x" in sens.columns
