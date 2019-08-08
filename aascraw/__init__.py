from selenium import webdriver


class Agent():
    def __init__(self):
        self.actions = {# action_key: [action_value, action_rank]
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




def find_all_event_listeners(preceding_xpath, element):
    elements = element.find_elements_by_xpath("./*")
    
    if len(elements) == 0:
        return [f"{preceding_xpath}-{element.tag_name}"]
    else:
        event_listeners = []
        for element in elements:
            print(f"{preceding_xpath}-{element.tag_name}")
            event_listeners =  event_listeners + find_all_event_listeners(f"{preceding_xpath}-{element.tag_name}", element)
        return event_listeners

# Finding hrefs
def find_all_hrefs(element):
    actions = []
    elements = element.find_elements_by_xpath("//a[@href]")
    for element in elements:
        href = element.get_attribute("href")
        actions.append(f"HREF::{href}")
    return actions

TEST_URL = "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=101&oid=025&aid=0002928205"

# Finding get parameters
def find_get_params_candidates(url):
    get_params = {}
    for pair in url.split("?")[1].split("&"):
        get_params[pair.split("=")[0]] = pair.split("=")[1]
    return get_params

class Deliverer(Agent):
    def __init__(self):
        super().__init__()
        self.page = ""
        self.actions = {}
        self.driver = webdriver.Chrome("./chromedriver")

    def __sample_action(self):
        # Pick action in actions space weighted by rank
        # SAMPLING ACTION
        something_selected = self.actions[0]

        action_type = something_selected.split("::")[0]
        action = something_selected.split("::")[1]
        return action_type, action

    def __sort_actions(self):
        self.actions = sorted(self.actions, key=lambda key, rank: rank)

    def proceed(self):
        action_type, action = self.__sample_action()
        
        if action_type == "HREF":
            self.driver.get(action)
        elif action_type == "GET_PARAM":
            self.url = format_url(self.url, action)
            self.driver.get(self.url)
        # elif action_type == "EVENT":
        #     xpath = format_xpath(action)
        #     trigger = format_trigger(action)
        #     self.driver.find_element_by_xpath(xpath).execute(trigger)

        self.page = self.driver.find_element_by_xpath("html") # OTHER WAY TO FIND ROOT NODE

    def update_action_space(self):
        print("This function will look for possible event triggers and get queries")
        
        # find all event listeners
        # find_all_event_listeners(f"{element.tag_name}", element)
        
        # find all hrefs
        for href in find_all_hrefs(element):
            if href not in self.actions:
                self.actions[href] = 0
        
        # find all get candidate -> i.e. next url
        for param in find_get_params_candidates(url):
            if param not in self.actions:
                self.actions[param] = 0

        self.__sort_actions()
        # MAYBE NORMALIZE


    def give_task(self):
        # Trigger event or send request to the server

        # Get the document of currently displayed page
        return self.page

class Filterer(Agent):
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

    def get_rank_delta(self):
        # [action_master, rank_delta]
        return [], []



# def pick_influential_param(get_params):
#     param = ""
#     previous_rank = -1
#     for key, value in get_params.items():
#         current_rank = feature1(value)
#         if previous_rank < current_rank:
#             param = key
#             previous_rank = current_rank
#         elif previous_rank == current_rank:
#             # RANDOMLY SELECT ONE OF TWO
#             pass
#     return param

# def feature1(value):
#     try:
#         int(value)
#         return 1
#     except:
#         return 0




get_params = find_get_params_candidates(TEST_URL)
print(get_params)

# Finding event listeners
# driver = webdriver.Chrome("./chromedriver")
# driver.get(TEST_URL)
# element = driver.find_element_by_xpath("html")
# event_listeners = find_all_event_listeners(f"{element.tag_name}", element)
# print(len(event_listeners))
# driver.close()





# hrefs = find_all_hrefs(element)
# print(len(hrefs))