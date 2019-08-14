from aascraw import Deliverer, Filterer, Storage
import kernels

TEST_URL = "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=101&oid=025&aid=0002928205"


# - initial setup
#     - 
#         - crawled data. maybe I will insert it directly to database
#         - xpaths sorted by ran

#define desired schema for collected data. 
sample_data= [("some moderately long text about something", "someones name", "year-month-date", "XXXXX")]

# define storage variables and insert the sample to the storage
storage = Storage()
storage.add_sample_data(sample_data, real_data = False)
storage.add_kernel(kernels.rank_tuple_consistency)
storage.add_kernel(kernels.rank_content_variance)

deliverer = Deliverer(TEST_URL) 
filterer = Filterer()

rank_delta_deliverer = []
rank_delta_filterer = []

# Exploration step
for i in range(1):
    # Action for agent 1
    action_taken = deliverer.proceed()
    page = deliverer.get_page()
    
    # Action for agent 2
    filterer.load_page(action_taken, page)              
    filterer.update_action_space()             
    data = filterer.run_page()

    # Calculate reward
    storage.evaluate_results(data)
    
    # # Update policy
    # rank_delta_deliverer, rank_delta_filterer = storage.get_rank_delta()
    # deliverer.update_policy(rank_delta_deliverer) #
    # deliverer.update_action_space() #
    # filterer.update_policy(rank_delta_filterer)         #
    
# deliverer.driver.close()

# Exploitation step
# ... or after sufficient amount of exploration, we compile state-acion matrix into a procedural codes and execute exploitation.

# for i in range(100):
#     deliverer.proceed()            # move on to the next page
#     task = deliverer.give_task()   
    
#     filterer.load_task(task)
#     data = filterer.run_task()     # locate elements which contain desired information 

#     storage.ingest(data)        # save the data at located elements
