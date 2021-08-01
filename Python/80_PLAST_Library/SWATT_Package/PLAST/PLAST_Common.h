#ifndef PLAST_COMMON_H
#define PLAST_COMMON_H


#include "ctester.h"
#include "Python.h"
#include "windows.h"
#include "swatt_Std_Types.h"
#include <string.h>
#include <stdio.h>

//Common function headers

#define HELPER_MODULE "SWATT_Package.Helper"

#define   OK 0
#define N_OK 1

enum PLAST_BASIC_TYPE_IDS
{
    TYPE_ID_PLAST_UINT8,
    TYPE_ID_PLAST_SINT8,
    TYPE_ID_PLAST_UINT16,
    TYPE_ID_PLAST_SINT16,
    TYPE_ID_PLAST_UINT32,
    TYPE_ID_PLAST_SINT32,
    TYPE_ID_PLAST_UINT64,
    TYPE_ID_PLAST_SINT64,
    TYPE_ID_PLAST_DOUBLE
};

extern PyObject* PLAST_loadModule(char* moduleName);
extern PyObject* PLAST_getDictionary(PyObject* module, char* function);
extern PyObject* argumen(unsigned int line, const char* filename);
extern int PLAST_sleep(double delay);
#endif
