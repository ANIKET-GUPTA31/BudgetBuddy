import streamlit as st
import pandas as pd
from datetime import datetime
from main import CSV, plot_summary_bar_chart, plot_pie_chart, plot_transactions, plot_net_saving_bar_chart, plot_transactions_bar_chart

# Ensure CSV file is initialized
CSV.initialize_csv()

# Function to format date
def format_date(date):
    return date.strftime("%d-%m-%Y")

# Sidebar for user inputs
st.sidebar.image("./logo/budgetbuddy_logo.png")
st.sidebar.header("BudgetBuddy")
option = st.sidebar.selectbox("Select an option", ["Add Transaction", "Delete Transaction", "View Transactions", "View Summary"])
st.sidebar.write("This project is a personal finance tracker that allows users to add, delete, and view transactions. It provides detailed summaries of income and expenses, including monthly bar charts and pie charts for visual insights. Users can also view transaction history over specified date ranges with graphical representations. The app uses Streamlit for a user-friendly interface and Matplotlib for visualizing financial data.")

if option == "Add Transaction":
    st.header("Add a New Transaction")
    
    date = st.date_input("Date", value=datetime.today())
    amount = st.number_input("Amount", min_value=1, step=1)
    category = st.selectbox("Category", ["Income", "Expense"])
    description = st.text_input("Description (optional)")
    
    if st.button("Add Transaction"):
        CSV.add_entry(format_date(date), amount, category, description)
        st.success("Transaction added successfully!")

elif option == "Delete Transaction":
    st.header("Delete a Transaction")
    delete_date = st.date_input("Enter The Date")
    if st.button("Delete Transaction"):
        result = CSV.delete_entry(format_date(delete_date))
        if result:
            st.success(f"Transaction for {format_date(delete_date)} deleted successfully!")
        else:
            st.warning(f"No entries for {format_date(delete_date)} to delete.")

elif option == "View Transactions":
    st.header("View Transactions")
    
    start_date = st.date_input("Start Date", value=datetime.today() - pd.DateOffset(days=30))
    end_date = st.date_input("End Date", value=datetime.today())
    
    if st.button("Get Transactions"):
        df = CSV.get_transactions(format_date(start_date), format_date(end_date))
        if not df.empty:
            st.write(df)
        else:
            st.info("No transactions found for the given date range.")

elif option == "View Summary":
    st.header("Finance Summary")
    summary = CSV.get_summary()  # Call the method on the class itself
    st.write(f"**Total Income:** ${summary['Total Income']:.2f}")
    st.write(f"**Total Expense:** ${summary['Total Expense']:.2f}")
    st.write(f"**Net Saving:** ${summary['Net Saving']:.2f}")

    # Plot the summary bar chart
    if st.button("Plot Monthly Transactions"): 
        st.header("Monthly Income and Expense")
        fig_bar = plot_summary_bar_chart(summary)
        st.pyplot(fig_bar)

        # Plot the net savings bar chart
        st.header("Monthly Net Savings")
        fig_net_saving = plot_net_saving_bar_chart(summary)
        st.pyplot(fig_net_saving)

        # Plot the pie chart
        st.header("Income vs Expense")
        fig_pie = plot_pie_chart(summary["Total Income"], summary["Total Expense"])
        st.pyplot(fig_pie)

    st.header("View Transactions Plot")
    start_date = st.date_input("Start Date for Plot", value=datetime.today() - pd.DateOffset(days=30))
    end_date = st.date_input("End Date for Plot", value=datetime.today())
    
    if st.button("Plot Transactions"):
        df = CSV.get_transactions(format_date(start_date), format_date(end_date))
        df2 = CSV.get_transactions(format_date(start_date), format_date(end_date))
        if not df.empty:
            fig_bar = plot_transactions_bar_chart(df)  # Updated to use bar chart function
            st.pyplot(fig_bar)

            fig = plot_transactions(df2)
            st.pyplot(fig)
        else:
            st.info("No transactions found for the given date range.")
