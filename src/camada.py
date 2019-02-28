from numpy import exp, array, random, dot, delete


class camada(object):
    numeroNeuronios = 0
    entradasPorNeuronio = 0

    def __init__(self,numeroDeNeuronios,entradasPorNeuronio):
        self.numeroNeuronios = numeroDeNeuronios
        self.entradasPorNeuronio = entradasPorNeuronio
        self.gerarCamada(numeroDeNeuronios,entradasPorNeuronio)



    def gerarCamada(self,numeroDeNeuronios,entradasPorNeuronio):
        self.pesos= 2 * random.random((entradasPorNeuronio,numeroDeNeuronios)) - 1


