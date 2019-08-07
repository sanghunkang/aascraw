from aascraw import Master, Slave, Storage



master = Master() 
slave = Slave()
storage = Storage()

rank_delta = None
for i in range(100):
    master.update_policy(rank_delta) #
    slave.update_policy(rank_delta) #

    task = master.give_task()
    data = slave.run_task(task)

    storage.append(data)
    rank_delta = storage.get_rank_delta()
