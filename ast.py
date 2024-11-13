# ast.py

class ASTNode:
    pass

class BinOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

class VarAssignNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class VarAccessNode(ASTNode):
    def __init__(self, name):
        self.name = name

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class IfNode(ASTNode):
    def __init__(self, condition, if_body, else_body=None):  # Добавлен параметр else_body
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body
