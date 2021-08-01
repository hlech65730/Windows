/*============================================================================*/
/*                       Div I BS SOFTWARE GROUP                              */
/*============================================================================*/
/*                        OBJECT SPECIFICATION                                */
/*============================================================================*
* %name:            dbg_interface.h %
* %instance:        TPL_1 %
* %version:         6 %
* %created_by:      uid94250 %
* %date_created:    Fri Aug  1 16:15:43 2014 %
*=============================================================================*/
/* DESCRIPTION :     Testframe V3 Dbg interface                               */
/*============================================================================*/
/* FUNCTION COMMENT :                                                         */
/* This header declares the interface with Isystem WinIdea debugger           */
/*                                                                            */
/*============================================================================*/
/* COPYRIGHT (C) Continental AG 2013                                          */
/* ALL RIGHTS RESERVED                                                        */
/*                                                                            */
/* The reproduction, transmission, or use of this document or its content is  */
/* not permitted without express written authority. Offenders will be liable  */
/* for damages.                                                               */
/* All rights, including rights created by patent grant or registration of a  */
/* utility model or design, are reserved.                                     */
/*============================================================================*/
/*                               OBJECT HISTORY                               */
/*============================================================================*/
/*  REVISION |   DATE      |                               |      AUTHOR      */
/*----------------------------------------------------------------------------*/
/*    1.0    | 23/09 /2013 | Creation of the tool LPL~4409 | A.Diaconu        */
/*============================================================================*/
/*    2.0    | 23/09 /2013 | LPL~5492,LPL~5596,LPL~5604 | A.Diaconu           */
/*============================================================================*/
/*    3.0    | 23/09 /2013 | Adding template headers | A.Diaconu              */
/*============================================================================*/
#ifndef PLAST_WINIDEAINTERFACE_H
#define PLAST_WINIDEAINTERFACE_H

/**
 * \file iSystemWinIdeaInterface.h
 *
 * \brief In this file are all macros which allow interfacing to iSystem debugger from simple ASNI C code.
 *  The calling options are:
 * - Using as static library, where the external refernce make sense
 * - Using as Dynamic Link Library where LoadLibrary and GetProcAddress are needed.
 * To use one or the other :
 * - define the iSYSTEM_WINIDEA_STATIC_LIBRARY - then the library has to be statically linked.
 * - do not define anything, then the library has to be dynamically loaded, the handle to it must be dll_handle_iSystem_WinIdea.
 * In this case the handle to library can be either in a global variable or retrieved from GetModuleHandle API.
 * \ingroup iSystemWinIdea
 */

#ifdef iSYSTEM_WINIDEA_DLL_EXPORTS
 ///In this case we export the API in DLL
#define iSYSTEM_WINIDEA_DLL_API __declspec(dllexport)
#else
	#ifdef iSYSTEM_WINIDEA_STATIC_LIBRARY
	///In this case we use this API from a static linking lib from a DLL and tell the compiler to expect it at link time
	#define iSYSTEM_WINIDEA_DLL_API __declspec(dllimport)
	#else
	///In this case the DLL is loaded dynamically and we access the APIs using GetProcAddress, etc
	#define iSYSTEM_WINIDEA_DLL_API
	#endif
#endif


#ifdef __cplusplus
 extern "C" {
 #endif

/* We just want to reuse of the basic AUTOSAR types like uint8, uint16 ... */
#include "swatt_Std_Types.h"
#include "Python.h"

#define SLEEP(time) PyRun_SimpleString("import time; time.sleep(" #time ")")
///Union used to represent bytes/words/longs in the same area, used to have less API when updating values using WinIdea interface
typedef union
{
///Byte representation
	uint8 ByteValue;
///Word representation	
	uint16 WordValue;
///Long representation
	uint32 LongValue;
} U_DBG_VALUE;


/** data type for error logging function */
typedef void (__cdecl *T_iSYSTEM_WINIDEA_DLL_LOG_PRINT)(uint8 ErrorLevel, const char* MessageStr);

/** Error levels to be used with the log print interface */
enum iSYSTEM_WINIDEA_MSG_ErrorLevel
{
	// MSG_iSYSTEM_WINIDEA_FATAL_ERROR = 0, /**< test is failed, exit the executable */
	MSG_iSYSTEM_WINIDEA_ERROR = 1,       /**< test is failed */
	//MSG_iSYSTEM_WINIDEA_WARNING = 2,     /**< warning to be displayed for the user (e.g. deprecated feature used) */
	MSG_iSYSTEM_WINIDEA_INFO = 3,        /**< info, to be displayed only on high verbosity */
	//MSG_iSYSTEM_WINIDEA_VERBOSE_INFO = 4, /**< info,  to be displayed for tool testing purposes */
	//MSG_iSYSTEM_WINIDEA_DEBUG_INFO = 5,   /**< info, to be displayed for tool debug purposes */
};


/** Function address from the target */
typedef unsigned long T_DBG_FCTADDR;


/*!\brief This function sets the callback wich can be use to print failures from the DLL.
  * In case of SWATT DLL api it can be mapped to abort_executable function
  * \param logFunction The function to be called to report failures, info (see enum iSYSTEM_WINIDEA_MSG_ErrorLevel)
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern iSYSTEM_WINIDEA_DLL_API uint8 WinI_SetLogPrintFunction(T_iSYSTEM_WINIDEA_DLL_LOG_PRINT logFunction);
#else
	typedef uint8 (*WinI_SetLogPrintFunction_type)(T_iSYSTEM_WINIDEA_DLL_LOG_PRINT logFunction);
	#define  WinI_SetLogPrintFunction     ((WinI_SetLogPrintFunction_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_SetLogPrintFunction")))
#endif 



/*!\brief This function can be used to connect to WinIdea.
  * \param void
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern  iSYSTEM_WINIDEA_DLL_API uint8 WinI_Connect(void);
#else
	typedef uint8 (*WinI_Connect_type)(void);
	#define WinI_Connect  ((WinI_Connect_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_Connect")))
#endif


/*!\brief This function donwloads the executable files configured in winIdea to the microcontroller.
  * \param void
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern  iSYSTEM_WINIDEA_DLL_API uint8 WinI_Download(void);
#else
	typedef uint8 (*WinI_Download_type)(void);
	#define WinI_Download  ((WinI_Download_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_Download")))
#endif


/*!\brief This function performs a reset.
  * \param void
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern  iSYSTEM_WINIDEA_DLL_API uint8 WinI_Reset(void);
#else
	typedef uint8 (*WinI_Reset_type)(void);
	#define WinI_Reset ((WinI_Reset_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_Reset")))
#endif


/*!\brief This function starts running the code.
  * \param void
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern  iSYSTEM_WINIDEA_DLL_API uint8 WinI_Run(void);
#else
	typedef uint8 (*WinI_Run_type)(void);
	#define WinI_Run  ((WinI_Run_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_Run")))
#endif


/*!\brief This function performs a reset and a run.
  * \param void
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern  iSYSTEM_WINIDEA_DLL_API uint8 WinI_ResetAndRun(void);
#else
	typedef uint8 (*WinI_ResetAndRun_type)(void);
	#define WinI_ResetAndRun  ((WinI_ResetAndRun_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_ResetAndRun")))
#endif


/*!\brief This function stops running the code.
  * \param void
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern  iSYSTEM_WINIDEA_DLL_API uint8 WinI_Stop(void);
#else
	typedef uint8 (*WinI_Stop_type)(void);
	#define WinI_Stop  ((WinI_Stop_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_Stop")))
#endif


/*!\brief This function set the option: do not refresh winIDEA GUI after write operation.
  * \param void
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern  iSYSTEM_WINIDEA_DLL_API uint8 WinI_NoRefresh(void);
#else
	typedef uint8 (*WinI_NoRefresh_type)(void);
	#define WinI_NoRefresh  ((WinI_NoRefresh_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_NoRefresh")))
#endif


/*!\brief This function performs a step, if we are at a function call we step into that function.
  * \param void
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern  iSYSTEM_WINIDEA_DLL_API uint8 WinI_stepInto(void);
#else
	typedef uint8 (*WinI_stepInto_type)(void);
	#define  WinI_stepInto     ((WinI_stepInto_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_stepInto")))
#endif


/*!\brief This function performs a step, if we are at a function call we step over that function.
  * \param void
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern  iSYSTEM_WINIDEA_DLL_API uint8 WinI_stepOver(void);
#else
	typedef uint8 (*WinI_stepOver_type)(void);
	#define  WinI_stepOver     ((WinI_stepOver_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_stepOver")))
#endif


/*!\brief This function steps until the end of the current function.
  * \param void
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern  iSYSTEM_WINIDEA_DLL_API uint8 WinI_stepReturn(void);
#else
	typedef uint8 (*WinI_stepReturn_type)(void);
	#define  WinI_stepReturn     ((WinI_stepReturn_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_stepReturn")))
#endif


/*!\brief This function checks if the program counter is at the expected value or not.
  * In case of more breakpoints are used it can be used check that the execution stopped at the desired breakpoint.
  * Additionally if the log function is set prints as info the current state of the CPU.
  * \param PC - expected value (address) of the Program Counter
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern  iSYSTEM_WINIDEA_DLL_API uint8 WinI_CheckCPUStatus(uint32 PC);
#else
	typedef uint8 (*WinI_CheckCPUStatus_type)(uint32 PC);
	#define WinI_CheckCPUStatus  ((WinI_CheckCPUStatus_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_CheckCPUStatus")))
#endif


/*!\brief This function saves in the parameter the address of a function.
  * \param StrFctName - The name of the function
  * \param PtrAddress - The place to store the address
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern  iSYSTEM_WINIDEA_DLL_API uint8 WinI_GetFunctionAddress(const char* StrFctName,T_DBG_FCTADDR *PtrAddress);
#else
	typedef uint8 (*WinI_GetFunctionAddress_type)(const char* StrFctName,T_DBG_FCTADDR *PtrAddress);
	#define WinI_GetFunctionAddress  ((WinI_GetFunctionAddress_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_GetFunctionAddress")))
#endif


/*!\brief This function saves in the parameter the address of a line.
  * \param StrFileName - The name of the file
  * \param Line - the line number
  * \param PtrAddress - The place to store the address
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern  iSYSTEM_WINIDEA_DLL_API uint8 WinI_GetLineAddress(const char* StrFileName, uint32 Line, T_DBG_FCTADDR * PtrAddress);
#else
	typedef uint8 (*WinI_GetLineAddress_type)(const char* StrFileName, uint32 Line, T_DBG_FCTADDR * PtrAddress);
	#define WinI_GetLineAddress  ((WinI_GetLineAddress_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_GetLineAddress")))
#endif


/*!\brief This function set a breakpoint on a function.
  * \param StrSymbolName - The name of the function
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern iSYSTEM_WINIDEA_DLL_API uint8 WinI_SetSymbolBreakpoint(const char* StrSymbolName) ;
#else
	typedef uint8 (*WinI_SetSymbolBreakpoint_type)(const char* StrSymbolName) ;
	#define WinI_SetSymbolBreakpoint  ((WinI_SetSymbolBreakpoint_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_SetSymbolBreakpoint")))
#endif
	

/*!\brief This function set a breakpoint on a line.
  * \param StrFileName - The name of the file
  * \param Line - the line number
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern iSYSTEM_WINIDEA_DLL_API uint8 WinI_SetLineBreakpoint(const char* StrFileName, uint32 Line);
#else
	typedef uint8 (*WinI_SetLineBreakpoint_type)(const char* StrFileName, uint32 Line);
	#define WinI_SetLineBreakpoint  ((WinI_SetLineBreakpoint_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_SetLineBreakpoint")))
#endif


/*!\brief This function checks if the CPU stops at any breakpoint within a limited time frame.
  * \param Timeout - The maximum time to wait for CPU stop
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern  iSYSTEM_WINIDEA_DLL_API uint8 WinI_WaitForCpuStop(uint32 Timeout);
#else
	typedef uint8 (*WinI_WaitForCpuStop_type)(uint32 Timeout);
	#define  WinI_WaitForCpuStop     ((WinI_WaitForCpuStop_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_WaitForCpuStop")))
#endif


/*!\brief This function evaluates an expression.
  * The expression is expected to have result on unsigned int on 32 bits
  * \param StrExpression - The expression to evaluate
  * \param pEvalResult - Address to store the result of the evaluation
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern  iSYSTEM_WINIDEA_DLL_API uint8 WinI_EvaluateU32(const char* StrExpression, uint32* pEvalResult);
#else
	typedef uint8 (*WinI_EvaluateU32_type)(const char* StrExpression, uint32* pEvalResult);
	#define  WinI_EvaluateU32     ((WinI_EvaluateU32_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_EvaluateU32")))
#endif


/*!\brief This function clears a breakpoint which was set on a line.
  * \param StrFileName - The file on which to set the breakpoint
  * \param line -  The line on which to set the breakpoint
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern iSYSTEM_WINIDEA_DLL_API uint8 WinI_ClearLineBreakpoint(const char* StrFileName, uint32 line);
#else
	typedef uint8 (*WinI_ClearLineBreakpoint_type)(const char* StrFileName, uint32 Line);
	#define WinI_ClearLineBreakpoint  ((WinI_ClearLineBreakpoint_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_ClearLineBreakpoint")))
#endif


/*!\brief This function clears a breakpoint which was set on a function (symbol).
  * \param StrSymbolName - The function on which to clear the breakpoint
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern iSYSTEM_WINIDEA_DLL_API uint8 WinI_ClearSymbolBreakpoint(const char* StrSymbolName);
#else
	typedef uint8 (*WinI_ClearSymbolBreakpoint_type)(const char* StrSymbolName);
	#define WinI_ClearSymbolBreakpoint  ((WinI_ClearSymbolBreakpoint_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_ClearSymbolBreakpoint")))
#endif


/*!\brief This function clears all existing breakpoints.
  * \param void
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern iSYSTEM_WINIDEA_DLL_API uint8 WinI_ClearAllBreakpoints(void);
#else
	typedef uint8 (*WinI_ClearAllBreakpoints_type)(void);
	#define WinI_ClearAllBreakpoints  ((WinI_ClearAllBreakpoints_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_ClearAllBreakpoints")))
#endif

/*!\brief This function disables a function (symbol) breakpoint.
  * \param StrSymbolName - the name of the function on which we disable the breakpoint
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern iSYSTEM_WINIDEA_DLL_API uint8 WinI_SetDisableBreakpoint(const char* StrSymbolName);
#else
	typedef uint8 (*WinI_SetDisableBreakpoint_type)(const char* StrSymbolName);
	#define WinI_SetDisableBreakpoint  ((WinI_SetDisableBreakpoint_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_SetDisableBreakpoint")))
#endif

/*!\brief This function enables a disabled a function (symbol) breakpoint.
  * \param StrSymbolName - the name of the function on which we disable the breakpoint
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern iSYSTEM_WINIDEA_DLL_API uint8 WinI_SetEnableBreakpoint(const char* StrSymbolName);
#else
	typedef uint8 (*WinI_SetEnableBreakpoint_type)(const char* StrSymbolName);
	#define WinI_SetEnableBreakpoint  ((WinI_SetEnableBreakpoint_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_SetEnableBreakpoint")))
#endif

/*!\brief This function disables all breakpoints.
  * \param void
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern iSYSTEM_WINIDEA_DLL_API uint8 WinI_DisableAllBreakpoints(void);
#else
	typedef uint8 (*WinI_DisableAllBreakpoints_type)(void);
	#define WinI_DisableAllBreakpoints  ((WinI_DisableAllBreakpoints_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_DisableAllBreakpoints")))
#endif

/*!\brief This function enables all breakpoints.
  * \param void
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern iSYSTEM_WINIDEA_DLL_API uint8 WinI_EnableAllBreakpoints(void);
#else
	typedef uint8 (*WinI_EnableAllBreakpoints_type)(void);
	#define WinI_EnableAllBreakpoints  ((WinI_EnableAllBreakpoints_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_EnableAllBreakpoints")))
#endif


/*!\brief This function reads the value of a named variable.
  * \param StrSymbolName - the name of the variable
  * \param PtrValue - address to store the value (see U_DBG_VALUE)
  * \param NbOfBits - number of bits to read, suported values: 8, 16, 32
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern  iSYSTEM_WINIDEA_DLL_API uint8 WinI_ReadValue(const char* StrSymbolName, U_DBG_VALUE* PtrValue,uint8 NbOfBits);
#else
	typedef uint8 (*WinI_ReadValue_type)(const char* StrSymbolName, U_DBG_VALUE* PtrValue,uint8 NbOfBits);
	#define WinI_ReadValue  ((WinI_ReadValue_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_ReadValue")))
#endif


/*!\brief This function writes the value of a named variable.
  * \param StrSymbolName - the name of the variable
  * \param Value -  the value to be written (see U_DBG_VALUE)
  * \param NbOfBits - number of bits to write, suported values: 8, 16, 32
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern  iSYSTEM_WINIDEA_DLL_API uint8 WinI_WriteValue(const char* StrSymbolName, U_DBG_VALUE Value, uint8 NbOfBits);
#else
	typedef uint8 (*WinI_WriteValue_type)(const char* StrSymbolName, U_DBG_VALUE Value, uint8 NbOfBits);
	#define WinI_WriteValue		  ((WinI_WriteValue_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_WriteValue")))
#endif


/*!\brief This function reads the value from a given address.
  * \param Address - the address to read from
  * \param PtrValue - address to store the value (see U_DBG_VALUE)
  * \param NbOfBits - number of bits to read, suported values: 8, 16, 32
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern  iSYSTEM_WINIDEA_DLL_API uint8 WinI_ReadValuebyAddr(uint32 Address, U_DBG_VALUE* PtrValue, uint8 NbOfBits);
#else
	typedef uint8 (*WinI_ReadValuebyAddr_type)(uint32 Address, U_DBG_VALUE* PtrValue, uint8 NbOfBits);
	#define WinI_ReadValuebyAddr  ((WinI_ReadValuebyAddr_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_ReadValuebyAddr")))
#endif


/*!\brief This function reads the value from a given address.
  * \param Address - the address to read from
  * \param PtrValue - address to store the value (see U_DBG_VALUE)
  * \param NbOfBits - number of bits to read, suported values: 8, 16, 32
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern  iSYSTEM_WINIDEA_DLL_API uint8 WinI_WriteValuebyAddr(uint32 Address, U_DBG_VALUE Value, uint8 NbOfBits);
#else
	typedef uint8 (*WinI_WriteValuebyAddr_type)(uint32 Address, U_DBG_VALUE Value, uint8 NbOfBits);
	#define WinI_WriteValuebyAddr  ((WinI_WriteValuebyAddr_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_WriteValuebyAddr")))
#endif


/*!\brief This function reads the value from a named register.
  * \param StrRegisterName - name of the register we are reading
  * \param PtrValue - address to store the value (see U_DBG_VALUE)
  * \param NbOfBits - number of bits to read, suported values: 8, 16, 32
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern  iSYSTEM_WINIDEA_DLL_API uint8 WinI_ReadRegister( const char* StrRegisterName, U_DBG_VALUE * PtrValue, uint8 NbOfBits);
#else
	typedef uint8 (*WinI_ReadRegister_type)( const char* StrRegisterName, U_DBG_VALUE * PtrValue, uint8 NbOfBits);
	#define WinI_ReadRegister  ((WinI_ReadRegister_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_ReadRegister")))
#endif


/*!\brief This function writes a value to a named register.
  * \param StrRegisterName - name of the register we are reading
  * \param Value - the value to be written (see U_DBG_VALUE)
  * \param NbOfBits - number of bits to read, suported values: 8, 16, 32
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern  iSYSTEM_WINIDEA_DLL_API uint8 WinI_WriteRegister(const char* StrRegisterName, const U_DBG_VALUE Value,uint8 NbOfBits);
#else
	typedef uint8 (*WinI_WriteRegister_type)(const char* StrRegisterName, const U_DBG_VALUE Value,uint8 NbOfBits);
	#define WinI_WriteRegister  ((WinI_WriteRegister_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_WriteRegister")))
#endif


/*!\brief This function reads a certain amount of data from a given address from microcontroller into a given buffer on PC.
  * \param EcuSourcePtr - the start address on the miocrocontroller we are reading
  * \param PcDestPtr - the destination pointer on the PC
  * \param Length - number of bytes to read from the microcontroller
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern iSYSTEM_WINIDEA_DLL_API uint8 WinI_ReadMemoryArray(uint32 EcuSourcePtr,uint8* PcDestPtr, uint32 Length);
#else
	typedef  uint8 (*WinI_ReadMemoryArray_type)(uint32 EcuSourcePtr,uint8* PcDestPtr, uint32 Length);
	#define WinI_ReadMemoryArray   ((WinI_ReadMemoryArray_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_ReadMemoryArray")))
#endif


/*!\brief This function writes a certain amount of data from a given address from microcontroller from a given buffer on PC.
  * \param EcuDestPtr - the start address on the miocrocontroller we are writing
  * \param PcSourcePtr - the source pointer on the PC
  * \param Length - number of bytes to write into the microcontroller
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern iSYSTEM_WINIDEA_DLL_API uint8 WinI_WriteMemoryArray(uint32 EcuDestPtr,uint8* PcSourcePtr, uint32 Length);
#else
	typedef uint8 (*WinI_WriteMemoryArray_type)(uint32 EcuDestPtr,uint8* PcSourcePtr, uint32 Length);
	#define WinI_WriteMemoryArray	((WinI_WriteMemoryArray_type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_WriteMemoryArray")))
#endif


/*!\brief This function fills a memory zone on the microcontroller starting from a given address with a given value.
  * \param EcuDestPtr - the start address on the miocrocontroller we are reading
  * \param ByteValue - the value with which we fill the memory zone
  * \param Length - number of bytes to write into the microcontroller
  * \return 0 in case of success, otherwise error 
  * \hideinitializer
\ingroup iSystemWinIdea
*/
#ifndef iSYSTEM_WINIDEA_LINK_DLL
	extern iSYSTEM_WINIDEA_DLL_API uint8 WinI_FillMemoryArray(uint32 EcuDestPtr,uint8 ByteValue, uint32 Length);
#else
	typedef uint8 (*WinI_FillMemoryArray_Type)(uint32 EcuDestPtr,uint8 ByteValue, uint32 Length);
	#define WinI_FillMemoryArray ((WinI_FillMemoryArray_Type)(GetProcAddress(dll_handle_iSystem_WinIdea,"WinI_FillMemoryArray")))
#endif


#ifdef __cplusplus
 }
 #endif

#endif
