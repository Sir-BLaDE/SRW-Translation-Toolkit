"""recheck_final.py - recomprobacion final de acentos, ñ y¿/¡ en todo el juego."""
import sys, os, re, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

FONT = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf = load(FONT)
rows = {r['id']: r for r in cf.rows}

# --- 1. mapas de fuente (fila 1 = dialogos, fila 2 = UI/batalla) -----------
CHARS = list('áéíóúñÁÉÍÓÚü¿¡')
print('=== MAPAS DE FUENTE ===')
for rid in (1, 2):
    d = cf.plain(rows[rid])
    h = [struct.unpack_from('<I', d, i*4)[0] for i in range(12)]
    s = d[h[6]:h[7]].decode('utf-8', 'ignore')
    missing = [c for c in CHARS if c not in s]
    print('  fila %d: %s' % (rid, ('OK - todos presentes' if not missing else 'FALTAN ' + ''.join(missing))))

# --- 2. glifos (fila 3 = metricas, fila 4 = textura) -----------------------
p3 = cf.plain(rows[3]); tex = cf.plain(rows[4]); W = 4096; HDR = 40
N = (len(p3)-HDR)//36
byc = {}
for g in range(N):
    u = struct.unpack_from('<I', p3, HDR+g*36)[0]
    byc.setdefault(u, g)
missing = [c for c in CHARS if ord(c) not in byc]
print('  glifos: %s' % ('OK - todos dibujados' if not missing else 'FALTAN ' + ''.join(missing)))
# comprobar que no son relleno (¿ y ñ)
for ch in ['ñ','¿','¡','á']:
    g = byc[ord(ch)]
    fl = struct.unpack_from('<8f', p3, HDR+g*36+4)
    x=int(round(fl[0]*W)); y=int(round(fl[1]*W)); w=int(round(fl[2]*W)); h=int(round(fl[3]*W))
    px=sum(1 for yy in range(h) for xx in range(w) if tex[(y+yy)*W+x+xx]>30)
    print('    %r g=%d pixeles=%d' % (ch, g, px))

# --- 3. todos los CPK de texto instalados ---------------------------------
G = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data'
FILES = [
 ('SYSTEXT',  G + r'/AIDDATA/EN/SysText.cpk'),
 ('STGEST',   G + r'/STAGE/STGEST_EN.CPK'),
 ('CMN00',    G + r'/BTLC/EN0/CMN00.CPK'),
 ('KPACK_LN', G + r'/KURODATA/EN/KPACK_P4_LN_EN.CPK'),
 ('KPACK_RG', G + r'/KURODATA/EN/KPACK_P4_RG_EN.CPK'),
 ('LT00_EN',  r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk'),
 ('MTZKN_NM', r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/MtZkn_Nm.cpk'),
 ('MTZKN_PT', r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/MtZkn_Pt.cpk'),
 ('MTZKN_RT', r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/MtZkn_Rt.cpk'),
]
ACC = re.compile(r'[áéíóúñÁÉÍÓÚü]')
print('\n=== CPK INSTALADOS ===')
print('%-10s %9s %7s %7s %7s %7s %s' % ('FILE','SIZE','FILAS','ACENT','Ñ','¿/¡','ESTADO'))
for name, p in FILES:
    if not os.path.exists(p):
        print('%-10s NO ENCONTRADO' % name); continue
    try: c = load(p)
    except Exception as e:
        print('%-10s ERROR %s' % (name, e)); continue
    ok = all(r['ex'] == len(c.plain(r)) for r in c.rows)
    diag = c.cpk.diagnose()
    acc = enye = inv = 0
    for r in c.rows:
        try: pt = c.plain(r)
        except Exception: continue
        acc += len(ACC.findall(pt.decode('utf-8','ignore')))
        enye += pt.count(b'\xc3\xb1') + pt.count(b'\xc3\x91')
        inv += pt.count(b'\xc2\xbf') + pt.count(b'\xc2\xa1')
    estado = 'OK' if (ok and not diag) else 'FAIL %s' % diag
    print('%-10s %9d %7d %7d %7d %7d %s' % (name, os.path.getsize(p), len(c.rows), acc, enye, inv, estado))
    sys.stdout.flush()
