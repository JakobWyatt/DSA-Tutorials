import sys
from typing import Any
from DSAStack import DSAStack
from DSAQueue import DSAQueue, DSACircularQueue, DSAShufflingQueue

def solve(equation : str) -> float:
    return _evaluatePostfix(_parseInfixToPostfix(equation))

def _parseInfixToPostfix(equation : str) -> DSAQueue:
    tokens = equation.split(' ')
    stack = DSAStack(len(tokens))
    queue = DSAShufflingQueue(len(tokens))
    for x in tokens:
        if x == '(':
            stack.push(x)
        elif _precedenceOf(x) > 0:
            while _precedenceOf(stack.top()) >= _precedenceOf(x):
                queue.enqueue(stack.pop())
            stack.push(x)
        elif x == ')':
            while stack.top() != '(':
                queue.enqueue(stack.pop())
            stack.pop()
        else:
            queue.enqueue(float(x))
    while not stack.isEmpty():
        queue.enqueue(stack.pop())
    return queue


def _evaluatePostfix(postfixQueue : DSAQueue) -> float:
    operandStack = DSAStack(postfixQueue.count())
    while not postfixQueue.isEmpty():
        x = postfixQueue.dequeue()
        if _precedenceOf(x) > 0:
            op2, op1 = (operandStack.pop(), operandStack.pop())
            operandStack.push(_executeOperation(x, op1, op2))
        else:
            operandStack.push(x)
    return operandStack.pop()

def _precedenceOf(theOp : str) -> int:
    return {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2
    }.get(theOp, 0)

def _executeOperation(op : str, op1 : float, op2 : float):
    return {
        '+': op1 + op2,
        '-': op1 - op2,
        '*': op1 * op2,
        '/': op1 / op2
    }[op]

if __name__ == '__main__':
    print(solve(sys.argv[1]))
