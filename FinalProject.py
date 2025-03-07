class linkedListNode:
    def __init__(self, payload, nextNode = None):
        self.dataload = payload
        self.nextNode = nextNode
        

#MAIN
nodeA = linkedListNode('Binil')
nodeB = linkedListNode('Sam')
nodeC = linkedListNode('Rachel')
nodeD = linkedListNode('Tamara')


nodeA.nextNode = nodeB
nodeB.nextNode = nodeC
nodeC.nextNode = nodeD

currentNode = nodeA
while currentNode.nextNode is not None:
    print(f"The friend of {currentNode.dataload} = {currentNode.nextNode.dataload}")
    currentNode = currentNode.nextNode
if currentNode.nextNode is None:
    print(f"The friend of {currentNode.dataload} = None")



currentNode = nodeA
while True:
    print(f"{currentNode.dataload}")
    if currentNode.nextNode is not None:
        print(f"The friend of {currentNode.dataload} = ")
    currentNode = currentNode.nextNode
    if currentNode.nextNode is None:
        print("None")
        break