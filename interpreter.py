from ast import *


class Interpreter:
    """
    Interpreter for executing an Abstract Syntax Tree (AST).

    Attributes:
        variables (dict): Stores variable names and their values for the program's environment.
    """

    def __init__(self):
        """
        Initializes the interpreter with an empty environment for variables.
        """
        self.variables = {}  # Dictionary to store variable values

    def interpret(self, nodes):
        """
        Interprets a list of AST nodes representing a program.

        Args:
            nodes (list of ASTNode): The list of AST nodes to execute.

        Returns:
            result: The result of the last executed statement.
        """
        result = None  # To store the result of the last evaluated node
        for node in nodes:
            result = self.interpret_node(node)
        return result

    def interpret_node(self, node):
        """
        Interprets a single AST node and returns its result.

        Args:
            node (ASTNode): The AST node to interpret.

        Returns:
            result: The result of interpreting the node, based on its type.

        Raises:
            ValueError: If an unknown node type is encountered.
        """
        # Handle numeric literals
        if isinstance(node, NumberNode):
            return node.value

        # Handle binary operations (e.g., +, -, *, /)
        elif isinstance(node, BinOpNode):
            left_val = self.interpret_node(node.left)
            right_val = self.interpret_node(node.right)

            # Perform the operation based on the operator in the node
            if node.op == '+':
                return left_val + right_val
            elif node.op == '-':
                return left_val - right_val
            elif node.op == '*':
                return left_val * right_val
            elif node.op == '/':
                # Perform integer division if both operands are integers
                if isinstance(left_val, int) and isinstance(right_val, int):
                    return left_val // right_val
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

        # Handle variable assignment
        elif isinstance(node, VarAssignNode):
            value = self.interpret_node(node.value)  # Evaluate the assigned value
            self.variables[node.name] = value  # Store the value in the variables dictionary
            return value

        # Handle variable access
        elif isinstance(node, VarAccessNode):
            # Retrieve the variable value or return 0 if the variable is not defined
            return self.variables.get(node.name, 0)

        # Handle 'while' loop
        elif isinstance(node, WhileNode):
            result = None
            # Loop while the condition evaluates to True
            while self.interpret_node(node.condition):
                for stmt in node.body:
                    result = self.interpret_node(stmt)
            return result

        # Handle 'if' statement with optional 'else' clause
        elif isinstance(node, IfNode):
            if self.interpret_node(node.condition):
                # Execute the 'if' body if the condition is true
                for stmt in node.if_body:
                    self.interpret_node(stmt)
            elif node.else_body:
                # Execute the 'else' body if the condition is false and 'else' body exists
                for stmt in node.else_body:
                    self.interpret_node(stmt)
            return None

        # Error handling for unexpected node types
        else:
            raise ValueError(f"Unknown node type: {type(node)}")
