#Falta corregir el metodo de mutacion y que se ejecute varias veces (ademas de hacer mas legible el codigo)

import random
import matplotlib.pyplot as plt
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)


#Funcion que transforma binario a decimal
def bin_to_dec(cromosoma):
    dec = 0
    for i in range(len(cromosoma)):
        dec += cromosoma[i]*2**(len(cromosoma)-1-i) 
    return dec

#Funcion que crea la poblacion inicial en base a la cantidad de poblacion inicial y cant_genes
def crear_poblacion(cant_poblacion, cant_genes):
    for _ in range(cant_poblacion):
        cromosoma = [random.randint(0, 1) for i in range(cant_genes)]
        poblacion.append(cromosoma)
    return poblacion

#Funcion que elige un cromosoma en base a su probabilidad (fitness)
def ruleta(fitness, poblacion):
    randomNum = random.random()
    acum = 0
    indiceCromosoma = 0
    for i in range(len(fitness)):
        if randomNum > acum and randomNum < (acum + fitness[i]):
            indiceCromosoma = i
            break  
        acum += fitness[i]
    return poblacion[indiceCromosoma]

def crossover (padre1, padre2):
    num = random.randrange(0,100)
    if num > (probabilidad_crossover*100):
        hijo1 = padre1
        hijo2 = padre2
    else:
        punto_corte = random.randint(1,cant_genes-1)
        hijo1 = padre1[:punto_corte] + padre2[punto_corte:]
        hijo2 = padre2[:punto_corte] + padre1[punto_corte:]
    #     print(f"punto de corte {punto_corte}")
    # print(f"numero aleatorio {num} y probalidad_crossover {probabilidad_crossover*100}" )
    return hijo1, hijo2

def mutacion (hijo): #No se si los punto donde se hace la mutacion son correctos para el caso que el punto1 sea igual al comienzo (posicion 0) y punto2 sea igual al final (posicion 5)
    num = random.randrange(0,100)
    # print(f"numero aleatorio {num} y probabilidad_mutacion {probabilidad_mutacion*100}" )
    if num < (probabilidad_mutacion*100):
        # punto_mutacion = random.randint(0,cant_genes-1)
        # hijo[punto_mutacion] = 1 - hijo[punto_mutacion]
        punto1 = random.randint(0,cant_genes-1)
        punto2 = random.randint(0,cant_genes-1)
        #si los puntos son iguales o consecutivos se vuelve a buscar, ya que sino el cromosoma queda igual
        while punto1 == punto2 or abs(punto1 - punto2) == 1:
            punto1 = random.randint(0, len(hijo) - 1)
            punto2 = random.randint(0, len(hijo) - 1)
        print(f"punto1 {punto1} y punto2 {punto2}")
        if punto1 > punto2:
            punto1, punto2 = punto2, punto1
            # print(f"hijo sin modificar {hijo} para cuando punto1 > punto2 se invierte el valor de cada uno")
        hijo = hijo[:punto1] + hijo[punto1:punto2][::-1] + hijo[punto2:]
        # print(f"hijo {hijo} para cuando punto1 < punto2")
    return hijo

def fitness(poblacion):
    global maxCromosoma
    global datos_poblacionales
    global datos_valores
    valores_funcion = []
    valores = []
    #Obtengo el cromosoma con mayor valor de la poblacion
    if maxCromosoma < max(poblacion):
        maxCromosoma = max(poblacion)
    #Guardo los valores de los cromosomas en decimal y en funcion de la poblacion
    for cromosoma in poblacion:
        valores.append(bin_to_dec(cromosoma))
        valores_funcion.append((bin_to_dec(cromosoma)/(2**30-1))**2)
    print("valores decimales antes de aplicar la funcion:")
    print(valores)
    print("valores despues de aplicar la funcion:")
    print(valores_funcion)
    
    #Guardo los valores maximos, minimos y promedios de la poblacion
    datos_poblacionales.append([max(valores),min(valores),int(sum(valores)/len(valores)),max(poblacion)])
    datos_valores.append([max(valores_funcion),min(valores_funcion),sum(valores_funcion)/len(valores_funcion)])
    print(f"la cantidad de poblacion es: {cant_poblacion}")

    #Calcula el fitness de cada una de los cromosomas
    for i in range(cant_poblacion):
        fitnessPoblacion.append(valores_funcion[i]/sum(valores_funcion))
        # print(f"Fitness del cromosoma {i}: {fitnessPoblacion[i]}")
    return fitnessPoblacion

#Funcion que genera una nueva poblacion en base a la ruleta y sin elitismo
def generar_nueva_poblacion_ruleta_sin_elitismo(poblacion, fitnessPoblacion):
    global cant_poblacion
    poblacion2= []
    for i in range((cant_poblacion//2) ): 
        padre1 = ruleta(fitnessPoblacion,poblacion)
        padre2 = ruleta(fitnessPoblacion,poblacion)
        hijo1, hijo2 = crossover(padre1, padre2)
        hijo1 = mutacion(hijo1)
        hijo2 = mutacion(hijo2)
        poblacion2.append(hijo1)
        poblacion2.append(hijo2)
        # print("padres:")
        # print(padre1)
        # print(padre2)
        # print("hijos:")
        # print(hijo1)
        # print(hijo2)
    return poblacion2
    
#VARIABLE INICIALES
cant_poblacion = 10 
cant_genes = len(bin(2**30-1))-2 #-2 para quitarle el 0b al principio
probabilidad_crossover = 0.75
probabilidad_mutacion = 0.05
maxiteraciones = 200

poblacion = []
cromosoma = []

datos_valores = []
datos_poblacionales = []
maxCromosoma = []

#Creacion de la poblacion
crear_poblacion(cant_poblacion, cant_genes)
print("poblacion inicial:")
print(poblacion)

#iteraciones
for iteraciones in range(maxiteraciones):
    fitnessPoblacion = []
    
    print("-------------------------------------------------------------------------------------------------")
    # print("poblacion inicial:")
    # print(poblacion)
    fitnessPoblacion = fitness(poblacion)
    #elitismo
    #seleccionar los dos mejores cromosomas y pasarlos a la siguiente generacion
    #Considero como mejor cromosoma a los 2 de mayor valor y modifico el rango par que se reste 1 repeticion y haya solo 4 cromosomas

    poblacion = generar_nueva_poblacion_ruleta_sin_elitismo(poblacion, fitnessPoblacion)
    # print("resultado final:")
    # print(poblacion)

# print("-------------------------------------------------------------------------------------------------")
# print("poblacion final:")
# for i in range(cant_poblacion):
#     print(poblacion[i])
print("cromosoma con valor maximo:")
print(maxCromosoma)
print(bin_to_dec(maxCromosoma))

# Crear un DataFrame(tabla) con los datos de la población
Columnas = ['Maximos', 'Minimos', 'Promedios','cromosoma del maximo']
df = pd.DataFrame(datos_poblacionales, columns=Columnas,index=list(range(1,maxiteraciones+1)))
print(df)

# Crear los graficos de los datos
ejex= list(range(maxiteraciones))
valores_maximos = [val[0] for val in datos_valores]
valores_minimos = [val[1] for val in datos_valores]
valores_promedios = [val[2] for val in datos_valores]
# Grafica de la funcion objetivo para 200 interaciones
plt.figure(1)
plt.plot(ejex, valores_maximos,label='valores maximos')
plt.plot(ejex, valores_minimos,label='valores minimos')
plt.plot(ejex, valores_promedios,label='valores promedios')
plt.title('Valores maximo, minimo y prom de la funcion en cada iteracion')
plt.legend()
plt.show()

