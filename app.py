import streamlit as st
import pandas as pd

# Set page title
st.set_page_config(page_title="NZOA Member Portal", page_icon="📋")

st.title("📋 NZOA Membership Search")

# 1. Your Google Sheet CSV Export Link
# To get this: In Google Sheets, go to File > Share > Publish to web. 
# Select 'Entire Document' and 'Comma-separated values (.csv)'. Copy that link.
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRE6Vy5KOX2C7cA-n0L92njVELkOkNKuH6y_9ybp41OAXweDIhYBFwRmoNih8_XtvMoXq-b8JSRPO4T/pub?output=csv"

@st.cache_data(ttl=300) # Updates every 5 minutes
def load_data():
    try:
        return pd.read_csv(SHEET_CSV_URL)
    except Exception as e:
        st.error("Could not connect to the Google Sheet. Please check the 'Publish to Web' link.")
        return None

df = load_data()

if df is not None:
    # Clean up column names just in case
    df.columns = [str(c).strip() for c in df.columns]
    
    search_input = st.text_input("Search by Name, Email, or Mobile", "").strip()

    if search_input:
        # Search across Name, Mobile, and E-mail
        mask = (
            df['Name'].astype(str).str.contains(search_input, case=False, na=False) |
            df['Mobile'].astype(str).str.contains(search_input, na=False) |
            df['E-mail'].astype(str).str.contains(search_input, case=False, na=False)
        )
        results = df[mask]
        
        if not results.empty:
            st.success(f"Matches Found: {len(results)}")
            st.table(results[['LM number', 'Name', 'City', 'Mobile', 'E-mail']])
        else:
            st.warning("No member found. Please try a different detail.")
    else:
        st.info("Enter details above to search the database.")

st.divider() # Adds a visual line to separate the search from the update section

st.subheader("📝 Something look wrong?")
st.write("If your information is missing, outdated, or contains a typo, please let us know.")

# Replace the URL below with your actual Google Form Link
google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSc4sHX_ZmLNbLqTQR95GhxAgb88bWTsKqZdmivI4_X_8Bgf-w/viewform?usp=sharing&ouid=117740253316801220512"

if st.button("Update My Information"):
    # This opens the form in a new browser tab
    st.markdown(f'<a href="{google_form_url}" target="_blank" style="text-decoration: none;"><button style="background-color: #FF4B4B; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">Fill Correction Form</button></a>', unsafe_index=False, unsafe_allow_html=True)

# Alternative: A subtle notice if no results are found
if search_input and results.empty:
    st.info("Can't find your name? It might not be in our database yet. Click the button above to register your details.")
