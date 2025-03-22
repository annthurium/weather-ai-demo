from dotenv import load_dotenv
load_dotenv()

import os
import openai
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai.client import LDAIClient, AIConfig, ModelConfig
import uuid


ldclient.set_config(Config(os.getenv("LAUNCHDARKLY_SDK_KEY")))

ld_ai_client = LDAIClient(ldclient.get())
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate(**kwargs):
    """
    Calls OpenAI's chat completion API to generate some text based on a prompt.

    """
    import uuid
    user_id = str(uuid.uuid4())
    context = Context.builder(user_id).kind('user').name('Sandy').build()
    try:
        ai_config_key = "weather-assistant"
        default_value = AIConfig(
        enabled=True,
        model=ModelConfig(name='gpt-4o'),
        messages=[],
        )
        config_value, tracker = ld_ai_client.config(
        ai_config_key,
        context,
        default_value,
        kwargs
    )
        model_name = config_value.model.name
        print("CONFIG VALUE: ", config_value)
        print("MODEL NAME: ", model_name)
        messages = [] if config_value.messages is None else config_value.messages
        completion = tracker.track_openai_metrics(
            lambda:
                openai_client.chat.completions.create(
                    model=model_name,
                    messages=[message.to_dict() for message in messages],
                )
        )
        response = completion.choices[0].message.content
        print("Success.")
        print("AI Response:", response)
        return response

    except Exception as e:
        print(e)

# generate(NAME="Maria")