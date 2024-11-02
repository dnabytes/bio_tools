#!/usr/bin/python3
import os
import sys
import subprocess
from tqdm import tqdm

def align(fasta, algorithm):
    outfile = fasta.replace(".fasta", f".{algorithm}")
    with open(os.devnull, 'wb') as devnull:
        if algorithm == 'muscle':
            subprocess.check_call(f'muscle -align {fasta} -output {outfile}'.split(), stdout=devnull, stderr=subprocess.STDOUT)
        elif algorithm == 'clustal':
            subprocess.check_call(f'clustalw -infile={fasta} -output=FASTA -outfile={outfile}'.split(), stdout=devnull, stderr=subprocess.STDOUT)
            os.remove(f'{fasta.replace(".fasta", ".dnd")}')

def main():
    usr_input = sys.argv[1:]
    if  len(usr_input) < 2 or usr_input[0] not in ['muscle', 'clustal']:
        print('usage: align algorithm[muscle/clustal] fasta/s')
        sys.exit(1)

    algorithm = usr_input[0]
    fastas = usr_input[1:]
    for fasta in tqdm(fastas):
        if not os.path.isfile(fasta):
            print(f'{fasta} not found')
            continue
        align(fasta, algorithm)

if __name__ == '__main__':
    main()
