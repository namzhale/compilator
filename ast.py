# ast.py

class ASTNode:
    """
    Base class for all nodes in the Abstract Syntax Tree (AST).
    This class acts as a parent for more specific node types.
    """
    pass


class BinOpNode(ASTNode):
    """
    Node representing a binary operation (e.g., addition, subtraction).

    Attributes:
        left (ASTNode): The left operand of the binary operation.
        op (str): The operator for the binary operation (e.g., '+', '-', '*', '/').
        right (ASTNode): The right operand of the binary operation.
    """

    def __init__(self, left, op, right):
        """
        Initializes a binary operation node.

        Args:
            left (ASTNode): The left operand of the operation.
            op (str): The operator as a string.
            right (ASTNode): The right operand of the operation.
        """
        self.left = left
        self.op = op
        self.right = right


class NumberNode(ASTNode):
    """
    Node representing a numeric value (either integer or float).

    Attributes:
        value (int or float): The numeric value stored in the node.
    """

    def __init__(self, value):
        """
        Initializes a number node with a specific numeric value.

        Args:
            value (int or float): The numeric value to store in this node.
        """
        self.value = value


class VarAssignNode(ASTNode):
    """
    Node representing a variable assignment operation.

    Attributes:
        name (str): The name of the variable being assigned.
        value (ASTNode): The value or expression to be assigned to the variable.
    """

    def __init__(self, name, value):
        """
        Initializes a variable assignment node.

        Args:
            name (str): The name of the variable being assigned.
            value (ASTNode): The expression or value being assigned to the variable.
        """
        self.name = name
        self.value = value


class VarAccessNode(ASTNode):
    """
    Node representing access to a variable's value.

    Attributes:
        name (str): The name of the variable being accessed.
    """

    def __init__(self, name):
        """
        Initializes a variable access node.

        Args:
            name (str): The name of the variable to access.
        """
        self.name = name


class WhileNode(ASTNode):
    """
    Node representing a 'while' loop, which repeatedly executes a body of code as long as a condition is true.

    Attributes:
        condition (ASTNode): The condition that controls the loop execution.
        body (list of ASTNode): The list of statements to execute as long as the condition is true.
    """

    def __init__(self, condition, body):
        """
        Initializes a while loop node.

        Args:
            condition (ASTNode): The loop condition to be evaluated before each iteration.
            body (list of ASTNode): The body of the loop to execute as long as the condition is true.
        """
        self.condition = condition
        self.body = body


class IfNode(ASTNode):
    """
    Node representing an 'if' conditional statement with an optional 'else' clause.

    Attributes:
        condition (ASTNode): The condition to evaluate to determine whether to execute the 'if' body.
        if_body (list of ASTNode): The list of statements to execute if the condition is true.
        else_body (list of ASTNode, optional): The list of statements to execute if the condition is false.
    """

    def __init__(self, condition, if_body, else_body=None):
        """
        Initializes an if-conditional node, including optional 'else' statements.

        Args:
            condition (ASTNode): The condition to evaluate to decide whether to execute the 'if' body.
            if_body (list of ASTNode): The list of statements to execute if the condition is true.
            else_body (list of ASTNode, optional): The list of statements to execute if the condition is false.
        """
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body
