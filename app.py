import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="NZOA Member Portal", page_icon="📋")

st.title("📋 NZOA Membership Search")
st.write("Real-time Member Database")

# Replace this with YOUR actual Google Sheet URL
url = "https://docs.google.com/spreadsheets/d/1IDaobVgyoCVPcSYfB2VfdPaETadVcqd18JDZP8Wza2c/edit?usp=sharing"

# Establish connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Read data (ttl="10m" means it checks for new data every 10 minutes)
# Use ttl=0 if you want it to refresh every single time the page loads
try:
    df = conn.read(spreadsheet=url, ttl="5m")
    
    search_input = st.text_input("Search by Name, Email, or Mobile", "").strip()

    if search_input:
        mask = (
            df['Name'].astype(str).str.contains(search_input, case=False, na=False) |
            df['Mobile'].astype(str).str.contains(search_input, na=False) |
            df['E-mail'].astype(str).str.contains(search_input, case=False, na=False)
        )
        results = df[mask]
        
        if not results.empty:
            st.success(f"Matches Found: {len(results)}")
            st.dataframe(results[['LM number', 'Name', 'City', 'Mobile', 'E-mail']], hide_index=True)
        else:
            st.warning("No member found. Check the spelling or try another detail.")
    else:
        st.info("Enter details above to search.")

except Exception as e:
    st.error("Could not connect to Google Sheets. Please check the URL and Sharing permissions.")
