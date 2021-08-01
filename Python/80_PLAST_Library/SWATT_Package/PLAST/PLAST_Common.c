
#include "ctester.h"
#include "Python.h"
#include "PLAST_Common.h"
#define   OK 0
#define N_OK 1

PyObject* PLAST_loadModule(char* moduleName)
{
    /* The module object */
    PyObject *localLoad = NULL;

    /* Load the module */
    localLoad = PyImport_ImportModule(moduleName);

    /* Check whether we succeeded */
    if(localLoad == NULL)
    {
        /* If not, print the error message and get out of here */
        PyErr_Print();
        PyErr_Clear();
        printf("Failed to initialize \"%s\"\n", moduleName);
    }
    return localLoad;
}


PyObject* PLAST_getDictionary(PyObject* module, char* function)
{
	
    /* Objects we need to get a reference to a function or method */
    PyObject *dict = NULL, *ret = NULL;
	if(NULL!=module){
    /* Get the module's dictionary. */
    dict = PyModule_GetDict(module);

    /* Get the class attribute. */
    ret = PyDict_GetItemString(dict, function);
	}
	
    return ret;
}

PyObject* argumen(unsigned int line, const char* filename)
{
    PyObject *args = NULL;
    args = PyTuple_New(2);
    PyTuple_SetItem(args, 0, Py_BuildValue("i", line));
    PyTuple_SetItem(args, 1, Py_BuildValue("s", filename));

    return args;
}
int PLAST_sleep(double delay){

    char command[50]=" ";

    sprintf(command,"import time; time.sleep(%f)",delay);
    //printf("%s",command);
    if(PyRun_SimpleString(command)!=-1){
            return OK;
    }
    else{
            return N_OK;
    }

}
