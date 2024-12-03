import random
import sqlite3
import time

from model import Model
from reward import obtain_reward


def gen_models(db_num, one_repeat, query_num, query_list, table_size, db_path):
    """
    generate models for test.
    :param db_path: database path.
    :param db_num: number of databases.
    :param one_repeat: number of models for one database.
    :param query_num: number of queries.
    :param query_list: list of queries.
    :param table_size: total table size of a model.
    :return: models for test.
    """
    all_models = []
    if query_num < one_repeat:
        one_repeat = query_num - 1
    for i in range(db_num):
        model_list = []
        for _ in range(one_repeat):  # generate several models for one db.
            one_random = random.randint(1, 10)
            if one_random < 6:  # 1 query model is 0.5, 2 and 3 are 0.25
                one_query_num = random.randint(1, query_num) - 1
                model_set = []
                for model in model_list:
                    table_set = set()
                    for table in model.tables:
                        table_set.add(table)
                    model_set.append(table_set)
                # avoid same model
                while len(model_list) > 0 and {one_query_num} in model_set:
                    one_query_num = random.randint(1, query_num) - 1
                    model_set = []
                    for model in model_list:
                        table_set = set()
                        for table in model.tables:
                            table_set.add(table)
                        model_set.append(table_set)
                rerun_times = random.randint(5, 15)
                one_cost = table_size[one_query_num]
                model = Model(db=i, tables=[one_query_num], cost=one_cost/1024, rerun_times=rerun_times)
                # get reward.
                reward = obtain_reward(model, db_path, query_candidate=query_list)
                model.init_reward = reward
                model_list.append(model)
            else:
                two_or_three = random.randint(1, 10)

                if two_or_three < 6:
                    selected_length = 2
                else:
                    selected_length = 3

                selected_numbers = random.sample(range(0, query_num), selected_length)
                sample_query_list = []
                for num in selected_numbers:
                    sample_query_list.append(query_list[num])
                model_set = []
                for model in model_list:
                    table_set = set()
                    for table in model.tables:
                        table_set.add(table)
                    model_set.append(table_set)
                # avoid same model structure.
                while len(model_list) > 0 and set(selected_numbers) in model_set:
                    selected_numbers = random.sample(range(0, query_num), selected_length)
                    sample_query_list = []
                    for num in selected_numbers:
                        sample_query_list.append(query_list[num])
                    model_set = []
                    for model in model_list:
                        table_set = set()
                        for table in model.tables:
                            table_set.add(table)
                        model_set.append(table_set)
                rerun_times = random.randint(5, 10)
                multi_cost = 0
                for num in selected_numbers:
                    multi_cost += table_size[num]
                # model replay for test.
                model = Model(db=i, tables=selected_numbers, cost=multi_cost/1024, rerun_times=rerun_times)
                reward = obtain_reward(model, db_path, query_candidate=query_list)
                model.init_reward = reward
                model_list.append(model)
        all_models.append(model_list)
    print("All Models:")
    print(all_models)
    print("")
    return all_models


def gen_query_list_from_models(all_models, query_length, query_num):
    """
    generate query list from models for test.
    :param all_models: all models.
    :param query_length: query list length.
    :param query_num: different query candidate for generating.
    :return: query list for test.
    """
    all_query_list = []
    for db_count in range(len(all_models)):
        db_query_routine = []
        for model in all_models[db_count]:
            model_query_list = []
            for _ in range(model[3]):
                model_query_list.extend(model[0])
            db_query_routine.extend(model_query_list)
        while len(db_query_routine) < query_length:
            db_query_routine.append(random.randint(1, query_num) - 1)
        all_query_list.append(db_query_routine)
    return all_query_list


def gen_test_workload(best_models, efficient_rate, query_num, workload_length):
    """
    generate workload list for test based on models.
    :param workload_length: workload list length.
    :param query_num: different query candidate number for generating.
    :param efficient_rate: efficient query rate(queries in models).
    :param best_models: best models for each database.
    :return: workload list for test.
    """
    workload_list = []
    for i in range(len(best_models)):
        model = best_models[i]
        query_list = model[0]
        other_query_list = []
        for x in range(query_num):
            if x not in query_list:
                other_query_list.append(x)
        model_len = int(workload_length * efficient_rate)
        selected_numbers = []
        for _ in range(model_len):
            selected_numbers.extend(random.sample(query_list, 1))
        random_length = workload_length - model_len
        random_numbers = []
        if len(other_query_list) != 0:
            for _ in range(random_length):
                random_numbers.extend(random.sample(other_query_list, 1))
        final_numbers = query_list + selected_numbers + random_numbers
        workload_list.append(final_numbers)
    return workload_list


def test_models(best_models, cost_list, query_routine, query_path, db_path):
    with open(query_path, 'r', encoding='utf8') as f:
        queries = f.readlines()
    query_list = []
    for line in query_routine:
        one_db_query_list = []
        for num in line:
            one_db_query_list.append(queries[int(num)])
        query_list.append(one_db_query_list)
    all_brain = []
    all_default = []
    for _ in range(5):
        brain_list = []
        default_list = []
        for i in range(len(best_models)):
            # 对每一个数据库分别跑，目前来看还不需要并发，只需要不同时使用所有的内存资源即可。
            # 先跑默认方法
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            start_default = time.perf_counter()
            for query in query_list[i]:
                cursor.execute(query)
                cursor.fetchall()
            end_default = time.perf_counter()
            default_time = end_default - start_default
            cursor.close()
            conn.close()
            # 再跑优化方法
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            db_cost = 0
            for table_num in best_models[i][0]:
                db_cost += cost_list[int(table_num)]
            db_cost = int(1.1 * db_cost)
            assert db_cost != 0
            cursor.execute(f'PRAGMA cache_size=-{db_cost};')
            start_brain = time.perf_counter()
            for query in query_list[i]:
                cursor.execute(query)
                cursor.fetchall()
            end_brain = time.perf_counter()
            brain_time = end_brain - start_brain
            cursor.close()
            conn.close()
            brain_list.append(brain_time)
            default_list.append(default_time)
            # print(f"brain time:{brain_time}\tdefault time:{default_time}")
        all_brain.append(brain_list)
        all_default.append(default_list)
    brian_avg = []
    default_avg = []
    for i in range(len(all_brain[0])):
        col_sum_brian = 0
        col_sum_default = 0
        for j in range(len(all_brain)):
            col_sum_brian += all_brain[j][i]
            col_sum_default += all_default[j][i]
        brian_avg.append(col_sum_brian / len(all_brain))
        default_avg.append(col_sum_default / len(all_brain))
    print(f"brain avg time:{brian_avg}\tdefault avg time:{default_avg}\n\n")
