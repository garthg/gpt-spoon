from pyllamacpp.model import Model


def on_text(text):
    print(text, end="", flush=True)

model = Model(ggml_model='./local-gpt/converted-model/converted-gpt4all-lora-quantized.bin', n_ctx=2048)
tokens_to_generate = 55
prompt = 'Once upon a time, '
generated_text = model.generate(prompt, new_text_callback=on_text, n_predict=tokens_to_generate, temp=.1)
print(generated_text)

