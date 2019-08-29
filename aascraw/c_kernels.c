#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject * spam_system(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = system(command);
    return PyLong_FromLong(sts);
}

static PyMethodDef SpamMethods[] = {
    
    {"system",  spam_system, METH_VARARGS, "Execute a shell command."},
    
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "spam",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    SpamMethods
};


PyMODINIT_FUNC PyInit_spam(void)
{
    return PyModule_Create(&spammodule);
}


int main(int argc, char *argv[])
{
    wchar_t *program = Py_DecodeLocale(argv[0], NULL);
    if (program == NULL) {
        fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
        exit(1);
    }

    /* Add a built-in module, before Py_Initialize */
    PyImport_AppendInittab("spam", PyInit_spam);

    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(program);

    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Optionally import the module; alternatively,
       import can be deferred until the embedded script
       imports it. */
    PyImport_ImportModule("spam");


    PyMem_RawFree(program);
    return 0;
}


// float rank_tuple_vicinity(char **xpath_set)
// int rank_tuple_vicinity(char **xpath_set)
// {
    // DO I REALLY NEED VECTOR, OR IS IT OKAY WITH STRING ARRAYS?
    // int pos = 0;
    // int numer = 0;
    // int denom = 0;
    
    // static char *xxpath_set= { "A", "B", "C", NULL };

    // int len_xpathSet = 0;
    // while (xxpath_set[len_xpathSet] != NULL)
    // {
    //     len_xpathSet++;
    // }

    // while (xpath_set[len_xpathSet] != NULL)
    // {
    //     len_xpathSet++;
    // }

    // return len_xpathSet;
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
// }
