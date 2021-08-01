#include "ctester.h"
#include "Python.h"

#include "windows.h"

#include "PLAST.h"

void PLAST_Init(void)
{
    /* Stuff we need to be able to load a module not in PYTHONPATH */
    PyObject *path = NULL, *pwd = NULL;

    Py_Finalize();
    //
    //    /* Initialize the Python framework */
    Py_Initialize();
    if (!Py_IsInitialized())
    {
        printf("Error initializing Python interpreter\n");
    }

    /* "module" is in ".", so we need to alter the module search path "." is not in it by default */
    /* Get the current path (this is a list) */
    path = PySys_GetObject("path");
    /* Create a value to add to the list */
    // pwd = PyString_FromString(PLAST_WORKSPACE_LOCATION);
    pwd = PyString_FromString(PLAST_LOCATION);
    /* And add it */
    PyList_Insert(path, 0, pwd);
    /* We don't need that string value anymore, so deref it */
    Py_DECREF(pwd);
}

void Z_SWATT_setup_PLAST(void)
{
    PLAST_Init();

#ifdef ENABLE_PLAST_ALL

    PLAST_PowerSource_Init();
    PLAST_Debugger_Init();
    PLAST_SignalGenerator_Init();
    PLAST_SMS_Init();
    PLAST_DBCParser_Init();
#else

    #ifdef ENABLE_PLAST_POWERSOURCE
        PLAST_PowerSource_Init();
    #else
        PLAST_PowerSource_DummyInit();
    #endif

    #ifdef ENABLE_PLAST_DEBUGGER
        PLAST_Debugger_Init();
    #else
        PLAST_Debugger_DummyInit();
    #endif

    #ifdef ENABLE_PLAST_SIGNALGENERATOR
        PLAST_SignalGenerator_Init();
    #else
        PLAST_SignalGenerator_DummyInit();
    #endif

    #ifdef ENABLE_PLAST_SMS
        PLAST_SMS_Init();
    #else
        PLAST_SMS_DummyInit();
    #endif

    #ifdef ENABLE_PLAST_DBCPARSER
        PLAST_DBCParser_Init();
    #else
        PLAST_DBCParser_DummyInit();
    #endif

#ifdef ENABLE_PLAST_LDFPARSER
    PLAST_LDFParser_Init();
#else
    PLAST_LDFParser_DummyInit();
#endif


#endif

}
