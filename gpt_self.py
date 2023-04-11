import sys
import json

from pyllamacpp.model import Model
from enum import IntEnum



tokens_max_input = 2048
model_args = 'gpt_model_args.json'

model_file = './local-gpt/converted-model/converted-gpt4all-lora-quantized.bin'


tokens_to_generate = 500
text_input_truncate = int(tokens_max_input*3.9)


def get_model_args(args_file):
    return json.loads(open(args_file).read())

def on_text(text):
    print(text, end="", flush=True)

def generate_once(model, prompt, tokens_to_generate, args):
    if len(prompt) > text_input_truncate:
        print(f'WARNING! Truncating from {len(prompt)} to last {text_input_truncate} characters')
        prompt = prompt[-text_input_truncate:]
    generated_text = model.generate(prompt, new_text_callback=on_text, n_predict=tokens_to_generate, **args)
    if generated_text.strip().startswith(prompt):
        generated_text = generated_text[len(prompt):]
    return generated_text

def generate_from_template(model, template, goal, context):
    global tokens_to_generate
    global model_args
    prompt = template.replace('{{goal}}', goal).replace('{{context}}', context)
    return generate_once(model, prompt, tokens_to_generate, model_args)

class State(IntEnum):
    START = 0
    SUBDIVIDE_GOAL = 1
    DOES_FUNCTION_SOLVE = 2
    CHOOSE_FUNCTION = 3
    CHOOSE_FUNCTION_ARGS = 4
    PRODUCE_NEW_FUNCTION = 5
    DEBUG_FUNCTION = 6
    DOCUMENT_FUNCTION = 7
    CALL_FUNCTION = 8
    ASK_DONE = 9


# TODO get from vector db based on closest match to current sub-goal
available_functions = \
'''Available functions:

def print_hello_name(name: str) -> str:
    ```hello_name

    prints a string saying hello to the passed name, and then returns empty string
    ```

def multiply(a: int, b: int) -> int:
    ```multiply

    multiplies the two numbers and returns the result
    ```
'''

if __name__ == '__main__':
    get_model_args(model_args)  # make sure it works
    model = Model(ggml_model=model_file, n_ctx=tokens_max_input)

    prompt_template = open('prompt_template.txt').read().strip()

    model_args = get_model_args(model_args)

    ultimate_goal = 'print out the phrase "hello world"' # TODO user input

    goal = ultimate_goal
    state = State.START
    function = None
    function_args = []
    while True:
        if state == State.START:
            state = State.DOES_FUNCTION_SOLVE
            continue
        elif state == State.DOES_FUNCTION_SOLVE:
            context = available_functions + '\n\nWould calling one of these functions solve your goal? Answer YES or NO.'
            resp = generate_from_template(model, prompt_template, goal, context)
            if resp.lower() == 'yes':
                state = State.CHOOSE_FUNCTION
            elif resp.lower() == 'no':
                state = State.SUBDIVIDE_GOAL
            else:
                raise RuntimeError()
        elif state == State.CHOOSE_FUNCTION:
            function = None
            context = available_functions + '\n\nWhich function best solves your goal? Answer with the name of the function.'
            resp = generate_from_template(model, prompt_template, goal, context)
            function = resp
        elif state == State.CHOOSE_FUNCTION_ARGS:
            if function is None:
                raise RuntimeError()
            context = f'You will call {function}, what arguments will you pass?'
            resp = generate_from_template(model, prompt_template, goal, context)
            # TODO you are done here, just put it together and eval
        else:
            raise NotImplementedError


