import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"  # This line for naming a file
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"  # formatting date style

    @classmethod  # CREATING A DECORATORS
    def initialize_csv(cls):  # This code is for creating a file if it does not exist
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)  # this will make the table
            # DataFrame -- object within pandas that allows us to access different rows/columns from a CSV file
            df.to_csv(cls.CSV_FILE, index=False)


    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:  # "a" for appending data and newline for adding a newline
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)  # this is for writing data/entry
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def delete_entry(cls, delete_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)
        delete_date = datetime.strptime(delete_date, cls.FORMAT)

        # Filter out rows with the delete_date
        df = df[df["date"] != delete_date]

        df["date"] = df["date"].dt.strftime(cls.FORMAT)  # convert back to string
        if len(df) < len(pd.read_csv(cls.CSV_FILE)):  # Check if any rows were deleted
            df.to_csv(cls.CSV_FILE, index=False)
            print(f"Entries for {delete_date.strftime(cls.FORMAT)} have been deleted.")
            return True
        else:
            print(f"No entries for {delete_date.strftime(cls.FORMAT)} to delete.")
            return False

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)  # convert all of the dates inside of the date column to a datetime object
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        # filter the dataframe to only include transactions between the start and end dates
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)  # & :- only being used when working with pandas dataframe or mask specifically
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the given date range")
        else:
            print(
                f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}"
            )
            print(
                filtered_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
                )
            )

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\n Summary")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Saving: ${(total_income - total_expense):.2f}")

        return filtered_df

    @classmethod
    def get_summary(cls):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)

        total_income = df[df["category"] == "Income"]["amount"].sum()
        total_expense = df[df["category"] == "Expense"]["amount"].sum()
        net_saving = total_income - total_expense

        # Monthly totals
        df["month"] = df["date"].dt.to_period("M")
        monthly_income = df[df["category"] == "Income"].groupby("month")["amount"].sum()
        monthly_expense = df[df["category"] == "Expense"].groupby("month")["amount"].sum()

        summary = {
            "Total Income": total_income,
            "Total Expense": total_expense,
            "Net Saving": net_saving,
            "Monthly Income": monthly_income,
            "Monthly Expense": monthly_expense
        }
        return summary


# ----------- plots --------------
def plot_summary_bar_chart(summary):
    months = [str(period) for period in summary["Monthly Income"].index]
    income_values = summary["Monthly Income"].values
    expense_values = summary["Monthly Expense"].reindex(months, fill_value=0).values

    fig, ax = plt.subplots(figsize=(12, 6))
    width = 0.4
    x = range(len(months))

    ax.bar(x, income_values, width=width, label='Income', color='green', align='center')
    ax.bar([p + width for p in x], expense_values, width=width, label='Expense', color='red', align='center')
    ax.set_xlabel('Month')
    ax.set_ylabel('Amount')
    ax.set_title('Monthly Income and Expense')
    ax.set_xticks([p + width / 2 for p in x])
    ax.set_xticklabels(months, rotation=45)
    ax.legend()
    plt.tight_layout()

    return fig


def plot_pie_chart(total_income, total_expense):
    labels = ['Income', 'Expense']
    sizes = [total_income, total_expense]
    colors = ['green', 'red']

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    ax.set_title('Income vs Expense')
    plt.tight_layout()

    return fig



def plot_transactions(df):
    df.set_index("date", inplace=True)
    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(income_df.index, income_df["amount"], label="Income", color="g")
    ax.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    ax.set_xlabel("Date")
    ax.set_ylabel("Amount")
    ax.set_title("Income & Expense Over Time")
    ax.grid(True)
    ax.legend()
    plt.tight_layout()
    
    return fig

def plot_net_saving_bar_chart(summary):
    months = [str(period) for period in summary["Monthly Income"].index]
    income_values = summary["Monthly Income"].values
    expense_values = summary["Monthly Expense"].reindex(months, fill_value=0).values
    net_saving_values = income_values - expense_values

    fig, ax = plt.subplots(figsize=(12, 6))
    width = 0.4
    x = range(len(months))

    ax.bar(x, net_saving_values, width=width, label='Net Saving', color='blue', align='center')
    ax.set_xlabel('Month')
    ax.set_ylabel('Amount')
    ax.set_title('Monthly Net Savings')
    ax.set_xticks([p + width / 2 for p in x])
    ax.set_xticklabels(months, rotation=45)
    ax.legend()
    plt.tight_layout()

    return fig

def plot_transactions_bar_chart(df):
    df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
    df.set_index("date", inplace=True)
    daily_totals = df.groupby(["date", "category"])["amount"].sum().unstack().fillna(0)

    fig, ax = plt.subplots(figsize=(12, 6))
    daily_totals.plot(kind="bar", stacked=True, ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("Amount")
    ax.set_title("Daily Transactions")
    ax.legend(title="Category")
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig
