#!/usr/bin/python3
"""
instalar deps: pip3 install pyyaml json

  # ...comentário
  #     Dados gerais das questões
  meta (yaml)

  #     Dados específicos das questões
  ** id
  *c classificadores
  *p precedência
  enunciado
  (*r n n n n : resp    )* //Vários
  *i imagens
  *v videos
  *s explicação complementar
"""

import sys,os,re,json,yaml

def parse_exer(exer):
   E={"header":"","body":[]}
   ### exer : id \n*s class \n*p precs\n enun (\n*r resp)*
   g = re.search(r'''
           ^\s*(.*)\n                    ## id
           \*c\s*(.*)\n                  ## *c
           \*p(.*)((?:.|\n)*?)           ## *p
           (\n\*r(?:.|\n)*?)             ## *r ... *r
           (?:\n \*i\s*(.+)\s*)?            ## *i  (opt)
           (?:\n \*v\s*(.+)\s*)?            ## *v  (opt)
           (?:\n \*s\s*(.+)\s*)?            ## *s  (opt)
           \s*$

           ''',
              exer, re.X)
   if g:
      E["_id"], cl, precs, E["header"], resps, _i, _v, _s = g.groups()
      for r in re.findall(r'\*r\s*(\d+)\s*(\d+)\s*(\d+)\s*(\d+)\s*:(.*)',resps):
          E["body"].append({
             "answer":r[4],
             "points":r[3],
             "correction":r[0],
             "mandatory":r[1],
             "eliminative":r[2],
          })
      E["images"] = _i
      E["videos"] = _v
      E["explanation"] = _s
      cl = cl.split()
      E["difficulty_level"] = cl[0]
      E["display_mode"] = cl[1]
      E["answering_time"] = cl[2]
      E["type"] = cl[3]
      E["repetitions"] = cl[4]
      E["precedence"] = precs.split()
      #print(E["_id"])
   
   else: print("####Invalid Exercise: {{{{ ",exer,"}}}}")
   return E

def parse_dom(exer):
   E={}
   result = re.split('\n',exer)
   #print(result)
   for i in result:
      #print(i)
      s = re.search(':', i)
      if s:
         a = re.split(':',i)
         E[a[0].strip()] = a[1].strip()
   #print(E)
   return E


def mkjson(x): return json.dumps(x,ensure_ascii=False,indent=3)

def main():
   #print("1")
   txt = sys.stdin.read()
   #print(txt)
   txt=re.sub(r'(^|\n)#.*','',txt)          ## remove comentário
   meta,*exs= re.split(r'\n\*\*',txt)       ## divide por exerc.
   #print(*exs)
   #print("2")
   #print(meta)
   #print(type(meta))
   ##f = open('store_file.yaml', 'w')
   ##f.write(meta)
   #f.close()
   #f = open("store_file.yaml", "r")
   #print(f.read())
   dmeta = parse_dom(meta)
   #print(dmeta)
   #print(dmeta)
   #dmeta= yaml.safe_load(meta)
   #print("3")
   for i, exer in enumerate(exs):
      #print("4")
      dexer=parse_exer(exer)
      #print(dexer)
       # print( "===")
      print(mkjson({**dmeta,**dexer}))
      if i+1 != len(exs): print(",") # don't split on the last call

main()
