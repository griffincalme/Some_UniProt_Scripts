# Python 3 Griffin Calme
# This script converts copies of fasta files from uniprot (user should place in same directory as script)
# to excel spreadsheets

from Bio import SeqIO
import pandas as pd
import os

#file = input('\nEnter fasta filepath: (default: HUMAN_ATP_BINDING_Canon_Iso.fasta)') \
#       or 'HUMAN_ATP_BINDING_Canon_Iso.fasta'

# gene name, sometimes a protein has no known gene name, try to pull one out
def get_gene_name(seq_record):
    try:
        return seq_record.description.split('GN=')[1].split(' ')[0]
    except:
        return ''


def fasta_to_excel(filepath):
    fasta_line_generator = SeqIO.parse(open(filepath),
                                       'fasta')  # this is a generator object that gets 'used up' by id_lists

    # generates list of lists, sublist looks like: ['sp', 'Q05932', 'FOLC_HUMAN']
    id_lists = [seq_record.id.split('|') for seq_record in fasta_line_generator]

    # pulls out the db initials (like sp or tr)
    database_initials = [x[0] for x in id_lists]
    df = pd.DataFrame({'database initials': database_initials})

    # pulls out the uniprot ID (Q05932)
    uniprot_id = [x[1] for x in id_lists]
    df['Uniprot_ID'] = uniprot_id

    # pulls out protein name (FOLC_HUMAN) from id_lists
    df['protein_name'] = [x[2] for x in id_lists]

    # create another generator object
    fasta_line_generator2 = SeqIO.parse(open(filepath), 'fasta')

    # call gene name function
    df['gene_name'] = [get_gene_name(seq_record) for seq_record in fasta_line_generator2]

    # get description by slicing everything after the first space until OS=
    fasta_line_generator3 = SeqIO.parse(open(filepath), 'fasta')
    df['description'] = [seq_record.description.split(' ', 1)[1].split('OS=')[0] for seq_record in
                         fasta_line_generator3]

    # finally, get the sequence
    fasta_line_generator4 = SeqIO.parse(open(filepath), 'fasta')
    df['sequence'] = [str(seq_record.seq) for seq_record in fasta_line_generator4]

    # this program leaves out PE (protein evidence) and SV (sequence version) for TrEMBL entries

    # Save pandas df to excel
    df.to_excel(filepath[:-6] + 'uniprot.xlsx', sheet_name='Sheet1', index=False)


# iterate over each file in local directory
for filename in os.listdir('.'):
    if os.path.isfile(filename):
        if filename.endswith('.fasta'):
            print(filename[:-6])  # slices off ".fasta"
            fasta_to_excel(filename)

