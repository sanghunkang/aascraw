from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
# driver = webdriver.Chrome()



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



# Finding get parameters
def parse_get_params(url):
    get_params = {}
    for pair in url.split("?")[1].split("&"):
        get_params[pair.split("=")[0]] = pair.split("=")[1]
    return get_params

def find_get_params_candidates(url):
    actions = []
    get_params = parse_get_params(url)
    for param_name, param_value in get_params.items():
        try:
            int(value)
            actions.append(f"GET_PARAMS::++>{param_name}")
        except:
            actions.append(f"GET_PARAMS::OTHER_OPERATION>{param_name}")
    return actions


def format_url(url, action):
    operator = action.split(">")[0]
    param = action.split(">")[1]

    get_params = parse_get_params(url)
    param_value = get_params[param]
    
    if operator == "++":
        param_value = f"{int(param_value) + 1}".rjust("0", len(param_value))
    elif operator == "--":
        param_value = f"{int(param_value) - 1}".rjust("0", len(param_value))
    elif operator == "OTHER_OPERATION":
        pass    
    else:
        raise Exception("Update operation undefined")

    return re.sub(r"&" + param + r"=.+", "&", url) + f"&{param}={param_value}"

class Deliverer():
    def __init__(self, entry_point):
        super().__init__()
        
        self.new_action_default_rank = 0
        self.sum_rank = 0 # Just in case
        # self.page = ""
        # self.entry_point = entry_point
        self.actions = {
            f"HREF::{entry_point}": 1
            #"GET_PARAM::operator>param" : 10,
            #"HREF::https://naver.com/?some=get&query=params" : 15
        }
        # self.driver = webdriver.Chrome("./drivers/chromedriver", chrome_options=chrome_options)
        self.driver = webdriver.PhantomJS("./drivers/phantomjs")
        # self.driver.get(entry_point)
        # self.page = self.driver.find_element_by_xpath("html") # OTHER WAY TO FIND ROOT NODE


    def __sample_action(self):
        # Pick action in actions space weighted by rank
        # SAMPLING ACTION
        action_key = list(self.actions.keys())[0]

        # something_selected = self.actions[action_key]

        action_type = action_key.split("::")[0]
        action = action_key.split("::")[1]
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
        return action_type + action

    def get_page(self):
        # Trigger event or send request to the server

        # Get the document of currently displayed page
        return self.driver.execute_script("return document.documentElement.outerHTML;")


    def update_action_space(self):
        print("This function will look for possible event triggers and get queries")
        
        # find all event listeners
        # find_all_event_listeners(f"{element.tag_name}", element)
        
        # find all hrefs
        for href in find_all_hrefs(self.page):
            if href not in self.actions:
                self.actions[href] = self.new_action_default_rank
        
        # find all get candidate -> i.e. next url
        for param in find_get_params_candidates(self.driver.current_url):
            if param not in self.actions:
                self.actions[param] = self.new_action_default_rank


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
        # MAYBE NORMALIZE

    