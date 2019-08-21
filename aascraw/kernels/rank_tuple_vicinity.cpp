#include <Python.h>
#include <vector> 
using namespace std; 

float rank_tuple_vicinity(vector<string> xpath_set)
{
    // DO I REALLY NEED VECTOR, OR IS IT OKAY WITH STRING ARRAYS?
    int pos = 0;
    int numer = 0;
    int denom = 0;

    while (pos < xpath_set[0].size()) 
    {

        // Filling in a vertical slice
        int vertical_slice[xpath_set.size()] = {};
        for (int i=0; i++; i < xpath_set.size()) 
        {
            if (pos < xpath_set[i][0].size())
            {
                vertical_slice[i] = xpath_set[i][pos];
            }
            
        }

        // Calculate the numerator value
        int matching_score = 1;
        for (int i=0; i++; i < xpath_set.size())
        {
            int temp_matching_score = 1;
            char c = vertical_slice[i]
            for (int j=0; j++; j < xpath_set.size())
            {
                if (c == vertical_slice[j])
                {
                    temp_matching_score++;
                }
            }
            
            if (matching_score < temp_matchin_score)
            {
                matching_score = temp_matching_score;
            }
        }

        //     print(vertical_slice)
        numer += matching_score;
        denom += xpath_set[0].size(); // MAYBE ADD ONLY WHEN TRUE
        
        pos ++;
    }        
    return (float)numer/(float)denom; // TYPE CONVERSION!
}
