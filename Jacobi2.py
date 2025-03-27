import numpy as np

def preparar_H_g(A, b):
    linha, coluna = A.shape
    H = np.zeros((linha, coluna))
    g = np.zeros(coluna)
    for i in range(linha):
        H[i, :] = -A[i, :] / A[i, i]
        H[i, i] = 0  # Zera a diagonal
        g[i] = b[i] / A[i, i]
    return H, g

def metodo_iterativo(A, b, x0, erro_tol=0.001, max_iter=100):
    H, g = preparar_H_g(A, b)
    x = np.array(x0, dtype='double')
    
    print("Iteração | Solução Aproximada                | Erro Relativo")
    print("-------------------------------------------------------------")
    
    for k in range(1, max_iter + 1):
        xk = np.dot(H, x) + g
        
        # Norma infinito para o erro relativo
        erro_abs = np.abs(xk - x).max()
        erro_rel = erro_abs / (np.abs(xk).max() + 1e-10)  # adiciona eps para evitar divisão por zero
        
        print(f"{k:^9} | {xk.round(6)} | {erro_rel:.6f}")
        
        if erro_rel < erro_tol:
            print("\nConvergência atingida.")
            return xk
        
        x = xk

    print("\nNúmero máximo de iterações atingido.")
    return xk

# ---------- PARTE PRINCIPAL ----------

A = np.array([[10, 2, 1],
              [1, 5, 1],
              [2, 3, 10]], dtype='double')

b = np.array([7, -8, 6], dtype='double')
x0 = [0, 0, 0]  # Chute inicial

solucao = metodo_iterativo(A, b, x0, erro_tol=0.001, max_iter=100)
print(f"\nSolução final: {solucao.round(6)}")
