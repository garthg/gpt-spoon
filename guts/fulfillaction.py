from subroutines import listactions
from subroutines import gpt_localhost4all as gpt

action_prompt = open('action_prompt.txt').read()

def action(request):
    actions = list_actions()
    filled = action_prompt.replace('{functions}', '\n'.join(actions)).replace('{goal}', request)
    target_action = gpt.complete(filled)
    print(target_action)
