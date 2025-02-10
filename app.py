import csv
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Set the Streamlit app to wide mode
st.set_page_config(layout="wide")

class CSV:
    date_format = "%d-%m-%Y"  # Date format used in the CSV file
    CSV_FILE = "finance_data.csv"  # Name of the CSV file
    columns = ["Date", "Amount", "Category", "Description"]  # Columns in the CSV file

    @classmethod
    def initialize_csv(cls):
        """Initialize the CSV file with the required columns if it doesn't exist."""
        try:
            # Try to read the CSV file to check if it exists
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            # If the file does not exist, create a new DataFrame with the specified columns
            df = pd.DataFrame(columns=cls.columns)
            # Save the DataFrame to a CSV file
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def entry_data(cls, date, amount, category, description):
        """Add a new entry to the CSV file."""
        # Create a dictionary for the new entry
        new_entry = {
            "Date": date,
            "Amount": amount,
            "Category": category,
            "Description": description
        }
        # Open the CSV file in append mode and write the new entry
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.columns)
            writer.writerow(new_entry)

    @classmethod
    def get_transactions(cls, start_date, end_date):
        """Retrieve transactions within the specified date range."""
        # Read the CSV file into a DataFrame
        df = pd.read_csv(cls.CSV_FILE)

        # Check if the 'Date' column exists in the DataFrame
        if 'Date' not in df.columns:
            st.error("The CSV file does not contain the 'Date' column.")
            return pd.DataFrame(columns=cls.columns)

        # Convert the 'Date' column to datetime format
        df["Date"] = pd.to_datetime(df["Date"], format=CSV.date_format)
        # Convert the start and end dates to datetime format
        start_date = datetime.strptime(start_date, CSV.date_format)
        end_date = datetime.strptime(end_date, CSV.date_format)

        # Create a mask to filter the DataFrame for the specified date range
        mask = (df["Date"] >= start_date) & (df["Date"] <= end_date)
        # Apply the mask to the DataFrame to get the filtered transactions
        filtered_df = df.loc[mask]

        return filtered_df

def plot_transaction(df):
    """Plot income and expenses over time using Matplotlib."""
    # Set the "Date" column as the index of the DataFrame
    df.set_index("Date", inplace=True)

    # Create a new DataFrame for income data
    income_df = df[df["Category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)

    # Create a new DataFrame for expense data
# Filter the original DataFrame to include only rows where "Category" is "Expense"
    # Resample the data to a daily frequency and sum the amounts for each day
    # Reindex the DataFrame to ensure it has the same index as the original DataFrame, filling missing dates with zeros
    expense_df = df[df["Category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)

    # Plotting the data using Matplotlib
    plt.figure(figsize=(10, 5))
    
    # Plotting the income data
# The x-axis values are the dates (index of income_df)
    # The y-axis values are the amounts from the "Amount" column of income_df
    # The label "INCOME" will be used in the plot legend
    # The color "g" (green) is used for the income line
    plt.plot(income_df.index, income_df["Amount"], label="INCOME", color="g")

    # Plotting the expense data
# The x-axis values are the dates (index of expense_df)
    # The y-axis values are the amounts from the "Amount" column of expense_df
    # The label "EXPENSE" will be used in the plot legend
    # The color "r" (red) is used for the expense line
    plt.plot(expense_df.index, expense_df["Amount"], label="EXPENSE", color="r")
    
    plt.xlabel("Date")
    plt.ylabel("Income and Expenses over Time")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

@st.fragment
def show_plot(df):
    """Show the plot button and plot the transaction data when clicked."""
    if st.button("Show Plot"):
        plot_transaction(df)

def main():
    """Main function to run the Streamlit app."""
    st.title("Personal Finance Tracker")

    # Sidebar content
    st.sidebar.title("Navigation")
    st.sidebar.markdown("Use the menu below to navigate through the app.")
    
    # Sidebar menu
    menu = ["🏠 Add Transaction", "📊 View Transactions and Summary"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Initialize the CSV file
    CSV.initialize_csv()

    if choice == "🏠 Add Transaction":
        st.subheader("Add New Transaction")
        date = st.date_input("Date")
        description = st.text_input("Description")
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        category = st.selectbox("Category", ["Income", "Expense"])
        if st.button("Add Entry"):
            CSV.entry_data(date.strftime(CSV.date_format), amount, category, description)
            st.success("Entry added successfully!")

    elif choice == "📊 View Transactions and Summary":
        st.subheader("View Transactions and Summary")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        if st.button("Show Transactions"):
            df = CSV.get_transactions(start_date.strftime(CSV.date_format), end_date.strftime(CSV.date_format))
            if not df.empty:
                st.write("### Transactions")
                st.dataframe(df)  # Display the DataFrame in a tabular format
                st.write("### Summary")
                total_income = df[df["Category"] == "Income"]["Amount"].sum()
                total_expense = df[df["Category"] == "Expense"]["Amount"].sum()
                st.write(f"**Total Income:** ₹{total_income:.2f}")
                st.write(f"**Total Expense:** ₹{total_expense:.2f}")
                st.write(f"**Net Savings:** ₹{(total_income - total_expense):.2f}")
                
                # Create two columns for income and expense DataFrames
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("### Income Data")
                    st.dataframe(df[df["Category"] == "Income"])
                
                with col2:
                    st.write("### Expense Data")
                    st.dataframe(df[df["Category"] == "Expense"])
                
                show_plot(df)  # Call the show_plot function to display the plot button and plot the data
            else:
                st.warning("No transactions found in the given date range.")

if __name__ == "__main__":
    main()