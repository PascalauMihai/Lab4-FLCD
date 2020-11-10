class FiniteAutomata:
    def __init__(self, givenFileName):
        self.fileName = givenFileName
        self.states = []
        self.inputSymbols = []
        self.initialState = ""
        self.finalStates = []
        self.transitions = {}
        self.readInputFromFile()

    def readStates(self, givenCurrentLine, givenFileReader):
        self.states = givenCurrentLine.split(" ")
        self.states[-1] = self.states[-1][0:-1]
        currentLine = givenFileReader.readline()
        return currentLine, givenFileReader

    def readInputSymbols(self, givenCurrentLine, givenFileReader):
        self.inputSymbols = givenCurrentLine.split(" ")
        self.inputSymbols[-1] = self.inputSymbols[-1][0:-1]
        currentLine = givenFileReader.readline()
        return currentLine, givenFileReader

    def readInitialState(self, givenCurrentLine, givenFileReader):
        self.initialState = givenCurrentLine[0:-1]
        currentLine = givenFileReader.readline()
        return currentLine, givenFileReader

    def readFinalStates(self, givenCurrentLine, givenFileReader):
        self.finalStates = givenCurrentLine.split(" ")
        self.finalStates[-1] = self.finalStates[-1][0:-1]
        currentLine = givenFileReader.readline()
        return currentLine, givenFileReader

    def readTransitions(self, givenCurrentLine, givenFileReader):
        while givenCurrentLine:
            if givenCurrentLine == '\n':
                return givenCurrentLine, givenFileReader
            transitionResult = givenCurrentLine.split("->")[1].strip()
            transitionInput = [element.strip() for element in givenCurrentLine.split("->")[0].split(",")]
            if (transitionInput[0], transitionInput[1]) in self.transitions:
                if isinstance(self.transitions[(transitionInput[0], transitionInput[1])], list):
                    self.transitions[(transitionInput[0], transitionInput[1])].append(transitionResult)
                else:
                    firstTransitionExistent = self.transitions[(transitionInput[0], transitionInput[1])]
                    newSetOfTransitions = [firstTransitionExistent, transitionResult]
                    self.transitions[(transitionInput[0], transitionInput[1])] = newSetOfTransitions
            else:
                self.transitions[(transitionInput[0], transitionInput[1])] = transitionResult
            givenCurrentLine = givenFileReader.readline()

        return givenCurrentLine, givenFileReader

    def readInputFromFile(self):
        with open(self.fileName, 'r') as fileReader:
            currentLine = fileReader.readline()
            lineNumber = 1
            switchCase = {
                1: self.readStates,
                2: self.readInputSymbols,
                3: self.readInitialState,
                4: self.readFinalStates,
                5: self.readTransitions
            }
            while currentLine:
                if lineNumber not in switchCase:
                    print("Error: invalid input. Line - ", lineNumber)
                currentReadFunction = switchCase[lineNumber]
                currentLine, fileReader = currentReadFunction(currentLine, fileReader)
                lineNumber += 1

    def _validateSequence(self, currentState, givenSequence):
        if givenSequence == "":
            if currentState in self.finalStates:
                return True
            return False

        currentPoint = (currentState, givenSequence[0])
        if currentPoint not in self.transitions:
            return False

        if isinstance(self.transitions[currentPoint], list):
            for state in self.transitions[currentPoint]:
                if self._validateSequence(state, givenSequence[1:]):
                    return True
            return False
        else:
            return self._validateSequence(self.transitions[currentPoint], givenSequence[1:])

    def validateSequence(self, givenSequence):
        for key in self.transitions.keys():
            if isinstance(self.transitions[key], list):
                print("Given FA is not DFA")
                return "Not DFA"
        return self._validateSequence(self.initialState, givenSequence)

    def print(self):
        print("States: ", end="")
        for state in self.states:
            print(state + " ", end="")

        print("\nInput Symbols: ", end="")
        for symbol in self.inputSymbols:
            print(symbol + " ", end="")

        print("\nInitial State: " + self.initialState)

        print("Final States: ", end="")
        for state in self.finalStates:
            print(state + " ", end="")

        print("\nTransitions:")
        for transition in self.transitions:
            print(str(transition) + " = " + str(self.transitions[transition]))


def runFA_in():
    print("\nFinite Automata FA.in:\n")
    FA = FiniteAutomata("FA.in")
    FA.print()
    sequence = input("Sequence to be verified:")
    print(FA.validateSequence(sequence))


def runIdentifier():
    print("\nFinite Automata Identifier:\n")
    FAIdentifier = FiniteAutomata("FAIdentifier.in")
    FAIdentifier.print()
    sequence = input("Sequence to be verified:")
    print(FAIdentifier.validateSequence(sequence))


def runConstant():
    print("\nFinite Automata Integer Constant:\n")
    FAConstant = FiniteAutomata("FAIntegerConstant.in")
    FAConstant.print()
    sequence = input("Sequence to be verified:")
    print(FAConstant.validateSequence(sequence))


def run():
    while True:
        print("1. Print FA.in and verify a sequence")
        print("2. Print FA Identifier and verify a sequence")
        print("3. Print FA Constant and verify a sequence")
        print("0. Exit")
        inputGiven = input("Option:")
        print(inputGiven)
        if inputGiven == "1":
            runFA_in()
        elif inputGiven == "2":
            runIdentifier()
        elif inputGiven == "3":
            runConstant()
        elif inputGiven == "0":
            return


#run()
