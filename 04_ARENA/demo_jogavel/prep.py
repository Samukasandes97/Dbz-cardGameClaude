import json,os,random,subprocess,shutil,glob
from PIL import Image
S='/tmp/claude-0/-home-claude/84f3faec-af92-5d88-b151-bbf1e79ccb25/scratchpad'; M=S+'/MESTRE/DBZ_CardGame'; A=S+'/demo/a'
def sh(*c): subprocess.run(c,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
# cards
for src,pre in ((M+'/02_CARTAS/Starter_Deck_Goku/cartas_v4_super_3D_premium/cartas','GK'),(M+'/02_CARTAS/Starter_Deck_Vegeta/cartas','VG')):
    for f in sorted(glob.glob(src+'/*.png')):
        n=os.path.basename(f)[:-4]
        Image.open(f).convert('RGBA').resize((300,430),Image.LANCZOS).save(f'{A}/cards/{n}.webp',quality=82)
# heroes
for k,f in (('goku','Goku/Retrato/Base/retrato_goku_base.jpg'),('goku_t','Goku/Retrato/Transformacao/retrato_goku_transformacao.jpg'),('vegeta','Vegeta/Retrato/Base/retrato_vegeta_base.jpg'),('vegeta_t','Vegeta/Retrato/Transformacao/retrato_vegeta_transformacao.jpg')):
    Image.open(f'{M}/01_HEROIS/{f}').convert('RGB').resize((380,380),Image.LANCZOS).save(f'{A}/heroes/{k}.jpg',quality=84)
# scenes
random.seed(7)
for i in random.sample(range(35),8):
    Image.open(f'{M}/03_CENARIOS/widescreen_16x9/{i:02d}.jpg').convert('RGB').resize((1280,720),Image.LANCZOS).save(f'{A}/scenes/s{i:02d}.jpg',quality=68)
# arena assets
P=M+'/04_ARENA/projeto'
for i in range(1,11): Image.open(f'{P}/esfera_{i}.png').convert('RGBA').resize((88,88),Image.LANCZOS).save(f'{A}/heroes/esfera_{i}.webp',quality=85)
Image.open(f'{P}/baba.png').convert('RGBA').resize((90,140),Image.LANCZOS).save(f'{A}/heroes/baba.webp',quality=85)
for n in ('z_vazio','z_cheio','z_gold'): Image.open(f'{P}/{n}.png').convert('RGBA').resize((112,90),Image.LANCZOS).save(f'{A}/heroes/{n}.webp',quality=85)
# videos
H=M+'/01_HEROIS'
for out,src in (('goku_transf','Goku/Transformacao/Goku_Transformacao_Kaioken_FHD.mp4'),('goku_comeback','Goku/Comeback/Goku_Comeback_Kaioken_x3_Kamehameha_FHD.mp4'),('vegeta_transf','Vegeta/Transformacao/Vegeta_Transformacao_Oozaru_FHD.mp4'),('vegeta_comeback','Vegeta/Comeback/Vegeta_Comeback_Oozaru_Rajada_FHD.mp4')):
    sh('ffmpeg','-y','-i',f'{H}/{src}','-vf','scale=960:540','-c:v','libx264','-crf','27','-preset','slow','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-movflags','+faststart',f'{A}/video/{out}.mp4')
# sfx
PK=H+'/_COMUM/Efeitos_sonoros/Pack_EFEITOS_DBZ_Z_por_categoria/'
SF={'soco1':('socos/soco.wav',1.2),'soco2':('socos/soco_forte.wav',1.2),'soco3':('socos/soco_medio.wav',1.2),'chute1':('chutes/chute.wav',1.2),'chute2':('chutes/chute_forte.wav',1.2),
 'rush':('voos e rushs/swoop.wav',1.5),'rush2':('voos e rushs/chainswoop.wav',1.5),'invest':('voos e rushs/swoophit.wav',1.5),'hit':('voos e rushs/groundhit2.wav',1.5),'guard':('poder/reflect.wav',1.5),
 'ki':('poder/kiblast.wav',1.3),'charge':('poder/basicbeam_charge.wav',2.5),'beam':('poder/basicbeam_fire.wav',2.5),'kame_charge':('kamehameha/kame_charge.wav',2.5),'kame_fire':('kamehameha/kamehameha_fire.wav',2.8),
 'boom':('explosoes/boom.wav',2.0),'kiplo':('explosoes/kiplosion.wav',1.8),'death':('voos e rushs/deathfall.wav',1.6),'tele':('teleport/teleport.wav',1.5),'powerup':('explosoes/powerup.wav',3.0),'aura':('aura ssj/aura2.wav',2.2),'senzu':('senzu/sensu.wav',1.5),'turn':('poder/candypop.wav',1.0)}
for k,(f,d) in SF.items():
    sh('ffmpeg','-y','-i',PK+f,'-t',str(d),'-ac','1','-ar','32000','-b:a','56k','-af',f'afade=t=out:st={max(d-0.15,0)}:d=0.15',f'{A}/sfx/{k}.mp3')
# voices
AV=json.load(open(M+'/06_COMBATENTES_AUDIO/audio_cartas_v2.json'))
def pick(lst,n,seed):
    r=random.Random(seed); l=list(lst); r.shuffle(l); return l[:n]
def conv(rel,out):
    rel=('06_COMBATENTES_AUDIO/'+rel[len('Combatentes/'):]) if rel.startswith('Combatentes/') else rel; sh('ffmpeg','-y','-i',M+'/'+rel,'-t','2.6','-ac','1','-ar','32000','-b:a','48k',f'{A}/voz/{out}.mp3')
V={}
def char(key,card):
    c=AV['cartas'][card]; V[key]={'atk':[],'dmg':[],'play':[]}
    for i,r in enumerate(pick(c['ataque_pool'],6,key+'a')): conv(r,f'{key}_a{i}'); V[key]['atk'].append(f'{key}_a{i}')
    for i,r in enumerate(pick(c['dano_pool'],6,key+'d')): conv(r,f'{key}_d{i}'); V[key]['dmg'].append(f'{key}_d{i}')
    if c.get('jogada'): conv(c['jogada'],f'{key}_p0'); V[key]['play'].append(f'{key}_p0')
char('goku','GK02'); char('vegeta','VG02'); char('oozaru','VG07'); char('nappa','VG03'); char('raditz','VG09')
# especiais
conv('06_COMBATENTES_AUDIO/Goku/Goku_inicio/_identificados/Goku_inicio_064_Kamehameha.ogg','goku_kame'); conv('06_COMBATENTES_AUDIO/Goku/Goku_inicio/_identificados/Goku_inicio_061_Kaioken.ogg','goku_kaioken')
V['esp']={'goku_kame':'goku_kame','goku_kaioken':'goku_kaioken'}
# vegeta: mira=frase, disparo=grito curto
for i,r in enumerate(pick([x for x in AV['cartas']['VG02']['ataque_pool']],3,'vm')): conv(r,f'vegeta_gr{i}')
V['vegeta']['grito']=[f'vegeta_gr{i}' for i in range(3)]
V['vegeta']['mira']=[]
for i,r in enumerate(pick(glob.glob(M+'/01_HEROIS/Vegeta/Vozes/Vegeta_Scouter/_por_tipo/frase/*.ogg'),3,'vf')): conv(os.path.relpath(r,M),f'vegeta_m{i}'); V['vegeta']['mira'].append(f'vegeta_m{i}')
conv('01_HEROIS/Vegeta/Comeback/Originais_dele/voz_comeback_2_disparo_GreatApe_112.ogg','oozaru_boca'); V['esp']['oozaru_boca']='oozaru_boca'
json.dump(V,open(f'{A}/voz_map.json','w'))
print('ok')
