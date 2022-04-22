from cortex2 import EmotivCortex2Client
import time 
url = "wss://localhost:6868"

# Remember to start the Emotiv App before you start!
# Start client with authentication
client = EmotivCortex2Client(url,
                            client_id='0DyMfKwKuYAG72VKATaJUI51sEHlyGqpsTk19jPP',
                            client_secret="Nv8JIEu7ew4zsdSbj1xha2vePzAr71JfYNi55oQDvnIOit4wSwctBIAha3XzLs4EbWR9R0ruo1gqUcUJ72UfKFnetgykJfkIfdW3OqqhZ4QcvUvIBmuZOiMBfJrGxk1F",
                            check_response=True,
                            authenticate=True,
                            debug=False)

# Test API connection by using the request access method
client.request_access()

# Explicit call to Authenticate (approve and get Cortex Token)
client.authenticate()

# Connect to headset, connect to the first one found, and start a session for it
client.query_headsets()
client.connect_headset(0)
client.create_session(0)

# Subscribe to the motion and mental command streams
# Spins up a separate subscription thread
client.subscribe(streams=["mot", "com"])

# Test message handling speed
a = client.subscriber_messages_handled
time.sleep(5)
b = client.subscriber_messages_handled
print("bruh", (b - a) / 5)

# Grab a single instance of data
print("data", client.receive_data())


counter = 0
# Continously grab data, while making requests periodically
while True:
    counter += 1
    # time.sleep(0.1)

    if counter % 5000 == 0:
        print(client.request_access())

    # Try stopping the subscriber thread
    if counter == 50000:
        client.stop_subscriber()
        break

    try:
        # Check the latest data point from the motion stream, from the first session
        print(list(client.data_streams.values())[0]['mot'][0])
    except:
        pass
