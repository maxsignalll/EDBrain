import sqlite3
import time
import reward_cache


def obtain_reward(model, reward_db_path, query_candidate):
    cache_return = reward_cache.model_cache.find_cache(set(model.tables), model.db, model.init_cost)
    if cache_return != -1 and cache_return != -2:
        print("use reward cache.")
        return cache_return
    elif cache_return == -1:
        # replay or lwr
        n_time, y_time = model_replay(model.tables, model.rerun_times, reward_db_path, query_candidate)
        exact_reward = n_time - y_time
        reward_cache.model_cache.update(set(model.tables), model.db, model.init_cost, exact_reward)
        return exact_reward
    elif cache_return == -2:
        # replay or lwr
        n_time, y_time = model_replay(model.tables, model.rerun_times, reward_db_path, query_candidate)
        exact_reward = n_time - y_time
        reward_cache.model_cache.add_cache(set(model.tables), model.db, model.init_cost, exact_reward)
        return exact_reward


def model_replay(replay_query_list, rerun_times, replay_db_path, query_candidate):
    conn = sqlite3.connect(replay_db_path)
    cursor = conn.cursor()
    start_n = time.perf_counter()
    cursor.execute("PRAGMA cache_size=-0;")
    for repeat in range(3):
        for _ in range(rerun_times):
            for query in replay_query_list:
                cursor.execute(query_candidate[query])
    end_n = time.perf_counter()
    cursor.execute("PRAGMA cache_size=-120000;")  # replay with full cache
    start_y = time.perf_counter()
    for repeat in range(3):
        for _ in range(rerun_times):
            for query in replay_query_list:
                cursor.execute(query_candidate[query])
    end_y = time.perf_counter()
    cursor.close()
    conn.close()
    return (end_n - start_n) / 3, (end_y - start_y) / 3


def lwr():
    pass
