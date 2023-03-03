from . import config
from slack_bolt import App
from slack_sdk.web import WebClient
import ssl as ssl_lib
import certifi
import re
from . import ChatGTP

ssl_context = ssl_lib.create_default_context(cafile=certifi.where())

app = App(
  token = config.SLACK_BOT_TOKEN,
  signing_secret = config.SLACK_SIGNING_SECRET
)

chatgpt = ChatGTP()

def _remove_mention(text):
  """Remove the mention from the text"""
  return re.compile(r'<@[^>]+> ').sub('', text)

@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)

@app.event("app_mention")
def handle_mention(body, say, logger):
  event_user = body.get("event", {}).get("user")
  event_ts = body.get("event", {}).get("ts")
  event_text = _remove_mention(body.get("event", {}).get("text"))

  say(f"<@{event_user}> Processing your request...")

  response_message_text, past_messages = chatgpt.completion(event_text)

  say(f"""\
<@{event_user}>
Req: {event_text[:20]} {"..." if len(event_text) > 20 else ""}
====================
{response_message_text}
""")
