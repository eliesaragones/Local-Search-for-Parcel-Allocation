from typing import Generator

from aima.search import Problem

from azamon_operators import AzamonOperator
from azamon_state import StateRepresentation
from aima . search import hill_climbing, simulated_annealing, exp_schedule
from random import *
from cmath import log
from typing import List, Set, Generator
from azamon_problem import Azamon
from azamon_operators import AzamonOperator, MoveParcel, SwapParcels
from azamon_problem_parameters import ProblemParameters
from azamon_state import StateRepresentation, generate_initial_state
from abia_azamon import *
from timeit import default_timer as timer
import timeit
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from numpy import mean
import statistics


if __name__ == '__main__':
    print('Benvingut a l\'experimentació')
    print('1 - Primer experiment (elecció d\'operadors)')
    print('2 - Segon experiment (elecció de generador de solucions inicials)')
    print('3 - Tercer experiment (elecció de paràmetres de Simulated Anealing)')
    print('4 - Quart experiment (Temps d\'execució en funció de paràmetres)')
    print('6 - Sisè experiment (happiness amb HC)')
    print('7 - Setè experiment (happiness amb SA)')
    print('8 - Vuitè experiment (personalitzat)')
    
    exp = int(input('Si us plau, introdueixi el número associat a l\'experiment desitjat: '))
    print('====================================================================================')

#==============================================================================================================================
#===================================================== EXPERIMENT 1 ===========================================================
#==============================================================================================================================

    if exp == 1:
        print('1 - Temps d\'execució')
        print('2 - Pasos')
        print('3 - Cost final')
        print('4 - Taula de l\'operador/operadors')
        grafics = (input('Si us plau, introdueixi quins gràfics voldrà desar (separats per espais): '))
        graf = list(map(int, grafics.split()))
        print('====================================================================================')
        if 4 in graf:
            print('1 - Move')
            print('2 - Swap')
            print('3 - Swap múltiple')
            print('Per fer combinacions escriure junt i de forma creixent (ex. Move i swap = 12)')
            input_operadors = (input('Si us plau, introdueixi de quins operadors voldrà desar la taula (separats per espais): '))
            llista_operadors = list(map(int, input_operadors.split()))
            print('====================================================================================')
        
        npaq = 50
        sol = 1
        heuristic = 1
        semillas = [1234,5678,1357,2468,1122,3344,5566,7788,9910,7777]
        temps = [[] for _ in range(10)]
        res = [[],[],[],[],[],[],[]]
        operadors = [1,2,3,12,13,23,123]
        for op in range(len(operadors)):
            for seed in semillas:
                paquetes = random_paquetes(npaq, seed)
                ofertas = random_ofertas(paquetes, 1.2, seed)
                experiment = 1
                problema = ProblemParameters(ofertas,paquetes,experiment,operadors[op],heuristic)
                
                start1 = timer()
                estado_inicial = generate_initial_state(problema, sol)
                end1 = timer()
                temps_ini = round((end1-start1)*1000,2)

                cont = 0
                cst = 0
                t = 0
                fel = 0
                heur = []

                for i in range(10):
                
                    start2 = timer()
                    n = hill_climbing ( Azamon( estado_inicial ) )
                    end2 = timer()
                    
                    cont += n.params.contador/10
                    cst += n.calcular_cost()/10
                    fel += n.happiness()/10
                    t += (end2-start2)*1000/10 #Dividim entre 10 i multipliquem per 1000 per tenir ms
                    n.params.contador = 0
                    
                
                res[op].append([seed, temps_ini, round(cont,2),round(estado_inicial.calcular_cost(),2),round(cst,2),round(estado_inicial.calcular_cost()-cst,2),round(fel,2),round(t,2)])
                
        dic = {valor: i for i, valor in enumerate(operadors)}
        if 4 in graf:
            for index in dic:
                if index in llista_operadors:
                    column_labels = ["Seed", "T. assig (ms)", "Pasos", "Cost inicial (€)", "Cost (€)", "Diferencia (€)" ,"Felicitat", "Temps (ms)"]

                    fig, ax = plt.subplots()

                    ax.axis("tight")
                    ax.axis("off")

                    table = ax.table(cellText=res[dic[index]], colLabels=column_labels, cellLoc="center", loc="center")

                    table.scale(1.23, 1.3)  
                    table.auto_set_font_size(False)
                    table.set_fontsize(7)

                    plt.title(f"Taula {index}")
                  
                    plt.savefig(f"taula{index}.png")

        if 1 in graf or 2 in graf or 3 in graf:
            pasos = [[] for _ in range(7)]
            cost = [[] for _ in range(7)]
            temps = [[] for _ in range(7)]

            for i in range(len(operadors)):
                pasos[i] = [fila[2] for fila in res[i]]
                cost[i] = [fila[4] for fila in res[i]]
                temps[i] = [fila[7] for fila in res[i]]

            if 1 in graf:
                fig, ax = plt.subplots()
                for i in range(len(operadors)):
                    ax.plot(temps[i], label=operadors[i], marker='o') 
                ax.set_xlabel("Valors de les seeds")
                ax.set_ylabel("Valors")
                plt.title('Temps')
            
                ax.legend(loc='upper right', framealpha=0.6)
                plt.tight_layout()
                plt.savefig(f"temps{operadors[i]}.png")
            
            if 2 in graf:
                fig, ax = plt.subplots()
                for i in range(len(operadors)):
                    ax.plot(pasos[i], label=operadors[i], marker='o')  
                ax.set_xlabel("Valors de les seeds")
                ax.set_ylabel("Valors")
                plt.title('Pasos')
                
                ax.legend(loc='upper right', framealpha=0.6)
                plt.tight_layout()
                plt.savefig(f"pasos{operadors[i]}.png")
                   
            if 3 in graf:
                fig, ax = plt.subplots()
                for i in range(len(operadors)):
                    ax.plot(cost[i], label=operadors[i], marker='o')
                ax.set_xlabel("Valors de les seeds")
                ax.set_ylabel("Valors")
                plt.title('Costos')

                ax.legend(loc='upper right', framealpha=0.6)
                plt.tight_layout()  
                plt.savefig(f"cost{operadors[i]}.png")

#==============================================================================================================================
#===================================================== EXPERIMENT 2 ===========================================================
#==============================================================================================================================
        
    if exp == 2:
        print('1 - Comparació valors de les heurístiques per cada seed')
        print('2 - Comparació dels temps de generació de la solució inicial i execució')
        print('3 - Taula')
        inp = input('Si us plau, introdueixi quins gràfics voldràs obtenir (separats per espais): ')
        print('====================================================================================')
        grafics = list(map(int, inp.split()))
        print(grafics)
        op = 1
        npaq = 50
        heuristic = 1
        semillas = [1234,5678,1357,2468,1122]
        temps_ini = [[],[]]
        temps_ex = [[],[]]
        experiment = 1
        
        for seed in semillas:
            lst = [[],[]]
            paquetes = random_paquetes(npaq, seed)
            ofertas = random_ofertas(paquetes, 1.2, seed)
            experiment = 1
            problema = ProblemParameters(ofertas,paquetes,experiment,op, heuristic)
            
           
            start1 = timer()
            estado_inicial1 = generate_initial_state(problema, 0)
            end1 = timer()
            cost_ini1 = estado_inicial1.calcular_cost()

            start2 = timer()
            estado_inicial2 = generate_initial_state(problema, 1)
            end2 = timer()
            cost_ini2 = estado_inicial2.calcular_cost()

            temps_ini[0].append(round((end1-start1)*1000,2))
            temps_ini[1].append(round((end2-start2)*1000,2))

            start3 = timer()
            n = hill_climbing(Azamon(estado_inicial1))
            end3 = timer()
            lst1 = n.params.heuristiques
            n.params.heuristiques = []
            cost1 = n.calcular_cost()
            temps_ex[0].append(round((end3-start3)*1000,2))

            start4 = timer()
            m = hill_climbing(Azamon(estado_inicial2))
            end4 = timer()
            temps_ex[1].append(round((end4-start4)*1000,2))  
            cost2 = m.calcular_cost()
            
            lst2 = m.params.heuristiques
            m.params.heuristiques = []
            
            if 1 in grafics:
                x_values1 = range(len(lst1))  
                x_values2 = range(len(lst2))  
                plt.plot(x_values1, lst1, label="Generació 1", marker='x')
                plt.plot(x_values2, lst2, label="Generació 2", marker='x')                    
                plt.xlabel("iteracions")
                plt.ylabel("Heurística")
                plt.legend()
                plt.savefig(f"{seed}.png")
                plt.clf()

        if 2 in grafics:
            print(temps_ini)
            print(temps_ex)
            plt.plot(range(len(temps_ini[0])), temps_ini[0], label="Generació 1", marker='x')
            plt.plot(range(len(temps_ini[1])), temps_ini[1], label="Generació 2", marker='x')                    
            plt.xlabel("Seeds")
            plt.ylabel("Temps d'execució (ms)")
            plt.legend(loc='upper right')
            plt.savefig(f"Temps ini.png")
            plt.clf()

            plt.plot(range(len(temps_ex[0])), temps_ex[0], label="Generació 1", marker='x')
            plt.plot(range(len(temps_ex[1])), temps_ex[1], label="Generació 2", marker='x')                    
            plt.xlabel("Seeds")
            plt.ylabel("Temps d'execució (ms)")
            plt.legend(loc='upper right')
            plt.savefig(f"Temps exec.png")
            plt.clf()
        
        if 3 in grafics:

            sol1 = ['Primer', round(mean(temps_ini[0]),2), round(mean(temps_ex[0]),2), round(cost_ini1,2), round(cost1,2), round(cost_ini1-cost1,2)]
            sol2 = ['Segon',round(mean(temps_ini[1]),2), round(mean(temps_ex[1]),2), round(cost_ini2,2), round(cost2,2), round(cost_ini2-cost2,2)]
            res = [sol1,sol2]
            
            column_labels = ["Generador solució","Mitjana t. ini.", "Mitjana t. ex.", "Cost ini. (€)", "Cost final (€)", "Diferència (€)"]
            fig, ax = plt.subplots()

            ax.axis("tight")
            ax.axis("off")

            table = ax.table(cellText=res, colLabels=column_labels, cellLoc="center", loc="center")

            table.scale(1.23, 1.3)  
            table.auto_set_font_size(True)
            plt.savefig('Taula')

#==============================================================================================================================
#===================================================== EXPERIMENT 3 ===========================================================
#==============================================================================================================================

    if exp == 3:
        K_values = [1, 5, 25, 125]
        lambda_values = [0.001, 0.01, 1]
        valores = []
        valores2 = []

        for i in range(4):
            print()
            print('-----------Iteración ',i+1,'semilla 1234-------------')
            print()
            experiment = 2 #SA
            operador = 1 #Move
            heuristica = 1 #cost
            for K in K_values:
                fila = []
                for lambda_param in lambda_values:                  
                    paquetes = random_paquetes(50, 1234)
                    ofertas = random_ofertas(paquetes, 1.2, 1234)
                    problema = ProblemParameters(ofertas, paquetes, experiment, operador, heuristica) 
                    estado_inicial = generate_initial_state(problema, 1)
                    coste_inicial= estado_inicial.calcular_cost()
                    
                    start = timer()
                    resultado = simulated_annealing(Azamon(estado_inicial), schedule=exp_schedule(K, lambda_param, limit=100000))
                    end = timer()
                    coste=resultado.calcular_cost()
                    
                    print('K:', K,', Lambda:',lambda_param,', Coste:',round(coste,2),', Temps:',round((end-start),2))
                
                    fila.append(coste) 
                valores.append(fila)

        for i in range(4):
            print()
            print('-----------Iteración ',i+1,'semilla 5678-------------')
            print()
            for K in K_values:
                fila2 = []
                for lambda_param in lambda_values:
                    
                    paquetes = random_paquetes(50, 5678)
                    ofertas = random_ofertas(paquetes, 1.2, 5678)
                    problema =  ProblemParameters(ofertas, paquetes, experiment, operador, heuristica) 
                    estado_inicial = generate_initial_state(problema, 1)
                    coste_inicial= estado_inicial.calcular_cost()
                    
                    start = timer()
                    resultado = simulated_annealing(Azamon(estado_inicial), schedule=exp_schedule(K, lambda_param, limit=100000))
                    end = timer()
                    coste=resultado.calcular_cost()
                    
                    print('K:', K,', Lambda:',lambda_param,', Coste:',round(coste,2),', Temps:',round((end-start),2))
                    fila2.append(coste)  

#==============================================================================================================================
#===================================================== EXPERIMENT 4 ===========================================================
#==============================================================================================================================

    if exp == 4:
        npaq = [50 + 10 * i for i in range(10)]
        sol = 1
        semillas = [1234, 5678, 1357, 2468, 1122, 3344, 5566, 7788, 9910, 7777]
        factor = 1.2 
        resultados_por_npaq = []

        for paq in npaq:
            res = []

            for seed in semillas:
                paquetes = random_paquetes(paq, seed)
                ofertas = random_ofertas(paquetes, factor, seed)
                experiment = 1 #HC
                operador = 1 #Move
                heuristica = 1 #Cost
                problema = ProblemParameters(ofertas, paquetes, experiment, operador, heuristica) 

                start1 = timer()
                estado_inicial = generate_initial_state(problema, sol)
                end1 = timer()
                temps_ini = round((end1 - start1) * 1000, 2)

                conts, costs, felicidades, tiempos, pasos = [], [], [], [], []

                for _ in range(10):
                    start2 = timer()
                    n = hill_climbing(Azamon(estado_inicial))
                    end2 = timer()

                    conts.append(n.params.contador)
                    costs.append(n.calcular_cost())
                    felicidades.append(n.happiness())
                    tiempos.append((end2 - start2) * 100)
                    pasos.append(n.params.contador)  

                    n.params.contador = 0
                    

                #Mitjanes
                cont = round(statistics.mean(conts), 2)
                cst = round(statistics.mean(costs), 2)
                fel = round(statistics.mean(felicidades), 2)
                t = round(statistics.mean(tiempos), 2)
                avg_pasos = round(statistics.mean(pasos), 2)  # Promedio de pasos
                print("Realizado experimento con ", paq, " paquetes en la semilla: ", seed)
                res.append([seed, temps_ini, avg_pasos, round(estado_inicial.calcular_cost(), 2), cst, round(estado_inicial.calcular_cost() - cst, 2), fel, t])

            resultados_por_npaq.append((paq, res))

        promedios = []
        for n_paq, res in resultados_por_npaq:
            promedio_cost_inicial = statistics.mean([fila[3] for fila in res])
            promedio_cost = statistics.mean([fila[4] for fila in res])
            promedio_pasos = statistics.mean([fila[2] for fila in res]) 
            promedio_temps = statistics.mean([fila[7] for fila in res])
            promedios.append([n_paq, promedio_cost_inicial, promedio_cost, promedio_pasos, promedio_temps])

        num_paquetes = [fila[0] for fila in promedios]
        cost_iniciales = [fila[1] for fila in promedios]
        costs = [fila[2] for fila in promedios]
        pasos = [fila[3] for fila in promedios]  
        tiempos = [fila[4] for fila in promedios]

        fig, ax = plt.subplots()
        ax.plot(num_paquetes, cost_iniciales, label="Cost inicial (€)", marker='o')
        ax.plot(num_paquetes, costs, label="Cost (€)", marker='o')
        ax.plot(num_paquetes, pasos, label="Pasos", marker='o')  
        ax.plot(num_paquetes, tiempos, label="Temps (ms)", marker='o')

        ax.set_title("Impacto del número de paquetes en los resultados")
        ax.set_xlabel("Número de paquetes")
        ax.set_ylabel("Valores promedio")
        ax.legend()

        plt.savefig("Exp4paquets.png")

        npaq = 50
        semillas = [1234, 5678, 1357, 2468, 1122, 3344, 5566, 7788, 9910, 7777]
        factores = [1.2 + 0.2 * i for i in range(10)]
        resultados_por_factor = []

        for factor in factores:
            res = []

            for seed in semillas:
                paquetes = random_paquetes(npaq, seed)
                ofertas = random_ofertas(paquetes, factor, seed)
                experiment = 1 #HC
                operador = 1 #Move
                heuristica = 1 #Cost
                problema = ProblemParameters(ofertas, paquetes, experiment, operador, heuristica)

                start1 = timer()
                estado_inicial = generate_initial_state(problema, sol)
                end1 = timer()
                temps_ini = round((end1 - start1) * 1000, 2)

                conts, costs, pasos, tiempos = [], [], [], []

                for _ in range(10):
                    start2 = timer()
                    n = hill_climbing(Azamon(estado_inicial))
                    end2 = timer()

                    conts.append(n.params.contador)
                    costs.append(n.calcular_cost())
                    tiempos.append((end2 - start2) * 100)
                    pasos.append(n.params.contador)  

                    n.params.contador = 0

                cont = round(statistics.mean(conts), 2)
                cst = round(statistics.mean(costs), 2)
                t = round(statistics.mean(tiempos), 2)
                avg_pasos = round(statistics.mean(pasos), 2) 
                print("Realizado experimento con factor ", factor, " en la semilla: ", seed)
                res.append([seed, temps_ini, avg_pasos, round(estado_inicial.calcular_cost(), 2), cst, round(estado_inicial.calcular_cost() - cst, 2), t])

            resultados_por_factor.append((factor, res))

        promedios = []
        for factor, res in resultados_por_factor:
            promedio_cost_inicial = statistics.mean([fila[3] for fila in res])
            promedio_cost = statistics.mean([fila[4] for fila in res])
            promedio_pasos = statistics.mean([fila[5] for fila in res])
            promedio_temps = statistics.mean([fila[6] for fila in res])
            promedios.append([factor, promedio_cost_inicial, promedio_cost, promedio_pasos, promedio_temps])

        factors = [fila[0] for fila in promedios]
        cost_iniciales = [fila[1] for fila in promedios]
        costs = [fila[2] for fila in promedios]
        pasos = [fila[3] for fila in promedios]
        tiempos = [fila[4] for fila in promedios]

        fig, ax = plt.subplots()
        ax.plot(factors, cost_iniciales, label="Cost inicial (€)", marker='o')
        ax.plot(factors, costs, label="Cost (€)", marker='o')
        ax.plot(factors, pasos, label="Pasos", marker='o')
        ax.plot(factors, tiempos, label="Temps (ms)", marker='o')

        for i, factor in enumerate(factors):
            ax.text(factor, cost_iniciales[i], f"{cost_iniciales[i]}", ha='center', va='bottom')
            ax.text(factor, costs[i], f"{costs[i]}", ha='center', va='bottom')
            ax.text(factor, pasos[i], f"{pasos[i]}", ha='center', va='bottom')
            ax.text(factor, tiempos[i], f"{tiempos[i]}", ha='center', va='bottom')

        ax.set_title("Impacto de incrementar el factor en los resultados")
        ax.set_xlabel("Factor de oferta")
        ax.set_ylabel("Valores promedio")
        ax.legend()

        plt.savefig("Exp4factorpes.png")

#==============================================================================================================================
#===================================================== EXPERIMENT 6 ===========================================================
#==============================================================================================================================

    if exp == 6:
        npaq = 50
        sol = 1
        semillas = [1234, 5678, 1357, 2468, 1122]
        pesos_happiness = [0 + (1 * i) for i in range(11)] #diferències de 1, solució final després de fer la prova amb 0.5
        factor = 1.2
        resultados_por_happiness = []
        operador = 1
        heuristica = 2

        for peso in pesos_happiness:
            res = []
            for seed in semillas:
                paquetes = random_paquetes(npaq, seed)
                ofertas = random_ofertas(paquetes, factor, seed)
                experiment = 1 #HC
                problema = ProblemParameters(ofertas, paquetes, experiment, operador, heuristica)
                problema.peso_happiness = peso
            
                start1 = timer()
                estado_inicial = generate_initial_state(problema, sol)
                end1 = timer()
                temps_ini = round((end1 - start1) * 1000, 2)

                conts, costs, felicidades, tiempos, pasos = [], [], [], [], []

                for _ in range(10):
                    start2 = timer()
                    n = hill_climbing(Azamon(estado_inicial))
                    end2 = timer()

                    conts.append(n.params.contador)
                    costs.append(n.calcular_cost())
                    felicidades.append(n.happiness())
                    tiempos.append((end2 - start2))
                    pasos.append(n.params.contador)  

                    n.params.contador = 0
                    
                #Mitjanes
                cont = round(statistics.mean(conts), 2)
                cst = round(statistics.mean(costs), 2)
                fel = round(statistics.mean(felicidades), 2)
                t = round(statistics.mean(tiempos), 2)
                avg_pasos = round(statistics.mean(pasos), 2)  
                print(f"Realizado experimento con peso happiness: {peso} en la semilla: {seed}")
                res.append([peso, temps_ini, avg_pasos, round(estado_inicial.calcular_cost(), 2), cst, round(estado_inicial.calcular_cost() - cst, 2), fel, t])

            resultados_por_happiness.append((peso, res))

        promedios = []
        for pesos_happiness, res in resultados_por_happiness:
            promedio_cost_inicial = statistics.mean([fila[3] for fila in res])
            promedio_cost = statistics.mean([fila[4] for fila in res])
            promedio_diferencia = statistics.mean([fila[5] for fila in res])
            promedio_felicitat = statistics.mean([fila[6] for fila in res])
            promedio_temps = statistics.mean([fila[7] for fila in res])
            promedios.append([pesos_happiness, promedio_cost_inicial, promedio_cost, promedio_diferencia, promedio_felicitat, promedio_temps])

        pesos = [fila[0] for fila in promedios]
        cost_iniciales = [fila[1] for fila in promedios]
        costs = [fila[2] for fila in promedios]
        diferencias = [fila[3] for fila in promedios]
        felicidades = [fila[4] for fila in promedios]
        tiempos = [fila[5] for fila in promedios]

        fig, ax = plt.subplots(figsize=(12, 7))

        ax.plot(pesos, diferencias, label="Diferencia (€)", marker='^', linestyle='-.', color='darkblue', markersize=8, linewidth=2)
        ax.plot(pesos, felicidades, label="Felicitat", marker='o', linestyle='--', color='darkorange', markersize=8, linewidth=2)

        for i, (peso, dif, fel) in enumerate(zip(pesos, diferencias, felicidades)):
            ax.text(peso, dif, f"{dif:.1f}", ha='right', color='darkblue', fontsize=9)
            ax.text(peso, fel, f"{fel:.1f}", ha='left', color='darkorange', fontsize=9)

        ax.set_facecolor("#f7f7f7")  
        ax.set_title("Impacto de incrementar el peso de Happiness en los resultados", fontsize=16)
        ax.set_xlabel("Peso de Happiness", fontsize=14)
        ax.set_ylabel("Valores Promedio", fontsize=14)
        ax.legend(title="Métricas", loc="best", fontsize=12)

        plt.grid(True, which='both', linestyle='--', linewidth=0.6, color='gray', alpha=0.7)
        plt.tight_layout()
        plt.savefig("exp6.png")

        plt.switch_backend('TkAgg')

        fig, ax = plt.subplots(figsize=(8, 6))

        ax.axis('tight')
        ax.axis('off')

        data = {'Peso de Happiness': pesos, 'Tiempo Promedio (s)': tiempos}

        tabla = ax.table(cellText=[data[key] for key in data.keys()],
                        rowLabels=['Peso de Happiness', 'Tiempo Promedio (s)'],
                        cellLoc='center',
                        loc='center')

        tabla.scale(1, 2)
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(10)
        tabla.auto_set_column_width(col=list(range(len(pesos))))

        ax.set_title("Tala_temps_exp6", fontsize=16)
        plt.show()

#==============================================================================================================================
#===================================================== EXPERIMENT 7 ===========================================================
#==============================================================================================================================
     
    if exp == 7:               
        npaq = 50
        sol = 1
        semillas = [1234,5678,1357,2468,1122]
        pesos_happiness = [0 + (1 * i) for i in range(11)]  # Pesos de felicidad de 0 a 2 en pasos de 0.2
        factor = 1.2
        resultados_por_happiness = []
        operador = 1
        heuristica = 2

        for peso in pesos_happiness:
            res = []

            for seed in semillas:
                paquetes = random_paquetes(npaq, seed)
                ofertas = random_ofertas(paquetes, factor, seed)
                experiment = 2 #SA
                problema = ProblemParameters(ofertas, paquetes, experiment, operador, heuristica)
                problema.peso_happiness = peso
            
                start1 = timer()
                estado_inicial = generate_initial_state(problema, sol)
                end1 = timer()
                temps_ini = round((end1 - start1) * 1000, 2)

                conts, costs, felicidades, tiempos, pasos = [], [], [], [], []

                for _ in range(5):
                    start2 = timer()
                    n = simulated_annealing (Azamon( estado_inicial ), schedule = exp_schedule( k =125 , lam =0.01 , limit =100000) )
                    end2 = timer()
                    
                    conts.append(n.params.contador)
                    costs.append(n.calcular_cost())
                    felicidades.append(n.happiness())
                    tiempos.append((end2 - start2))
                    pasos.append(n.params.contador)  

                    n.params.contador = 0
                    

                # Mitjanes
                cont = round(statistics.mean(conts), 2)
                cst = round(statistics.mean(costs), 2)
                fel = round(statistics.mean(felicidades), 2)
                t = round(statistics.mean(tiempos), 2)
                avg_pasos = round(statistics.mean(pasos), 2)  
                print(f"Realizado experimento con peso happiness: {peso} en la semilla: {seed}")
                res.append([peso, temps_ini, avg_pasos, round(estado_inicial.calcular_cost(), 2), cst, round(estado_inicial.calcular_cost() - cst, 2), fel, t])

            resultados_por_happiness.append((peso, res))

        promedios = []
        for pesos_happiness, res in resultados_por_happiness:
            promedio_cost_inicial = statistics.mean([fila[3] for fila in res])
            promedio_cost = statistics.mean([fila[4] for fila in res])
            promedio_diferencia = statistics.mean([fila[5] for fila in res])
            promedio_felicitat = statistics.mean([fila[6] for fila in res])
            promedio_temps = statistics.mean([fila[7] for fila in res])
            promedios.append([pesos_happiness, promedio_cost_inicial, promedio_cost, promedio_diferencia, promedio_felicitat, promedio_temps])

        pesos = [fila[0] for fila in promedios]
        cost_iniciales = [fila[1] for fila in promedios]
        costs = [fila[2] for fila in promedios]
        diferencias = [fila[3] for fila in promedios]
        felicidades = [fila[4] for fila in promedios]
        tiempos = [fila[5] for fila in promedios]

        fig, ax = plt.subplots(figsize=(12, 7))

        ax.plot(pesos, diferencias, label="Diferencia (€)", marker='^', linestyle='-.', color='darkblue', markersize=8, linewidth=2)
        ax.plot(pesos, felicidades, label="Felicitat", marker='o', linestyle='--', color='darkorange', markersize=8, linewidth=2)

        for i, (peso, dif, fel) in enumerate(zip(pesos, diferencias, felicidades)):
            ax.text(peso, dif, f"{dif:.1f}", ha='right', color='darkblue', fontsize=9)
            ax.text(peso, fel, f"{fel:.1f}", ha='left', color='darkorange', fontsize=9)

        ax.set_facecolor("#f7f7f7") 
        ax.set_title("Impacto de incrementar el peso de Happiness en los resultados", fontsize=16)
        ax.set_xlabel("Peso de Happiness", fontsize=14)
        ax.set_ylabel("Valores Promedio", fontsize=14)
        ax.legend(title="Métricas", loc="best", fontsize=12)

        plt.grid(True, which='both', linestyle='--', linewidth=0.6, color='gray', alpha=0.7)

        plt.tight_layout()

        plt.savefig("exp7.png")
        plt.switch_backend('TkAgg')
        
        fig, ax = plt.subplots(figsize=(8, 6))

        ax.axis('tight')
        ax.axis('off')

        data = {'Peso de Happiness': pesos, 'Tiempo Promedio (s)': tiempos}

        tabla = ax.table(cellText=[data[key] for key in data.keys()],
                        rowLabels=['Peso de Happiness', 'Tiempo Promedio (s)'],
                        cellLoc='center',
                        loc='center')

        tabla.scale(1, 2)
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(10)
        tabla.auto_set_column_width(col=list(range(len(pesos))))

        ax.set_title("taula_temps_exp7", fontsize=16)
    
#==============================================================================================================================
#===================================================== EXPERIMENT 8 ===========================================================
#==============================================================================================================================

    if exp == 8:
        npaq = int((input('Si us plau, introdueixi el nombre de paquets: ')))
        print('====================================================================================')
        seed = int((input('Si us plau, introdueixi la seed: ')))
        print('====================================================================================')
        print('1 - Move')
        print('2 - Swap')
        print('3 - Swap múltiple')
        print('Per fer combinacions escriurem junt i de forma creixent (ex. Move i swap = 12)')
        operadors = int(input('Si us plau, introdueixi de quins operadors voldrà utilitzar: '))       
        print('====================================================================================')
        print('1 - Primer generador (prioritza cost)')
        print('2 - Segon generador (prioritza felicitat)')
        sol = int(input('Si us plau, introdueixi el número associat al generador que vulgui utilitzar: '))
        print('====================================================================================')
        print('1 - Primera herística (cost)')
        print('2 - Segona herística (cost+felicitat)')
        heuristica = int(input('Si us plau, introdueixi el número associat al generador que vulgui utilitzar: '))
        print('====================================================================================')
        print('1 - Hill Climbing')
        print('2 - Simulated Anealing')
        experiment = int(input('Si us plau, introdueixi el número associat a l\'experiment voldrà executar: '))
        print('====================================================================================')
        if experiment == 2:
            kval = int(input('Si us plau, introdueixi el valor del paràmetre k (recomanat 125): '))
            lambdaval = float(input('Si us plau, introdueixi el valor del paràmetre lambda (recomanat 0.01): '))
            limitval = int(input('Si us plau, introdueixi el valor del paràmetre limit (recomanat 100000): '))

        sol = 1 if sol == 2 else 0
        factor = 1.2
        paquetes = random_paquetes(npaq, seed)
        ofertas = random_ofertas(paquetes, factor, seed)
        problema = ProblemParameters(ofertas, paquetes, experiment, operadors, heuristica)
        start = timer()
        estado_inicial = generate_initial_state(problema, sol)
        end = timer()
        print('Tiempo de generación de estado inicial (ms):',(end - start)*1000)
    
        if experiment == 1:
            start = timer()
            n = hill_climbing ( Azamon( estado_inicial ) )
            end = timer()
            print('Tiempo que tardo en encontrar solución (ms):',(end - start)*1000)
            print ('Pasos: ',n.params.contador) # Estat final
            lst = n.params.heuristiques
            plt.plot(lst)

            plt.xlabel("iteracions")
            plt.ylabel("Heurística")

            plt.savefig("heur.png")

            print("Coste sol inicial: " , estado_inicial.calcular_cost())
            print("Coste sol final: " , n.calcular_cost())
            print("Calcul de felicitat inicial: ",estado_inicial.happiness())
            print("Calcul de felicitat final: ",n.happiness())
        
        if experiment == 2:
            start = timer()
            n = simulated_annealing (Azamon( estado_inicial ), schedule = exp_schedule( k =kval , lam =lambdaval , limit =limitval) )
            end = timer()
            print('Tiempo que tardo en encontrar solución (ms):',(end - start)*1000)
            print ('Pasos: ',n.params.contador  ) # Estat final
            lst = n.params.heuristiques
            plt.plot(lst)

            plt.xlabel("iteracions")
            plt.ylabel("Heurística")

            plt.savefig("heur.png")
            print("Coste sol inicial: " , estado_inicial.calcular_cost())
            print("Coste sol final: " , n.calcular_cost())
            print("Calcul de felicitat inicial: ",estado_inicial.happiness())
            print("Calcul de felicitat final: ",n.happiness())

        

                
                
            
  
    

   

    
    
    
    