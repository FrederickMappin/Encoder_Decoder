# File: /dictionary-registry/dictionary-registry/src/index.py

from registry import DictionaryRegistry
from dictionaries.amino_acid import amino_acid_dict
from dictionaries.ascii_dict import ascii_dict
from dictionaries.binary_dict import binary
from dictionaries.chemical_dict import chemical_dict
from dictionaries.dna_dict import dna_nucleotides
from dictionaries.extended_ascii_dict import extended_ascii
from dictionaries.navajo_code import navajo_code
from dictionaries.rna_dict import rna_nucleotides

def main():
    registry = DictionaryRegistry()
    
    # Register dictionaries
    registry.register_dictionary('amino_acid', amino_acid_dict)
    registry.register_dictionary('ascii', ascii_dict)
    registry.register_dictionary('binary', binary)
    registry.register_dictionary('chemical', chemical_dict)
    registry.register_dictionary('dna', dna_nucleotides)
    registry.register_dictionary('extended_ascii', extended_ascii)
    registry.register_dictionary('navajo', navajo_code)
    registry.register_dictionary('rna', rna_nucleotides)

    # Example of retrieving a dictionary
    amino_acid = registry.get_dictionary('amino_acid')
    print(amino_acid)

if __name__ == "__main__":
    main()