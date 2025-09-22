from email import message
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# This sample slack application uses SocketMode
# For the companion getting started setup guide, 
# see: https://slack.dev/bolt-python/tutorial/getting-started 

# Initializes your app with your bot token
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

tips_channel = "C09G9HYDGR3"

@app.shortcut("happenings_submit")
def submit(ack, shortcut, client):
    ack()
    
    # Get the original message that was tipped
    original_message_ts = shortcut["message"]["ts"]
    original_channel = shortcut["channel"]["id"]
    
    duplicate_found = False
    
    message_link = f"https://hackclub.slack.com/archives/{original_channel}/p{original_message_ts.replace('.', '')}"
    
    # Search for duplicates in tips channel
    try:
        history = client.conversations_history(
            channel=tips_channel,
            limit=50
        )
        
        # Check if this message was already tipped
        for message in history["messages"]:
            # Look for messages that contain the original message timestamp
            if "blocks" in message:
                for block in message["blocks"]:
                    if block.get("type") == "section" and "text" in block:
                        text = block["text"].get("text", "")
                        # Check if this tip references the same original message
                        if f"/{original_channel}/p{original_message_ts.replace('.', '')}" in text:
                            duplicate_found = True
                            break
            if duplicate_found:
                break
            
        dm_channel = client.conversations_open(users=[shortcut["user"]["id"]])

        if duplicate_found:
            client.chat_postMessage(
                channel=dm_channel["channel"]["id"], 
                text=f":rac_info: great minds think alike! the Happenings team has already been tipped about <{message_link}|this message>"
            )
        else:
            client.chat_postMessage(
                channel=dm_channel["channel"]["id"], 
                text=f":rac_woah: your <{message_link}|tip> has been sent! the Happenings team will take a look and it might make it into the next edition ^-^"
            )
        
    except Exception as e:
        print(f"Error checking for duplicates: {e}")
        # Continue anyway if duplicate check fails
    
    
    if not duplicate_found:
        # Get user info for avatar
        user_info = client.users_info(user=shortcut["user"]["id"])
        user_profile = user_info["user"]["profile"]

        
        client.chat_postMessage(
            channel=tips_channel,
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<{message_link}|new tip!>"
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "image", 
                            "image_url": user_profile.get("image_48", user_profile.get("image_32")),
                            "alt_text": "user avatar"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"<@{shortcut['user']['id']}> thinks this is worth sharing..."
                        }
                    ]
                }
            ],
            text=f"new tip from <@{shortcut['user']['id']}>"
        )

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
