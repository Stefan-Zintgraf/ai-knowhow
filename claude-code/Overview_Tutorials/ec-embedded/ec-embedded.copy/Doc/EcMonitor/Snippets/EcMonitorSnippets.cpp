/* Copyright    acontis technologies GmbH, Ravensburg, Germany
 * Response     Holger Oelhaf
 * Description  Code snippets, examples for documentation */

#include "../../Tests/EcMonitorTests/EcMonitorTests.h"

TEST_GROUP(DocumentationSnippets), CEcMonitorTestApp
{
    TEST_SETUP()
    {
    }
    TEST_TEARDOWN()
    {
    }
    EC_T_DWORD dwInstanceId;
    EC_T_DWORD dwRes;
};

IGNORE_TEST(DocumentationSnippets, emonOpenPacketCapture)
{
    EC_T_PACKETCAPTURE_PARMS PacketCaptureParms;
    OsMemset(&PacketCaptureParms, dwInstanceId, sizeof(EC_T_PACKETCAPTURE_PARMS));

    OsStrcpy(PacketCaptureParms.szFileName, "C:\\ecat.pcap");
    dwRes = emonOpenPacketCapture(0, &PacketCaptureParms);
    if (EC_E_NOERROR != dwRes)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "Cannot open packet capture: %s (0x%lx))\n",
            ecatGetText(dwRes), dwRes));
    }
    /* IGNORE_TEST(DocumentationSnippets, emonOpenPacketCapture) */
}

IGNORE_TEST(DocumentationSnippets, emonGetMonitorParms)
{
    /* Read all monitor init parameters, including OS and Link parameters */
    EC_T_BYTE abyBuffer[sizeof(EC_T_MONITOR_INIT_PARMS) + sizeof(EC_T_OS_PARMS) + 512 /* LinkLayer parameters */];
    EC_T_MONITOR_INIT_PARMS* pParms = (EC_T_MONITOR_INIT_PARMS*)abyBuffer;
    OsMemset(abyBuffer, 0, sizeof(abyBuffer));

    dwRes = emonGetMonitorParms(dwInstanceId, pParms, sizeof(abyBuffer));
    if (EC_E_NOERROR != dwRes)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "Cannot get monitor parameters: %s (0x%lx))\n",
            ecatGetText(dwRes), dwRes));
    }
    /* IGNORE_TEST(DocumentationSnippets, emonGetMonitorParms) */
}

IGNORE_TEST(DocumentationSnippets, emonSetLicenseKey)
{
    dwRes = emonSetLicenseKey(dwInstanceId, "DA1099F2-15C249E9-54327FBC");
    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "ERROR: Cannot set license key: %s (0x%lx))\n",
            ecatGetText(dwRes), dwRes));
    }
    /* IGNORE_TEST(DocumentationSnippets, emonSetLicenseKey) */
}

IGNORE_TEST(DocumentationSnippets, PdAccess_HardCodedOffsets)
{
    EC_T_BYTE* pbyPdOut = emonGetProcessImageInputPtr(dwInstanceId);
    EC_T_BYTE  byValue = 0x00;
    EC_T_DWORD dwBitOffset = 10;
    EC_T_DWORD dwBitSize = 1;

    /* get variable in process data */
    EC_GETBITS(pbyPdOut, &byValue, dwBitOffset, dwBitSize);
    /* IGNORE_TEST(DocumentationSnippets, PdAccess_HardCodedOffsets) */
}
IGNORE_TEST(DocumentationSnippets, PdAccess_GeneratedLayout)
{
    /* IGNORE_TEST(DocumentationSnippets, PdAccess_GeneratedLayout)_Header */
#include EC_PACKED_INCLUDESTART(1)
#define PDLAYOUT_OUT_OFFSET_SLAVE_2002 22
    typedef struct _T_PDLAYOUT_OUT_SLAVE_2002
    {
        EC_T_SWORD  swChannel_1_Output; // Slave_2002 [EL4132].Channel 1.Output ...
        EC_T_SWORD  swChannel_2_Output; // Slave_2002 [EL4132].Channel 2.Output ...
    } EC_PACKED(1) T_PDLAYOUT_OUT_SLAVE_2002;
#include EC_PACKED_INCLUDESTOP
    /* IGNORE_TEST(DocumentationSnippets, PdAccess_GeneratedLayout)_Header */

    /* IGNORE_TEST(DocumentationSnippets, PdAccess_GeneratedLayout)_Set */
    EC_T_BYTE* pbyPdOut = emonGetProcessImageOutputPtr(dwInstanceId);
    T_PDLAYOUT_OUT_SLAVE_2002* pPdOutSlave2002 = (T_PDLAYOUT_OUT_SLAVE_2002*)(pbyPdOut + PDLAYOUT_OUT_OFFSET_SLAVE_2002);

    EC_T_WORD wChannel1Out = EC_GET_FRM_WORD(&pPdOutSlave2002->swChannel_1_Output);
    /* IGNORE_TEST(DocumentationSnippets, PdAccess_GeneratedLayout)_Set */
    EC_UNREFPARM(wChannel1Out);
}
IGNORE_TEST(DocumentationSnippets, PdAccess_GetCfgSlaveInfo)
{
    EC_T_CFG_SLAVE_INFO SlaveInfo;
    dwRes = emonGetCfgSlaveInfo(dwInstanceId, EC_TRUE, 1004, &SlaveInfo);

    EC_T_BYTE* pbyPdOut = emonGetProcessImageOutputPtr(dwInstanceId);
    EC_T_BYTE  byValue = 0x00;
    EC_T_DWORD dwBitOffset = SlaveInfo.dwPdOffsOut + 2;
    EC_T_DWORD dwBitSize = 1;

    /* get variable in process data */
    EC_GETBITS(pbyPdOut, &byValue, dwBitOffset, dwBitSize);
    /* IGNORE_TEST(DocumentationSnippets, PdAccess_GetCfgSlaveInfo) */
}
IGNORE_TEST(DocumentationSnippets, PdAcces_GetSlaveOutpVarInfoEx)
{
    EC_T_WORD wNumSlaveVars = 0;
    EC_T_WORD wNumVarsRead = 0;
    EC_T_PROCESS_VAR_INFO_EX* aProcVarInfo = EC_NULL;

    /* get number of output variables */
    dwRes = emonGetSlaveOutpVarInfoNumOf(dwInstanceId, EC_TRUE, 1004, &wNumSlaveVars);

    /* allocate buffer for the variable info structs */
    aProcVarInfo = (EC_T_PROCESS_VAR_INFO_EX*)OsMalloc(sizeof(EC_T_PROCESS_VAR_INFO_EX) * wNumSlaveVars);
    OsMemset(aProcVarInfo, 0, sizeof(EC_T_PROCESS_VAR_INFO_EX) * wNumSlaveVars);

    /* read all variables of the slave at once */
    dwRes = emonGetSlaveOutpVarInfoEx(dwInstanceId, EC_TRUE, 1004, wNumSlaveVars, aProcVarInfo, &wNumVarsRead);

    EC_T_BYTE* pbyPdOut = emonGetProcessImageOutputPtr(dwInstanceId);
    EC_T_BYTE  byValue = 0x00;

    /* get variable in process data */
    EC_GETBITS(pbyPdOut, &byValue, aProcVarInfo[0].nBitOffs, aProcVarInfo[0].nBitSize);
    /* IGNORE_TEST(DocumentationSnippets, PdAcces_GetSlaveOutpVarInfoEx) */
}
IGNORE_TEST(DocumentationSnippets, PdAcces_FindOutpVarByNameEx)
{
    EC_T_PROCESS_VAR_INFO_EX ProcVarInfo;
    dwRes = emonFindOutpVarByNameEx(dwInstanceId, "Slave_1004 [EL2004].Channel 3.Output", &ProcVarInfo);

    EC_T_BYTE* pbyPdOut = emonGetProcessImageOutputPtr(dwInstanceId);
    EC_T_BYTE  byValue = 0x00;

    /* get variable in process data */
    EC_GETBITS(pbyPdOut, &byValue, ProcVarInfo.nBitOffs, ProcVarInfo.nBitSize);
    /* IGNORE_TEST(DocumentationSnippets, PdAcces_FindOutpVarByNameEx) */
}
IGNORE_TEST(DocumentationSnippets, PdAcces_GetSlaveOutpVarByObjectEx)
{
    EC_T_PROCESS_VAR_INFO_EX ProcVarInfo;
    dwRes = emonGetSlaveOutpVarByObjectEx(dwInstanceId, EC_TRUE, 1004, 0x7010, 0x01, &ProcVarInfo);

    EC_T_BYTE* pbyPdOut = emonGetProcessImageOutputPtr(dwInstanceId);
    EC_T_BYTE  byValue = 0x00;

    /* get variable in process data */
    EC_GETBITS(pbyPdOut, &byValue, ProcVarInfo.nBitOffs, ProcVarInfo.nBitSize);
    /* IGNORE_TEST(DocumentationSnippets, PdAcces_GetSlaveOutpVarByObjectEx) */
}
IGNORE_TEST(DocumentationSnippets, Diag_WkcState)
{
    EC_T_BYTE* pbyDiagnosisImage = emonGetDiagnosisImagePtr(dwInstanceId);
    EC_T_CFG_SLAVE_INFO CfgSlaveInfo;

    dwRes = emonGetCfgSlaveInfo(dwInstanceId, EC_TRUE, 1002, &CfgSlaveInfo);

    for (EC_T_DWORD i = 0; i < EC_CFG_SLAVE_PD_SECTIONS; i++)
    {
        if (0xFFFF == CfgSlaveInfo.wWkcStateDiagOffsIn[i])
        {
            /* offset not available */
            break;
        }

        if (EC_TESTBIT(pbyDiagnosisImage, CfgSlaveInfo.wWkcStateDiagOffsIn[i]))
        {
            /* ... error ... */
        }
    }
    /*IGNORE_TEST(DocumentationSnippets, Diag_WkcState)*/
}
IGNORE_TEST(DocumentationSnippets, Diag_MsuWkcState)
{
    EC_T_BYTE* pbyDiagnosisImage = emonGetDiagnosisImagePtr(dwInstanceId);
    EC_T_MSU_INFO MsuInfo;
    
    dwRes = emonGetMasterSyncUnitInfo(dwInstanceId, 0, &MsuInfo);

    if (EC_TESTBIT(pbyDiagnosisImage, MsuInfo.wWkcStateDiagOffsIn))
    {
        /* ... error ... */
    }
    /*IGNORE_TEST(DocumentationSnippets, Diag_MsuWkcState)*/
}
IGNORE_TEST(DocumentationSnippets, emonGetCfgSlaveSmInfo)
{
    /* get information about slave's sync managers configured in ENI file */
    EC_T_CFG_SLAVE_SM_INFO oSlaveSmInfo;
    OsMemset(&oSlaveSmInfo, 0, sizeof(EC_T_CFG_SLAVE_SM_INFO));
    dwRes = emonGetCfgSlaveSmInfo(dwInstanceId, EC_TRUE, 1001, &oSlaveSmInfo);
    /*IGNORE_TEST(DocumentationSnippets, emonGetCfgSlaveSmInfo)*/
    CHECK_NOERROR(dwRes);
}

#if 0
IGNORE_TEST(DocumentationSnippets, quickstartDemoExtension)
{
    /* IGNORE_TEST(DocumentationSnippets, quickstartDemoExtension)_Appdesc */
    typedef struct _T_MY_APP_DESC
    {
        // ...
        // Add the following line
        EC_T_BYTE       bSub1002In1Status;
    } T_MY_APP_DESC;
    /* IGNORE_TEST(DocumentationSnippets, quickstartDemoExtension)_Appdesc */
    /* IGNORE_TEST(DocumentationSnippets, quickstartDemoExtension)_Workpd */
    static EC_T_DWORD myAppWorkpd(T_EC_DEMO_APP_CONTEXT* pAppContext)
    {
        // ...
        // We are processing an input variable, so we get the PDI input pointer
        EC_T_BYTE* pbyPdIn = emonGetProcessImageInputPtr(pAppContext->dwInstanceId);

        // The type and offset of the variable are defined in the exported header file
        // We add the offset to the PDI input pointer, cast it to the target type, and dereference our desired member
        EC_T_BYTE currentStatus = ((_T_PDLAYOUT_IN_SUBDEVICE_1002*)(pbyPdIn + PDLAYOUT_IN_OFFSET_SUBDEVICE_1002))->byChannel_1_Input;

        // Finally, we print to the console when the variable has changed
        if (pMyAppDesc->bSub1002In1Status != currentStatus) {
            pMyAppDesc->bSub1002In1Status = currentStatus;
            printf("Variable has changed: %u\n", currentStatus);
        }
        
        return EC_E_NOERROR;
    }
    /* IGNORE_TEST(DocumentationSnippets, quickstartDemoExtension)_Workpd */
}
#endif