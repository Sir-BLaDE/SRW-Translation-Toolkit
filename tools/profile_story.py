import sys, time
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
import story_build as sb

def mark(label, t):
    print('%s: %.2fs' % (label, time.time() - t), flush=True)

t = time.time()
tr = sb.load_translations(); mark('load_translations ' + str(len(tr)), t)
t = time.time()
tm = sb.load_tm(); mark('load_tm ' + str(len(tm)), t)
t = time.time()
by = sb.load_dialogues(); mark('load_dialogues ' + str(len(by.get('_rec', {}))), t)
t = time.time()
cf = sb.load(sb.GAME); mark('load cpk ' + str(len(cf.rows)), t)
t = time.time()
recs = by['_rec']
per = {}
for i, d in recs.items():
    per.setdefault(d['entry'], []).append(d)
mark('group', t)

n = 0
for f in cf.rows:
    ds = per.get(f['id'])
    if not ds:
        continue
    t = time.time()
    pt = cf.plain(f)
    if n < 3: mark('plain id%s %.1fMB' % (f['id'], len(pt)/1e6), t)
    t = time.time()
    dialogs = sb.find_dialogs(f['id'], pt)
    if n < 3: mark('find_dialogs id%s n=%d' % (f['id'], len(dialogs)), t)
    n += 1
mark('all dialog rows ' + str(n), t)
