#     reinforcement
#         objective = minimise structure variance and maximise contents variance
#             minimise structure variance
#             if addition to the community spoils the structure more than the tolerance level, we reject it.
class Storage():
    def __init__(self):
        self.kernels = []
        self.records = [] 
        # action_master, action_slave, consistent_features, variant_features, rank_delta

    def __calculate_rank(self, text):
        rank = 0
        for kernel in self.kernels:
            rank += kernel(text)
        #             a set of elements

        # if a con
        #   coeff*xpath + coeff*tag_types + coeff*classes + coeff*id
        # -> this is to ensure that a coe

        # in an agent - state fashion

        return rank


    # Methods for setup
    def add_sample_data(self, sample_data, real_data = False)
        for sample_record in sample_data:
            self.records.append(["SAMPLE", "SAMPLE", sample_record, 1]) # THE HIGHEST RANK AVAILABLE

    def add_kernel(self, kernel):
        if False: # SAFETY CHECK FOR KERNEL FUNCTION
            raise Exception
        else:
            self.kernels.append(kernel)
        
    # Methods for exploration
    def evaluate_results(self, results, will_save=True):
        # Evaluate rank
        for result in results:
            # calculate_contrib_to_consistency
            # caclulate_contrib_to_variety
            rank = self.__calculate_rank(result[2])
            if will_save == True:
                self.records.append(result + [rank])    
        
    def get_rank_delta(self):
        # [action_master, rank_delta]
        return [], []