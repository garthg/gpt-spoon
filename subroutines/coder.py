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
    resp = resp.replace(' ', '_')
    if not resp.endswith('.py'):
        resp += '.py'
    return resp


def implement_single_function(requirements, target_function, other_functions):
    if other_functions:
        other_list = '\n'.join(other_functions)
        other_block = 'These other functions are available:\n'+other_list
    else:
        other_block = ''
    prompt = func_p.format(requirements=requirements, function=target_function, other_functions=other_block)
    print(prompt)
    return gpt.complete(prompt)


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
            fid.write(impl)
            fid.write('\n\n')


if __name__ == '__main__':
    print(here)
    implement(sys.argv[1])
