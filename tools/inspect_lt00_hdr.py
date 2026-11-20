import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from srwv_cpk import Cpk

paths = [
    r'C:/Dev/Default Project/srwv/backup/LT00_EN_instalado_antes.cpk',
    r'C:/Dev/Default Project/srwv/backup/LT00_EN_original.cpk',
    r'C:/Dev/Default Project/srwv/outputs/LT00_EN_es.cpk',
    r'C:/Dev/Default Project/srwv/backup/STGEST_EN_original.cpk',
]
for path in paths:
    try:
        c = Cpk(path)
    except Exception as e:
        print(path, 'ERROR', type(e).__name__, e)
        continue
    info = c.itoc_info
    print('==', path)
    print('  filesize', len(c.raw), 'align', c.align, 'content_offset', c.content_offset,
          'content_size', c.content_size)
    print('  hdr FileSize', c.h.get('FileSize'), 'Files', c.files_count,
          'EnabledDataSize', c.h.get('EnabledDataSize'),
          'EnabledPackedSize', c.h.get('EnabledPackedSize'))
    print('  tables', {k: (v.rows_count, v.base) for k, v in info.items() if hasattr(v, 'rows_count')})
    print('  diagnose', c.diagnose() or 'ok')
