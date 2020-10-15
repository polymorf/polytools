from pygments import highlight, lexers, formatters
import json

def print_obj(obj):
    j = json.dumps(obj, sort_keys=True, indent=4)
    colorful_json = highlight(j, lexers.JsonLexer(), formatters.TerminalFormatter())
    print(colorful_json)
