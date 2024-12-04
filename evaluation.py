"""
Model evaluation code.
"""


def evaluation(all_models, max_memory):
    """
    model evaluation.
    :param max_memory: available system memory.
    :param all_models: all models of databases.
    :return: best model for each database.
    """
    db_num = len(all_models)
    pareto_frontiers = []
    # obtain Pareto frontier for all databases.
    for i in range(db_num):
        db_models = all_models[i]
        not_in_border = []

        for j in db_models:
            for k in db_models:
                if float(j.init_reward) < float(k.init_reward) and float(j.cost) < float(k.cost):
                    not_in_border.append(j)
        borderline = list(filter(lambda x: x not in not_in_border, db_models))

        # reward normalization.
        all_reward = []
        for model in borderline:
            all_reward.append(float(model.init_reward))
        max_reward = max(all_reward)
        min_reward = min(all_reward)
        if max_reward != min_reward:
            norm_borderline = []
            for model in borderline:
                reward = float(model.init_reward)
                norm_reward = (reward - min_reward) / (max_reward - min_reward)
                model.reward = norm_reward
                norm_borderline.append(model)
        else:
            norm_borderline = []
            for model in borderline:
                reward = float(model.init_reward)
                norm_reward = reward
                model.reward = norm_reward
                norm_borderline.append(model)
        pareto_frontiers.extend(norm_borderline)
    # sort all models list.
    sorted_models = sorted(pareto_frontiers, key=lambda x: x.reward + x.cost, reverse=True)
    # decide each database's model.
    best_models = []
    total_cost = 0
    model_pointer = 0
    selected_db = []
    while len(best_models) < db_num and total_cost < max_memory:
        model = sorted_models[model_pointer]
        if model.db not in selected_db:
            total_cost += model.init_cost
            if total_cost > max_memory:
                model_pointer += 1
                continue
            best_models.append(model)
            selected_db.append(model.db)
        model_pointer += 1
    print("Best models:")
    print(best_models)
    return best_models
