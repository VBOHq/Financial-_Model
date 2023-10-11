
import streamlit as st
import pandas as pd

class IncomeStatement:
    
    def __init__(self, assumptions, historical_data):
        self.assumptions = assumptions
        self.historical_data = historical_data
        
    def calculate_revenue(self):
        # Calculate revenue based on the revenue growth rate
        revenue_growth = self.assumptions["Revenue Growth Rate"]
        last_year_revenue = self.historical_data["Revenue"].iloc[-1]
        projected_years = [
            self.historical_data["Year"].iloc[-1] + i for i in range(1, 6)
        ]
        projected_revenue = [
            last_year_revenue * (1 + revenue_growth) ** i for i in range(1, 6)
        ]

        return pd.DataFrame({"Year": projected_years, "Revenue": projected_revenue})
    
    def calculate_cogs(self):
        # Calculate COGS based on revenue and COGS as % of Revenue
        revenue_df = self.calculate_revenue()
        projected_cogs = [
            revenue_df["Revenue"].iloc[i] * self.assumptions["COGS as % of Revenue"]
            for i in range(5)
        ]
        return pd.DataFrame(
            {
                "Year": revenue_df["Year"],
                "Cost of Goods Sold (COGS)": projected_cogs,
            }
        )
        
    def calculate_gross_profit(self):
        revenue = self.calculate_revenue()["Revenue"]
        cogs = self.calculate_cogs()["Cost of Goods Sold (COGS)"]
        gross_profit = revenue.subtract(cogs)

        return pd.DataFrame(
            {"Year": self.calculate_revenue()["Year"], "Gross Profit": gross_profit}
        )
        
    def calculate_sga_expenses(self):
        revenue = self.calculate_revenue()["Revenue"]
        sga_expenses = revenue * self.assumptions["SG&A as % of Sales"]

        return pd.DataFrame(
            {"Year": self.calculate_revenue()["Year"], "SG&A Expenses": sga_expenses}
        )
        
    def calculate_operating_income(self):
        gross_profit = self.calculate_gross_profit()["Gross Profit"]
        sga_expenses = self.calculate_sga_expenses()["SG&A Expenses"]
        operating_income = gross_profit - sga_expenses

        return pd.DataFrame(
            {
                "Year": self.calculate_revenue()["Year"],
                "Operating Income": operating_income,
            }
        )
        
    def calculate_interest_expense(self):
        net_debt = (
            self.historical_data["Total Liabilities"] - self.historical_data["Cash"]
        )
        interest_expense = net_debt * self.assumptions["LIBOR"]

        return pd.DataFrame(
            {
                "Year": self.calculate_revenue()["Year"],
                "Interest Expense": interest_expense,
            }
        )
        
    def calculate_net_income(self):
        operating_income = self.calculate_operating_income()["Operating Income"]
        interest_expense = self.calculate_interest_expense()["Interest Expense"]
        other_income_expense = self.historical_data["Other Income / (Expense)"].iloc[-1]
        taxes = (
            operating_income - interest_expense + other_income_expense
        ) * self.assumptions["Tax Rate"]
        net_income = operating_income - interest_expense + other_income_expense - taxes

        return pd.DataFrame(
            {"Year": self.calculate_revenue()["Year"], "Net Income": net_income}
        )
    # ... (rest of the code)

    def calculate_all_line_items(self):
        # Calculate all line items in a single DataFrame
        projected_data = self.calculate_revenue()

        # Calculate COGS
        projected_data["Cost of Goods Sold (COGS)"] = (
            projected_data["Revenue"] * self.assumptions["COGS as % of Revenue"]
        )

        # Calculate Gross Profit
        projected_data["Gross Profit"] = (
            projected_data["Revenue"] - projected_data["Cost of Goods Sold (COGS)"]
        )

        # Calculate SG&A Expenses
        projected_data["SG&A Expenses"] = (
            projected_data["Revenue"] * self.assumptions["SG&A as % of Sales"]
        )

        # Calculate Operating Income
        projected_data["Operating Income"] = (
            projected_data["Gross Profit"] - projected_data["SG&A Expenses"]
        )

        # Calculate Interest Expense
        net_debt = (
            self.historical_data["Total Liabilities"] - self.historical_data["Cash"]
        )
        projected_data["Interest Expense"] = net_debt * self.assumptions["LIBOR"]

        # Calculate Net Income
        other_income_expense = self.historical_data["Other Income / (Expense)"].iloc[-1]
        taxes = (
            projected_data["Operating Income"]
            - projected_data["Interest Expense"]
            + other_income_expense
        ) * self.assumptions["Tax Rate"]
        projected_data["Net Income"] = (
            projected_data["Operating Income"]
            - projected_data["Interest Expense"]
            + other_income_expense
            - taxes
        )

        return projected_data


        # ... (unchanged)

def get_assumptions():
    
    assumptions = {}  # Initialize the assumptions dictionary
    with st.sidebar:
        st.subheader("Assumptions")
        col1, col2 = st.columns(2)
        
        

        # Column 1
        col1.text("Revenue Growth Rate")
        assumptions["Revenue Growth Rate"] = col1.number_input("##rev_growth", min_value=0.0, value=0.05)

        col1.text("Depreciation as % of Gross PP&E")
        assumptions["Depreciation as % of Gross PP&E"] = col1.number_input("##depreciation", min_value=0.0, value=0.02)

        col1.text("SG&A as % of Sales")
        assumptions["SG&A as % of Sales"] = col1.number_input("##sga_sales", min_value=0.0, value=0.2)

        col1.text("Other Income / (Expense)")
        assumptions["Other Income / (Expense)"] = col1.number_input("##other_income", min_value=0.0, value=0.0)

        col1.text("Days Accounts Receivable")
        assumptions["Days Accounts Receivable"] = col1.number_input("##days_ar", min_value=0, value=30)

        col1.text("Other Current Assets")
        assumptions["Other Current Assets"] = col1.number_input("##other_current_assets", min_value=0, value=1)

        col1.text("Capex as % of sales")
        assumptions["Capex as % of sales"] = col1.number_input("##capex_percent", min_value=0.0, value=0.05)

        col1.text("Days Payable")
        assumptions["Days Payable"] = col1.number_input("##days_payable", min_value=0, value=50)

        col1.text("Other Current Liabilities as % of COGS")
        assumptions["Other Current Liabilities as % of COGS"] = col1.number_input("##other_liabilities_cogs", min_value=0.0, value=0.02)

        col1.text("Common Stock")
        assumptions["Common Stock"] = col1.number_input("##common_stock", min_value=0, value=10)

        col1.text("Revolver")
        assumptions["Revolver"] = col1.number_input("##revolver", min_value=0.0, value=0.03)

        col1.text("Unsecured Debt")
        assumptions["Unsecured Debt"] = col1.number_input("##unsecured_debt", min_value=0.0, value=0.12)

        col1.text("Unsecured Debt Amortization")
        assumptions["Unsecured Debt Amortization"] = col1.number_input("##unsecured_debt_amortization", min_value=0, value=0)

        # Column 2
        col2.text("COGS as % of Revenue")
        assumptions["COGS as % of Revenue"] = col2.number_input("##cogs_percent", min_value=0.0, value=0.4)

        col2.text("Amortization")
        assumptions["Amortization"] = col2.number_input("##amortization", min_value=0.0, value=0.0)

        col2.text("LIBOR")
        assumptions["LIBOR"] = col2.number_input("##libor", min_value=0.0, max_value=1.0, value=0.01)

        col2.text("Tax Rate")
        assumptions["Tax Rate"] = col2.number_input("##tax_rate", min_value=0.0, max_value=1.0, value=0.4)

        col2.text("Days Inventory")
        assumptions["Days Inventory"] = col2.number_input("##days_inventory", min_value=0, value=45)

        col2.text("Other Assets")
        assumptions["Other Assets"] = col2.number_input("##other_assets", min_value=0, value=0)

        col2.text("Asset Disposition")
        assumptions["Asset Disposition"] = col2.number_input("##asset_disposition", min_value=0, value=0)

        col2.text("Term Loan")
        assumptions["Term Loan"] = col2.number_input("##term_loan", min_value=0.0, value=0.035)

        col2.text("Term of Amortization")
        assumptions["Term of Amortization"] = col2.number_input("##term_amortization", min_value=0, value=20)

        col2.text("Interest Earned On Cash")
        assumptions["Interest Earned On Cash"] = col2.number_input("##interest_earned_on_cash", min_value=0.0, value=0.0063)

        col2.text("Empty Field (Ignore)")
        assumptions["Empty Field (Ignore)"] = col2.number_input("##empty_field_ignore", min_value=0, max_value=1, value=0)

    
        
        

    # ... (unchanged)

    return assumptions

def get_historical_data():
    st.sidebar.subheader("Upload Historical Data")
    uploaded_file = st.sidebar.file_uploader("Upload Historical Data (CSV)", type=["csv"])

    if uploaded_file is not None:
        try:
            historical_data = pd.read_csv(uploaded_file)
        except pd.errors.EmptyDataError:
            st.error("The uploaded CSV file is empty.")
            return pd.DataFrame()  # Return an empty DataFrame in case of an error
    else:
        # Use a configurable default file path or allow users to specify their default file
        st.warning("No historical data file uploaded. Using default file.")
        historical_data = pd.read_csv("default_historical_data.csv")

    return historical_data

def display_projected_income_statement(income_statement, historical_data):
    # Display the projected data
    projected_income_statement = income_statement.calculate_all_line_items()
    st.header("Projected Income Statement:")
    st.dataframe(projected_income_statement)

    # Display historical data
    transposed_data = historical_data.T
    st.subheader("Transposed Historical Data")
    st.dataframe(transposed_data)

def main():
    st.title("Financial Projection App")

    # Get user inputs for assumptions and historical data
    assumptions = get_assumptions()
    historical_data = get_historical_data()

    # Check if historical_data is not empty before proceeding
    if historical_data.empty:
        st.warning("No historical data available or the file structure is incorrect.")
        st.text("Please make sure the uploaded CSV file has the correct structure.")
    else:
        # Apply the input data
        income_statement = IncomeStatement(assumptions, historical_data)

        # Calculate Financial Statement
        income_statement.calculate_cogs()  # Ensure COGS is calculated first
        income_df = income_statement.calculate_net_income()

        # Display Results
        display_projected_income_statement(income_statement, historical_data)



if __name__ == "__main__":
    main()
