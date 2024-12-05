# EDBrain
From ICDE paper: **_**EDBrain: Efficient Cache Tuning for Embedded Databases**_**

## How to use:
    python3 ./main.py

During the first run, the database will be initialized. Each database is approximately 350MB. \
Then, the algorithm will output the selected model for each database and, at the end, compare the models with the default method.

## File Structure Overview
/project-root\
├── **/data** _# TPC-C data .sql files to build .db for test._\
├── **config.ini**  _# Config file of test._ \
├── **cost.py**  _# Calculate cost of each model and proportion of each db._ \
├── **evaluation.py**  _# Evaluate models and select one best for each db._ \
├── **gen_models.py**  _# Generate models instead of identification in workload._ \
├── **main.py**  _# Main function of test._ \
├── **reward.py**  _# Calculate exact reward by workload replay and reward cache._ \
├── **reward_cache.py**  _# Reward cache of models._ \
├── **reward_cache.txt**  _# Reward cache file._ \
├── **test_models.txt**  _# Test default and EDBrain by generated workload._ \
└── **tpcc.txt**  _# All queries in TPC-C benchmark for test._ 
