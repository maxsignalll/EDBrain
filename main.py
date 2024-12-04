"""
Main.
"""
from gen_models import *
from cost import *
from evaluation import *
import configparser
import reward_cache


if __name__ == '__main__':
    parser = configparser.ConfigParser()
    parser.read('config.ini')
    table_size = {0: 66420, 1: 4, 2: 7245, 3: 7382, 4: 80710, 5: 5505, 6: 119488, 7: 1}  # each table size.
    max_memory = int(parser.get('edbrain', 'max_memory'))  # obtain from system or manual setting.
    one_repeat = int(parser.get('edbrain', 'one_repeat'))
    query_path = parser.get('edbrain', 'query_path')
    db_num = int(parser.get('edbrain', 'db_num'))
    with open(query_path, "r") as f:
        query_list = f.readlines()
    db_path = parser.get('edbrain', 'db_path')
    print("Generating models for test.")
    # generate models, based on workload replay for reward calculation.
    all_models = gen_models(db_num=db_num, one_repeat=one_repeat, query_num=len(table_size),
                            query_list=query_list, table_size=table_size, db_path=db_path)
    print("Cost calculation.")
    # cost calculation.
    mu_list = calculate_mu(all_models, table_size)
    cost_models = cost_calculation(all_models, mu_list, max_memory)
    print("Model evaluation.")
    # evaluation.
    best_models = evaluation(cost_models, max_memory)
    # write reward cache.
    global reward_cache
    reward_cache.model_cache.write("reward_cache.txt")



