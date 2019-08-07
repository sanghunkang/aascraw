class Agent():
    def __init__(self):
        
        self.actions = {
            # action_key: [action_value, action_rank]
        }

    # def __search_action_space(self):
    #     raise NotImplementedError

    def update_policy(self, rank_deltas):
        self.__search_action_space()
        for rank_delta in rank_deltas:
            action_key = rank_delta[0]
            action_value = rank_delta[1]
            action_rank = rank_delta[2]
            if action_key in actions:
                self.actions[action_key][1] += action_rank
            else:
                self.actions[action_key] = [action_value, action_rank]

class Master(Agent):
    def __init__(self):
        super().__init__()

    def __search_action_space(self):
        print("This function will look for possible event triggers and get queries")

    def give_task(self):
        # Trigger event or send request to the server

        # Get the document of currently displayed page
        return 

class Slave(Agent):
    def __init__(self):
        super().__init__()

    def __search_action_space(self):
        print("This function will look for selector sequences")

    def run_task(self, task):
        # Locate element

        return

class Storage():
    def __init__(self):
        pass     

    def get_rank_delta(self):
        pass