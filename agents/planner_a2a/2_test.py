import requests
import json

# The endpoint URL you provided
url = "https://planner-agent-680248386202.us-central1.run.app"

# The JSON body for the POST request
payload = {
  "jsonrpc": "2.0",
  "id": 33,
  "method": "message/send",
  "params": {
    "message": {
      "role": "user",
      "parts": [
        { "type": "text", "text": "Plan something for tomorrow in warsaw. I like live music" }
      ],
      "messageId":"foo2"
    },
    "configuration": {
      "acceptedOutputModes": ["text"]
    }
  }
}

# Set the headers to indicate that we are sending JSON
headers = {
    'Content-Type': 'application/json'
}

print(f"Sending POST request to: {url}")
print("Request body:")
# Using json.dumps for pretty printing the dictionary
print(json.dumps(payload, indent=2))

try:
    # Make the POST request
    response = requests.post(url, headers=headers, json=payload)

    # Raise an exception for bad status codes (4xx or 5xx)
    response.raise_for_status()

    # Print the successful response details
    print("\n--- Request Successful ---")
    print(f"Status Code: {response.status_code}")
    
    # Try to parse the response as JSON, otherwise print as text
    try:
        print("Response JSON:")
        # Pretty-print the JSON response
        print(json.dumps(response.json(), indent=2))
    except json.JSONDecodeError:
        print("Response Text:")
        print(response.text)

except requests.exceptions.HTTPError as errh:
    print(f"\n--- HTTP Error ---")
    print(f"An HTTP error occurred: {errh}")
    print(f"Status Code: {errh.response.status_code}")
    print(f"Response Body: {errh.response.text}")
except requests.exceptions.ConnectionError as errc:
    print(f"\n--- Connection Error ---")
    print(f"A connection error occurred: {errc}")
except requests.exceptions.Timeout as errt:
    print(f"\n--- Timeout Error ---")
    print(f"The request timed out: {errt}")
except requests.exceptions.RequestException as err:
    print(f"\n--- An Unexpected Error Occurred ---")
    print(f"An unexpected error occurred: {err}")