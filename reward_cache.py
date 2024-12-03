

class RewardCacheUnit:
    def __init__(self, table_set, db, table_size, init_reward):
        self.table_set = table_set
        self.table_size = table_size
        self.db = db
        self.init_reward = init_reward


class RewardCache:
    def __init__(self):
        self.cache_map = {}

    def add_cache(self, table_set, db, table_size, init_reward):
        self.cache_map[(db, frozenset(table_set))] = (table_size, init_reward)

    def get_from_path(self, cache_path):
        with open(cache_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                split_line = line.split('\t')
                table_set = set()
                for table in split_line[0].split(","):
                    table_set.add(int(table))
                self.cache_map[(int(split_line[1]), frozenset(table_set))] = (float(split_line[2]), float(split_line[3]))

    def find_cache(self, table_set, db, table_size):
        cache_tuple = self.cache_map.get((db, frozenset(table_set)), None)
        if cache_tuple is not None:
            if abs(cache_tuple[0] - table_size) / table_size > 0.1:
                return -1
            else:
                return cache_tuple[1]
        else:
            return -2

    def write(self, cache_path):
        with open(cache_path, 'w') as f:
            for cache_db, table_set in self.cache_map.keys():
                unit_str = ""
                for table in table_set:
                    unit_str += str(table) + ","
                unit_str = unit_str[:-1]
                unit_str += (f"\t{cache_db}\t{self.cache_map[(cache_db, frozenset(table_set))][0]}"
                             f"\t{self.cache_map[(cache_db, frozenset(table_set))][1]}\n")
                f.write(unit_str)

    def update(self, table_set, db, table_size, init_reward):
        self.cache_map[(db, frozenset(table_set))] = (table_size, init_reward)


model_cache = RewardCache()
model_cache.get_from_path("./reward_cache.txt")
