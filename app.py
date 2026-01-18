import streamlit as st
import pandas as pd
import os
from datetime import date
import plotly.express as px  


CSV_FILE = 'expenses.csv'
CATEGORIES = ['food', 'transport', 'rent', 'bills', 'health', 'other']

# --- 1. DATA HANDLING ---
def load_data():
    """Loads the CSV into a Pandas DataFrame."""
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df['date'] = pd.to_datetime(df['date'])
        return df
    else:
        return pd.DataFrame(columns=["date", "category", "amount", "description"])

def save_expense(date_input, category, amount, description):
    """Saves a new single expense to the CSV."""
    new_data = pd.DataFrame({
        "date": [date_input],
        "category": [category],
        "amount": [amount],
        "description": [description]
    })
    
    if os.path.exists(CSV_FILE):
    
        new_data.to_csv(CSV_FILE, mode='a', header=False, index=False)
    else:
    
        new_data.to_csv(CSV_FILE, mode='w', header=True, index=False)

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="Expense Tracker V3", page_icon="💰", layout="wide")
st.title("Expense Tracker V3")
st.markdown("### The evolution: CLI → Pandas → Interactive Dashboard")

# --- 3. SIDEBAR: ADD EXPENSE (v1) ---
with st.sidebar:
    st.header("Add New Expense")
    
    with st.form("expense_form"):
       
        d_input = st.date_input("Date", date.today())
        cat_input = st.selectbox("Category", CATEGORIES)
        amt_input = st.number_input("Amount ($)", min_value=0.01, step=0.01)
        desc_input = st.text_input("Description (Optional)")
        
        submitted = st.form_submit_button("Add Expense")
        
        if submitted:
            if amt_input > 0:
                save_expense(d_input, cat_input, amt_input, desc_input)
                st.success("Expense Added!")

                st.rerun() 
            else:
                st.error("Amount must be greater than 0.")

# --- 4. DASHBOARD (v2) ---
df = load_data()

if not df.empty:
    total_spent = df['amount'].sum()
    
    avg_expense = df['amount'].mean()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Spent", f"${total_spent:.2f}")
    col2.metric("Average Transaction", f"${avg_expense:.2f}")
    col3.metric("Total Transactions", len(df))

    st.markdown("---")
    c1, c2 = st.columns([2, 1])

    with c1:
        st.subheader("📈 Spending Trend")
        
        df_sorted = df.sort_values(by="date")
        fig_trend = px.line(df_sorted, x='date', y='amount', title="Spending Over Time", markers=True)
        st.plotly_chart(fig_trend, use_container_width=True)

    with c2:
        st.subheader("Category Breakdown")
        category_total = df.groupby('category')['amount'].sum().reset_index()
        fig_pie = px.pie(category_total, values='amount', names='category', hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Recent Expenses")
    st.dataframe(df.sort_values(by="date", ascending=False), use_container_width=True)

else:
    st.info("No expenses found. Add your first expense in the sidebar to get started!")