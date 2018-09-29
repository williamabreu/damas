from .square import Square
from .piece import Piece
from constants import Color
from constants import Direction

class Board:
	def __init__(self):
		self.matrix = self.new_board()

	def new_board(self):
		"""
		Create a new board matrix.
		"""

		# initialize squares and place them in matrix

		matrix = [[None] * 8 for i in range(8)]

		# The following code block has been adapted from
		# http://itgirl.dreamhosters.com/itgirlgames/games/Program%20Leaders/ClareR/Checkers/checkers.py
		for x in range(8):
			for y in range(8):
				if (x % 2 != 0) and (y % 2 == 0):
					matrix[y][x] = Square(Color.WHITE)
				elif (x % 2 != 0) and (y % 2 != 0):
					matrix[y][x] = Square(Color.BLACK)
				elif (x % 2 == 0) and (y % 2 != 0):
					matrix[y][x] = Square(Color.WHITE)
				elif (x % 2 == 0) and (y % 2 == 0): 
					matrix[y][x] = Square(Color.BLACK)

		# initialize the pieces and put them in the appropriate squares

		for x in range(8):
			for y in range(3):
				if matrix[x][y].color == Color.BLACK:
					matrix[x][y].occupant = Piece(Color.RED)
			for y in range(5, 8):
				if matrix[x][y].color == Color.BLACK:
					matrix[x][y].occupant = Piece(Color.BLUE)

		return matrix

	def board_string(self, board):
		"""
		Takes a board and returns a matrix of the board space colors. Used for testing new_board()
		"""

		board_string = [[None] * 8] * 8 

		for x in range(8):
			for y in range(8):
				if board[x][y].color == Color.WHITE:
					board_string[x][y] = "WHITE"
				else:
					board_string[x][y] = "BLACK"


		return board_string
	
	def rel(self, dir, coord):
		"""
		Returns the coordinates one square in a different direction to (x,y).

		===DOCTESTS===

		>>> board = Board()

		>>> board.rel(NORTHWEST, (1,2))
		(0,1)

		>>> board.rel(SOUTHEAST, (3,4))
		(4,5)

		>>> board.rel(NORTHEAST, (3,6))
		(4,5)

		>>> board.rel(SOUTHWEST, (2,5))
		(1,6)
		"""
		x, y = coord

		if dir == Direction.NORTHWEST:
			return (x - 1, y - 1)
		elif dir == Direction.NORTHEAST:
			return (x + 1, y - 1)
		elif dir == Direction.SOUTHWEST:
			return (x - 1, y + 1)
		elif dir == Direction.SOUTHEAST:
			return (x + 1, y + 1)
		else:
			return 0

	def adjacent(self, coord):
		"""
		Returns a list of squares locations that are adjacent (on a diagonal) to (x,y).
		"""
		x, y = coord
		return [self.rel(Direction.NORTHWEST, (x,y)), self.rel(Direction.NORTHEAST, (x,y)),self.rel(Direction.SOUTHWEST, (x,y)),self.rel(Direction.SOUTHEAST, (x,y))]

	def location(self, coord):
		"""
		Takes a set of coordinates as arguments and returns self.matrix[x][y]
		This can be faster than writing something like self.matrix[coords[0]][coords[1]]
		"""
		x, y = coord
		return self.matrix[x][y]

	def blind_legal_moves(self, coord):
		"""
		Returns a list of blind legal move locations from a set of coordinates (x,y) on the board. 
		If that location is empty, then blind_legal_moves() return an empty list.
		"""
		x, y = coord

		if self.matrix[x][y].occupant != None:
			
			if self.matrix[x][y].occupant.king == False and self.matrix[x][y].occupant.color == Color.BLUE:
				blind_legal_moves = [self.rel(Direction.NORTHWEST, (x,y)), self.rel(Direction.NORTHEAST, (x,y))]
				
			elif self.matrix[x][y].occupant.king == False and self.matrix[x][y].occupant.color == Color.RED:
				blind_legal_moves = [self.rel(Direction.SOUTHWEST, (x,y)), self.rel(Direction.SOUTHEAST, (x,y))]

			else:
				blind_legal_moves = [self.rel(Direction.NORTHWEST, (x,y)), self.rel(Direction.NORTHEAST, (x,y)), self.rel(Direction.SOUTHWEST, (x,y)), self.rel(Direction.SOUTHEAST, (x,y))]

		else:
			blind_legal_moves = []

		return blind_legal_moves

	def legal_moves(self, coord, hop = False):
		"""
		Returns a list of legal move locations from a given set of coordinates (x,y) on the board.
		If that location is empty, then legal_moves() returns an empty list.
		"""

		x, y = coord
		blind_legal_moves = self.blind_legal_moves((x,y)) 
		legal_moves = []

		if hop == False:
			for move in blind_legal_moves:
				if hop == False:
					if self.on_board(move):
						if self.location(move).occupant == None:
							legal_moves.append(move)

						elif self.location(move).occupant.color != self.location((x,y)).occupant.color and self.on_board((move[0] + (move[0] - x), move[1] + (move[1] - y))) and self.location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant == None: # is this location filled by an enemy piece?
							legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

		else: # hop == True
			for move in blind_legal_moves:
				if self.on_board(move) and self.location(move).occupant != None:
					if self.location(move).occupant.color != self.location((x,y)).occupant.color and self.on_board((move[0] + (move[0] - x), move[1] + (move[1] - y))) and self.location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant == None: # is this location filled by an enemy piece?
						legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

		return legal_moves

	def remove_piece(self, coord):
		"""
		Removes a piece from the board at position (x,y). 
		"""
		x, y = coord
		self.matrix[x][y].occupant = None

	def move_piece(self, coord_start, coord_end):
		"""
		Move a piece from (start_x, start_y) to (end_x, end_y).
		"""
		start_x, start_y = coord_start
		end_x, end_y = coord_end
		self.matrix[end_x][end_y].occupant = self.matrix[start_x][start_y].occupant
		self.remove_piece((start_x, start_y))

		self.king((end_x, end_y))

	def is_end_square(self, coords):
		"""
		Is passed a coordinate tuple (x,y), and returns true or 
		false depending on if that square on the board is an end square.

		===DOCTESTS===

		>>> board = Board()

		>>> board.is_end_square((2,7))
		True

		>>> board.is_end_square((5,0))
		True

		>>>board.is_end_square((0,5))
		False
		"""

		if coords[1] == 0 or coords[1] == 7:
			return True
		else:
			return False

	def on_board(self, coord):
		"""
		Checks to see if the given square (x,y) lies on the board.
		If it does, then on_board() return True. Otherwise it returns false.

		===DOCTESTS===
		>>> board = Board()

		>>> board.on_board((5,0)):
		True

		>>> board.on_board(-2, 0):
		False

		>>> board.on_board(3, 9):
		False
		"""
		x, y = coord

		if x < 0 or y < 0 or x > 7 or y > 7:
			return False
		else:
			return True


	def king(self, coord):
		"""
		Takes in (x,y), the coordinates of square to be considered for kinging.
		If it meets the criteria, then king() kings the piece in that square and kings it.
		"""
		x, y = coord

		if self.location((x,y)).occupant != None:
			if (self.location((x,y)).occupant.color == Color.BLUE and y == 0) or (self.location((x,y)).occupant.color == Color.RED and y == 7):
				self.location((x,y)).occupant.king = True 
