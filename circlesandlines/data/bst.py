import random

class TreeNode:
    def __init__(self,key,val,left=None,right=None,parent=None, height=0, size=1):
        self.key = key
        self.payload = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent
        self.height = height
        self.size = size

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def replaceNodeData(self,key,value,lc,rc,h,s):
        self.key = key
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        self.height = h
        self.size = s
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self

    def updateheight(self, dheight, newHeight):
        if (dheight > 0 and newHeight > self.height) or (dheight < 0 and newHeight == self.height-1): #farthest leaf is starting node
                if self.height+dheight >= 0:
                    self.height += dheight
                if self.parent:
                    if self.parent.hasBothChildren():
                        if (self.isLeftChild() and self.height != self.parent.rightChild.height-1) or (self.isRightChild() and self.height != self.parent.leftChild.height-1):
                                self.parent.updateheight(dheight, newHeight+1)
                    else:
                        self.parent.updateheight(dheight, newHeight+1)


    def updatesize(self, dsize):
        self.size += dsize
        if self.parent:
            self.parent.updatesize(dsize)

class BinarySearchTree:

    def __init__(self):
        self.root = None

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def checkBalance(self, node):
        if node.height <= 3:
            return False
        elif node.hasBothChildren():
            factor = node.leftChild.size/node.rightChild.size
            if factor <= 0.5 or factor >= 2:
                return True
            else:
                return False
        else:
            return True

    def put(self,key,val):
        if self.root:
            self._put(key,val,self.root)
        else:
            self.root = TreeNode(key,val)

    def _put(self,key,val,currentNode):
        if self.checkBalance(currentNode):
            self.balance(currentNode)
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self._put(key,val,currentNode.leftChild)
            else:
                
                currentNode.leftChild = TreeNode(key,val,None,None,currentNode,0,1)
                currentNode.updateheight(1, 1)
                currentNode.updatesize(1)
        else:
            if currentNode.hasRightChild():
                self._put(key,val,currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key,val,None,None,currentNode,0,1)
                currentNode.updateheight(1, 1)
                currentNode.updatesize(1)

    def __setitem__(self,k,v):
        self.put(k,v)

    def get(self,key):
        if self.root:
            res = self._get(key,self.root)
            if res:
                return res.payload
            else:
                return None
        else:
            return None

    def _get(self,key,currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self._get(key,currentNode.leftChild)
        else:
            return self._get(key,currentNode.rightChild)

    def __getitem__(self,key):
        return self.get(key)

    def __contains__(self,key):
        if self._get(key,self.root):
            return True
        else:
            return False

    def delete(self,key):
        if self.root and self.root.hasAnyChildren():
            nodeToRemove = self._get(key,self.root)
            if nodeToRemove:
                self.remove(nodeToRemove)
            else:
                raise KeyError('Error, key not in tree')
        elif self.root and self.root.isLeaf() and self.root.key == key:
            self.root = None
            self.root.height, self.root.size = 0, 1
        else:
            raise KeyError('Error, key not in tree')

    def __delitem__(self,key):
        self.delete(key)

    def spliceOut(self,currentNode):
        if currentNode.isLeaf():
            if currentNode.isLeftChild():
                currentNode.parent.leftChild = None
            else:
                currentNode.parent.rightChild = None
            if currentNode.parent.isLeaf():
                currentNode.parent.updateheight(-1, 0)
            currentNode.parent.updatesize(-1)
        elif currentNode.hasAnyChildren():
            if currentNode.hasLeftChild():
                if currentNode.isLeftChild():
                    currentNode.parent.leftChild = currentNode.leftChild
                    currentNode.parent.updateheight(-1, currentNode.parent.leftChild.height+1)
                else:
                    currentNode.parent.rightChild = currentNode.leftChild
                    currentNode.parent.updateheight(-1, currentNode.parent.rightChild.height+1)
                currentNode.leftChild.parent = currentNode.parent

            else:
                if currentNode.isLeftChild():
                    currentNode.parent.leftChild = currentNode.rightChild
                    currentNode.parent.updateheight(-1, currentNode.parent.leftChild.height+1)
                else:
                    currentNode.parent.rightChild = currentNode.rightChild
                    currentNode.parent.updateheight(-1, currentNode.parent.rightChild.height+1)
                currentNode.rightChild.parent = currentNode.parent
            currentNode.parent.updatesize(-1)

    def findSuccessor(self,currentNode):
        if checkbalance(currentNode):
            balance(currentNode)
        succ = None
        if currentNode.hasRightChild():
            succ = self.findMin(currentNode.rightChild)
        else:
            if currentNode.parent:
                if currentNode.isLeftChild():
                    succ = currentNode.parent
                else:
                    currentNode.parent.rightChild = None
                    succ = currentNode.parent.findSuccessor()
                    currentNode.parent.rightChild = currentNode
        return succ

    def findMin(self, currentNode): #returns a node with lowest key from subtree starting at currentNode
        while currentNode.hasLeftChild():
            if checkbalance(currentNode):
                balance(currentNode)
            currentNode = currentNode.leftChild
        return currentNode

    def remove(self,currentNode):
        if checkbalance(currentNode):
            balance(currentNode)
        if currentNode.isLeaf(): #leaf
            if currentNode == currentNode.parent.leftChild:
                currentNode.parent.leftChild = None
            else:
                currentNode.parent.rightChild = None
            currentNode.parent.updateheight(-1, 0)
            currentNode.parent.updatesize(-1)
        elif currentNode.hasBothChildren(): #interior
            succ = self.findSuccessor(currentNode)
            self.spliceOut(succ)
            currentNode.key = succ.key
            currentNode.payload = succ.payload

        else: # this node has one child
            if currentNode.hasLeftChild():
                if currentNode.isLeftChild():
                    currentNode.parent.updateheight(-1, currentNode.height)
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.leftChild
                    currentNode.parent.updatesize(-1)
                elif currentNode.isRightChild():
                    currentNode.parent.updateheight(-1, currentNode.height)
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.leftChild
                    currentNode.parent.updatesize(-1)
                else:
                    currentNode.replaceNodeData(currentNode.leftChild.key,
                                    currentNode.leftChild.payload,
                                    currentNode.leftChild.leftChild,
                                    currentNode.leftChild.rightChild, currentNode.leftChild.height, currentNode.leftChild.size)
            else:
                if currentNode.isLeftChild():
                    currentNode.parent.updateheight(-1, currentNode.height)
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.rightChild
                    currentNode.parent.updatesize(-1)
                elif currentNode.isRightChild():
                    currentNode.parent.updateheight(-1, currentNode.height)
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.rightChild
                    currentNode.parent.updatesize(-1)
                else:
                    currentNode.replaceNodeData(currentNode.rightChild.key,
                                    currentNode.rightChild.payload,
                                    currentNode.rightChild.leftChild,
                                    currentNode.rightChild.rightChild, currentNode.rightChild.height, currentNode.rightChild.size)
    def balance(self, subroot):
        sort = []
        size = subroot.size
        parent = subroot.parent
        def stepthrough(subroot):
            if subroot:
                for l in stepthrough(subroot.leftChild):
                    yield l
                for r in stepthrough(subroot.rightChild):
                    yield r
                yield (subroot.key, subroot.payload)
        sort = list(stepthrough(subroot))
        print(sort)
        mid = len(sort)//2
        subroot = TreeNode(sort[mid][0], sort[mid][1], None, None, parent)
        self.rebuild(subroot, sort)
    def rebuild(self, node, sort):
        if not sort:
            return
        else:
            mid = len(sort)//2
            node = TreeNode(sort[mid][0], sort[mid][1], self.rebuild(node.leftChild, sort[:mid]), self.rebuild(node.rightChild, sort[mid+1:]), node.parent)


#Demonstrating how it works:
a = BinarySearchTree()
a[50], a[75], a[13], a[63], a[87], a[7], a[19], a[69], a[93], a[3], a[16], a[66], a[15], a[18], a[17], a[65], a[67] = '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17'
"""del a[16]
del a[66]
del a[7]
del a[19]
del a[63]
del a[87]"""
a.balance(a.root.leftChild)

#itried
a.balance(a.root.rightChild)

def sorted(self, currentNode):
    if currentNode == None:
        return []
    else:
        return self.sorted(currentNode.leftChild) + [currentNode] + self.sorted(currentNode.rightChild)