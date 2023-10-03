from subroutines import gpt_localhost4all as gpt

main_loop_prompt = open('main_loop_prompt.txt').read()


def run_once_chat():   
    print('Okay chief')
    print()
    done = False
    messages = [{'role':'system','content':main_loop_prompt}]
    while not done:
        print('@__ ', end='')
        user = input()
        messages.append({'role':'user','content':user})
        print('------------')
        print(messages)
        assistant = gpt.chat_complete(messages)
        print(assistant)
        messages.append({'role':'assistant','content':assistant})
        if assistant.lower().strip().startswith('DONE'):
            done = True


def run_once_complete():   
    print('Okay chief')
    print()
    done = False
    messages = []
    while not done:
        print('@__ ', end='')
        user = input()
        messages.append({'role':'user','content':user})
        print('------------')
        text = main_loop_prompt.replace('{messages}', '\n'.join(x['role']+': '+x['content'] for x in messages))
        print(text)
        assistant = gpt.complete(text)
        print(assistant)
        messages.append({'role':'assistant','content':assistant})
        if assistant.lower().strip().startswith('DONE'):
            done = True
