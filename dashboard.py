import streamlit as st
import sqlite3
import pandas as pd
import json
import re
from security_pipeline import run_security_pipeline, init_db  # Import your security functions

# Initialize DB
init_db()

# Streamlit UI Setup
st.set_page_config(page_title="Cybersecurity Scanner", layout="wide")
st.title("🛡️ Cybersecurity Scanner Dashboard")
st.subheader("Run security scans with AI-powered insights.")

# Function to clear all previous scans
def clear_scan_history():
    conn = sqlite3.connect("security_scans.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scans")  # Deletes all scan records
    conn.commit()
    conn.close()
    st.success("✅ All previous scan history has been cleared!")

# User Inputs: Target & Tools
target = st.text_input("Enter Target (Domain/IP)", "example.com")
tools = st.multiselect("Select Security Tools", ["nmap", "ffuf"], ["nmap"])

# Button to Run Security Scan
if st.button("🔍 Start Scan"):
    st.info(f"Scanning `{target}` using {', '.join(tools)}...")
    
    allowed_scope = [target]  # Define scan scope
    results = run_security_pipeline(target, tools, allowed_scope)

    st.success("✅ Scan Completed!")
    
    # Display Groq AI Analysis
    st.subheader("🧠 AI Security Insights")
    st.write(results["groq_analysis"])

    # Display Scan Results
    st.subheader("📊 Security Scan Results")
    for task, output in results["scan_results"].items():
        with st.expander(f"🔍 {task}"):
            st.code(output, language="bash")
    
    # Save Scan Results to File
    safe_target = re.sub(r"[^\w.-]", "_", target)  # ✅ Replace invalid characters
    report_file = f"{safe_target}_security_report.json"
    with open(report_file, "w") as f:
        json.dump(results, f, indent=4)
    
    st.download_button(label="📥 Download JSON Report", data=open(report_file, "rb"), file_name=report_file, mime="application/json")

# View Previous Scans from SQLite
st.subheader("📂 Previous Scan Logs")
conn = sqlite3.connect("security_scans.db")
df = pd.read_sql_query("SELECT * FROM scans ORDER BY timestamp DESC", conn)
conn.close()

if not df.empty:
    st.dataframe(df)
else:
    st.write("No previous scans found.")

# **New Button to Clear Scan History**
st.subheader("🗑️ Manage Scan Data")
if st.button("🧹 Clear Scan History"):
    clear_scan_history()

# Footer
st.markdown("---")
st.markdown("🔹 Developed with ❤️ using **Streamlit + LangChain + Groq AI**")