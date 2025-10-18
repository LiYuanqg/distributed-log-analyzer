import streamlit as st
from kafka import KafkaConsumer
import json
import pandas as pd
from datetime import datetime
from collections import deque

# Kafka configuration
KAFKA_BROKER = "localhost:9092"  # if Streamlit runs on your host
TOPIC = "logs"

# Set page config
st.set_page_config(page_title="Real-Time Log Dashboard", layout="wide")

st.title("📊 Real-Time Log Dashboard")

# UI elements
log_placeholder = st.empty()
level_chart_placeholder = st.empty()

# Use deque to keep a rolling window of logs
MAX_LOGS = 1000
logs = deque(maxlen=MAX_LOGS)

# Prepare Kafka consumer
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    auto_offset_reset='latest',   # start from latest
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Initialize chart data
level_count = {"INFO": 0, "WARNING": 0, "ERROR": 0}

# Main streaming loop
for message in consumer:
    log = message.value
    logs.appendleft(log)

    # Update level count
    level = log.get("level", "INFO")
    if level in level_count:
        level_count[level] += 1

    # Render logs table
    log_placeholder.table(list(logs)[:20])

    # Prepare chart data
    df = pd.DataFrame(
        {
            "Level": ["INFO", "WARNING", "ERROR"],
            "Count": [level_count["INFO"], level_count["WARNING"], level_count["ERROR"]]
        }
    ).set_index("Level")

    # Render chart
    level_chart_placeholder.bar_chart(df)