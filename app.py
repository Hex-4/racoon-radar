import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# This sample slack application uses SocketMode
# For the companion getting started setup guide, 
# see: https://slack.dev/bolt-python/tutorial/getting-started 

# Initializes your app with your bot token
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

tips_channel = "C09G9HYDGR3"


# Listens to incoming messages that contain "hello"
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "<https://google.com|new tip!>"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "image",
                        "image_url": "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg",
                        "alt_text": "cute cat"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "@hx4 sent this tip"
                    }
                ]
            }
        ],
        text="new tip! from @hx4"
    )

@app.shortcut("happenings_submit")
def submit(ack, shortcut, client):
    # Acknowledge the shortcut request
    ack()
    
    link 
    
    client.chat_postMessage(
        channel=tips_channel,
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "<https://google.com|new tip!>"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "image",
                        "image_url": shortcut["user"]["profile"]["image_48"],
                        "alt_text": "cute cat"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"<@{shortcut["user"]["id"]}> sent this tip"
                    }
                ]
            }
        ],
        text=f"new tip! <@{shortcut["user"]["id"]}>"
    )


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
