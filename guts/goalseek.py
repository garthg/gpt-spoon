import sys
import os

from guts import gpt_openai as gpt
from guts import list_all_funcs


system_prompt = """Goal: {goal}

Choose actions to best accomplish that goal.

Reply with one of the following:
- ACTION <name>: take an available action from the list of actions
- NEW <description>: develop a new action to solve the goal
- OUTPUT: the text output of the last action fulfills the goal
- DONE: state that the goal is accomplished without sending output"""


blacklisted_files = set([
    os.path.basename(__file__),
    'mainloop.py',
    'gpt_openai.py',
    'list_all_funcs.py',
])


def available_actions_text():
    funcs = list_all_funcs.get_top_level_functions('guts')
    print(funcs)
    list = 'Available actions:\n'+'\n'.join(f[0].replace('.py', '')+'.'+f[1] for f in funcs if f[0] not in blacklisted_files)
    return list+'\n\n'+'Or, make a new action by writing NEW followed by the desired action.'


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
        break # DEBUGGING
    return True, ''


if __name__ == '__main__':
    print(goalseek(sys.argv[1]))
