# import streamlit as st
# import pandas as pd
# from utils.data_handler import identify_table, validate_data

# st.set_page_config(page_title="ECommerceEasyAnalytics", layout="wide")
# st.title("ECommerceEasyAnalytics - Home")
# st.markdown("Upload your Excel file here to unlock the analytics pages.")

# # Initialize session state for file and tables if not already present
# if 'uploaded_file' not in st.session_state:
#     st.session_state['uploaded_file'] = None
# if 'file_name' not in st.session_state:
#     st.session_state['file_name'] = None
# if 'tables' not in st.session_state:
#     st.session_state['tables'] = {
#         'Categories': None,
#         'Customer_Sessions': None,
#         'Customers': None,
#         'Discounts': None,
#         'Inventory_Movements': None,
#         'Order_Details': None,
#         'Orders': None,
#         'Payments': None,
#         'Products': None,
#         'Returns': None,
#         'Reviews': None,
#         'Shipping': None,
#         'Suppliers': None,
#         'Wishlists': None
#     }

# # Check if a file is already loaded in session state
# if st.session_state['uploaded_file'] is not None:
#     st.success(f"File '{st.session_state['file_name']}' is loaded.")
#     # Display loaded tables status
#     st.write("Loaded tables:", {k: "Loaded" if v is not None else "None" for k, v in st.session_state['tables'].items()})
    
#     # Option to clear the current file
#     if st.button("Clear Uploaded File"):
#         st.session_state['uploaded_file'] = None
#         st.session_state['file_name'] = None
#         st.session_state['tables'] = {k: None for k in st.session_state['tables']}
#         st.session_state.clear()  # Clear all session state
#         st.experimental_rerun()  # Rerun to reset the UI

# # File uploader (shown only if no file is loaded or after clearing)
# if st.session_state['uploaded_file'] is None:
#     uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"])
# else:
#     uploaded_file = None  # Skip uploader if file is already loaded

# # Process the file (new upload or from session state)
# if uploaded_file is not None or st.session_state['uploaded_file'] is not None:
#     with st.spinner("Processing Excel file..."):
#         # Use new uploaded file or fall back to session state
#         if uploaded_file is not None:
#             # Store file contents and name in session state
#             file_bytes = uploaded_file.read()
#             st.session_state['uploaded_file'] = file_bytes
#             st.session_state['file_name'] = uploaded_file.name
#             excel_data = pd.read_excel(file_bytes, sheet_name=None)
#         else:
#             # Read from session state
#             excel_data = pd.read_excel(st.session_state['uploaded_file'], sheet_name=None)

#         # Reset tables in session state
#         tables = st.session_state['tables']
#         for key in tables:
#             tables[key] = None

#         # Identify and process sheets
#         for sheet_name, df in excel_data.items():
#             df.columns = df.columns.str.strip()
#             table = identify_table(df, sheet_name)
#             st.write(f"Sheet '{sheet_name}' identified as: {table if table else 'None'}")

#             if table:
#                 if table == 'Customers':
#                     if 'first_name' in df.columns and 'last_name' in df.columns:
#                         df['name'] = df['first_name'] + ' ' + df['last_name']
#                     if 'group' not in df.columns:
#                         df['group'] = 'Unknown'
#                 elif table == 'Categories' and 'parent_id' not in df.columns:
#                     df['parent_id'] = 0

#                 tables[table] = df
#             else:
#                 st.warning(f"Sheet '{sheet_name}' could not be identified as any expected table.")

#         # Debug: Show loaded tables
#         st.write("Loaded tables:", {k: "Loaded" if v is not None else "None" for k, v in tables.items()})

#         # Validate data
#         errors = validate_data(tables)
#         if errors:
#             st.error("Validation Errors:")
#             for e in errors:
#                 st.write(f"- {e}")
#             # Clear session state if validation fails
#             st.session_state['uploaded_file'] = None
#             st.session_state['file_name'] = None
#             st.session_state['tables'] = {k: None for k in st.session_state['tables']}
#         else:
#             st.success(f"File '{st.session_state['file_name']}' uploaded and validated successfully!")
#             # Update session state with tables
#             st.session_state['tables'] = tables
#             st.write("Session state updated with tables:", list(tables.keys()))
















import streamlit as st
import pandas as pd
from utils.data_handler import identify_table, validate_data

# Page config
st.set_page_config(page_title="📊 ECommerceEasyAnalytics", layout="wide")
st.title("📈 ECommerceEasyAnalytics - Home")
st.markdown("### 📤 Upload your Excel file to unlock analytics insights.")

# Session state initialization
if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None
if 'file_name' not in st.session_state:
    st.session_state['file_name'] = None
if 'tables' not in st.session_state:
    st.session_state['tables'] = {
        'Categories': None,
        'Customer_Sessions': None,
        'Customers': None,
        'Discounts': None,
        'Inventory_Movements': None,
        'Order_Details': None,
        'Orders': None,
        'Payments': None,
        'Products': None,
        'Returns': None,
        'Reviews': None,
        'Shipping': None,
        'Suppliers': None,
        'Wishlists': None
    }

# Status of uploaded file
if st.session_state['uploaded_file'] is not None:
    st.success(f"✅ **File loaded:** `{st.session_state['file_name']}`")

    with st.expander("📋 View Loaded Tables Status"):
        table_status = {
            k: "✅ Loaded" if v is not None else "❌ Not Loaded"
            for k, v in st.session_state['tables'].items()
        }
        st.json(table_status)

    if st.button("🗑️ Clear Uploaded File"):
        st.session_state['uploaded_file'] = None
        st.session_state['file_name'] = None
        st.session_state['tables'] = {k: None for k in st.session_state['tables']}
        st.session_state.clear()
        st.experimental_rerun()

# File uploader
if st.session_state['uploaded_file'] is None:
    uploaded_file = st.file_uploader("📂 Upload Excel File", type=["xlsx", "xls"])
else:
    uploaded_file = None

# File processing
if uploaded_file is not None or st.session_state['uploaded_file'] is not None:
    with st.spinner("🔄 Processing Excel file..."):
        if uploaded_file is not None:
            file_bytes = uploaded_file.read()
            st.session_state['uploaded_file'] = file_bytes
            st.session_state['file_name'] = uploaded_file.name
            excel_data = pd.read_excel(file_bytes, sheet_name=None)
        else:
            excel_data = pd.read_excel(st.session_state['uploaded_file'], sheet_name=None)

        tables = st.session_state['tables']
        for key in tables:
            tables[key] = None

        st.markdown("### 🧩 Sheet Identification Results")
        for sheet_name, df in excel_data.items():
            df.columns = df.columns.str.strip()
            table = identify_table(df, sheet_name)

            if table:
                st.success(f"✅ Sheet **'{sheet_name}'** ➝ Identified as **{table}**")

                if table == 'Customers':
                    if 'first_name' in df.columns and 'last_name' in df.columns:
                        df['name'] = df['first_name'] + ' ' + df['last_name']
                    if 'group' not in df.columns:
                        df['group'] = 'Unknown'
                elif table == 'Categories' and 'parent_id' not in df.columns:
                    df['parent_id'] = 0

                tables[table] = df
            else:
                st.warning(f"⚠️ Sheet **'{sheet_name}'** could not be matched to any known table.")

        # Display table load status
        with st.expander("📦 Final Loaded Tables Overview"):
            st.json({
                k: "✅ Loaded" if v is not None else "❌ Not Loaded"
                for k, v in tables.items()
            })

        # Validate data
        errors = validate_data(tables)
        if errors:
            st.error("🚫 **Validation Errors Found:**")
            for e in errors:
                st.markdown(f"- ❌ {e}")

            # Clear session on error
            st.session_state['uploaded_file'] = None
            st.session_state['file_name'] = None
            st.session_state['tables'] = {k: None for k in st.session_state['tables']}
        else:
            st.success(f"🎉 File `{st.session_state['file_name']}` uploaded and validated successfully!")
            st.session_state['tables'] = tables

            with st.expander("📂 Loaded Table Keys"):
                st.code("\n".join(list(tables.keys())), language="python")







