import streamlit as st
import requests

st.set_page_config(page_title="Insight Dashboard", layout="wide")

# API_URL = "http://localhost:8000"  # Orchestrator service URL
API_URL = "http://backend:8000"


st.title(" Insight Platform")

with st.sidebar:
    st.header("Actions")
    new_url = st.text_input("Submit a new article URL:")
    if st.button("Run Insight Pipeline"):
        if new_url:
            response = requests.post(f"{API_URL}/run_pipeline", json={"url": new_url})
            st.write(response.json())
        else:
            st.warning("Please enter a valid URL.")

st.header("Published Insights")

insights_response = requests.get(f"{API_URL}/list_insights")
if insights_response.status_code == 200:
    insights = insights_response.json().get("insights", [])
    for item in insights:
        with st.expander(item["title"]):
            st.markdown(f"**Tags:** {', '.join(item['tags'])}")
            st.markdown(item["summary"])
            st.markdown(f"[Original]({item['source_url']})")
else:
    st.error("Failed to load insights.")

st.header("Protocol Logs")
if st.button("Download Logs"):
    logs_response = requests.get(f"{API_URL}/logs/protocols")
    if logs_response.status_code == 200:
        st.download_button("Download protocol_trace.json", logs_response.content, file_name="protocol_trace.json")
    else:
        st.error("No logs available or server not reachable.")
