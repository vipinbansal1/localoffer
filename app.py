import streamlit as st
from modules.data_loader import load_customer_data
from modules.template_engine import render_messages, DEFAULT_TEMPLATE
from modules.messenger import send_whatsapp_messages
from modules.storage import init_db, fetch_logs, fetch_stats

# Initialize DB
init_db()

st.set_page_config(page_title="Vendor Offer PoC", layout="wide")
st.title("📢 Vendor Offer PoC")

# --- Step 1: Upload Data ---
st.header("Step 1: Upload Customer List")
uploaded_file = st.file_uploader("Upload CSV (must include name, phone, offer)", type=["csv"])

if uploaded_file:
    try:
        df = load_customer_data(uploaded_file)
        st.success("✅ Data loaded successfully!")
        st.dataframe(df.head())

        # --- Step 2: Write Template ---
        st.header("Step 2: Write Offer Template")
        template_str = st.text_area(
            "Enter message template (use {{name}}, {{offer}})",
            value=DEFAULT_TEMPLATE,
            height=120
        )

        # --- Step 3: Preview Messages ---
        if st.button("Preview Messages"):
            messages = render_messages(df, template_str)
            st.session_state["messages"] = messages
            st.success("Generated personalized messages!")
            st.write("### Preview (first 5):")
            for m in messages[:5]:
                st.text(f"{m['phone']} → {m['message']}")

        # --- Step 4: Send Messages ---
        if "messages" in st.session_state:
            st.header("Step 3: Send Messages")
            dry_run = st.checkbox("Dry Run (do not actually send)", value=True)
            if st.button("Send Now"):
                send_whatsapp_messages(st.session_state["messages"], dry_run=dry_run)
                st.success("✅ Messages processed. Check logs below.")

    except Exception as e:
        st.error(f"Error: {e}")

# --- Step 5: Analytics & Logs ---
st.header("📊 Analytics & Logs")
stats = fetch_stats()
col1, col2 = st.columns(2)
col1.metric("Total Logged", stats["total"])
col2.metric("Sent Successfully", stats["sent"])

logs = fetch_logs(limit=20)
st.write("Recent Activity:")
st.table(logs)
