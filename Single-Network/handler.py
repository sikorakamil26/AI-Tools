from singleNeuron import SingleNeuron
from directoryScanner import DirectoryScanner
from singleLayer import SingleLayer
from parser import Parser
import matplotlib.pyplot as plt

class Handler:
    # listOfDirectories: dictionary of (class, directory)
    def __init__(self, listOfDirectories):
        scanner = DirectoryScanner()
        # create neurons
        self.neurons = []
        for label in listOfDirectories:
            self.neurons.append(SingleNeuron(label))

        #create trainingVectors
        self.trainingVectors = []
        for label in listOfDirectories:
            self.trainingVectors.extend(scanner.scanDirectory(listOfDirectories[label], label))
        
        # create layer
        self.layer = SingleLayer(self.neurons)

    def trainNetwork(self, numberOfIterations, learningRate):
        i = 0
        for _ in range(numberOfIterations):
            for vetor in self.trainingVectors:
                i = i + 1
                # print("training nr: ", str(i))
                self.layer.train(vetor, learningRate)

    def getSimplecVector(self, myFile):
        parser = Parser()
        text = parser.parseText(myFile)
        vector = parser.createSimpleVector(text)
        return vector

    def classifySingleVector(self, vector):
        result = self.layer.classify(vector)
        return result

    def classifyVectorsFromDirectories(self, listOfDirectories):
        testVectors = []
        scanner = DirectoryScanner()
        for label in listOfDirectories:
            testVectors.extend(scanner.scanDirectory(listOfDirectories[label], label))

        total = 0 
        correct = 0

        for vector in testVectors:
            result = self.classifySingleVector(vector.vector)
            total += 1
            if result == vector.label:
                correct += 1
            
        return (float(correct)/float(total))*100

    def graphAccuracy(self, numberOfIterations, learningRate):
        testDirectories = {
            "English": "data/lang.test/English/",
            "German": "data/lang.test/German/",
            "Polish": "data/lang.test/Polish/"
        }
        print("plotting")
        iRange = []
        for i in range(numberOfIterations):
            iRange.append(i)
        
        acc = []
        for r in iRange:
            self.layer = SingleLayer(self.neurons)
            self.trainNetwork(r, learningRate)
            acc.append(self.classifyVectorsFromDirectories(testDirectories))

        print(acc)
        plt.plot(iRange,  acc)
        plt.show()

