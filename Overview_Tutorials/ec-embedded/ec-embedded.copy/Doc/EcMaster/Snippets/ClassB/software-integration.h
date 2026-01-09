namespace EcMasterTests { namespace DocumentationSnippets {

IGNORE_TEST(DocumentationSnippets, Timing_CycFramesPolling)
{
    EC_T_USER_JOB_PARMS oJobParms;

    /* Job P: Process data are saved in the process data image */
    emExecJob(dwInstanceId, eUsrJob_ProcessAllRxFrames, &oJobParms);

    /* App. Task */

    /* Job S: Send updated process data. 
       Outputs are updated in slaves and input data is collected to be present for the next cycle. 
       The process data image is saved during eUsrJob_ProcessAllRxFrames */
    emExecJob(dwInstanceId, eUsrJob_SendAllCycFrames, EC_NULL);

    /* Job MT: Trigger master state machines. 
       Required to perform any status changes or internal administration tasks */
    emExecJob(dwInstanceId, eUsrJob_MasterTimer, EC_NULL);
/* IGNORE_TEST(DocumentationSnippets, Timing_CycFramesPolling) */
}
IGNORE_TEST(DocumentationSnippets, Timing_CycAcycFramesPolling)
{
    EC_T_USER_JOB_PARMS oJobParms;

    /* Job P: Process data are saved in the process data image */
    emExecJob(dwInstanceId, eUsrJob_ProcessAllRxFrames, &oJobParms);

    /* App. Task */

    /* Job S: Send updated process data. 
       Outputs are updated in slaves and input data is collected to be present for the next cycle. 
       The process data image is saved during eUsrJob_ProcessAllRxFrames */
    emExecJob(dwInstanceId, eUsrJob_SendAllCycFrames, EC_NULL);

    /* Job MT: Trigger master state machines. 
       Required to perform any status changes or internal administration tasks */
    emExecJob(dwInstanceId, eUsrJob_MasterTimer, EC_NULL);

    /* Job AS: Transmission of the acyclic commands from the queue. 
       These may have been queued by the application or by the internal administration task (eUsrJob_MasterTimer) */
    emExecJob(dwInstanceId, eUsrJob_SendAcycFrames, EC_NULL);
/* IGNORE_TEST(DocumentationSnippets, Timing_CycAcycFramesPolling) */
}
IGNORE_TEST(DocumentationSnippets, Timing_CycAcycFramesInterrupt)
{
    EC_PF_CYCFRAME_RECV CycFrameReceivedCallback = EC_NULL; EC_T_VOID* S_pvCycFrameReceivedEvent = EC_NULL; 
    EC_T_VOID* S_pvtJobThread; EC_PF_THREADENTRY EcMasterJobTask = EC_NULL; EC_T_CPUSET CpuSet = 0; EC_T_VOID* pAppContext = EC_NULL;
    EC_T_DWORD dwCycleTime = 0;

/* IGNORE_TEST(DocumentationSnippets, Timing_CycAcycFramesInterrupt)_Setup */
    emInitMaster(dwInstanceId, &oInitMasterParms);

    /* create event for "cyclic frame received" and register RX callback function */
    {
        EC_T_CYCFRAME_RX_CBDESC oCycFrameRxCallbackDesc;

        S_pvCycFrameReceivedEvent = OsCreateEvent();

        /* setup callback function which is called after RX */
        OsMemset(&oCycFrameRxCallbackDesc, 0, sizeof(EC_T_CYCFRAME_RX_CBDESC));
        oCycFrameRxCallbackDesc.pfnCallback = CycFrameReceivedCallback;
        oCycFrameRxCallbackDesc.pCallbackContext = S_pvCycFrameReceivedEvent;

        emIoCtl(dwInstanceId, EC_IOCTL_REGISTER_CYCFRAME_RX_CB, &oCycFrameRxCallbackDesc, sizeof(EC_T_CYCFRAME_RX_CBDESC), EC_NULL, 0, EC_NULL);
    }
    /* create cyclic process data Thread */
    S_pvtJobThread = OsCreateThread((EC_T_CHAR*)"EcMasterJobTask", EcMasterJobTask, CpuSet,
        JOBS_THREAD_PRIO, JOBS_THREAD_STACKSIZE, (EC_T_VOID*)pAppContext);
/* IGNORE_TEST(DocumentationSnippets, Timing_CycAcycFramesInterrupt)_Setup */

/* IGNORE_TEST(DocumentationSnippets, Timing_CycAcycFramesInterrupt)_JobTask */
    /* Job S: Send updated process data.
       Outputs are updated in slaves and input data is collected to be present for the current cycle.
       The process data image is saved after receiving the response frame within the interrupt service thread */
    emExecJob(dwInstanceId, eUsrJob_SendAllCycFrames, EC_NULL);

    /* wait until cyclic frame is received */
    OsWaitForEvent(S_pvCycFrameReceivedEvent, dwCycleTime);

    /* App. Task */

    /* Job MT: Trigger master state machines.
       Required to perform any status changes or internal administration tasks */
    emExecJob(dwInstanceId, eUsrJob_MasterTimer, EC_NULL);

    /* Job AS: Transmission of the acyclic commands from the queue.
       These may have been queued by the application or by the internal administration task (eUsrJob_MasterTimer) */
    emExecJob(dwInstanceId, eUsrJob_SendAcycFrames, EC_NULL);
/* IGNORE_TEST(DocumentationSnippets, Timing_CycAcycFramesInterrupt)_JobTask */
    EC_UNREFPARM(S_pvtJobThread);
}

IGNORE_TEST(DocumentationSnippets, ModeOfOperation_Degraded)
{
    /* IGNORE_TEST(DocumentationSnippets, ModeOfOperation_Degraded)_Setup */
    
    dwRes = emInitMaster(dwInstanceId, &oInitMasterParms);

    /* expected WKC should automatically ajusted according the presence and state of the slaves */
    EC_T_BOOL bSetAutoAdjustCycCmdWkcEnabled = EC_TRUE;
    dwRes = emIoCtl(dwInstanceId, EC_IOCTL_SET_AUTO_ADJUST_CYCCMD_WKC_ENABLED, (EC_T_BYTE*)&bSetAutoAdjustCycCmdWkcEnabled, sizeof(EC_T_BOOL), EC_NULL, 0, EC_NULL);

    /* configure master */
    const EC_T_CHAR* szEniFilename = "EniFile.xml";
    dwRes = emConfigureNetwork(dwInstanceId, eCnfType_Filename, (EC_T_BYTE*)szEniFilename, (EC_T_DWORD)OsStrlen(szEniFilename));

    /* scan bus */
    dwRes = emScanBus(dwInstanceId, 10000);
    if (dwRes == EC_E_BUSCONFIG_MISMATCH)
    {
        /* activate degraded mode of operation */
        EC_T_BOOL bAllSlavesMustReachMasterstate = EC_FALSE;
        dwRes = emIoCtl(dwInstanceId, EC_IOCTL_ALL_SLAVES_MUST_REACH_MASTER_STATE, (EC_T_BYTE*)&bAllSlavesMustReachMasterstate, sizeof(EC_T_BOOL), EC_NULL, 0, EC_NULL);
    }
    /* set all the slaves to OP even if slaves are missing */
    dwRes = emSetMasterState(dwInstanceId, 5000, eEcatState_OP);

    /* IGNORE_TEST(DocumentationSnippets, ModeOfOperation_Degraded) */
}

namespace DocumentationSnippetsPdAccessHardCodedOffsetsExample
{
    static EC_T_DWORD myAppWorkpd(T_EC_DEMO_APP_CONTEXT* pAppContext)
    {
        EC_T_DWORD dwInstanceId = pAppContext->dwInstanceId;
        EC_T_BYTE* pbyPdIn = emGetProcessImageInputPtr(dwInstanceId);
        EC_T_BYTE* pbyPdOut = emGetProcessImageOutputPtr(dwInstanceId);

        /* Slave_1002 [EC-Training Generator].Counter1.Value (Offset: 9.0) */
        EC_T_SDWORD sdwCounter1_Value = EC_GET_FRM_DWORD(&pbyPdIn[9 /* 9.0 */]);
        EcLogMsg(EC_LOG_LEVEL_INFO, (pEcLogContext, EC_LOG_LEVEL_INFO, 
            "Counter1.Value: %d\n", sdwCounter1_Value));

        /* Slave_1002 [EC-Training Generator].Counter1.Enable (Offset: 11.0) */
        EC_T_BYTE byCounter1_Enable = 1;
        EC_COPYBIT(&pbyPdOut[11], 0 /* 11.0 */, byCounter1_Enable);

        /* Slave_1002 [EC-Training Generator].Counter1.Increment (Offset: 9.0) */
        EC_T_SWORD swCounter1_Increment = 100;
        EC_SET_FRM_WORD(&pbyPdIn[9 /* 9.0 */], swCounter1_Increment);

        return EC_E_NOERROR;
    }
} /* DocumentationSnippetsPdAccessHardCodedOffsetsExample */
IGNORE_TEST(DocumentationSnippets, PdAccess_HardCodedOffsets)
{
    DocumentationSnippetsPdAccessHardCodedOffsetsExample::myAppWorkpd(EC_NULL);
}

/* DocumentationSnippetsPdAccessGeneratedPdLayoutHeaderStructure */
#include EC_PACKED_INCLUDESTART(1)
#define PDLAYOUT_IN_OFFSET_SLAVE_1002 9
typedef struct _T_PDLAYOUT_IN_SLAVE_1002
{
    EC_T_SDWORD sdwCounter1_Value;       // Slave_1002 ...Counter1.Value
    EC_T_SWORD  swCounter1_NetworkClock; // Slave_1002 ...Counter1.NetworkClock
    EC_T_SDWORD sdwCounter2_Value;       // Slave_1002 ...Counter2.Value
    EC_T_SWORD  swCounter2_NetworkClock; // Slave_1002 ...Counter2.NetworkClock
} EC_PACKED(1) T_PDLAYOUT_IN_SLAVE_1002;
#include EC_PACKED_INCLUDESTOP

#include EC_PACKED_INCLUDESTART(1)
#define PDLAYOUT_OUT_OFFSET_SLAVE_1002 9
typedef struct _T_PDLAYOUT_OUT_SLAVE_1002
{
    EC_T_SWORD  swCounter1_Increment;    // Slave_1002 ...Counter1.Increment
    EC_T_BYTE   byCounter1_Enable : 1;   // Slave_1002 ...Counter1.Enable
    //...
} EC_PACKED(1) T_PDLAYOUT_OUT_SLAVE_1002;
#include EC_PACKED_INCLUDESTOP
/* DocumentationSnippetsPdAccessGeneratedPdLayoutHeaderStructure */

namespace DocumentationSnippetsPdAccessGeneratedPdLayoutHeaderExample
{
    #include "pdlayout.h"
    static EC_T_DWORD myAppWorkpd(T_EC_DEMO_APP_CONTEXT* pAppContext)
    {
        EC_T_DWORD dwInstanceId = pAppContext->dwInstanceId;
        T_PDLAYOUT_IN* poPdIn = (T_PDLAYOUT_IN*)emGetProcessImageInputPtr(dwInstanceId);
        T_PDLAYOUT_OUT* poPdOut = (T_PDLAYOUT_OUT*)emGetProcessImageOutputPtr(dwInstanceId);

        /* Slave_1002 [EC-Training Generator].Counter1.Value (Offset: 9.0) */
        EcLogMsg(EC_LOG_LEVEL_INFO, (pEcLogContext, EC_LOG_LEVEL_INFO,
            "Counter1.Value: %d\n", EC_GET_FRM_DWORD(&poPdIn->sdwSlave_1002_Counter1_Value)));

        /* Slave_1002 [EC-Training Generator].Counter1.Enable (Offset: 11.0) */
        poPdOut->bySlave_1002_Counter1_Enable = 1;

        /* Slave_1002 [EC-Training Generator].Counter1.Increment (Offset: 9.0) */
        EC_SET_FRM_WORD(&poPdOut->swSlave_1002_Counter1_Increment, 100);

        return EC_E_NOERROR;
    }
} /* DocumentationSnippetsPdAccessGeneratedPdLayoutHeaderExample */
#undef PDLAYOUT_H
#undef PDLAYOUT_IN_OFFSET_SLAVE_1001
#undef PDLAYOUT_IN_OFFSET_SLAVE_1002
IGNORE_TEST(DocumentationSnippets, PdAccess_GeneratedLayout)
{
    DocumentationSnippetsPdAccessGeneratedPdLayoutHeaderExample::myAppWorkpd(EC_NULL);
}

namespace DocumentationSnippetsPdAccessGeneratedCustomPdLayoutHeaderStructure
{
#include EC_PACKED_INCLUDESTART(1)
#define PDLAYOUT_OUT_OFFSET_EC_TRAINING_SAMPLER 0
typedef struct _T_PDLAYOUT_OUT_EC_TRAINING_SAMPLER
{
    EC_T_BYTE   byOutputDigital_Bit0 : 1;   // ...
    EC_T_BYTE   byOutputDigital_Bit1 : 1;   // ...
    EC_T_BYTE   byOutputDigital_Bit2 : 1;   // ...
    EC_T_BYTE   byOutputDigital_Bit3 : 1;   // ...
    EC_T_BYTE   byOutputDigital_Bit4 : 1;   // ...
    EC_T_BYTE   byOutputDigital_Bit5 : 1;   // ...
    EC_T_BYTE   byOutputDigital_Bit6 : 1;   // ...
    EC_T_BYTE   byOutputDigital_Bit7 : 1;   // ...
    EC_T_SWORD  swOutputAnalog_SpeedFactor; // ...
    EC_T_SWORD  swOutputAnalog_Reserved_2;  // ...
    EC_T_SWORD  swOutputAnalog_Reserved_3;  // ...
    EC_T_SWORD  swOutputAnalog_Reserved_4;  // ...
} EC_PACKED(1) T_PDLAYOUT_OUT_EC_TRAINING_SAMPLER;
#include EC_PACKED_INCLUDESTOP
} /* namespace DocumentationSnippetsPdAccessGeneratedCustomPdLayoutHeaderStructure */

namespace DocumentationSnippetsPdAccessGeneratedCustomPdLayoutHeaderExample
{
    #include "pdlayoutcustom.h"
    static EC_T_DWORD myAppWorkpd(T_EC_DEMO_APP_CONTEXT* pAppContext)
    {
        EC_T_DWORD dwInstanceId = pAppContext->dwInstanceId;
        T_PDLAYOUT_IN* poPdIn = (T_PDLAYOUT_IN*)emGetProcessImageInputPtr(dwInstanceId);
        T_PDLAYOUT_OUT* poPdOut = (T_PDLAYOUT_OUT*)emGetProcessImageOutputPtr(dwInstanceId);

        /* EC-Training-Generator.Counter1.Value (Offset: 9.0, Size: 4.0, Datatype: DINT) */
        EcLogMsg(EC_LOG_LEVEL_INFO, (pEcLogContext, EC_LOG_LEVEL_INFO,
            "Counter1.Value: %d\n", EC_GET_FRM_DWORD(&poPdIn->sdwEC_Training_Generator_Counter1_Value_Counter1_Value)));

        /* EC-Training-Generator.Counter1.Enable (Offset: 11.0, Size: 0.1, Datatype: BOOL) */
        poPdOut->byEC_Training_Generator_Counter1_Enable_Counter1_Enable = 1;

        /* EC-Training-Generator.Counter1.Increment (Offset: 9.0, Size: 2.0, Datatype: INT) */
        EC_SET_FRM_WORD(&poPdOut->swEC_Training_Generator_Counter1_Increment_Counter1_Increment, 100);

        return EC_E_NOERROR;
    }
} /* DocumentationSnippetsPdAccessGeneratedCustomPdLayoutHeaderExample */
#undef PDLAYOUT_H
#undef PDLAYOUT_IN_OFFSET_EC_TRAINING_SAMPLER
#undef PDLAYOUT_IN_OFFSET_EC_TRAINING_GENERATOR
IGNORE_TEST(DocumentationSnippets, PdAccess_GeneratedCustomPdLayout)
{
    DocumentationSnippetsPdAccessGeneratedCustomPdLayoutHeaderExample::myAppWorkpd(EC_NULL);
}

namespace DocumentationSnippetsPdAccessGetCfgSlaveInfoExample
{
    static EC_T_DWORD myAppPrepare(T_EC_DEMO_APP_CONTEXT* pAppContext)
    {
        EC_T_DWORD dwRetVal       = EC_E_NOERROR;
        EC_T_DWORD dwInstanceId   = pAppContext->dwInstanceId;
        T_MY_APP_DESC* pMyAppDesc = pAppContext->pMyAppDesc;
        OsMemset(pMyAppDesc->aSlaveList, 0, sizeof(pMyAppDesc->aSlaveList));

        dwRetVal = emGetCfgSlaveInfo(dwInstanceId, EC_TRUE, 1001, &pMyAppDesc->aSlaveList[0]);
        if (EC_E_NOERROR != dwRetVal)
            return dwRetVal;

        dwRetVal = emGetCfgSlaveInfo(dwInstanceId, EC_TRUE, 1002, &pMyAppDesc->aSlaveList[1]);
        if (EC_E_NOERROR != dwRetVal)
            return dwRetVal;

        return EC_E_NOERROR;
    }
    static EC_T_DWORD myAppWorkpd(T_EC_DEMO_APP_CONTEXT* pAppContext)
    {
        EC_T_DWORD dwInstanceId = pAppContext->dwInstanceId;
        T_MY_APP_DESC* pMyAppDesc = pAppContext->pMyAppDesc;

        EC_T_BYTE* pbyPdIn = emGetProcessImageInputPtr(dwInstanceId);
        EC_T_BYTE* pbyPdOut = emGetProcessImageOutputPtr(dwInstanceId);

        /* Slave_1002 [EC-Training Generator].Counter1.Value (first INPUT variable) */
        EC_T_SDWORD* psdwCounter1Value = (EC_T_SDWORD*)&(pbyPdIn[pMyAppDesc->aSlaveList[1].dwPdOffsIn / 8]);

        EcLogMsg(EC_LOG_LEVEL_INFO, (pEcLogContext, EC_LOG_LEVEL_INFO,
            "Counter1.Value: %d\n", EC_GET_FRM_DWORD(psdwCounter1Value)));

        /* Slave_1002 [EC-Training Generator].Counter1.Increment (first OUTPUT variable) */
        EC_T_SWORD* pswCounter1Increment = (EC_T_SWORD*)&(pbyPdOut[pMyAppDesc->aSlaveList[1].dwPdOffsOut / 8]);
        EC_SET_FRM_WORD(pswCounter1Increment, 100);

        return EC_E_NOERROR;
    }
} /* DocumentationSnippetsPdAccessGetCfgSlaveInfoExample */
IGNORE_TEST(DocumentationSnippets, PdAccess_GetCfgSlaveInfo)
{
    DocumentationSnippetsPdAccessGetCfgSlaveInfoExample::myAppPrepare(EC_NULL);
    DocumentationSnippetsPdAccessGetCfgSlaveInfoExample::myAppWorkpd(EC_NULL);
}
namespace DocumentationSnippetsPdAccessFindOutpVarByNameExExample
{
    struct _T_MY_APP_DESC;
    typedef struct _T_EC_DEMO_APP_CONTEXT
    {
        T_EC_DEMO_APP_PARMS    AppParms;    
        EC_T_LOG_PARMS         LogParms;    
        EC_T_DWORD             dwInstanceId;
        struct _T_MY_APP_DESC* pMyAppDesc;
    } T_EC_DEMO_APP_CONTEXT;

    typedef struct _T_MY_APP_DESC
    {
        EC_T_PROCESS_VAR_INFO_EX aoProcVarInfo[3];
    } T_MY_APP_DESC;

    static EC_T_DWORD myAppPrepare(T_EC_DEMO_APP_CONTEXT* pAppContext)
    {
        EC_T_DWORD dwRetVal = EC_E_NOERROR;
        EC_T_DWORD dwInstanceId = pAppContext->dwInstanceId;
        T_MY_APP_DESC* pMyAppDesc = pAppContext->pMyAppDesc;
        EC_T_PROCESS_VAR_INFO_EX* aoProcVarInfo = pMyAppDesc->aoProcVarInfo;

        OsMemset(pMyAppDesc->aoProcVarInfo, 0, sizeof(pMyAppDesc->aoProcVarInfo));

        dwRetVal = emFindInpVarByNameEx(dwInstanceId, "Slave_1002 [EC-Training Generator].Counter1.Value", &aoProcVarInfo[0]);
        if (EC_E_NOERROR != dwRetVal)
            return dwRetVal;

        dwRetVal = emFindOutpVarByNameEx(dwInstanceId, "Slave_1002 [EC-Training Generator].Counter1.Enable", &aoProcVarInfo[1]);
        if (EC_E_NOERROR != dwRetVal)
            return dwRetVal;

        dwRetVal = emFindOutpVarByNameEx(dwInstanceId, "Slave_1002 [EC-Training Generator].Counter1.Increment", &aoProcVarInfo[2]);
        if (EC_E_NOERROR != dwRetVal)
            return dwRetVal;

        return EC_E_NOERROR;
    }
    static EC_T_DWORD myAppWorkpd(T_EC_DEMO_APP_CONTEXT* pAppContext)
    {
        EC_T_DWORD dwInstanceId = pAppContext->dwInstanceId;
        T_MY_APP_DESC* pMyAppDesc = pAppContext->pMyAppDesc;
        EC_T_PROCESS_VAR_INFO_EX* aoProcVarInfo = pMyAppDesc->aoProcVarInfo;

        EC_T_BYTE* pbyPdIn = emGetProcessImageInputPtr(dwInstanceId);
        EC_T_BYTE* pbyPdOut = emGetProcessImageOutputPtr(dwInstanceId);

        /* Slave_1002 [EC-Training Generator].Counter1.Value (Offset: 9.0) */
        EcLogMsg(EC_LOG_LEVEL_INFO, (pEcLogContext, EC_LOG_LEVEL_INFO,
            "Counter1.Value: %d\n", EC_GET_FRM_DWORD(&pbyPdIn[aoProcVarInfo[0].nBitOffs / 8])));

        /* Slave_1002 [EC-Training Generator].Counter1.Enable (Offset: 11.0) */
        EC_SETBIT(pbyPdOut, aoProcVarInfo[1].nBitOffs);

        /* Slave_1002 [EC-Training Generator].Counter1.Increment (Offset: 9.0) */
        EC_SET_FRM_WORD(&pbyPdOut[aoProcVarInfo[2].nBitOffs / 8], 100);

        return EC_E_NOERROR;
    }
} /* DocumentationSnippetsPdAccessFindOutpVarByNameExExample */
IGNORE_TEST(DocumentationSnippets, PdAcces_FindOutpVarByNameEx)
{
    DocumentationSnippetsPdAccessFindOutpVarByNameExExample::myAppPrepare(EC_NULL);
    DocumentationSnippetsPdAccessFindOutpVarByNameExExample::myAppWorkpd(EC_NULL);
}

namespace DocumentationSnippetsPdAccessGetSlaveOutpVarByObjectExExample
{
    struct _T_MY_APP_DESC;
    typedef struct _T_EC_DEMO_APP_CONTEXT
    {
        T_EC_DEMO_APP_PARMS    AppParms;
        EC_T_LOG_PARMS         LogParms;
        EC_T_DWORD             dwInstanceId;
        struct _T_MY_APP_DESC* pMyAppDesc;
    } T_EC_DEMO_APP_CONTEXT;

    typedef struct _T_MY_APP_DESC
    {
        EC_T_PROCESS_VAR_INFO_EX aoProcVarInfo[3];
    } T_MY_APP_DESC;

    static EC_T_DWORD myAppPrepare(T_EC_DEMO_APP_CONTEXT* pAppContext)
    {
        EC_T_DWORD dwRetVal = EC_E_NOERROR;
        EC_T_DWORD dwInstanceId = pAppContext->dwInstanceId;
        T_MY_APP_DESC* pMyAppDesc = pAppContext->pMyAppDesc;
        EC_T_PROCESS_VAR_INFO_EX* aoProcVarInfo = pMyAppDesc->aoProcVarInfo;

        OsMemset(pMyAppDesc->aoProcVarInfo, 0, sizeof(pMyAppDesc->aoProcVarInfo));

        /* Slave_1002 [EC-Training Generator].Counter1.Value (Object 0x6000:01) */
        dwRetVal = emGetSlaveInpVarByObjectEx(dwInstanceId, EC_TRUE, 1002, 0x6000, 1, &aoProcVarInfo[0]);
        if (EC_E_NOERROR != dwRetVal)
            return dwRetVal;

        /* Slave_1002 [EC-Training Generator].Counter1.Enable (Object 0x7000:01) */
        dwRetVal = emGetSlaveOutpVarByObjectEx(dwInstanceId, EC_TRUE, 1002, 0x7000, 1, &aoProcVarInfo[1]);
        if (EC_E_NOERROR != dwRetVal)
            return dwRetVal;

        /* Slave_1002 [EC-Training Generator].Counter1.Increment (Object 0x7000:02) */
        dwRetVal = emGetSlaveOutpVarByObjectEx(dwInstanceId, EC_TRUE, 1002, 0x7000, 2, &aoProcVarInfo[2]);
        if (EC_E_NOERROR != dwRetVal)
            return dwRetVal;

        return EC_E_NOERROR;
    }
    static EC_T_DWORD myAppWorkpd(T_EC_DEMO_APP_CONTEXT* pAppContext)
    {
        EC_T_DWORD dwInstanceId = pAppContext->dwInstanceId;
        T_MY_APP_DESC* pMyAppDesc = pAppContext->pMyAppDesc;
        EC_T_PROCESS_VAR_INFO_EX* aoProcVarInfo = pMyAppDesc->aoProcVarInfo;

        EC_T_BYTE* pbyPdIn = emGetProcessImageInputPtr(dwInstanceId);
        EC_T_BYTE* pbyPdOut = emGetProcessImageOutputPtr(dwInstanceId);

        /* Slave_1002 [EC-Training Generator].Counter1.Value (Object 0x6000:01) */
        EcLogMsg(EC_LOG_LEVEL_INFO, (pEcLogContext, EC_LOG_LEVEL_INFO,
            "Counter1.Value: %d\n", EC_GET_FRM_DWORD(&pbyPdIn[aoProcVarInfo[0].nBitOffs / 8])));

        /* Slave_1002 [EC-Training Generator].Counter1.Enable (Object 0x7000:01) */
        EC_SETBIT(pbyPdOut, aoProcVarInfo[1].nBitOffs);

        /* Slave_1002 [EC-Training Generator].Counter1.Increment (Object 0x7000:02) */
        EC_SET_FRM_WORD(&pbyPdOut[aoProcVarInfo[2].nBitOffs / 8], 100);

        return EC_E_NOERROR;
    }
} /* DocumentationSnippetsPdAccessGetSlaveOutpVarByObjectExExample */
IGNORE_TEST(DocumentationSnippets, PdAcces_GetSlaveOutpVarByObjectEx)
{
    DocumentationSnippetsPdAccessGetSlaveOutpVarByObjectExExample::myAppPrepare(EC_NULL);
    DocumentationSnippetsPdAccessGetSlaveOutpVarByObjectExExample::myAppWorkpd(EC_NULL);
}

IGNORE_TEST(DocumentationSnippets, TraceData_ConfigViaApi)
{
    /* IGNORE_TEST(DocumentationSnippets, TraceData_ConfigViaApi)_Config */
    //emInitMaster();

    emTraceDataConfig(dwInstanceId, sizeof(EC_T_DWORD));
    
    //emConfigureNetwork;
    /* IGNORE_TEST(DocumentationSnippets, TraceData_ConfigViaApi)_Config */

    /* IGNORE_TEST(DocumentationSnippets, TraceData_ConfigViaApi)_GetInfo */
    EC_T_TRACE_DATA_INFO oTraceDataInfo;
    emTraceDataGetInfo(dwInstanceId, &oTraceDataInfo);
    
    EC_SET_FRM_DWORD(oTraceDataInfo.pbyData + oTraceDataInfo.dwOffset, 0x11223344);
    /* IGNORE_TEST(DocumentationSnippets, TraceData_ConfigViaApi)_GetInfo */
}
IGNORE_TEST(DocumentationSnippets, CoeSdoUploadReq)
{
    dwClientId = 0;  /* see RegisterClientResults.dwClntId from emRegisterClient() */
    EC_T_DWORD        dwSlaveId = 0;
    EC_T_MBXTFER*     pMbxTferObject = EC_NULL;
    EC_T_BYTE         abyObjectDataBuffer[] = { 0, 0, 0, 0 };
    EC_T_MBXTFER_DESC oObjectDataTferDesc;
    OsMemset(&oObjectDataTferDesc, 0, sizeof(EC_T_MBXTFER_DESC));

    /* we are going to use the slave with station address 1006 */
    dwSlaveId = ecatGetSlaveId(1006);
    oObjectDataTferDesc.pbyMbxTferDescData = abyObjectDataBuffer;
    oObjectDataTferDesc.dwMaxDataLen = sizeof(abyObjectDataBuffer); 

    pMbxTferObject = ecatMbxTferCreate(&oObjectDataTferDesc);
    if (EC_NULL == pMbxTferObject)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "Error creating the mailbox transfer object \n"));
    }

    pMbxTferObject->dwClntId = dwClientId;
    pMbxTferObject->dwTferId = 1; /* should be unique for each transfer request, use an increment for example */

    /* Make a CoeSdoUploadRequest of object index 0x1018, subindex 1, timeout 5s */
    dwRes = ecatCoeSdoUploadReq(pMbxTferObject, dwSlaveId, 0x1018, 1, 5000, 0);
    if (EC_E_NOERROR != dwRes)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "Upload request was not successful \n"));
    }
    /*IGNORE_TEST(DocumentationSnippets, CoeSdoUploadReq)*/
}
} } /* namespace EcMasterTests::DocumentationSnippets */
