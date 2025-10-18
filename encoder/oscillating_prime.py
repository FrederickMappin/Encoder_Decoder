import math

def find_parent_standard(child_address, base):
    """
    Standard parent finder - unchanged from original.
    """
    # For nodes 1 through base, they are root nodes with no parent
    if child_address <= base:
        return None, None
    
    # Calculate parent and child index
    child_index = (child_address - 1) % base
    parent_address = (child_address - 1 - child_index) // base
    
    return parent_address, child_index

def encode_data(data_to_encode, base, dna_dict):
    """
    Encodes the given data using standard tree encoding.
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

def calculate_child_address(parent_address, child_index, level, base):
    """
    Calculate child address using oscillating transformations based on level.
    """
    print(f"Calculating child at level {level}: parent={parent_address}, child_index={child_index}")

    if level % 2 == 0:  # Even levels use power transformation
        # Power transformation (x^2)
        transformed = parent_address ** 2
        child_address = transformed + child_index + 1
        print(f"  Level {level} (POWER): {parent_address}^2 + {child_index} + 1 = {child_address}")
    else:  # Odd levels use logarithmic transformation
        # Logarithmic transformation - using base 2 log
        if parent_address <= 1:
            transformed = 0  # Handle special case
        else:
            transformed = math.log2(parent_address)
        child_address = transformed + child_index + 1
        print(f"  Level {level} (LOG): log2({parent_address}) + {child_index} + 1 = {child_address}")
    
    return child_address

def find_parent_oscillating(child_address, child_level, base):
    """
    Find parent using oscillating inverse transformations.
    """
    print(f"Finding parent of {child_address} at level {child_level}")
    
    # Level 0 nodes have no parent
    if child_level == 0:
        print(f"  Node at level 0 has no parent")
        return None, None
    
    # Calculate the parent's level
    parent_level = child_level - 1
    
    # First determine the child index
    child_idx = int((child_address - 1) % base)
    
    # Calculate the transformed value
    transformed_value = child_address - child_idx - 1
    print(f"  Transformed value: {transformed_value} = {child_address} - {child_idx} - 1")
    
    # Apply inverse transformation based on level
    if child_level % 2 == 0:  # Even child level means we used power transform
        # Inverse is square root
        parent_address = math.sqrt(transformed_value)
        print(f"  Inverse POWER: sqrt({transformed_value}) = {parent_address}")
    else:  # Odd child level means we used log transform
        # Inverse is 2^x
        parent_address = 2 ** transformed_value
        print(f"  Inverse LOG: 2^{transformed_value} = {parent_address}")
    
    # Round to handle floating point issues
    if abs(parent_address - round(parent_address)) < 1e-10:
        parent_address = int(round(parent_address))
    
    print(f"  Parent address: {parent_address}, Child index: {child_idx}")
    return parent_address, child_idx

def encode_data_oscillating(data_to_encode, base, dna_dict):
    """
    Encodes data using oscillating transformations.
    """
    # Reverse the dictionary for fast lookups
    reverse_dna_dict = {v: k for k, v in dna_dict.items()}

    # Initialize with the root character
    root_char = data_to_encode[0]
    root_value = reverse_dna_dict[root_char]
    current_address = root_value
    current_level = 0

    print(f"Encoding '{data_to_encode}'")
    print(f"  Root character: {root_char}, Root value: {root_value}")

    # Process remaining characters
    for i in range(1, len(data_to_encode)):
        next_char = data_to_encode[i]
        child_index = reverse_dna_dict[next_char] - 1  # Convert to 0-indexed
        current_level += 1
        
        # Calculate the address of the child using oscillating transforms
        current_address = calculate_child_address(
            current_address, child_index, current_level, base)
        
        print(f"  Level {current_level}: Char={next_char}, Index={child_index}, Address={current_address}")
        
    return current_address, current_level

def trace_path_oscillating(leaf_address, leaf_level, base, dna_dict):
    """
    Trace path from leaf to root using oscillating transforms.
    """
    current_address = leaf_address
    current_level = leaf_level
    path_indices = []
    
    print(f"Tracing path from address {leaf_address} at level {leaf_level}")
    
    # Trace until we reach a root node (level 0)
    while current_level > 0:
        parent_address, child_index = find_parent_oscillating(current_address, current_level, base)
        if parent_address is None:
            break
            
        path_indices.append(child_index + 1)  # +1 because dict is 1-indexed
        print(f"  Node at level {current_level}: parent={parent_address}, child_index={child_index}")
        
        current_address = parent_address
        current_level -= 1
    
    # Add the root node value
    path_indices.append(int(current_address))
    print(f"  Root node value: {current_address}")
    
    # Convert indices to characters and reverse (root to leaf)
    reversed_indices = list(reversed(path_indices))
    print(f"  Path indices (root to leaf): {reversed_indices}")
    
    path_chars = [dna_dict[idx] for idx in reversed_indices]
    print(f"  Path characters: {path_chars}")
    
    return path_chars

def standard_to_oscillating_address(standard_address, base):
    """
    Convert a standard tree address to an oscillating tree address.
    This traces the path in the standard tree and re-encodes it in the oscillating tree.
    """
    # First trace the path in the standard tree
    path_indices = []
    current = standard_address
    
    print(f"Converting standard address {standard_address} to oscillating address")
    
    while current > base:
        parent, idx = find_parent_standard(current, base)
        path_indices.append(idx)
        current = parent
    
    path_indices.append(current-1)  # Add root index (0-based)
    path_indices.reverse()  # Root to leaf order
    
    print(f"  Path indices in standard tree: {path_indices}")
    
    # Now encode using oscillating transformations
    oscillating_address = path_indices[0] + 1  # Root address (1-based)
    current_level = 0
    
    for i in range(1, len(path_indices)):
        current_level += 1
        child_idx = path_indices[i]
        oscillating_address = calculate_child_address(
            oscillating_address, child_idx, current_level, base)
    
    print(f"  Equivalent oscillating address: {oscillating_address} at level {current_level}")
    return oscillating_address, current_level

if __name__ == "__main__":
    base = 4
    
    # DNA dictionary (1-indexed)
    dna_dict = {
        0: "null",
        1: 'A',
        2: 'T',
        3: 'C',
        4: 'G'
    }
    
    print("\n===== TESTING OSCILLATING TREE ENCODING =====")
    
    # Test encoding a short sequence
    dna_sequence = "TGCCA"
    oscillating_address, level = encode_data_oscillating(dna_sequence, base, dna_dict)
    print(f"\nFinal oscillating address for '{dna_sequence}': {oscillating_address} at level {level}")
    
    # Test decoding the oscillating address
    print("\n===== TESTING OSCILLATING TREE DECODING =====")
    path = trace_path_oscillating(oscillating_address, level, base, dna_dict)
    path_str = ''.join(path)
    print(f"\nDecoded path: {path_str}")
    
    # Verify encoding/decoding match
    if path_str == dna_sequence:
        print("\nSuccess! Oscillating encoding/decoding match.")
    else:
        print(f"\nMismatch! Expected '{dna_sequence}' but got '{path_str}'")
    
    # Test with standard encoding for reference
    print("\n===== COMPARING WITH STANDARD TREE =====")
    standard_address = encode_data(dna_sequence, base, dna_dict)
    print(f"\nStandard address for '{dna_sequence}': {standard_address}")
    print(f"Oscillating address for '{dna_sequence}': {oscillating_address}")
    
    # Show address space savings
    test_sequences = [
        "A",
        "AT",
        "ATC",
        "ATCG",
        "ATCGA",
        "ATCGAT",
        "ATCGATC",
        "ATCGATCG"
    ]
    
    print("\n===== ADDRESS SPACE COMPARISON =====")
    print("Sequence | Standard Address | Oscillating Address | Savings")
    print("---------|------------------|---------------------|--------")
    
    for seq in test_sequences:
        std_addr = encode_data(seq, base, dna_dict)
        osc_addr, _ = encode_data_oscillating(seq, base, dna_dict)
        savings = (1 - (osc_addr / std_addr)) * 100 if std_addr > 0 else 0
        print(f"{seq:9} | {std_addr:16} | {osc_addr:19} | {savings:.2f}%")
    
    # Test the alternative oscillation scheme with stronger compression
    print("\n===== TESTING ALTERNATIVE OSCILLATION SCHEME =====")
    
    # Define a function for stronger compression
    def calculate_child_address_alt(parent_address, child_index, level, base):
        print(f"Calculating child at level {level}: parent={parent_address}, child_index={child_index}")
        
        if level % 2 == 0:  # Even levels: moderate growth
            power_factor = 1.5
            transformed = parent_address ** power_factor
            child_address = transformed + child_index + 1
            print(f"  Level {level} (POWER^1.5): {parent_address}^{power_factor} + {child_index} + 1 = {child_address}")
        else:  # Odd levels: stronger compression
            if parent_address <= 1:
                transformed = 0
            else:
                # Strong logarithmic compression
                transformed = math.log10(parent_address)
            child_address = transformed + child_index + 1
            print(f"  Level {level} (LOG10): log10({parent_address}) + {child_index} + 1 = {child_address}")
        
        return child_address
        
    print("\nComparing address spaces with different compression schemes:")
    print("Sequence | Standard | Basic Osc | Strong Compression")
    print("---------|----------|-----------|------------------")
    
    for seq in test_sequences[:5]:  # First 5 sequences
        std_addr = encode_data(seq, base, dna_dict)
        
        # Create reverse dictionary for the compression tests
        reverse_dna_dict = {v: k for k, v in dna_dict.items()}
        
        # Original oscillating encoding
        current_level = 0
        current_addr = reverse_dna_dict[seq[0]]
        for i in range(1, len(seq)):
            current_level += 1
            child_idx = reverse_dna_dict[seq[i]] - 1
            current_addr = calculate_child_address(current_addr, child_idx, current_level, base)
        basic_osc = current_addr
        
        # Strong compression oscillating encoding
        current_level = 0
        current_addr = reverse_dna_dict[seq[0]]
        for i in range(1, len(seq)):
            current_level += 1
            child_idx = reverse_dna_dict[seq[i]] - 1
            current_addr = calculate_child_address_alt(current_addr, child_idx, current_level, base)
        strong_osc = current_addr
        
        print(f"{seq:9} | {std_addr:8} | {basic_osc:9.2f} | {strong_osc:8.2f}")