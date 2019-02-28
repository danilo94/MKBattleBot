from gerenciadorMemoria import *
from Player import *
from copy import copy
from camada import *
from Network import *
from KeyController import *
from random import *
import time
import math

POPULACAO = 15
MUTATIONRATE = 25

class GameController(object):
    player1 = None
    player2 = None
    memoryHandler = None
    populacao = []
    individuoSelecionado = None
    controladorTeclado = None
    melhorIndividuo = None
    indice = 0
    tempoVivo = 0

    def criaPopulacaoInicial(self):
        for i in range(0, POPULACAO):
            self.populacao.append(self.criaRede())

    def __init__(self, emulatorName):
        self.controladorTeclado = keyController()
        self.memoryHandler = MemoryHandler(emulatorName)
        self.player1 = Player(0)
        self.player2 = Player(1)
        self.criaPopulacaoInicial()
        self.indice = 0
        self.tempoVivo = 0
        self.selecionarIndiviuo()
        self.melhorIndividuo = None

    def startGame(self):
        while True:

            tempoInicial = time.time() * 1000
            self.atualizarPlayers()
            if not self.player1.isDead():
                vidap1, vidap2, distancia,lado = self.obterDadosPlayers()
                saida = self.individuoSelecionado.entradaDados(vidap1, vidap2, distancia,lado)
                self.gerarComandos(saida)

            if self.player1.isDead():
                self.calculaQualidade()
                self.selecionarIndiviuo()

            if self.venceu() > 1:
                self.individuoSelecionado.wins = self.individuoSelecionado.wins + 1
                time.sleep(3)
            tempoFinal = time.time() * 1000
            self.atualizarTempoVivo(tempoInicial, tempoFinal)

    def atualizarTempoVivo(self, tempoInicial, tempoFinal):
        self.tempoVivo = self.tempoVivo + int(tempoFinal - tempoInicial)

    def gerarComandos(self, networkOutput):
        comandOut = []
        for i in range(0, len(networkOutput)):
            if networkOutput[i] >= 0.5:
                comandOut.append(True)
            else:
                comandOut.append(False)

        self.controladorTeclado.pressionar(comandOut)

    def obterDadosPlayers(self):
        vidap1 = self.player1.getLife()
        vidap2 = self.player2.getLife()
        distancia = self.player1.getDistance()
        lado = self.player1.getLado()
        return vidap1, vidap2, distancia, lado

    def selecionarIndiviuo(self):
        self.tempoVivo = 0
        self.selecionarMelhorIndividuo()
        if (self.indice == POPULACAO - 1):
            self.indice = 0
            self.algoritmoGenetico()
        else:
            self.indice = self.indice + 1
        self.resetarJogo()
        self.individuoSelecionado = self.populacao[self.indice]

    def atualizarPlayers(self):
        self.updatePlayer1()
        self.updatePlayer2()

    def updatePlayer1(self):
        vidap1 = self.memoryHandler.lerByte(P1LIFE)
        distp1 = self.memoryHandler.lerPalavra(POSP1)
        distp2 = self.memoryHandler.lerPalavra(POSP2)
        dist = self.calcDist(distp1, distp2)
        lado = self.memoryHandler.lerByte(P1LADO)
        self.player1.updateData(dist, distp1, vidap1, self.tempoVivo,lado)
        pass

    def updatePlayer2(self):
        pass
        vidap2 = self.memoryHandler.lerByte(P2LIFE)
        distp1 = self.memoryHandler.lerPalavra(POSP2)
        distp2 = self.memoryHandler.lerPalavra(POSP1)
        dist = self.calcDist(distp1, distp2)
        self.player2.updateData(dist, distp2, vidap2, self.tempoVivo,0)
    def calcDist(self, dist1, dist2):
        return math.fabs(dist1 - dist2)

    def criaRede(self):
        camada1 = camada(4, 4)
        camada2 = camada(6, 4)
        camada3 = camada(10,6)
        camada4 = camada(10, 10)

        rede = Network()
        rede.inserirCamada(camada1)
        rede.inserirCamada(camada2)
        rede.inserirCamada(camada3)
        rede.inserirCamada(camada4)
        return rede

    def resetarJogo(self):
        self.controladorTeclado.pressKey(CARREGARSAVESTATE)
        time.sleep(1)
        self.controladorTeclado.releaseKey(CARREGARSAVESTATE)

    def calculaQualidade(self):
        danoSofrido = self.danoSofrido()
        danoCausado = self.danoCausado()
        tempoVivo = self.tempoSobrevivido()
        self.individuoSelecionado.fitness = danoCausado - danoSofrido

    def danoSofrido(self):
        vidap = self.player1.life
        porcentagemVida = float(((100 * vidap / 166)) / 100)
        vidaPerdida = math.fabs(porcentagemVida * 166 - 166)

        return int(vidaPerdida * 2)

    def danoCausado(self):
        vidap = self.player2.life
        porcentagemVida = float(((100 * vidap / 166)) / 100)
        vidaPerdida = math.fabs(porcentagemVida * 166 - 166)

        return int(vidaPerdida * 6)

    def tempoSobrevivido(self):
        timeAlive = self.tempoVivo
        self.tempoVivo = 0
        return int((timeAlive * 1)/10)

    def venceu(self):
        return self.memoryHandler.lerByte(P1WINS)

    def selecionarMelhorIndividuo(self):
        if (self.melhorIndividuo == None):
            self.melhorIndividuo = copy(self.individuoSelecionado)
        else:
            if (self.melhorIndividuo.fitness < self.individuoSelecionado.fitness):
                self.melhorIndividuo = copy(self.individuoSelecionado)
                self.melhorIndividuo.store()

    def resetarIndividuos(self):
        self.populacao.clear()
        self.populacao.append(copy(self.melhorIndividuo))
        self.criaPopulacaoInicialApartir(1)

    def criaPopulacaoInicialApartir(self, start):
        for start in range(1, POPULACAO):
            self.populacao.append(self.criaRede())



    def algoritmoGenetico(self):
        melhoresIndividuos = self.selecao()
        self.cruzamento(melhoresIndividuos)

        pass


    def cruzamento(self,individuos):
        melhorIndividuo = self.melhorIndividuo
        self.populacao.clear()
        for individuo in individuos:
           novoIndividuo = self.executarCruzamento(melhorIndividuo,individuo)
           self.populacao.append(copy(novoIndividuo))

        while len(self.populacao)<POPULACAO:
            self.populacao.append(self.criaRede())


    def executarCruzamento(self,melhorIndividuo,individuo):
        novoIndividuo = Network()
        for i in range(0,len(melhorIndividuo.layers)):
            geneA = melhorIndividuo.layers[i]
            geneB = individuo.layers[i]
            novaCamada = self.crossOver(geneA,geneB)
            novoIndividuo.inserirCamada(novaCamada)
        return novoIndividuo
        pass



    def crossOver(self,genesA,genesB):
        novaCamada = copy(genesA)
        for i in range(0,len(genesA.pesos)):
            for j in range(0,len(genesA.pesos[i])):
                peso = uniform(0,1)
                if peso >= 0.5:
                    novaCamada.pesos[i][j] = genesA.pesos[i][j]
                else:
                    novaCamada.pesos[i][j] = genesB.pesos[i][j]
                mutar = uniform(0,1)
                if (mutar<=MUTATIONRATE):
                    novaCamada.pesos[i][j] = uniform(-1,1)
        return novaCamada


    def selecao(self):
        individuos = copy(self.populacao)
        print ("Melhor Individuo: ",self.melhorIndividuo.fitness)
        individuos.sort(key=lambda a:a.fitness,reverse=True)
        del(individuos[0])
        i=0
        for individuo in individuos:
            if (individuo.fitness < 0.6*self.melhorIndividuo.fitness):
                del(individuos[i])
            i=i+1

        return individuos

