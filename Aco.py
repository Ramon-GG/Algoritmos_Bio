import numpy as np

# Función que queremos minimizar
def funcion(x):
    return np.sum(x ** 2)


# Parámetros del algoritmo
n_hormigas = 20
n_iteraciones = 100
n_mejores = 5

limite_inferior = -10
limite_superior = 10


# Población inicial
# Cada hormiga tiene [x, y]

soluciones = np.random.uniform(
    limite_inferior,
    limite_superior,
    size=(n_hormigas, 2)
)

mejor_solucion = None
mejor_valor = float("inf")


# Iteraciones
for iteracion in range(n_iteraciones):

    # Evaluar soluciones
    valores = np.array([
        funcion(solucion)
        for solucion in soluciones
    ])

    # Ordenar de mejor a peor
    indices = np.argsort(valores)

    soluciones = soluciones[indices]
    valores = valores[indices]

    # Guardar la mejor solución global
    if valores[0] < mejor_valor:
        mejor_valor = valores[0]
        mejor_solucion = soluciones[0].copy()

    # Seleccionar las mejores soluciones
    mejores = soluciones[:n_mejores]

    # Generar nuevas soluciones
    # cerca de las mejores
    nuevas_soluciones = []

    for i in range(n_hormigas):

        # Elegir una de las mejores soluciones
        indice = np.random.randint(n_mejores)

        centro = mejores[indice]

        # Desviación para explorar alrededor
        desviacion = 1.0 * (1 - iteracion / n_iteraciones) + 0.01

        nueva = centro + np.random.normal(
            0,
            desviacion,
            size=2
        )

        # Mantener dentro de los límites
        nueva = np.clip(
            nueva,
            limite_inferior,
            limite_superior
        )

        nuevas_soluciones.append(nueva)

    soluciones = np.array(nuevas_soluciones)

print("Mejor solución:", mejor_solucion)
print("Valor de la función:", mejor_valor)