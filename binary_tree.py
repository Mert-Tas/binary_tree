#!/usr/bin/python

import random

# Binary Tree Implementation
class BinaryTree():

	global MININT, MAXINT
	MININT = -10000
	MAXINT =  10000

	global LEFT, RIGHT
	LEFT = -1
	RIGHT = 1

	def __init__(self, value):
		self.left = None
		self.right = None
		# if not converted to number it will be treated as string, '6' > '30'
		self.root = int(value) 

		
	def getLeftChild(self):
		return self.left
	def getRightChild(self):
		return self.right
	def setRootVal(self, value):
		self.root = value
	def getRootVal(self):
		return self.root
	def getRootNode(self):
		return self

	def insertLeft(self, newNode):
		if self.left is None:
			self.left = newNode
		else:
			self = self.left
			if newNode.root < self.getRootVal():
				#print("insert left")
				self.insertLeft(newNode)
			else:
				#print("insert right")
				self.insertRight(newNode)
	
	def insertRight(self, newNode):
		if self.right is None:
			self.right = newNode
		else:
			self = self.right
			if newNode.root < self.getRootVal():
				#print("insert left")
				self.insertLeft(newNode)
			else:
				#print("insert right")
				self.insertRight(newNode)
				
	# Returns the height or maxDepth (The number of nodes along the longest path from the root
	# down to the farthest leaf node) of the tree. The height of an empty tree is 0.
	# Parameters: (2) the current root of the tree. Give root if you want to count all nodes.	
	def height(self, currentNode):
		if currentNode is None:
			return 0
		else:
			leftCnt = self.height(currentNode.left)
			rightCnt = self.height(currentNode.right)
			
			if (leftCnt > rightCnt):
				return leftCnt + 1
			else:
				return rightCnt + 1
				
	def printNodesInLevel(self, currentNode, level, direction):
		if currentNode is None:
			return
		else:
			if level == 1:
				print(currentNode.root, end = " ")
			else:
				# Print nodes from left to right
				if direction == LEFT:
					self.printNodesInLevel(currentNode.left, level - 1, direction)
					self.printNodesInLevel(currentNode.right, level - 1, direction)
				# Print nodes from right to left
				else:
					self.printNodesInLevel(currentNode.right, level - 1, direction)
					self.printNodesInLevel(currentNode.left, level - 1, direction)
				
	def breadthFirstPrint(self, currentNode):
		print("\nBinary Tree nodes in breadth first order:\n") 
		for i in range(0, self.height(currentNode)):    
			print('Level {} -     '.format(i), end = " ")
			self.printNodesInLevel(currentNode, i + 1, LEFT)
			print()

	# Added 27.11.2017
	def zigzagOrderPrint(self, currentNode):
		# Start from left to right, then alternate
		direction = LEFT
		print("\nBinary Tree nodes in zigzag order:\n") 
		for i in range(0, self.height(currentNode)):    
			print('Level {} -     '.format(i), end = " ")
			self.printNodesInLevel(currentNode, i + 1, direction)
			# Change direction on each level (ternary operator used)
			direction = RIGHT if (direction == LEFT) else LEFT 
			print()	

	# For a binary tree of n nodes, counts how many structurally
	# different binary trees could be constructed 
	def countPossibleTrees(self, numNodes):
		treeCnt = 0
		if numNodes < 2:
			treeCnt = 1
		else:
			for root in range(1, numNodes):
				left = self.countPossibleTrees(root - 1)
				right= self.countPossibleTrees(numNodes - root)

				# Number of possible trees with this root = left x right
				treeCnt += left * right

		return treeCnt

	def display(self, currentNode, level):
		if currentNode is not None:
			self.display(currentNode.right, level + 1)
			print()  # writes '\n'
			
			for i in range(0, level):
				print(end = "   ")
			print(str(currentNode.root))
			self.display(currentNode.left, level + 1)
			
	# AVL Trees: Balanced trees. The height difference between left and right
	# subtrees does not exceeds 1
		
	# Rotates the tree to left to make it balanced
	# Ex:  21
	#       \
	#        42
	#         \
	#          56
	# Unbalanced tree. height(left) = 0, height(right) = 2
	# Difference = 2.
	# Rotate root node to left so the tree becomes balanced
	# 		   42
	# 		  /  \
	# 		 21  56
	# Now height(left) = 1, height(right) = 1. Difference = 0
	def rotateLeft(self, currentNode):
		if currentNode is None or currentNode.right is None:
			return None
		else:
			newNode = currentNode.right  # 42-56
			currentNode.right = newNode.left   # None
			newNode.left = currentNode  # 21 
			
			return newNode
		
	# Rotates the tree to right to make it balanced
	# Ex:       21
	#          /
	#         13
	#        /
	#       8
	# Unbalanced tree. height(left) = 2, height(right) = 0
	# Difference = 2.
	# Rotate root node to right so the tree becomes balanced
	# 		   13
	# 		  /  \
	# 		 8   21
	# Now height(left) = 1, height(right) = 1. Difference = 0
	def rotateRight(self, currentNode):
		if currentNode is None or currentNode.left is None:
			return None
		else:
			newNode = currentNode.left  # 13-8
			currentNode.left = newNode.right  # None
			newNode.right = currentNode  # 21
			
			return newNode
			
	# Rebalances the given subtrees   (56 lines comment)
	#***************************************************
	# (1) Rebalance the right subtree. Compares the left and right subtree heights
	# If they differ more than 1:
	# (a)  21           height(R) = 2 > height(L) = 0  Diff = 2 inbalanced
	#       \
	#        42         height(R) = 1 > height(L) = 0
	#         \
	#          56
	# applies a left rotation to current.
	# 		   42
	# 		  /  \
	# 		 21  56
	# (b1) 21
	#       \
	#        42        height(L) = 1 > height(R) = 0
	#       /
	#     30
	# applies a right rotation to current->right.
	# (b2) 21
	#       \
	#        30
	#         \
	#          42
	# applies a left rotation to current.
	# So applies a double rotaion (RL)
	# 		   30
	# 		  /  \
	# 		 21   42
	#************************************************
	# (2) Rebalance the left subtree. Compares the left and right subtree heights
	# If they differ more than 1:
	# (a)       21       height(L) = 2 > height(R) = 0  Diff = 2 inbalanced
	#          /
	#         13	      height(R) = 1 > height(L) = 0
	#        /
	#       8
	# applies a right rotation to current.
	# 		   13
	# 		  /  \
	# 		 8   21
	# (b1)   21
	#       /
	#      13        height(R) = 1 > height(L) = 0
	#       \
	#        18
	# applies a left rotation to current->left.
	# (b2)   21
	#       /
	#      18
	#     /
	#    13
	# applies a right rotation to current.
	# So applies a double rotaion (LR)
	# 		   18
	# 		  /  \
	# 		13   21
	def rebalanceTree(self, currentNode):
		if currentNode is not None:	
			leftHeight = self.height(currentNode.left)
			rightHeight = self.height(currentNode.right)
			
			# Rotate to right
			if rightHeight > leftHeight + 1:
				# Case b1: Double rotation (RL)
				if (self.height(currentNode.right.left) > self.height(currentNode.right.right)):
					currentNode.right = self.rotateRight(currentNode.right)
				# Case a or b2: Apply left rotation to currentNode.right
				currentNode = self.rotateLeft(currentNode)
			# Rotate to left
			elif leftHeight > rightHeight + 1:
				# Case b1: Double rotation (LR)
				if (self.height(currentNode.left.right) > self.height(currentNode.left.left)):
					currentNode.left = self.rotateLeft(currentNode.left)
				# Case (a) or (b2): Apply right rotation to currentNode.left
				currentNode = self.rotateRight(currentNode)
				
		return currentNode
			
	# A Tree is balanced if the difference between the height of its hidari and migi
	# nodes are in the range -1 .. 1.  If the difference is -2 or 2 it is unbalanced.	
	def isBalanced(self, currentNode): 
		# If the tree is empty it is balanced
		if currentNode is None:
			return True
		else:
			leftHeight = self.height(currentNode.left)
			rightHeight = self.height(currentNode.right)
			
			# If difference between the subtrees is -2 or 2 tree is not balanced
			if leftHeight > rightHeight + 1 or rightHeight > leftHeight + 1:
				return False
			
			# The height of tree should be one more than the maximum height of its subtrees
			if self.height(currentNode) != (leftHeight + 1 if leftHeight > rightHeight else rightHeight +1):
				return False
				
			# Check the subtrees for balance
			return self.isBalanced(currentNode.left) and self.isBalanced(currentNode.right)

	# Returns true if the given tree is a Binary Search Tree
	def isBST(self, currentNode):
		return self.checkBST(currentNode, MININT, MAXINT) # float('inf'), int('-inf'))
	
	# Returns true if the given tree is a BST and its values are >= min and <= max
	def checkBST(self, currentNode, minVal, maxVal):
		if currentNode is None:
			return False
		else:
			# Check the current value if it is within minimum and maximum values
			if (currentNode.root < minVal and currentNode.root > maxVal):
				return False
				
			# Otherwise check the subtrees
			return self.checkBST(currentNode.left, minVal, currentNode.root) and self.checkBST(currentNode.right, currentNode.root + 1, maxVal)
		
	# A tree is an AVL Tree if it is both an ordered tree (BST) and balanced tree.
	def isAVL(self, currentNode):
		return self.isBST(currentNode) and self.isBalanced(currentNode)

	# Inserting an element to an AVL Tree is almost identical to inserting to a BST.
	# The difference is that after insertion the tree is rebalanced and new height
	# is calculated.
	def insertAVL(self, currentNode, value):
		value = int(value)
		if currentNode is None:
			currentNode = BinaryTree(value)
			currentNode.left = None
			currentNode.right =  None
			#print('Rebalance root node {}'.format(value))
			#currentNode = self.rebalanceTree(currentNode)
		else:
			if value <= currentNode.root:
				currentNode.left = self.insertAVL(currentNode.left, value)
				# Rebalance the left subtree
				currentNode.left = self.rebalanceTree(currentNode.left)
			else:
				currentNode.right = self.insertAVL(currentNode.right, value)
				# Rebalance the right subtree
				currentNode.right = self.rebalanceTree(currentNode.right)
				
		return currentNode
				
	def create(self):
		another_node = 'y'
		while another_node.lower() == 'y':
			rootNode = input("Enter a value for the new node: ")
			newNode = BinaryTree(rootNode)
			newNode.left = None;
			newNode.right = None;
			
			if newNode.root < self.getRootVal():
				#print("insert left")
				self.insertLeft(newNode)
			else:	
				#print("insert right")
				self.insertRight(newNode)
		
			another_node = input("Create another node (y/n)? ")

	def createAVLTree(self):
		another_node = 'y'
		nodeCnt = 0

		while another_node.lower() == 'y':
			rootNode = input("Enter a node for the AVL Tree: ")
			self.insertAVL(self.getRootNode(), rootNode)
			self.display(self.getRootNode().right, 1)
			nodeCnt += 1

			another_node = input("Enter a new value (y/n)? ")

		return nodeCnt
		
	def copyTree(self, currentNode):
		if currentNode is not None:
			newRoot = BinaryTree(currentNode.root)
			newRoot.left = self.copyTree(currentNode.left)
			newRoot.right = self.copyTree(currentNode.right)
		else:
			newRoot = None
			
		return newRoot


	def randomAVLTree(self, nodeList):
		for i in nodeList:
			self.insertAVL(self.getRootNode(), i)
			
##########################
# End of binary tree class       
	
def test():
	rootValue = input("Enter a number which will become the root: ")
	tree = BinaryTree(rootValue)
	
	tree.createAVLTree()
	
	#tree.create()
	#tree.display(tree.getRootNode(), 1)
	tree.breadthFirstPrint(tree.getRootNode())

def run():
	# First creates an initial (fake) node. 
	# Its value is lower than all the other nodes so the
	# real binary tree will be the right branch of this node.
	tree = BinaryTree(MININT)
	nodeNum = 0

	# Get the binary tree creation method from the user
	choice = int(input("(1) Create a random binary tree.\n(2) Create a binary tree manualy.\nPlease enter your choice: "))

	if choice == 1:
		# Gets the number of nodes from the user
		nodeNum = int(input("Please enter number of nodes (including root node) : "))

		# Creates a random list of nodes from a sufficient range of numbers
		nodeList = random.sample(range(1, nodeNum * 2), nodeNum)

		#for i in nodeList:
			#	print(i)

		# Creates a binary tree from the random nodes. 
		tree.randomAVLTree(nodeList)

	elif choice == 2:
		nodeNum = tree.createAVLTree()
	else:
		print("Exiting binary tree.")
		return 0

	# Copies the right branch to a new tree
	newTree = tree.copyTree(tree.getRootNode().right)

	tree.display(newTree.getRootNode(), 1)

	# Lists the nodes that are in the same depth
	tree.breadthFirstPrint(newTree.getRootNode())
	# Lists the nodes in alternating way for each level
	tree.zigzagOrderPrint(newTree.getRootNode())

	print('For {0} nodes number of possible different trees is {1}'.
		format(nodeNum, tree.countPossibleTrees(nodeNum)))
