import pygame
import tkinter as tk
from tkinter.simpledialog import askstring

def cx_question():
    root = tk.Tk()
    ans = askstring('cx','On which qubit should we place X?')
    root.withdraw()
    return(ans)
TILESIZE = 80
n = int(input("Enter number of qubits: "))
n = n+2
m=30
BOARD_POS = (10, 10)

menu = ['H','Px','Py','Pz','C']

def create_board_surf():
    board_surf = pygame.Surface((TILESIZE*m, TILESIZE*n))
    dark = False
    for x in range(len(menu)):
        rect = pygame.Rect(x*TILESIZE, 0*TILESIZE, TILESIZE, TILESIZE)
        pygame.draw.rect(board_surf, pygame.Color('green'), rect)
        rect = pygame.Rect(x*TILESIZE, 1*TILESIZE, TILESIZE, TILESIZE)
        pygame.draw.rect(board_surf, pygame.Color('beige'), rect)
        pygame.draw.line(board_surf, pygame.Color('darkgrey'), (x*TILESIZE, 0*TILESIZE),(x*TILESIZE, (1)*TILESIZE),2)
    
    # for run button 
    for x in range(len(menu),len(menu)+1):
        rect = pygame.Rect(x*TILESIZE, 0*TILESIZE, TILESIZE, TILESIZE)
        pygame.draw.rect(board_surf, pygame.Color('red'), rect)
        rect = pygame.Rect(x*TILESIZE, 1*TILESIZE, TILESIZE, TILESIZE)
        pygame.draw.rect(board_surf, pygame.Color('beige'), rect)
        pygame.draw.line(board_surf, pygame.Color('darkgrey'), (x*TILESIZE, 0*TILESIZE),(x*TILESIZE, (1)*TILESIZE),2)
        pygame.draw.polygon(board_surf, pygame.Color('green'), [(x*TILESIZE+15,15),(x*TILESIZE+15,TILESIZE-15),((x+1)*TILESIZE-15,TILESIZE//2)])

    for x in range(len(menu)+1,m):
        rect = pygame.Rect(x*TILESIZE, 0*TILESIZE, TILESIZE, 2*TILESIZE)
        pygame.draw.rect(board_surf, pygame.Color('beige'), rect)
        #pygame.draw.line(board_surf, pygame.Color('darkgrey'), (x*TILESIZE, 0*TILESIZE),(x*TILESIZE, (1)*TILESIZE),2)

    for y in range(2,n):
        x = 0
        rect = pygame.Rect(x*TILESIZE, y*TILESIZE, TILESIZE, TILESIZE)
        pygame.draw.rect(board_surf, pygame.Color('darkgrey' if dark else 'beige'), rect)
        for x in range(1,m):
            rect = pygame.Rect(x*TILESIZE, y*TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(board_surf, pygame.Color('darkgrey' if dark else 'beige'), rect)
            pygame.draw.line(board_surf, pygame.Color('black'), (x*TILESIZE, (y+0.5)*TILESIZE),((x+1)*TILESIZE, (y+0.5)*TILESIZE),4)
            pygame.draw.line(board_surf, pygame.Color('darkgrey'), ((x+0.5)*TILESIZE, y*TILESIZE),((x+0.5)*TILESIZE, (y+1)*TILESIZE),1)
        
    return board_surf

def get_square_under_mouse(board):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - BOARD_POS
    x, y = [int(v // TILESIZE) for v in mouse_pos]
    try: 
        if x >= 0 and y >= 0: return (board[y][x], x, y)
    except IndexError: pass
    return None, None, None

def get_gate_under_mouse(board):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - BOARD_POS
    x, y = [int(v // TILESIZE) for v in mouse_pos]
    try: 
        if x >= 0 and y == 0 and x<len(menu): return (menu[x], x, y)
    except IndexError: pass
    return None, None, None
    
def get_run_under_mouse(board):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - BOARD_POS
    x, y = [int(v // TILESIZE) for v in mouse_pos]
    try: 
        if x == len(menu) and y == 0 : return True
    except IndexError: pass
    return False

def get_qubit_under_mouse(board):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - BOARD_POS
    x, y = [int(v // TILESIZE) for v in mouse_pos]
    try: 
        if x == 0 and y >= 2: return (board[y][x], x, y)
    except IndexError: pass
    return None, None, None

def create_circuit():
    circuit = []
    for y in range(n):
        circuit.append([0])
        for x in range(1,m):
            circuit[y].append(None)
    return circuit
    


def draw_pieces(screen, board, font, selected_gate):
    sx, sy = None, None
    if selected_gate:
        gate, sx, sy = selected_gate

    for y in range(2,n):
        # for qubits
        for x in range(0,1):
            color="black"
            type = str(board[y][x])
            selected = x == sx and y == sy
            s1 = font.render(type, True, pygame.Color('red' if selected else color))
            s2 = font.render(type, True, pygame.Color('darkgrey'))
            pos = pygame.Rect(BOARD_POS[0] + x * TILESIZE+1, BOARD_POS[1] + y * TILESIZE + 1, TILESIZE, TILESIZE)
            screen.blit(s2, s2.get_rect(center=pos.center).move(1, 1))
            screen.blit(s1, s1.get_rect(center=pos.center))

        # for gates
        for x in range(1,m):
            gate = board[y][x]
            if gate:
                selected = x == sx and y == sy
                type = gate
                color="black"
                rect = (BOARD_POS[0] + x * TILESIZE, BOARD_POS[1] + y * TILESIZE, TILESIZE, TILESIZE)
                pygame.draw.rect(screen, pygame.Color('green'), rect)
                pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)
                s1 = font.render(type, True, pygame.Color('red' if selected else color))
                s2 = font.render(type, True, pygame.Color('darkgrey'))
                pos = pygame.Rect(BOARD_POS[0] + x * TILESIZE+1, BOARD_POS[1] + y * TILESIZE + 1, TILESIZE, TILESIZE)    
                screen.blit(s2, s2.get_rect(center=pos.center).move(1, 1))
                screen.blit(s1, s1.get_rect(center=pos.center))
                
            if gate=="C":
                for i in range(y+1,n):
                    if(board[i][x]=="X"):
                        break
                    pygame.draw.line(screen, pygame.Color('red'), ((x+0.5)*TILESIZE, i*TILESIZE),((x+0.5)*TILESIZE, (i+1)*TILESIZE),4)
                    
                        
                
                

def draw_menu(screen, board, font, selected_gate):
    y=0
    sx, sy = None, None
    if selected_gate:
        gate, sx, sy = selected_gate
    for x in range(len(menu)):
        selected = x==sx
        type = menu[x]
        color = "black"
        s1 = font.render(type, True, pygame.Color('red' if selected else color))
        s2 = font.render(type, True, pygame.Color('darkgrey'))
        pos = pygame.Rect(BOARD_POS[0] + x * TILESIZE+1, BOARD_POS[1] + y * TILESIZE + 1, TILESIZE, TILESIZE)
        screen.blit(s2, s2.get_rect(center=pos.center).move(1, 1))
        screen.blit(s1, s1.get_rect(center=pos.center))
    
    
    
    
def draw_selector(screen, piece, x, y):
    if piece != None:
        rect = (BOARD_POS[0] + x * TILESIZE, BOARD_POS[1] + y * TILESIZE, TILESIZE, TILESIZE)
        pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)

def draw_drag(screen, board, selected_gate, font):
    if selected_gate:
        gate, x, y = get_square_under_mouse(board)
        if x != None:
            rect = (BOARD_POS[0] + x * TILESIZE, BOARD_POS[1] + y * TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(screen, (0, 255, 0, 50), rect, 2)

        color = "black"
        type = selected_gate[0]
        s1 = font.render(type, True, pygame.Color(color))
        s2 = font.render(type, True, pygame.Color('darkgrey'))
        pos = pygame.Vector2(pygame.mouse.get_pos())
        screen.blit(s2, s2.get_rect(center=pos + (1, 1)))
        screen.blit(s1, s1.get_rect(center=pos))
        selected_rect = pygame.Rect(BOARD_POS[0] + selected_gate[1] * TILESIZE, BOARD_POS[1] + selected_gate[2] * TILESIZE, TILESIZE, TILESIZE)
        #pygame.draw.line(screen, pygame.Color('red'), selected_rect.center, pos)
        return (x, y)



def main():
    pygame.init()
    font = pygame.font.SysFont('', 32)
    screen = pygame.display.set_mode((2080, 1040))
    board = create_circuit()
    board_surf = create_board_surf()
    clock = pygame.time.Clock()
    selected_piece = None
    selected_gate = None
    drop_pos = None
    while True:
        piece, x, y = get_square_under_mouse(board)
        gate, x1, y1 = get_gate_under_mouse(board)
        curr_qubit,xq,yq = get_qubit_under_mouse(board)
        run = get_run_under_mouse(board)
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.MOUSEBUTTONDOWN:
                if gate != None:
                    selected_gate = gate, x1, y1
                if(curr_qubit!=None):
                    board[yq][xq]= 1-board[yq][xq]
                if(run):
                    print(board)
                
                
            if e.type == pygame.MOUSEBUTTONUP:
                if drop_pos:
                    gate, old_x, old_y = selected_gate      
                    new_x, new_y = drop_pos
                    board[new_y][new_x] = gate
                    if(gate=="C"):
                        controlled_bit = int(cx_question())
                        board[controlled_bit+2][new_x] = "X"
                        
                selected_piece = None
                selected_gate = None
                drop_pos = None

        screen.fill(pygame.Color('grey'))
        screen.blit(board_surf, BOARD_POS)
        draw_pieces(screen, board, font, selected_gate)
        draw_menu(screen,board,font, selected_gate)
        draw_selector(screen, gate, x, y)
        drop_pos = draw_drag(screen, board, selected_gate, font)

        pygame.display.flip()
        clock.tick(60)
    print(board)

if __name__ == '__main__':    
    main()
