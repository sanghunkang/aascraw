# - features which contributes to variance of contents


# - collect a data get by xpath(s) with highest rank and compare
#     structure remains same and contents are variant: there is a high probability this is what we wanted. We increase the rank of this key
#     otherwise: we deem it as uninteresting. We decrease the rank of this key.
#     (어떤 element를 찾았는데, 이것이 맞으면 수집을 하고, 맞지 않으면 무시한다.)

#     How xpath rank is calculated will be discussed later.

# Kernels may deal with single element of a result tuple, or the entire tuple itself.

import numpy as np

# I HAVE TO CONSIDER USING DECORATORS
def rank_tuple_consistency(new_record, existing_records, element_id, record_length):
    """
    This function returns an integer which indicates how much the relative sizes of contents is preserved.
    It is 0 if relative sizes of contents are perfectly different from previous records, 
    and it is 1 if relative sizes of contents are at exact average of previous records.
    """
    # - features which contributes to consistency of format
    #     tag types   ~ 100, consider all. there are
    #     attributes  ~ 200, for now, concentrate in most common 5
    #     content types ~ ?
    rank = np.zeros(record_length)
    # print(new_record)
    
    # TAKE LOG TO TAKE INTO ACCOUNT THAT STRUCTURED DATA ARE SHORT, WHEREAS UNSTRUCTURED DATA ARE LENGTHY
    # length_array_existing_records = np.zeros(len(existing_records[0][2]))
    # for existing_record in existing_records:
    #     length_array_existing_records += [np.log(len(element)) for element in existing_record[2]]

    # length_array_existing_records = length_array_existing_records / len(existing_records)
    # length_array_new_record = [np.log(len(element)) for element in new_record[2]]
    
    # print(length_array_existing_records)
    # print(length_array_new_record)


    return rank

def rank_tuple_vicinity(new_record, existing_records):
    rank = 0
    return rank

# Content level kernels
def rank_consistency_by_datatype(new_record, existing_records):
    rank = 0
    # FOR NOW, ONLY STRING, NUMBER, AND DATETIME-LIKE IS CONSIDERED
    for element in new_record:
        element_type = str # Defaults to string
        try:
            int()
        except Error:
            # SOME DATATIME CONVERSION
            pass
        
    # COMPARE MEAN OF VECTORS OF EXISTING RECORDS?

    return rank

def rank_content_variance(new_record, existing_records, element_id, record_length):
    """
    This functions measures how much a new record is variant from previously collected records.
    It is 0 if it the new record is exactly the same with one of previously collected records,
    and it is 1 if the new record is completly different from previously collected records.
    """

    rank = np.zeros(record_length)
    
    # FOR NOW, ANY DIFFERENCE IN CONTENT IS CONSIDERED SIGNIFICANT VARIANCE
    rank[element_id] = 1
    for existing_record in existing_records: # IF existing_record[3]==element_id 
        if existing_record[2] == new_record:
            rank[element_id] = 0
            
    return rank

def rank_content_length(new_record, existing_records, element_id, record_length):
    arr_existing_elements = [np.log(len(record[2])) for record in existing_records if record[3]==element_id]
    
    score_mean_existing_elements = np.mean(arr_existing_elements)
    score_new_record = np.log(len(new_record[2]))
    
    rank = np.zeros(record_length)
    rank[element_id] = np.square(score_new_record - score_mean_existing_elements)
    return rank


# how xpath rank is calculated?
# A desired property that

# A function to find xpath rank is defined accordingly.



#     distance between x2v 
#     if within average (+ some buffer) distance -> include to the board
#     else reject



