import sys
import time

import openai



top_p=0.4
max_tokens=1024
sleep_secs = 30


def chat_complete(messages, temperature=1.0):
    model = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )
    return response['choices'][0]['message']['content']


def chat_complete_one(user_message, temperature=1.0, system_message=''):
    messages = []
    if system_message:
        messages.append({'role':'system', 'content':system_message})
    messages.append({'role':'user', 'content':user_message})
    return chat_complete(messages, temperature)


def complete(prompt, temperature=1.0):
    model = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{'role':'user', 'content':prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )
    time.sleep(sleep_secs)
    return response['choices'][0]['message']['content']


if __name__ == '__main__':
    prompt = sys.argv[1]
    
    #response = complete(prompt)
    
    response = chat_complete_one(prompt, system_message='Respond briefly to this')
    
    print(response)
