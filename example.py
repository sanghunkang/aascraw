from aascraw import Deliverer, Filterer, Storage



deliverer = Deliverer() 
filterer = Filterer()
storage = Storage()

rank_delta_deliverer = []
rank_delta_filterer = []

# Exploration step
for i in range(1):
    deliverer.proceed()
    deliverer.update_action_space() #
    deliverer.update_policy(rank_delta_deliverer) #
    task = deliverer.give_task()
    
    filterer.load_task(task)                   # 
    filterer.update_action_space()             #
    filterer.update_policy(rank_delta_filterer)         #
    data = filterer.run_task()

    storage.ingest(data)
    storage.evaluate_data()
    rank_delta_deliverer, rank_delta_filterer = storage.get_rank_delta()
    
# Exploitation step
for i in range(100):
    deliverer.proceed()            # move on to the next page
    task = deliverer.give_task()   
    
    filterer.load_task(task)
    data = filterer.run_task()     # locate elements which contain desired information 

    storage.ingest(data)        # save the data at located elements
