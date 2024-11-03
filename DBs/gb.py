#!/usr/bin/python3
import os
import sys
import time
import shlex
import subprocess
from tqdm import tqdm

COMMANDS = {
    'genome': 'efetch -db nuccore -id %id -format fasta',
    'proteome': 'efetch -db nuccore -id %id -format fasta_cds_aa',
    'orfeome': 'efetch -db nuccore -id %id -format fasta_cds_na',
    'protein': 'efetch -db protein -id %id -format fasta_cds_aa',
    'genbank': 'efetch -db nuccore -id %id -format gb',
    'gff': 'efetch -db nuccore -id %id -format gff3',
    'papers': 'efetch -db nuccore -id %id -format gb',
    'search': 'firefox https://www.ncbi.nlm.nih.gov/nuccore/?term='
}

OUTPUT_FILE_EXT = {
    'genome': 'fasta',
    'proteome': 'fasta',
    'orfeome': 'fasta',
    'protein': 'fasta',
    'genbank': 'gb',
    'gff': 'gff',
    'papers': 'csv'
}

PARAMS_DESCRIPTION = {
    'param': 'input -> output format',
    '-'*9: '-'*30,
    'genome': f'id/ids file -> {OUTPUT_FILE_EXT["genome"]}',
    'proteome': f'id/ids file -> {OUTPUT_FILE_EXT["proteome"]}',
    'orfeome': f'id/ids file -> {OUTPUT_FILE_EXT["orfeome"]}',
    'protein': f'id/ids file -> {OUTPUT_FILE_EXT["protein"]}',
    'genbank': f'id/ids file -> {OUTPUT_FILE_EXT["genbank"]}',
    'gff': f'id/ids file -> {OUTPUT_FILE_EXT["gff"]}',
    'papers': f'id/ids file -> {OUTPUT_FILE_EXT["papers"]}',
    'search': 'search query/id in genbank website'
}

class Downloader:
    def __init__(self, option):
        self.option = option
        self.one_file_output = self.option in ['papers']
        self.output_file_ext = OUTPUT_FILE_EXT[self.option]
        self.command = COMMANDS[self.option]

    def download(self, id_):
        output = subprocess.getoutput(self.command.replace("%id", id_))
        err = 1 if not output.strip() or 'QUERY FAILURE' in output else 0
        if self.option == 'papers':
            output = self.get_pubmed_ids(output, id_)
        return output, err

    def get_pubmed_ids(self, gb_file, id_):
        return ("").join([f'{id_},{line.split()[1]}\n' for line in gb_file.split('\n') if line.strip().startswith('PUBMED')])

    def save_to_file(self, output, id_):
        with open(
            f'{self.option}.{self.output_file_ext}' if self.one_file_output else f'{id_}-{self.option}.{self.output_file_ext}',
            'a' if self.one_file_output else 'w',
            encoding='utf-8'
        ) as fhandle:
            fhandle.write(output)

def help():
    print('usage:\n')
    print(('\n\n').join([f'  {option:10s} {description}' for option, description in PARAMS_DESCRIPTION.items()]))
    print()
    sys.exit(0)

def get_usr_input():
    if len(sys.argv) < 3 or sys.argv[1] not in list(COMMANDS.keys()):
        help()
    option, query_ids_file = sys.argv[1], sys.argv[2:]
    return option, query_ids_file

def get_ids(query_ids_file):
    if os.path.isfile(query_ids_file[0]):
        with open(query_ids_file[0], 'r', encoding='utf-8') as f_handle:
            return [line.strip() for line in f_handle if line.strip()]
    return query_ids_file

def main():
    option, query_ids_file = get_usr_input()

    if option == 'search':
        cmd = shlex.split(f'{COMMANDS["search"]}{("+").join(query_ids_file)}')
        p = subprocess.Popen(cmd, start_new_session=True)
    else:
        downloader = Downloader(option)
        ids = get_ids(query_ids_file)
        waiting_time = 2
        for id_ in tqdm(ids):
            while True:
                time.sleep(waiting_time)
                output, err = downloader.download(id_)
                if not err:
                    downloader.save_to_file(output, id_)
                    break
                waiting_time *= 2
                print(f'Error trying to download {id_}. Waiting {waiting_time} seconds and retrying')

if __name__ == '__main__':
    main()
