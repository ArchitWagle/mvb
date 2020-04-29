import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, pi, cos, sin
import cmath 

H_MAT = np.mat([[1/sqrt(2),1/sqrt(2)],[1/sqrt(2),-1/sqrt(2)]])
PX_MAT = np.mat([[0,1],[1,0]])
PY_MAT= np.mat([[0,-1j],[1j,0]])
PZ_MAT = np.mat([[1,0],[0,-1]])
I_MAT  = np.mat([[1,0],[0,1]])
T_MAT = np.mat([[1,0],[0,(1+1j)/sqrt(2)]])
T_MAT_H = T_MAT.getH()

gates = {'H':H_MAT, 'Px':PX_MAT, 'Py':PY_MAT, 'Pz':PZ_MAT, 'T_MAT':T_MAT, 'T_MAT_H':T_MAT_H}

def init_control_gate(qu_gate, control_qubit=1, target_qubit=2, num_qubits=2):
    index = 1
    control_mat = 1
    target_mat = 1
    while index <= num_qubits:
        if index == control_qubit:
            control_mat = np.kron(control_mat, np.mat([[1,0],[0,0]]))
            target_mat = np.kron(target_mat,np.mat([[0,0],[0,1]]))
        elif index == target_qubit:
            control_mat = np.kron(control_mat, np.eye(2))
            target_mat = np.kron(target_mat, gates[qu_gate])
        else:
            control_mat = np.kron(control_mat, np.eye(2))
            target_mat = np.kron(target_mat, np.eye(2))
        index += 1    
    control_gate = control_mat + target_mat
    return(control_gate)

def init_toffoli_gate(qu_gate, control_qubits=[1,2], target_qubit=3, num_qubits=3):
    index = 1
    c1,c2 = control_qubits
    t = target_qubit
    target_mat = init_control_gate('Px',c1,c2,num_qubits)
    #t#######################
    transform = 1
    for i in range(1,num_qubits+1):
        if(i==c1):
            transform = np.kron(transform,T_MAT)
        elif(i==c2):
            transform = np.kron(transform,T_MAT_H)
        else:
            transform = np.kron(transform,I_MAT)   


    target_mat = target_mat*transform
    ############################
    target_mat =  target_mat*init_control_gate('Px',c1,c2,num_qubits) 
    ###########################
    transform = 1
    for i in range(1,num_qubits+1):
        if(i==t):
            transform = np.kron(transform,H_MAT)
        else:
            transform = np.kron(transform,I_MAT)    
    target_mat = target_mat*transform
    ###########################
    transform = 1
    for i in range(1,num_qubits+1):
        if(i==t or i==c2):
            transform = np.kron(transform,T_MAT)
        else:
            transform = np.kron(transform,I_MAT)    
    target_mat = target_mat *transform
    
    ###########################
    target_mat =  target_mat*init_control_gate('Px',c1,t,num_qubits) 
    ###########################
    transform = 1
    for i in range(1,num_qubits+1):
        if(i==t):
            transform = np.kron(transform,T_MAT_H)
        else:
            transform = np.kron(transform,I_MAT)
    target_mat = target_mat*transform
    ###########################
    target_mat = target_mat*init_control_gate('Px',c2,t,num_qubits) 
    
    ###########################
    transform = 1
    for i in range(1,num_qubits+1):
        if(i==t):
            transform = np.kron(transform,T_MAT)
        else:
            transform = np.kron(transform,I_MAT)     
    target_mat = target_mat  * transform
    ###########################
    target_mat =  target_mat*init_control_gate('Px',c1,t,num_qubits)

    ###########################
    transform = 1
    for i in range(1,num_qubits+1):
        if(i==t):
            transform = np.kron(transform,T_MAT_H)
        else:
            transform = np.kron(transform,I_MAT)
    target_mat = target_mat*transform
    ###########################
    target_mat = target_mat *init_control_gate('Px',c2,t,num_qubits)    
    ##########################
    transform = 1
    for i in range(1,num_qubits+1):
        if(i==t):
            transform = np.kron(transform,H_MAT)
        else:
            transform = np.kron(transform,I_MAT)    
    target_mat = target_mat  *transform
    return(np.around(target_mat))

#print(init_toffoli_gate('Px', control_qubits=[1,2], target_qubit=3, num_qubits=3))


    
def print_TableForm(A):
    with np.printoptions(precision=4, suppress=True, formatter={'float': '{:0.4f}'.format}, linewidth=100):
        print(A)
    

def init_qft_gate(start, number, n):
    x = number
    number = 2**number
    w = complex(cos(2*pi/number), sin(2*pi/number))
    
    QFT_mat = [[1]*number for i in range(number)]
    for i in range(1,number):
        QFT_mat[i][1] = w**i
        for j in range(2,number):
            QFT_mat[i][j] = QFT_mat[i][j-1] * QFT_mat[i][1]
    #QFT_mat= np.around(QFT_mat)
    QFT_mat = np.mat(QFT_mat)
    #print_TableForm(QFT_mat)
    QFT_mat/=sqrt(number)
    ans = 1
    j = 0
    for i in range(start):
        ans = np.kron(ans,I_MAT)
        
    ans = np.kron(ans,QFT_mat)
        
    for i in range(start+x, n):
        ans = np.kron(ans,I_MAT)
    
    return np.mat(ans)
#print(init_qft_gate(0,3,3))


def circuit_run(board):
    #print(board)
    history = []
    print("board size", len(board))
    for i in range(len(board)):
        history.append([0]*len(board[0]))
    qubits = np.mat([[1]])
    for i in range(len(board)):
        if(board[i][0]==0):
            qubits = np.kron(qubits,np.mat([[1],[0]]))
        else:
            qubits = np.kron(qubits,np.mat([[0],[1]]))
    print("qubit size", len(qubits),len(board))
    transform=1
    transform_hist = np.eye(2**len(board))
    for column in range(1,len(board[0])):
        transform = np.mat([[1]])
        for row in range(len(board)):
            cell = board[row][column]
            if(cell==None or cell=="X"):
                transform = np.kron(transform,I_MAT)
            elif(cell[0]=="C"):
                control_qubit=row
                row1 = 0
                while(board[row1][column]!='X'):
                     row1+=1
                target_qubit= row1
                transform = init_control_gate('Px', control_qubit+1, target_qubit+1, len(board))
                break
            elif(cell[0]=="Q" and cell[3]=="i"):
                transform = np.linalg.inv(init_qft_gate(row, int(cell[4::]), len(board)))
                break
            elif(cell[0]=="Q"):    
                transform = init_qft_gate(row, int(cell[3::]), len(board))
                break
            elif(cell[0]=="T"):
                control_qubit_1=row
                row+=1
                while(board[row][column]!='X'):
                    if(board[row][column]=='T'):
                        control_qubit_2=row
                    row+=1
                target_qubit= row
                transform = init_toffoli_gate('Px', [control_qubit_1+1,control_qubit_2+1], target_qubit+1, len(board))
                break
            else:
                transform = np.kron(transform, gates[cell])
        qubits = transform*qubits
        transform_hist = transform*transform_hist
        for j in range(len(board)):
            history[j][column] = qubits[j][0,0]
        print("qubit size", len(qubits))
    print_TableForm(transform_hist)
    #print(history)
    return(qubits)

def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)


root = 0
def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
    #print("quittingggg")
    
def mlp_plot(n,result_vec):
    format(10, '016b')
    print("final length", len(result_vec))
    global root
    print(result_vec)
    N = len(result_vec)
    temp = result_vec
    print("final length", len(result_vec))
    ind = [i for i in range(len(result_vec))]
    bin_i = [int(format(i, '016b')[-n:][::-1],2) for i in ind]
    print(bin_i,[format(i, '016b')[-n:][::-1] for i in ind])
    print("final length", len(temp))
    #result_vec = [temp[i] for i in bin_i ]
    
    
    result_vec = [abs(x[0,0])**2 for x in result_vec]
    print("final length", len(result_vec))
    #print(result_vec)
    N = len(result_vec)
    #ind = np.arange(len(result_vec))
    
    #print(result_vec,N,ind)
    width = 0.35
    
    root = tkinter.Tk()
    root.wm_title("Embedding in Tk")
            
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    print("final length", len(result_vec))
    labels_bin = ['|'+format(i,'016b')[-n:]+'>' for i in ind]
    rects1 = ax.bar([format(i,'016b')[-n:] for i in ind], result_vec, width)
    #ax.set_xticks(ind,[format(i,'016b')[-n:] for i in ind])

    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    
    canvas.mpl_connect("key_press_event", on_key_press)
    print("1")
    #button.pack(side=tkinter.BOTTOM)
    button = tkinter.Button(master=root, text="Quit", command=_quit)
    button.pack(side=tkinter.BOTTOM)
    tkinter.mainloop()
    print("1")
    
