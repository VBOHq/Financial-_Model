import json
import requests
import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
from BalanceSheet import BalanceSheet
from BalanceSheetpro import BalanceSheetpro
from IncomeStatement import IncomeStatement


#logo
#st.sidebar.image("data/logo1.png", caption="Frozen Co.")
# Function to load Lottie file from file path
def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading Lottie file: {e}")
        return None

# Function to load Lottie file from URL
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error loading Lottie URL: {e}")
        return None

# Set background and sidebar styling
def set_bg_hack_url():
    st.markdown(
        """
        <style>
        .stApp {
            #background: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRwc-Md-aNgexxeW_h8ZBp_g3K3CiMaJm5tkIa7zyiGxyAZ23_30ErUUL_4GSDsxonDlxw&usqp=CAU");
            background-size: cover;
            background-repeat: no-repeat;
        }
        [data-testid=stSidebar] {
            #background-color: transparent;
            font-family: sans-serif;
            opacity: 0.7;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function to set the background
set_bg_hack_url()

# Main function to switch between pages
def main():
    st.sidebar.title("Navigation")
    page_options = ["Home", "BalanceSheet", "BalanceSheetpro", "IncomeStatement", "CashFlow"]
    choice = st.sidebar.selectbox("Select Page", page_options)

    if choice == "IncomeStatement":
        income_statement()
    elif choice == "BalanceSheet":
        balance_sheet()
    elif choice == "BalanceSheetpro":
        balance_sheets()   
    elif choice == "CashFlow":
        Cashflow()
    else:
        home()

def balance_sheet():
            
    st.sidebar.header("BalanceSheet Input", divider='rainbow')    
    
    # Collect user inputs for BalanceSheet parameters
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

    # Create an instance of BalanceSheet with user-provided values
    balance_sheet = BalanceSheet(
        assets,
        otherAsset_value,
        liabilities,
        equity,
        gross_ppe_value,
        accumulated_depreciation_value,
        goodwill_value,
    )

    # Add a button to trigger the calculation in the sidebar
    if st.sidebar.button("Calculate Balance Sheet"):
        # Call the display_balance_sheet method
        balance_sheet.display_balance_sheet()
    else:
        st.header("Balance Sheet Calculating Section")
        st.divider()
        # Load Lottie animations for the Home page
        
        lottie_coding = load_lottiefile("lottiefiles/coding.json")
        lottie_analysis = load_lottiefile("lottiefiles/analysis.json")

        # Display Lottie animations in columns
        col1, col2 = st.columns(2)
        with col2:
            st_lottie(
                lottie_analysis,
                speed=1,
                reverse=False,
                loop=True,
                quality="low",
                height=400,
                width=None,
                key=None,
            )
        with col1:
            st_lottie(
                lottie_coding,
                speed=1,
                reverse=False,
                loop=True,
                quality="low",
                height=400,
                width=None,
                key=None,
            )
        
        

        
# Function to calculate and display the projected balance sheet
def calculate_and_display_balance_sheets(assumptions, historical_data):
    balance_sheets = BalanceSheetpro(assumptions, historical_data)
    projected_balance_sheets = balance_sheets.calculate_all_line_items()
    
    st.subheader("Projected Balance Sheet:")
    st.write(projected_balance_sheets)
    
    # Return the projected balance sheet
    return projected_balance_sheets
        
def balance_sheets():
    # Input assumptions
    st.sidebar.header("Assumptions", divider='rainbow')
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
    
    
    


    # Upload historical data (assuming a CSV file for simplicity)
    uploaded_file = st.file_uploader("Upload Historical Data (CSV)", type=["csv"])
    if uploaded_file is not None:
        historical_data = pd.read_csv(uploaded_file)
        st.subheader("Historical Data:")
        st.write(historical_data)

        # Calculate and display the projected balance sheet
        calculate_and_display_balance_sheets(assumptions, historical_data)
        # Calculate and display the projected balance sheet
        projected_balance_sheet = calculate_and_display_balance_sheets(assumptions, historical_data)
        
        # Add download button
        st.download_button(
            label="Download Projected Balance Sheet",
            data=projected_balance_sheet.to_csv(index=False).encode(),
            file_name='projected_balance_sheets.csv',
            key='download_projected_balance_sheet'
        )

        

        
def home():
    
    st.sidebar.header("Home Section", divider='rainbow')
    countries = [
        "United States",
        "Canada",
        "United Kingdom  ",
        "Germany",
        "Nigeria",
        "France",
        "Japan",
        "Australia",
        "China",
        "India",
        "Brazil",
        "South Africa",
    ]

    # Create two columns, with 3/4 and 1/4 of the width
    col1, col2 = st.columns([3, 1])

    # Position the dropdown in the second column (col2) at the top right corner
    with col2:
        selected_country = st.selectbox(" ", countries)

    # Display the selected country in the first column (col1)
    with col1:
        st.write(" ", selected_country)
    
    st.header("Frozen Food Co. - Financial Model")
    st.divider()
    # Load Lottie animations for the Home page
    lottie_analysis = load_lottiefile("lottiefiles/analysis.json")
    lottie_animation = load_lottiefile("lottiefiles/animation.json")

    # Display Lottie animations in columns
    col1, col2 = st.columns(2)
    with col1:
        st_lottie(
            lottie_analysis,
            speed=1,
            reverse=False,
            loop=True,
            quality="low",
            height=400,
            width=None,
            key=None,
        )
    with col2:
        st_lottie(
            lottie_animation,
            speed=1,
            reverse=False,
            loop=True,
            quality="low",
            height=400,
            width=None,
            key=None,
        )

    st.write("This is the Home Page.")
    # Add specific content related to the Home Page here

def income_statement():
    st.sidebar.header("Assumptions", divider='rainbow')
    # Assumptions inputs
    assumptions = {}  # Initialize the assumptions dictionary
    
    with st.sidebar:
        st.subheader("Assumptions")
        col1, col2 = st.columns(2)

        # ... (complete the assumption inputs)
        # Column 1
        col1.text("Revenue Growth Rate")
        assumptions["Revenue Growth Rate"] = col1.number_input("rev_growth", min_value=0.0, value=0.05)

        col1.text("Depreciation as % of Gross PP&E")
        assumptions["Depreciation as % of Gross PP&E"] = col1.number_input("depreciation", min_value=0.0, value=0.02)

        col1.text("SG&A as % of Sales")
        assumptions["SG&A as % of Sales"] = col1.number_input("sga_sales", min_value=0.0, value=0.2)

        col1.text("Other Income / (Expense)")
        assumptions["Other Income / (Expense)"] = col1.number_input("other_income", min_value=0.0, value=0.0)

        col1.text("Days Accounts Receivable")
        assumptions["Days Accounts Receivable"] = col1.number_input("days_ar", min_value=0, value=30)

        col1.text("Other Current Assets")
        assumptions["Other Current Assets"] = col1.number_input("other_current_assets", min_value=0, value=1)

        col1.text("Capex as % of sales")
        assumptions["Capex as % of sales"] = col1.number_input("capex_percent", min_value=0.0, value=0.05)

        col1.text("Days Payable")
        assumptions["Days Payable"] = col1.number_input("days_payable", min_value=0, value=50)

        col1.text("Other Current Liabilities as % of COGS")
        assumptions["Other Current Liabilities as % of COGS"] = col1.number_input("other_liabilities_cogs", min_value=0.0, value=0.02)

        col1.text("Common Stock")
        assumptions["Common Stock"] = col1.number_input("common_stock", min_value=0, value=10)

        col1.text("Revolver")
        assumptions["Revolver"] = col1.number_input("revolver", min_value=0.0, value=0.03)

        col1.text("Unsecured Debt")
        assumptions["Unsecured Debt"] = col1.number_input("unsecured_debt", min_value=0.0, value=0.12)

        col1.text("Unsecured Debt Amortization")
        assumptions["Unsecured Debt Amortization"] = col1.number_input("unsecured_debt_amortization", min_value=0, value=0)

        # Column 2
        col2.text("COGS as % of Revenue")
        assumptions["COGS as % of Revenue"] = col2.number_input("cogs_percent", min_value=0.0, value=0.4)

        col2.text("Amortization")
        assumptions["Amortization"] = col2.number_input("amortization", min_value=0.0, value=0.0)

        col2.text("LIBOR")
        assumptions["LIBOR"] = col2.number_input("libor", min_value=0.0, max_value=1.0, value=0.01)

        col2.text("Tax Rate")
        assumptions["Tax Rate"] = col2.number_input("tax_rate", min_value=0.0, max_value=1.0, value=0.4)

        col2.text("Days Inventory")
        assumptions["Days Inventory"] = col2.number_input("days_inventory", min_value=0, value=45)

        col2.text("Other Assets")
        assumptions["Other Assets"] = col2.number_input("other_assets", min_value=0, value=0)

        col2.text("Asset Disposition")
        assumptions["Asset Disposition"] = col2.number_input("asset_disposition", min_value=0, value=0)

        col2.text("Term Loan")
        assumptions["Term Loan"] = col2.number_input("term_loan", min_value=0.0, value=0.035)

        col2.text("Term of Amortization")
        assumptions["Term of Amortization"] = col2.number_input("term_amortization", min_value=0, value=20)

        col2.text("Interest Earned On Cash")
        assumptions["Interest Earned On Cash"] = col2.number_input("interest_earned_on_cash", min_value=0.0, value=0.0063)

        col2.text("Empty Field (Ignore)")
        assumptions["Empty Field (Ignore)"] = col2.number_input("empty_field_ignore", min_value=0, max_value=1, value=0)



        calculate_button = st.button("Calculate")
        
    if calculate_button:
        try:
            # Read historical data from CSV file
            historical_data = pd.read_csv("historical_data.csv")

            # Calculate Financial Statement
            income_statement_obj = IncomeStatement(assumptions, historical_data)
            projected_income_statement = income_statement_obj.calculate_all_line_items()

            # Display Results
            st.subheader("Projected Financial Statement - Income Statement")
            st.dataframe(projected_income_statement.set_index("Year"))

            # Transpose and display historical data
            st.subheader("Historical Data - Transposed")
            st.dataframe(historical_data.T)

        except FileNotFoundError:
            st.error("Historical data file not found. Please make sure the file exists.")


        

if __name__ == "__main__":
    main()
