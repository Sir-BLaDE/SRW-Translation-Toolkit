import json,re,bisect,functools
MK=re.compile(rb'\{Cmd_BranchProtagonist_(Begin|End),\s*(\d)\}')
@functools.lru_cache(None)
def spans(entry):
    pt=open('/home/claude/srwx/stg/%04d.bin'%entry,'rb').read()
    out=[];stack=[]
    for m in MK.finditer(pt):
        if m.group(1)==b'Begin': stack.append((m.start(),m.group(2)))
        elif stack:
            s,g=stack.pop(); out.append((s,m.start(),'M' if g==b'0' else 'F'))
    return out
def route_of(d):
    r='N'
    for s,e,g in spans(d['entry']):
        if s<d['start']<e: r=g
    return r

TB=re.compile(rb'\n(t_\d+) = \{')
@functools.lru_cache(None)
def tables(entry):
    pt=open('/home/claude/srwx/stg/%04d.bin'%entry,'rb').read()
    return [m.start() for m in TB.finditer(pt)]
def table_of(d):
    t=tables(d['entry']); i=bisect.bisect_right(t,d['start'])-1
    return (d['entry'],i)
