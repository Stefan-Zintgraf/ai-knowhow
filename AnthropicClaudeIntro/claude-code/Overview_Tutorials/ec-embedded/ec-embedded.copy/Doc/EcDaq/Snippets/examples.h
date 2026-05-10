#include <EcDaq.h>

namespace EcMasterTests { namespace DocumentationSnippets {
IGNORE_TEST(DocumentationSnippets, DaqConfigAddTriggerByValue_Greater)
{
    /* Recording is stopped. Recording will be started, if variable “myVariable” is greater than 1: */

    ecDaqConfigAddTriggerByValue(hDaq, EC_NULL, "myVariable", "1", eDaqOperator_Greater, EC_TRUE /* bEnable */, EC_TRUE /* bStart */);

    /* IGNORE_TEST(DocumentationSnippets, DaqConfigAddTriggerByValue_Greater) */
}

IGNORE_TEST(DocumentationSnippets, DaqConfigAddTriggerByValue_GreaterDuration)
{
    /* Recording is stopped. Recording will be started for 1000ms, if variable “myVariable” is greater than 1 (after 1000ms recording will be automatically stopped): */

    ecDaqConfigAddTriggerByValue(hDaq, EC_NULL, "myVariable", "1", eDaqOperator_Greater, EC_TRUE /* bEnable */, EC_TRUE /* bStart */, 1000 /* dwDuration */);

    /* IGNORE_TEST(DocumentationSnippets, DaqConfigAddTriggerByValue_GreaterDuration) */
}

IGNORE_TEST(DocumentationSnippets, DaqConfigAddTriggerByValue_GreaterDurationCnt)
{
    /* Recording is stopped. Recording will be started for 1000ms, if variable “myVariable” is greater than 1. This will happen for 10 times, afterwards this trigger will be automatically disabled: */

    ecDaqConfigAddTriggerByValue(hDaq, EC_NULL, "myVariable", "1", eDaqOperator_Greater, EC_TRUE /* bEnable */, EC_TRUE /* bStart */, 1000 /* dwDuration */, 10 /* dwCount */);

    /* IGNORE_TEST(DocumentationSnippets, DaqConfigAddTriggerByValue_GreaterDurationCnt) */
}

IGNORE_TEST(DocumentationSnippets, DaqConfigAddTriggerByValue_Smaller)
{
    /* Recording is started. This will stop recording, if variable “myVariable” is smaller than 1: */

    ecDaqConfigAddTriggerByValue(hDaq, EC_NULL, "myVariable", "1", eDaqOperator_Smaller, EC_TRUE /* bEnable */, EC_FALSE /* bStart */);

    /* IGNORE_TEST(DocumentationSnippets, DaqConfigAddTriggerByValue_Smaller) */
}

IGNORE_TEST(DocumentationSnippets, DaqConfigAddTriggerByValue_EnableDisable)
{
    /* Recording is stopped.This will start recording, if “myVariable1” or “myVariable2” is 1 and recording will be stopped, if “myVarible1” or “myVarible2” is 0: */

    ecDaqConfigAddTriggerByValue(hDaq, EC_NULL, "myVariable1", "1", eDaqOperator_Equal, EC_TRUE /* bEnable */, EC_TRUE /* bStart */);
    ecDaqConfigAddTriggerByValue(hDaq, EC_NULL, "myVariable2", "1", eDaqOperator_Equal, EC_TRUE /* bEnable */, EC_TRUE /* bStart */);
    ecDaqConfigAddTriggerByValue(hDaq, EC_NULL, "myVariable1", "0", eDaqOperator_Equal, EC_TRUE /* bEnable */, EC_FALSE /* bStart */);
    ecDaqConfigAddTriggerByValue(hDaq, EC_NULL, "myVariable2", "0", eDaqOperator_Equal, EC_TRUE /* bEnable */, EC_FALSE /* bStart */);

    /* IGNORE_TEST(DocumentationSnippets, DaqConfigAddTriggerByValue_EnableDisable) */
}

IGNORE_TEST(DocumentationSnippets, DaqConfigAddTriggerByValue_GreaterVariable)
{
    /* Recording is stopped. This will start recording for 1000ms, if variable “myVariable1” is greater than variable “myVariable2”: */

    ecDaqConfigAddTriggerByVariable(hDaq,  EC_NULL, "myVariable1", "myVariable2", eDaqOperator_Greater, EC_TRUE, EC_TRUE, 1000);

    /* Compare also samples of “ecDaqConfigAddTriggerByVariable()”. */

    /* IGNORE_TEST(DocumentationSnippets, DaqConfigAddTriggerByValue_GreaterVariable) */
}

IGNORE_TEST(DocumentationSnippets, DAQ_Init)
{
    EC_T_DAQ_REC S_hDaq = EC_NULL;

    EC_T_DAQ_FP tEcDaqFp;
    OsMemset(&tEcDaqFp, 0, sizeof(EC_T_DAQ_FP));
    tEcDaqFp.RegisterClient = emRegisterClient;
    tEcDaqFp.UnregisterClient = emUnregisterClient;
    tEcDaqFp.GetCfgSlaveInfo = emGetCfgSlaveInfo;
    tEcDaqFp.GetSlaveInpVarInfoNumOf = emGetSlaveInpVarInfoNumOf;
    tEcDaqFp.GetSlaveInpVarInfo = emGetSlaveInpVarInfoEx;
    tEcDaqFp.GetSlaveOutpVarInfoNumOf = emGetSlaveOutpVarInfoNumOf;
    tEcDaqFp.GetSlaveOutpVarInfo = emGetSlaveOutpVarInfoEx;
    tEcDaqFp.SystemTimeGet = OsSystemTimeGet;
    tEcDaqFp.QueryMsecCount = OsQueryMsecCount;

    EC_T_DAQ_REC_PARMS tEcDaqParms;
    OsMemset(&tEcDaqParms, 0, sizeof(EC_T_DAQ_REC_PARMS));
    tEcDaqParms.dwMasterInstanceId = dwInstanceId;
    tEcDaqParms.dwSampleRate = 0;
    tEcDaqParms.dwBusCycleTimeUsec = 1000;
    tEcDaqParms.bRealTimeStamp = EC_FALSE;
    tEcDaqParms.bCycleCounter = EC_TRUE;
    tEcDaqParms.bElapsedTimeMsec = EC_TRUE;
    strcpy(tEcDaqParms.szWriter, "MDF");
    strcpy(tEcDaqParms.szName, "WriterMdf.mf4");
    strcpy(tEcDaqParms.szFile, "c:\\temp\\WriterMdf.mf4");

    dwRes = ecDaqRecCreate(&S_hDaq, &tEcDaqFp, &tEcDaqParms);
    /* IGNORE_TEST(DocumentationSnippets, DAQ_Init) */
}

IGNORE_TEST(DocumentationSnippets, DAQ_Conf)
{
    dwRes = ecDaqConfigAddDataVariable(hDaq, "Slave_1005.Inputs.Channel");
    dwRes = ecDaqConfigApply(hDaq);
    /* IGNORE_TEST(DocumentationSnippets, DAQ_Conf) */
}

IGNORE_TEST(DocumentationSnippets, DAQ_Start)
{
    dwRes = ecDaqRecStart(hDaq);
    /* IGNORE_TEST(DocumentationSnippets, DAQ_Start) */
}

IGNORE_TEST(DocumentationSnippets, DAQ_Stop)
{
    dwRes = ecDaqRecStop(hDaq);
    /* IGNORE_TEST(DocumentationSnippets, DAQ_Stop) */
}

IGNORE_TEST(DocumentationSnippets, DAQ_Processing)
{
    dwRes = ecDaqProcessRt(hDaq);
    /* IGNORE_TEST(DocumentationSnippets, DAQ_Processing) */
}

IGNORE_TEST(DocumentationSnippets, DAQ_Deinit)
{
    dwRes = ecDaqRecDelete(hDaq);
    /* IGNORE_TEST(DocumentationSnippets, DAQ_Deinit) */
}
} } /* namespace EcMasterTests::DocumentationSnippets */