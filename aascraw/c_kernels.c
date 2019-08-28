#include <stdio.h>
#include <signal.h>
// #include "iostream"
// #include <vector> 
// using namespace std; 


// float rank_tuple_vicinity(char **xpath_set)
int rank_tuple_vicinity(char **xpath_set)
{
    // DO I REALLY NEED VECTOR, OR IS IT OKAY WITH STRING ARRAYS?
    int pos = 0;
    int numer = 0;
    int denom = 0;
    
    static char *xxpath_set= { "A", "B", "C", NULL };

    int len_xpathSet = 0;
    while (xxpath_set[len_xpathSet] != NULL)
    {
        len_xpathSet++;
    }

    // while (xpath_set[len_xpathSet] != NULL)
    // {
    //     len_xpathSet++;
    // }

    return len_xpathSet;
    // while (pos < xpath_set[0].size()) 
    // while (pos < sizeof(xpath_set[0])/sizeof(char))
    // {

        // Filling in a vertical slice
        // int vertical_slice[sizeof(xpath_set[0])] = {};
        // for (int i=0; i < sizeof(xpath_set[0]); i++) 
        // {
        //     if (pos < sizeof(xpath_set[i]))
        //     {
        //         vertical_slice[i] = xpath_set[i][pos];
        //     }
            
        // }

        // Calculate the numerator value
        // int matching_score = 1;
        // for (int i=0; i < sizeof(xpath_set[0]); i++)
        // {
        //     int temp_matching_score = 1;
        //     char c = vertical_slice[i];
        //     for (int j=0; j < sizeof(xpath_set[0]); j++)
        //     {
        //         if (c == vertical_slice[j])
        //         {
        //             temp_matching_score++;
        //         }
        //     }
            
        //     if (matching_score < temp_matching_score)
        //     {
        //         matching_score = temp_matching_score;
        //     }
        // }

        //     print(vertical_slice)
        // numer += matching_score;
        // numer += 1;
        // denom += sizeof(xpath_set)/sizeof(char*); // MAYBE ADD ONLY WHEN TRUE
        
        // pos ++;
    // }        
    // return (float)numer/(float)denom; // TYPE CONVERSION!
    // return 1.0;
}
