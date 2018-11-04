#Token Types
INTEGER = 'INTEGER'
PLUS = 'PLUS'
EOF = 'EOF'
MINUS = 'MINUS'
DIV = 'DIV'
MULT = 'MULT'


class ParseException(Exception): pass

class Token:
	def __init__(self, type, value):
		#token type:
		self.type = type
		#token value
		self.value = value

	def __str__(self):
		"""String representation of the class instance.

		Examples:
			Token(INTEGER, 3)
			Token(PLUS, '+')
		"""
		return 'Token({}, {})'.format(self.type, repr(self.value))

	def __repr__(self):
		return self.__str__()

class Interpreter:
	def __init__(self, text):
		# user input e.g., "3+5"
		self._text = text
		# self._pos is an index into self._text
		self._pos = 0
		# current token instance
		self._current_token = None
		self._current_char = self._text[self._pos]

	def error(self):
		raise ParseException('Invalid syntax')

	def advance(self):
		"""Advance the 'pos' pointer and set the 'current_char' variable."""
		self._pos += 1
		if self._pos > len(self._text) - 1:
			self._current_char = None #End of Input
		else:
			self._current_char = self._text[self._pos]

	def skip_whitespace(self):
		"""Advance the pointer and ignore whitespace characters"""
		while self._current_char is not None and self._current_char.isspace():
			self.advance()

	def integer(self):
		"""Return an integer > 9 consumed from the input"""
		result = ''
		while self._current_char is not None and self._current_char.isdigit():
			result += self._current_char
			self.advance()
		return int(result)

	def get_next_token(self):
		"""Lexical analyzer (scanner / tokenizer)

		This method is responsible for breaking a sentence
		apart into tokens. One token at a time
		"""
		while self._current_char is not None:
			
			if self._current_char.isspace():
				self.skip_whitespace()
				continue

			if self._current_char.isdigit():
				return Token(INTEGER, self.integer())

			if self._current_char == '+':
				self.advance()
				return Token(PLUS, '+')

			if self._current_char == '-':
				self.advance()
				return Token(MINUS, '-')

			if self._current_char == '*':
				self.advance()
				return Token(MULT, '*')

			if self._current_char == '/':
				self.advance()
				return Token(DIV, '/')

			self.error()

		return Token(EOF, None)

    ##########################################################
    # Parser / Interpreter code                              #
    ##########################################################
	def eat(self, token_type):

		if self._current_token.type == token_type:
			self._current_token = self.get_next_token()
		else:
			self.error()

	def term(self):
		token = self._current_token
		self.eat(INTEGER)
		return token.value

	def expr(self):
		self._current_token = self.get_next_token()

		result = self.term()
		while self._current_token.type in (PLUS, MINUS, MULT, DIV):
			token = self._current_token
			if token.type == PLUS:
				self.eat(PLUS)
				result = result + self.term()
			elif token.type == MINUS:
				self.eat(MINUS)
				result = result - self.term()
			elif token.type == DIV:
				self.eat(DIV)
				result = result / self.term()
			elif token.type == MULT:
				self.eat(MULT)
				result = result * self.term()
			else:
				self.error()

		return result

def main():
	while True:
		try:
			text = input('pascal> ')
		except EOFError:
			break
	
		if not text:
			continue
		interpreter = Interpreter(text)
		result = interpreter.expr()
		print(result)

if __name__ == '__main__':
	main()
