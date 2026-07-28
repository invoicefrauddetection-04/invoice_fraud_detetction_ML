from database.scripts.db_connection import get_connection


def get_supplier_features(supplier_id):
    """
    Fetch historical supplier information from training_invoices.
    Returns a dictionary containing supplier-related features.
    """

    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT
            supplier_invoice_count_30d,
            supplier_avg_amount_90d,
            supplier_country,
            supplier_age_days,
            supplier_risk_score,
            blacklisted_flag,
            avg_invoice_amount,
            region,
            annual_budget
        FROM training_invoices
        WHERE supplier_id = %s
        LIMIT 1;
    """

    cur.execute(query, (supplier_id,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if row is None:
        print(f"Supplier '{supplier_id}' not found.")

        return {
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

    return {

        "supplier_invoice_count_30d": row[0],
        "supplier_avg_amount_90d": row[1],
        "supplier_country": row[2],
        "supplier_age_days": row[3],
        "supplier_risk_score": row[4],
        "blacklisted_flag": row[5],
        "avg_invoice_amount": row[6],
        "region": row[7],
        "annual_budget": row[8]

    }

'''
#testing purpose
if __name__ == "__main__":

    supplier_id = "1165e210-9854-4881-918a-9d292f923996"
    # supplier_id = 'f1b64afe-7f89-40f0-8d70-f8c0e57774a7' --> unseen data

    features = get_supplier_features(supplier_id)

    print("\nSupplier Features:\n")

    for key, value in features.items():
        print(f"{key} : {value}")

'''