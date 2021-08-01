/*============================================================================*/
/*                        I BS SOFTWARE GROUP                                 */
/*============================================================================*/
/*                        OBJECT SPECIFICATION                                */
/*============================================================================*/
/*!
 * $Source: PLAST_DBCParser.h $
 * $Author: Mancas, Andrei04 (uidv4966) $
 */
/*============================================================================*/
/* DESCRIPTION :                                                              */
/** \file
    PLAST DBC  module header.
 */
/*============================================================================*/
/* COPYRIGHT (C) CONTINENTAL AUTOMOTIVE 2014                                  */
/* AUTOMOTIVE GROUP, Interior Division, Body and Security                     */
/* ALL RIGHTS RESERVED                                                        */
/*                                                                            */
/* The reproduction, transmission, or use of this document or its content is  */
/* not permitted without express written authority. Offenders will be liable  */
/* for damages.                                                               */
/* All rights, including rights created by patent grant or registration of a  */
/* utility model or design, are reserved.                                     */
/*                                                                            */

#ifndef PLAST_DBC_H
#define PLAST_DBC_H

/* Includes */
/*============================================================================*/

#define USE_DBC_SWATT_ERROR_HANDLER


#include "PLAST_Common.h"

/* Constants and types */
/*============================================================================*/
typedef PyObject* PLAST_DBCParser;
typedef PyObject* PLAST_CANMessage;

enum SWATT_DBC_ERROR_HANDLING_BEHAVIOR
{

    /** generate fatal error and stop execution */
    DBC_SWATT_HALT_IF_ANY_ERROR,

    /** generate fatal error and stop execution if calling method with a null objecct */
    DBC_SWATT_HALT_IF_NOT_INITIALIZED,

    /** do not generate fatal error, allow test skip instead of failure */
    DBC_SWATT_HALT_NONE
};

enum SWATT_DBC_ERROR_CODE
{
    /** success */
    DBC_E_OK_SWATT,
    /**not initialized */
    DBC_E_NOT_INITIALIZED_SWATT,
    /** general failure  */
    DBC_E_FAILED_SWATT
};

/* Type definitions for interface functions */
typedef int (*Type_SWATT_DBC_FNC_outputdbcparser_string)(PLAST_DBCParser*,char*);
typedef int (*Type_SWATT_DBC_FNC_dbcparser_string_outputcanmdbc)(PLAST_DBCParser,char*,PLAST_CANMessage*);
typedef int (*Type_SWATT_DBC_FNC_canmdbc_simple)(PLAST_CANMessage);
typedef int (*Type_SWATT_DBC_FNC_canmdbc_string_string)(PLAST_CANMessage,char*,char*);
typedef int (*Type_SWATT_DBC_FNC_enum)(enum SWATT_DBC_ERROR_HANDLING_BEHAVIOR);


struct DBC_api
{
        /**
         * Instantiates a new dbc parser
         * \param output  PLAST_DBCParser* dbcParser object
         * \param char* dbcFile
         * \return int, value DBC_E_OK_SWATT in case of success, otherwise error (DBC_E_FAILED_SWATT)
         */
        Type_SWATT_DBC_FNC_outputdbcparser_string getDBCParser;

        /**
         * Identifies the message with 'mdbcName' and initializes the corresponding data fields
         * \param PLAST_DBCParser dbcParser
         * \param char*  mdbcName
         * \param output PLAST_CANMessage* canMessage
         * \return int, value DBC_E_OK_SWATT in case of success, otherwise error (DBC_E_FAILED_SWATT)
         */
        Type_SWATT_DBC_FNC_dbcparser_string_outputcanmdbc getCANMessage;

        /**
         * Returns the value of the signal.
         * \param  PLAST_CANMessage canMessage
         * \param  char* signalName = the name of the signal whose value we want to return
         * \param char* signalValue = the value of the signal
         * \return int, value DBC_E_OK_SWATT in case of success, otherwise error (DBC_E_FAILED_SWATT)
         */
        Type_SWATT_DBC_FNC_canmdbc_string_string getSignalValue;

        /**
         * Sets the value of the signal 'signalName' to 'value'. Returns the updated value of the message data
         * \param  PLAST_CANMessage canMessage
         * \param char* signalName = the name of the signal whose value we want to change
         * \param char* signalValue = the value of the signal whose value we want to change (hex formatted)
         * \return int, value DBC_E_OK_SWATT in case of success, otherwise error (DBC_E_FAILED_SWATT)
         */

        Type_SWATT_DBC_FNC_canmdbc_string_string setSignalValue;

        /**
         * Starts sending a CAN message using a thread
         * \param  PLAST_CANMessage canMessage
         * \return int, value DBC_E_OK_SWATT in case of success, otherwise error (DBC_E_FAILED_SWATT)
         */
        Type_SWATT_DBC_FNC_canmdbc_simple startSending;

        /**
         * Stops sending the CAN message
         * \param  PLAST_CANMessage canMessage
         * \return int, value DBC_E_OK_SWATT in case of success, otherwise error (DBC_E_FAILED_SWATT)
         */
        Type_SWATT_DBC_FNC_canmdbc_simple stopSending;
        /**
         * set the dbc parser error handling behavior
         * \param SWATT_DBC_ERROR_HANDLING_BEHAVIOR behavior - error handling behavior
         * \return int, value DBC_E_OK_SWATT in case of success, otherwise error (DBC_E_FAILED_SWATT)
         */
        Type_SWATT_DBC_FNC_enum setErrorHandlerBehaviour;
};


/**
    Structure for the dbc parser interface instance
 */
struct PLAST_DBCParser_class
{
        const char* file;
        unsigned int line;
        enum SWATT_DBC_ERROR_HANDLING_BEHAVIOR errorHandlingBehaviorOption;
        struct DBC_api dbc_api;
};


/* Exported Variables */
/*============================================================================*/
extern struct PLAST_DBCParser_class PLAST_DBCParser_instance ;

#define dbc (PLAST_DBCParser_instance.file=__FILE__, PLAST_DBCParser_instance.line=__LINE__,&PLAST_DBCParser_instance)->dbc_api

/* Exported functions prototypes */
/*============================================================================*/
#ifdef __CDT_PARSER__
#define SWATT_DBC_INLINE inline
#else
#define SWATT_DBC_INLINE static __attribute__((always_inline))
#endif




SWATT_DBC_INLINE void ZSWATT_DBC_ErrorHandlingBehavior(enum SWATT_DBC_ERROR_CODE err_code);
SWATT_DBC_INLINE void ZSWATT_DBC_ErrorHandlingBehavior(enum SWATT_DBC_ERROR_CODE err_code)
{
#ifdef USE_DBC_SWATT_ERROR_HANDLER
    SWATT_number_of_assertions_executed++;
    if (DBC_E_OK_SWATT == err_code)
    {
        return;
    }
    SWATT_number_of_assertions_failed++;
    switch (PLAST_DBCParser_instance.errorHandlingBehaviorOption)
    {
        case DBC_SWATT_HALT_NONE:
            break;
        case DBC_SWATT_HALT_IF_NOT_INITIALIZED:
            if (err_code == DBC_E_NOT_INITIALIZED_SWATT )
            {
                SWATT_abort_executable("ERROR: Fatal dbc parser error");
            }
            break;
        case DBC_SWATT_HALT_IF_ANY_ERROR:
            SWATT_abort_executable("ERROR: Fatal dbc parser error");
            break;
        default:
            break;
    }
#endif
}

extern void PLAST_DBCParser_Init(void);
extern void PLAST_DBCParser_DummyInit(void);

#endif  /* Notice: the file ends with a blank new line to avoid compiler warnings */

