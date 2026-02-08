import streamlit as st
import pandas as pd

st.set_page_config(page_title="NZOA Member Portal", page_icon="📋")
st.title("📋 NZOA Membership Search")

# 1. Your Google Sheet CSV Export Link
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRE6Vy5KOX2C7cA-n0L92njVELkOkNKuH6y_9ybp41OAXweDIhYBFwRmoNih8_XtvMoXq-b8JSRPO4T/pub?output=csv"

@st.cache_data(ttl=300)
def load_data():
    try:
        # We add on_bad_lines='skip' to prevent the crash
        # and engine='python' for better error handling
        data = pd.read_csv(SHEET_CSV_URL, on_bad_lines='skip', engine='python')
        data.columns = [str(c).strip() for c in data.columns]
        return data
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None


df = load_data()

if df is not None:
    search_input = st.text_input("Search by Name, Email, or Mobile", "").strip()

    # Define the columns we want to search in (cleaned versions)
    # Ensure these match your Google Sheet headers
    name_col = 'Name'
    mobile_col = 'Mobile'
    email_col = 'E-mail'

    if search_input:
        try:
            # Flexible search logic
            mask = (
                df[name_col].astype(str).str.contains(search_input, case=False, na=False) |
                df[mobile_col].astype(str).str.contains(search_input, na=False) |
                df[email_col].astype(str).str.contains(search_input, case=False, na=False)
            )
            results = df[mask]
            
            if not results.empty:
                st.success(f"Matches Found: {len(results)}")
                # Show specific columns in your requested order
                st.dataframe(results[['LM number', 'Name', 'City', 'Mobile', 'E-mail']], hide_index=True)
            else:
                st.warning("No member found. Check your spelling or try another detail.")
        except KeyError as e:
            st.error(f"Column Name Error: The app couldn't find the column {e}.")
            st.info("Check your Google Sheet headers. They must be exactly: LM number, Name, City, Mobile, E-mail")
            # This helps you see what the app actually sees:
            st.write("Current Columns detected:", list(df.columns))
    else:
        st.info("Enter details above to search.")

# --- Form Update Button ---
st.divider()
st.subheader("📝 Information Incorrect?")
google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSc4sHX_ZmLNbLqTQR95GhxAgb88bWTsKqZdmivI4_X_8Bgf-w/viewform?usp=sharing&ouid=117740253316801220512"
st.link_button("Request Data Correction", google_form_url, type="primary")
