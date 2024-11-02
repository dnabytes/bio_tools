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
    'genbank': 'fasta',
    'gff': 'gff',
    'papers': 'csv'
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
            output = self.get_papers(output, id_)
        return output, err

    def get_papers(self, gb_file, id_):
        return ("").join([f'{id_},{line.split()[1]}\n' for line in gb_file.split('\n') if line.strip().startswith('PUBMED')])

    def save_to_file(self, output, id_):
        with open(
            f'{self.option}.{self.output_file_ext}' if self.one_file_output else f'{id_}-{self.option}.{self.output_file_ext}',
            'a' if self.one_file_output else 'w',
            encoding='utf-8'
        ) as fhandle:
            fhandle.write(output)

def get_usr_input():
    option_list = list(COMMANDS.keys())
    if len(sys.argv) < 3 or sys.argv[1] not in option_list:
        print(f'usage:\n  gb {("/").join(option_list)} ids/ids_file/query')
        sys.exit(0)
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
        cmd = shlex.split(f'{COMMANDS[option]}{("+").join(query_ids_file)}')
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
