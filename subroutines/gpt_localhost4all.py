import sys

import openai

openai.api_base = "http://localhost:4891/v1"
openai.api_key = "not needed for a local LLM"

model = "gpt4all-j-v1.3-groovy"

top_p=0.4
max_tokens=4096


def complete(prompt, temperature=1.0):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        n=1,
        echo=False,
        stream=False
    )
    return response['choices'][0]['text']


def chat_complete(messages, temperature=1.0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )
    return response['choices'][0]['message']['content']



if __name__ == '__main__':
    prompt = sys.argv[1]
    response = complete(prompt)
    #messages = [
    #    {'role':'system','content':'Answer this'},
    #    {'role':'user', 'content':prompt}
    #]
    #response = chat_complete(messages)
    print(response)
