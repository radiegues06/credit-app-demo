import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Fintech Credit Analytics", layout="wide", page_icon="💳")

# Connect to database
DB_PATH = "database/ume_finops.db"

@st.cache_data
def load_data(query):
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Load Marts
portfolio_df = load_data("SELECT * FROM portfolio_metrics")
reconciliation_df = load_data("SELECT * FROM reconciliation_metrics")
collection_df = load_data("SELECT * FROM collection_metrics")
vintage_df = load_data("SELECT * FROM vintage_default_metrics")
transactions_df = load_data("SELECT * FROM fct_credit_transactions")
client_risk_df = load_data("SELECT * FROM client_risk_metrics")
clients_sample_df = load_data("SELECT * FROM stg_clients LIMIT 10")
recon_detail_df = load_data("SELECT * FROM mart_reconciliation_detail")

# Title
st.title("💳 Fintech Credit Portfolio Dashboard")
st.markdown("Monitor outstanding credit, portfolio health, and collections reconciliation.")

# Section 1 - Portfolio Health
st.header("1. Portfolio Health")

if not portfolio_df.empty:
    metrics = portfolio_df.iloc[0]
    
    # Alert System
    if metrics['par90'] > 0.08:
        st.error(f"🚨 ALERT: PAR90 has exceeded the 8% risk threshold! Current: {metrics['par90']*100:.2f}%")
        
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Outstanding Portfolio", f"R$ {metrics['outstanding_principal']:,.2f}")
    c2.metric("PAR30", f"{metrics['par30']*100:.2f}%")
    c3.metric("PAR90", f"{metrics['par90']*100:.2f}%")
    c4.metric("Average Ticket", f"R$ {metrics['average_ticket']:,.2f}")
else:
    st.info("No portfolio metrics available.")

st.divider()

# Section 2 - Portfolio Evolution
st.header("2. Portfolio Evolution")
if not transactions_df.empty:
    evolution_df = transactions_df.groupby('origination_month')['purchase_value'].sum().reset_index()
    fig1 = px.line(evolution_df, x='origination_month', y='purchase_value', title="Originated Volume by Month", markers=True)
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.info("No transaction data available.")

st.divider()

# Section 3 - Vintage Default Curve
st.header("3. Vintage Default Curve")
if not vintage_df.empty:
    fig2 = px.line(vintage_df, x='origination_month', y='default_rate', title="Default Rate by Origination Cohort", markers=True)
    fig2.update_yaxes(tickformat=".2%")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No vintage default data available.")
    
st.divider()

# Section 4 - Collections
st.header("4. Collections")
if not collection_df.empty:
    col = collection_df.iloc[0]
    c1, c2 = st.columns(2)
    # Simple bar chart
    expected = col['expected_collection']
    actual = col['actual_collection']
    
    df_bar = pd.DataFrame({
        "Type": ["Expected Collection", "Actual Collection"],
        "Amount": [expected, actual]
    })
    
    fig3 = px.bar(df_bar, x="Type", y="Amount", title="Collections Performance", color="Type")
    # c1 metric
    c1.metric("Collection Rate", f"{col['collection_rate']*100:.2f}%")
    c2.plotly_chart(fig3, use_container_width=True)
else:
    st.info("No collection data available.")
    
st.divider()

# Section 5 - Reconciliation Monitoring
st.header("5. Reconciliation Monitoring")
if not reconciliation_df.empty:
    rec = reconciliation_df.iloc[0]
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Reconciliation Rate", f"{rec['reconciliation_rate']*100:.2f}%")
    c2.metric("Unmatched Payments", f"{int(rec['unmatched_payments'])}")
    c3.metric("Difference (Expected vs Settled)", f"R$ {rec['difference']:,.2f}")
# Section 6 - Client Risk Analysis
st.header("6. Client Risk Analysis")

if not client_risk_df.empty:
    c1, c2 = st.columns(2)
    
    # Sort by risk class for better visualization
    risk_order = ['A', 'B', 'C', 'D', 'E']
    client_risk_df['client_credit_risk'] = pd.Categorical(client_risk_df['client_credit_risk'], categories=risk_order, ordered=True)
    client_risk_df = client_risk_df.sort_values('client_credit_risk')
    
    # Chart 1: Total Financed per Risk Class
    fig4 = px.bar(client_risk_df, x='client_credit_risk', y='total_financed', 
                  title="Total Financed Value per Risk Class",
                  color='client_credit_risk',
                  labels={'client_credit_risk': 'Credit Risk Tier', 'total_financed': 'Total Financed (R$)'})
    c1.plotly_chart(fig4, use_container_width=True)
    
    # Chart 2: Default Rate per Risk Class
    fig5 = px.line(client_risk_df, x='client_credit_risk', y='default_rate', 
                   title="Default Rate per Risk Class", markers=True,
                   labels={'client_credit_risk': 'Credit Risk Tier', 'default_rate': 'Default Rate'})
    fig5.update_yaxes(tickformat=".2%")
    c2.plotly_chart(fig5, use_container_width=True)
    
    # Summary Table
    st.subheader("Risk Metrics Summary")
    st.dataframe(client_risk_df, use_container_width=True)
    
    # Clients Sample
    st.subheader("Sample Clients (Demographics & Risk)")
    if not clients_sample_df.empty:
        st.dataframe(clients_sample_df, use_container_width=True)
else:
    st.info("No client risk metrics available.")

# Section 7 - Transaction History Lookup
st.header("7. Transaction History Lookup")

if not recon_detail_df.empty:
    tx_ids = recon_detail_df['transaction_id'].unique().tolist()
    selected_tx = st.selectbox("Select a Transaction ID to drill-down", options=[""] + tx_ids)
    
    if selected_tx:
        st.subheader(f"History for Transaction: {selected_tx}")
        tx_history = recon_detail_df[recon_detail_df['transaction_id'] == selected_tx].sort_values('installment_number')
        
        # Quick summary metrics for the transaction
        t_info = tx_history.iloc[0]
        c1, c2, c3 = st.columns(3)
        c1.metric("Date", str(t_info['transaction_date']))
        c2.metric("Total Value", f"R$ {t_info['purchase_value']:.2f}")
        c3.metric("Installments", f"{int(tx_history['installment_number'].max())}")
        
        # Detailed audit trail table
        st.write("Full Audit Trail (Installments → Payments → Settlements)")
        # Select and rename columns for readability
        display_cols = {
            'installment_number': 'Ins #',
            'due_date': 'Due Date',
            'expected_installment_amount': 'Expected (R$)',
            'installment_status': 'Inst. Status',
            'paid_amount': 'Paid (R$)',
            'payment_date': 'Paid Date',
            'settled_amount': 'Settled (R$)',
            'reconciliation_status': 'Recon. Status',
            'bank_reference': 'Bank Ref'
        }
        st.dataframe(tx_history[list(display_cols.keys())].rename(columns=display_cols), use_container_width=True)
    else:
        st.info("Select a transaction ID from the list to see its full lifecycle.")
else:
    st.info("No reconciliation detail data available.")

st.divider()

st.caption("Auto-generated by UME FinOps pipeline.")
