import openai
from . import config

class ChatGTP:
  def __init__(self): 
    openai.api_key = config.OPENAI_API_KEY
    self.past_messages = []
  
  def completion(self, new_message_text:str, settings_text:str = ''):
    """
    This function generates a response message using OpenAI's GPT-3 model by taking in a new message text, 
    optional settings text and a list of past messages as inputs.

    Args:
    new_message_text (str): The new message text which the model will use to generate a response message.
    settings_text (str, optional): The optional settings text that will be added as a system message to the past_messages list. Defaults to ''.
    past_messages (list, optional): The optional list of past messages that the model will use to generate a response message. Defaults to [].

    Returns:
    tuple: A tuple containing the response message text and the updated list of past messages after appending the new and response messages.
    """
    # if len(past_messages) == 0 and len(settings_text) != 0:
    #   system = {"role": "system", "content": settings_text}
    #   past_messages.append(system)
    new_message = {"role": "user", "content": new_message_text}
    self.past_messages.append(new_message)

    result = openai.ChatCompletion.create(
      model=config.CHATGPT_MODEL,
      messages=self.past_messages
    )
    response_message = {"role": "assistant", "content": result.choices[0].message.content}
    self.past_messages.append(response_message)
    response_message_text = result.choices[0].message.content
    return response_message_text, self.past_messages, result

if __name__ == "__main__":
  chatgpt = ChatGTP()
  response_message_text, past_messages = chatgpt.completion("""\
Hello World Hello World Hello World Hello World Hello World Hello World Hello World Hello World hello
""")
  print(response_message_text)