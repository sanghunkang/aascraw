#include <stdio.h> 


float rank_tuple_vicinity(char **xpath_set)
{
    // float xpath_set_length = (float)sizeof(xpath_set);
    int numer = 0;
    int denom = 0;
    
    int xpath_set_length = 0;
    while (*xpath_set != NULL) // Or just sizeof implementation?
    {
        xpath_set_length += 1;
        xpath_set++;
    }
        
    
    int pos = 0;
    while (pos < xpath_set_length)
    {
        char vertical_slice[xpath_set_length]; // = xpa [None]*len(xpath_set);
        pos++;
    }

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

    // return 1.0;
    return xpath_set_length;
}





