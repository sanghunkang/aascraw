from aascraw import Deliverer, Filterer, Storage

TEST_URL = "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=101&oid=025&aid=0002928205"

deliverer = Deliverer(TEST_URL) 
filterer = Filterer()
storage = Storage()

rank_delta_deliverer = []
rank_delta_filterer = []

# Exploration step
for i in range(1):
    # Action for agent 1
    deliverer.proceed()
    page = deliverer.get_page()
    

    
    # Action for agent 2
    filterer.load_page(page)                   # 
    filterer.update_action_space()             #
    # data = filterer.run_page()

    # # Calculate reward
    # storage.ingest(data)
    # storage.evaluate_data()
    
    # # Update policy
    # rank_delta_deliverer, rank_delta_filterer = storage.get_rank_delta()
    # deliverer.update_policy(rank_delta_deliverer) #
    # deliverer.update_action_space() #
    # filterer.update_policy(rank_delta_filterer)         #
    
# deliverer.driver.close()

# Exploitation step
# for i in range(100):
#     deliverer.proceed()            # move on to the next page
#     task = deliverer.give_task()   
    
#     filterer.load_task(task)
#     data = filterer.run_task()     # locate elements which contain desired information 

#     storage.ingest(data)        # save the data at located elements
