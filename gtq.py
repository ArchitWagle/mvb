import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
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
            #print("1")
            control_mat = np.kron(control_mat, np.mat([[1,0],[0,0]]))
            target_mat = np.kron(target_mat,np.mat([[0,0],[0,1]]))
        elif index == target_qubit:
            #print("2")
            control_mat = np.kron(control_mat, np.eye(2))
            target_mat = np.kron(target_mat, gates[qu_gate])
        else:
            #print("3")
            control_mat = np.kron(control_mat, np.eye(2))
            target_mat = np.kron(target_mat, np.eye(2))
        #print(control_mat)
        #print(target_mat)

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
    #print(target_mat.shape)0
    return(np.around(target_mat))

#print(init_toffoli_gate('Px', control_qubits=[1,2], target_qubit=3, num_qubits=3))

def circuit_run(board):
    #print(board)
    history = []
    for i in range(len(board)):
        history.append([0]*len(board[0]))
    qubits = np.mat([[1]])
    for i in range(len(board)):
        if(board[i][0]==0):
            qubits = np.kron(qubits,np.mat([[1],[0]]))
        else:
            qubits = np.kron(qubits,np.mat([[0],[1]]))
    
    for column in range(1,len(board[0])):
        transform = np.mat([[1]])
        for row in range(len(board)):
            cell = board[row][column]
            if(cell==None):
                transform = np.kron(transform,I_MAT)
            elif(cell[0]=="C"):
                control_qubit=row
                while(board[row][column]!='X'):
                     row+=1
                target_qubit= row
                transform = init_control_gate('Px', control_qubit+1, target_qubit+1, len(board))
                break
            elif(cell[0]=="T"):
                control_qubit_1=row
                row+=1
                while(board[row][column]!='X'):
                    if(board[row][column]=='T'):
                        control_qubit_2=row
                    row+=1
                target_qubit= row
                #print([control_qubit_1+1,control_qubit_2+1,target_qubit])
                transform = init_toffoli_gate('Px', [control_qubit_1+1,control_qubit_2+1], target_qubit+1, len(board))
                break
            else:
                transform = np.kron(transform, gates[cell])
        qubits = transform*qubits
        for j in range(len(board)):
            history[j][column] = qubits[j][0,0]
        
        #print("-----------",column)
        #if(i<10):
        #    print(transform,qubits)
    print(history)
    return(qubits)

def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)


root = 0
def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
    #print("quittingggg")
    
def mlp_plot(result_vec):
    global root
    print(result_vec)
    result_vec = [abs(x[0,0])**2 for x in result_vec]
    print(result_vec)
    N = len(result_vec)
    #ind = np.arange(len(result_vec))
    ind = [i for i in range(len(result_vec))]
    #print(result_vec,N,ind)
    width = 0.35
    
    root = tkinter.Tk()
    root.wm_title("Embedding in Tk")
            
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    rects1 = ax.bar(ind, result_vec, width)
    ax.set_xticks(ind)

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
    
