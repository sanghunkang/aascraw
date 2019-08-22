from aascraw import Deliverer, Filterer, Storage
from aascraw import kernels
from aascraw.cache import Cache

from aascraw.kernels_src.kernels import rank_tuple_vicinity

# Initial setup
# Define desired schema for collected data. 
sample_data= [("some moderately long text about something", "someones name", "year-month-date", "XXXXX")]

# Define storage variables and insert the sample to the storage
storage = Storage(schema_length=4, consistency_embedding_length=2, use_default_kernels=False)
storage.add_sample_data(sample_data, real_data=False)

# Add elementwise kernels
for i in range(4):
    storage.add_element_kernel(kernels.rank_content_variance, i)
    storage.add_element_kernel(kernels.rank_content_length, i)

# Add tuplewise kernels
storage.add_tuple_kernel(kernels.rank_tuple_consistency)
storage.add_tuple_kernel(rank_tuple_vicinity)
# storage.add_tuple_kernel(kernels.rank_tuple_vicinity)

TEST_URL = "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=101&oid=025&aid=0002928205"
# TEST_URL = "https://www.coupang.com/vp/products/25207211?itemId=97938090&vendorItemId=4162978715&q=%EC%88%98%EC%97%BC&itemsCount=36&searchId=be59377c412c4886811eb899ee6be14d&rank=5"
# deliverer = Deliverer(TEST_URL) 
filterer = Filterer()
cache = Cache("cache.json")

rank_delta_deliverer = []
rank_delta_filterer = []

# Exploration step
for i in range(1):
    # Deliverer actions
    # action_taken = deliverer.proceed()
    # page = deliverer.get_page()    
    # cache.add(action_taken, page)
    # cache.save()

    action_taken, page = cache.get() # dev

    # Filterer actions
    filterer.load_page(action_taken, page)              
    filterer.update_action_space()             
    data = filterer.run_page()

    # Calculate reward
    storage.evaluate_results(data)
    
    # # Update policy
    # for record in storage.records:
    #     print(record)
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
