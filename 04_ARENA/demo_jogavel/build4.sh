python3 - <<'P'
import json,os
s=open('game4.src.html').read()
s=s.replace('__DECKS__',open('decks.json').read()).replace('__SCENES__',json.dumps(sorted(os.listdir('a/scenes'))))
open('game4.html','w').write(s)
P
