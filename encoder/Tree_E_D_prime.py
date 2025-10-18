"""
# Tree Depth Analysis for Base 3

When you change the base to 3 (as in your current code), the tree becomes a ternary tree where each node has 3 children. Let's analyze the depth and structure for the example leaf address 124596:

## Path Tracing Analysis for Leaf Address 124596 with Base 3

```
124596 → Parent: 41532, Child index: 0 (1st child)
41532 → Parent: 13844, Child index: 0 (1st child)
13844 → Parent: 4615, Child index: 2 (3rd child)
4615 → Parent: 1539, Child index: 1 (2nd child)
1539 → Parent: 513, Child index: 0 (1st child)
513 → Parent: 171, Child index: 0 (1st child)
171 → Parent: 57, Child index: 0 (1st child)
57 → Parent: 19, Child index: 0 (1st child)
19 → Parent: 7, Child index: 1 (2nd child)
7 → Parent: 3, Child index: 1 (2nd child)
3 → Parent: 1, Child index: 0 (1st child)
1 → Root
```

This shows the leaf node is at **level 12** of the tree (including the root).

## Base 3 Tree Structure

- **Root Level**: 3 nodes (addresses 1-3)
- **Level 1**: 9 nodes (addresses 4-12)
- **Level 2**: 27 nodes (addresses 13-39)
- **Level 3**: 81 nodes (addresses 40-120)
- **Level 4**: 243 nodes
- **Level 5**: 729 nodes
- **Level 6**: 2,187 nodes
- **Level 7**: 6,561 nodes
- **Level 8**: 19,683 nodes
- **Level 9**: 59,049 nodes
- **Level 10**: 177,147 nodes
- **Level 11**: 531,441 nodes (Address 124596 falls in this level)
"""

def find_parent(child_address, base):
    """
    Find the parent address and child index for a given child address.
    This must be the exact inverse of the encoding operation in encode_data.
    """
    # For nodes 1 through base, they are root nodes with no parent
    if child_address <= base:
        return None, None
    
    # Calculate parent and child index
    # This is the exact inverse of the formula in encode_data:
    # current_address = base * current_address + child_index + 1
    child_index = (child_address - 1) % base  # Get the remainder
    parent_address = (child_address - 1 - child_index) // base  # Integer division
    
    return parent_address, child_index

def encode_data(data_to_encode, base, dna_dict):
    """
    Encodes the given data into a tree structure and returns the final current address.
    """
    # Reverse the dictionary for fast lookups
    reverse_dna_dict = {v: k for k, v in dna_dict.items()}

    # Initialize with the root character
    root_char = data_to_encode[0]
    root_value = reverse_dna_dict[root_char]
    current_address = root_value

    # Process remaining characters
    for i in range(1, len(data_to_encode)):
        next_char = data_to_encode[i]
        child_index = reverse_dna_dict[next_char] - 1  # Convert to 0-indexed
        
        # Calculate the address of the child
        current_address = base * current_address + child_index + 1
        
    return current_address

def trace_path_to_root(leaf_address, base, dna_dict):
    """
    Trace the path from a leaf node to the root, returning all characters along the path.
    """
    current_address = leaf_address
    path_indices = []
    
    # Trace until we reach a root node (nodes 1-base)
    while current_address > base:
        parent_address, child_index = find_parent(current_address, base)
        path_indices.append(child_index + 1)  # +1 because your dict is 1-indexed
        current_address = parent_address
    
    # Add the root node value
    path_indices.append(current_address)
    
    # Convert indices to characters and reverse (root to leaf)
    reversed_indices = list(reversed(path_indices))
    path_chars = [dna_dict[idx] for idx in reversed_indices]
    
    return path_chars

if __name__ == "__main__":
    # Example usage with leaf address 5
    leaf_address = 3400000
    base = 4
    
    # DNA dictionary (1-indexed)
    dna_dict = {
        0: "null",
        1: 'A',
        2: 'T',
        3: 'C',
        4: 'G'
    }
    
    #Example usage. Decoding 
    path = trace_path_to_root(leaf_address, base, dna_dict)
    path_str = ''.join(path)
    print(f"Path from root to leaf: {path_str}")




     # Example usage: Encoding 
    dna_sequence = "TGCCACGGCCG"
    address = encode_data(dna_sequence, base, dna_dict)
    print(f"The address for '{dna_sequence}' is: {address}")



    """"
    Test case 1: Trace path from leaf to root and back
    path = trace_path_to_root(leaf_address, base, dna_dict)
    path_str = ''.join(path)
    print(f"Path from root to leaf: {path_str}")
    
    # Re-encode the path to verify
    final_address = encode_data(path_str, base, dna_dict)
    print(f"Re-encoded address: {final_address}")
    
    # Verify that encoding and decoding are inverses
    assert final_address == leaf_address, "Encoding/decoding mismatch!"
    print("Success! Encoding and decoding match.")
    
    # Test case 2: Try with a different address
    leaf_address_2 = 17
    path_2 = trace_path_to_root(leaf_address_2, base, dna_dict)
    path_str_2 = ''.join(path_2)
    print(f"\nTest case 2 - Path from root to leaf: {path_str_2}")
    
    final_address_2 = encode_data(path_str_2, base, dna_dict)
    print(f"Re-encoded address: {final_address_2}")
    
    assert final_address_2 == leaf_address_2, "Encoding/decoding mismatch!"
    print("Success! Encoding and decoding match.")
    """