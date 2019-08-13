def rank_tuple_consistency(new_record, existing_records):
    """
    This function returns an integer which indicates how much the relative sizes of contents is preserved.
    It is 0 if relative sizes of contents are perfectly different from previous records, 
    and it is 1 if relative sizes of contents are at exact average of previous records.
    """
    # - features which contributes to consistency of format
    #     tag types   ~ 100, consider all. there are
    #     attributes  ~ 200, for now, concentrate in most common 5
    #     content types ~ ?
    rank = 0
    return rank

def rank_content_variance(new_record, existing_records):
    """
    This functions measures how much a new record is variant from previously collected records.
    It is 0 if it the new record is exactly the same with one of previously collected records,
    and it is 1 if the new record is completly different from previously collected records.
    """
    rank = 0
    return rank

# how xpath rank is calculated?
# A desired property that

# A function to find xpath rank is defined accordingly.



#     distance between x2v 
#     if within average (+ some buffer) distance -> include to the board
#     else reject

# - features which contributes to variance of contents


# - collect a data get by xpath(s) with highest rank and compare
#     structure remains same and contents are variant: there is a high probability this is what we wanted. We increase the rank of this key
#     otherwise: we deem it as uninteresting. We decrease the rank of this key.
#     (어떤 element를 찾았는데, 이것이 맞으면 수집을 하고, 맞지 않으면 무시한다.)

#     How xpath rank is calculated will be discussed later.

