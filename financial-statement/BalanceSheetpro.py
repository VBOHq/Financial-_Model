import streamlit as st
import pandas as pd

class BalanceSheetpro:
    # ... (your existing BalanceSheet class code)
    def __init__(self, assumptions, historical_data):
        self.assumptions = assumptions
        self.historical_data = historical_data
        
    def calculate_inventory(self):
        # Calculate inventory based on the days inventory assumption
        days_inventory = self.assumptions["Days Inventory"]
        projected_inventory = [
            (self.historical_data["Cost of Goods Sold (COGS)"].iloc[i] / 365)
            * days_inventory
            for i in range(5)
        ]

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Inventory": projected_inventory,
            }
        )
        
    def calculate_accounts_receivable(self):
        days_accounts_receivable = self.assumptions["Days Accounts Receivable"]
        projected_accounts_receivable = [
            (self.historical_data["Revenue"].iloc[i] / 365) * days_accounts_receivable
            for i in range(5)
        ]

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Accounts Receivable": projected_accounts_receivable,
            }
        )
        
    def calculate_other_current_assets(self):
        # Provide a default value or handle the case when the key is not present
        other_current_assets = self.assumptions.get("Other Current Assets", 0)  # Use 0 as a default value, you can change it as needed
        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1] + [i for i in range(1, 6)],
                "Other Current Assets": [other_current_assets] * 5,
            }
        )




        
    def calculate_total_current_assets(self):
        inventory = self.calculate_inventory()["Inventory"]
        accounts_receivable = self.calculate_accounts_receivable()["Accounts Receivable"]
        
        # Ensure that other_current_assets is a numeric value
        other_current_assets = self.calculate_other_current_assets()["Other Current Assets"]
        other_current_assets = pd.to_numeric(other_current_assets, errors='coerce').fillna(0)

        total_current_assets = inventory + accounts_receivable + other_current_assets

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1] + [i for i in range(1, 6)],
                "Total Current Assets": total_current_assets,
            }
        )

    def calculate_net_ppe(self):
        gross_ppe = self.historical_data["Gross PP&E"]
        accumulated_depreciation = self.historical_data["Accumulated Depreciation"]
        net_ppe = gross_ppe - accumulated_depreciation

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Net PP&E": net_ppe,
            }
        )
        
    def calculate_goodwill(self):
        goodwill = self.historical_data["Goodwill"].iloc[-1]
        projected_goodwill = [goodwill] * 5

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Goodwill": projected_goodwill,
            }
        )
        
    def calculate_other_assets(self):
        other_assets = self.assumptions["Other Assets"]

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Other Assets": [other_assets] * 5,
            }
        )

    def calculate_total_assets(self):
        total_current_assets = self.calculate_total_current_assets()["Total Current Assets"]
        
        # Ensure that net_ppe, goodwill, and other_assets are numeric
        net_ppe = pd.to_numeric(self.calculate_net_ppe()["Net PP&E"], errors='coerce').fillna(0)
        goodwill = pd.to_numeric(self.calculate_goodwill()["Goodwill"], errors='coerce').fillna(0)
        other_assets = pd.to_numeric(self.calculate_other_assets()["Other Assets"], errors='coerce').fillna(0)

        total_assets = total_current_assets + net_ppe + goodwill + other_assets

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1] + [i for i in range(1, 6)],
                "Total Assets": total_assets,
            }
        )


    def calculate_accounts_payable(self):
        days_payable = self.assumptions["Days Payable"]
        projected_accounts_payable = [
            (self.historical_data["Cost of Goods Sold (COGS)"].iloc[i] / 365)
            * days_payable
            for i in range(5)
        ]

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Accounts Payable": projected_accounts_payable,
            }
        )

    def calculate_accrued_liabilities(self):
        accrued_liabilities_as_percentage_of_cogs = self.assumptions[
            "Accrued Liabilities as % of COGS"
        ]
        projected_accrued_liabilities = [
            self.historical_data["Cost of Goods Sold (COGS)"].iloc[i]
            * accrued_liabilities_as_percentage_of_cogs
            for i in range(5)
        ]

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Accrued Liabilities": projected_accrued_liabilities,
            }
        )

    def calculate_other_current_liabilities(self):
        other_current_liabilities_as_percentage_of_cogs = self.assumptions[
            "Other Current Liabilities as % of COGS"
        ]
        projected_other_current_liabilities = [
            self.historical_data["Cost of Goods Sold (COGS)"].iloc[i]
            * other_current_liabilities_as_percentage_of_cogs
            for i in range(5)
        ]

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Other Current Liabilities": projected_other_current_liabilities,
            }
        )

    def calculate_total_current_liabilities(self):
        accounts_payable = self.calculate_accounts_payable()["Accounts Payable"]
        accrued_liabilities = self.calculate_accrued_liabilities()[
            "Accrued Liabilities"
        ]
        other_current_liabilities = self.calculate_other_current_liabilities()[
            "Other Current Liabilities"
        ]

        total_current_liabilities = (
            accounts_payable + accrued_liabilities + other_current_liabilities
        )

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Total Current Liabilities": total_current_liabilities,
            }
        )

    def calculate_total_liabilities(self):
        total_current_liabilities = self.calculate_total_current_liabilities()[
            "Total Current Liabilities"
        ]
        other_liabilities = self.assumptions["Other Liabilities"]

        total_liabilities = total_current_liabilities + other_liabilities

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Total Liabilities": total_liabilities,
            }
        )

    def calculate_common_stock(self):
        common_stock = self.assumptions["Common Stock"]
        projected_common_stock = [common_stock] * 5

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Common Stock": projected_common_stock,
            }
        )

    def calculate_total_shareholders_equity(self):
        common_stock = self.calculate_common_stock()["Common Stock"]
        retained_earnings = self.historical_data["Retained Earnings"]
        total_shareholders_equity = common_stock + retained_earnings

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Total Shareholders Equity": total_shareholders_equity,
            }
        )

    def calculate_total_liabilities_and_equity(self):
        total_liabilities = self.calculate_total_liabilities()["Total Liabilities"]
        total_shareholders_equity = self.calculate_total_shareholders_equity()[
            "Total Shareholders Equity"
        ]
        total_liabilities_and_equity = total_liabilities + total_shareholders_equity

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Total Liabilities and Equity": total_liabilities_and_equity,
            }
        )

    def calculate_all_line_items(self):
        projected_inventory = self.calculate_inventory()
        projected_accounts_receivable = self.calculate_accounts_receivable()
        projected_other_current_assets = self.calculate_other_current_assets()
        projected_total_current_assets = self.calculate_total_current_assets()
        projected_net_ppe = self.calculate_net_ppe()
        projected_goodwill = self.calculate_goodwill()
        projected_other_assets = self.calculate_other_assets()
        projected_total_assets = self.calculate_total_assets()
        projected_accounts_payable = self.calculate_accounts_payable()
        projected_accrued_liabilities = self.calculate_accrued_liabilities()
        projected_other_current_liabilities = self.calculate_other_current_liabilities()
        projected_total_current_liabilities = self.calculate_total_current_liabilities()
        projected_total_liabilities = self.calculate_total_liabilities()
        projected_common_stock = self.calculate_common_stock()
        projected_total_shareholders_equity = self.calculate_total_shareholders_equity()
        projected_total_liabilities_and_equity = (
            self.calculate_total_liabilities_and_equity()
        )

        return pd.DataFrame(
            {
                "Year": projected_inventory["Year"],
                "Inventory": projected_inventory["Inventory"],
                "Accounts Receivable": projected_accounts_receivable[
                    "Accounts Receivable"
                ],
                "Other Current Assets": projected_other_current_assets[
                    "Other Current Assets"
                ],
                "Total Current Assets": projected_total_current_assets[
                    "Total Current Assets"
                ],
                "Net PP&E": projected_net_ppe["Net PP&E"],
                "Goodwill": projected_goodwill["Goodwill"],
                "Other Assets": projected_other_assets["Other Assets"],
                "Total Assets": projected_total_assets["Total Assets"],
                "Accounts Payable": projected_accounts_payable["Accounts Payable"],
                "Accrued Liabilities": projected_accrued_liabilities[
                    "Accrued Liabilities"
                ],
                "Other Current Liabilities": projected_other_current_liabilities[
                    "Other Current Liabilities"
                ],
                "Total Current Liabilities": projected_total_current_liabilities[
                    "Total Current Liabilities"
                ],
                "Total Liabilities": projected_total_liabilities["Total Liabilities"],
                "Common Stock": projected_common_stock["Common Stock"],
                "Total Shareholders Equity": projected_total_shareholders_equity[
                    "Total Shareholders Equity"
                ],
                "Total Liabilities and Equity": projected_total_liabilities_and_equity[
                    "Total Liabilities and Equity"
                ],
            }
        )

# Function to calculate and display the projected balance sheet
def calculate_and_display_balance_sheets(assumptions, historical_data):
    balance_sheets = BalanceSheetpro(assumptions, historical_data)
    projected_balance_sheet = balance_sheets.calculate_all_line_items()
    
    st.subheader("Projected Balance Sheet:")
    st.write("projected_balance_sheets")

# Streamlit app
# Streamlit app
def main():
    st.title("Projected Balance Sheet Calculator")

    # Input assumptions
    st.sidebar.header("Assumptions")
    days_inventory = st.sidebar.slider("Days Inventory", min_value=1, max_value=365, value=30)
    days_accounts_receivable = st.sidebar.slider("Days Accounts Receivable", min_value=1, max_value=365, value=30)
    
    # Use text input for assumptions that are strings
    other_current_assets = st.sidebar.text_input("Other Current Assets", "Default Value")
    other_assets = st.sidebar.text_input("Other Assets", "Default Value")
    days_payable = st.sidebar.slider("Days Payable", min_value=1, max_value=365, value=30)
    accrued_liabilities_percentage = st.sidebar.slider("Accrued Liabilities as % of COGS", min_value=0.0, max_value=100.0, value=5.0)
    other_current_liabilities_percentage = st.sidebar.slider("Other Current Liabilities as % of COGS", min_value=0.0, max_value=100.0, value=5.0)
    other_liabilities = st.sidebar.slider("Other Liabilities", min_value=0.0, max_value=100.0, value=5.0)
    common_stock = st.sidebar.slider("Common Stock", min_value=0.0, max_value=100.0, value=5.0)



    assumptions = {
        "Days Inventory": days_inventory,
        "Days Accounts Receivable": days_accounts_receivable,
        "Other Current Assets": other_current_assets,
        "Other Assets": other_assets,
        "Days Payable": days_payable,
        "Accrued Liabilities as % of COGS": accrued_liabilities_percentage, 
        "Other Current Liabilities as % of COGS": other_current_liabilities_percentage,
        "Other Liabilities": other_liabilities,
        "Common Stock": common_stock
        # Add other assumptions as needed...
    }
    
    
    #assumptions = {
        #"Days Inventory": days_inventory,
        #"Days Accounts Receivable": days_accounts_receivable,
        #"Other Current Assets": default_value,  # Provide a default value here
        # Add other assumptions as needed...
    #}


    # Upload historical data (assuming a CSV file for simplicity)
    uploaded_file = st.file_uploader("Upload Historical Data (CSV)", type=["csv"])
    if uploaded_file is not None:
        historical_data = pd.read_csv(uploaded_file)
        st.subheader("Historical Data:")
        st.write(historical_data)

        # Calculate and display the projected balance sheet
        calculate_and_display_balance_sheets(assumptions, historical_data)

if __name__ == "__main__":
    main()


   