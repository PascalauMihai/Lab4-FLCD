class Node:
    def __init__(self, givenValue):
        self.__value = givenValue
        self.__nextNodePosition = -1

    def getValue(self):
        return self.__value

    def setValue(self, givenValue):
        self.__value = givenValue

    def getNextNodePosition(self):
        return self.__nextNodePosition

    def setNextNodePosition(self, givenNextNodePosition):
        self.__nextNodePosition = givenNextNodePosition

    def printNode(self):
        print("Value: " + str(self.getValue()) + " NextNodePosition: " + str(self.getNextNodePosition()))

    def printNodeString(self):
        return "Value: " + str(self.getValue()) + " NextNodePosition: " + str(self.getNextNodePosition())


class HashTable:
    def __init__(self, givenCapacity=51):
        self.capacity = givenCapacity
        self.data = [Node([""]) for index in range(self.capacity)]
        self.emptyPosition = 0

    def calculateHashCode(self, givenElement):
        characters = list(givenElement)
        hashCode = 0
        for character in characters:
            hashCode += ord(character)

        return hashCode

    def hashFunction(self, givenElement, constant=13):
        return (givenElement % self.capacity + constant) % self.capacity

    def findEmptyPosition(self):
        for index in range(self.capacity):
            if self.data[index].getValue()[0] == "":
                self.emptyPosition = index
                return
        self.emptyPosition = -1
        return

    def add(self, givenElement):
        self.findEmptyPosition()
        if self.emptyPosition == -1:  # list is full -> we increase the capacity
            oldCapacity = self.capacity
            self.capacity *= 2
            oldData = self.data
            self.data = [Node([""]) for index in range(self.capacity)]
            for index in range(oldCapacity):
                self.data[index] = oldData[index]

        currentPosition = self.hashFunction(self.calculateHashCode(givenElement))
        if self.data[currentPosition].getValue()[0] == "":  # empty node on current position
            self.data[currentPosition].setValue(givenElement)
        elif self.data[currentPosition].getNextNodePosition() == -1:  # occupied node on current position but no
            # nextNodePosition
            self.data[self.emptyPosition].setValue(givenElement)
            self.data[currentPosition].setNextNodePosition(self.emptyPosition)
        else:  # occupied node on current position and existing
            # nextNodePosition -> we go until we dont have
            # another nextNodePosition
            while self.data[currentPosition].getNextNodePosition() != -1:
                currentPosition = self.data[currentPosition].getNextNodePosition()
            self.data[self.emptyPosition].setValue(givenElement)
            self.data[currentPosition].setNextNodePosition(self.emptyPosition)

    def find(self, givenElement):
        currentPosition = self.hashFunction(self.calculateHashCode(givenElement))
        if self.data[currentPosition].getValue() == givenElement:
            return currentPosition
        elif self.data[currentPosition].getNextNodePosition() == -1:
            return -1
        else:
            while self.data[currentPosition].getNextNodePosition() != -1:
                if self.data[currentPosition].getValue() == givenElement:
                    return currentPosition
                else:
                    currentPosition = self.data[currentPosition].getNextNodePosition()
            if self.data[currentPosition].getValue() == givenElement:
                return currentPosition
            return -1

    def print(self):
        for index in range(self.capacity):
            if self.data[index].getValue() != ['']:
                print("Position: " + str(index), end=' ')
                self.data[index].printNode()

    def printString(self):
        printableString = ""
        for index in range(self.capacity):
            if self.data[index].getValue() != ['']:
                printableString += "Position: " + str(index) + " " + self.data[index].printNodeString() + '\n'

        return printableString

    def getValueOfPosition(self, givenPosition):
        return self.data[givenPosition].getValue()
