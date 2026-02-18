# This file is part of the materials accompanying the book
# "Mathematical Logic through Python" by Gonczarowski and Nisan,
# Cambridge University Press. Book site: www.LogicThruPython.org
# (c) Yannai A. Gonczarowski and Noam Nisan, 2017-2022
# File name: propositions/operators.py

"""Syntactic conversion of propositional formulas to use only specific sets of
operators."""

from propositions.syntax import *
from propositions.semantics import *

def to_not_and_or(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'~'``, ``'&'``, and ``'|'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'~'``, ``'&'``, and
        ``'|'``.
    """
    # Task 3.5
    root = formula.root
    if is_variable(root):
        return formula
    if root == 'T':
        p = Formula('p')
        return Formula('|',p, Formula('~', p))
    if root =='F':
        p = Formula('p')
        return Formula('&',p, Formula('~', p))
    if root == '~':
        inner = to_not_and_or(formula.first)
        return Formula('~', inner)
    left = to_not_and_or(formula.first)
    right = to_not_and_or(formula.second)
    if root == '&':
        return Formula('&',left, right)
    if root == '|':
        return Formula('|',left, right)
    if root == '->':
        return Formula('|',Formula('~', left),right)

    if root =='+':
        a = Formula('&', left, Formula('~', right))
        b =Formula('&', Formula('~', left), right)
        return Formula('|', a,b)

    if root == '<->':
        a= Formula('&',left, right)
        b = Formula('&',Formula('~', left),Formula('~', right))
        return Formula('|', a, b)
    if root== '-&':
        return Formula('~', Formula('&',left, right))
    if root =='-|':
        return Formula('~',Formula('|', left, right))
    assert False

def to_not_and(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'~'`` and ``'&'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'~'`` and ``'&'``.
    """
    # Task 3.6a
    temp = to_not_and_or(formula)
    new_formula = temp.substitute_operators({
        '|': Formula.parse('~(~p&~q)')})
    return new_formula
def to_nand(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'-&'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'-&'``.
    """
    # Task 3.6b
    f = to_not_and(formula)
    f = f.substitute_operators({'~': Formula.parse('(p-&p)'), '&': Formula.parse('((p-&q)-&(p-&q))')})
    return f

def to_implies_not(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'->'`` and ``'~'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'->'`` and ``'~'``.
    """
    # Task 3.6c
    f = to_not_and_or(formula)
    f = f.substitute_operators({'|': Formula.parse('(~p->q)'),'&': Formula.parse('~(p->~q)')})
    return f

def to_implies_false(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'->'`` and ``'F'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'->'`` and ``'F'``.
    """
    # Task 3.6d
    temp = to_implies_not(formula)
    new_form= temp.substitute_operators({'~': Formula.parse('(p->F)')})
    return new_form

