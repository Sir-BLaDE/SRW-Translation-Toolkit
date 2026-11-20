with open('C:/Dev/Default Project/srwv/datos/lt00_translations_comprehensive.txt', 'r') as f:
    content = f.read()
    lines = content.split('\n')
    count = 0
    for i, l in enumerate(lines):
        if l.strip():
            parts = l.split('\t')
            if len(parts) >= 2:
                print(f'{i}: EN={parts[0][:60]!r} ES={parts[1][:60]!r}')
                count += 1
    print(f'Total entries: {count}')
