# interpreter.py

from ast import *

class Interpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, nodes):
        result = None
        for node in nodes:
            result = self.interpret_node(node)
        return result

    def interpret_node(self, node):
        if isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, BinOpNode):
            left_val = self.interpret_node(node.left)
            right_val = self.interpret_node(node.right)
            if node.op == '+':
                return left_val + right_val
            elif node.op == '-':
                return left_val - right_val
            elif node.op == '*':
                return left_val * right_val
            elif node.op == '/':
                if isinstance(left_val, int) and isinstance(right_val, int):
                    return left_val // right_val  # Integer division
                else:
                    return left_val / right_val
            elif node.op == '>':
                return left_val > right_val
            elif node.op == '<':
                return left_val < right_val
            elif node.op == '>=':
                return left_val >= right_val
            elif node.op == '<=':
                return left_val <= right_val
            elif node.op == '==':
                return left_val == right_val
            elif node.op == '!=':
                return left_val != right_val
            elif node.op == '&&':
                return left_val and right_val
            elif node.op == '||':
                return left_val or right_val
            else:
                raise ValueError(f"Unknown operator {node.op}")
        elif isinstance(node, VarAssignNode):
            value = self.interpret_node(node.value)
            self.variables[node.name] = value
            return value
        elif isinstance(node, VarAccessNode):
            return self.variables.get(node.name, 0)
        elif isinstance(node, WhileNode):
            result = None
            while self.interpret_node(node.condition):
                for stmt in node.body:
                    result = self.interpret_node(stmt)
            return result
        elif isinstance(node, IfNode):
            if self.interpret_node(node.condition):
                for stmt in node.if_body:
                    self.interpret_node(stmt)
            elif node.else_body:
                for stmt in node.else_body:
                    self.interpret_node(stmt)
            return None
        else:
            raise ValueError(f"Unknown node type: {type(node)}")
