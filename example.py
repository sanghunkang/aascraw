from aascraw import Master, Slave, Storage

master = Master() 
slave = Slave()
storage = Storage()

rank_delta = None

# Exploration step
for i in range(100):
    master.proceed()
    master.update_action_space() #
    master.update_policy(rank_delta_slave) #
    task = master.give_task()
    
    slave.load_task(task)
    slave.update_action_space() #
    slave.update_policy(rank_delta) #
    data = slave.run_task()

    storage.ingest(data)
    storage.evaluate_data()
    rank_delta_master = storage.get_rank_delta_master()
    rank_delta_slave = storage.get_rank_delta_slave()
    
# Exploitation step
for i in range(100):
    master.proceed()            # move on to the next page
    task = master.give_task()   
    
    slave.load_task(task)
    data = slave.run_task()     # locate elements which contain desired information 

    storage.ingest(data)        # save the data at located elements
