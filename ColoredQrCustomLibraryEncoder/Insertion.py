import json
import DataEnc
import FuncData
import numpy as np
import matplotlib.pyplot as plt
import reedsolo

def drawQR(sentence, version):
    matrix= FuncData.draw_func_data(version)
    dataStream= DataEnc.send_sent(sentence)
    bitstream = ''.join(format(byte, '08b') for byte in dataStream)
    print(dataStream)
    color_encoded_data= color_encode(dataStream)
    enc_stream= ''.join(color_encoded_data)
    print(enc_stream)
    draw_matrix(enc_stream, matrix)
    
   
    
def color_encode(data):
    hex_vals= [hex(num) for num in data]
    hex_vals= [num.upper() for num in hex_vals]
    hex_vals = [h[2:] for h in hex_vals]
    print("Hex vals list are" , hex_vals)
    hex_vals= ''.join(hex_vals)

    print("Hex vals list are" , hex_vals)
    
    with open("data_key.json", "r") as f:
        color_map = json.load(f)

    keyed_data= [color_map.get(hex_digit,"#000000")  for hex_digit in hex_vals]
    print(keyed_data)

    return(keyed_data)
             

#Printing matrix to visualise
def draw_matrix(data, mat):
    insert_data(mat, data)
    for row in mat:
        print(' '.join(str(int(cell)) if isinstance(cell, float) else str(cell) for cell in row))
    new_mat= post_process(mat)
    print(data)
    render_matrix(new_mat)


def insert_data(matrix, bitstream):
    """
    Inserts a 359-bit bitstream (352 data + 7 padding) into a Version 2 (25x25) QR matrix.
    Follows the standard QR code module placement order (zig-zag vertical pairs).
    
    Args:
        bitstream (str): 359-bit string (e.g., "010101...0000000")
        matrix (list): 25x25 QR matrix (modified in-place)
    """
    size = 25  # Version 2 QR code
    bit_index = 0
    going_up = True  # Start moving upward (bottom to top)
    col = size - 1   # Start from the rightmost column

    while col >= 0 and bit_index < len(bitstream):
        # Skip vertical timing pattern (column 6)
        if col == 6:
            col -= 1
            continue

        # Determine row traversal direction (up or down)
        rows = range(size - 1, -1, -1) if going_up else range(size)

        for row in rows:
            # Process current column (right side of the pair)
            if 0 <= row < size and 0 <= col < size:
                if matrix[row][col] in ('0', None):  # Empty module
                    if bit_index < len(bitstream):
                        matrix[row][col] = bitstream[bit_index]
                        bit_index += 1
                    else:
                        return  # All bits placed
            
            # Process left column (if exists)
            if col > 0:
                left_col = col - 1
                if 0 <= row < size and 0 <= left_col < size:
                    if matrix[row][left_col] in ('0', None):  # Empty module
                        if bit_index < len(bitstream):
                            matrix[row][left_col] = bitstream[bit_index]
                            bit_index += 1
                        else:
                            return  # All bits placed

        # Move left by 2 columns and reverse direction
        col -= 2
        going_up = not going_up

import numpy as np
import matplotlib.pyplot as plt
import json

# Load color map from JSON file
with open("color_key.json", "r") as f:
    color_map = json.load(f)

def render_matrix(matrix):
    h, w = len(matrix), len(matrix[0])
    image = np.zeros((h, w, 3), dtype=np.uint8)

    for y in range(h):
        for x in range(w):
            cell = matrix[y][x]
            hex_color = color_map.get(cell, "#AAAAAA")  # fallback color
            # Convert hex color string to RGB tuple
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
            image[y, x] = rgb

    plt.imshow(image)
    plt.title("Colored QR Code Matrix")
    plt.axis('off')
    plt.show()

def apply_mask_pattern_0(matrix):
    """
    Applies Mask Pattern 0 (checkerboard) to a QR matrix where:
    - 'b' = black (1)
    - 'w' = white (0)
    - '0'/'1' = data bits to be masked
    """
    size = len(matrix)
    for i in range(size):
        for j in range(size):
            if (i + j) % 2 == 0:
                # Invert the module (works for '0'/'1')
                if matrix[i][j] == '0':
                    matrix[i][j] = '1'  # Change to black/data
                elif matrix[i][j] == '1':
                    matrix[i][j] = '0'  # Change to white/data
                elif matrix[i][j] == 'z':
                    matrix[i][j]= '5'
                elif matrix[i][j] == 'o':
                    matrix[i][j]= '4'
                elif matrix[i][j] == '2':
                    matrix[i][j]= '3'
                elif matrix[i][j] == '6':
                    matrix[i][j]= 'c'
                elif matrix[i][j] == '7':
                    matrix[i][j]= 'd'
                elif matrix[i][j] == '8':
                    matrix[i][j]= 'a'
                elif matrix[i][j] == '9':
                    matrix[i][j]= 'p'
                elif matrix[i][j] == 'e':
                    matrix[i][j]= 'f'
   
    return matrix

def post_process(matrix):

    new_mat=apply_mask_pattern_0(matrix)
    for row in range(len(new_mat)):
        for col in range(len(new_mat[row])):
            if new_mat[row][col] == 'w':  
                new_mat[row][col] = '0' 

    for row in range(len(new_mat)):
        for col in range(len(new_mat[row])):
            if new_mat[row][col] == 'b':  
                new_mat[row][col] = '1' 

    mat_new= insert_format_string(new_mat, "011011111000100")
    return mat_new

def insert_format_string(matrix, format_str):
    """
    Inserts a 15-bit format string into the QR matrix at the required positions.
    For Version 2 (25x25) QR codes.
    
    Args:
        matrix: 25x25 QR matrix (modified in-place)
        format_str: 15-bit string (e.g., '111011111000100' for ECC level H, mask 0)
    """
    size = len(matrix)
    
    # Primary format area (around top-left finder)
    format_coords_top = [
        (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 7), (8, 8),
        (7, 8), (5, 8), (4, 8), (3, 8), (2, 8), (1, 8), (0, 8)
    ]
    
    # Secondary format area (near top-right and bottom-left finders)
    format_coords_secondary = [
        (size-1, 8), (size-2, 8), (size-3, 8), (size-4, 8), (size-5, 8), (size-6, 8), (size-7, 8),
        (8, size-8), (8, size-7), (8, size-6), (8, size-5), (8, size-4), (8, size-3), (8, size-2), (8, size-1)
    ]
    
    # Insert into primary area
    for idx, (i, j) in enumerate(format_coords_top):
        if idx < len(format_str):
            matrix[i][j] = format_str[idx]
    
    # Insert into secondary areas (redundant copies)
    for idx, (i, j) in enumerate(format_coords_secondary):
        if idx < len(format_str):
            matrix[i][j] = format_str[idx]

    return matrix



sent= "hello"
version= 2

drawQR(sent, version)









#For Debuging
"""
for row in matrix:
        print(' '.join(str(int(cell)) if isinstance(cell, float) else str(cell) for cell in row))

count_0 = np.count_nonzero(matrix == '0')
count_b = np.count_nonzero(matrix == 'b')
count_w = np.count_nonzero(matrix == 'w')
count_r = np.count_nonzero(matrix == 'r')
print("Count of 0, b, w, r:", count_0, count_b, count_w, count_r)

"""