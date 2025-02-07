import pandas as pd
import matplotlib.pyplot as plt
import csv 
from datetime import datetime
from data_entry import get_amount,get_discription,get_category,get_date
class CSV :
    date_format="%d-%m-%Y"
    CSV_FILE ="finance_data.csv"
    columns=["Date","Amount","Category","Discription"]
    #initializing csv file
    @classmethod#this will have access to class itself but it wont have access to its instance 
    def initialize_csv(cls):
        try:
            #reading csv 
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            #creating file 
            df=pd.DataFrame(columns=cls.columns)
            #exporting to csv file 
            df.to_csv(cls.CSV_FILE,index=False)
    @classmethod
    #entering data 
    def entry_data(cls,date,amount,category,discription):
        #dictionary
        new_entry ={
            "Date":date,
            "Amount" : amount,
            "Category":category,
            "Discription":discription
        }
        #context manager
        with open(cls.CSV_FILE,"a",newline="") as csvfile:#opening the file in append mode . automatically close after writing
            #csv writer object
            writer = csv.DictWriter(csvfile,fieldnames=cls.columns)#take a dictionary and write it into the csv file .
            writer.writerow(new_entry)
            print("entry added successfully")

    @classmethod
        #getting transactions in a range
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["Date"] = pd.to_datetime(df["Date"], format=CSV.date_format)
        start_date = datetime.strptime(start_date, CSV.date_format)
        end_date = datetime.strptime(end_date, CSV.date_format)

        mask = (df["Date"] >= start_date) & (df["Date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the given date range.")
        else:
            print(
                f"Transactions from {start_date.strftime(CSV.date_format)} to {end_date.strftime(CSV.date_format)}"
            )
            print(
                filtered_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(CSV.date_format)}
                )
            )

            total_income = filtered_df[filtered_df["Category"] == "Income"]["Amount"].sum()
            total_expense = filtered_df[filtered_df["Category"] == "Expense"]["Amount"].sum()
            print("\nSummary:")
            print(f"Total Income: ₹{total_income:.2f}")
            print(f"Total Expense: ₹{total_expense:.2f}")
            print(f"Net Savings: ₹{(total_income - total_expense):.2f}")

        return filtered_df

# #collecting data
def add():
    CSV.initialize_csv()
    date=get_date("Enter the date of transaction or press enter for todays date :",allow_default=True)
    amount=get_amount()
    category=get_category()
    discription=get_discription()
    #adding data to csv file
    CSV.entry_data(date,amount,category,discription)

#ploting graph 
def plot_transaction(df):
    df.set_index("Date",inplace = True)
    #income dataframe 
    income_df =df[df["Category"]=="Income"].resample("D").sum().reindex(df.index,fill_value=0)#fliter df as there is an entry forall missing dates as empty
    expense_df =df[df["Category"]=="Expense"].resample("D").sum().reindex(df.index,fill_value=0)

    #setting frame 
    plt.figure(figsize=(10,5))
    plt.plot(income_df.index,income_df["Amount"],label ="INCOME ", color ="g")
    plt.plot(expense_df.index,expense_df["Amount"],label ="Expense  ", color ="r")
    plt.xlabel("Date")
    plt.ylabel("Income and Expenses over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    while True :
                
        print("1.Add new transaction.")
        print("2.View transaction and summary within range .")
        print("3.Exit")
        choice=input("Enter the choice (1-3) : ")
        if choice =='1' :
            add()
        elif choice =='2':
            start_date=get_date("Enter the start date (dd-mm-yyyy) : ")
            end_date=get_date("Enter the start date (dd-mm-yyyy) : ")
            df=CSV.get_transactions(start_date,end_date)
            if input("Do you want to see a plot (Y or N) : " ).lower()=='y':
                plot_transaction(df)
        elif choice =='3':
            print("Exiting.....")
            break
        else:
            print("Invalid choice. Enter 1 or 2 or 3 : ")

if __name__=="__main__":
    main()