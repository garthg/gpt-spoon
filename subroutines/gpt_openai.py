import sys

import openai



temperature = 0.7
top_p=0.4
max_tokens=1024


def complete_oldstyle(prompt):
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


def chat_complete(messages):
    model = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )
    return response['choices'][0]['message']['content']


def complete(prompt):
    model = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{'role':'user', 'content':prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )
    return response['choices'][0]['message']['content']


if __name__ == '__main__':
    prompt = sys.argv[1]
    #response = complete(prompt)
    #messages = [
    #    {'role':'system','content':'Answer this'},
    #    {'role':'user', 'content':prompt}
    #]
    #response = chat_complete(messages)
    response = complete(prompt)
    print(response)
