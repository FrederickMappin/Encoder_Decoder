from registry import DictionaryRegistry

def test_dictionary_registry():
    # Create a registry instance
    registry = DictionaryRegistry()

    # Original dictionary
    dna_dict = {
        0: 'A',
        1: 'T',
        2: 'G',
        3: 'C'
    }

    # Expected processed dictionary
    expected_processed_dict = {
        'A': 1,
        'T': 2,
        'G': 3,
        'C': 4,
        'null': 0
    }

    # Register the dictionary
    registry.register_dictionary("dna", dna_dict)
  

    # Retrieve the processed dictionary
    processed_dna_dict = registry.get_dictionary("dna")
    

    # Assertions
    assert processed_dna_dict == expected_processed_dict, "Processed dictionary does not match expected output."

    # Test listing dictionaries
    assert registry.list_dictionaries() == ["dna"], "Dictionary name not listed correctly."

    print("All tests passed!")

# Run the test
if __name__ == "__main__":
    test_dictionary_registry()