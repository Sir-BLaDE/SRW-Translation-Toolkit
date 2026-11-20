#!/usr/bin/env python3
"""Investigate F1 files and identify what they contain"""

with open('C:/Dev/Default Project/srwv/outputs/cmn_f1_test.bin', 'rb') as f:
    data = f.read(64)
print('F1 test first 64 bytes:', data)

with open('C:/Dev/Default Project/srwv/outputs/cmn_f1_traducido.bin', 'rb') as f:
    data = f.read(64)
print('F1 traducido first 64 bytes:', data)

# Check file sizes
import os
for fp in ['C:/Dev/Default Project/srwv/outputs/cmn_f1_test.bin', 'C:/Dev/Default Project/srwv/outputs/cmn_f1_traducido.bin']:
    st = os.stat(fp)
    print(f'{fp}: size={st.st_size}')

print()
print('F1 files might be part of CMN00 CPK or separate data.')
print('Let me check if there are more F files or story-related data.')
