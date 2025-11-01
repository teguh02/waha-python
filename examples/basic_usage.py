"""
Basic usage examples for WAHA Python client
"""

from waha_python import WAHAClient

# Initialize the client
client = WAHAClient(
    base_url="http://localhost:3000",
    api_key="your-api-key-here"  # Optional if you don't use API key
)

def example_send_message():
    """Example: Send a simple text message"""
    result = client.messages.send_text(
        session="default",
        chat_id="1234567890@c.us",
        text="Hello from WAHA Python! 👋"
    )
    print(f"Message sent: {result}")

def example_create_session():
    """Example: Create a new session with webhook"""
    session = client.sessions.create(
        name="my_session",
        config={
            "webhooks": [{
                "url": "https://your-webhook-url.com/webhook",
                "events": ["message", "session.status"]
            }]
        }
    )
    print(f"Session created: {session}")

def example_get_qr():
    """Example: Get QR code for authentication"""
    qr_data = client.sessions.get_qr("default", accept_json=True)
    print(f"QR Code: {qr_data}")

def example_list_chats():
    """Example: List all chats"""
    chats = client.chats.list("default")
    print(f"Total chats: {len(chats)}")
    for chat in chats[:5]:  # Print first 5 chats
        print(f"  - {chat.get('id', 'Unknown')}")

def example_list_contacts():
    """Example: List all contacts"""
    try:
        contacts = client.contacts.list_all("default")
        print(f"Total contacts: {len(contacts)}")
        for contact in contacts[:5]:  # Print first 5 contacts
            print(f"  - {contact.get('name', 'Unknown')} ({contact.get('id', 'Unknown')})")
    except Exception as e:
        print(f"Error listing contacts: {e}")

def example_check_phone():
    """Example: Check if a phone number exists in WhatsApp"""
    result = client.contacts.check_exists("default", "1234567890")
    if result["numberExists"]:
        print(f"Phone exists! Chat ID: {result['chatId']}")
    else:
        print("Phone number not found in WhatsApp")

def example_send_image():
    """Example: Send an image"""
    result = client.messages.send_image(
        session="default",
        chat_id="1234567890@c.us",
        file={
            "url": "https://github.com/devlikeapro/waha/raw/core/examples/dev.likeapro.jpg",
            "mimetype": "image/jpeg",
            "filename": "image.jpg"
        },
        caption="Check this out! 🖼️"
    )
    print(f"Image sent: {result}")

def example_send_poll():
    """Example: Send a poll"""
    result = client.messages.send_poll(
        session="default",
        chat_id="1234567890@c.us",
        poll={
            "name": "How are you?",
            "options": ["Awesome!", "Good!", "Not bad!"],
            "multipleAnswers": False
        }
    )
    print(f"Poll sent: {result}")

def example_add_reaction():
    """Example: Add reaction to a message"""
    result = client.messages.add_reaction(
        session="default",
        message_id="false_1234567890@c.us_AAAAAAAAAAAAAAAAAA",
        reaction="👍"
    )
    print(f"Reaction added: {result}")

if __name__ == "__main__":
    print("WAHA Python Basic Usage Examples")
    print("=" * 50)
    
    # Uncomment the examples you want to run
    
    # example_send_message()
    # example_create_session()
    # example_get_qr()
    # example_list_chats()
    # example_list_contacts()
    # example_check_phone()
    # example_send_image()
    # example_send_poll()
    # example_add_reaction()
    
    print("\nDone! Uncomment examples in the code to try them.")

