#     reinforcement
#         objective = minimise structure variance and maximise contents variance
#             minimise structure variance
#             if addition to the community spoils the structure more than the tolerance level, we reject it.



import numpy as np

# The goal of Storage class is to give rewards to Deliver and Filterer so that they can optimise the selection of
# of xpaths.

class Storage():
    def __init__(self, schema_length, consistency_embedding_length):        
        self.records = [] 
        # [action_deliverer, action_filterer, crawled data, index, rank_delta]

        self.element_kernels = []
        self.tuple_kernels = []
        
        self.__schema_length = schema_length
        self.__consistency_embedding_length = consistency_embedding_length
        self.count = 1

    def __calculate_elementwise_rank(self, records):
        for record in records:
            elementwise_rank = np.zeros(self.__schema_length)
            existing_records = self.__sample_existing_records()
                    
            # Calculate rank based on each element
            for kernel, element_id in self.element_kernels:
                # NOTE MULTIPLY WEIGHT TO KERNEL
                elementwise_rank += kernel(record, existing_records, element_id, self.__schema_length)
            
            # if any(x < 100 for x in elementwise_rank):
            #     print(self.count, elementwise_rank, record[2])
            #     self.count += 1

            record.append(elementwise_rank)
        return records

    def __sample_tuple(self, records):
        # if elementwise_rank < 100:
        #     print(elementwise_rank, record[2])

        # Select candidates for xpath sets.
        # The purpose of this selection is to set contraint of computaional complexity.
        # SORT AND SELECT TOP N ELEMENTS FOR EACH ELEMENT IN ELEMENTWISE_RANK
        sample_size = 10
        tuple_sample = []
        for i in range(self.__schema_length):
            candidates_for_schema_i = sorted(records, key=lambda x: x[3][i])[:sample_size]
            tuple_sample.append(candidates_for_schema_i)
            
        return tuple_sample

    def __calculate_tuplewise_rank(self, record):
        # Calculate rank based on tuple
        # FIND A SET OF XPATHS WHICH BRINGS OUT MOST SIMILAR RANK VECTOR TO SAMPLE
        tuple_rank = np.zeros(self.__consistency_embedding_length)
        existing_records = self.__sample_existing_records()
        for kernel in self.tuple_kernels:
            tuple_rank += kernel(record, existing_records)

        return tuplewise_rank

    def __sample_existing_records(self):
        return self.records

    # Methods for setup
    def add_sample_data(self, sample_data, real_data=False):
        for sample_record in sample_data:
            for element_index, element in enumerate(sample_record):
                self.records.append(["SAMPLE", "SAMPLE", element, element_index, 1]) # THE HIGHEST RANK AVAILABLE

    def add_element_kernel(self, kernel, element_id):
        if False: # NOTE ADD SAFETY CHECK FOR KERNEL FUNCTIONS
            raise Exception
        else:
            self.element_kernels.append((kernel, element_id))
        
    def add_tuple_kernel(self, kernel):
        if False: # NOTE ADD SAFETY CHECK FOR KERNEL FUNCTIONS
            raise Exception
        else:
            self.tuple_kernels.append(kernel)


    # Methods for exploration
    def evaluate_results(self, results, will_save=True):
        # Evaluate rank
        results = [self.__calculate_elementwise_rank(result) for result in results]
        tuple_sample = self.__sample_tuple(results)
        self.__calculate_tuplewise_rank(tuple_sample, results)
            # if will_save==True:
            #     self.records.append(result + [rank])    
        
    def get_rank_delta(self):
        # [action_master, rank_delta]
        return [], []