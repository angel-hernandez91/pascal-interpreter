#Token Types
INTEGER = 'INTEGER'
PLUS = 'PLUS'
EOF = 'EOF'
WHITESPACE = 'WHITESPACE'
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
		return 'Token({}, {})'.format(self.type, self.value)

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

	def error(self):
		raise ParseException('Error parsing input.')

	def get_next_token(self):
		"""Lexical analyzer (scanner / tokenizer)

		This method is responsible for breaking a sentence
		apart into tokens. One token at a time
		"""
		text = self._text

		if self._pos > len(text) - 1:
			return Token(EOF, None)

		current_char = text[self._pos]

		if current_char.isdigit():
			token = Token(INTEGER, int(current_char))
			self._pos += 1
			return token

		if current_char == '+':
			token = Token(PLUS, current_char)
			self._pos += 1
			return token

		# Account for whitespace
		if current_char in ['\t', ' ']:
			token = Token(WHITESPACE, None)
			self._pos += 1
			return token



		self.error()

	def eat(self, token_type):
		print(self._current_token.type + '====' + token_type)
		if self._current_token.type == token_type:
			self._current_token = self.get_next_token()
		else:
			self.error()

	def expr(self):
		self._current_token = self.get_next_token()

		left = self._current_token
		self.eat(INTEGER)

		op = self._current_token
		self.eat(PLUS)

		right = self._current_token
		self.eat(INTEGER)

		result = eval('{}{}{}'.format(left.value, op.value, right.value))
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
