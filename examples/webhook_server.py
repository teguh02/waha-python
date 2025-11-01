"""
Example webhook server to receive messages from WAHA
"""

from flask import Flask, request
from waha_python import WAHAClient

app = Flask(__name__)

# Initialize WAHA client
client = WAHAClient(
    base_url="http://localhost:3000",
    api_key="your-api-key-here"  # Optional
)

@app.route("/webhook", methods=["POST"])
def webhook():
    """Handle incoming webhook from WAHA"""
    data = request.get_json()
    
    event_type = data.get("event")
    session = data.get("session")
    payload = data.get("payload", {})
    
    print(f"\n=== New Event: {event_type} ===")
    print(f"Session: {session}")
    
    if event_type == "message":
        # Handle incoming message
        from_number = payload.get("from", "Unknown")
        message_text = payload.get("body", "")
        has_media = payload.get("hasMedia", False)
        
        print(f"From: {from_number}")
        print(f"Message: {message_text}")
        print(f"Has Media: {has_media}")
        
        if has_media and payload.get("media"):
            media = payload["media"]
            print(f"Media: {media.get('url', 'N/A')}")
        
        # Echo back the message
        try:
            response = client.messages.send_text(
                session=session,
                chat_id=from_number,
                text=f"Echo: {message_text}"
            )
            print(f"Replied successfully: {response}")
        except Exception as e:
            print(f"Error sending reply: {e}")
    
    elif event_type == "session.status":
        # Handle session status change
        status = payload.get("status", "Unknown")
        print(f"Session Status: {status}")
        
        if status == "WORKING":
            print("✅ Session is now working!")
        elif status == "SCAN_QR_CODE":
            print("📱 Please scan QR code")
        elif status == "FAILED":
            print("❌ Session failed")
    
    elif event_type == "message.reaction":
        # Handle message reaction
        reaction = payload.get("reaction", {})
        emoji = reaction.get("text", "")
        print(f"Reaction: {emoji}")
    
    else:
        print(f"Event data: {payload}")
    
    return "OK", 200

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return {"status": "OK", "service": "WAHA Webhook Server"}, 200

if __name__ == "__main__":
    print("Starting WAHA Webhook Server...")
    print("Make sure you have configured the webhook URL in your session config")
    print("Webhook URL should be: http://your-server-url:5000/webhook")
    print("\nStarting Flask server on http://0.0.0.0:5000...")
    
    app.run(host="0.0.0.0", port=5000, debug=True)

