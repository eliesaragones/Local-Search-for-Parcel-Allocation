from typing import List
from abia_azamon import random_ofertas,random_paquetes,Paquete,Oferta
#from azamon_state import StateRepresentation


class ProblemParameters(object):
    def __init__(self, ofertas = List[Oferta], packages = List[Paquete], experiment = 1, operadors = 1, heuristica = 1, peso_happiness = 0):
        self.ofertas = ofertas  # ofertas de transporte
        self.packages = packages # paquetes a enviar
        self.contador = 0
        self.heuristiques = []
        self.experiment = experiment
        self.operadors = operadors
        self.heuristica = heuristica
        self.peso_happiness = peso_happiness
        

    def __repr__(self):
        return f"Params(ofertas={self.ofertas}, packages={self.packages})"
    

    


    
        
    