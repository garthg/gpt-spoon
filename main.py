import os

from gpt_localhost import chat_complete
import tools

if os.environ['USER'] != 'somebodyelse':
    # TODO: whitelist or something
    raise RuntimeError('must run as somebodyelse')

while True:
    reload(tools)
    tools = filter(lambda x: not x.startswith('_'), dir(tools))
