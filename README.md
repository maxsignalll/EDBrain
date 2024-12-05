# EDBrain
From ICDE paper: **_**EDBrain: Efficient Cache Tuning for Embedded Databases**_**

## How to use:
    python3 ./main.py

During the first run, the database will be initialized. Each database is approximately 350MB. \
Then, the algorithm will output the selected model for each database and, at the end, compare the models with the default method.

## File Structure Overview
/project-root\
├── /data # TPC-C data .sql files to build .db for test.\
├── config.ini  # Config file of test. \
├── cost.py  # Calculate cost of each model and proportion of each db. \
├── evaluation.py  # Evaluate models and select one best for each db. \
├── gen_models.py  # Generate models instead of identification in workload. \
├── main.py  # Main function of test. \
├── reward.py  # Calculate exact reward by workload replay and reward cache. \
├── reward_cache.py  # Reward cache of models. \
├── reward_cache.txt  # Reward cache file. \
├── test_models.txt  # Test default and EDBrain by generated workload. \
└── tpcc.txt  # All queries in TPC-C benchmark for test. 
