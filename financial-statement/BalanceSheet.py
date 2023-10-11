import pandas as pd
import streamlit as st
import json
from streamlit_lottie import st_lottie



# Function to load Lottie file from file path
def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading Lottie file: {e}")
        return None




class BalanceSheet:
    def __init__(self, assets, otherAsset, liabilities, equity, gross_ppe, accumulated_depreciation, goodwill):
        self.assets = assets
        self.otherAsset = otherAsset
        self.liabilities = liabilities
        self.equity = equity
        self.gross_ppe = gross_ppe
        self.accumulated_depreciation = accumulated_depreciation
        self.goodwill = goodwill

    def calculate_total_assets(self):
        return self.calculate_total_current_assets() + self.goodwill + self.calculate_net_ppe()

    def calculate_total_current_assets(self):
        return sum([self.assets["Cash"], self.assets["Accounts Receivable"], self.assets["inventory"], self.assets["Other Current Assets"], self.otherAsset])

    def calculate_net_ppe(self):
        return self.gross_ppe - self.accumulated_depreciation

    def calculate_total_liabilities(self):
        return sum(self.liabilities.values())

    def calculate_total_equity(self):
        return sum(self.equity.values())

    def calculate_total_liabilities_and_equity(self):
        return self.calculate_total_liabilities() + self.calculate_total_equity()
    
    

    def display_balance_sheet(self):
        st.title("Balance Sheet")
        


        # Display Assets
        assets_data = {
            'Categories': ['Cash', 'Accounts Receivable', 'Inventory', 'Other Current Assets', 'Other Asset'],
            'Amount': [self.assets["Cash"], self.assets["Accounts Receivable"], self.assets["inventory"], self.assets["Other Current Assets"], self.otherAsset]
        }
        assets_df = pd.DataFrame(assets_data, columns=['Categories', 'Amount'])
        st.subheader("Assets:")
        st.table(assets_df)

        # Display Net PPE
        net_ppe_data = {
            'Categories': ['Gross PP&E', 'Accumulated Depreciation', 'Net PPE'],
            'Amount': [self.gross_ppe, self.accumulated_depreciation, self.calculate_net_ppe()]
        }
        net_ppe_df = pd.DataFrame(net_ppe_data, columns=['Categories', 'Amount'])
        st.subheader("Net PPE:")
        st.table(net_ppe_df)

        # Display Total Assets
        total_assets_data = {
            'Categories': ['Total Assets'],
            'Amount': [self.calculate_total_assets()]
        }
        total_assets_df = pd.DataFrame(total_assets_data, columns=['Categories', 'Amount'])
        st.subheader("Total Assets:")
        st.table(total_assets_df)

        # Display Liabilities
        liabilities_data = {
            'Categories': list(self.liabilities.keys()),
            'Amount': list(self.liabilities.values())
        }
        liabilities_df = pd.DataFrame(liabilities_data, columns=['Categories', 'Amount'])
        st.subheader("Liabilities:")
        st.table(liabilities_df)

        # Display Equity
        equity_data = {
            'Categories': list(self.equity.keys()),
            'Amount': list(self.equity.values())
        }
        equity_df = pd.DataFrame(equity_data, columns=['Categories', 'Amount'])
        st.subheader("Equity:")
        st.table(equity_df)

        # Display Total Liabilities and Equity
        total_liabilities_and_equity_data = {
            'Categories': ['Total Liabilities and Equity'],
            'Amount': [self.calculate_total_liabilities_and_equity()]
        }
        total_liabilities_and_equity_df = pd.DataFrame(total_liabilities_and_equity_data, columns=['Categories', 'Amount'])
        st.subheader("Total Liabilities and Equity:")
        st.table(total_liabilities_and_equity_df)

        # Plot the stacked bar chart
        st.subheader("Balance Sheet Chart")
        data = {
            'Categories': ['Assets', 'Liabilities', 'Shareholders_Equity'],
            'Amount': [self.calculate_total_assets(), self.calculate_total_liabilities(), self.calculate_total_equity()]
        }
        df = pd.DataFrame(data)
        pivoted_df = df.pivot(columns='Categories', values='Amount')
        st.bar_chart(pivoted_df)
        
        

def main():
    st.set_page_config(page_title="Balance Sheet App", page_icon="💰")
    
    
    # Sidebar for input fields
    st.sidebar.title("Balance Sheet Inputs")

    assets = {
        "Cash": st.sidebar.number_input("Cash", value=0.0),
        "Accounts Receivable": st.sidebar.number_input("Accounts Receivable", value=13.0),
        "inventory": st.sidebar.number_input("Inventory", value=8.5),
        "Other Current Assets": st.sidebar.number_input("Other Current Assets", value=1.0),
    }

    otherAsset_value = st.sidebar.number_input("Other Asset", value=0.0)
    gross_ppe_value = st.sidebar.number_input("Gross PP&E", value=287.2)
    accumulated_depreciation_value = st.sidebar.number_input("Accumulated Depreciation", value=30.0)
    goodwill_value = st.sidebar.number_input("Goodwill", value=5.0)

    liabilities = {
        "Accounts Payable": st.sidebar.number_input("Accounts Payable", value=9.0),
        "Accrued Liabilities": st.sidebar.number_input("Accrued Liabilities", value=2.1),
        "Other Current Liabilities": st.sidebar.number_input("Other Current Liabilities", value=0.0),
        "Revolving Credit Facility": st.sidebar.number_input("Revolving Credit Facility", value=18.9),
        "Term Loan": st.sidebar.number_input("Term Loan", value=160.0),
        "Unsecured Debt": st.sidebar.number_input("Unsecured Debt", value=50.0),
        "Other Liabilities": st.sidebar.number_input("Other Liabilities", value=2.0),
    }

    equity = {
        "Retained Earnings": st.sidebar.number_input("Retained Earnings", value=32.7),
        "Common Stock": st.sidebar.number_input("Common Stock", value=10.0),
    }

    # Pass the parameters to create an instance of BalanceSheet
    balance_sheet = BalanceSheet(assets, otherAsset_value, liabilities, equity, gross_ppe_value, accumulated_depreciation_value, goodwill_value)

    # Call the display_balance_sheet method
    balance_sheet.display_balance_sheet()

if __name__ == "__main__":
    main()
