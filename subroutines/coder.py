import os
import sys

from subroutines import gpt_localhost4all as gpt
#from subroutines import gpt_openai as gpt


arch_p = """You are a Python programmer. Program requirements:
{requirements}

Bulleted list of the simplest set of Python function signatures required to implement this, one per line, with no other text:"""


func_p = """You are a Python programmer. Program requirements:
{requirements}

{other_functions}
Function to implement:
{function}

Python implementation of this, with no other text:"""


filename_p = """Filename of a program for these requirements:
{requirements}
Filename: """


comment_p = """In a program with these requirements:
{requirements}

For this function:
{function}

One line comment describing this function:"""


here = os.path.dirname(__file__)


def architect(requirements):
    resp = gpt.complete(arch_p.format(requirements=requirements), temperature=0.7)
    lines = resp.split('\n')
    out = []
    for l in lines:
        clean = l.strip().lstrip('1234567890).-')
        if clean:
            out.append(clean)
    return out


def filename(requirements):
    resp = gpt.complete(filename_p.format(requirements=requirements), temperature=0.1)
    resp = resp.strip().replace(' ', '_')
    if not resp.endswith('.py'):
        resp = resp.rstrip('.') + '.py'
    return resp


def implement_single_function(requirements, target_function, other_functions):
    if other_functions:
        other_list = '\n'.join(other_functions)
        other_block = 'These other functions are available:\n'+other_list+'\n'
    else:
        other_block = ''
    prompt = func_p.format(requirements=requirements, function=target_function, other_functions=other_block)
    print(prompt)
    out = gpt.complete(prompt, temperature=0.2)
    lines = out.split('\n')
    lines = list(filter(lambda x: x.strip() and not x.startswith('```'), lines))
    return '\n'.join(lines)+'\n'


def describe_function(requirements, target_function):
    if '#' in target_function:
        desc = target_function.partition('#')[2]
    else:
        desc = gpt.complete(comment_p.format(requirements=requirements, function=target_function))
    if not desc.startswith('#'):
        desc = '#' + desc
    return desc


def implement(requirements):
    print('Begin implementation for requirements:')
    print(requirements)
    funcs = architect(requirements)
    print('Functions:')
    print(funcs)
    name = filename(requirements)
    print('Filename:')
    print(name)
    chars = 0
    with open(os.path.join(here, name), 'w') as fid:
        fid.write('# implemented by LLM\n\n')
        fid.write('# Requirements driving this file:\n')
        for l in requirements.split('\n'):
            fid.write('# '+l)
        fid.write('\n\n')
        fid.flush()
        for i in range(len(funcs)):
            others = funcs[:i]+funcs[i+1:]
            f = funcs[i]
            impl = implement_single_function(requirements, f, others)
            chars += len(impl)
            comment = describe_function(requirements, f)
            fid.write(comment + '\n')
            fid.write(impl)
            fid.write('\n\n')
            fid.flush()
    print(f'implemented with {chars} characters in {name}')


if __name__ == '__main__':
    print(here)
    implement(sys.argv[1])
