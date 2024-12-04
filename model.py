"""
Model.
"""


class Model:
    """
    Model class.
    An abstraction of repeated query sequences.
    """
    def __init__(self, db, tables, cost, rerun_times):
        self.tables = tables
        self.db = db
        self.init_reward = 0
        self.init_cost = cost
        self.rerun_times = rerun_times
        self.cost = 0
        self.reward = 0

    def __repr__(self):
        return f'(Model: tables:{self.tables}, db:{self.db}, cost: {self.cost}, reward: {self.reward})'
