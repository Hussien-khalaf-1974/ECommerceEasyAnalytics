import pandas as pd

# In utils/data_handler.py
def identify_table(df, sheet_name):
    """
    Identify the table type based on sheet name and columns.
    Returns the table name or None if unidentified.
    """
    # Normalize sheet name and columns
    sheet_name = sheet_name.strip().lower()
    columns = [col.strip().lower() for col in df.columns]

    # Debug: Log sheet name and columns
    print(f"Checking sheet '{sheet_name}' with columns: {columns}")

    # Order_Details: customer_id, product_id, added_date
    if sheet_name == "order_details" or all(col in columns for col in ['customer_id', 'product_id', 'added_date']):
        return 'Order_Details'

    # Wishlists: customer_id, product_id (no added_date)
    if sheet_name == "wishlists" or (all(col in columns for col in ['customer_id', 'product_id']) and 'added_date' not in columns):
        return 'Wishlists'

    # Customers: id, name, email, group
    if sheet_name == "customers" or all(col in columns for col in ['id', 'name', 'email', 'group']):
        return 'Customers'

    # Suppliers: supplier_id, name, contact_info
    if sheet_name == "suppliers" or all(col in columns for col in ['supplier_id', 'name', 'contact_info']):
        return 'Suppliers'

    # Categories: id, name, parent_id
    if sheet_name == "categories" or all(col in columns for col in ['id', 'name', 'parent_id']):
        return 'Categories'

    # Customer_Sessions: customer_id, session_start, session_end
    if sheet_name == "customer_sessions" or all(col in columns for col in ['customer_id', 'session_start', 'session_end']):
        return 'Customer_Sessions'

    # Discounts: discount_id, amount
    if sheet_name == "discounts" or all(col in columns for col in ['discount_id', 'amount']):
        return 'Discounts'

    # Inventory_Movements: product_id, movement_type, quantity
    if sheet_name == "inventory_movements" or all(col in columns for col in ['product_id', 'movement_type', 'quantity']):
        return 'Inventory_Movements'

    # Orders: order_id, customer_id, order_date
    if sheet_name == "orders" or all(col in columns for col in ['order_id', 'customer_id', 'order_date']):
        return 'Orders'

    # Payments: payment_id, order_id, amount
    if sheet_name == "payments" or all(col in columns for col in ['payment_id', 'order_id', 'amount']):
        return 'Payments'

    # Products: product_id, name, price
    if sheet_name == "products" or all(col in columns for col in ['product_id', 'name', 'price']):
        return 'Products'

    # Returns: return_id, order_id, reason
    if sheet_name == "returns" or all(col in columns for col in ['id', 'order_id', 'reason']):
        return 'Returns'

    # Reviews: review_id, product_id, rating
    if sheet_name == "reviews" or all(col in columns for col in ['review_id', 'product_id', 'rating']):
        return 'Reviews'

    # Shipping: shipping_id, order_id, shipping_date
    if sheet_name == "shipping" or all(col in columns for col in ['shipping_id', 'order_id', 'shipping_date']):
        return 'Shipping'

    print(f"Sheet '{sheet_name}' not identified as any expected table.")
    return None




# In utils/data_handler.py
def validate_data(tables):
    """
    Validate the tables dictionary for required tables and columns.
    Returns a list of error messages.
    """
    errors = []

    # Check if Order_Details is present
    if tables['Order_Details'] is None:
        errors.append("Order_Details table is missing or could not be identified.")
    else:
        required_cols = ['customer_id', 'product_id', 'added_date']
        missing_cols = [col for col in required_cols if col not in tables['Order_Details'].columns]
        if missing_cols:
            errors.append(f"Order_Details missing required columns: {', '.join(missing_cols)}")
        # Check if added_date is convertible to datetime
        try:
            pd.to_datetime(tables['Order_Details']['added_date'])
        except Exception as e:
            errors.append(f"Order_Details 'added_date' column is not in a valid datetime format: {e}")

    # Check Categories (optional, but validate if present)
    if tables['Categories'] is None:
        errors.append("Categories table is missing or could not be identified.")
    else:
        required_cols = ['id', 'name', 'parent_id']
        missing_cols = [col for col in required_cols if col not in tables['Categories'].columns]
        if missing_cols:
            errors.append(f"Categories missing required columns: {', '.join(missing_cols)}")

    # Check Customer_Sessions (optional)
    if tables['Customer_Sessions'] is None:
        errors.append("Customer_Sessions table is missing or could not be identified.")
    else:
        required_cols = ['customer_id', 'session_start', 'session_end']
        missing_cols = [col for col in required_cols if col not in tables['Customer_Sessions'].columns]
        if missing_cols:
            errors.append(f"Customer_Sessions missing required columns: {', '.join(missing_cols)}")

    # Check Customers (optional)
    if tables['Customers'] is None:
        errors.append("Customers table is missing or could not be identified.")
    else:
        required_cols = ['id', 'name', 'email']
        missing_cols = [col for col in required_cols if col not in tables['Customers'].columns]
        if missing_cols:
            errors.append(f"Customers missing required columns: {', '.join(missing_cols)}")

    return errors
