#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Editor de texto de Super Robot Wars V (traducción al español).

Doble clic o:  python editor_texto.py
Pestañas:  Combate (CMN00)  y  Historia (STGEST).
  1. Busca (en español o en inglés).  2. Pulsa una línea.  3. Cambia el texto español.
  4. 'Guardar cambio'  5. 'Aplicar al juego' (hace copia de seguridad automática).

Tus cambios se guardan en datos/ediciones_usuario.json y se vuelven a aplicar solos
si el archivo se reconstruye, así no se pierden.

Opciones de línea de comandos:
  --test      prueba sin tocar el juego (escribe en outputs/_editor_test_*.cpk)
"""
import os, sys, re, json, time, shutil, struct, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.environ.get('SRWV_ROOT', os.path.dirname(HERE))
GAME = os.environ.get('SRWV_GAME', r'D:/Juegos/-SPARROW-/Super Robot Wars V')
if not os.path.isdir(GAME):
    GAME = os.path.expanduser('~/mnt/Super Robot Wars V')
DATOS = os.path.join(ROOT, 'datos'); BACK = os.path.join(ROOT, 'backup'); OUTS = os.path.join(ROOT, 'outputs')
EDITS = os.path.join(DATOS, 'ediciones_usuario.json')

from cpk_util import load as cpk_load
from srwv_cpkbuild2 import build_ordered
from srwv_bltu import load as bltu_load

FILES = {
    'CMN00': dict(rel='Data/BTLC/EN0/CMN00.CPK', orig='CMN00_CPK_original.cpk', titulo='Combate (CMN00)'),
    'STGEST': dict(rel='Data/STAGE/STGEST_EN.CPK', orig='STGEST_EN_original.cpk', titulo='Historia (STGEST)'),
}
PAT = re.compile(rb'\[\[(.*?)\]\]', re.S)


def gpath(k): return os.path.join(GAME, FILES[k]['rel'])
def opath(k): return os.path.join(BACK, FILES[k]['orig'])


def load_edits():
    try: return json.load(open(EDITS, encoding='utf-8'))
    except Exception: return {}


def save_edits(e):
    os.makedirs(DATOS, exist_ok=True)
    json.dump(e, open(EDITS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


# ---------- extracción ----------
def entries(key, path):
    """Devuelve lista de (clave, texto) en orden. clave: 'i' (CMN00) o 'fila:n' (STGEST)."""
    c = cpk_load(path); out = []
    if key == 'CMN00':
        row = [r for r in c.rows if r['id'] == 1][0]
        t = bltu_load(c.plain(row))
        for x in t.all_strings(): out.append((str(x[0]), x[3]))
    else:
        for r in c.rows:
            p = c.plain(r)
            for n, m in enumerate(PAT.findall(p)):
                out.append(('%d:%d' % (r['id'], n), m.decode('utf-8', 'replace')))
    return out


def cache_file(key): return os.path.join(DATOS, '_editor_cache_%s.json' % key)


def load_pairs(key, force=False):
    """[(clave, en, es)] con caché."""
    gp = gpath(key); sig = '%d' % os.path.getsize(gp) + ':' + '%d' % int(os.path.getmtime(gp))
    cf = cache_file(key)
    if not force and os.path.exists(cf):
        try:
            d = json.load(open(cf, encoding='utf-8'))
            if d.get('sig') == sig: return d['pairs']
        except Exception: pass
    en = dict(entries(key, opath(key))); es = entries(key, gp)
    pairs = [(k, en.get(k, ''), v) for k, v in es]
    json.dump({'sig': sig, 'pairs': pairs}, open(cf, 'w', encoding='utf-8'), ensure_ascii=False)
    return pairs


# ---------- reconstrucción ----------
def rebuild_bltu(plain, newmap):
    t = bltu_load(plain); out = bytearray()
    for v in t.header: out += struct.pack('<I', v)
    start = t.header[2] if t.header[2] else 0x30
    while len(out) < start: out += b'\x00'
    gid = 0
    for ch in t.chunks:
        strs = []
        for s in ch.strings:
            strs.append(newmap.get(str(gid), s)); gid += 1
        blob = bytearray(); offs = []
        for s in strs:
            offs.append(len(blob)); blob += s.encode('utf-8') + b'\x00'
        blk = bytearray(struct.pack('<I', len(strs)))
        for o in offs: blk += struct.pack('<I', o)
        blk += blob
        while len(blk) % 16: blk += b'\x00'
        out += blk
    out[40:44] = struct.pack('<I', len(out))
    return bytes(out)


def build(key, edits, src_path, out_path):
    """Aplica 'edits' {clave: texto} sobre src_path y escribe out_path. Devuelve nº de cambios."""
    c = cpk_load(src_path); new = {}
    if key == 'CMN00':
        row = [r for r in c.rows if r['id'] == 1][0]
        nb = rebuild_bltu(c.plain(row), edits)
        new[1] = (c.cipher(row, nb), len(nb))
    else:
        porfila = {}
        for k, v in edits.items():
            f, n = k.split(':'); porfila.setdefault(int(f), {})[int(n)] = v
        for r in c.rows:
            if r['id'] not in porfila: continue
            p = c.plain(r); ed = porfila[r['id']]; cnt = [-1]
            def rep(m):
                cnt[0] += 1
                return b'[[' + ed[cnt[0]].encode('utf-8') + b']]' if cnt[0] in ed else m.group(0)
            nb = PAT.sub(rep, p)
            new[r['id']] = (c.cipher(r, nb), len(nb))
    data = build_ordered(src_path, new)
    open(out_path, 'wb').write(data)
    c2 = cpk_load(out_path)
    for r in c2.rows:
        if r['id'] in new and r['ex'] != len(c2.plain(r)):
            raise RuntimeError('verificación fallida en fila %s' % r['id'])
    return len(edits)


def apply_to_game(key, edits_key):
    stamp = time.strftime('%Y%m%d_%H%M%S')
    os.makedirs(BACK, exist_ok=True)
    gp = gpath(key); bk = os.path.join(BACK, 'editor_%s_%s_%s' % (stamp, key, os.path.basename(gp)))
    shutil.copy2(gp, bk)
    tmp = os.path.join(OUTS, '_editor_tmp_%s.cpk' % key)
    build(key, edits_key, gp, tmp)
    shutil.copy2(tmp, gp)
    return bk


# ---------- interfaz ----------
def gui():
    import tkinter as tk
    from tkinter import ttk, messagebox
    root = tk.Tk(); root.title('Editor de texto SRW V'); root.geometry('1250x760')
    edits = load_edits()
    nb = ttk.Notebook(root); nb.pack(fill='both', expand=True)
    estado = tk.StringVar(value='Listo.')
    tk.Label(root, textvariable=estado, anchor='w').pack(fill='x')

    def pestana(key):
        fr = ttk.Frame(nb); nb.add(fr, text=FILES[key]['titulo'])
        st = {'pairs': [], 'vis': [], 'sel': None}
        top = ttk.Frame(fr); top.pack(fill='x', padx=6, pady=4)
        q = tk.StringVar(); ttk.Label(top, text='Buscar:').pack(side='left')
        e = ttk.Entry(top, textvariable=q, width=50); e.pack(side='left', padx=4)
        solo = tk.BooleanVar(value=False)
        ttk.Checkbutton(top, text='solo editadas', variable=solo).pack(side='left', padx=6)
        lb = tk.Listbox(fr, height=18, font=('Consolas', 10)); lb.pack(fill='both', expand=True, padx=6)
        sb = ttk.Scrollbar(lb, command=lb.yview); sb.pack(side='right', fill='y'); lb.config(yscrollcommand=sb.set)
        mid = ttk.Frame(fr); mid.pack(fill='both', padx=6, pady=4)
        ttk.Label(mid, text='Inglés original (no editable)').grid(row=0, column=0, sticky='w')
        ttk.Label(mid, text='Español (editable)').grid(row=0, column=1, sticky='w')
        ten = tk.Text(mid, height=8, width=70, font=('Consolas', 10), state='disabled'); ten.grid(row=1, column=0, padx=3)
        tes = tk.Text(mid, height=8, width=70, font=('Consolas', 10)); tes.grid(row=1, column=1, padx=3)
        bt = ttk.Frame(fr); bt.pack(fill='x', padx=6, pady=4)

        def cur_es(k, base):
            return edits.get(key, {}).get(k, base)

        def refresh(*_):
            s = q.get().lower(); lb.delete(0, 'end'); st['vis'] = []
            for k, en, es in st['pairs']:
                es2 = cur_es(k, es)
                if solo.get() and k not in edits.get(key, {}): continue
                if s and s not in es2.lower() and s not in en.lower(): continue
                st['vis'].append((k, en, es2))
                if len(st['vis']) >= 3000: break
            for k, en, es2 in st['vis']:
                mark = '*' if k in edits.get(key, {}) else ' '
                lb.insert('end', '%s%-9s %s' % (mark, k, es2.replace('\r\n', ' ¶ ').replace('\n', ' ¶ ')[:150]))
            estado.set('%d líneas mostradas (máx. 3000). * = editada por ti.' % len(st['vis']))

        def pick(_=None):
            i = lb.curselection()
            if not i: return
            k, en, es2 = st['vis'][i[0]]; st['sel'] = k
            ten.config(state='normal'); ten.delete('1.0', 'end'); ten.insert('1.0', en.replace('\r\n', '\n')); ten.config(state='disabled')
            tes.delete('1.0', 'end'); tes.insert('1.0', es2.replace('\r\n', '\n'))

        def guardar():
            k = st['sel']
            if k is None: return
            txt = tes.get('1.0', 'end-1c')
            if key == 'STGEST': txt = txt.replace('\r\n', '\n').replace('\n', '\r\n')
            edits.setdefault(key, {})[k] = txt; save_edits(edits); refresh()
            estado.set('Cambio guardado (aún no aplicado al juego).')

        def deshacer():
            k = st['sel']
            if k and k in edits.get(key, {}): del edits[key][k]; save_edits(edits); refresh(); estado.set('Cambio descartado.')

        def aplicar():
            ed = edits.get(key, {})
            if not ed: messagebox.showinfo('Nada que aplicar', 'No hay cambios guardados en esta pestaña.'); return
            estado.set('Aplicando... puede tardar unos minutos, no cierres.'); root.update()
            try:
                bk = apply_to_game(key, ed)
                load_pairs(key, force=True); st['pairs'] = load_pairs(key); refresh()
                messagebox.showinfo('Hecho', 'Cambios aplicados al juego.\nCopia anterior: %s' % bk)
                estado.set('Aplicado.')
            except Exception as ex:
                messagebox.showerror('Error', str(ex)); estado.set('Error: %s' % ex)

        ttk.Button(bt, text='Guardar cambio', command=guardar).pack(side='left', padx=4)
        ttk.Button(bt, text='Descartar mi cambio', command=deshacer).pack(side='left', padx=4)
        ttk.Button(bt, text='APLICAR AL JUEGO', command=aplicar).pack(side='left', padx=20)
        ttk.Button(bt, text='Recargar desde el juego', command=lambda: (st.update(pairs=load_pairs(key, True)), refresh())).pack(side='left', padx=4)
        q.trace_add('write', refresh); solo.trace_add('write', refresh); lb.bind('<<ListboxSelect>>', pick)
        estado.set('Cargando %s (la primera vez tarda varios minutos)...' % FILES[key]['titulo']); root.update()
        st['pairs'] = load_pairs(key); refresh()

    for k in FILES: pestana(k)
    root.mainloop()


def test():
    os.makedirs(OUTS, exist_ok=True)
    for key in FILES:
        t0 = time.time(); pairs = load_pairs(key, True)
        print(key, len(pairs), 'líneas', round(time.time() - t0), 's')
        k, en, es = [p for p in pairs if len(p[2]) > 20][5]
        out = os.path.join(OUTS, '_editor_test_%s.cpk' % key)
        build(key, {k: es + ' [PRUEBA]'}, gpath(key), out)
        got = dict(entries(key, out))[k]
        print(' edición', k, 'OK' if got.endswith('[PRUEBA]') else 'FALLO')


if __name__ == '__main__':
    if '--test' in sys.argv: test()
    else: gui()
