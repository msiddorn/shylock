#!/usr/bin/python3
'''
    Conceptualisation of people spending money within a pool of peers
'''
from collections import defaultdict


class BaseShylockException(Exception):
    ''' base exception class for the shylock program'''


class MemberNotFoundError(BaseShylockException):
    ''' Member not found where it was expected '''


class NoneUniqueMemberError(BaseShylockException):
    ''' Ambiguous reference to a member '''


class Pool:
    '''
        A pool is a group of members and transactions where people spend and consume money
        and everything is fair and equal
    '''

    def __init__(self, name='Nameless pool'):
        self.name = name
        self.members = []
        self.balances = defaultdict(float)
        self.old_transactions = []

    def add_member(self, name):
        if name is None or name in self.members:
            raise NoneUniqueMemberError('new members in a pool must have a unique name')
        self.members.append(name)

    def add_transaction(self, spender, amount, consumers):
        for member in [spender] + list(consumers.keys()):
            if member not in self.members:
                raise MemberNotFoundError('Member {} not in pool'.format(member))
        self.balances[spender] -= amount
        norm_factor = 1 / sum(ratio for ratio in consumers.values())
        for consumer, ratio in consumers.items():
            self.balances[consumer] += amount * ratio * norm_factor

        self.old_transactions.append({
            'spender': spender,
            'amount': amount,
            'consumers': consumers,
        })
