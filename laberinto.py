import random
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import tkinter as tk

# Generamos dimensiones del laberinto
dimensiones_laberinto = random.randint(11, 23)

# Nos aseguramos de que sea impar
while dimensiones_laberinto % 2 == 0:
    dimensiones_laberinto = random.randint(11, 23)

print(f"El laberinto tiene dimensiones {dimensiones_laberinto} x {dimensiones_laberinto}")


def crear_entrada_salida():
    bordes = ["superior", "inferior", "derecha", "izquierda"]
    borde_entrada = random.choice(bordes)

    if borde_entrada == "superior":
        entrada = (1, random.randint(2, dimensiones_laberinto - 1))
    elif borde_entrada == "inferior":
        entrada = (dimensiones_laberinto, random.randint(2, dimensiones_laberinto - 1))
    elif borde_entrada == "derecha":
        entrada = (random.randint(2, dimensiones_laberinto - 1), dimensiones_laberinto)
    else:  # izquierda
        entrada = (random.randint(2, dimensiones_laberinto - 1), 1)

    borde_salida = random.choice(bordes)
    while borde_salida == borde_entrada:
        borde_salida = random.choice(bordes)

    if borde_salida == "superior":
        salida = (1, random.randint(2, dimensiones_laberinto - 1))
    elif borde_salida == "inferior":
        salida = (dimensiones_laberinto, random.randint(2, dimensiones_laberinto - 1))
    elif borde_salida == "derecha":
        salida = (random.randint(2, dimensiones_laberinto - 1), dimensiones_laberinto)
    else:  # izquierda
        salida = (random.randint(2, dimensiones_laberinto - 1), 1)

    return entrada, salida


def crear_laberinto():    
    laberinto = []
    for _ in range(dimensiones_laberinto):
        laberinto.append([])

    for fila in laberinto:
        for _ in range(dimensiones_laberinto):
            if random.randint(1, 4) == 1:
                fila.append(1)
            else:
                fila.append(0)

    for i in range(dimensiones_laberinto):
        laberinto[0][i] = 1
        laberinto[-1][i] = 1
        laberinto[i][0] = 1
        laberinto[i][-1] = 1

    return laberinto


def matriz_visitados(filas, columnas):
    visitado = []
    for _ in range(filas):
        fila = []
        for _ in range(columnas):
            fila.append(False)
        visitado.append(fila)
    return visitado


def encontrar_un_camino(laberinto, entrada, salida):
    filas = len(laberinto)
    columnas = len(laberinto[0])
    visitado = matriz_visitados(filas, columnas)
    camino = []

    def dfs(x, y):
        if x == (salida[0] - 1) and y == (salida[1] - 1):
            camino.append((x + 1, y + 1))
            return True
        
        visitado[x][y] = True
        camino.append((x + 1, y + 1))
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for (dx, dy) in movimientos:
            nx = x + dx
            ny = y + dy

            if (0 <= nx < filas) and (0 <= ny < columnas):
                if not visitado[nx][ny] and (laberinto[nx][ny] == 0 or laberinto[nx][ny] == 3):
                    if dfs(nx, ny):
                        return True
        
        camino.pop()
        return False

    x_inicio = entrada[0] - 1
    y_inicio = entrada[1] - 1

    if dfs(x_inicio, y_inicio):
        return camino
    else:
        return None


def visualizar_laberinto(canvas1, canvas2, laberinto, camino=None):
    size = 500 / dimensiones_laberinto
    for i, fila in enumerate(laberinto):
        for j, celda in enumerate(fila):
            color = "white" if celda == 0 else "black"
            if (i + 1, j + 1) == entrada:
                color = "green"
            if (i + 1, j + 1) == salida:
                color = "blue"
            canvas1.create_rectangle(j * size, i * size, (j + 1) * size, (i + 1) * size, fill=color, outline="gray")
            if camino and (i + 1, j + 1) in camino:
                color = "red"
            canvas2.create_rectangle(j * size, i * size, (j + 1) * size, (i + 1) * size, fill=color, outline="gray")

# GUI principal
root = tk.Tk()
root.title("Laberinto con Camino")
frame = tk.Frame(root)
frame.pack()

info_label = tk.Label(root, text="", justify='left', font=('Arial', 12))
info_label.pack()

canvas1 = tk.Canvas(frame, width=500, height=500, bg='white')
canvas1.pack(side='left')
canvas2 = tk.Canvas(frame, width=500, height=500, bg='white')
canvas2.pack(side='right')

def generar_y_mostrar():
    global laberinto, entrada, salida, camino
    camino = None
    while not camino:
        entrada, salida = crear_entrada_salida()
        laberinto = crear_laberinto()
        laberinto[entrada[0] - 1][entrada[1] - 1] = 2
        laberinto[salida[0] - 1][salida[1] - 1] = 3
        camino = encontrar_un_camino(laberinto, entrada, salida)
    visualizar_laberinto(canvas1, canvas2, laberinto, camino)
    info_label.config(text=f"Dimensiones: {dimensiones_laberinto}x{dimensiones_laberinto}\nEntrada: {entrada}\nSalida: {salida}")

generar_btn = tk.Button(root, text="Generar Laberinto", command=generar_y_mostrar)
generar_btn.pack()
root.mainloop()
