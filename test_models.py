"""
test default and EDBrain methods' performance.
"""
import time
import sqlite3


def test_model(workloads, db_name, db_num, query_candidate, best_models):
    """
    test two different method.
    :param workloads: workload list for each database.
    :param db_name: name of db in config.
    :param db_num: number of db in config.
    :param query_candidate: query candidate of benchmark.
    :param best_models: models selected by EDBrain method.
    """
    print("\nTesting default method.")
    default_time = default_method(workloads, db_name, db_num, query_candidate)
    print("Testing EDBrain method.")
    model_time = model_method(best_models, workloads, db_name, db_num, query_candidate)
    print('Default time: {:.2f}, Model time: {:.2f}, performance improvement: {:.2f}%.'.format(
        default_time, model_time, ((default_time - model_time) * 100 / default_time)))


def default_method(workloads, db_name, db_num, query_candidate):
    """
    test workload without any cache tuning.
    :param workloads: workload list for each database.
    :param db_name: name of db in config.
    :param db_num: number of db in config.
    :param query_candidate: query candidate of benchmark.
    :return: total workload running time.
    """
    start = time.perf_counter()
    for i in range(db_num):
        conn = sqlite3.connect(f"{db_name}{i}.db")
        cursor = conn.cursor()
        for query_num in workloads[i]:
            cursor.execute(query_candidate[query_num])
            cursor.fetchall()
        cursor.close()
        conn.close()
    end = time.perf_counter()
    total_time = end - start
    return total_time


def model_method(best_models, workloads, db_name, db_num, query_candidate):
    """
    test workload with EDBrain cache tuning.
    :param best_models: models selected by EDBrain method.
    :param workloads: workload list for each database.
    :param db_name: name of db in config.
    :param db_num: number of db in config.
    :param query_candidate: query candidate of benchmark.
    :return: total workload running time.
    """
    start = time.perf_counter()
    for i in range(db_num):
        conn = sqlite3.connect(f"{db_name}{i}.db")
        cursor = conn.cursor()
        for model in best_models:
            if model.db == i:
                cursor.execute(f"PRAGMA cache_size=-{int(model.init_cost * 1024)}")
        for query_num in workloads[i]:
            cursor.execute(query_candidate[query_num])
            cursor.fetchall()
        cursor.close()
        conn.close()
    end = time.perf_counter()
    total_time = end - start
    return total_time


