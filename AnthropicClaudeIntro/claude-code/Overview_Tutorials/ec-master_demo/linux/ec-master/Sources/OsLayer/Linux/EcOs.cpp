/*----------------------------------------------------------------------------
 * EcOs.cpp
 * Copyright                acontis technologies GmbH, Ravensburg, Germany
 * Response                 Paul Bussmann
 * Description              EC-Master OS-Layer for Linux
 *---------------------------------------------------------------------------*/

#define EC_OS_CPP

/*-LOGGING-------------------------------------------------------------------*/
#ifndef pEcLogParms
extern "C" struct _EC_T_LOG_PARMS* G_pLogParmsEcOs;
#define pEcLogParms G_pLogParmsEcOs
#endif

/*-INCLUDES------------------------------------------------------------------*/
#include <errno.h> /* errno */
#include <limits.h> /* PTHREAD_STACK_MIN */
#include <syslog.h> /* syslog */
#include <dlfcn.h> /* dynamic loader */
#include <sys/prctl.h> /* prctl() */

#include "EcOs.h"
#include "EcError.h"
#include "EcLog.h"

/*-DEFINES--------------------------------------------------------------------*/
#define TRACE_FILENAME "ecatTrace.log"

#ifndef EC_OS_MAX_SODIR_LEN
#define EC_OS_MAX_SODIR_LEN 255
#endif

#ifndef PAGE_SIZE
#   define PAGE_SIZE 0x1000
#endif
#ifndef PAGE_UP
#   define PAGE_UP(addr)   (((addr)+((PAGE_SIZE)-1))&(~((PAGE_SIZE)-1)))
#endif
#ifndef PAGE_DOWN
#   define PAGE_DOWN(addr) ((addr)&(~((PAGE_SIZE)-1)))
#endif

#if (defined EC_OS_NAMESPACE)
namespace EC_OS_NAMESPACE
{
#endif

/*-LOGGING-------------------------------------------------------------------*/
EC_T_DWORD EC_FNCALL LogMsgOsPrintf(struct _EC_T_LOG_CONTEXT* /* pContext */, EC_T_DWORD /* dwLogMsgSeverity*/, const EC_T_CHAR* szFormat, ...)
{
    EC_T_VALIST vaArgs;
    EC_VASTART(vaArgs, szFormat);
    OsVprintf(szFormat, vaArgs);
    EC_VAEND(vaArgs);
    return EC_E_NOERROR;
}

static struct _EC_T_LOG_PARMS S_oLogParmsEcOs = {EC_LOG_LEVEL_ERROR, LogMsgOsPrintf, EC_NULL};
struct _EC_T_LOG_PARMS* G_pLogParmsEcOs = &S_oLogParmsEcOs;

/*-TYPEDEFS------------------------------------------------------------------*/

/*-LOCALS--------------------------------------------------------------------*/
static EC_PF_SYSTIME             S_pfSystemTimeGet        = EC_NULL;
static EC_PF_QUERY_MSEC_COUNT    S_pfSystemQueryMsecCount = EC_NULL;
static EC_PF_GETLINKLAYERREGFUNC S_pfGetLinkLayerRegFunc  = EC_NULL;
EC_T_INT S_nMutexType = PTHREAD_MUTEX_RECURSIVE;
EC_T_INT S_nMutxProtocol = PTHREAD_PRIO_INHERIT;

#ifdef DEBUG
static EC_T_BOOL        S_bSpinLockActive       = EC_FALSE;     /* flag: if set, no OS calls are allowed */
static pthread_t        S_SpinLockThread        = EC_NULL;      /* thread which owns the spin lock */
#endif
static pthread_t        S_JobTaskThread         = EC_NULL;      /* job thread */

static E_SLEEP S_ESleep = eSLEEP_CLOCK_NANOSLEEP;

struct ThreadArg
{
#define MAX_THREADNAME_LEN 16

   EC_PF_THREADENTRY entry;
   void*             arg;
   char              name[MAX_THREADNAME_LEN];
   uint              cpuMask;
   uint              threadPrio;
};
/*-TYPEDEFS------------------------------------------------------------------*/
#define EC_DRIVER_IDENT_MAXLEN   39                           /* maximum length for a driver ident string (zero terminated) */
#define EC_DRIVER_IDENT_NAMESIZE (EC_DRIVER_IDENT_MAXLEN + 1) /* driver ident string is zero terminated */
#define MAX_LINKLAYERREG_ENTRIES 16
typedef struct _LINKLAYERREG_ENTRY
{
  EC_T_CHAR szDriverIdent[EC_DRIVER_IDENT_NAMESIZE];
  void* pvLibHandle;
} LINKLAYERREG_ENTRY;

static LINKLAYERREG_ENTRY S_aLinkLayerRegList[MAX_LINKLAYERREG_ENTRIES];
static EC_T_BOOL          S_bLinkLayerRegListInitialized = EC_FALSE;

#if (defined DEBUG)
static unsigned CpuSetToMask(cpu_set_t cpuSet)
{
   unsigned cpuMask = 0;
   int cpuCnt = CPU_COUNT(&cpuSet);
   for (int i = 0; i < cpuCnt; ++i)
   {
     if (CPU_ISSET(i, &cpuSet)) cpuMask |= (1 << i);
   }
   return cpuMask;
}
#endif /* DEBUG */

static cpu_set_t CpuMaskToSet(unsigned cpuMask)
{
   cpu_set_t cpuSet;
   CPU_ZERO(&cpuSet);
   for (int i = 0; i < 32; ++i)
   {
     if (cpuMask & (1 << i))
     {
        CPU_SET(i, &cpuSet);
     }
   }
   return cpuSet;
}

/******************************************************************************/
/** \brief OS Layer initialization.
*
* \return status code
*/
EC_OS_API EC_T_DWORD EC_OS_API_FNCALL OsInit(EC_T_OS_PARMS* pOsParms)
{
    EC_T_DWORD dwRetVal = EC_E_ERROR;

    if (EC_NULL != pOsParms)
    {
        if (EC_OS_PARMS_SIGNATURE != pOsParms->dwSignature)
        {
            EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "ERROR: OsInit() OS layer parameter signature 0x%08X wrong! Expected EC_OS_PARMS_SIGNATURE (0x%08X).\n",
                pOsParms->dwSignature, EC_OS_PARMS_SIGNATURE));
            dwRetVal = EC_E_INVALIDPARM;
            goto Exit;
        }
        if (pOsParms->dwSize < sizeof(EC_T_OS_PARMS))
        {
            EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "ERROR: OsInit() OS layer parameter size %d too small! Size of EC_T_OS_PARMS is %d bytes.\n",
                pOsParms->dwSize, sizeof(EC_T_OS_PARMS)));
            dwRetVal = EC_E_INVALIDPARM;
            goto Exit;
        }
        if (EC_NULL != pOsParms->pLogParms)
        {
            OsMemcpy(G_pLogParmsEcOs, pOsParms->pLogParms, sizeof(EC_T_LOG_PARMS));
        }
        if ((EC_NULL == S_pfSystemTimeGet) && (EC_NULL != pOsParms->pfSystemTimeGet))
        {
            S_pfSystemTimeGet = pOsParms->pfSystemTimeGet;
        }
        if ((EC_NULL == S_pfSystemQueryMsecCount) && (EC_NULL != pOsParms->pfSystemQueryMsecCount))
        {
            S_pfSystemQueryMsecCount = pOsParms->pfSystemQueryMsecCount;
        }
        if(EC_TRUE == pOsParms->PlatformParms.bConfigMutex)
        {
            S_nMutexType = pOsParms->PlatformParms.nMutexType;
            S_nMutxProtocol = pOsParms->PlatformParms.nMutexProtocol;
        }
    }

    dwRetVal = EC_E_NOERROR;
Exit:
    return dwRetVal;
}

EC_OS_API EC_T_VOID EC_OS_API_FNCALL OsSetLogParms(_EC_T_LOG_PARMS* pLogParms)
{
    OsMemcpy(G_pLogParmsEcOs, pLogParms, sizeof(EC_T_LOG_PARMS));
}
/******************************************************************************/
/** \brief OS Layer de-initialization.
*
* \return status code
*/
EC_OS_API EC_T_DWORD EC_OS_API_FNCALL OsDeinit(EC_T_VOID)
{
    return EC_E_NOERROR;
}

/******************************************************************************/
/** \brief Determine millisecond counter value since start.
*
* \return Milliseconds since start (start = first call to this function).
*/
EC_T_DWORD OsQueryMsecCount(EC_T_VOID)
{
    static EC_T_BOOL s_bInitMsecCount = EC_FALSE;
    static struct timespec s_tsStart;
    struct timespec ts;
    struct timespec tsRes;
    EC_T_DWORD dwMsec;
    EC_T_DWORD dwNsecDelta;
    EC_T_DWORD dwSecDelta;

    if (EC_NULL != S_pfSystemQueryMsecCount)
    {
        /* from configured function */
        dwMsec = S_pfSystemQueryMsecCount();
    }
    else
    {
        clock_gettime(CLOCK_MONOTONIC, &ts);
        if( !s_bInitMsecCount )
        {
            clock_getres(CLOCK_MONOTONIC, &tsRes);
            if( tsRes.tv_nsec > 1000000 )
            {
                EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "OsQueryMsecCount - clock_getres resolution too small!\n"));
                OsDbgAssert(EC_FALSE);
            }
            s_tsStart.tv_nsec = ts.tv_nsec;
            s_tsStart.tv_sec = ts.tv_sec;
            s_bInitMsecCount = EC_TRUE;
        }
        if( ts.tv_nsec < s_tsStart.tv_nsec )
        {
            dwNsecDelta = s_tsStart.tv_nsec - ts.tv_nsec;
            dwSecDelta = (dwNsecDelta + 999999999)/1000000000;   /* round up to full seconds */
            ts.tv_sec -= dwSecDelta;
            ts.tv_nsec += 1000000000 * dwSecDelta;
        }
        OsDbgAssert( ts.tv_nsec >= s_tsStart.tv_nsec );
        ts.tv_nsec = ts.tv_nsec - s_tsStart.tv_nsec;
        ts.tv_sec = ts.tv_sec - s_tsStart.tv_sec;

        OsDbgAssert( ts.tv_sec >= 0 );
        OsDbgAssert( ts.tv_nsec <= 1000000000 );
        dwMsec = ts.tv_nsec / 1000000;
        dwMsec += 1000 * ts.tv_sec;
    }
    return dwMsec;
}

/***************************************************************************************************/
/**
\brief  Replaces the built in function to get system's msec count

\return EC_E_NOERROR
*/
EC_OS_API EC_T_DWORD EC_OS_API_FNCALL OsReplaceQueryMsecCount(EC_PF_QUERY_MSEC_COUNT pfQueryMsecCount)
{
    S_pfSystemQueryMsecCount = pfQueryMsecCount;
    return EC_E_NOERROR;
}

/******************************************************************************/
/** \brief Open configuration file
*
* \return handle to configuration file or NULL in case of error
*/
EC_OS_FNNAME EC_T_VOID* EC_OS_FNCALL OsCfgFileOpen(const EC_T_CHAR* szCfgFileName)
{
    return fopen(szCfgFileName, "r");
}

/******************************************************************************/
/** \brief Close configuration file
*
* \return if no error has occurred, OsCfgFileClose returns 0. Otherwise, it returns a nonzero value.
*/
EC_OS_FNNAME EC_T_INT EC_OS_FNCALL OsCfgFileClose(EC_T_VOID* pvCfgFile)
{
    EC_T_INT nRet = 0;

    if( EC_NULL != pvCfgFile )
    {
        nRet = fclose( (FILE*)pvCfgFile );
    }

    return nRet;
}

/******************************************************************************/
/** \brief Read next chunk of the configuration file
*
* \return number of bytes read
*/
EC_OS_FNNAME EC_T_INT EC_OS_FNCALL OsCfgFileRead(EC_T_VOID* pvCfgFile, EC_T_VOID* pvDst, EC_T_INT nLen)
{
    EC_T_INT nRet = 0;

    if( EC_NULL != pvCfgFile )
    {
        nRet = fread(pvDst, 1, nLen, (FILE*)pvCfgFile);
    }

    return nRet;
}

/******************************************************************************/
/** \brief Determine if last OsCfgFileRead operation did cause an error
*
* \return if no error has occurred, OsCfgFileError returns 0. Otherwise, it returns a nonzero value.
*/
EC_OS_FNNAME EC_T_INT EC_OS_FNCALL OsCfgFileError(EC_T_VOID* pvCfgFile)
{
    return ferror((FILE*)pvCfgFile);
}

/******************************************************************************/
/** \brief Determine if the end of the configuration file is reached
*
* \return Returns 0 if the current position has not reached the end of the configuration file.
*/
EC_OS_FNNAME EC_T_INT EC_OS_FNCALL OsCfgFileEof(EC_T_VOID* pvCfgFile)
{
    return feof((FILE*)pvCfgFile);
}

/******************************************************************************/
/** \brief Assert proxy to halt on error and expose break point possibility
*/
EC_OS_FNNAME EC_T_VOID EC_OS_FNCALL OsDbgAssertFail(const EC_T_CHAR* szFile, EC_T_DWORD dwLine)
{
    EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "ERROR: Assert failure in %s, line %d!\n", szFile, dwLine));
#if (defined OS_DBG_ASSERT_PAUSE)
    syslog(LOG_USER | LOG_ERR, "ASSERTION in file %s, line %d\n", szFile, (int)dwLine);
    pause();
#endif
}

/******************************************************************************/
/** \brief Assert proxy to halt on error and expose break point possibility
*/
EC_OS_FNNAME EC_T_VOID EC_OS_FNCALL OsDbgAssertFunc(EC_T_BOOL bAssertCondition, const EC_T_CHAR* szFile, EC_T_DWORD dwLine)
{
    if (!bAssertCondition)
    {
        OsDbgAssertFail(szFile, dwLine);
    }
}

/******************************************************************************/
/** \brief Create a synchronization mutual exclusion object
*
* \return handle to the mutex object.
*/
EC_OS_API EC_T_VOID* EC_OS_API_FNCALL OsCreateLock(EC_T_VOID)
{
    return OsCreateLockTyped(eLockType_DEFAULT);
}

/******************************************************************************/
/** \brief Create a synchronization mutual exclusion object
*
* \return handle to the mutex object.
*/
EC_OS_API EC_T_VOID* EC_OS_API_FNCALL OsCreateLockTyped(EC_T_OS_LOCK_TYPE eLockType)
{
    pthread_mutexattr_t MutexAttr;
    OS_LOCK_DESC* pvLockDesc = (OS_LOCK_DESC*)OsMalloc(sizeof(OS_LOCK_DESC));
    OsDbgAssert(EC_NULL != pvLockDesc);

    /* check if spin lock is active */

    if (pvLockDesc != NULL)
    {
      pthread_mutexattr_init(&MutexAttr);

      // Set the mutex as a recursive mutex
      pthread_mutexattr_settype(&MutexAttr, S_nMutexType);

      // Set the mutex protocol
      pthread_mutexattr_setprotocol(&MutexAttr, S_nMutxProtocol);

      // create the muteIdx with the attributes set
      pthread_mutex_init(&pvLockDesc->Mutex, &MutexAttr);

      //After initializing the mutex, the thread attribute can be destroyed
      pthread_mutexattr_destroy(&MutexAttr);

      pvLockDesc->nLockCnt = 0;
      pvLockDesc->pThread = EC_NULL;
      pvLockDesc->eLockType = eLockType;
   }
    return pvLockDesc;
}

/******************************************************************************/
/** \brief Delete a mutex object if not EC_NULL
 *
 * \return N/A
 */
EC_OS_API EC_T_VOID EC_OS_API_FNCALL OsDeleteLock(EC_T_VOID* pvLockHandle)
{
    OS_LOCK_DESC* pvLockDesc = (OS_LOCK_DESC*)pvLockHandle;
    if (EC_NULL == pvLockDesc)
    {
        return;
    }

    /* check if spin lock is active */
    OsDbgAssert(pvLockDesc->nLockCnt == 0);
    pthread_mutex_destroy(&pvLockDesc->Mutex);

    OsFree(pvLockDesc);
}

/******************************************************************************/
EC_OS_API EC_T_VOID EC_OS_API_FNCALL OsLock(EC_T_VOID* pvLockHandle)
{
    OS_LOCK_DESC* pvLockDesc = (OS_LOCK_DESC*)pvLockHandle;

    OsDbgAssert(pvLockDesc != EC_NULL);

    if (pvLockDesc != NULL)
    {
        pthread_mutex_lock(&(pvLockDesc->Mutex));
#if (defined DEBUG)
        pvLockDesc->pThread = pthread_self();
        if (pvLockDesc->eLockType == eLockType_SPIN)
        {
            S_bSpinLockActive = EC_TRUE;
            S_SpinLockThread = pvLockDesc->pThread;
        }
        /* it is not allowed to call oslock inside the job task with a lock type not equal to spin */
        else if (S_JobTaskThread == pvLockDesc->pThread)
        {
            OsDbgAssert(EC_FALSE);
        }
        pvLockDesc->nLockCnt++;
        OsDbgAssert(pvLockDesc->nLockCnt < 10);  /* that much nesting levels? */
#endif
    }
}

/******************************************************************************/
EC_OS_API EC_T_VOID EC_OS_API_FNCALL OsUnlock(EC_T_VOID* pvLockHandle)
{
    OS_LOCK_DESC* pvLockDesc = (OS_LOCK_DESC*)pvLockHandle;

    OsDbgAssert( pvLockDesc != EC_NULL );

    if (pvLockDesc != NULL)
    {
#ifdef DEBUG
        pvLockDesc->nLockCnt--;
        if (pvLockDesc->nLockCnt == 0)
        {
            pvLockDesc->pThread = EC_NULL;
        }
        OsDbgAssert(pvLockDesc->nLockCnt >= 0);

        if(pvLockDesc->eLockType == eLockType_SPIN)
        {
            S_bSpinLockActive = EC_FALSE;
            S_SpinLockThread = EC_NULL;
        }

#endif
        pthread_mutex_unlock(&(pvLockDesc->Mutex));
    }
}

/********************************************************************************/
/** \brief Create a binary semaphore
*
* \return event object to be referenced in further calls or EC_NULL in case of errors.
*/
EC_OS_API EC_T_VOID* EC_OS_API_FNCALL OsCreateEvent(EC_T_VOID)
{
    sem_t* pSemaphore;
    EC_T_VOID* pvRetVal = EC_NULL;

    /* create event */
    pSemaphore = (sem_t*)OsMalloc(sizeof(sem_t));
    if( pSemaphore == NULL )
    {
        goto Exit;
    }
    OsMemset(pSemaphore, 0, sizeof(sem_t));
    if (sem_init(pSemaphore, 0, 0) < 0)
    {
        perror("sem_init failed");
        SafeOsFree(pSemaphore);
        goto Exit;
    }

    /* no errors */
    pvRetVal = (EC_T_VOID*)pSemaphore;
Exit:
    return pvRetVal;
}

/********************************************************************************/
/** \brief  Delete an event object
*
* \return N/A.
*/
EC_OS_API EC_T_VOID EC_OS_API_FNCALL OsDeleteEvent(EC_T_VOID* pvEvent)
{
    /* delete event */
    sem_destroy((sem_t*)pvEvent);
    SafeOsFree(pvEvent);
}

/********************************************************************************/
/** \brief  Set event
*/
EC_OS_API EC_T_VOID EC_OS_API_FNCALL OsPlatformImplSetEvent(EC_T_VOID* pEvent)
{
    int iRes = 0;
    int iVal = 0;

    /* Ensure the event trigger count does not exceed one per cycle. */
    iRes = sem_getvalue((sem_t*)pEvent, &iVal);
    if ((0 == iRes) && (iVal > 0))
        return;

    sem_post((sem_t*)pEvent);
}

/********************************************************************************/
/** \brief  Wait for event
*
* \return EC_E_NOERROR if event was set for the timeout, or error code in case of errors.
*/
EC_OS_API EC_T_DWORD EC_OS_API_FNCALL OsWaitForEvent(EC_T_VOID* pvEvent, EC_T_DWORD dwTimeout)
{
    int nResult;
    struct timespec tsCurr;
    struct timespec tsLatest;
    EC_T_DWORD dwRetVal = EC_E_ERROR;

    /* handle different timeout cases */
    switch (dwTimeout)
    {
    case EC_NOWAIT:
        nResult = sem_trywait( (sem_t*)pvEvent );
        if (nResult == 0)
        {
            dwRetVal = EC_E_NOERROR;
        }
        else if ((nResult == -1) && (errno == EAGAIN))
        {
            dwRetVal = EC_E_TIMEOUT;
        }
        else
        {
            EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "OsWaitForEvent: ERROR: sem_trywait returned %d\n",
                    nResult));
            OsDbgAssert(EC_FALSE);
            dwRetVal = EC_E_ERROR;
        }
        break;

    case EC_WAITINFINITE:
        nResult = sem_wait((sem_t*)pvEvent);
        if (nResult == 0)
        {
            dwRetVal = EC_E_NOERROR;
        }
        else
        {
            EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "OsWaitForEvent: ERROR: sem_wait returned %d\n",
                    nResult));
            OsDbgAssert(EC_FALSE);
            dwRetVal = EC_E_ERROR;
        }
        break;

    default:
        /* Calculate relative interval as current time plus number of milliseconds */
        if (clock_gettime(CLOCK_REALTIME, &tsCurr) == -1)
        {
            EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "OsWaitForEvent: clock_gettime returned an error\n"));
            OsDbgAssert(EC_FALSE);
        }
        tsLatest.tv_sec = dwTimeout / 1000;
        tsLatest.tv_nsec = (dwTimeout % 1000) * 1000000;

        tsLatest.tv_sec += tsCurr.tv_sec;
        tsLatest.tv_nsec += tsCurr.tv_nsec;
        if (tsLatest.tv_nsec >= 1000000000)
        {
           ++tsLatest.tv_sec;
           tsLatest.tv_nsec -= 1000000000;
        }
        OsDbgAssert(tsLatest.tv_nsec < 1000000000);

        nResult = sem_timedwait((sem_t*)pvEvent, &tsLatest);
        if (nResult == 0)
        {
            dwRetVal = EC_E_NOERROR;
        }
        else if ((nResult == -1) && (errno == ETIMEDOUT))
        {
            dwRetVal = EC_E_TIMEOUT;
        }
        else
        {
            EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "OsWaitForEvent: sem_timedwait returned error %d\n", nResult));
            OsDbgAssert(EC_FALSE);
            dwRetVal = EC_E_ERROR;
        }
        break;
    }

    return dwRetVal;
}

/********************************************************************************/
/** \brief Determine type of OsSleep implementation.
*
* \return N/A.
*/
EC_T_VOID   OsSleepSetType(E_SLEEP ESleep)
{
    S_ESleep = ESleep;
}

/********************************************************************************/
/** \brief Sleep for a specified amount of time.
*
* \return N/A.
*/
EC_T_VOID  OsPlatformImplSleep(EC_T_DWORD dwMsec)
{
    struct timespec ts;
    OsMemset(&ts, 0, sizeof(struct timespec));

    switch (S_ESleep)
    {
    case eSLEEP_USLEEP:
        usleep(1000 * dwMsec);
        break;

    case eSLEEP_NANOSLEEP:
        ts.tv_sec = dwMsec / 1000;
        ts.tv_nsec = 1000000 * (dwMsec % 1000);
        nanosleep(&ts, EC_NULL);
        break;

    case eSLEEP_CLOCK_NANOSLEEP:
    default:
        ts.tv_sec = dwMsec / 1000;
        ts.tv_nsec = 1000000 * (dwMsec % 1000);
        clock_nanosleep(CLOCK_MONOTONIC, 0, &ts, EC_NULL);
        break;
    }
}

static void* ThreadStub(ThreadArg* arg)
{
   /* Set threadname (max 16 bytes) */
   prctl(PR_SET_NAME, arg->name, 0, 0, 0);

   /* Set CPU affinity mask */
   if (arg->cpuMask != 0)
   {
      OsSetThreadAffinity(EC_NULL, arg->cpuMask);
   }

   /* Try to set up realtime scheduling. This will probably fail if the kernel
    * has no preemption support compiled in.
    */
   struct sched_param schedParam = { 0 };
   schedParam.sched_priority = arg->threadPrio;
   if (sched_setscheduler(0, SCHED_FIFO, &schedParam) < 0)
   {
       EcLogMsg(EC_LOG_LEVEL_VERBOSE, (pEcLogContext, EC_LOG_LEVEL_VERBOSE, "Couldn't change to realtime scheduling class (SCHED_FIFO).\n"));
   }

#if defined(DEBUG) && 1 /* Print scheduling info about the thread */

   /* Query scheduling parameters of calling thread */
   schedParam.sched_priority = 0;
   sched_getparam(0, &schedParam);

   /* Query the CPU of calling thread */
   int cpuIdx = sched_getcpu();

   /* Query CPU's on whoes the calling thread is allowed to run */
   cpu_set_t cpuSet;
   CPU_ZERO(&cpuSet);
   if (pthread_getaffinity_np(pthread_self(), sizeof(cpuSet), &cpuSet) < 0)
   {
       EcLogMsg(EC_LOG_LEVEL_WARNING, (pEcLogContext, EC_LOG_LEVEL_WARNING, "pthread_getaffinity_np failed\n"));
   }

   /* Query scheduling policy of calling thread */
   int schedPolicy = sched_getscheduler(0);
   const char *schedPolicyName = "UNKNOWN";
   switch (schedPolicy)
   {
     case SCHED_FIFO: schedPolicyName = "SCHED_FIFO"; break;
     case SCHED_RR: schedPolicyName = "SCHED_RR"; break;
     case SCHED_OTHER: schedPolicyName = "SCHED_OTHER"; break;
     case SCHED_BATCH: schedPolicyName = "SCHED_BATCH"; break;
   }

   /* Query scheduling timer resolution */
   struct timespec tsRes = { 0 };
   clock_getres(schedPolicy, &tsRes);

   EcLogMsg(EC_LOG_LEVEL_VERBOSE, (pEcLogContext, EC_LOG_LEVEL_VERBOSE, "   >>> [OSAL] Thread '%s' created. Scheduler: %s, Prio %d, ClockRes: %u, CPU: %d, CPUAffinityMask: 0x%x\n",
         arg->name,
         schedPolicyName,
         schedParam.sched_priority,
         tsRes.tv_nsec,
         cpuIdx,
         CpuSetToMask(cpuSet)));

#endif

   /* Call thread entry */
   arg->entry(arg->arg);

   delete arg;

   return NULL;
}

/********************************************************************************/
/** \brief Create thread.
*
* \return thread object or EC_NULL in case of an error.
*/
EC_OS_API EC_T_VOID* EC_OS_API_FNCALL OsPlatformImplCreateThread(
                                       const EC_T_CHAR* szThreadName,
                                       EC_PF_THREADENTRY pfThreadEntry,
                                       EC_T_CPUSET cpuAffinityMask,
                                       EC_T_DWORD dwPrio,
                                       EC_T_DWORD dwStackSize,
                                       EC_T_VOID* pvParams
                                       )
{
    int nResult;
    pthread_t pThread;
    pthread_attr_t ThreadAttr;
    EC_T_VOID* pvThreadObject = EC_NULL;
    ThreadArg* arg = new ThreadArg;
    memset(arg, 0, sizeof(ThreadArg));

#if (defined DEBUG)
    EcLogMsg(EC_LOG_LEVEL_VERBOSE, (pEcLogContext, EC_LOG_LEVEL_VERBOSE, "Create thread: Name '%s', CpuMask 0x%x, Prio %d, Stack %d\n",
          szThreadName,
          (unsigned int)cpuAffinityMask,
          dwPrio,
          dwStackSize));
#endif

    /*
     *  set thread attributes
     */
    nResult = pthread_attr_init(&ThreadAttr);
    if (0 != nResult)
    {
       EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "Create thread: pthread_attr_init() failed. Error: %d\n",
          nResult));
       goto FatalExit;
    }
    /* Set the stack size of the thread */
    dwStackSize = (dwStackSize < PTHREAD_STACK_MIN) ? PTHREAD_STACK_MIN : PAGE_UP(dwStackSize);
    nResult = pthread_attr_setstacksize(&ThreadAttr, dwStackSize);
    if (0 != nResult)
    {
       EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "Create thread: pthread_attr_setstacksize() failed. Error: %d\n",
          nResult));
       goto FatalExit;
    }
    /* Set thread to detached state. No need for pthread_join*/
    nResult = pthread_attr_setdetachstate(&ThreadAttr, PTHREAD_CREATE_DETACHED);
    if (0 != nResult)
    {
       EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "Create thread: pthread_attr_setdetachstate() failed. Error: %d\n",
          nResult));
       goto FatalExit;
    }
    nResult = pthread_attr_setinheritsched(&ThreadAttr, PTHREAD_EXPLICIT_SCHED);
    if (0 != nResult)
    {
       EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "Create thread: pthread_attr_setinheritsched() failed. Error: %d\n",
          nResult));
       goto FatalExit;
    }
    /*
     * Fill arguments for thread stub
     */
    arg->entry = pfThreadEntry;
    arg->arg = pvParams;
    strncpy(arg->name, szThreadName, sizeof(arg->name) - 1);
    arg->name[MAX_THREADNAME_LEN - 1] = '\0';
    arg->threadPrio = dwPrio & 0xFFFF;
    arg->cpuMask = dwPrio >> 16; /* Use high word of priority as CPU mask */

    /*
     *  create the thread
     */
    nResult = pthread_create( &pThread, &ThreadAttr, (void*(*)(void*))ThreadStub, arg );
    if(0 != nResult)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "Create thread: pthread_create() failed. Error: %d\n",
           nResult));
       goto FatalExit;
    }

    pvThreadObject = (EC_T_VOID*)pThread;

    /* is this the job task ? */
    if( OsStrcmp(szThreadName, "tEcJobTask") == 0)
    {
        S_JobTaskThread = pThread;
    }

    /* cpu affinity mask */
    if (0 != cpuAffinityMask)
    {
        OsSetThreadAffinity(pvThreadObject, cpuAffinityMask);
    }

    goto Exit;

FatalExit:
    delete arg;
Exit:
    pthread_attr_destroy( &ThreadAttr );
    return pvThreadObject;
}

/***************************************************************************************************/
/** \brief  Delete a thread Handle returned by OsCreateThread.
*
* \return N/A.
*/
EC_OS_API EC_T_DWORD EC_OS_API_FNCALL OsPlatformImplDeleteThreadHandle(
    EC_T_VOID* pvThreadObject       /**< [in]   Previously allocated Thread Handle */
                                            )
{
    /* reset job task handle */
    if ((EC_T_VOID*)S_JobTaskThread == pvThreadObject)
    {
        S_JobTaskThread = EC_NULL;
    }
    return EC_E_NOERROR;
}

/********************************************************************************/
/** \brief Set thread priority.
*
* \return N/A.
*/
EC_OS_API EC_T_DWORD EC_OS_API_FNCALL OsSetThreadPriority(EC_T_VOID* pvThreadObject, EC_T_DWORD dwPrio)
{
    pthread_attr_t ThreadAttr;
    int nSchedPolicy = SCHED_FIFO;    // scheduling policy - real time
    struct sched_param SchedParam;  // scheduling priority

    /* set thread attributes */
    /*************************/
    pthread_attr_init( &ThreadAttr );
    /* Set the policy of the thread to real time*/
    pthread_attr_setschedpolicy( &ThreadAttr, nSchedPolicy);
    /* Set the scheduling priority of the thread - (1 = lowest, 99 = highest) */
    SchedParam.sched_priority = dwPrio;
    pthread_attr_setschedparam( &ThreadAttr, &SchedParam );

    /* change thread priority */
    /**************************/
    pthread_setschedparam( (pthread_t)pvThreadObject, nSchedPolicy, &SchedParam );

    pthread_attr_destroy( &ThreadAttr );

    return EC_E_NOERROR;
}

/********************************************************************************/
/** \brief Set thread affinity.
 *
 * \return EC_TRUE if successful, EC_FALSE otherwise.
 */
EC_OS_API EC_T_DWORD EC_OS_API_FNCALL OsSetThreadAffinity(EC_T_VOID* pvThreadObject, EC_T_CPUSET cpuMask)
{
    pthread_t thread = (pvThreadObject == EC_NULL)
         ? pthread_self()
         : (pthread_t) pvThreadObject;

    cpu_set_t cpuSet = CpuMaskToSet(cpuMask);
    if (pthread_setaffinity_np(thread, sizeof(cpuSet), &cpuSet) < 0)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "pthread_setaffinity_np failed\n"));
        return EC_E_ERROR;
    }

    return EC_E_NOERROR;
}

/********************************************************************************/
/** \brief Get thread affinity.
*
* \return EC_TRUE if successful, EC_FALSE otherwise.
*/
EC_OS_API EC_T_DWORD EC_OS_API_FNCALL OsGetThreadAffinity(EC_T_VOID* pvThreadObject, EC_T_CPUSET* pCpuSet)
{
    pthread_t thread;
    if (pvThreadObject == NULL) thread = pthread_self();
    else                        thread = (pthread_t) pvThreadObject;

    if (pthread_getaffinity_np(thread, sizeof(EC_T_CPUSET), (cpu_set_t *) pCpuSet) < 0)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "pthread_getaffinity_np failed\n"));
        return EC_E_ERROR;
    }

    return EC_E_NOERROR;
}

/***************************************************************************************************/
/**
\brief  Replaces the built in Link Layer Driver Registration function

\return N/A
*/
EC_T_VOID OsPlatformImplReplaceGetLinkLayerRegFunc(EC_PF_GETLINKLAYERREGFUNC pfGetLinkLayerRegFunc)
{
    S_pfGetLinkLayerRegFunc = pfGetLinkLayerRegFunc;
}

/***************************************************************************************************/
/**
\brief  Get Link Layer Driver Registration function

This function returns the link layer registration function.
\return link layer registration function.
*/
EC_PF_LLREGISTER OsPlatformImplGetLinkLayerRegFunc(EC_T_CHAR* szDriverIdent, EC_T_CHAR* szLoadPath)
{
    EC_PF_LLREGISTER    pfRetVal = EC_NULL;
    EC_T_CHAR           szTmp[EC_OS_MAX_SODIR_LEN + 1];
    void*               pvLibHandle = EC_NULL;
    void*               pvSymbol = EC_NULL;
    char*               szError = NULL;
    EC_T_BOOL           bLoadStrict = (0 != OsStrlen(szLoadPath));
    EC_T_INT            nLoadTries = 2;
    EC_T_INT            nIndex = 2;

    szTmp[EC_OS_MAX_SODIR_LEN] = '\0';

    if (EC_NULL != S_pfGetLinkLayerRegFunc)
    {
        pfRetVal = (*S_pfGetLinkLayerRegFunc)(szDriverIdent, szLoadPath);
        goto Exit;
    }

    /* Clear any pending error message */
    dlerror();

    /* search LinkLayer first in specified loading path then in the current working directory
     * and then with ld library search path
     */
    for (nLoadTries = 2; 0 != nLoadTries; nLoadTries--)
    {
        if (bLoadStrict)
        {
            nLoadTries = 1;
            snprintf(szTmp, EC_OS_MAX_SODIR_LEN, "%s/libemll%s.so", szLoadPath, szDriverIdent);
        }
        else
        {
            if (2 == nLoadTries)
            {
                if (EC_NULL != getcwd(szTmp, EC_OS_MAX_SODIR_LEN))
                {
                    int nCwdStrLen = strlen(szTmp);
                    snprintf(szTmp + nCwdStrLen, EC_OS_MAX_SODIR_LEN - nCwdStrLen, "/libemll%s.so", szDriverIdent);
                }
                else
                {
                    continue;
                }
            }
            else
            {
                snprintf(szTmp, EC_OS_MAX_SODIR_LEN, "libemll%s.so", szDriverIdent);
            }
        }
        EcLogMsg(EC_LOG_LEVEL_VERBOSE, (pEcLogContext, EC_LOG_LEVEL_VERBOSE, "OsGetLinkLayerRegFunc: try to load '%s'\n", szTmp));
        pvLibHandle = dlopen(szTmp, RTLD_LAZY | RTLD_GLOBAL);
        if (EC_NULL != pvLibHandle)
        {
            break;
        }
    }
    if (NULL == pvLibHandle)
    {
        szError = dlerror();
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "OsGetLinkLayerRegFunc: dlopen returned error '%s'\n", ((NULL != szError) ? szError : "unknown")));
        EC_UNREFPARM(szError);
        goto Exit;
    }

    snprintf(szTmp, EC_OS_MAX_SODIR_LEN, "emllRegister%s", szDriverIdent);

    dlerror(); /* clear any pending error message */

    pvSymbol = dlsym(pvLibHandle, szTmp);
    if (EC_NULL == pvSymbol)
    {
        szError = dlerror();
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "ERROR: dlsym returned error '%s' when looking for symbol '%s'!\n", ((NULL != szError) ? szError : "unknown"), szTmp));
        goto Exit;
    }
    /* fill link layer registration entry */
    if (!S_bLinkLayerRegListInitialized)
    {
        OsMemset(S_aLinkLayerRegList, 0, sizeof(S_aLinkLayerRegList));
        S_bLinkLayerRegListInitialized = EC_TRUE;
    }
    for (nIndex = 0; nIndex < MAX_LINKLAYERREG_ENTRIES; nIndex++)
    {
        if (EC_NULL == S_aLinkLayerRegList[nIndex].pvLibHandle)
        {
            S_aLinkLayerRegList[nIndex].pvLibHandle = pvLibHandle;
            OsStrncpy(S_aLinkLayerRegList[nIndex].szDriverIdent, szDriverIdent, EC_DRIVER_IDENT_MAXLEN);
            S_aLinkLayerRegList[nIndex].szDriverIdent[EC_DRIVER_IDENT_MAXLEN] = '\0';
            break;
        }
    }

    pfRetVal = (EC_PF_LLREGISTER)pvSymbol;
Exit:
    return pfRetVal;
}

EC_T_VOID OsPlatformImplReleaseLinkLayerRegFunc(EC_T_CHAR* szDriverIdent)
{
    EC_T_INT nIndex = 0;

    if (!S_bLinkLayerRegListInitialized)
    {
        return;
    }
    for (nIndex = 0; nIndex < MAX_LINKLAYERREG_ENTRIES; nIndex++)
    {
        if (0 == OsStrcmp(S_aLinkLayerRegList[nIndex].szDriverIdent, szDriverIdent))
        {
            /* free library */
            dlclose(S_aLinkLayerRegList[nIndex].pvLibHandle);

            /* delete link layer registration entry */
            OsMemset(&S_aLinkLayerRegList[nIndex], 0, sizeof(LINKLAYERREG_ENTRY));

            break;
        }
    }
}

/***************************************************************************************************/
/**
\brief  Get current system time in nanoseconds

\return error code, EC_E_NOERROR in case of success
*/
EC_OS_API EC_T_DWORD EC_OS_API_FNCALL OsSystemTimeGet(EC_T_UINT64* pqwSystemTime)
{
    EC_T_DWORD dwRetVal = EC_E_ERROR;
    EC_T_DWORD dwRes    = EC_E_ERROR;

    /* check parameters */
    if (EC_NULL == pqwSystemTime)
    {
        dwRetVal = EC_E_INVALIDPARM;
        goto Exit;
    }
    /* get system time */
    if( EC_NULL != S_pfSystemTimeGet )
    {
        /* from configured function */
        dwRes = S_pfSystemTimeGet(pqwSystemTime);
        if (EC_E_NOERROR != dwRes)
        {
            dwRetVal = dwRes;
            goto Exit;
        }
    }
    else
    {
        /* from default */
        struct timespec ts;
        EC_T_UINT64 qwSec = 0;
        EC_T_UINT64 qwNsec = 0;

        clock_gettime(CLOCK_REALTIME, &ts);

        EC_SETQWORD(&qwSec, (EC_T_UINT64)ts.tv_sec);

        /* year 1970 (UNIX epoche) vs. 2000 (EtherCAT epoche) */
        qwSec = qwSec - 946684800ul;

        EC_SETQWORD(&qwNsec, (EC_T_UINT64)ts.tv_nsec);
        qwNsec = qwNsec + qwSec * 1000000000ul;

        EC_SETQWORD(pqwSystemTime, qwNsec);
    }

    /* no errors */
    dwRetVal = EC_E_NOERROR;

Exit:
    return dwRetVal;
}

static EC_T_BOOL   S_bCalibrated       = EC_FALSE;
static EC_T_DWORD  S_dw100kHzFrequency = 0; /* frequency in 100 kHz units (e.g. 1MHz = 10) */

/***************************************************************************************************/
/**
@brief  OsMeasCalibrate

Measure the TSC frequency for timing measurements. Must be called before using OsMeasGet100kHzFrequency().
*/
EC_OS_API EC_T_VOID EC_OS_API_FNCALL OsMeasCalibrate(EC_T_UINT64 qwHzFrequencySet)
{
    if (0 == qwHzFrequencySet)
    {
        /* auto-calibrate */
        if (!S_bCalibrated)
        {
            EC_T_UINT64 qwHzFrequency = 0;
            EC_T_UINT64 qwTimeStamp1 = 0;
            EC_T_UINT64 qwTimeStamp2 = 0;
            EC_T_UINT64 qwTimeStamp3 = 0;

            EcLogMsg(EC_LOG_LEVEL_VERBOSE, (pEcLogContext, EC_LOG_LEVEL_VERBOSE, "Calibrate PerfMeasCounter frequency... \n"));

            OsSleep(1);
            qwTimeStamp1 = OsMeasGetCounterTicks();

            OsSleep(1000);
            qwTimeStamp2 = OsMeasGetCounterTicks();

            OsSleep(2000);
            qwTimeStamp3 = OsMeasGetCounterTicks();

            qwHzFrequency = ((qwTimeStamp3 - qwTimeStamp2) / 2 + (qwTimeStamp2 - qwTimeStamp1)) / 2;
            S_dw100kHzFrequency = (EC_T_DWORD)(qwHzFrequency / 100000);

            EcLogMsg(EC_LOG_LEVEL_VERBOSE, (pEcLogContext, EC_LOG_LEVEL_VERBOSE, "done: %d MHz\n",
                (EC_T_INT)(qwHzFrequency / 1000000)));

            S_bCalibrated = EC_TRUE;
        }
    }
    else
    {
        S_dw100kHzFrequency = (EC_T_DWORD)(qwHzFrequencySet / 100000);
    }
}

/***************************************************************************************************/
/**
@brief  OsMeasGet100kHzFrequency

@return the frequency of the TSC in 100kHz multiples [EC_T_DWORD]
*/
EC_OS_API EC_T_DWORD EC_OS_API_FNCALL OsMeasGet100kHzFrequency(EC_T_VOID)
{
    EC_T_DWORD dwRetVal = 0;

    if (!S_bCalibrated)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "TscGet100kHzFrequency() TSC not calibrated\n"));
        goto Exit;
    }

    dwRetVal = S_dw100kHzFrequency;

Exit:
    return dwRetVal;
}

/***************************************************************************************************/
/**
@brief  OsMeasGetCounterTicks

@return the current TSC count [EC_T_UINT64]
*/
EC_OS_API EC_T_UINT64 EC_OS_API_FNCALL OsMeasGetCounterTicks(EC_T_VOID)
{
    EC_T_DWORD   dwTimeStampLo = 0;
    EC_T_DWORD   dwTimeStampHi = 0;

#if defined(__GNUC__) && (defined(__i386__) || defined(__x86_64__))
    __asm__ volatile (
             "rdtsc"
             : "=a" (dwTimeStampLo), "=d" (dwTimeStampHi)
             );
#elif defined(__GNUC__) && defined(__PPC__)
    {
       EC_T_DWORD dwTmp = 0;

       /* Read PowerPC architecture's time base register.
        * The following code reads the high dword 2 times and
        * loops if they are not equal (check for rollover).
        */
      __asm__ volatile (
                 "0:                   \n"
                 "\tmftbu   %0         \n" /* Read high word (dwTimeStampHi) */
                 "\tmftb    %1         \n" /* Read low word (dwTimeStampLo) */
                 "\tmftbu   %2         \n" /* Read high word again (dwTmp) */
                 "\tcmpw    %2,%0      \n" /* compare (dwTimeStampHi) and (dwTmp). Check for rollover */
                 "\tbne     0b         \n" /* jump if not equal to label 0: */
                 : "=r"(dwTimeStampHi),"=r"(dwTimeStampLo),"=r"(dwTmp)
                 );
    }
#else

    struct timespec TimeStamp;
    clock_gettime(CLOCK_MONOTONIC, &TimeStamp);

    EC_T_UINT64 qwTimeStampNsec = TimeStamp.tv_nsec;
    EC_T_UINT64 qwTimeStampSec  = TimeStamp.tv_sec;
    EC_T_UINT64 qwTimeStamp     = qwTimeStampNsec + qwTimeStampSec * 1000000000;

    return qwTimeStamp;

#endif
    return EC_MAKEQWORD(dwTimeStampHi, dwTimeStampLo);
}

#if (defined EC_SOCKET_IP_SUPPORTED)
EC_OS_API EC_T_DWORD EC_OS_API_FNCALL OsSocketInit(EC_T_VOID)
{
    return EC_E_NOERROR;
}

EC_OS_API EC_T_DWORD EC_OS_API_FNCALL OsSocketDeInit(EC_T_VOID)
{
    return EC_E_NOERROR;
}
#endif /* EC_SOCKET_IP_SUPPORTED */

#if (defined EC_OS_NAMESPACE)
} /* namespace EC_OS_NAMESPACE */
#endif

/*-END OF SOURCE FILE--------------------------------------------------------*/

