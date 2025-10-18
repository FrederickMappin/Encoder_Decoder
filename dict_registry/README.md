# Dictionary Registry

This project implements a dictionary registry pattern to manage various types of dictionaries used in different applications. The registry allows for easy registration and retrieval of dictionaries, making it a flexible solution for handling diverse data types.

## Project Structure

```
dictionary-registry
├── src
│   ├── index.py               # Entry point for the dictionary registry application
│   ├── registry.py             # Manages the registration and retrieval of dictionaries
│   ├── dictionaries            # Contains different dictionary definitions
│   │   ├── __init__.py        # Makes the dictionaries directory a Python package
│   │   ├── amino_acid.py      # Maps amino acid codes to their names
│   │   ├── ascii_dict.py      # Maps ASCII values to corresponding characters
│   │   ├── binary_dict.py     # Contains binary representations
│   │   ├── chemical_dict.py    # Maps chemical terms to their definitions
│   │   ├── dna_dict.py        # Maps DNA nucleotide codes to their names
│   │   ├── extended_ascii_dict.py # Maps extended ASCII values to characters
│   │   ├── navajo_code.py     # Maps letters and numbers to Navajo code equivalents
│   │   └── rna_dict.py        # Maps RNA nucleotide codes to their names
├── requirements.txt            # Lists the dependencies required for the project
└── README.md                   # Documentation for the project
```

## Usage

1. **Installation**: Clone the repository and install the required dependencies listed in `requirements.txt`.
2. **Running the Application**: Execute `src/index.py` to start the application and access the dictionary registry.
3. **Adding Dictionaries**: Use the `register_dictionary` method in `registry.py` to add new dictionaries.
4. **Retrieving Dictionaries**: Use the `get_dictionary` method to retrieve a specific dictionary by name.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.