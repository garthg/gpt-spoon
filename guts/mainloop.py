#from guts import gpt_localhost4all as gpt
from guts import gpt_openai as gpt
from guts import goalseek

main_loop_prompt = open('guts/main_loop_prompt.txt').read()


def run_once_chat():   
    print('Okay chief')
    print()
    done = False
    messages = [{'role':'system','content':main_loop_prompt}]
    while not done:
        print('>__> ', end='')
        user = input()
        if user.strip().lower() in ('quit', 'exit', 'die', 'stop'):
            break
        messages.append({'role':'user','content':user})
        print('------------')
        print(messages)
        assistant = gpt.chat_complete(messages)
        print(assistant)
        messages.append({'role':'assistant','content':assistant})
        if assistant.strip().lower().startswith('goalseek'):
            success, output = goalseek.goalseek(assistant[8:])
            messages.append({'role':'system', 'content': f'Goalseek result: {success}\nOputput: {output}'})



def run_once_complete():   
    print('Okay chief')
    print()
    done = False
    messages = []
    while not done:
        print('>__> ', end='')
        user = input()
        messages.append({'role':'user','content':user})
        print('------------')
        text = main_loop_prompt.replace('{messages}', '\n'.join(x['role']+': '+x['content'] for x in messages))
        print(text)
        assistant = gpt.complete(text)
        print(assistant)
        messages.append({'role':'assistant','content':assistant})
        assistant_strip = assistant.strip()
        first_word = assistant_strip.partition(' ')[0].lower()
        if first_word.startswith('done'):
            done = True
            break
        if first_word.startswith('action'):
            fullfillac

def run_once():
    # choose which one here
    #run_once_complete()       
    run_once_chat()
        
