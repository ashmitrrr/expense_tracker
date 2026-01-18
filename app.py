import streamlit as st
import pandas as pd
import os
from datetime import date
import plotly.express as px

# --- CONSTANTS ---
CSV_FILE = 'expenses.csv'
CATEGORIES = ['food', 'transport', 'rent', 'bills', 'health', 'other']

# budget goals 
BUDGETS = {
    'food': 300,
    'transport': 150,
    'rent': 1000,
    'bills': 200,
    'health': 100,
    'other': 100
}

# --- 1. DATA HANDLING ---
def load_data():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            if df.empty:
                return pd.DataFrame(columns=["date", "category", "amount", "description"])
            df['date'] = pd.to_datetime(df['date'])
            return df
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=["date", "category", "amount", "description"])
    else:
        return pd.DataFrame(columns=["date", "category", "amount", "description"])

def save_expense(date_input, category, amount, description):
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

# --- 2. NLP PARSER ---
def parse_smart_input(text):
    """
    Extracts amount and category, but KEEPS the keywords in the description
    so sentences remain readable.
    """
    tokens = text.split()
    amount = 0.0
    category = "other"
    description_words = []

    #Keyword Matching
    cat_keywords = {
        'food': ['food', 'burger', 'lunch', 'dinner', 'groceries', 'snack', 'mcdonalds', "mcdonald's", 'kfc', 'pizza', 'subway', 'coffee', 'starbucks'],
        'transport': ['uber', 'taxi', 'bus', 'train', 'gas', 'fuel', 'ticket', 'lyft'],
        'health': ['gym', 'doctor', 'meds', 'dentist', 'pharmacy'],
        'bills': ['wifi', 'electric', 'phone', 'bill', 'utilities'],
        'rent': ['rent', 'lease']
    }

    for token in tokens:
        # 1. Try to find the Amount (remove numbers from description)
        try:
            val = float(token)
            amount = val
            continue 
        except ValueError:
            pass

        # 2. Check for Category 
        lower_token = token.lower()
        for cat, keywords in cat_keywords.items():
            if lower_token in keywords or lower_token == cat:
                category = cat
                break
        description_words.append(token)

    # Clean up description
    description = " ".join(description_words).title()
    if not description:
        description = "General Expense"

    return amount, category, description

# --- 3. PAGE CONFIG ---
st.set_page_config(page_title="Expense Tracker AI", page_icon="💰", layout="wide")
st.title("💸 AI Expense Tracker")

# --- 4. SIDEBAR: SMART INPUT ---
with st.sidebar:
    st.header("Smart Add")
    st.caption("Try: 'Lunch 15' or 'Uber 25'")
    
    smart_text = st.text_input("Type expense here...")
    
    # Parse Logic
    parsed_amt, parsed_cat, parsed_desc = 0.0, "other", ""
    if smart_text:
        parsed_amt, parsed_cat, parsed_desc = parse_smart_input(smart_text)

    st.markdown("---")
    st.header("Verify & Save")
    
    with st.form("expense_form"):
        # Pre-fill widgets
        d_input = st.date_input("Date", date.today())
        
        # Handle Category Selection safely
        try:
            cat_index = CATEGORIES.index(parsed_cat)
        except ValueError:
            cat_index = 5 # Default to 'other'
            
        cat_input = st.selectbox("Category", CATEGORIES, index=cat_index)
        amt_input = st.number_input("Amount ($)", min_value=0.00, step=0.01, value=parsed_amt)
        desc_input = st.text_input("Description", value=parsed_desc)
        
        submitted = st.form_submit_button("Add Expense")
        
        if submitted:
            if amt_input > 0:
                save_expense(d_input, cat_input, amt_input, desc_input)
                st.success("Expense Added!")
                st.rerun()
    
    st.markdown("---") 
    st.caption("© 2026 Ashmit Raina")
    st.caption("built using streamlit, pandas, and plotly")

# --- 5. DASHBOARD ---
df = load_data()

if not df.empty:
    # --- BUDGET PROGRESS (Red Alert Logic) ---
    st.subheader("Budget Goals")
    
    b1, b2, b3 = st.columns(3)
    cols = [b1, b2, b3]
    
    cat_spend = df.groupby('category')['amount'].sum()
    
    for i, (cat, limit) in enumerate(BUDGETS.items()):
        spent = cat_spend.get(cat, 0)
        remaining = limit - spent
        percent = min(spent / limit, 1.0)
        
        col = cols[i % 3]
        
        with col:
            
            if remaining >= 0:
                delta_val = f"${remaining:.0f} left"
                bar_color = "#00c0f2" 
            else:
                delta_val = f"-${abs(remaining):.0f} over" # Explicit negative sign
                bar_color = "#ff4b4b" # Streamlit Red

            st.metric(label=cat.title(), value=f"${spent:.0f} / ${limit}", delta=delta_val)
            
            st.markdown(f"""
            <div style="width: 100%; background-color: #f0f2f6; border-radius: 5px; height: 8px;">
                <div style="width: {percent*100}%; background-color: {bar_color}; height: 8px; border-radius: 5px;"></div>
            </div>
            <br>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # --- CHARTS ---
    c1, c2 = st.columns([2, 1])

    with c1:
        st.subheader("Trends")
        df_sorted = df.sort_values(by="date")
        fig_trend = px.line(df_sorted, x='date', y='amount', title="Daily Spending", markers=True)
        st.plotly_chart(fig_trend, use_container_width=True)

    with c2:
        st.subheader("Breakdown")
        fig_pie = px.pie(df, values='amount', names='category', hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("History")
    st.dataframe(df.sort_values(by="date", ascending=False), use_container_width=True)

else:
    st.info("Welcome! Try typing 'Lunch 15' in the sidebar to start.")