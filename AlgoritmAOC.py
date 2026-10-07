"""
Optimización por Colonia de Hormigas (ACO) aplicada al problema del viajante (TSP).
En cada iteración se imprime el mejor resultado de esa iteración
y el mejor global encontrado hasta el momento.

Presenta:Juan Ramon Rodríguez Armas
Profesor: Pablo Salazar
Materia: Algoritmos bioinspirados
Link del claude https://claude.ai/share/2f7b6bcc-2b7f-4de5-ba01-7101427234ec
"""
import math
import random
import matplotlib.pyplot as plt

# Parámetros del algoritmo
n_hormigas = 5
n_iteraciones = 100

alpha = 1       # Importancia de la feromona
beta = 2        # Importancia de la distancia
rho = 0.5       # Evaporación
Q = 100         # Cantidad de feromona

n_ciudades = 25
semilla = 42


# ---------------------------------------------------------------
# 1. Problema: ciudades y distancias
# ---------------------------------------------------------------
def crear_ciudades(n, semilla=42):
    random.seed(semilla)
    return [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]


def matriz_distancias(ciudades):
    n = len(ciudades)
    return [[math.dist(ciudades[i], ciudades[j]) for j in range(n)] for i in range(n)]


def longitud_ruta(ruta, dist):
    """Longitud total de un recorrido cerrado (vuelve a la ciudad inicial)."""
    n = len(ruta)
    return sum(dist[ruta[i]][ruta[(i + 1) % n]] for i in range(n))


# ---------------------------------------------------------------
# 2. Construcción de la ruta de una hormiga
# ---------------------------------------------------------------
def construir_ruta(dist, feromona):
    n = len(dist)
    inicio = random.randrange(n)
    ruta = [inicio]
    visitadas = {inicio}

    while len(ruta) < n:
        actual = ruta[-1]
        candidatas = [j for j in range(n) if j not in visitadas]

        # Probabilidad ∝ feromona^alpha * (1/distancia)^beta
        pesos = [
            (feromona[actual][j] ** alpha) * ((1.0 / dist[actual][j]) ** beta)
            for j in candidatas
        ]
        siguiente = random.choices(candidatas, weights=pesos, k=1)[0]

        ruta.append(siguiente)
        visitadas.add(siguiente)

    return ruta


# ---------------------------------------------------------------
# 3. Algoritmo principal ACO
# ---------------------------------------------------------------
def aco(dist):
    n = len(dist)
    feromona = [[1.0] * n for _ in range(n)]  # feromona inicial uniforme

    mejor_ruta_global = None
    mejor_long_global = float("inf")

    # Historiales para la gráfica (se crean ANTES del ciclo)
    historial_it = []        # mejor de cada iteración
    historial_global = []    # mejor global hasta ese momento

    for it in range(1, n_iteraciones + 1):
        # a) Cada hormiga construye una solución
        rutas = [construir_ruta(dist, feromona) for _ in range(n_hormigas)]
        longitudes = [longitud_ruta(r, dist) for r in rutas]

        # b) Mejor solución de ESTA iteración
        idx = min(range(n_hormigas), key=lambda i: longitudes[i])
        mejor_ruta_it, mejor_long_it = rutas[idx], longitudes[idx]

        # c) Actualizar el mejor global
        if mejor_long_it < mejor_long_global:
            mejor_long_global = mejor_long_it
            mejor_ruta_global = mejor_ruta_it[:]

        # d) Evaporación de feromona
        for i in range(n):
            for j in range(n):
                feromona[i][j] *= (1.0 - rho)

        # e) Depósito de feromona: mejores rutas dejan más rastro
        for ruta, largo in zip(rutas, longitudes):
            deposito = Q / largo
            for k in range(n):
                a, b = ruta[k], ruta[(k + 1) % n]
                feromona[a][b] += deposito
                feromona[b][a] += deposito  # problema simétrico

        # f) Guardar historial para graficar
        historial_it.append(mejor_long_it)
        historial_global.append(mejor_long_global)

        # g) Impresión en consola por iteración
        print(f"Iteración {it:3d} | Mejor de la iteración: {mejor_long_it:8.2f} "
              f"| Mejor global: {mejor_long_global:8.2f}")

    return mejor_ruta_global, mejor_long_global, historial_it, historial_global


# ---------------------------------------------------------------
# 4. Gráficas
# ---------------------------------------------------------------
def graficar(ciudades, ruta, historial_it, historial_global):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # --- Gráfica 1: camino encontrado ---
    ruta_cerrada = ruta + [ruta[0]]  # volver a la ciudad inicial
    xs = [ciudades[i][0] for i in ruta_cerrada]
    ys = [ciudades[i][1] for i in ruta_cerrada]
    ax1.plot(xs, ys, "-o", color="tab:blue", markersize=6)
    ax1.plot(xs[0], ys[0], "s", color="red", markersize=10, label="Inicio")
    for i, (x, y) in enumerate(ciudades):
        ax1.annotate(str(i), (x, y), textcoords="offset points", xytext=(5, 5), fontsize=8)
    ax1.set_title("Mejor camino encontrado")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.legend()

    # --- Gráfica 2: avance por iteración ---
    iteraciones = range(1, len(historial_it) + 1)
    ax2.plot(iteraciones, historial_it, color="tab:orange", alpha=0.6,
             label="Mejor de la iteración")
    ax2.plot(iteraciones, historial_global, color="tab:green", linewidth=2,
             label="Mejor global")
    ax2.set_title("Avance de las iteraciones")
    ax2.set_xlabel("Iteración")
    ax2.set_ylabel("Longitud de la ruta")
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    plt.tight_layout()
    plt.savefig("resultado_aco.png", dpi=150)
    plt.show()


# ---------------------------------------------------------------
# 5. Ejecución
# ---------------------------------------------------------------
if __name__ == "__main__":
    ciudades = crear_ciudades(n_ciudades, semilla)
    dist = matriz_distancias(ciudades)

    ruta, longitud, hist_it, hist_global = aco(dist)

    print("\n=== RESULTADO FINAL ===")
    print("Mejor ruta:", ruta)
    print(f"Longitud: {longitud:.2f}")

    graficar(ciudades, ruta, hist_it, hist_global)