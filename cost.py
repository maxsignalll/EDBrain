import math


def calculate_mu(all_models, table_size):
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
    for i in range(len(all_models)):
        for model in all_models[i]:
            init_cost = model.init_cost
            cost_pct = init_cost / float(max_memory)
            cost = normal_pdf(cost_pct, mu_list[i], 0.2)
            model.cost = cost
    return all_models


def normal_pdf(x, mu, sigma):
    coefficient = 1 / (sigma * math.sqrt(2 * math.pi))
    exponent = -((x - mu) ** 2) / (2 * sigma ** 2)
    return coefficient * math.exp(exponent)

