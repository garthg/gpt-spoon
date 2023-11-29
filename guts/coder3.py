import sys
import os

from guts import gpt_openai as gpt




def binary_completion(prompt):
    response = gpt.chat_complete_one(prompt + ' Answer YES or NO with no other text.')
    return response.lower().strip().startswith('yes')


def is_programmable(goal):
    return binary_completion(f'Goal: {goal}\n\nIs this something that can be accomplished by a computer program with access to the internet?')


def is_one_program(goal):
    return binary_completion(f'Goal: {goal}\n\Can this be implemented by a short Python program? If so answer YES. If it is too large for that, answer NO.')


def get_modules(goal):
    return gpt.chat_complete_one(f'Goal: {goal}\n\nWhat are the sub-components needed for this? Provide a bulleted list with no other text.')


def get_code(goal):
    return gpt.chat_complete_one(f'Goal: {goal}\n\nProvide Python code to implement this. Reply with the code and no other text.')


def get_filename(goal):
    name = gpt.chat_complete_one(f'Goal: {goal}\n\nWhat is a suitable name for a Python file implementing this? Reply with the name and no other text.')
    name = name.replace(' ', '_')
    if not name.endwith('.py'):
        name += '.py'
    return name


def implement(goal, depth=0):
    if depth > 3:
        return False, 'depth exceeded'
    if not is_programmable(goal):
        return False, 'cannot be implemented'
    if not is_one_program(goal):
        modules = get_modules(goal)
        for m in modules:
            implement(m + ' in order to accomplish '+goal, depth+1)
    fname = get_filename(goal)
    code = get_code(goal)
    with open(os.path.join('guts', fname), 'w') as fid:
        fid.write(code)
    return True, ''    
    

if __name__ == '__main__':
    print(implement(sys.argv[1]))
