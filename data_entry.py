import pandas as pd
import csv
from datetime import datetime
from main import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt

class CSV:
    
    # defines a class attribute named CSV_FILE
    # a string that holds the name of the CSV file that the class will interact with.
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date","amount","category","description"]
    
    # since this is a class method, decorate it with @classmethod
    @classmethod
    def initialize_csv(cls):
        
        try:
            #  attempts to read the CSV file specified by CSV_FILE.
            pd.read_csv(cls.CSV_FILE)
            
        # exception handling
        # If the specified CSV file does not exist, the code inside this block will be executed.
        except FileNotFoundError:
            #  creates a new DataFrame with specified column names.
            df = pd.DataFrame(columns=cls.COLUMNS)
            # writes the DataFrame df to a CSV file.
            df.to_csv(cls.CSV_FILE, index = False)
    
    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date" : date,
            "amount" : amount,
            "category" : category,
            "description" : description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            # csv.DictWriter takes a dict and writes it into a csv file
            writer = csv.DictWriter(csvfile, fieldnames = cls.COLUMNS)
            writer.writerow(new_entry)
        print("\nEntry added successfully")
        
    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df['date'], format = "%d-%m-%Y")
        start_date = datetime.strptime(start_date, "%d-%m-%Y")
        end_date = datetime.strptime(end_date, "%d-%m-%Y")
        
        mask = (df["date"]>=start_date) & (df["date"]<=end_date)
        filtered_df = df.loc[mask]
        
        if filtered_df.empty:
            print("\nNo transactions found in the given date range")
        else:
            print(f"\nTransactions from {start_date.strftime("%d-%m-%Y")} to {end_date.strftime("%d-%m-%Y")} : \n")
            print(
                filtered_df.to_string(
                    index = False, 
                    formatters={"date": lambda x : x.strftime("%d-%m-%Y")}
                )
            )
            
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\nSummary : ")
            print(f"Total income : Rs.{total_income:.2f}")
            print(f"Total expense : Rs.{total_expense:.2f}")
            print(f"Savings : Rs.{(total_income - total_expense):.2f}")
        
        return filtered_df
            

def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of transaction  ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)
    

def plot_transactions(df):
    df.set_index("date", inplace=True)
    
    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(10,5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses over time")
    plt.legend()
    plt.grid(True)
    plt.show()




def main():
    while True:
        print("\n1 : Add new transaction")
        print("2 : View transactions and summary within a given date range")
        print("3 : Exit")
        choice = input("\nEnter choice : ")
        
        if choice == '1':
            add()
        elif choice == '2':
            start_date = input("Enter start date : ")
            end_date = input("Enter end date : ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to see a plot?  (y/n) ").lower() == "y":
                plot_transactions(df)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice")
            
            
if __name__ == "__main__":
    main()

# add()


# CSV.get_transactions("02-09-2024","04-09-2024")


# CSV.initialize_csv()
# # after running above code, a new csv file "finance_data.csv" is created with columns : date,amount,category,description

# CSV.add_entry("01-09-2024",200,"Income","Salary")
# CSV.add_entry("01-09-2024",350,"Income","Salary")
# CSV.add_entry("01-09-2024",30,"Expense","Snacks")
    