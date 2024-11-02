#!/usr/bin/python3
import os

pdbs = [xfile for xfile in os.listdir(os.curdir) if xfile.endswith('.pdb')]

for pdb in pdbs:
    add_n_to_aa = 0
    last_n_aa = 0
    add_now = True
    new_pdb = open(pdb.replace('.pdb', '-new.pdb'), 'w')
    with open(pdb) as fhandle:
        for line in fhandle:
            if not line.startswith('ATOM'):
                continue
            n_aa = int(line.strip().split()[5])
            if n_aa == 2:
                add_now = True
            if n_aa == 1 and add_now:
                add_n_to_aa = last_n_aa
                add_now = False
            new_pos = n_aa + add_n_to_aa
            new_line = f'{line[:21]}A {new_pos:4d}{line[27:]}'
            new_pdb.write(new_line)
            last_n_aa = new_pos
    new_pdb.write('TER\nEND')
    new_pdb.close()
