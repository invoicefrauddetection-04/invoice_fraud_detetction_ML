from app.pipeline_DB.database.scripts.db_connection import get_connection


# ----------------------------------------------------
# Get Historical Supplier Features
# ----------------------------------------------------

def get_supplier_features(supplier_id):
    """
    Fetch historical supplier information from training_invoices.
    Returns default values for unseen suppliers.
    """

    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT

            COUNT(*) AS supplier_frequency,

            MAX(supplier_invoice_count_30d),

            MAX(supplier_avg_amount_90d),

            MAX(supplier_country),

            MAX(supplier_age_days),

            MAX(supplier_risk_score),

            BOOL_OR(blacklisted_flag),

            MAX(avg_invoice_amount),

            MAX(region),

            MAX(annual_budget)

        FROM training_invoices

        WHERE supplier_id = %s;
    """

    cur.execute(query, (supplier_id,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    # ----------------------------------------------------
    # Cold Start / Unseen Supplier
    # ----------------------------------------------------

    if row is None or row[0] == 0:

        print(f"Supplier '{supplier_id}' not found. Using default values.")

        return {

            "supplier_frequency": 0,

            "supplier_invoice_count_30d": 0,

            "supplier_avg_amount_90d": 0.0,

            "supplier_country": "UNKNOWN",

            "supplier_age_days": 0,

            "supplier_risk_score": 0.0,

            "blacklisted_flag": False,

            "avg_invoice_amount": 0.0,

            "region": "UNKNOWN",

            "annual_budget": 0.0

        }

    # ----------------------------------------------------
    # Existing Supplier
    # ----------------------------------------------------

    return {

        "supplier_frequency": row[0],

        "supplier_invoice_count_30d":
            row[1] if row[1] is not None else 0,

        "supplier_avg_amount_90d":
            float(row[2]) if row[2] is not None else 0.0,

        "supplier_country":
            row[3] if row[3] is not None else "UNKNOWN",

        "supplier_age_days":
            row[4] if row[4] is not None else 0,

        "supplier_risk_score":
            float(row[5]) if row[5] is not None else 0.0,

        "blacklisted_flag":
            bool(row[6]) if row[6] is not None else False,

        "avg_invoice_amount":
            float(row[7]) if row[7] is not None else 0.0,

        "region":
            row[8] if row[8] is not None else "UNKNOWN",

        "annual_budget":
            float(row[9]) if row[9] is not None else 0.0

    }

'''
# ----------------------------------------------------
# Testing
# ----------------------------------------------------

if __name__ == "__main__":

    supplier_id = input("Enter Supplier ID : ")

    features = get_supplier_features(supplier_id)

    print("\nSupplier Features\n")

    for key, value in features.items():

        print(f"{key:30}: {value}")
'''