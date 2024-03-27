import simpy
import random

class FilaSimples:
    def __init__(self, env, taxa_chegada, taxa_atendimento, capacidade_fila):
        self.env = env
        self.servidor = simpy.Resource(env, capacity=1)
        self.taxa_chegada = taxa_chegada
        self.taxa_atendimento = taxa_atendimento
        self.capacidade_fila = capacidade_fila
        self.fila = []
        self.perda_clientes = 0
        self.tempo_global = 0

    def chegada_cliente(self):
        while True:
            yield self.env.timeout(random.uniform(*self.taxa_chegada))
            if len(self.fila) < self.capacidade_fila:
                self.fila.append(self.env.now)
            else:
                self.perda_clientes += 1

    def atendimento_cliente(self):
        while True:
            with self.servidor.request() as req:
                yield req
                if self.fila:
                    self.fila.pop(0)
                    yield self.env.timeout(random.uniform(*self.taxa_atendimento))
                else:
                    yield self.env.timeout(0)

    def monitoramento(self):
        while True:
            yield self.env.timeout(1)
            self.tempo_global += 1

def simulacao(taxa_chegada, taxa_atendimento, capacidade_fila, max_eventos):
    env = simpy.Environment()
    fila = FilaSimples(env, taxa_chegada, taxa_atendimento, capacidade_fila)
    env.process(fila.chegada_cliente())
    env.process(fila.atendimento_cliente())
    env.process(fila.monitoramento())
    
    eventos_processados = 0
    while eventos_processados < max_eventos:
        print(eventos_processados)
        env.step()
        eventos_processados += 1

    print("Resultados da simulação:")
    print(f"Número de clientes perdidos: {fila.perda_clientes}")
    print(f"Tempo global da simulação: {fila.tempo_global}")
    if fila.tempo_global > 0:
        print(f"Distribuição de probabilidades: {len(fila.fila) / fila.tempo_global}")
    else:
        print("Nenhum cliente foi atendido durante a simulação.")

# Simulação para G/G/1/5
print("Simulação para G/G/1/5:")
simulacao([2, 5], [3, 5], 5, 1000)

# Simulação para G/G/2/5
print("\nSimulação para G/G/2/5:")
simulacao([2, 5], [3, 5], 5, 1000)