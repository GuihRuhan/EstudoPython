#Entradas

import numpy as np
A = np.array([[10,2,1],
             [1,5,1],
             [2,3,10]
             ], dtype='double')
b = np.array([[7], [-8],[6]], dtype='double')

x = [0,0,0]
erro = 0.001
niter= 100

linha, coluna = A.shape
H = np.zeros((linha,coluna))
g = np.zeros(coluna)

for i in list(range(0,linha,1)):
    H[i,:]=-A[i,:]/A[i,i]
    g[i]=b[i]/A[i,i]
    H[i,i]=0
    
#Processo interativo
k= 0
e= 1
while e>erro and k<niter:
    xk = np.dot(H,x)+g
    dif = xk - x
    maxd = max(min(dif), max(dif), key=abs)
    maxxk = max(min(xk), max(xk), key=abs)
    e= abs(maxd)/abs(maxxk)
    k = k+1
    x = xk
    print(xk)
    print(k)
    print(e)