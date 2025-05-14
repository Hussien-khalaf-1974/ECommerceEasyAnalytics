# import streamlit as st
# import pandas as pd
# import plotly.express as px

# st.set_page_config(page_title="E-Commerce & Customer Analysis", layout="wide")
# st.title("E-Commerce & Customer Analysis Dashboard")

# # Check for tables in session state
# required_tables = ['Order_Details', 'Orders', 'Customer_Sessions', 'Products', 'Customers', 'Returns', 'Shipping']
# if 'tables' not in st.session_state or any(st.session_state['tables'][table] is None for table in required_tables):
#     st.warning("⚠️ Please upload data from the Home page first.")
#     st.stop()

# # Load required tables
# order_details = st.session_state['tables']['Order_Details']
# orders_df = st.session_state['tables']['Orders']
# sessions_df = st.session_state['tables']['Customer_Sessions']
# products_df = st.session_state['tables']['Products']
# customers_df = st.session_state['tables']['Customers']
# returns_df = st.session_state['tables']['Returns']
# shipping_df = st.session_state['tables']['Shipping']

# if any(df is None for df in [order_details, orders_df, sessions_df, products_df, customers_df, returns_df, shipping_df]):
#     st.error("⚠️ One or more required tables is None. Please ensure data is loaded correctly.")
#     st.write("Session state tables:", list(st.session_state['tables'].keys()))
#     st.stop()

# # Validate Order_Details columns
# required_columns = ['product_id', 'added_date']
# if not all(col in order_details.columns for col in required_columns):
#     st.error(f"Missing required columns in Order_Details: {', '.join(set(required_columns) - set(order_details.columns))}")
#     st.stop()

# # Convert 'added_date' to datetime if needed
# if not pd.api.types.is_datetime64_any_dtype(order_details['added_date']):
#     try:
#         order_details['added_date'] = pd.to_datetime(order_details['added_date'])
#     except Exception as e:
#         st.error(f"Failed to convert 'added_date' to datetime: {e}")
#         st.stop()

# # Filter Data (Shared for all chapters)
# st.subheader("Filter Data")
# start_date = st.date_input("Start Date", orders_df['order_date'].min())
# end_date = st.date_input("End Date", orders_df['order_date'].max())
# filtered_orders = orders_df[(orders_df['order_date'] >= pd.Timestamp(start_date)) & (orders_df['order_date'] <= pd.Timestamp(end_date))]
# filtered_sessions = sessions_df[(sessions_df['session_start'] >= pd.Timestamp(start_date)) & (sessions_df['session_end'] <= pd.Timestamp(end_date))]
# filtered_returns = returns_df[returns_df['order_id'].isin(filtered_orders['id'])]
# filtered_shipping = shipping_df[shipping_df['order_id'].isin(filtered_orders['id'])]

# # Chapter 1: E-Commerce KPIs
# st.subheader("Chapter 1: E-Commerce KPIs")

# # KPI Calculations with filtered data
# total_visitors = filtered_sessions['customer_id'].nunique()
# completed_orders = filtered_orders[filtered_orders['status'].isin(['completed', 'shipped'])]['id'].nunique()
# conversion_rate = (completed_orders / total_visitors) * 100 if total_visitors > 0 else 0

# total_revenue = filtered_orders[filtered_orders['status'].isin(['completed', 'shipped'])]['total_amount'].sum()
# total_orders = completed_orders
# aov = total_revenue / total_orders if total_orders > 0 else 0

# total_customers = filtered_orders['customer_id'].nunique()
# returning_customers = filtered_orders['customer_id'].value_counts()[filtered_orders['customer_id'].value_counts() > 1].count()
# repeat_purchase_rate = (returning_customers / total_customers) * 100 if total_customers > 0 else 0

# purchase_frequency = filtered_orders['customer_id'].value_counts().mean()
# customer_orders = filtered_orders.groupby('customer_id')['order_date'].agg(['min', 'max'])
# customer_lifespan = (customer_orders['max'] - customer_orders['min']).mean().days / 365
# clv = aov * purchase_frequency * customer_lifespan if aov > 0 and purchase_frequency > 0 and customer_lifespan > 0 else 0

# min_date = filtered_orders['order_date'].min()
# max_date = filtered_orders['order_date'].max()
# midpoint = min_date + (max_date - min_date) / 2
# customers_start = filtered_orders[filtered_orders['order_date'] < midpoint]['customer_id'].nunique()
# customers_end = filtered_orders[filtered_orders['order_date'] >= midpoint]['customer_id'].nunique()
# first_orders = filtered_orders.groupby('customer_id')['order_date'].min().reset_index()
# new_customers = len(first_orders[first_orders['order_date'] >= midpoint])
# customer_retention_rate_ecom = ((customers_end - new_customers) / customers_start) * 100 if customers_start > 0 else 0

# # Display E-Commerce KPIs
# col1, col2, col3 = st.columns(3)
# with col1:
#     st.metric("Conversion Rate", f"{conversion_rate:.2f}%")
# with col2:
#     st.metric("AOV", f"${aov:.2f}")
# with col3:
#     st.metric("Repeat Purchase Rate", f"{repeat_purchase_rate:.2f}%")
# col4, col5, col6 = st.columns(3)
# with col4:
#     st.metric("CLV", f"${clv:.2f}")
# with col5:
#     st.metric("Customer Retention Rate", f"{customer_retention_rate_ecom:.2f}%")

# # Export E-Commerce KPIs
# kpi_data_ecom = pd.DataFrame({
#     "Metric": ["Conversion Rate", "AOV", "Repeat Purchase Rate", "CLV", "Customer Retention Rate"],
#     "Value": [f"{conversion_rate:.2f}%", f"${aov:.2f}", f"{repeat_purchase_rate:.2f}%", f"${clv:.2f}", f"{customer_retention_rate_ecom:.2f}%"]
# })
# csv_ecom = kpi_data_ecom.to_csv(index=False)
# st.download_button(label="Download E-Commerce KPIs as CSV", data=csv_ecom, file_name="ecommerce_kpis.csv", mime="text/csv")


# # Chapter 2: Customer Experience (CX) Analysis KPIs
# st.subheader("Chapter 2: Customer Experience (CX) Analysis KPIs")
# st.write("Note: Only feasible KPIs are calculated due to limited data availability.")

# # 4. Customer Retention Rate (CRR)
# customer_retention_rate_cx = ((customers_end - new_customers) / customers_start) * 100 if customers_start > 0 else 0
# col7, col8 = st.columns(2)
# with col7:
#     st.metric("Customer Retention Rate (CRR)", f"{customer_retention_rate_cx:.2f}%")

# # 7. Complaint Rate
# total_interactions = len(filtered_orders) + len(filtered_sessions)  # Approximation: Orders + Sessions
# complaints = filtered_returns['order_id'].nunique()  # Approximation: Returns as complaints
# complaint_rate = (complaints / total_interactions) * 100 if total_interactions > 0 else 0
# with col8:
#     st.metric("Complaint Rate", f"{complaint_rate:.2f}%")



# # Chapter 3: Supply Chain KPIs
# st.subheader("Chapter 3: Supply Chain KPIs")
# st.write("Note: Some KPIs are approximated due to limited data availability.")

# # 1. Order Accuracy
# total_orders_count = len(filtered_orders)
# orders_with_returns = filtered_returns['order_id'].nunique()
# correct_orders = total_orders_count - orders_with_returns  # Approximation: Orders without returns
# order_accuracy = (correct_orders / total_orders_count) * 100 if total_orders_count > 0 else 0
# col9, col10 = st.columns(2)
# with col9:
#     st.metric("Order Accuracy", f"{order_accuracy:.2f}%")

# # 2. Cycle Time
# merged_orders_shipping = filtered_orders.merge(filtered_shipping, left_on='id', right_on='order_id', how='left')
# cycle_time = (merged_orders_shipping['shipping_date'] - merged_orders_shipping['order_date']).dt.total_seconds() / (24 * 3600)  # Convert to days
# average_cycle_time = cycle_time.mean() if not cycle_time.empty else 0
# with col10:
#     st.metric("Average Cycle Time", f"{average_cycle_time:.2f} days")

# # 5. On-Time Delivery Rate
# # Assuming on-time if delivered within 7 days of order placement
# merged_orders_shipping['days_to_delivery'] = (merged_orders_shipping['shipping_date'] - merged_orders_shipping['order_date']).dt.total_seconds() / (24 * 3600)
# on_time_deliveries = len(merged_orders_shipping[merged_orders_shipping['days_to_delivery'] <= 7])
# total_deliveries = len(merged_orders_shipping)
# on_time_delivery_rate = (on_time_deliveries / total_deliveries) * 100 if total_deliveries > 0 else 0
# col11, col12 = st.columns(2)
# with col11:
#     st.metric("On-Time Delivery Rate", f"{on_time_delivery_rate:.2f}%")



import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="KPIs", layout="wide")
st.title("📊 KPIs")

# Check if required data tables are in session state
required_tables = [
    'Order_Details', 'Orders', 'Customer_Sessions', 
    'Products', 'Customers', 'Returns', 'Shipping'
]

if 'tables' not in st.session_state or any(
    st.session_state['tables'].get(table) is None for table in required_tables
):
    st.warning("⚠️ Please upload all required data from the Home page first.")
    st.stop()

# Load data from session state
data = st.session_state['tables']
order_details = data['Order_Details']
orders_df = data['Orders']
sessions_df = data['Customer_Sessions']
products_df = data['Products']
customers_df = data['Customers']
returns_df = data['Returns']
shipping_df = data['Shipping']

# Ensure required columns exist in Order_Details
required_order_columns = ['product_id', 'added_date']
missing_columns = [col for col in required_order_columns if col not in order_details.columns]
if missing_columns:
    st.error(f"Missing required columns in Order_Details: {', '.join(missing_columns)}")
    st.stop()

# Ensure datetime format for 'added_date' in Order_Details
if not pd.api.types.is_datetime64_any_dtype(order_details['added_date']):
    try:
        order_details['added_date'] = pd.to_datetime(order_details['added_date'])
    except Exception as e:
        st.error(f"Error parsing 'added_date': {e}")
        st.stop()

# -------------------- Filters -------------------- #
st.subheader("🗂️ Filter Data")
start_date = st.date_input("Start Date", orders_df['order_date'].min())
end_date = st.date_input("End Date", orders_df['order_date'].max())

# Filter orders, sessions, returns, and shipping based on date range
filtered_orders = orders_df[
    (orders_df['order_date'] >= pd.Timestamp(start_date)) & 
    (orders_df['order_date'] <= pd.Timestamp(end_date))
]
filtered_sessions = sessions_df[
    (sessions_df['session_start'] >= pd.Timestamp(start_date)) & 
    (sessions_df['session_end'] <= pd.Timestamp(end_date))
]
filtered_returns = returns_df[returns_df['order_id'].isin(filtered_orders['id'])]
filtered_shipping = shipping_df[shipping_df['order_id'].isin(filtered_orders['id'])]

# -------------------- Chapter 1: E-Commerce KPIs -------------------- #
st.subheader("📈 1: E-Commerce KPIs")

# Metrics Calculations
total_visitors = filtered_sessions['customer_id'].nunique()
completed_orders = filtered_orders[filtered_orders['status'].isin(['completed', 'shipped'])]['id'].nunique()
conversion_rate = (completed_orders / total_visitors) * 100 if total_visitors > 0 else 0

total_revenue = filtered_orders[filtered_orders['status'].isin(['completed', 'shipped'])]['total_amount'].sum()
aov = total_revenue / completed_orders if completed_orders > 0 else 0

total_customers = filtered_orders['customer_id'].nunique()
returning_customers = filtered_orders['customer_id'].value_counts().gt(1).sum()
repeat_purchase_rate = (returning_customers / total_customers) * 100 if total_customers > 0 else 0

purchase_frequency = filtered_orders['customer_id'].value_counts().mean()
customer_orders = filtered_orders.groupby('customer_id')['order_date'].agg(['min', 'max'])
customer_lifespan = (customer_orders['max'] - customer_orders['min']).mean().days / 365
clv = aov * purchase_frequency * customer_lifespan if all([aov > 0, purchase_frequency > 0, customer_lifespan > 0]) else 0

min_date = filtered_orders['order_date'].min()
max_date = filtered_orders['order_date'].max()
midpoint = min_date + (max_date - min_date) / 2
customers_start = filtered_orders[filtered_orders['order_date'] < midpoint]['customer_id'].nunique()
customers_end = filtered_orders[filtered_orders['order_date'] >= midpoint]['customer_id'].nunique()
first_orders = filtered_orders.groupby('customer_id')['order_date'].min().reset_index()
new_customers = len(first_orders[first_orders['order_date'] >= midpoint])
customer_retention_rate = ((customers_end - new_customers) / customers_start) * 100 if customers_start > 0 else 0

# -------------------- Display Metrics -------------------- #
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🔁 Conversion Rate", f"{conversion_rate:.2f}%")
with col2:
    st.metric("💵 Average Order Value (AOV)", f"${aov:.2f}")
with col3:
    st.metric("📦 Repeat Purchase Rate", f"{repeat_purchase_rate:.2f}%")

col4, col5 = st.columns(2)
with col4:
    st.metric("👤 Customer Lifetime Value (CLV)", f"${clv:.2f}")
with col5:
    st.metric("📈 Customer Retention Rate", f"{customer_retention_rate:.2f}%")

# -------------------- Export KPI Data -------------------- #
kpi_data = pd.DataFrame({
    "Metric": [
        "Conversion Rate", "Average Order Value", 
        "Repeat Purchase Rate", "Customer Lifetime Value", 
        "Customer Retention Rate"
    ],
    "Value": [
        f"{conversion_rate:.2f}%", f"${aov:.2f}", 
        f"{repeat_purchase_rate:.2f}%", f"${clv:.2f}", 
        f"{customer_retention_rate:.2f}%"
    ]
})

csv = kpi_data.to_csv(index=False)
st.download_button(
    label="⬇️ Download KPIs as CSV",
    data=csv,
    file_name="ecommerce_kpis.csv",
    mime="text/csv"
)

# -------------------- Chapter 2: Customer Experience (CX) Analysis KPIs -------------------- #
st.subheader("2: Customer Experience (CX) Analysis KPIs")


# Customer Retention Rate (CRR)
customer_retention_rate_cx = ((customers_end - new_customers) / customers_start) * 100 if customers_start > 0 else 0
col7, col8 = st.columns(2)
with col7:
    st.metric("Customer Retention Rate (CRR)", f"{customer_retention_rate_cx:.2f}%")

# Complaint Rate
total_interactions = len(filtered_orders) + len(filtered_sessions)  # Orders + Sessions
complaints = filtered_returns['order_id'].nunique()  # Approximation: Returns as complaints
complaint_rate = (complaints / total_interactions) * 100 if total_interactions > 0 else 0
with col8:
    st.metric("Complaint Rate", f"{complaint_rate:.2f}%")

# -------------------- Chapter 3: Supply Chain KPIs -------------------- #
st.subheader("3: Supply Chain KPIs")


# Order Accuracy
total_orders_count = len(filtered_orders)
orders_with_returns = filtered_returns['order_id'].nunique()
correct_orders = total_orders_count - orders_with_returns  # Orders without returns
order_accuracy = (correct_orders / total_orders_count) * 100 if total_orders_count > 0 else 0
col9, col10 = st.columns(2)
with col9:
    st.metric("Order Accuracy", f"{order_accuracy:.2f}%")

# Cycle Time
merged_orders_shipping = filtered_orders.merge(filtered_shipping, left_on='id', right_on='order_id', how='left')
cycle_time = (merged_orders_shipping['shipping_date'] - merged_orders_shipping['order_date']).dt.total_seconds() / (24 * 3600)  # Convert to days
average_cycle_time = cycle_time.mean() if not cycle_time.empty else 0
with col10:
    st.metric("Average Cycle Time", f"{average_cycle_time:.2f} days")

# -------------------- Chapter 4: Financial KPIs -------------------- #
st.subheader(" 4: Financial KPIs")


# Gross Profit Margin
total_revenue = filtered_orders['revenue'].sum() if 'revenue' in filtered_orders else 0
total_cost_of_goods_sold = filtered_orders['cost_of_goods_sold'].sum() if 'cost_of_goods_sold' in filtered_orders else 0
gross_profit_margin = ((total_revenue - total_cost_of_goods_sold) / total_revenue) * 100 if total_revenue > 0 else 0
col11, col12 = st.columns(2)
with col11:
    st.metric("Gross Profit Margin", f"{gross_profit_margin:.2f}%")

# Net Profit Margin
net_profit = total_revenue - total_cost_of_goods_sold - filtered_orders['expenses'].sum() if 'expenses' in filtered_orders else 0
net_profit_margin = (net_profit / total_revenue) * 100 if total_revenue > 0 else 0
with col12:
    st.metric("Net Profit Margin", f"{net_profit_margin:.2f}%")
