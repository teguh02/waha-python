# WAHA Python

**Unofficial** Python client library for [WAHA (WhatsApp HTTP API)](https://waha.devlike.pro) - a powerful solution to interact with WhatsApp Web through HTTP API.

[![Unofficial](https://img.shields.io/badge/Status-Unofficial-red.svg)](https://github.com/teguh02/waha-python)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![WAHA](https://img.shields.io/badge/WAHA-2025.9-orange.svg)](https://waha.devlike.pro)

## Features

✅ **Complete API Coverage** - Support for all WAHA endpoints
- 📤 **Send Messages**: Text, Image, Video, Voice, File, Location, Contact, Poll
- 📥 **Receive Messages**: Webhooks and Event Handling
- 💬 **Chats Management**: List, Archive, Read, Delete
- 👤 **Contacts Management**: Get, Update, Block, Check Existence
- 👥 **Groups Management**: Create, Manage, Admin Controls
- 🟢 **Status Management**: Send and Manage WhatsApp Status
- 📢 **Channels Management**: Create and Manage Channels
- 🔐 **Session Management**: Create, Start, Stop, QR Code
- And much more!

✅ **Simple & Intuitive** - Clean, Pythonic API design
✅ **Type Hints** - Full type hints for better IDE support
✅ **Error Handling** - Comprehensive error handling
✅ **Documentation** - Complete documentation and examples

## Installation

```bash
pip install waha-python
```

Or install from source:

```bash
git clone https://github.com/teguh02/waha-python.git
cd waha-python
pip install -e .
```

## Quick Start

### 1. Start WAHA Server

First, you need to have WAHA server running. Follow the [Quick Start Guide](https://waha.devlike.pro/docs/overview/quick-start/):

```bash
docker pull devlikeapro/waha
docker run -it --env-file .env -v "$(pwd)/sessions:/app/.sessions" --rm -p 3000:3000 --name waha devlikeapro/waha
```

### 2. Use the Python Client

```python
from waha_python import WAHAClient

# Initialize the client
client = WAHAClient(
    base_url="http://localhost:3000",
    api_key="your-api-key-here"  # Optional, if you set WAHA_API_KEY
)

# Send a text message
result = client.messages.send_text(
    session="default",
    chat_id="1234567890@c.us",
    text="Hello from Python! 👋"
)

print(f"Message sent: {result}")
```

### 3. Create Session with QR Code

```python
# Create a new session
session = client.sessions.create(
    name="my_session",
    config={
        "webhooks": [{
            "url": "https://your-webhook-url.com/webhook",
            "events": ["message"]
        }]
    }
)

# Get QR code for authentication
qr_code = client.sessions.get_qr("my_session", accept_json=True)
print(f"QR Code (Base64): {qr_code['data']}")

# Scan the QR code with your WhatsApp app
# The session status will change to WORKING
```

### 4. Receive Messages with Webhooks

```python
from flask import Flask, request

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    
    if data.get("event") == "message":
        payload = data["payload"]
        from_number = payload["from"]
        message_text = payload.get("body", "")
        
        print(f"Received: {message_text} from {from_number}")
        
        # Reply to the message
        client.messages.send_text(
            session=data["session"],
            chat_id=from_number,
            text=f"You said: {message_text}"
        )
    
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

## Complete Examples

### Send Different Types of Messages

```python
# Send text message
client.messages.send_text(
    session="default",
    chat_id="1234567890@c.us",
    text="Hello World!"
)

# Send image with URL
client.messages.send_image(
    session="default",
    chat_id="1234567890@c.us",
    file={"url": "https://example.com/image.jpg", "mimetype": "image/jpeg"},
    caption="Check this out!"
)

# Send image from file
client.messages.send_image(
    session="default",
    chat_id="1234567890@c.us",
    file="path/to/image.jpg",
    caption="My image"
)

# Send video
client.messages.send_video(
    session="default",
    chat_id="1234567890@c.us",
    file={"url": "https://example.com/video.mp4", "mimetype": "video/mp4"}
)

# Send voice message
client.messages.send_voice(
    session="default",
    chat_id="1234567890@c.us",
    file={"url": "https://example.com/voice.opus", "mimetype": "audio/ogg; codecs=opus"}
)

# Send document
client.messages.send_file(
    session="default",
    chat_id="1234567890@c.us",
    file={"url": "https://example.com/document.pdf", "mimetype": "application/pdf"}
)

# Send location
client.messages.send_location(
    session="default",
    chat_id="1234567890@c.us",
    latitude=38.8937255,
    longitude=-77.0969763,
    title="My Location"
)

# Send contact
client.messages.send_contact(
    session="default",
    chat_id="1234567890@c.us",
    contacts=[{
        "fullName": "John Doe",
        "organization": "Company",
        "phoneNumber": "+91 11111 11111",
        "whatsappId": "911111111111"
    }]
)

# Send poll
client.messages.send_poll(
    session="default",
    chat_id="1234567890@c.us",
    poll={
        "name": "How are you?",
        "options": ["Awesome!", "Good!", "Not bad!"],
        "multipleAnswers": False
    }
)
```

### Manage Sessions

```python
# List all active sessions
sessions = client.sessions.list()

# List all sessions including stopped ones
all_sessions = client.sessions.list(all_sessions=True)

# Get specific session
session = client.sessions.get("default")

# Create session
new_session = client.sessions.create(
    name="my_session",
    config={"webhooks": [...]}
)

# Start session
client.sessions.start("my_session")

# Stop session
client.sessions.stop("my_session")

# Restart session
client.sessions.restart("my_session")

# Logout session
client.sessions.logout("my_session")

# Delete session
client.sessions.delete("my_session")

# Get QR code
qr = client.sessions.get_qr("default", accept_json=True)

# Request pairing code
code_info = client.sessions.request_code("default", "12132132130")
print(f"Pairing code: {code_info['code']}")
```

### Manage Chats

```python
# List all chats
chats = client.chats.list("default")

# Get chat picture
picture = client.chats.get_picture("default", "1234567890@c.us")

# Archive chat
client.chats.archive("default", "1234567890@c.us")

# Unarchive chat
client.chats.unarchive("default", "1234567890@c.us")

# Mark as unread
client.chats.unread("default", "1234567890@c.us")

# Read messages
client.chats.read_messages("default", "1234567890@c.us")

# Get messages
messages = client.chats.get_messages("default", "1234567890@c.us", limit=100)

# Get specific message
message = client.chats.get_message(
    "default",
    "1234567890@c.us",
    "message_id_here"
)

# Delete chat
client.chats.delete("default", "1234567890@c.us")
```

### Manage Contacts

```python
# List all contacts
contacts = client.contacts.list_all("default")

# Get specific contact
contact = client.contacts.get_contact("default", "1234567890")

# Update contact
client.contacts.update(
    "default",
    "1234567890@c.us",
    first_name="John",
    last_name="Doe"
)

# Check if phone exists
result = client.contacts.check_exists("default", "1234567890")
if result["numberExists"]:
    print(f"Chat ID: {result['chatId']}")

# Get contact about
about = client.contacts.get_about("default", "1234567890")

# Get profile picture
profile_pic = client.contacts.get_profile_picture("default", "1234567890")

# Block contact
client.contacts.block("default", "1234567890@c.us")

# Unblock contact
client.contacts.unblock("default", "1234567890@c.us")
```

### Manage Groups

```python
# List all groups
groups = client.groups.list("default")

# Get specific group
group = client.groups.get("default", "1234567890@g.us")

# Create group
new_group = client.groups.create(
    "default",
    "My New Group",
    participants=["1234567890@c.us"]
)

# Update group name
client.groups.update_subject("default", "1234567890@g.us", "Updated Name")

# Update group description
client.groups.update_description("default", "1234567890@g.us", "Description")

# Get invite code
invite_code = client.groups.get_invite_code("default", "1234567890@g.us")

# Revoke invite code
client.groups.revoke_invite_code("default", "1234567890@g.us")

# Get participants
participants = client.groups.get_participants("default", "1234567890@g.us")

# Add participants
client.groups.add_participants(
    "default",
    "1234567890@g.us",
    ["9876543210@c.us"]
)

# Remove participants
client.groups.remove_participants(
    "default",
    "1234567890@g.us",
    ["9876543210@c.us"]
)

# Promote to admin
client.groups.promote_admin(
    "default",
    "1234567890@g.us",
    ["9876543210@c.us"]
)

# Demote from admin
client.groups.demote_admin(
    "default",
    "1234567890@g.us",
    ["9876543210@c.us"]
)

# Leave group
client.groups.leave("default", "1234567890@g.us")
```

### Manage Status (Stories)

```python
# Send text status
client.status.send_text("default", "My status update")

# Send image status
client.status.send_image(
    "default",
    file={"url": "https://example.com/image.jpg", "mimetype": "image/jpeg"}
)

# Send video status
client.status.send_video(
    "default",
    file={"url": "https://example.com/video.mp4", "mimetype": "video/mp4"}
)

# Send voice status
client.status.send_voice(
    "default",
    file={"url": "https://example.com/voice.opus", "mimetype": "audio/ogg; codecs=opus"}
)

# Delete status
client.status.delete("default", "message_id_here")

# Get new message ID
message_id = client.status.get_new_message_id("default")
```

### Manage Channels

```python
# List all channels
channels = client.channels.list("default")

# Get specific channel
channel = client.channels.get("default", "channel_id")

# Create channel
new_channel = client.channels.create("default", "My Channel", "Description")

# Get channel messages
messages = client.channels.get_messages("default", "channel_id", limit=100)

# Delete channel
client.channels.delete("default", "channel_id")
```

### Message Reactions and Actions

```python
# Add reaction
client.messages.add_reaction(
    session="default",
    message_id="message_id_here",
    reaction="👍"
)

# Remove reaction
client.messages.add_reaction(
    session="default",
    message_id="message_id_here",
    reaction=""
)

# Star message
client.messages.star_message(
    session="default",
    chat_id="1234567890@c.us",
    message_id="message_id_here"
)

# Unstar message
client.messages.star_message(
    session="default",
    chat_id="1234567890@c.us",
    message_id="message_id_here",
    star=False
)

# Edit message
client.messages.edit_message(
    session="default",
    chat_id="1234567890@c.us",
    message_id="message_id_here",
    text="Updated message"
)

# Delete message
client.messages.delete_message(
    session="default",
    chat_id="1234567890@c.us",
    message_id="message_id_here"
)

# Forward message
client.messages.forward_message(
    session="default",
    chat_id="1234567890@c.us",
    message_id="message_id_here"
)

# Pin message
client.messages.pin_message(
    session="default",
    chat_id="1234567890@c.us",
    message_id="message_id_here"
)

# Unpin message
client.messages.unpin_message(
    session="default",
    chat_id="1234567890@c.us",
    message_id="message_id_here"
)
```

## Error Handling

```python
from waha_python import WAHAClient, WAHAAuthenticationError, WAHANotFoundError

try:
    client = WAHAClient(base_url="http://localhost:3000", api_key="wrong-key")
    result = client.messages.send_text(
        session="default",
        chat_id="1234567890@c.us",
        text="Hello"
    )
except WAHAAuthenticationError:
    print("Authentication failed")
except WAHANotFoundError:
    print("Resource not found")
except Exception as e:
    print(f"Error: {e}")
```

## Using Context Manager

```python
from waha_python import WAHAClient

with WAHAClient(base_url="http://localhost:3000", api_key="your-key") as client:
    result = client.messages.send_text(
        session="default",
        chat_id="1234567890@c.us",
        text="Hello from context manager!"
    )
# Client is automatically closed
```

## Requirements

- Python 3.8+
- requests library
- WAHA server running (see [Quick Start Guide](https://waha.devlike.pro/docs/overview/quick-start/))

## Documentation

- [WAHA Documentation](https://waha.devlike.pro)
- [WAHA GitHub](https://github.com/devlikeapro/waha)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Support

- GitHub Issues: [https://github.com/teguh02/waha-python/issues](https://github.com/teguh02/waha-python/issues)
- WAHA Documentation: [https://waha.devlike.pro](https://waha.devlike.pro)

## Important Disclaimer

**This is an UNOFFICIAL community project** and is not affiliated, associated, authorized, endorsed by, or in any way officially connected with:
- WhatsApp LLC or any of its subsidiaries or affiliates
- WAHA (devlikeapro) team

The official WhatsApp website can be found at [whatsapp.com](https://whatsapp.com).  
The official WAHA documentation can be found at [waha.devlike.pro](https://waha.devlike.pro).

"WhatsApp" as well as related names, marks, emblems and images are registered trademarks of their respective owners.

### Usage Warning

This library interacts with WhatsApp through unofficial means. There are risks associated with using unofficial WhatsApp clients:
- Account suspension or banning
- Security risks
- Data privacy concerns
- No official support

Use at your own risk. For business applications, we recommend using the [official WhatsApp Business API](https://developers.facebook.com/docs/whatsapp).

