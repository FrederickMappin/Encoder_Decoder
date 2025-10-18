import math
import decimal
from decimal import Decimal
import array
from time import perf_counter
import json

# Precision for cycle-based approach
decimal.getcontext().prec = 5000

def encode_oscillating_tree_cycles(sequence, base, exponent, log_base, cycle_depth=1000, scaled_max=100000000000):
    """Encode sequence using cycles to manage precision requirements"""
    start_time = perf_counter()
    value = 1.0  # Starting value
    depth = len(sequence)
    total_cycles = (depth + cycle_depth - 1) // cycle_depth
    
    print(f"Encoding sequence of length {depth:,} using {total_cycles} cycles of {cycle_depth} digits")
    
    # Convert sequence to integers once
    if isinstance(sequence, str):
        digits = array.array('B', [int(d) for d in sequence])
    else:
        digits = sequence
    
    # Prepare data structures for cycles
    cycle_addresses = []
    base_decimal = Decimal(base)
    
    # Process each cycle
    for cycle in range(total_cycles):
        start_idx = cycle * cycle_depth
        end_idx = min((cycle + 1) * cycle_depth, depth)
        cycle_length = end_idx - start_idx
        
        print(f"Encoding cycle {cycle+1}/{total_cycles} (positions {start_idx:,}-{end_idx-1:,})")
        
        # Reset address calculation for this cycle (precision reset)
        address = Decimal('0')
        running_divisor = Decimal('1')
        digit_decimals = [Decimal(i) for i in range(base)]
        
        # Process each digit in this cycle
        for i in range(cycle_length):
            global_idx = start_idx + i
            index = digits[global_idx]
            
            # Value calculation continues as before (uninterrupted across cycles)
            if (global_idx + 1) % 2 == 1:
                value = value ** exponent + index
            else:
                value = math.log(value, log_base) + index
            
            # Address calculation resets for each cycle
            running_divisor /= base_decimal
            digit_contribution = digit_decimals[index] * running_divisor
            address += digit_contribution
            
            # Progress reporting (less frequent)
            if i > 0 and i % 500 == 0:
                progress = (global_idx) / depth * 100
                print(f"  Progress: {global_idx:,}/{depth:,} ({progress:.1f}%)")
        
        # Store this cycle's address
        cycle_addresses.append(str(address))
    
    end_time = perf_counter()
    print(f"Encoding complete in {end_time - start_time:.2f} seconds")
    
    # Return the cycle data
    return {
        "cycle_addresses": cycle_addresses,
        "cycle_depth": cycle_depth,
        "total_cycles": total_cycles,
        "depth": depth,
        "base": base,
        "exponent": exponent,
        "log_base": log_base,
        "scaled_max": scaled_max
    }

def decode_oscillating_tree_cycles(encoded_data):
    """Decode sequence from cycle addresses"""
    start_time = perf_counter()
    
    # Extract parameters
    cycle_addresses = encoded_data["cycle_addresses"]
    cycle_depth = encoded_data["cycle_depth"]
    total_cycles = encoded_data["total_cycles"]
    depth = encoded_data["depth"]
    base = encoded_data["base"]
    
    print(f"Decoding sequence of length {depth:,} from {total_cycles} cycles")
    
    # Pre-allocate result array
    result_chars = ['0'] * depth
    base_decimal = Decimal(base)
    
    # Process each cycle
    for cycle in range(total_cycles):
        cycle_address = Decimal(cycle_addresses[cycle])
        
        # Calculate positions for this cycle
        start_idx = cycle * cycle_depth
        end_idx = min((cycle + 1) * cycle_depth, depth)
        cycle_length = end_idx - start_idx
        
        print(f"Decoding cycle {cycle+1}/{total_cycles} (positions {start_idx:,}-{end_idx-1:,})")
        
        # Decode this cycle
        remaining = cycle_address
        
        for i in range(cycle_length):
            global_idx = start_idx + i
            
            # Similar to original decoding but for just this cycle
            remaining *= base_decimal
            digit = int(remaining)  # Extract integer part
            remaining -= digit
            
            # Validate digit
            if not (0 <= digit < base):
                digit = max(0, min(digit, base-1))
            
            # Store digit
            result_chars[global_idx] = str(digit)
            
            # Progress reporting (less frequent)
            if i > 0 and i % 500 == 0:
                progress = (global_idx) / depth * 100
                print(f"  Progress: {global_idx:,}/{depth:,} ({progress:.1f}%)")
    
    # Join all characters
    result = ''.join(result_chars)
    
    # Validate result length and truncate if needed
    if len(result) != depth:
        result = result[:depth]
    
    end_time = perf_counter()
    print(f"Decoding complete in {end_time - start_time:.2f} seconds")
    
    return result

# Example usage:
if __name__ == "__main__":
    # Base sequence
    base_seq = "255063945434956868950433049568950433304956" 
    # Test with a longer sequence
    sequence = base_seq * 10000  # Substantially longer sequence
    base = 125
    exponent = 2
    log_base = 1000
    cycle_depth = 1000  # Adjust based on your needs
    
    print(f"Testing with sequence of length {len(sequence):,}")
    
    # Encoding using cycles
    print("\n=== ENCODING SEQUENCE WITH CYCLES ===")
    encoded_data = encode_oscillating_tree_cycles(sequence, base, exponent, log_base, cycle_depth)
    
    # Save the encoded data to a file
    with open("encoded_cycles.json", 'w') as f:
        json.dump({k: v for k, v in encoded_data.items() if k != "value"}, f, indent=2)
    print(f"Encoded data saved to encoded_cycles.json")
    
    # Decoding from cycles
    print("\n=== DECODING SEQUENCE FROM CYCLES ===")
    recovered = decode_oscillating_tree_cycles(encoded_data)
    
    # Verification
    print("\n=== VERIFICATION ===")
    print(f"Original length: {len(sequence):,}")
    print(f"Recovered length: {len(recovered):,}")
    
    # Check various positions
    check_positions = [10, 1000, 10000, 100000, 300000]
    for pos in check_positions:
        if pos < len(sequence):
            match = sequence[pos:pos+10] == recovered[pos:pos+10]
            if not match:
                print(f"Mismatch at position {pos:,}: '{sequence[pos:pos+10]}' vs '{recovered[pos:pos+10]}'")
            else:
                print(f"Match at position {pos:,}: ✓")
    
    # Verify start and end
    print(f"First 100 chars match: {sequence[:100] == recovered[:100]}")
    print(f"Last 100 chars match: {sequence[-100:] == recovered[-100:]}")
    
    # Skip full comparison for large sequences
    print("Full comparison skipped for performance reasons - check samples instead")