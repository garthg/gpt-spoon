import json

from pyllamacpp.model import Model


tokens_max_input = 2048
model_args = 'gpt_model_args.json'

model_file = './local-gpt/converted-model/converted-gpt4all-lora-quantized.bin'


tokens_to_generate = 500
text_input_truncate = int(tokens_max_input*3.9)


def get_args(args_file):
    return json.loads(open(args_file).read())

def on_text(text):
    print(text, end="", flush=True)

def generate_once(model, prompt, tokens_to_generate, args):
    generated_text = model.generate(prompt, new_text_callback=on_text, n_predict=tokens_to_generate, **args)
    if generated_text.startswith(prompt):
        generated_text = generated_text[len(prompt):]
    return generated_text


get_args(model_args)  # make sure it works
model = Model(ggml_model=model_file, n_ctx=tokens_max_input)

while True:
    args = get_args(model_args)
    user_prompt = input('> ')
    user_prompt_clean = user_prompt.lstrip('>').strip()
    resp = generate_once(model, user_prompt_clean, tokens_to_generate, args)
    print('------------')
    print(resp)
    print()

