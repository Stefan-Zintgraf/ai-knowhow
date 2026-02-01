namespace EcMasterTests { namespace DocumentationSnippets {
TEST_GROUP(Api), CDocumentationSnippetsBase
{};

TEST(Api, DOC_GetMasterParms)
{
    CEcSimulatorSilTestApplication oTestApplication;
    oTestApplication.SetupMaster(oTestApplication.GetEniFileName());

    /** DocumentationSnippetsGetMasterParmsExample */
    EC_T_BYTE abyBuffer[sizeof(EC_T_INIT_MASTER_PARMS)
        + sizeof(EC_T_OS_PARMS) + 512 /* LinkLayer parameters */];
    EC_T_INIT_MASTER_PARMS* pParms = (EC_T_INIT_MASTER_PARMS*)abyBuffer;
    dwRes = emGetMasterParms(dwInstanceId, pParms, sizeof(abyBuffer));
    /** DocumentationSnippetsGetMasterParmsExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(DocumentationSnippets, emSetLicenseKey)
{
    dwRes = emSetLicenseKey(dwInstanceId, "DA1099F2-15C249E9-54327FBC");
    /* IGNORE_TEST(DocumentationSnippets, emSetLicenseKey) */
}
IGNORE_TEST(DocumentationSnippets, emSetOemKey)
{
    dwRes = emSetOemKey(dwInstanceId, 0x1234567812345678);
    /* IGNORE_TEST(DocumentationSnippets, emSetOemKey) */
}

IGNORE_TEST(Api, DOC_SetMasterParms)
{
    /** DocumentationSnippetsSetMasterParmsExample */
    EC_T_BYTE abyBuffer[sizeof(EC_T_INIT_MASTER_PARMS) + sizeof(EC_T_OS_PARMS)
        + 512 /* LinkLayer parameters */];
    EC_T_INIT_MASTER_PARMS* pParms = (EC_T_INIT_MASTER_PARMS*)abyBuffer;
    dwRes = emGetMasterParms(dwInstanceId, pParms, sizeof(abyBuffer));
    pParms->wReserved = 1;
    /* change Master initialization parameters */
    dwRes = emSetMasterParms(dwInstanceId, pParms);
    /** DocumentationSnippetsSetMasterParmsExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_GetMasterState)
{
    /** DocumentationSnippetsGetMasterStateExample */
    /* get EtherCAT master current state */
    EC_T_STATE eMasterState = emGetMasterState(dwInstanceId);
    EcLogMsg(EC_LOG_LEVEL_INFO, (pEcLogContext, EC_LOG_LEVEL_INFO,
        "Current Master State: %s:\n", ecatStateToStr(eMasterState)));
    /** DocumentationSnippetsGetMasterStateExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_SetMasterState)
{
    /** DocumentationSnippetsSetMasterStateExample */
    /* set EtherCAT master (and all slaves) into requested state */
    dwRes = emSetMasterState(dwInstanceId, 5000, eEcatState_PREOP);
    /** DocumentationSnippetsSetMasterStateExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_SetMasterStateReq)
{
    /** DocumentationSnippetsSetMasterStateReqExample */
    /* set EtherCAT master (and all slaves) into requested state */
    dwRes = emSetMasterStateReq(dwInstanceId, 5000, eEcatState_PREOP);
    /** DocumentationSnippetsSetMasterStateReqExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_GetMasterStateEx)
{
    /** DocumentationSnippetsGetMasterStateExExample */
    EC_T_WORD wCurrState = 0;
    EC_T_WORD wReqState = 0;
    /* get EtherCAT master current state */
    dwRes = emGetMasterStateEx(dwInstanceId, &wCurrState, &wReqState);
    EcLogMsg(EC_LOG_LEVEL_INFO, (pEcLogContext, EC_LOG_LEVEL_INFO,
        "Current state: %s, requested state: %s\n", 
        ecatDeviceStateText(wCurrState), ecatDeviceStateText(wReqState)));
    /** DocumentationSnippetsGetMasterStateExExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_GetProcessData)
{
    /** DocumentationSnippetsGetProcessDataExample */
    /* get Process data (synchronized with JobTask) */
    EC_T_BYTE abyData[1] = { 0 };
    dwRes = emGetProcessData(dwInstanceId, EC_FALSE, 0 /* byte offset */,
        abyData, 1 /* byte length */, 5000);
    EcLogMsg(EC_LOG_LEVEL_INFO, (pEcLogContext, EC_LOG_LEVEL_INFO, 
        "Process Data: 0x%02X\n", abyData[0]));
    /** DocumentationSnippetsGetProcessDataExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_SetProcessData)
{
    /** DocumentationSnippetsSetProcessDataExample */
    /* write value 0x12 to Process Data Image (synchronized with JobTask) */
    EC_T_BYTE abyData[1] = { 0x12 };
    dwRes = emSetProcessData(dwInstanceId, EC_FALSE, 0 /* byte offset */,
        abyData, 1 /* byte length */, 5000);
    /** DocumentationSnippetsSetProcessDataExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_GetProcessDataBits)
{
    /** DocumentationSnippetsGetProcessDataBitsExample */
    /* get bits from Process Data Image (synchronized with JobTask) */
    EC_T_BYTE abyData[1] = { 0 };
    dwRes = emGetProcessDataBits(dwInstanceId, EC_FALSE, 0 /* bit offset */, 
        abyData, 8 /* bit length */, 5000);
    /** DocumentationSnippetsGetProcessDataBitsExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_SetProcessDataBits)
{
    /** DocumentationSnippetsSetProcessDataBitsExample */
    /* write bits to Process Data Image (synchronized with JobTask) */
    EC_T_BYTE abyData[1] = { 0x12 };
    dwRes = emSetProcessDataBits(dwInstanceId, EC_TRUE, 0 /* bit offset */,
        abyData, 8 /* bit length */, 5000);
    /** DocumentationSnippetsSetProcessDataBitsExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_GetDiagnosisImagePtr)
{
    /** DocumentationSnippetsGetDiagnosisImagePtrExample */
    /* get diagnosis image pointer */
    EC_T_BYTE* pbyProcessImageOutput = emGetDiagnosisImagePtr(dwInstanceId);
    /** DocumentationSnippetsGetDiagnosisImagePtrExample */
    CHECK(EC_NULL != pbyProcessImageOutput);
}

IGNORE_TEST(Api, DOC_GetProcessImageInputPtr)
{
    /** DocumentationSnippetsGetProcessImageInputPtrExample */
    /* get process data input image pointer */
    EC_T_BYTE* pbyProcessImageInput = emGetProcessImageInputPtr(dwInstanceId);
    /** DocumentationSnippetsGetProcessImageInputPtrExample */
    CHECK(EC_NULL != pbyProcessImageInput);
}

IGNORE_TEST(Api, DOC_GetProcessImageOutputPtr)
{
    /** DocumentationSnippetsGetProcessImageOutputPtrExample */
    /* get process data output image pointer */
    EC_T_BYTE* pbyProcessImageOutput = emGetProcessImageOutputPtr(dwInstanceId);
    /** DocumentationSnippetsGetProcessImageOutputPtrExample */
    CHECK(EC_NULL != pbyProcessImageOutput);
}

IGNORE_TEST(Api, DOC_GetSrcMacAdressExample)
{
    /** DocumentationSnippetsGetSrcMacAdressExample */
    /* get MAC address of EtherCAT network adapter */
    ETHERNET_ADDRESS oMacSrc;
    OsMemset(&oMacSrc, 0, sizeof(ETHERNET_ADDRESS));
    dwRes = emGetSrcMacAddress(dwInstanceId, &oMacSrc);
    /** DocumentationSnippetsGetSrcMacAdressExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_GetVersionExample)
{
    /** DocumentationSnippetsGetVersionExample */
    /* get stack version */
    EC_T_DWORD dwVersion = EC_E_ERROR;
    EC_T_DWORD dwVersionType = 0;
    dwRes = emGetVersion(dwInstanceId, &dwVersion, &dwVersionType);
    /** DocumentationSnippetsGetVersionExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_GetMasterSyncUnitInfoNumOf)
{
    /** DocumentationSnippetsGetMasterSyncUnitInfoNumOfExample */
    /* get Master Sync Units info entries count */
    EC_T_DWORD dwSyncedUnitsCount = emGetMasterSyncUnitInfoNumOf(dwInstanceId);
    EcLogMsg(EC_LOG_LEVEL_INFO, (pEcLogContext, EC_LOG_LEVEL_INFO, 
        "Units count: %d", dwSyncedUnitsCount));
    /** DocumentationSnippetsGetMasterSyncUnitInfoNumOfExample */
}

IGNORE_TEST(Api, DOC_GetMasterSyncUnitInfo)
{
    /** DocumentationSnippetsGetMasterSyncUnitInfoExample */
    /* get information about specific Master Sync Unit */
    EC_T_WORD wMsuId = 0;
    EC_T_MSU_INFO oMsuInfo;
    OsMemset(&oMsuInfo, 0, sizeof(EC_T_MSU_INFO));
    dwRes = emGetMasterSyncUnitInfo(dwInstanceId, wMsuId, &oMsuInfo);
    /** DocumentationSnippetsGetMasterSyncUnitInfoExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_GetMemoryUsage)
{
    /** DocumentationSnippetsGetMemoryUsageExample */
    EC_T_DWORD dwCurrentUsage = EC_NULL;
    EC_T_DWORD dwMaxUsage = EC_NULL;
    dwRes = emGetMemoryUsage(dwInstanceId, &dwCurrentUsage, &dwMaxUsage);
    /** DocumentationSnippetsGetMemoryUsageExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_GetNumConfiguredSlaves)
{
    /** DocumentationSnippetsGetNumConfiguredSlavesExample */
    /* get configured slave count */
    EC_T_DWORD dwSlaveCnt = emGetNumConfiguredSlaves(dwInstanceId);
    EcLogMsg(EC_LOG_LEVEL_INFO, (pEcLogContext, EC_LOG_LEVEL_INFO, 
        " Slave Count: %d", dwSlaveCnt));
    /** DocumentationSnippetsGetNumConfiguredSlavesExample */
}

IGNORE_TEST(Api, DOC_GetNumConnectedSlaves)
{
    /** DocumentationSnippetsGetNumConnectedSlavesExample */
    /* get currently connected slave count */
    EC_T_DWORD dwSlaveCnt = emGetNumConnectedSlaves(dwInstanceId);
    EcLogMsg(EC_LOG_LEVEL_INFO, (pEcLogContext, EC_LOG_LEVEL_INFO, 
        " Slave Count: %d", dwSlaveCnt));
    /** DocumentationSnippetsGetNumConnectedSlavesExample */
}

IGNORE_TEST(Api, DOC_GetBusSlaveInfo)
{
    /** DocumentationSnippetsGetBusSlaveInfoExample */
    /* get information about slave connected to EtherCAT bus */
    EC_T_BUS_SLAVE_INFO oSlaveInfo;
    OsMemset(&oSlaveInfo, 0, sizeof(EC_T_BUS_SLAVE_INFO));
    dwRes = emGetBusSlaveInfo(dwInstanceId, EC_TRUE, 1001, &oSlaveInfo);
    /** DocumentationSnippetsGetBusSlaveInfoExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_GetCfgSlaveInfo)
{
    /** DocumentationSnippetsGetCfgSlaveInfoExample */
    /* get information about slave configured in ENI file */
    EC_T_CFG_SLAVE_INFO oSlaveInfo;
    OsMemset(&oSlaveInfo, 0, sizeof(EC_T_CFG_SLAVE_INFO));
    dwRes = emGetCfgSlaveInfo(dwInstanceId, EC_TRUE, 1001, &oSlaveInfo);
    /** DocumentationSnippetsGetCfgSlaveInfoExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_GetCfgSlaveEoeInfo)
{
    /** DocumentationSnippetsGetCfgSlaveEoeInfoExample */
    /* get EoE information about slave configured in ENI file */
    EC_T_CFG_SLAVE_EOE_INFO oSlaveInfo;
    OsMemset(&oSlaveInfo, 0, sizeof(EC_T_CFG_SLAVE_EOE_INFO));
    dwRes = emGetCfgSlaveEoeInfo(dwInstanceId, EC_TRUE, 1001, &oSlaveInfo);
    /** DocumentationSnippetsGetCfgSlaveEoeInfoExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_GetCfgSlaveSmInfo)
{
    /** DocumentationSnippetsGetCfgSlaveSmInfoExample */
    /* get information about slave's sync managers configured in ENI file */
    EC_T_CFG_SLAVE_SM_INFO oSlaveSmInfo;
    OsMemset(&oSlaveSmInfo, 0, sizeof(EC_T_CFG_SLAVE_SM_INFO));
    dwRes = emGetCfgSlaveSmInfo(dwInstanceId, EC_TRUE, 1001, &oSlaveSmInfo);
    /** DocumentationSnippetsGetCfgSlaveSmInfoExample */
    CHECK_NOERROR(dwRes);
}

TEST(Api, DOC_GetSlaveId)
{
    /** DocumentationSnippetsGetSlaveIdExample */
    /* get slave ID using slave station address */
    EC_T_WORD wStationAddress = 1002;
    EC_T_DWORD dwSlaveId = emGetSlaveId(dwInstanceId, wStationAddress);
    EcLogMsg(EC_LOG_LEVEL_INFO, (pEcLogContext, EC_LOG_LEVEL_INFO, 
        " Slave ID: %d", dwSlaveId));
    /** DocumentationSnippetsGetSlaveIdExample */
}

TEST(Api, DOC_GetSlaveIdAtPosition)
{
    /** DocumentationSnippetsGetSlaveIdAtPositionExample */
    /* get slave ID using configured auto increment address */
    EC_T_WORD wAutoIncAdress = 0xFFFB;
    EC_T_DWORD dwSlavePos = emGetSlaveIdAtPosition(dwInstanceId, wAutoIncAdress);
    EcLogMsg(EC_LOG_LEVEL_INFO, (pEcLogContext, EC_LOG_LEVEL_INFO, 
        " Slave Position: %d", dwSlavePos));
    /** DocumentationSnippetsGetSlaveIdAtPositionExample */
}

IGNORE_TEST(Api, DOC_GetMasterDump)
{
    /** DocumentationSnippetsGetMasterDumpExample */
    EC_T_DWORD dwBufferSize = 8192;
    EC_T_BYTE* byBuffer = (EC_T_BYTE*)OsMalloc(dwBufferSize);
    EC_T_DWORD dwDumpSize = dwBufferSize;
    dwRes = emGetMasterDump(dwInstanceId, byBuffer, dwBufferSize, &dwDumpSize);
    /** DocumentationSnippetsGetMasterDumpExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_GetMasterInfo)
{
    /** DocumentationSnippetsGetMasterInfoExample */
    EC_T_MASTER_INFO oMasterInfo;
    OsMemset(&oMasterInfo, 0, sizeof(EC_T_MASTER_INFO));
    dwRes = emGetMasterInfo(dwInstanceId, &oMasterInfo);
    /** DocumentationSnippetsGetMasterInfoExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_GetSlavePortState)
{
    /** DocumentationSnippetsGetSlavePortStateExample */
    EC_T_DWORD dwSlaveId = 2;
    EC_T_WORD wPortState = 0;
    dwRes = emGetSlavePortState(dwInstanceId, dwSlaveId, &wPortState);
    /** DocumentationSnippetsGetSlavePortStateExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_GetSlaveProp)
{
    /** DocumentationSnippetsGetSlavePropExample */
    EC_T_DWORD dwSlaveId = emGetSlaveId(dwInstanceId, 1002);
    EC_T_SLAVE_PROP oSlaveProp;
    OsMemset(&oSlaveProp, 0, sizeof(EC_T_SLAVE_PROP));
    EC_T_BOOL bSlaveProp = emGetSlaveProp(dwInstanceId, dwSlaveId, &oSlaveProp);
    EcLogMsg(EC_LOG_LEVEL_INFO, (pEcLogContext, EC_LOG_LEVEL_INFO, " Slave ID: %d", bSlaveProp));
    /** DocumentationSnippetsGetSlavePropExample */
}

IGNORE_TEST(Api, DOC_GetSlaveState)
{
    /** DocumentationSnippetsGetSlaveStateExample */
    /* get slave state */
    EC_T_DWORD dwSlaveId = emGetSlaveId(dwInstanceId, 1002);
    EC_T_WORD pwCurrDevState = 0;
    EC_T_WORD wReqDevState = 0;
    dwRes = emGetSlaveState(dwInstanceId, dwSlaveId, &pwCurrDevState, &wReqDevState);
    /** DocumentationSnippetsGetSlaveStateExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_GetSlaveStatistics)
{
    /** DocumentationSnippetsGetSlaveStatisticsExample */
    /* get slave's statistics counters */
    EC_T_DWORD dwSlaveId = emGetSlaveId(dwInstanceId, 1002);
    EC_T_SLVSTATISTICS_DESC oSlaveStatisticsDesc;
    OsMemset(&oSlaveStatisticsDesc, 0, sizeof(EC_T_SLVSTATISTICS_DESC));
    dwRes = dwSlaveId;
    dwRes = emGetSlaveStatistics(dwInstanceId, dwSlaveId, &oSlaveStatisticsDesc);
    /** DocumentationSnippetsGetSlaveStatisticsExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_ScanBusExample)
{
    /** DocumentationSnippetsScanBusExample */
    dwRes = emScanBus(dwInstanceId, 5000 /* timeout */);
    /** DocumentationSnippetsScanBusExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_ConfigExtendExample)
{
    /** DocumentationSnippetsConfigExtendExample */
    dwRes = emConfigExtend(dwInstanceId, EC_TRUE, 5000 /* timeout */);
    /** DocumentationSnippetsConfigExtendExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_ForceProcessDataBits)
{
    /** DocumentationSnippetsForceProcessDataBitsExample */
    /* force specific number of bits from given buffer to process image with a bit offset */
    EC_T_BYTE abyData[1] = { 1 };
    dwRes = emForceProcessDataBits(dwInstanceId, dwClientId,
        EC_FALSE, 0 /* bit offset */, 1 /* bit length */, abyData, 5000 /* timeout */);
    /** DocumentationSnippetsForceProcessDataBitsExample */
}

IGNORE_TEST(Api, DOC_FindInpVarByName)
{
    /** DocumentationSnippetsFindInpVarByNameExample */
    /* get general information about Process Data variable by name */
    EC_T_PROCESS_VAR_INFO oProcessVarInfoEntry;
    OsMemset(&oProcessVarInfoEntry, 0, sizeof(EC_T_PROCESS_VAR_INFO));
    dwRes = emFindInpVarByName(dwInstanceId, "Slave_1004 [EL1014].Channel 1.Input", &oProcessVarInfoEntry);
    /** DocumentationSnippetsFindInpVarByNameExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_FindInpVarByNameEx)
{
    /** DocumentationSnippetsFindInpVarByNameExExample */
    /* get extended information about Process Data variable by name */
    EC_T_PROCESS_VAR_INFO_EX oProcessVarInfoEntry;
    OsMemset(&oProcessVarInfoEntry, 0, sizeof(EC_T_PROCESS_VAR_INFO_EX));
    dwRes = emFindInpVarByNameEx(dwInstanceId, "Slave_1004 [EL1014].Channel 1.Input", &oProcessVarInfoEntry);
    /** DocumentationSnippetsFindInpVarByNameExExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_FindOutpVarByName)
{
    /** DocumentationSnippetsFindOutpVarByNameExample */
    /* get general information about Process Data variable by name */
    EC_T_PROCESS_VAR_INFO oProcessVarInfoEntry;
    OsMemset(&oProcessVarInfoEntry, 0, sizeof(EC_T_PROCESS_VAR_INFO));
    dwRes = emFindOutpVarByName(dwInstanceId, "Slave_1002 [EL2004].Channel 1.Output", &oProcessVarInfoEntry);
    /** DocumentationSnippetsFindOutpVarByNameExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_FindOutpVarByNameEx)
{
    /** DocumentationSnippetsFindOutpVarByNameExExample */
    /* get extended information about Process Data variable by name */
    EC_T_PROCESS_VAR_INFO_EX oProcessVarInfoEntry;
    OsMemset(&oProcessVarInfoEntry, 0, sizeof(EC_T_PROCESS_VAR_INFO_EX));
    dwRes = emFindOutpVarByNameEx(dwInstanceId, "Slave_1002 [EL2004].Channel 1.Output", &oProcessVarInfoEntry);
    /** DocumentationSnippetsFindOutpVarByNameExExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_IsSlavePresent)
{
    /** DocumentationSnippetsIsSlavePresentExample */
    EC_T_DWORD dwSlaveId = emGetSlaveId(dwInstanceId, 1002);
    EC_T_BOOL bPresence = EC_FALSE;

    /* returns whether a specific slave is currently connected to network */
    dwRes = emIsSlavePresent(dwInstanceId, dwSlaveId, &bPresence);
    /** DocumentationSnippetsIsSlavePresentExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_EthDbgMsg)
{
    /** DocumentationSnippetsEthDbgMsgExample */
    EC_T_CHAR* szMsg = (EC_T_CHAR*)"Hello World";
    EC_T_BYTE byEthTypeByte0 = 6;
    EC_T_BYTE byEthTypeByte1 = 6;
    /* send message as frame, validate given EtherType: 
       >= 1536: EtherType (supported as parameter), 
       <= 1500: size of payload (not supported as parameter), 
          1501-1535: undefined */
    /* send debug message to EtherCAT Link Layer */
    dwRes = emEthDbgMsg(dwInstanceId, byEthTypeByte0, byEthTypeByte1, szMsg);
    /** DocumentationSnippetsEthDbgMsgExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_BadConnectionsDetect)
{
    /** DocumentationSnippetsBadConnectionsDetectExample */
    dwRes = emBadConnectionsDetect(dwInstanceId, EC_TRUE, 5000 /* timeout */);
    /** DocumentationSnippetsBadConnectionsDetectExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_BadConnectionsReset)
{
    /** DocumentationSnippetsBadConnectionsResetExample */
    dwRes = emBadConnectionsReset(dwInstanceId);
    /** DocumentationSnippetsBadConnectionsResetExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_ClearSlaveStatistics)
{
    /** DocumentationSnippetsClearSlaveStatisticsExample */
    /* clear all error counters at slave */
    EC_T_DWORD dwSlaveId = emGetSlaveId(dwInstanceId, 1002);
    dwRes = emClearSlaveStatistics(dwInstanceId, dwSlaveId);
    /** DocumentationSnippetsClearSlaveStatisticsExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_GetSlaveInpVarInfoNumOf)
{
    /** DocumentationSnippetsGetSlaveInpVarInfoNumOfExample */
    /* get number of input variables of specific slave */
    EC_T_WORD numOfVars = 0;
    dwRes = emGetSlaveInpVarInfoNumOf(dwInstanceId, EC_TRUE, 1004, &numOfVars);
    /** DocumentationSnippetsGetSlaveInpVarInfoNumOfExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_GetSlaveInpVarInfo)
{
    /** DocumentationSnippetsGetSlaveInpVarInfoExample */
    /* get process variable information entries of specific slave */
    EC_T_PROCESS_VAR_INFO aSlaveInpVarInfoNumOf[4];
    EC_T_WORD wReadEntries = 0;
    EC_T_WORD numOfVars = 0;
    emGetSlaveInpVarInfoNumOf(dwInstanceId, EC_TRUE, 1004, &numOfVars);
    dwRes = emGetSlaveInpVarInfo(dwInstanceId, EC_TRUE, 
        1001, numOfVars, aSlaveInpVarInfoNumOf, &wReadEntries);
    /** DocumentationSnippetsGetSlaveInpVarInfoExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_GetSlaveInpVarInfoEx)
{
    /** DocumentationSnippetsGetSlaveInpVarInfoExExample */
    EC_T_PROCESS_VAR_INFO_EX aSlaveInpVarInfoNumOf[4];
    EC_T_WORD wReadEntries = 0;
    EC_T_WORD  wNumOfVarsToRead = 4;
    emGetSlaveInpVarInfoNumOf(dwInstanceId, EC_TRUE, 1004, &wNumOfVarsToRead);
    /* get extended process variable information entries of specific slave */
    dwRes = emGetSlaveInpVarInfoEx(dwInstanceId, EC_TRUE, 1001, 
        wNumOfVarsToRead, aSlaveInpVarInfoNumOf, &wReadEntries);
    /** DocumentationSnippetsGetSlaveInpVarInfoExExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_GetSlaveInpVarByObjectEx)
{
    /** DocumentationSnippetsGetSlaveInpVarByObjectExExample */
    /* get input process variable extended information entry by object index, 
       subindex of specific slave */
    EC_T_PROCESS_VAR_INFO_EX processVarInfoEntry;
    OsMemset(&processVarInfoEntry, 0, sizeof(EC_T_PROCESS_VAR_INFO_EX));
    dwRes = emGetSlaveInpVarByObjectEx(dwInstanceId, EC_TRUE, 
        1004, 0x6000 /* Index */, 1 /* SubIndex */, &processVarInfoEntry);
    /** DocumentationSnippetsGetSlaveInpVarByObjectExExample */
}

IGNORE_TEST(Api, DOC_GetSlaveOutpVarInfoNumOf)
{
    /** DocumentationSnippetsGetSlaveOutpVarInfoNumOfExample */
    /* get number of output variables of specific slave */
    EC_T_WORD numOfVars = 0;
    dwRes = emGetSlaveOutpVarInfoNumOf(dwInstanceId, EC_TRUE, 1002, &numOfVars);
    /** DocumentationSnippetsGetSlaveOutpVarInfoNumOfExample */
}

IGNORE_TEST(Api, DOC_GetSlaveOutpVarInfo)
{
    /** DocumentationSnippetsGetSlaveOutpVarInfoExample */
    /* get general output process variable information entries of specific slave */
    EC_T_PROCESS_VAR_INFO aoSlaveOutpVarInfo[4]; /* see emGetSlaveOutpVarInfoNumOf() */
    EC_T_WORD wSlaveOutpVarInfoCnt = 0;
    dwRes = emGetSlaveOutpVarInfo(dwInstanceId, EC_TRUE, 1002, 
        4 /* see emGetSlaveOutpVarInfoNumOf() */, aoSlaveOutpVarInfo, &wSlaveOutpVarInfoCnt);
    /** DocumentationSnippetsGetSlaveOutpVarInfoExample */
}

IGNORE_TEST(Api, DOC_GetSlaveOutpVarInfoEx)
{
    /** DocumentationSnippetsGetSlaveOutpVarInfoExExample */
    /* get extended output process variable information entries of specific slave */
    EC_T_PROCESS_VAR_INFO_EX aoSlaveOutpVarInfo[4]; /* see emGetSlaveOutpVarInfoNumOf() */
    EC_T_WORD wSlaveOutpVarInfoCnt = 0;
    dwRes = emGetSlaveOutpVarInfoEx(dwInstanceId, EC_TRUE, 1002, 
        4 /* see emGetSlaveOutpVarInfoNumOf() */, aoSlaveOutpVarInfo, &wSlaveOutpVarInfoCnt);
    /** DocumentationSnippetsGetSlaveOutpVarInfoExExample */
}

IGNORE_TEST(Api, DOC_GetSlaveOutpVarByObjectEx)
{
    /** DocumentationSnippetsGetSlaveOutpVarByObjectExExample */
    /* get output process variable extended information entry 
       by object index, subindex of specific slave. */
    EC_T_PROCESS_VAR_INFO_EX oSlaveOutpVarInfo;
    OsMemset(&oSlaveOutpVarInfo, 0, sizeof(EC_T_PROCESS_VAR_INFO_EX));
    dwRes = emGetSlaveOutpVarByObjectEx(dwInstanceId, EC_TRUE, 
        1002, 0x3001 /* Index */, 1 /* SubIndex */, &oSlaveOutpVarInfo);
    /** DocumentationSnippetsGetSlaveOutpVarByObjectExExample */
}

IGNORE_TEST(Api, DOC_SelfTestScan)
{
    /** DocumentationSnippetsSelfTestScanExample */
    EC_T_SELFTESTSCAN_PARMS oParms;
    OsMemset(&oParms, 0, sizeof(EC_T_SELFTESTSCAN_PARMS));
    oParms.dwSize = sizeof(EC_T_SELFTESTSCAN_PARMS);
    oParms.dwTimeout = 5000;
    oParms.dwFrameCount = 1500;
    oParms.dwFrameSizeMin = 60;
    oParms.dwFrameSizeMax = 1514;
    oParms.dwFrameSizeStep = 1;
    oParms.bDetectBadConnections = EC_FALSE;
    dwRes = emSelfTestScan(dwInstanceId, &oParms);
    /** DocumentationSnippetsSelfTestScanExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_ReadSlaveEEPRom)
{
    /** DocumentationSnippetsReadSlaveEEPRomExample */
    /* read EEPROM data from slave */
    EC_T_WORD awData[16];
    EC_T_DWORD dwNumOutData = 0;
    OsMemset(awData, 0, sizeof(awData));

    dwRes = emReadSlaveEEPRom(dwInstanceId, EC_TRUE, 1001, 
        7 /* WORD offset */, awData, EC_NUMOFELEMENTS(awData), 
        &dwNumOutData, 5000 /* timeout */);
    /** DocumentationSnippetsReadSlaveEEPRomExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_ReadSlaveEEPRomReq)
{
    EC_T_REGISTERRESULTS RegisterClientResults;
    OsMemset(&RegisterClientResults, 0, sizeof(EC_T_REGISTERRESULTS));

    /** DocumentationSnippetsReadSlaveEEPRomReqExample */
    EC_T_DWORD dwTferId = 1234; /* arbitrary unique ID from application */
    EC_T_WORD awData[16];
    EC_T_DWORD dwNumOutData = 0;
    OsMemset(awData, 0, sizeof(awData));

    /* requests EEPROM data read operation from slave */
    dwRes = emReadSlaveEEPRomReq(dwInstanceId, dwClientId, 
        dwTferId, EC_TRUE, 1001, 7 /* WORD offset */, awData, 
        EC_NUMOFELEMENTS(awData), &dwNumOutData, 5000 /* timeout */);
    /** DocumentationSnippetsReadSlaveEEPRomReqExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_ReloadSlaveEEPRom)
{
    /** DocumentationSnippetsReloadSlaveEEPRomExample */
    dwRes = emReloadSlaveEEPRom(dwInstanceId, EC_TRUE, 1001, 5000/* timeout */);
    /** DocumentationSnippetsReloadSlaveEEPRomExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_ReloadSlaveEEPRomReq)
{
    EC_T_REGISTERRESULTS RegisterClientResults;
    OsMemset(&RegisterClientResults, 0, sizeof(EC_T_REGISTERRESULTS));

    /** DocumentationSnippetsReloadSlaveEEPRomReqExample */
    EC_T_DWORD dwTferId = 1234; /* arbitrary unique ID from application */
    dwRes = emReloadSlaveEEPRomReq(dwInstanceId, dwClientId, 
        dwTferId, EC_TRUE, 1001, 5000 /* timeout */);
    /** DocumentationSnippetsReloadSlaveEEPRomReqExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_WriteSlaveEEPRom)
{
    EC_T_WORD awData[16];
    EC_T_DWORD dwWriteLen = 0;
    OsMemset(awData, 0, sizeof(awData));
    /** DocumentationSnippetsWriteSlaveEEPRomExample */

    dwRes = emWriteSlaveEEPRom(dwInstanceId, EC_TRUE, 
        1001, 0 /* offset */, awData, dwWriteLen, 5000 /* timeout */);
    /** DocumentationSnippetsWriteSlaveEEPRomExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_WriteSlaveEEPRomReq)
{
    EC_T_REGISTERRESULTS RegisterClientResults;
    OsMemset(&RegisterClientResults, 0, sizeof(EC_T_REGISTERRESULTS));

    EC_T_WORD awData[16];
    EC_T_DWORD dwWriteLen = 0;
    OsMemset(awData, 0, sizeof(awData));

    /** DocumentationSnippetsWriteSlaveEEPRomReqExample */
    EC_T_DWORD dwTferId = 1234; /* arbitrary unique ID from application */
    dwRes = emWriteSlaveEEPRomReq(dwInstanceId, dwClientId, dwTferId, 
        EC_TRUE, 1001, 0 /* offset */, awData, dwWriteLen, 5000 /* timeout */);
    /** DocumentationSnippetsWriteSlaveEEPRomReqExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_AssignSlaveEEPRom)
{
    /** DocumentationSnippetsAssignSlaveEEPRomExample */
    /* set EEPROM access to PDI */
    dwRes = emAssignSlaveEEPRom(dwInstanceId, EC_TRUE, 
        1001, EC_TRUE /* PDI access */, EC_TRUE /* force */, 5000 /* timeout */);
    /** DocumentationSnippetsAssignSlaveEEPRomExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_AssignSlaveEEPRomReq)
{
    EC_T_REGISTERRESULTS RegisterClientResults;
    OsMemset(&RegisterClientResults, 0, sizeof(EC_T_REGISTERRESULTS));

    /** DocumentationSnippetsAssignSlaveEEPRomReqExample */
    /* set EEPROM access to PDI (non-blocking) */
    EC_T_DWORD dwTferId = 1234; /* arbitrary unique ID from application */
    /* requests EEPROM Assignment to PDI or EtherCAT Master operation and return immediately */
    dwRes = emAssignSlaveEEPRomReq(dwInstanceId, dwClientId, dwTferId, 
        EC_TRUE, 1001, EC_TRUE /* PDI access */, EC_TRUE /* force */, 5000 /* timeout */);
    /** DocumentationSnippetsAssignSlaveEEPRomReqExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_ActivateSlaveEEPRomExample)
{
    /** DocumentationSnippetsActivateSlaveEEPRomExample */
    /* check whether EEPROM is marked access active by PDI */
    EC_T_BOOL bSlavePDIAccessActive = EC_FALSE;
    dwRes = emActiveSlaveEEPRom(dwInstanceId, EC_TRUE, 1001, 
        &bSlavePDIAccessActive, 5000 /* timeout */);
    /** DocumentationSnippetsActivateSlaveEEPRomExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_ActivateSlaveEEPRomReqExample)
{
    EC_T_REGISTERRESULTS RegisterClientResults;
    OsMemset(&RegisterClientResults, 0, sizeof(EC_T_REGISTERRESULTS));

    /** DocumentationSnippetsActivateSlaveEEPRomReqExample */
    /* check whether EEPROM is marked access active by PDI (non-blocking) */
    EC_T_DWORD dwTferId = 1234; /* arbitrary unique ID from application */
    EC_T_BOOL bSlavePDIAccessActive = EC_FALSE;
    dwRes = emActiveSlaveEEPRomReq(dwInstanceId, dwClientId, dwTferId, 
        EC_TRUE, 1001, &bSlavePDIAccessActive, 5000 /* timeout */);
    /** DocumentationSnippetsActivateSlaveEEPRomReqExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_ReadSlaveIdentification)
{
    /** DocumentationSnippetsReadSlaveIdentificationExample */
    /* get identification value from slave */
    EC_T_WORD wValue = 0;
    dwRes = emReadSlaveIdentification(dwInstanceId, EC_TRUE, 1001, 
        0x0134 /* explicit device ID */, &wValue, 5000 /* timeout */);
    /** DocumentationSnippetsReadSlaveIdentificationExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_ReadSlaveIdentificationReq)
{
    EC_T_REGISTERRESULTS RegisterClientResults;
    OsMemset(&RegisterClientResults, 0, sizeof(EC_T_REGISTERRESULTS));

    /** DocumentationSnippetsReadSlaveIdentificationReqExample */
    /* get identification value from slave (non-blocking) */
    EC_T_WORD wValue = 0;
    EC_T_DWORD dwTferId = 1234; /* arbitrary unique ID from application */
    dwRes = emReadSlaveIdentificationReq(dwInstanceId, dwClientId,
        dwTferId, EC_TRUE, 1001, 0x0134 /* explicit device ID */, &wValue, 5000 /* timeout */);
    /** DocumentationSnippetsReadSlaveIdentificationReqExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_ReadSlaveRegister)
{
    /** DocumentationSnippetsReadSlaveRegisterExample */
    /* read ESC memory */
    EC_T_BYTE abyData[2] = {0, 0};

    dwRes = emReadSlaveRegister(dwInstanceId, EC_TRUE, 1001, 
        0 /* ADO */, abyData, 2, 5000 /* timeout */);
    /** DocumentationSnippetsReadSlaveRegisterExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_ReadSlaveRegisterReq)
{
    EC_T_REGISTERRESULTS RegisterClientResults;
    OsMemset(&RegisterClientResults, 0, sizeof(EC_T_REGISTERRESULTS));

    /** DocumentationSnippetsReadSlaveRegisterReqExample */
    /* read ESC memory (non-blocking) */
    EC_T_BYTE abyData[2] = {0, 0};
    EC_T_DWORD dwTferId = 1234; /* arbitrary unique ID from application */

    /* get data read transfer from ESC memory of specified slave */
    dwRes = emReadSlaveRegisterReq(dwInstanceId, dwClientId, dwTferId, 
        EC_TRUE, 1001, 0 /* ADO */, abyData, 2);
    /** DocumentationSnippetsReadSlaveRegisterReqExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_SetSlaveDisabled)
{
    /** DocumentationSnippetsSetSlaveDisabledExample */
    /* enable or disable specific slave */
    dwRes = emSetSlaveDisabled(dwInstanceId, EC_TRUE, 1002, EC_TRUE /* disabled */);
    /** DocumentationSnippetsSetSlaveDisabledExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_SetSlaveDisconnected)
{
    /** DocumentationSnippetsSetSlaveDisconnectedExample */
    /*Connect or disconnect specific slave*/
    dwRes = emSetSlaveDisconnected(dwInstanceId, EC_TRUE, 1002, 
        EC_TRUE /* disconnected */);
    /** DocumentationSnippetsSetSlaveDisconnectedExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_SetSlavePortState)
{
    /** DocumentationSnippetsSetSlavePortStateExample */
    EC_T_DWORD dwSlaveId = emGetSlaveId(dwInstanceId, 1001);
    dwRes = emSetSlavePortState(dwInstanceId, dwSlaveId, ESC_PORT_B, 
        EC_TRUE /* close */ , EC_TRUE /* force */, 5000 /* timeout */);
    /** DocumentationSnippetsSetSlavePortStateExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_SetSlavePortStateReq)
{
    EC_T_REGISTERRESULTS RegisterClientResults;
    OsMemset(&RegisterClientResults, 0, sizeof(EC_T_REGISTERRESULTS));

    /** DocumentationSnippetsSetSlavePortStateReqExample */
    EC_T_DWORD dwTferId = 1234; /* arbitrary unique ID from application */
    EC_T_DWORD dwSlaveId = emGetSlaveId(dwInstanceId, 1001);
    dwRes = emSetSlavePortStateReq(dwInstanceId, dwTferId, dwClientId, 
        dwSlaveId, ESC_PORT_B, EC_TRUE /* close */ , EC_TRUE /* force */, 5000 /* timeout */);
    /** DocumentationSnippetsSetSlavePortStateReqExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_SetSlaveState)
{
    /** DocumentationSnippetsSetSlaveStateExample */
    EC_T_DWORD dwSlaveId = emGetSlaveId(dwInstanceId, 1001);
    EC_T_WORD wDeviceState = DEVICE_STATE_PREOP;
    dwRes = emSetSlaveState(dwInstanceId, dwSlaveId, wDeviceState, 5000 /* timeout */);
    /** DocumentationSnippetsSetSlaveStateExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_SetSlaveStateReq)
{
    /** DocumentationSnippetsSetSlaveStateReqExample */
    EC_T_DWORD dwSlaveId = emGetSlaveId(dwInstanceId, 1001);
    EC_T_WORD wDeviceState = DEVICE_STATE_PREOP;
    dwRes = emSetSlaveStateReq(dwInstanceId, dwSlaveId, wDeviceState, 5000 /* timeout */);
    /** DocumentationSnippetsSetSlaveStateReqExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_SetSlavesDisconnected)
{
    /** DocumentationSnippetsSetSlavesDisconnectedExample */
    /* set specific group of slaves for connection or disconnection */
    dwRes = emSetSlavesDisconnected(dwInstanceId, EC_TRUE, 1001, 
        eSlaveSelectionTopoFollowers, EC_TRUE /* disconnected*/);
    /** DocumentationSnippetsSetSlavesDisconnectedExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_SlaveParallelMbxTfers)
{
    /** DocumentationSnippetsSlaveParallelMbxTfersExample */
    /* re-enable parallel mailbox transfers to specified slave */
    EC_T_DWORD dwSlaveId = emGetSlaveId(dwInstanceId, 1001);
    dwRes = emSlaveParallelMbxTfers(dwInstanceId, dwSlaveId);
    /** DocumentationSnippetsSlaveParallelMbxTfersExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_SlaveSerializeMbxTfers)
{
    /** DocumentationSnippetsSlaveSerializeMbxTfersExample */
    /* serialize all mailbox transfers to specified slave */
    EC_T_DWORD dwSlaveId = emGetSlaveId(dwInstanceId, 1001);
    dwRes = emSlaveSerializeMbxTfers(dwInstanceId, dwSlaveId);
    /** DocumentationSnippetsSlaveSerializeMbxTfersExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_WriteSlaveRegister)
{
    EC_T_WORD wRegisterOffset = 0x0120;
    EC_T_BYTE abyData[2] = {0, 0};
    EC_T_WORD wLen = 2;
    /** DocumentationSnippetsWriteSlaveRegisterExample */
    dwRes = emWriteSlaveRegister(dwInstanceId, EC_TRUE, 
        1001, wRegisterOffset, abyData, wLen, 5000 /* timeout */);
    /** DocumentationSnippetsWriteSlaveRegisterExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_WriteSlaveRegisterReq)
{
    EC_T_WORD wRegisterOffset = 0x0120;
    EC_T_BYTE abyData[2] = {0, 0};
    EC_T_WORD wLen = 2;
    
    EC_T_REGISTERRESULTS RegisterClientResults;
    OsMemset(&RegisterClientResults, 0, sizeof(EC_T_REGISTERRESULTS));

    /** DocumentationSnippetsWriteSlaveRegisterReqExample */
    EC_T_DWORD dwTferId = 1234; /* arbitrary unique ID from application */
    /* assigned by application. should be unique for each transfer */

    /* write data into slave's ESC memory */
    dwRes = emWriteSlaveRegisterReq(dwInstanceId, dwClientId, dwTferId, 
        EC_TRUE, 1001, wRegisterOffset, abyData, wLen);
    /** DocumentationSnippetsWriteSlaveRegisterReqExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_StartExample)
{
    /** DocumentationSnippetsStartExample */
    /* set EtherCAT master and all slaves OPERATIONAL */
    dwRes = emStart(dwInstanceId, 5000 /* timeout */);
    /** DocumentationSnippetsStartExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_StopExample)
{
    /** DocumentationSnippetsStopExample */
    /* set EtherCAT master and all slaves back to INIT */
    dwRes = emStop(dwInstanceId, 5000 /* timeout */);
    /** DocumentationSnippetsStopExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_TraceDataConfig)
{
    /** DocumentationSnippetsTraceDataConfigExample */
    /* get trace data offset and size */
    EC_T_TRACE_DATA_INFO traceDataInfo;
    OsMemset(&traceDataInfo, 0, sizeof(EC_T_TRACE_DATA_INFO));
    dwRes = emTraceDataGetInfo(dwInstanceId, &traceDataInfo);
    /** DocumentationSnippetsTraceDataConfigExample */
}

IGNORE_TEST(Api, DOC_RescueScanExample)
{
    /** DocumentationSnippetsRescueScanExample */
    /* recovers bus from permanent frame loss situations */
    dwRes = emRescueScan(dwInstanceId, 5000 /* timeout */);
    /** DocumentationSnippetsRescueScanExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_ResetSlaveController)
{
    /** DocumentationSnippetsResetSlaveControllerExample */
    /* reset EtherCAT slave controller */
    dwRes = emResetSlaveController(dwInstanceId, EC_TRUE, 1001, 5000 /* timeout */);
    /** DocumentationSnippetsResetSlaveControllerExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_ReleaseAllProcessDataBits)
{ 
    /** DocumentationSnippetsReleaseAllProcessDataBitsExample */
    /* release all previously forced process data of client */
    dwRes = emReleaseAllProcessDataBits(dwInstanceId, dwClientId, 5000 /* timeout */);
    /** DocumentationSnippetsReleaseAllProcessDataBitsExample */
}

IGNORE_TEST(Api, DOC_ReleaseProcessDataBits)
{
    /** DocumentationSnippetsReleaseProcessDataBitsExample */
    /* release previously forced process data */
    dwRes = emReleaseProcessDataBits(dwInstanceId, dwClientId,
        EC_FALSE, 0 /* bit offset */, 1 /* bit length */, 5000 /* timeout */);
    /** DocumentationSnippetsReleaseProcessDataBitsExample */
}

IGNORE_TEST(Api, DOC_ConfigureNetworkExample)
{
    /** DocumentationSnippetsConfigureNetworkExample */
    /* load ENI */
    const EC_T_CHAR* szFileName = "eni.xml";
    dwRes = emConfigureNetwork(dwInstanceId, eCnfType_Filename,
        (EC_T_BYTE*)szFileName, (EC_T_DWORD)OsStrlen(szFileName));
    /** DocumentationSnippetsConfigureNetworkExample */
}

IGNORE_TEST(Api, DOC_ConfigGetExample)
{
    EC_T_CHAR* szFileName = EC_NULL;
/** DocumentationSnippetsConfigGetExample */
    EC_T_BYTE* pbyConfigData = EC_NULL;
    EC_T_DWORD dwConfigDataSize = 0;

    /* set config data memory pool */
    EC_IOCTL_SET_CONFIGDATA_MEMORY_POOL_DESC oPoolDesc;
    oPoolDesc.dwSize = 100000; /* max config file size */
    oPoolDesc.pbyStart = (EC_T_BYTE*)OsMalloc(oPoolDesc.dwSize);
    dwRes = emIoCtl(dwInstanceId, EC_IOCTL_SET_CONFIGDATA_MEMORY_POOL,
        &oPoolDesc, sizeof(EC_IOCTL_SET_CONFIGDATA_MEMORY_POOL_DESC),
        EC_NULL, 0, EC_NULL);
    if (dwRes != EC_E_NOERROR)
    {
        dwRetVal = dwRes;
        goto Exit;
    }

    /* load config */
    dwRes = emConfigLoad(dwInstanceId, eCnfType_Filename, 
        (EC_T_BYTE*)szFileName, (EC_T_DWORD)OsStrlen(szFileName));
    if (dwRes != EC_E_NOERROR)
    {
        dwRetVal = dwRes;
        goto Exit;
    }

    /* get config */
    dwRes = emConfigGet(dwInstanceId, &pbyConfigData, &dwConfigDataSize);
    if (dwRes != EC_E_NOERROR)
    {
        dwRetVal = dwRes;
        goto Exit;
    }
/** DocumentationSnippetsConfigGetExample */
    goto Exit;

Exit:
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_ExecJobExample)
{
    /** DocumentationSnippetsExecJobExample */
    EC_T_USER_JOB oUserJob;
    OsMemset(&oUserJob, 0, sizeof(EC_T_USER_JOB));
    oUserJob = eUsrJob_StartTask;
    EC_T_USER_JOB_PARMS oUserJobParms;
    OsMemset(&oUserJobParms, 0, sizeof(EC_T_USER_JOB));
    dwRes = emExecJob(dwInstanceId, oUserJob, &oUserJobParms);
    /** DocumentationSnippetsExecJobExample */
    CHECK_NOERROR(dwRes);
}

static EC_T_DWORD myAppNotify(EC_T_DWORD /* dwCode*/, EC_T_NOTIFYPARMS* /* pParms */) { return EC_E_NOERROR; }
IGNORE_TEST(Api, DOC_RegisterClientExample)
{
    EC_T_VOID* pvMyAppContext = EC_NULL;
    /** DocumentationSnippetsRegisterClientExample */
    EC_T_REGISTERRESULTS oRegResults;
    OsMemset(&oRegResults, 0, sizeof(EC_T_REGISTERRESULTS));
    dwRes = emRegisterClient(dwInstanceId, myAppNotify, pvMyAppContext, &oRegResults);
    /** DocumentationSnippetsRegisterClientExample */
    CHECK_NOERROR(dwRes);
}

/** DocumentationSnippetsLogFrameEnableExampleHandler */
    EC_T_VOID /* EC_FNCALL */ LogFrameHandler(EC_T_VOID* /* pvContext */,
        EC_T_DWORD dwLogFlags, EC_T_DWORD dwFrameSize, EC_T_BYTE* pbyFrame)
    {
        EC_T_WORD wFrameType = EC_ETHFRM_GET_FRAMETYPE(pbyFrame);
        EcLogMsg(EC_LOG_LEVEL_VERBOSE_CYC, (pEcLogContext, EC_LOG_LEVEL_VERBOSE_CYC, 
            "%d: LogFrameHandler(): Type: 0x%04X (%s, %s %s), length: %d bytes\n", wFrameType,
            ((0 != (dwLogFlags & EC_LOG_FRAME_FLAG_RED_FRAME)) ? "RED" : "MAIN"),
            ((0 != (dwLogFlags & EC_LOG_FRAME_FLAG_RX_FRAME)) ? "RX" : "TX"),
            ((0 != (dwLogFlags & EC_LOG_FRAME_FLAG_ACYC_FRAME)) ? "acyclic" : "cyclic"),
        dwFrameSize));
    }
/** DocumentationSnippetsLogFrameEnableExampleHandler */

IGNORE_TEST(Api, DOC_LogFrameEnable)
{
    /** DocumentationSnippetsLogFrameEnableExampleSetup */
    /* setup callback function to log EtherCAT network traffic */
    EC_T_VOID* pvMyAppContext = this;
    dwRes = emLogFrameEnable(dwInstanceId, LogFrameHandler, pvMyAppContext);
    /** DocumentationSnippetsLogFrameEnableExampleSetup */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(Api, DOC_LogFrameDisable)
{
    /** DocumentationSnippetsLogFrameDisableExample */
    /* disable frame logging callback */
    dwRes = emLogFrameDisable(dwInstanceId);
    /** DocumentationSnippetsLogFrameDisableExample */
    CHECK_NOERROR(dwRes);
}

} } /* namespace EcMasterTests::DocumentationSnippets */

