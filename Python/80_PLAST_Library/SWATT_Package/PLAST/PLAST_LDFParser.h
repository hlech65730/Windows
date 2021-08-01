/*============================================================================*/
/*                        I BS SOFTWARE GROUP                                 */
/*============================================================================*/
/*                        OBJECT SPECIFICATION                                */
/*============================================================================*/
/*!
 * $Source: PLAST_LDFParser.h $
 * $Author: Mancas, Andrei04 (uidv4966) $
 */
/*============================================================================*/
/* DESCRIPTION :                                                              */
/** \file
    PLAST LDF  module header.
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

#ifndef PLAST_LDF_H
#define PLAST_LDF_H

/* Includes */
/*============================================================================*/

#define USE_LDF_SWATT_ERROR_HANDLER


#include "PLAST_Common.h"

/* Constants and types */
/*============================================================================*/
typedef PyObject* PLAST_LDFParser;
typedef PyObject* PLAST_LINFrame;
typedef PyObject* PLAST_LINNode;



enum SWATT_LDF_ERROR_HANDLING_BEHAVIOR
{

    /** generate fatal error and stop execution */
    LDF_SWATT_HALT_IF_ANY_ERROR,

    /** generate fatal error and stop execution if calling method with a null objecct */
    LDF_SWATT_HALT_IF_NOT_INITIALIZED,

    /** do not generate fatal error, allow test skip instead of failure */
    LDF_SWATT_HALT_NONE
};

enum SWATT_LDF_ERROR_CODE
{
    /** success */
    LDF_E_OK_SWATT,
    /**not initialized */
    LDF_E_NOT_INITIALIZED_SWATT,
    /** general failure  */
    LDF_E_FAILED_SWATT
};

/* Type definitions for interface functions */
typedef int (*Type_SWATT_LDF_FNC_outputldfparser_string)(PLAST_LDFParser*,char*);
typedef int (*Type_SWATT_LDF_FNC_ldfparser_string_outputlinf)(PLAST_LDFParser,char*,PLAST_LINFrame*);
typedef int (*Type_SWATT_LDF_FNC_ldfparser_string_outputlinnode)(PLAST_LDFParser,char*,PLAST_LINNode*);
typedef int (*Type_SWATT_LDF_FNC_ldfparser_outputlinnode)(PLAST_LDFParser,PLAST_LINNode*);
typedef int (*Type_SWATT_LDF_FNC_linnode_linf)(PLAST_LINNode,PLAST_LINFrame);
typedef int (*Type_SWATT_LDF_FNC_linf_simple)(PLAST_LINFrame);
typedef int (*Type_SWATT_LDF_FNC_linf_string_string)(PLAST_LINFrame,char*,char*);
typedef int (*Type_SWATT_LDF_FNC_linnode_int_outputlinf_outputint)(PLAST_LINNode,int,PLAST_LINFrame*,int*);
typedef int (*Type_SWATT_LDF_FNC_enum)(enum SWATT_LDF_ERROR_HANDLING_BEHAVIOR);



struct LDF_api
{
        /**
         * Instantiates a new ldf parser
         * \param output  PLAST_LDFParser* ldfParser object
         * \param char* ldfFile
         * \return int, value LDF_E_OK_SWATT in case of success, otherwise error (LDF_E_FAILED_SWATT)
         */
        Type_SWATT_LDF_FNC_outputldfparser_string getLDFParser;

        /**
         * Identifies the message with 'mldfName' and initializes the corresponding data fields
         * \param PLAST_LDFParser ldfParser
         * \param char*  mldfName
         * \param output PLAST_LINFrame* linFrame
         * \return int, value LDF_E_OK_SWATT in case of success, otherwise error (LDF_E_FAILED_SWATT)
         */
        Type_SWATT_LDF_FNC_ldfparser_string_outputlinf getLINFrame;

        /**
         * Creates a new LIN master node
         * \param PLAST_LDFParser ldfParser
         * \param char*  schedTable  the schedule table name used by the LINMaster
         * \param output PLAST_LINNode* linNode
         * \return int, value LDF_E_OK_SWATT in case of success, otherwise error (LDF_E_FAILED_SWATT)
         */
        Type_SWATT_LDF_FNC_ldfparser_string_outputlinnode getLINNodeMaster;

        /**
         * Creates a new LIN slave node
         * \param PLAST_LDFParser ldfParser
         * \param output PLAST_LINNode* linNode
         * \return int, value LDF_E_OK_SWATT in case of success, otherwise error (LDF_E_FAILED_SWATT)
         */
        Type_SWATT_LDF_FNC_ldfparser_outputlinnode getLINNodeSlave;

        /**
         * Returns the value of the signal.
         * \param  PLAST_LINFrame linFrame
         * \param  char* signalName = the name of the signal whose value we want to return
         * \param char* signalValue = the value of the signal
         * \return int, value LDF_E_OK_SWATT in case of success, otherwise error (LDF_E_FAILED_SWATT)
         */
        Type_SWATT_LDF_FNC_linf_string_string getSignalValue;

        /**
         * Sets the value of the signal 'signalName' to 'value'. Returns the updated value of the message data
         * \param  PLAST_LINFrame linFrame
         * \param char* signalName = the name of the signal whose value we want to change
         * \param char* signalValue = the value of the signal whose value we want to change (hex formatted)
         * \return int, value LDF_E_OK_SWATT in case of success, otherwise error (LDF_E_FAILED_SWATT)
         */
        Type_SWATT_LDF_FNC_linf_string_string setSignalValue;

        /**
         * Adds an frame to an existing slave list
         * \param  PLAST_LINNode node
         * \param  PLAST_LINFrame frame
         * \return int, value LDF_E_OK_SWATT in case of success, otherwise error (LDF_E_FAILED_SWATT)
         */
        Type_SWATT_LDF_FNC_linnode_linf addFrame;

        /**
         * adds an frame from an existing slave list
         * \param  PLAST_LINNode node
         * \param  PLAST_LINFrame frame
         * \return int, value LDF_E_OK_SWATT in case of success, otherwise error (LDF_E_FAILED_SWATT)
         */
        Type_SWATT_LDF_FNC_linnode_linf removeFrame;

        /**
         * Removes an frame from an existing slave list
         * \param  PLAST_LINNode node
         * \param  int  maxNumberOfFrames
         * \param  output PLAST_LINFrame * returnedFrames - List of returned frames
         * \param  output int *numberOfReturnedFrames
         * \return int, value LDF_E_OK_SWATT in case of success, otherwise error (LDF_E_FAILED_SWATT)
         */
        Type_SWATT_LDF_FNC_linnode_int_outputlinf_outputint getFrames;

        /**
         * Starts sending the frames of a LIN node using a thread
         * \param  PLAST_LINNode node
         * \return int, value LDF_E_OK_SWATT in case of success, otherwise error (LDF_E_FAILED_SWATT)
         */
        Type_SWATT_LDF_FNC_linf_simple startSending;

        /**
         * Stops the frames of a LIN node
         * \param  PLAST_LINNode node
         * \return int, value LDF_E_OK_SWATT in case of success, otherwise error (LDF_E_FAILED_SWATT)
         */
        Type_SWATT_LDF_FNC_linf_simple stopSending;
        /**
         * set the ldf parser error handling behavior
         * \param SWATT_LDF_ERROR_HANDLING_BEHAVIOR behavior - error handling behavior
         * \return int, value LDF_E_OK_SWATT in case of success, otherwise error (LDF_E_FAILED_SWATT)
         */
        Type_SWATT_LDF_FNC_enum setErrorHandlerBehaviour;
};


/**
    Structure for the ldf parser interface instance
 */
struct PLAST_LDFParser_class
{
        const char* file;
        unsigned int line;
        enum SWATT_LDF_ERROR_HANDLING_BEHAVIOR errorHandlingBehaviorOption;
        struct LDF_api ldf_api;
};


/* Exported Variables */
/*============================================================================*/
extern struct PLAST_LDFParser_class PLAST_LDFParser_instance ;

#define ldf (PLAST_LDFParser_instance.file=__FILE__, PLAST_LDFParser_instance.line=__LINE__,&PLAST_LDFParser_instance)->ldf_api

/* Exported functions prototypes */
/*============================================================================*/
#ifdef __CDT_PARSER__
#define SWATT_LDF_INLINE inline
#else
#define SWATT_LDF_INLINE static __attribute__((always_inline))
#endif




SWATT_LDF_INLINE void ZSWATT_LDF_ErrorHandlingBehavior(enum SWATT_LDF_ERROR_CODE err_code);
SWATT_LDF_INLINE void ZSWATT_LDF_ErrorHandlingBehavior(enum SWATT_LDF_ERROR_CODE err_code)
{
#ifdef USE_LDF_SWATT_ERROR_HANDLER
    SWATT_number_of_assertions_executed++;
    if (LDF_E_OK_SWATT == err_code)
    {
        return;
    }
    SWATT_number_of_assertions_failed++;
    switch (PLAST_LDFParser_instance.errorHandlingBehaviorOption)
    {
        case LDF_SWATT_HALT_NONE:
            break;
        case LDF_SWATT_HALT_IF_NOT_INITIALIZED:
            if (err_code == LDF_E_NOT_INITIALIZED_SWATT )
            {
                SWATT_abort_executable("ERROR: Fatal ldf parser error");
            }
            break;
        case LDF_SWATT_HALT_IF_ANY_ERROR:
            SWATT_abort_executable("ERROR: Fatal ldf parser error");
            break;
        default:
            break;
    }
#endif
}

extern void PLAST_LDFParser_Init(void);
extern void PLAST_LDFParser_DummyInit(void);

#endif  /* Notice: the file ends with a blank new line to avoid compiler warnings */

