/*-----------------------------------------------------------------------------
 * Doc/EcMaster/Snippets/ClassB/mbx_coe.h
 * Copyright                acontis technologies GmbH, Ravensburg, Germany
 * Response                 Paul Bussmann
 * Description
 *---------------------------------------------------------------------------*/

#ifndef INC_DOC_ECMASTER_SNIPPETS_CLASSB_MBX_COE
#define INC_DOC_ECMASTER_SNIPPETS_CLASSB_MBX_COE

namespace EcMasterTests { namespace DocumentationSnippets {

TEST_GROUP(MbxCoe), CDocumentationSnippetsBase
{
};

/** DocumentationSnippetsCoeSdoDownloadExample */
EC_T_DWORD CoeSdoDownloadExample()
{
    EC_T_DWORD dwRetVal = EC_E_ERROR;
    EC_T_DWORD dwRes = EC_E_ERROR;

    /* slave with station address 2002 used for CoE SDO download */
    EC_T_DWORD        dwSlaveId = ecatGetSlaveId(2002);
    EC_T_BYTE         abyBuf[4];
    OsMemset(abyBuf, 0, sizeof(abyBuf));

    /* download value 123 to object index 0x40A2, subindex 2, timeout 5s, no complete access */
    EC_SET_FRM_DWORD(abyBuf, 123);
    dwRes = ecatCoeSdoDownload(dwSlaveId, 0x40A2, 2, abyBuf, (EC_T_DWORD)sizeof(abyBuf), 5000, 0);
    if (EC_E_NOERROR != dwRes)
    {
        dwRetVal = dwRes;
        goto Exit;
    }

    dwRetVal = EC_E_NOERROR;
Exit:
    return dwRetVal;
}
/** DocumentationSnippetsCoeSdoDownloadExample */

TEST(MbxCoe, DOC_CoeSdoDownloadExample)
{
    CEcSimulatorSilTestApplication oTestApplication;
    oTestApplication.SetupMaster(oTestApplication.GetEniFileName(), eEcatState_PREOP);

    CHECK_NOERROR(CoeSdoDownloadExample());
}

/** DocumentationSnippetsCoeSdoDownloadReqExample */
EC_T_DWORD CoeSdoDownloadReqExample()
{
    EC_T_DWORD dwRetVal = EC_E_ERROR;
    EC_T_DWORD dwRes = EC_E_ERROR;

    /* needed only for notifications, see
     - ecatRegisterClient(...)
     - pAppContext->pNotificationHandler->GetClientID() */
    EC_T_DWORD        dwClientId = 0;

    /* slave with station address 2002 used for CoE SDO download */
    EC_T_DWORD        dwSlaveId = ecatGetSlaveId(2002);

    EC_T_MBXTFER*     pMbxTferObject = EC_NULL;
    EC_T_BYTE         abyBuf[4];
    EC_T_MBXTFER_DESC oObjectDataTferDesc;
    OsMemset(abyBuf, 0, sizeof(abyBuf));
    OsMemset(&oObjectDataTferDesc, 0, sizeof(EC_T_MBXTFER_DESC));

    /* create mailbox transfer object */
    oObjectDataTferDesc.pbyMbxTferDescData = abyBuf;
    oObjectDataTferDesc.dwMaxDataLen = sizeof(abyBuf);
    pMbxTferObject = ecatMbxTferCreate(&oObjectDataTferDesc);
    if (EC_NULL == pMbxTferObject)
    {
        dwRes = EC_E_NOMEMORY;
        dwRetVal = dwRes;
        goto Exit;
    }

    /* create mailbox transfer object */
    pMbxTferObject->dwClntId = dwClientId;
    pMbxTferObject->dwTferId = 1; /* assigned by application. should be unique for each object */

    /* request download of value 123 to object index 0x40A2, subindex 2, timeout 5s, no complete access */
    EC_SET_FRM_DWORD(abyBuf, 123);
    dwRes = ecatCoeSdoDownloadReq(pMbxTferObject, dwSlaveId, 0x40A2, 2, 5000, 0);
    if (EC_E_NOERROR != dwRes)
    {
        dwRetVal = dwRes;
        goto Exit;
    }

    /* wait for transfer finished */
    while (eMbxTferStatus_Pend == pMbxTferObject->eTferStatus)
    {
        OsSleep(10);
    }

    /* check transfer result */
    dwRes = pMbxTferObject->dwErrorCode;
    if (EC_E_NOERROR != dwRes)
    {
        dwRetVal = dwRes;
        goto Exit;
    }

    dwRetVal = EC_E_NOERROR;
Exit:
    if (EC_NULL != pMbxTferObject)
    {
        pMbxTferObject->eTferStatus = eMbxTferStatus_Idle;
        ecatMbxTferDelete(pMbxTferObject);
    }

    return dwRetVal;
}
/** DocumentationSnippetsCoeSdoDownloadReqExample */

TEST(MbxCoe, DOC_CoeSdoDownloadReqExample)
{
    CEcSimulatorSilTestApplication oTestApplication;
    oTestApplication.SetupMaster(oTestApplication.GetEniFileName(), eEcatState_PREOP);

    CHECK_NOERROR(CoeSdoDownloadReqExample());
}

/** DocumentationSnippetsCoeSdoUploadExample */
EC_T_DWORD CoeSdoUploadExample()
{
    EC_T_DWORD dwRetVal = EC_E_ERROR;
    EC_T_DWORD dwRes = EC_E_ERROR;

    /* slave with station address 2002 used for CoE SDO upload */
    EC_T_DWORD        dwSlaveId = ecatGetSlaveId(2002);
    EC_T_BYTE         abyBuf[4];
    OsMemset(abyBuf, 0, sizeof(abyBuf));

    /* upload object index 0x1018, subindex 1, timeout 5s, no complete access */
    dwRes = ecatCoeSdoUpload(dwSlaveId, 0x1018, 1, abyBuf, (EC_T_DWORD)sizeof(abyBuf), EC_NULL, 5000, 0);
    if (EC_E_NOERROR != dwRes)
    {
        dwRetVal = dwRes;
        goto Exit;
    }

    dwRetVal = EC_E_NOERROR;
Exit:
    return dwRetVal;
}
/** DocumentationSnippetsCoeSdoUploadExample */

TEST(MbxCoe, DOC_CoeSdoUploadExample)
{
    CEcSimulatorSilTestApplication oTestApplication;
    oTestApplication.SetupMaster(oTestApplication.GetEniFileName(), eEcatState_PREOP);

    CHECK_NOERROR(CoeSdoUploadExample());
}

/** DocumentationSnippetsCoeSdoUploadReqExample */
EC_T_DWORD CoeSdoUploadReqExample()
{
    EC_T_DWORD dwRetVal = EC_E_ERROR;
    EC_T_DWORD dwRes = EC_E_ERROR;

    /* needed only for notifications, see
     - ecatRegisterClient(...)
     - pAppContext->pNotificationHandler->GetClientID() */
    EC_T_DWORD        dwClientId = 0;

    /* slave with station address 2002 used for CoE SDO upload */
    EC_T_DWORD        dwSlaveId = ecatGetSlaveId(2002);

    EC_T_MBXTFER*     pMbxTferObject = EC_NULL;
    EC_T_BYTE         abyBuf[4];
    EC_T_MBXTFER_DESC oObjectDataTferDesc;
    OsMemset(abyBuf, 0, sizeof(abyBuf));
    OsMemset(&oObjectDataTferDesc, 0, sizeof(EC_T_MBXTFER_DESC));

    /* create mailbox transfer object */
    oObjectDataTferDesc.pbyMbxTferDescData = abyBuf;
    oObjectDataTferDesc.dwMaxDataLen = sizeof(abyBuf);
    pMbxTferObject = ecatMbxTferCreate(&oObjectDataTferDesc);
    if (EC_NULL == pMbxTferObject)
    {
        dwRes = EC_E_NOMEMORY;
        dwRetVal = dwRes;
        goto Exit;
    }

    /* create mailbox transfer object */
    pMbxTferObject->dwClntId = dwClientId;
    pMbxTferObject->dwTferId = 1; /* assigned by application. should be unique for each object */

    /* request upload of object index 0x1018, subindex 1, timeout 5s, no complete access */
    dwRes = ecatCoeSdoUploadReq(pMbxTferObject, dwSlaveId, 0x1018, 1, 5000, 0);
    if (EC_E_NOERROR != dwRes)
    {
        dwRetVal = dwRes;
        goto Exit;
    }

    /* wait for transfer finished */
    while (eMbxTferStatus_Pend == pMbxTferObject->eTferStatus)
    {
        OsSleep(10);

        /* transfer can be canceled using ecatMbxTferAbort(...) if it takes too long */
    }

    /* check transfer result */
    dwRes = pMbxTferObject->dwErrorCode;
    if (EC_E_NOERROR != dwRes)
    {
        dwRetVal = dwRes;
        goto Exit;
    }

    dwRetVal = EC_E_NOERROR;
Exit:
    if (EC_NULL != pMbxTferObject)
    {
        pMbxTferObject->eTferStatus = eMbxTferStatus_Idle;
        ecatMbxTferDelete(pMbxTferObject);
    }

    return dwRetVal;
}
/** DocumentationSnippetsCoeSdoUploadReqExample */

TEST(MbxCoe, DOC_CoeSdoUploadReqExample)
{
    CEcSimulatorSilTestApplication oTestApplication;
    oTestApplication.SetupMaster(oTestApplication.GetEniFileName(), eEcatState_PREOP);

    CHECK_NOERROR(CoeSdoUploadReqExample());
}

IGNORE_TEST(MbxCoe, DOC_emCoeGetODListReq)
{
    CEcSimulatorSilTestApplication oTestApplication;
    T_EC_DEMO_APP_CONTEXT* pAppContext = oTestApplication.GetAppContext();
    dwInstanceId = pAppContext->dwInstanceId;
    EC_T_DWORD        dwSlaveId = emGetSlaveId(dwInstanceId, 1001 /* slave station address */);

    /** DocumentationSnippetsCoeGetODListReqExample */
    EC_T_MBXTFER*     pMbxTfer = EC_NULL;
    EC_T_MBXTFER_DESC oMbxTferDesc;

    OsMemset(&oMbxTferDesc, 0, sizeof(EC_T_MBXTFER_DESC));
    oMbxTferDesc.dwMaxDataLen = CROD_ODLTFER_SIZE;

    /* allocate payload memory */
    oMbxTferDesc.pbyMbxTferDescData = (EC_T_BYTE*)OsMalloc(oMbxTferDesc.dwMaxDataLen);
    if (EC_NULL == oMbxTferDesc.pbyMbxTferDescData)
    {
        dwRetVal = EC_E_NOMEMORY;
        goto Exit;
    }

    /* create mailbox transfer object */
    pMbxTfer = emMbxTferCreate(dwInstanceId, &oMbxTferDesc);
    if (EC_NULL == pMbxTfer)
    {
        dwRetVal = EC_E_NOMEMORY;
        goto Exit;
    }

    dwRes = emCoeGetODListReq(dwInstanceId, pMbxTfer, dwSlaveId, eODListType_ALL, 5000 /* timeout */);
    if (dwRes != EC_E_NOERROR)
    {
        dwRetVal = dwRes;
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "emCoeGetODList: %s (0x%lx))\n", ecatGetText(dwRes), dwRes));
        goto Exit;
    }

    /* wait for transfer finished, see also emMbxTferAbort(...) */
    while (eMbxTferStatus_Pend == pMbxTfer->eTferStatus)
    {
        OsSleep(10);
    }

    dwRetVal = pMbxTfer->dwErrorCode;
Exit:
    if (EC_NULL != pMbxTfer)
    {
        if (eMbxTferStatus_Pend == pMbxTfer->eTferStatus)
        {
            emMbxTferAbort(dwInstanceId, pMbxTfer);
        }
        emMbxTferDelete(dwInstanceId, pMbxTfer);
    }

    SafeOsFree(oMbxTferDesc.pbyMbxTferDescData);
    /** DocumentationSnippetsCoeGetODListReqExample */

    CHECK_NOERROR(dwRetVal);
}

IGNORE_TEST(MbxCoe, DOC_emCoeGetObjectDescReq)
{
    CEcSimulatorSilTestApplication oTestApplication;
    T_EC_DEMO_APP_CONTEXT* pAppContext = oTestApplication.GetAppContext();
    dwInstanceId = pAppContext->dwInstanceId;
    EC_T_DWORD        dwSlaveId = emGetSlaveId(dwInstanceId, 1001 /* slave station address */);

    /** DocumentationSnippetsCoeGetObjectDescReqExample */
    EC_T_MBXTFER*     pMbxTfer = EC_NULL;
    EC_T_MBXTFER_DESC oMbxTferDesc; /* mailbox transfer descriptor */

    OsMemset(&oMbxTferDesc, 0, sizeof(EC_T_MBXTFER_DESC));
    oMbxTferDesc.dwMaxDataLen = CROD_OBDESC_SIZE;

    /* allocate payload memory */
    oMbxTferDesc.pbyMbxTferDescData = (EC_T_BYTE*)OsMalloc(oMbxTferDesc.dwMaxDataLen);
    if (EC_NULL == oMbxTferDesc.pbyMbxTferDescData)
    {
        dwRetVal = EC_E_NOMEMORY;
        goto Exit;
    }

    /* create mailbox transfer object */
    pMbxTfer = emMbxTferCreate(dwInstanceId, &oMbxTferDesc);
    if (EC_NULL == pMbxTfer)
    {
        dwRetVal = EC_E_NOMEMORY;
        goto Exit;
    }
    dwRes = emCoeGetObjectDescReq(dwInstanceId, pMbxTfer, dwSlaveId, 0x6411, 5000);
    if (dwRes != EC_E_NOERROR)
    {
        dwRetVal = dwRes;
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "emCoeGetObjectDescReq: %s (0x%lx))\n", ecatGetText(dwRes), dwRes));
        goto Exit;
    }

    /* wait for transfer finished, see also emMbxTferAbort(...) */
    while (eMbxTferStatus_Pend == pMbxTfer->eTferStatus)
    {
        OsSleep(10);
    }

    dwRetVal = pMbxTfer->dwErrorCode;
Exit:
    if (EC_NULL != pMbxTfer)
    {
        if (eMbxTferStatus_Pend == pMbxTfer->eTferStatus)
        {
            emMbxTferAbort(dwInstanceId, pMbxTfer);
        }
        emMbxTferDelete(dwInstanceId, pMbxTfer);
    }

    SafeOsFree(oMbxTferDesc.pbyMbxTferDescData);
    /** DocumentationSnippetsCoeGetObjectDescReqExample */

    CHECK_NOERROR(dwRetVal);
}

IGNORE_TEST(MbxCoe, DOC_emCoeGetEntryDescReq)
{
    CEcSimulatorSilTestApplication oTestApplication;
    T_EC_DEMO_APP_CONTEXT* pAppContext = oTestApplication.GetAppContext();
    dwInstanceId = pAppContext->dwInstanceId;
    EC_T_DWORD        dwSlaveId = emGetSlaveId(dwInstanceId, 1001 /* slave station address */);

    /** DocumentationSnippetsCoeGetEntryDescReqExample */
    EC_T_MBXTFER*     pMbxTfer = EC_NULL;
    EC_T_MBXTFER_DESC oMbxTferDesc; /* mailbox transfer descriptor */

    OsMemset(&oMbxTferDesc, 0, sizeof(EC_T_MBXTFER_DESC));
    oMbxTferDesc.dwMaxDataLen = CROD_ENTRYDESC_SIZE;
    oMbxTferDesc.pbyMbxTferDescData = (EC_T_BYTE*)OsMalloc(oMbxTferDesc.dwMaxDataLen);

    /* allocate payload memory */
    if (EC_NULL == oMbxTferDesc.pbyMbxTferDescData)
    {
        dwRetVal = EC_E_NOMEMORY;
        goto Exit;
    }

    /* create transfer object */
    pMbxTfer = emMbxTferCreate(dwInstanceId, &oMbxTferDesc);
    if (EC_NULL == pMbxTfer)
    {
        dwRetVal = EC_E_NOMEMORY;

        goto Exit;
    }
    dwRes = emCoeGetEntryDescReq(dwInstanceId, pMbxTfer, dwSlaveId, 0x6411, 1, 0, 5000);
    if (dwRes != EC_E_NOERROR)
    {
        dwRetVal = dwRes;
        goto Exit;
    }

    /* wait for transfer finished, see also emMbxTferAbort(...) */
    while (eMbxTferStatus_Pend == pMbxTfer->eTferStatus)
    {
        OsSleep(10);
    }

    dwRetVal = pMbxTfer->dwErrorCode;
Exit:
    if (EC_NULL != pMbxTfer)
    {
        if (eMbxTferStatus_Pend == pMbxTfer->eTferStatus)
        {
            emMbxTferAbort(dwInstanceId, pMbxTfer);
        }
        emMbxTferDelete(dwInstanceId, pMbxTfer);
    }

    SafeOsFree(oMbxTferDesc.pbyMbxTferDescData);
    /** DocumentationSnippetsCoeGetEntryDescReqExample */

    CHECK_NOERROR(dwRetVal);
}

IGNORE_TEST(MbxCoe, DOC_emCoeProfileGetChannelInfo)
{
    CEcSimulatorSilTestApplication oTestApplication;
    T_EC_DEMO_APP_CONTEXT* pAppContext = oTestApplication.GetAppContext();
    dwInstanceId = pAppContext->dwInstanceId;
    EC_T_WORD wSlaveAddress = 1006;

    /** DocumentationSnippetsCoeProfileGetChannelInfoExample */
    /* get information about CoE profile channel configured in ENI */
    EC_T_PROFILE_CHANNEL_INFO oInfo;
    dwRes = emCoeProfileGetChannelInfo(dwInstanceId, EC_TRUE, wSlaveAddress, 0, &oInfo);
    /** DocumentationSnippetsCoeProfileGetChannelInfoExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(MbxCoe, DOC_emConvertEcErrorToCoeError)
{
    EC_T_DWORD dwCoeError;
    CEcSimulatorSilTestApplication oTestApplication;
    T_EC_DEMO_APP_CONTEXT* pAppContext = oTestApplication.GetAppContext();
    dwInstanceId = pAppContext->dwInstanceId;

    /** DocumentationSnippetsConvertEcErrorToCoeErrorExample*/
    dwCoeError = emConvertEcErrorToCoeError(dwInstanceId, EC_E_NOERROR);
    /** DocumentationSnippetsConvertEcErrorToCoeErrorExample*/
    EC_UNREFPARM(dwCoeError);
}

} } /* namespace EcMasterTests::DocumentationSnippets */

#endif /* INC_DOC_ECMASTER_SNIPPETS_CLASSB_MBX_COE */
