import csv
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class CSV:
    date_format = "%d-%m-%Y"  # Date format used in the CSV file
    CSV_FILE = "finance_data.csv"  # Name of the CSV file
    columns = ["Date", "Amount", "Category", "Description"]  # Columns in the CSV file

    @classmethod
    def initialize_csv(cls):
        """Initialize the CSV file with the required columns if it doesn't exist."""
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.columns)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def entry_data(cls, date, amount, category, description):
        """Add a new entry to the CSV file."""
        new_entry = {
            "Date": date,
            "Amount": amount,
            "Category": category,
            "Description": description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.columns)
            writer.writerow(new_entry)

    @classmethod
    def get_transactions(cls, start_date, end_date):
        """Retrieve transactions within the specified date range."""
        df = pd.read_csv(cls.CSV_FILE)

        if 'Date' not in df.columns:
            st.error("The CSV file does not contain the 'Date' column.")
            return pd.DataFrame(columns=cls.columns)

        df["Date"] = pd.to_datetime(df["Date"], format=CSV.date_format)
        start_date = datetime.strptime(start_date, CSV.date_format)
        end_date = datetime.strptime(end_date, CSV.date_format)

        mask = (df["Date"] >= start_date) & (df["Date"] <= end_date)
        filtered_df = df.loc[mask]

        return filtered_df

def plot_transaction(df):
    """Plot income and expenses over time."""
    st.write("Plotting data...")  # Debug statement
    st.write(df)  # Debug statement to show the DataFrame

    # Set the "Date" column as the index of the DataFrame
    df.set_index("Date", inplace=True)

    # Create a new DataFrame for income data
    # Filter the original DataFrame to include only rows where "Category" is "Income"
    # Resample the data to a daily frequency and sum the amounts for each day
    # Reindex the DataFrame to ensure it has the same index as the original DataFrame, filling missing dates with zeros
    income_df = df[df["Category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)

    # Create a new DataFrame for expense data
    # Filter the original DataFrame to include only rows where "Category" is "Expense"
    # Resample the data to a daily frequency and sum the amounts for each day
    # Reindex the DataFrame to ensure it has the same index as the original DataFrame, filling missing dates with zeros
    expense_df = df[df["Category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)

    st.write("Income DataFrame:")  # Debug statement
    st.write(income_df)  # Debug statement to show the income DataFrame
    st.write("Expense DataFrame:")  # Debug statement
    st.write(expense_df)  # Debug statement to show the expense DataFrame

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

def main():
    """Main function to run the Streamlit app."""
    st.title("Personal Finance Tracker")

    # Sidebar menu
    menu = ["Add Transaction", "View Transactions and Summary"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Initialize the CSV file
    CSV.initialize_csv()

    if choice == "Add Transaction":
        st.subheader("Add New Transaction")
        date = st.date_input("Date")
        description = st.text_input("Description")
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        category = st.selectbox("Category", ["Income", "Expense"])
        if st.button("Add Entry"):
            CSV.entry_data(date.strftime(CSV.date_format), amount, category, description)
            st.success("Entry added successfully!")

    elif choice == "View Transactions and Summary":
        st.subheader("View Transactions and Summary")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        if st.button("Show Transactions"):
            df = CSV.get_transactions(start_date.strftime(CSV.date_format), end_date.strftime(CSV.date_format))
            if not df.empty:
                st.write(df)
                total_income = df[df["Category"] == "Income"]["Amount"].sum()
                total_expense = df[df["Category"] == "Expense"]["Amount"].sum()
                st.write(f"Total Income: ₹{total_income:.2f}")
                st.write(f"Total Expense: ₹{total_expense:.2f}")
                st.write(f"Net Savings: ₹{(total_income - total_expense):.2f}")
                if st.button("Show Plot"):
                    plot_transaction(df)
            else:
                st.warning("No transactions found in the given date range.")

if __name__ == "__main__":
    main()