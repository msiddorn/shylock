#!/usr/bin/python3
'''
    Conceptualisation of people spending money within a pool of peers
'''
from collections import defaultdict


class BaseShylockException(Exception):
    ''' base exception class for the shylock program'''


class UserNotFoundError(BaseShylockException):
    ''' User not found where it was expected '''


class NoneUniqueUserError(BaseShylockException):
    ''' Ambiguous reference to a user '''


class Pool:
    '''
        A pool is a group of users and transactions where people spend and consume money
        and everything is fair and equal
    '''

    def __init__(self, name='Nameless pool'):
        self.name = name
        self.users = []
        self.balances = defaultdict(float)
        self.old_transactions = []

    def add_user(self, name):
        if name is None or name in self.users:
            raise NoneUniqueUserError('new users in a pool must have a unique name')
        self.users.append(name)

    def add_transaction(self, spender, amount, consumers):
        for user in [spender] + list(consumers.keys()):
            if user not in self.users:
                raise UserNotFoundError('User {} not in pool'.format(user))
        self.balances[spender] -= amount
        norm_factor = 1 / sum(ratio for ratio in consumers.values())
        for consumer, ratio in consumers.items():
            self.balances[consumer] += amount * ratio * norm_factor

        self.old_transactions.append({
            'spender': spender,
            'amount': amount,
            'consumers': consumers,
        })
