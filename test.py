import os

from groq import Groq

client = Groq(
    api_key="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",
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Can you generate information about multivariable derivative",
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)




