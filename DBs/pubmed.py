#!/usr/bin/python3
import sys
import shlex
import subprocess

if len(sys.argv) > 1:
    cmds = shlex.split(f'firefox https://pubmed.ncbi.nlm.nih.gov/?term={("+").join(sys.argv[1:])}')
    p = subprocess.Popen(cmds, start_new_session=True)
