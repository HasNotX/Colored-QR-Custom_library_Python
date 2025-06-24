import numpy as np
import matplotlib.pyplot as plt

#Function to draw b's in matrix
def draw_pattern(matrix,x,y):
    matrix[y,x]= 'b'

#Function to draw w's in matrix
def draw_blank(matrix,x,y):
    matrix[x, y] = 'w'

#Function to draw r's in matrix
def draw_reserve(matrix,x,y):
    if(matrix[x,y]!='b'):
        matrix[x,y]='r'




#Finder Pattern Drawing Logic
def finder_pattern(matrix, pos):
   
    arrowx= pos[0]
    arrowy= pos[1]

    #Outer Boundary
    for i in range(6):
        draw_pattern(matrix,arrowx,arrowy)
        arrowx +=1
        
    for i in range(6):
        draw_pattern(matrix,arrowx,arrowy)
        arrowy +=1    

    for i in range(6):
        draw_pattern(matrix,arrowx,arrowy)
        arrowx -=1 

    for i in range(6):
        draw_pattern(matrix,arrowx,arrowy)
        arrowy -=1

    arrowx= pos[0]
    arrowy= pos[1]
    
    #Inner Square
    for dx in range(3):
        for dy in range(3):
            draw_pattern(matrix, arrowx+2+dx, arrowy+2+dy)

    for dx in range(1, 6):
        for dy in range(1, 6):
            if matrix[arrowx + dx, arrowy + dy] == '0':
                draw_blank(matrix, arrowx + dx, arrowy + dy)

#Finder Patern Locater / Master func
def draw_finder_pattern(matrix,  matrix_size):
     
    #Starting Positions
    topLeft= (0,0)
    topRight= (matrix_size-7,0)
    bottomLeft= (0,matrix_size-7)

    finder_pattern(matrix, topLeft)
    finder_pattern(matrix, topRight)
    finder_pattern(matrix, bottomLeft)

#Draw Alignment pattern
def draw_align_pattern(matrix):
    pattern_loc= (18,18)
    draw_pattern(matrix,pattern_loc[0],pattern_loc[1])

    arrowx= pattern_loc[0]- 2
    arrowy= pattern_loc[1]- 2

    #Outer Boundary
    for i in range(4):
        draw_pattern(matrix,arrowx,arrowy)
        arrowx +=1
        
    for i in range(4):
        draw_pattern(matrix,arrowx,arrowy)
        arrowy +=1    

    for i in range(4):
        draw_pattern(matrix,arrowx,arrowy)
        arrowx -=1 

    for i in range(4):
        draw_pattern(matrix,arrowx,arrowy)
        arrowy -=1 

    arrowx= pattern_loc[0]- 2
    arrowy= pattern_loc[1]- 2

    for dx in range(1, 4):
        for dy in range(1, 4):
            if matrix[arrowx + dx, arrowy + dy] == '0':
                draw_blank(matrix, arrowx + dx, arrowy + dy)

#Draw Seperators around Finders
def draw_seperators(size, matrix):
    size-=1
    posx= 7
    posy= 0
    
    for i in range(7):
        draw_blank(matrix, posy, posx)
        posy+= 1
    for i in range(8):
        draw_blank(matrix, posy, posx)
        posx-= 1

    posx= size-7
    posy= 0

    for i in range(7):
        draw_blank(matrix, posy, posx)
        posy+= 1
    for i in range(8):
        draw_blank(matrix, posy, posx)
        posx+= 1

    posx= 0
    posy= size-7

    for i in range(7):
        draw_blank(matrix, posy, posx)
        posx+= 1
    for i in range(8):
        draw_blank(matrix, posy, posx)
        posy+= 1

#Draw Timing Patterns
def draw_timing_patterns(size, matrix):
    

    for x in range(8, size - 8):
        if x % 2 == 0:
            draw_pattern(matrix, x, 6)  # fixed row
        else:
            draw_blank(matrix, 6, x)

    for y in range(8, size - 8):
        if y % 2 == 0:
            draw_pattern(matrix, 6, y)  # fixed row
        else:
            draw_blank(matrix, y, 6)

#Reserve Fromat Information Area
def draw_format_info(size, matrix):
    posx= 8
    posy= 0
    for i in range(8):
        draw_reserve(matrix, posy, posx)
        posy+= 1
    posy= 8
    posx= 0

    for i in range(9):
        draw_reserve(matrix, posy, posx)
        posx+= 1

    posx= size-8
    posy= 8

    for i in range(8):
        draw_reserve(matrix, posy, posx)
        posx+= 1

    posx= 8
    posy= size-1

    for i in range(7):
        draw_reserve(matrix, posy, posx)
        posy-= 1


#Main Drawing Function
def draw_func_data(version):
    #size calculations
    matrix_size= (((version-1)*4)+21)
    matrix = np.full((matrix_size, matrix_size), '0', dtype=object)

   

    draw_finder_pattern(matrix, matrix_size)
    
    draw_align_pattern(matrix)

    draw_seperators(matrix_size, matrix)

    draw_timing_patterns(matrix_size,matrix)

    draw_format_info(matrix_size, matrix )

    draw_pattern(matrix, 8, matrix_size-8)
    

    return matrix


    for row in matrix:
        line = ''
        for cell in row:
            if cell in ['b', 1, '1']:  # black module
                line += '██'
            elif cell in ['w', 0, '0']:  # white module
                line += '  '
            
            else:  # for special placeholders
                line += '░░'
        print(line)

if __name__ == "__main__":
    version= 2
    mat= draw_func_data(version)

   





