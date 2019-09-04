
// # def rank_tuple_vicinity(xpath_set, existing_records):
// #     # I MIGHT HAVE TO CONSIDER IMPLEMETING THIS PART WITH CPP
// #     rank = 0
    
    
// #     # print(xpath_set)
// #     pos = 0
// #     numer = 0
// #     denom = 0
// #     max_xpath = 0
// #     # reduce(lambda x1, x2: max(len(x1), len(x2)), xpath_set)
// #     i = 0
// #     while i < len(xpath_set):
// #         max_xpath = max(len(xpath_set[i]["filterer_action"]), max_xpath)
// #         i += 1

// #     while pos < max_xpath: #len(xpath_set[0]["filterer_action"]):
// #         vertical_slice = [None]*len(xpath_set)

// #         i = 0
// #         while i < len(xpath_set):
// #             if pos < len(xpath_set[i]["filterer_action"]):
// #                 vertical_slice[i] = xpath_set[i]["filterer_action"][pos]
// #             denom += 1 # MAYBE ADD ONLY WHEN TRUE
// #             i += 1

// #         matching_score = 1 # Minimum
// #         i = 0
// #         while i < len(xpath_set):
// #             temp_matching_score = 1
// #             c = vertical_slice[i]
// #             j = 0
// #             while j < len(xpath_set):
// #                 if i!= j and c == vertical_slice[j]: # I THINK THIS OPERATION IS REDUNDANT
// #                     temp_matching_score += 1
// #                 j += 1

// #             if matching_score < temp_matching_score:
// #                 matching_score = temp_matching_score
// #             i += 1
        
// #         # print(vertical_slice)
// #         numer += matching_score
// #         pos += 1
        
// #     # for xpath in xpath_set:
// #     #     print(xpath["filterer_action"][:100])

// #     print("Ranking vicinity", numer/denom)
// #     return rank

