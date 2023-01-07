from antlr4 import *
from antlr4.tree.Trees import Trees
from cLexer import cLexer
from cParser import cParser
import xmltodict
import json
import os

EXAMPLE_PATH = '../example/'

def getjson(filename):
    lexer = cLexer(FileStream(filename))
    stream = CommonTokenStream(lexer)
    parser = cParser(stream)
    tree = parser.prog()
    s = Trees.toXMLTree(tree, None, parser)
    d = xmltodict.parse(s)
    with open(filename+'.json', 'w') as f:
        json.dump(d, f)
        print(f'json file {filename+".json"} created')
    
if __name__=='__main__':
    print(os.listdir(EXAMPLE_PATH))
    filename = input('choose a file like *.c: ')
    filename = os.path.join(EXAMPLE_PATH, filename)
    getjson(filename)