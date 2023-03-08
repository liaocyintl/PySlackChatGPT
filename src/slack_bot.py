from . import config
from slack_bolt import App
from slack_sdk.web import WebClient
import ssl as ssl_lib
import certifi
import re
from . import ChatGTP
from openai.error import InvalidRequestError

ssl_context = ssl_lib.create_default_context(cafile=certifi.where())

app = App(
  token = config.SLACK_BOT_TOKEN,
  signing_secret = config.SLACK_SIGNING_SECRET
)

# Set chatgpt instance for each Slack channel
channel_chatgpt = {}

def _remove_mention(text):
  """Remove the mention from the text"""
  return re.compile(r'<@[^>]+>').sub('', text).lstrip()

@app.event("message")
def handle_message_events(body, logger):
  pass

@app.event("app_mention")
def handle_mention(body, say, logger):
  past_messages = []
  result = {}
  try:
    event_user = body.get("event", {}).get("user")
    event_ts = body.get("event", {}).get("ts")
    event_text = _remove_mention(body.get("event", {}).get("text"))
    event_channel = body.get("event", {}).get("channel")

    if event_channel not in channel_chatgpt:
      channel_chatgpt[event_channel] = ChatGTP()
    chatgpt = channel_chatgpt[event_channel]

    # Reset the conversation
    if event_text == "reset":
      chatgpt.past_messages = []
      say(f"Conversation reset.")
      return

    say(f"<@{event_user}> Processing your request...")
    try:
      response_message_text, past_messages, result = chatgpt.completion(event_text)
    except Exception as err:
      raise err

    role_system_number = len([message for message in past_messages if message["role"] == "system"])
    role_assistant_number = len([message for message in past_messages if message["role"] == "assistant"])
    role_user_number = len([message for message in past_messages if message["role"] == "user"])

  except Exception as err:
    say(f"""\
<@{event_user}>
Opps! Something went wrong {err}
Reply `reset` to reset the conversation.
""")
  else:
    say(f"""\
<@{event_user}>
Req: {event_text[:20]} {"..." if len(event_text) > 20 else ""}
Role Count: System {role_system_number}, Assistant {role_assistant_number}, User {role_user_number}. Reply `reset` if you want to reset the conversation.
Token Count: Prompt Tokens {result["usage"]["prompt_tokens"]}, Completion Tokens {result["usage"]["completion_tokens"]}, Total Tokens {result["usage"]["total_tokens"]}
====================
{response_message_text}
""")
