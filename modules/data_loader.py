import pandas as pd

REQUIRED_COLUMNS = ["name", "phone", "offer"]

def load_customer_data(file):
    try:
        df = pd.read_csv(file)
    except Exception as e:
        raise ValueError(f"Error reading file: {e}")

    # check columns
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # basic phone number sanity check
    df["phone"] = df["phone"].astype(str)
    df["phone"] = df["phone"].astype(str).apply(lambda x: "+" + x)
    if not df["phone"].str.startswith("+").all():
        raise ValueError("All phone numbers must include country code (e.g., +91...)")

    return df
