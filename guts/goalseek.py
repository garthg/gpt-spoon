import sys
import os
import json
import importlib
import inspect

from guts import gpt_openai as gpt
from guts import list_all_funcs


system_prompt = """Goal: {goal}

Choose actions to best accomplish that goal.

Reply with one of the following:
- ACTION <name>: take an available action from the list of actions
- NEW <description>: develop a new action to solve the goal
- OUTPUT: the text output of the last action fulfills the goal
- DONE: state that the goal is accomplished without sending output"""


action_prompt = """Produce a Json object that describes the arguments to <<<action>>><<<signature>>> to accomplish the goal, like this:
```
{
  "args": [...],  # list of positional arguments
  "kwargs": {"k": "v", ...}  # dict of keyword arguments
}
```
Reply with the Json and no other text."""

action_prompt2 = """Produce Python code executing the function <<<action>>> to accomplish the goal stated above. Reply with the code and no other text."""



blacklisted_files = set([
    os.path.basename(__file__),
    'mainloop.py',
    'gpt_openai.py',
    'list_all_funcs.py',
    'coder3.py',
])


def available_actions_text():
    funcs = list_all_funcs.get_top_level_functions('guts')
    print(funcs)
    list = 'Available actions:\n'+'\n'.join(f[0].replace('.py', '')+'.'+f[1] for f in funcs if f[0] not in blacklisted_files)
    return list+'\n\n'+'Or, make a new action by writing NEW followed by the desired action.'


def execute(function, args, kwargs):
    return function(*args, **kwargs)


def import_chosen_func(module_name, function_name):
    m = importlib.import_module('guts.'+module_name)
    f = getattr(m, function_name)
    return f


def goalseek(goal):
    messages = [{'role':'system','content':system_prompt.format(goal=goal)}]
    done = False
    while not done:
        messages.append({'role':'user','content':available_actions_text()})
        print('------------')
        print(messages)
        assistant = gpt.chat_complete(messages)
        print(assistant)
        messages.append({'role':'assistant','content':assistant})
        if assistant.lower().strip().startswith('action'):
            action = assistant.split()[-1].strip()
            action_parts = action.split('.')
            if len(action_parts) != 2:
                raise RuntimeError(f'Failed to parse an action from: {assistant}')
            func = import_chosen_func(action_parts[0], action_parts[1])
            sig = inspect.signature(func)
            messages.append({'role':'user','content':action_prompt.replace('<<<action>>>', action).replace('<<<signature>>>', str(sig))})
            print(messages)
            assistant = gpt.chat_complete(messages)
            print(assistant)
            data = json.loads(assistant)
            return execute(func, data['args'], data['kwargs'])
        break # DEBUGGING
    return True


if __name__ == '__main__':
    res = goalseek(sys.argv[1])
    print('-----------------------')
    print()
    print(res)
