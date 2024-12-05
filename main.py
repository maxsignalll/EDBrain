"""
Main.
"""
import os

from gen_models import *
from cost import *
from evaluation import *
import configparser
import reward_cache
import sqlite3
import zipfile
import shutil
import test_models


def data_preparation(pre_db_name, gen_db_num):
    """
    prepare db for test.
    :param pre_db_name: db name in config.
    :param gen_db_num: number of db in config.
    """
    # import database from .sql scripts.
    if os.path.exists(f"{pre_db_name}0.db"):
        return
    conn = sqlite3.connect(f"{pre_db_name}0.db")
    cursor = conn.cursor()

    if not os.path.exists("data/data_sql/ORDER_LINE.sql"):
        with zipfile.ZipFile("data/data_sql/ORDER_LINE.zip", 'r') as zip_ref:
            zip_ref.extractall("./data/data_sql/")
    if not os.path.exists("data/data_sql/STOCK.sql"):
        with zipfile.ZipFile("data/data_sql/STOCK.zip", 'r') as zip_ref:
            zip_ref.extractall("./data/data_sql/")

    for root, dirs, files in os.walk("./data/"):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith(".sql"):
                with open(file_path, "r", encoding="utf8") as script_f:
                    script = script_f.read()
                    cursor.execute(script)

    for root, dirs, files in os.walk("./data/data_sql/"):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith(".sql"):
                with open(file_path, "r", encoding="utf8") as script_f:
                    script = script_f.read()
                    cursor.execute(script)
    cursor.close()
    conn.commit()
    conn.close()

    # copy databases.
    for i in range(gen_db_num-1):
        shutil.copy(f"{pre_db_name}{i}.db", f"{pre_db_name}{i+1}.db")


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
    db_name = parser.get('edbrain', 'db_name')
    print("Preparing data...")
    data_preparation(db_name, db_num)
    print("Done.")
    print("Generating models for test.")
    # generate models, based on workload replay for reward calculation.
    all_models = gen_models(db_num=db_num, one_repeat=one_repeat, query_num=len(table_size),
                            query_list=query_list, table_size=table_size, db_name=db_name)
    print("Cost calculation.")
    # cost calculation.
    mu_list = calculate_mu(all_models, table_size)
    cost_models = cost_calculation(all_models, mu_list, max_memory)
    print("Model evaluation.")
    # evaluation.
    best_models = evaluation(cost_models, max_memory)
    # write reward cache.
    print("Write reward cache.")
    global reward_cache
    reward_cache.model_cache.write("reward_cache.txt")
    # test model.
    workloads = gen_test_workload(best_models, 0.6, len(query_list), 100, db_num)
    test_models.test_model(workloads, db_name, db_num, query_list, best_models)





