import openai

openai.api_base = "http://localhost:4891/v1"
openai.api_key = "not needed for a local LLM"

model = "gpt4all-j-v1.3-groovy"


def complete(prompt, max_tokens=50, temperature=1.0):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=0.95,
        n=1,
        echo=False,
        stream=False
    )
    return response['choices'][0]['text']


def chat_complete(messages, max_tokens=50, temperature=1.0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response['choices'][0]['message']



if __name__ == '__main__':
    prompt = "What is the velocity of an unladen sparrow? Respond in at most 10 words."
    #response = complete(prompt)
    messages = [
        {'role':'system','content':'Answer this'},
        {'role':'user', 'content':prompt}
    ]
    response = chat_complete(messages)
    print(response)
