import numpy as np
import pandas as pd
from typing import Dict, Any, List
from .data_fetch import DataFetcher

class LBOModel:
    def __init__(self, ticker: str):
        self.fetcher = DataFetcher(ticker)
        self.inputs = {}
        self.projections = pd.DataFrame()
        self.debt_schedule = pd.DataFrame()
        self.returns = {}

    def run(self, 
            equity_pct: float = 0.3, 
            entry_multiple: float = 10.0, 
            exit_multiple: float = 10.0, 
            years: int = 5,
            interest_rate: float = 0.06,
            min_cash: float = 50e6):
        """Run the full LBO model."""
        self.inputs = self.fetcher.get_lbo_inputs()
        
        # 1. Transaction Summary (Sources & Uses)
        entry_ebitda = self.inputs['ebitda']
        enterprise_value = entry_ebitda * entry_multiple
        total_uses = enterprise_value # Simplified: assume EV includes debt payoff
        
        equity_contribution = total_uses * equity_pct
        total_debt_funded = total_uses - equity_contribution
        
        # 2. Projections
        proj_years = list(range(1, years + 1))
        rev_growth = self.inputs['rev_growth']
        ebitda_margin = self.inputs['ebitda_margin']
        tax_rate = self.inputs['tax_rate']
        capex_pct = self.inputs['capex_pct_rev']
        
        proj_data = []
        curr_rev = self.inputs['revenue']
        curr_debt = total_debt_funded
        curr_cash = self.inputs['total_cash']
        
        for year in proj_years:
            rev = curr_rev * (1 + rev_growth)
            ebitda = rev * ebitda_margin
            depreciation = ebitda * 0.2 # Assumption: D&A is 20% of EBITDA
            ebit = ebitda - depreciation
            interest = curr_debt * interest_rate
            pretax = ebit - interest
            taxes = max(0, pretax * tax_rate)
            net_income = pretax - taxes
            
            capex = rev * capex_pct
            change_in_wc = rev * 0.01 # Assumption: WC is 1% of revenue growth
            
            fcf_pre_debt = net_income + depreciation - capex - change_in_wc
            
            # Debt Paydown
            debt_repayment = min(curr_debt, fcf_pre_debt)
            curr_debt -= debt_repayment
            
            proj_data.append({
                'Year': year,
                'Revenue': rev,
                'EBITDA': ebitda,
                'EBIT': ebit,
                'Interest': interest,
                'Net Income': net_income,
                'FCF': fcf_pre_debt,
                'Debt Repayment': debt_repayment,
                'Ending Debt': curr_debt
            })
            curr_rev = rev
            
        self.projections = pd.DataFrame(proj_data)
        
        # 3. Exit & Returns
        exit_ebitda = proj_data[-1]['EBITDA']
        exit_ev = exit_ebitda * exit_multiple
        exit_debt = proj_data[-1]['Ending Debt']
        exit_equity_value = exit_ev - exit_debt
        
        moic = exit_equity_value / equity_contribution
        if moic > 0:
            irr = (moic ** (1/years)) - 1
        else:
            irr = -1.0 # Total loss
        
        self.returns = {
            'Entry EV': enterprise_value,
            'Equity Contribution': equity_contribution,
            'Debt Funded': total_debt_funded,
            'Exit EV': exit_ev,
            'Exit Equity Value': exit_equity_value,
            'MOIC': moic,
            'IRR': irr
        }
        
        return self.returns

    def sensitivity_analysis(self, entry_range: List[float], exit_range: List[float]) -> pd.DataFrame:
        """Generate IRR sensitivity matrix."""
        matrix = []
        for entry in entry_range:
            row = []
            for exit in exit_range:
                res = self.run(entry_multiple=entry, exit_multiple=exit)
                row.append(res['IRR'])
            matrix.append(row)
            
        return pd.DataFrame(matrix, 
                          index=[f"{float(x)}x" for x in entry_range], 
                          columns=[f"{float(x)}x" for x in exit_range])
