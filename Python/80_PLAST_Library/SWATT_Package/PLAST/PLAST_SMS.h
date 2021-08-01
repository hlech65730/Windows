/*============================================================================*/
/*                        I BS SOFTWARE GROUP                                 */
/*============================================================================*/
/*                        OBJECT SPECIFICATION                                */
/*============================================================================*/
/*!
 * $Source: PLAST_SMS.h $
 * $Author: Nitu, Laurentiu (uidv9994) $
 */
/*============================================================================*/
/* DESCRIPTION :                                                              */
/** \file
    PLAST SMS module header.
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

#ifndef PLAST_SMS_H
#define PLAST_SMS_H

/* Includes */
/*============================================================================*/

#define USE_SMS_SWATT_ERROR_HANDLER


#include "PLAST_Common.h"

/* Constants and types */
/*============================================================================*/

enum SWATT_SMS_ERROR_HANDLING_BEHAVIOR
{

    /** generate fatal error and stop execution */
    SMS_SWATT_HALT_IF_ANY_ERROR,

    /** generate fatal error and stop execution if can not connect to SMS */
    SMS_SWATT_HALT_IF_CONNECT,

    /** do not generate fatal error, allow test skip instead of failure */
    SMS_SWATT_HALT_NONE
};

enum SWATT_SMS_ERROR_CODE
{
    /** success */
    SMS_E_OK_SWATT,

    /** Not connected to the SMS */
    SMS_E_NOT_CONNECTED_SWATT,

    /** cannot connect to the SMS */
    SMS_E_CANNOT_CONNECT_SWATT,

    /** general failure  */
    SMS_E_FAILED_SWATT
};

/* Type definitions for interface functions */
typedef int (*Type_SWATT_SMS_FNC_simple)(void);
typedef int (*Type_SWATT_SMS_FNC_int)(int);
typedef int (*Type_SWATT_SMS_FNC_int_int)(int,int);
typedef int (*Type_SWATT_SMS_FNC_int_outputint)(int,int*);
typedef int (*Type_SWATT_SMS_FNC_enum)(enum SWATT_SMS_ERROR_HANDLING_BEHAVIOR);
typedef int (*Type_SWATT_SMS_FNC_int_string)(int,char*);
typedef int (*Type_SWATT_SMS_FNC_int_int_string)(int,int,char*);
typedef int (*Type_SWATT_SMS_FNC_int_outputstring_outstring)(int,char*,char*);
struct SMS_api
{
        /**
         * Connects to the SMS (instantiates the python object)
         * \param void
         * \return int, value SMS_E_OK_SWATT in case of success, otherwise error (SMS_E_CANNOT_CONNECT_SWATT)
         */
        Type_SWATT_SMS_FNC_simple connect;

        /**
         * Sets the position of the device number serNum to newPos
         * \param int serNum - device number
         * \param int newPos - new position
         * \return int, value SMS_E_OK_SWATT in case of success, otherwise error (SMS_E_CANNOT_CONNECT_SWATT)
         */
        Type_SWATT_SMS_FNC_int_int setPos;

        /**
         * Resets the device number serNum to default values
         * \param int serNum - device number
         * \return int, value SMS_E_OK_SWATT in case of success, otherwise error (SMS_E_FAILED_SWATT)
         */
        Type_SWATT_SMS_FNC_int reset;

        /**
         * Increase position
         * \param int serNum - device number
         * \return int, value SMS_E_OK_SWATT in case of success, otherwise error (SMS_E_FAILED_SWATT)
         */

        Type_SWATT_SMS_FNC_int inc;

        /**
         * Decrease position
         * \param int serNum - device number
         * \return int, value SMS_E_OK_SWATT in case of success, otherwise error (SMS_E_FAILED_SWATT)
         */

        Type_SWATT_SMS_FNC_int dec;

        /**
         * Returns the position of the device number serNum
         * \param int serNum - device number
         * \param int* position - read position
         * \return int, value SMS_E_OK_SWATT in case of success, otherwise error (SMS_E_FAILED_SWATT)
         */
        Type_SWATT_SMS_FNC_int_outputint readPos;

        /**
         * Returns the status of hall sensors of the device number serNum
         * \param int serNum - device number
         * \param char* a
         * \param char* b
         * \return int, value SMS_E_OK_SWATT in case of success, otherwise error (SMS_E_FAILED_SWATT)
         */
        Type_SWATT_SMS_FNC_int_outputstring_outstring getHallState;

        /**
         * Sets the status of hall sensors of the device number serNum
         * \param int serNum - device number
         * \param char* string
         * \return int, value SMS_E_OK_SWATT in case of success, otherwise error (SMS_E_FAILED_SWATT)
         */
        Type_SWATT_SMS_FNC_int_string setHallErr;

        /**
         * Blocking occours if the specified position is reached
         * \param int serNum - device number
         * \param int blockPos - new position
         * \param string blocktype
         * \return int, value SMS_E_OK_SWATT in case of success, otherwise error (SMS_E_FAILED_SWATT)
         */
        Type_SWATT_SMS_FNC_int_int_string setBlock;

        /**
         * Pinching will be triggered if the specified position is reached
         * \param int serNum - device number
         * \param int pinchPos - new position
         * \param string pinchType
         * \return int, value SMS_E_OK_SWATT in case of success, otherwise error (SMS_E_FAILED_SWATT)
         */
        Type_SWATT_SMS_FNC_int_int_string setPinch;

        /**
         * set SMS error handling behavior
         * \param SWATT_SMS_ERROR_HANDLING_BEHAVIOR behavior - error handling behavior
         * \return int, value SMS_E_OK_SWATT in case of success, otherwise error (SMS_E_FAILED_SWATT)
         */
        Type_SWATT_SMS_FNC_enum setErrorHandlerBehaviour;


};


/**
    Structure for the power source interface instance
 */
struct PLAST_SMS_class
{
        const char* file;
        unsigned int line;
        enum SWATT_SMS_ERROR_HANDLING_BEHAVIOR errorHandlingBehaviorOption;
        struct SMS_api sms_api;
};


/* Exported Variables */
/*============================================================================*/
extern struct PLAST_SMS_class PLAST_SMS_instance ;

#define sms (PLAST_SMS_instance.file=__FILE__, PLAST_SMS_instance.line=__LINE__,&PLAST_SMS_instance)->sms_api

/* Exported functions prototypes */
/*============================================================================*/
#ifdef __CDT_PARSER__
#define SWATT_SMS_INLINE inline
#else
#define SWATT_SMS_INLINE static __attribute__((always_inline))
#endif




SWATT_SMS_INLINE void ZSWATT_SMS_ErrorHandlingBehavior(enum SWATT_SMS_ERROR_CODE err_code);
SWATT_SMS_INLINE void ZSWATT_SMS_ErrorHandlingBehavior(enum SWATT_SMS_ERROR_CODE err_code)
{
#ifdef USE_SMS_SWATT_ERROR_HANDLER
    SWATT_number_of_assertions_executed++;
    if (SMS_E_OK_SWATT == err_code)
    {
        return;
    }
    //TODO make this work
    SWATT_number_of_assertions_failed++;
    switch (PLAST_SMS_instance.errorHandlingBehaviorOption)
    {
        case SMS_SWATT_HALT_NONE:
            break;
        case SMS_SWATT_HALT_IF_CONNECT:
            if ((err_code == SMS_E_CANNOT_CONNECT_SWATT) || (err_code == SMS_E_NOT_CONNECTED_SWATT) )
            {
                SWATT_abort_executable("ERROR: Fatal SMS error");
            }
            break;
        case SMS_SWATT_HALT_IF_ANY_ERROR:
            SWATT_abort_executable("ERROR: Fatal SMS error");
            break;
        default:
            break;
    }
#endif
}

extern void PLAST_SMS_Init(void);
extern void PLAST_SMS_DummyInit(void);

#endif  /* Notice: the file ends with a blank new line to avoid compiler warnings */

