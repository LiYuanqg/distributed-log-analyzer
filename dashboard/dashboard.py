import pandas as pd
import streamlit as st

# ---------------------------
# Load CSV
# ---------------------------
DATA_FILE = "../data/parsed_logs.csv"
df = pd.read_csv(DATA_FILE)

# ---------------------------
# Streamlit Layout
# ---------------------------
st.title("Distributed Log Analyzer Dashboard")

# Show raw logs
st.subheader("Raw Logs")
st.dataframe(df)

# ---------------------------
# Summary Metrics
# ---------------------------
st.subheader("Summary Metrics")
log_counts = df['Type'].value_counts()
st.write("Log counts by type:")
st.bar_chart(log_counts)

# Logs per Node
st.subheader("Logs per Node")
node_counts = df['Node'].value_counts()
st.bar_chart(node_counts)

# ---------------------------
# Filter Logs
# ---------------------------
st.subheader("Filter Logs")
selected_type = st.multiselect("Select log type:", options=df['Type'].unique(), default=df['Type'].unique())
selected_node = st.multiselect("Select node:", options=df['Node'].unique(), default=df['Node'].unique())

filtered_df = df[(df['Type'].isin(selected_type)) & (df['Node'].isin(selected_node))]
st.dataframe(filtered_df)

# ---------------------------
# Timeline of Alarms
# ---------------------------
st.subheader("Timeline of Alarms")
alarm_df = df[df['Type'] == "ALARM"]
if not alarm_df.empty:
    alarm_df['Timestamp'] = pd.to_datetime(alarm_df['Timestamp'])
    alarm_df = alarm_df.sort_values('Timestamp')
    st.line_chart(alarm_df.set_index('Timestamp')['Type'].groupby(alarm_df['Timestamp']).count())
else:
    st.write("No ALARM logs found.")
