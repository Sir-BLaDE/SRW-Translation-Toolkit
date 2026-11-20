"""Genera los parches binarios (zstd --patch-from) de la traducción al español de SRW V.
Uso: python3 release_build.py [grupo]   grupos: a (ficheros pequeños), b (grandes), c (DLC)
Requiere el CLI `zstd`. Escribe release/v0.9/patches/*.zst y manifest parcial en release/v0.9/manifest_<grupo>.json"""
import os,sys,json,hashlib,subprocess,glob
H=os.environ['HOME']; P=H+'/mnt/srwv/'; G=H+'/mnt/Super Robot Wars V/'; B=P+'backup/'
OUT=P+'release/v0.9/'
MAP={
 'CommonData/MtData/EN/MtZkn_Nm.cpk':'MtZkn_Nm_original.cpk','CommonData/MtData/EN/MtZkn_Pt.cpk':'MtZkn_Pt_original.cpk',
 'CommonData/MtData/EN/MtZkn_Rt.cpk':'MtZkn_Rt_original.cpk','CommonData/MtData/EN/rpw_jstr.cpk':'rpw_jstr_original.cpk',
 'CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk':'B_LT00_EN_original.cpk','CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk':None,
 'CommonData/hiyama/defaultSS_E.cpk':'defaultSS_E_original.cpk','Data/AIDDATA/EN/FontInfo.cpk':'FontInfo_EN_original.cpk',
 'Data/AIDDATA/EN/LayoutData.cpk':'LayoutData_original.cpk','Data/AIDDATA/EN/LayoutImage.cpk':'LayoutImage_original.cpk',
 'Data/AIDDATA/EN/Prologue.cpk':'Prologue_EN_original.cpk','Data/AIDDATA/EN/SysText.cpk':'SysText_original.cpk',
 'Data/BTLC/EN0/CMN00.CPK':'CMN00_CPK_original.cpk','Data/BTLC/EN0/CMN00_PC.CPK':'BTLC_EN0_CMN00_PC_original.cpk',
 'Data/BTLC/EN0/OP.CPK':'OP_CK_original.cpk','Data/BTLC/EN0/OP_PC.CPK':'BTLC_EN0_OP_PC_original.cpk',
 'Data/KURODATA/CMN/KPACK_PC_CMN.cpk':'KPACK_PC_CMN_original.cpk','Data/KURODATA/EN/KPACK_P4_LN_EN.CPK':'KPACK_P4_LN_EN_original.cpk',
 'Data/KURODATA/EN/KPACK_P4_RG_EN.CPK':'KPACK_P4_RG_EN_original.cpk','Data/STAGE/STGEST_EN.CPK':'STGEST_EN_original.cpk',
 'Data/TABATA/EN/TPACKWIN_EN.cpk':'TPACKWIN_EN_original.cpk','SRWV.EXE':'SRWV_original.EXE','Data/ANIME/effwin.cpk':'effwin_original.cpk'}
for f in sorted(glob.glob(B+'dlc_en/dlc*_en.cpk')):
    n=os.path.basename(f); 
    if os.path.exists(G+'Data/DLCDIRE/EN/'+n): MAP['Data/DLCDIRE/EN/'+n]='dlc_en/'+n
BIG={'Data/ANIME/effwin.cpk','Data/TABATA/EN/TPACKWIN_EN.cpk','Data/STAGE/STGEST_EN.CPK','Data/KURODATA/CMN/KPACK_PC_CMN.cpk'}
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for c in iter(lambda:f.read(1<<22),b''): h.update(c)
    return h.hexdigest()
def build(rel,orig):
    new=G+rel; name=rel.replace('/','__')+'.zst'; out=OUT+'patches/'+name
    e={'path':rel,'patch':name,'new_sha256':sha(new),'new_size':os.path.getsize(new)}
    if orig is None:
        subprocess.check_call(['zstd','-q','-19','-f',new,'-o',out]); e['full']=True
    else:
        o=B+orig; e['orig_sha256']=sha(o); e['orig_size']=os.path.getsize(o)
        lvl='-5' if rel in BIG else '-19'
        subprocess.check_call(['zstd','-q',lvl,'--long=31','-f','--patch-from='+o,new,'-o',out],stderr=subprocess.DEVNULL)
    e['patch_size']=os.path.getsize(out); return e
if __name__=='__main__':
    g=sys.argv[1]
    sel=[r for r in MAP if (g=='b' and r in BIG) or (g=='c' and r.startswith('Data/DLCDIRE')) or (g=='a' and r not in BIG and not r.startswith('Data/DLCDIRE'))]
    res=[]
    for r in sel:
        e=build(r,MAP[r]); res.append(e); print(r,e['patch_size'],flush=True)
    json.dump(res,open(OUT+'manifest_%s.json'%g,'w'),indent=1,ensure_ascii=False)
