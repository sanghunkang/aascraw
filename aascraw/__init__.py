from .deliverer import Deliverer

from lxml import etree
from lxml import html

from io import StringIO





class Filterer():
    def __init__(self):
        super().__init__()

        self.new_action_default_rank = 0
        self.actions = {
            #XPath to locate an element, rank
        }

    def load_page(self, page):
        self.page = page
    

    def run_page(self):
        # Locate element

        return
    


    def update_action_space(self):
        print("This function will look for selector sequences")
        # print(self.page)
        # for xpath in find_all_xpaths(self.page):
        #     if xpath not in self.actions:
        #         self.actions[xpath] = self.new_action_default_rank

        # f = StringIO('<foo><bar></bar></foo>')
        # f = StringIO(self.page)
        # tree = etree.parse(f)


        # >>> broken_html = "<html><head><title>test<body><h1>page title</h3>"
        tree = html.fromstring(self.page)
        # <Element html at 0x2dde650>
        r = tree.xpath('/div')
        print(r)
        len(r)


    def update_policy(self, rank_deltas):
        for rank_delta in rank_deltas:
            # action_key = rank_delta[0]
            # action_rank = rank_delta[1]
            
            # if action_key in self.actions:
            self.actions[rank_delta[0]][1] += rank_delta[1]
            self.sum_rank += rank_delta[1]
            # else:
            #     raise Exception("This case must not exist")

        self.__sort_actions()

    

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




# get_params = find_get_params_candidates(TEST_URL)
# print(get_params)

# Finding event listeners
# driver = webdriver.Chrome("./chromedriver")
# driver.get(TEST_URL)
# element = driver.find_element_by_xpath("html")
# event_listeners = find_all_event_listeners(f"{element.tag_name}", element)
# print(len(event_listeners))
# driver.close()





# hrefs = find_all_hrefs(element)
# print(len(hrefs))