#Token Types
INTEGER = 'INTEGER'
PLUS = 'PLUS'
EOF = 'EOF'
MINUS = 'MINUS'
DIV = 'DIV'
MULT = 'MULT'
LPAREN = '('
RPAREN = ')'


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

class Lexer:
	def __init__(self, text):
		# client string input, e.g. "3 * 5", "12 / 3 * 4", etc
		self._text = text
		# self._pos is an index into self._text
		self._pos = 0
		# current token instance
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

			if self._current_char == '(':
				self.advance()
				return Token(LPAREN, '(')

			if self._current_char == ')':
				self.advance()
				return Token(RPAREN, ')')

			self.error()

		return Token(EOF, None)


class Interpreter:
	def __init__(self, lexer):
		self._lexer = lexer
		self._current_token = self._lexer.get_next_token()

	def eat(self, token_type):
		""" Compare the current token type with the passed token
		If they match, eat the current token and assign the next token
		to the current token.
		"""
		if self._current_token.type == token_type:
			self._current_token = self._lexer.get_next_token()
		else:
			self._lexer.error()

	def factor(self):
		""" factor: INTEGER | LPAREN expr RPAREN"""
		token = self._current_token
		if token.type == INTEGER:
			self.eat(INTEGER)
			return token.value
		elif token.type == LPAREN:
			self.eat(LPAREN)
			result = self.expr()
			self.eat(RPAREN)
			return result

	def term(self):
		"""term: factor((MULT | DIV) factor)* 
		"""
		result = self.factor()
		while self._current_token.type in (MULT, DIV):
			token = self._current_token
			if token.type == MULT:
				self.eat(MULT)
				result = result * self.factor()
			elif token.type == DIV:
				self.eat(DIV)
				result = result / self.factor()
		return result

	def expr(self):
		"""Arithmetic expression parser / interpreter
		pascal> 14 + 2 * 3 - 6 / 2
		17

		expr 	: term((PLUS | MINUS) term)*
		term	: factor((MULT | DIV) factor)*
		factor	: INTEGER
		"""
		result = self.term()
		while self._current_token.type in (PLUS, MINUS):
			token = self._current_token
			if token.type == PLUS:
				self.eat(PLUS)
				result = result + self.term()
			elif token.type == MINUS:
				self.eat(MINUS)
				result = result - self.term()

		return result

def main():
	while True:
		try:
			text = input('pascal> ')
		except EOFError:
			break
	
		if not text:
			continue
		if text.lower() == 'exit':
			break
		lexer = Lexer(text)
		interpreter = Interpreter(lexer)
		result = interpreter.expr()
		print(result)

if __name__ == '__main__':
	main()
