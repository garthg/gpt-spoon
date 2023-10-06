import os
import sys

from subroutines import gpt_localhost4all as gpt
#from subroutines import gpt_openai as gpt


arch_p = """You are a programmer designing a program to accomplish these requirements. Requirements:
{requirements}

Bulleted list of the simplest set of Python function signatures required to implement this, one per line, with no other text:"""


func_p = """You are a Python programmer. Program requirements:
{requirements}

{other_functions}Function to implement:
{function}

Python implementation of this, with no other text:"""


filename_p = """Filename of a program for these requirements:
{requirements}
Filename: """


comment_p = """In a program these requirements:
{requirements}

For this function:
{function}

One line comment describing this function: """



here = os.path.dirname(__file__)


def architect(requirements):
    #resp = gpt.complete(arch_p.format(requirements=requirements))
    resp = "1) def first_n(n):  # returns the first n Fibonacci numbers"
    lines = resp.split('\n')
    out = []
    for l in lines:
        clean = l.strip().lstrip('1234567890).-')
        if clean:
            out.append(clean)
    return out


def filename(requirements):
    #resp = gpt.complete(filename_p.format(requirements=requirements))
    resp = 'sequence'
    resp = resp.strip().replace(' ', '_')
    if not resp.endswith('.py'):
        resp = resp.rstrip('.') + '.py'
    return resp


def implement_single_function(requirements, target_function, other_functions):
    if other_functions:
        other_list = '\n'.join(other_functions)
        other_block = 'These other functions are available:\n'+other_list
    else:
        other_block = ''
    prompt = func_p.format(requirements=requirements, function=target_function, other_functions=other_block)
    print(prompt)
    #out = gpt.complete(prompt)
    out = """def first_n(n):
if n == 0 or n == 1:
    return [0] * (n+2)

else:
    fib = [0, 1]
    for i in range(2,n+1):
        fib.append(fib[i-1]+fib[i-2])

    return fib[:n]"""
    print('=-=')
    print(out)
    print('=-=')
    return out


def describe_function(requirements, target_function):
    if '#' in target_function:
        desc = target_function.partition('#')[2]
    else:
        desc = gpt.complete(comment_p.format(requirements=requirements, function=target_function))
    if not desc.startswith('#'):
        desc = '#' + desc
    return desc



def implement(requirements):
    funcs = architect(requirements)
    print('Functions:')
    print(funcs)
    name = filename(requirements)
    print('Filename:')
    print(name)
    with open(os.path.join(here, name), 'w') as fid:
        for i in range(len(funcs)):
            others = funcs[:i]+funcs[i+1:]
            f = funcs[i]
            impl = implement_single_function(requirements, f, others)
            comment = describe_function(requirements, f)
            fid.write(comment + '\n')
            fid.write(impl)
            fid.write('\n\n')
    print('>>>>>>> implemented')


if __name__ == '__main__':
    print(here)
    implement(sys.argv[1])
