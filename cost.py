"""
Cost calculation.
"""
import math


def calculate_mu(all_models, table_size):
    """
    Calculate each database's proportion(mu) of table size.
    :param all_models: all models.
    :param table_size: each table size of one database.
                       Implemented based on TPC-C.
    :return: proportion of each database.
    """
    db_num = len(all_models)
    db_active_size_list = []
    all_db_active_table_size = 0
    for i in range(db_num):
        table_set = set()
        for model in all_models[i]:
            for table in model.tables:
                table_set.add(table)
        active_table_size = 0
        for table in table_set:
            active_table_size += table_size[table]
        db_active_size_list.append(active_table_size)
        all_db_active_table_size += active_table_size
    mu_list = []
    for i in range(db_num):
        mu_list.append(float(db_active_size_list[i]) / all_db_active_table_size)
    return mu_list


def cost_calculation(all_models, mu_list, max_memory):
    """
    Calculate each database's cost.
    :param all_models: all models
    :param mu_list: proportion of each database.
    :param max_memory: system available memory.
    :return: all models with calculated cost.
    """
    for i in range(len(all_models)):
        for model in all_models[i]:
            init_cost = model.init_cost
            cost_pct = init_cost / float(max_memory)
            cost = normal_pdf(cost_pct, mu_list[i], 0.2)
            model.cost = cost
    return all_models


def normal_pdf(x, mu, sigma):
    """
    normal pdf function.
    :param x: input of function.
    :param mu: average mu.
    :param sigma: standard deviation.
    :return: pdf of function.
    """
    coefficient = 1 / (sigma * math.sqrt(2 * math.pi))
    exponent = -((x - mu) ** 2) / (2 * sigma ** 2)
    return coefficient * math.exp(exponent)

