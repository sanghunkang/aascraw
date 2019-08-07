class Agent():
    def __init__(self):
        
        self.actions = {
            # action_key: [action_value, action_rank]
        }

    def update_action_space(self):
        raise NotImplementedError

    def update_policy(self, rank_deltas):
        for rank_delta in rank_deltas:
            action_key = rank_delta[0]
            action_value = rank_delta[1]
            action_rank = rank_delta[2]
            if action_key in self.actions:
                self.actions[action_key][1] += action_rank
            else:
                self.actions[action_key] = [action_value, action_rank]

class Master(Agent):
    def __init__(self):
        super().__init__()

    def proceed(self):
        pass

    def update_action_space(self):
        print("This function will look for possible event triggers and get queries")

    def give_task(self):
        # Trigger event or send request to the server

        # Get the document of currently displayed page
        return 

class Slave(Agent):
    def __init__(self):
        super().__init__()

    def load_task(self, task):
        pass

    def update_action_space(self):
        print("This function will look for selector sequences")

    def run_task(self):
        # Locate element

        return

class Storage():
    def __init__(self):
        self.task_log = [
            # action_master, action_slave, consistent_features, variant_features, rank_delta
        ] 

    def ingest(self, result):
        # This function saves newly collected result
        pass

    def evaluate_data(self):
        # This function evaluates objective functions
        
        # calculate_contrib_to_consistency
        # caclulate_contrib_to_variety
        pass

    def get_rank_delta_master(self):
        # [action_master, rank_delta]
        pass

    def get_rank_delta_slave(self):
        # [action_key, rank_delta]

        pass