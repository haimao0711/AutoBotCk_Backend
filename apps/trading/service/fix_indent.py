
import os

file_path = "e:\\ANguyenBot\\stock-predict-cms-be\\apps\\trading\\service\\handlers.py"

def indent_lines(start_line, end_line):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Adjust for 0-based index
    start_idx = start_line - 1
    end_idx = end_line # Slice is exclusive of end, so end_line index is excluded if range is [start, end)
                      # But end_line argument is inclusive? Standard is inclusive.
                      # Let's say lines 545 to 938. 
                      # line 545 is index 544.
                      # line 938 is index 937.
    
    # Check bounds
    if start_idx < 0 or end_idx > len(lines):
        print(f"Error: Range {start_line}-{end_line} out of bounds.")
        return

    print(f"Indenting lines {start_line} to {end_line}")
    for i in range(start_idx, end_idx):
        if lines[i].strip(): # Only indent non-empty lines
            lines[i] = "    " + lines[i]
            
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Done.")

# Ranges determined from analysis:
# process_buy_request: lines 545 to 938 (inclusive)
# process_sell_request: lines 1023 to 1384 (inclusive)

# Execute
indent_lines(545, 938)
indent_lines(1023, 1384)
