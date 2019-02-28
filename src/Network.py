from numpy import exp, array, random, dot


class Network(object):
    fitness = 0
    wins = 0
    layers = []

    def __init__(self):
        self.fitness = 0
        self.wins = 0
        self.layers = []

    def inserirCamada(self, camada):
        self.layers.append(camada)

    def sigmoid(self, x):
        return 1 / (1 + exp(x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def entradaDados(self, distancia, hpPlayer1, hpPlayer2,lado):
        pass
        dados = [distancia, hpPlayer1, hpPlayer2,lado]
        saida = []
        for i in range(0, len(self.layers)):

            if (i == 0):
                saida = self.sigmoid(dot(dados, self.layers[i].pesos))
            else:
                saida = self.sigmoid(dot(saida, self.layers[i].pesos))
        return saida


    def store(self):
        file = open("best.txt",'w')
        file.write(str(self.fitness)+" ")
        file.write(str(len(self.layers))+" ")
        for layer in self.layers:
            file.write(str(layer.numeroNeuronios)+" "+str(layer.entradasPorNeuronio)+"\\n")
            for i in range (0,len(layer.pesos)):
                file.write("\\n")
                for j in range (0,len(layer.pesos[i])):
                    file.write(str(layer.pesos[i][j])+" ")


