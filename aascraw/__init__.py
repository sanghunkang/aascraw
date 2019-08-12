from .deliverer import Deliverer

from lxml import etree
from lxml import html

from io import StringIO


def build_xpath(prefix, element, child_index):
    # tag_name = element.tag
    selector = f"[{child_index}]"
    for attrib_name, attrib_value in element.attrib.items():
        selector = selector + f"[@{attrib_name}='{attrib_value}']"

    xpath = f"{prefix}/{element.tag}{selector}"
    
    # print(elements[0].attrib)
    return xpath

def update_prev_tag_counts(tag_name, prev_tag_counts):
    if tag_name in prev_tag_counts:
        prev_tag_counts[tag_name] += 1
    else:
        prev_tag_counts[tag_name] = 1
    return prev_tag_counts

def find_all_xpaths(preceding_xpath, element, child_index):
    prefix_xpath = build_xpath(preceding_xpath, element, child_index)
    xpaths = [prefix_xpath]
    children = element.getchildren()

    if len(children) > 0:
        prev_tag_counts = {}
        for child in children:
            prev_tag_counts = update_prev_tag_counts(child.tag, prev_tag_counts)
            # prefix_xpath =  prefix_xpath #build_xpath(preceding_xpath, element.tag, i+1)
            xpaths =  xpaths + find_all_xpaths(prefix_xpath, child, prev_tag_counts[child.tag])
    return xpaths


class Filterer():
    def __init__(self):
        super().__init__()

        self.new_action_default_rank = 0
        self.sum_rank = 0
        self.actions = {
            #XPath to locate an element: rank
        }

    def __sample_action(self):
        return self.actions.keys()

    def load_page(self, action_taken, page):
        self.deliverer_action = action_taken
        self.page = page
        self.tree = html.fromstring(self.page)

    def run_page(self):
        # Locate element
        actions_to_execute = self.__sample_action()
        results = []
        for action_to_execute in actions_to_execute:
            try:
                elements = self.tree.xpath(action_to_execute)
                print(action_to_execute)
                print(elements[0].attrib)
                content = etree.tostring(elements[0], pretty_print=True, encoding="UTF-8").decode("utf-8")
                results.append([self.deliverer_action, action_to_execute, content])
                print(content)
            except etree.XPathEvalError:
                print("Invalid xpath")
        return results
    
    def update_action_space(self):
        print("This function will look for selector sequences")

        xpaths = find_all_xpaths("", self.tree, 1)
        for xpath in xpaths:
            if xpath not in self.actions:
                self.actions[xpath] = self.new_action_default_rank
        
        
        


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
        self.kernels = []
        self.task_log = [
            # action_master, action_slave, consistent_features, variant_features, rank_delta
        
            ]
        self.results = [] 
        # action_master, action_slave, consistent_features, variant_features, rank_delta

    def __calculate_rank(self, text):
        rank = 0
        for kernel in self.kernels:
            rank += kernel(text)
        return rank

    def add_kernel(self, kernel):
        if False: # SAFETY CHECK FOR KERNEL FUNCTION
            raise Exception
        else:
            self.kernels.append(kernel)
        

    def ingest(self, results):
        # Evaluate rank
        for result in results:
            # calculate_contrib_to_consistency
            # caclulate_contrib_to_variety
            rank = self.__calculate_rank(result[2])
            self.results.append(result + [rank])    
        
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