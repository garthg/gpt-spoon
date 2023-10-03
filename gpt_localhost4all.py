import openai

openai.api_base = "http://localhost:4891/v1"

openai.api_key = "not needed for a local LLM"

prompt = "Who is Michael Jordan?"

model = "gpt4all-j-v1.3-groovy"

response = openai.Completion.create(
    model=model,
    prompt=prompt,
    max_tokens=50,
    temperature=0.28,
    top_p=0.95,
    n=1,
    echo=True,
    stream=False
)
print(response)
