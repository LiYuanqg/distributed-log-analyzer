from kafka import KafkaProducer
import json
import time
import random

# Connect to your Kafka broker
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # if running outside Docker
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = "logs"

def generate_fake_log():
    levels = ["INFO", "WARNING", "ERROR"]
    return {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "level": random.choice(levels),
        "message": f"User action {random.randint(1000, 9999)} occurred"
    }

print("🚀 Sending logs to Kafka topic:", topic)
for i in range(100):
    log = generate_fake_log()
    producer.send(topic, value=log)
    print(f"[Sent] {log}")
    time.sleep(0.2)  # simulate continuous log streaming

producer.flush()
print("✅ Done sending logs.")
