/*-----------------------------------------------------------------------------
 * Doc/EcMaster/Snippets/ClassB/mbx_voe.h
 * Copyright                acontis technologies GmbH, Ravensburg, Germany
 * Response                 Thomas Schoenemann
 * Description
 *---------------------------------------------------------------------------*/

#ifndef INC_DOC_ECMASTER_SNIPPETS_CLASSB_MBX_VOE
#define INC_DOC_ECMASTER_SNIPPETS_CLASSB_MBX_VOE

namespace EcMasterTests { namespace DocumentationSnippets {

TEST_GROUP(MbxVoe), CDocumentationSnippetsBase
{
    EC_T_DWORD dwRetVal;
    EC_T_DWORD dwRes;
    EC_T_DWORD dwInstanceId;
    EC_T_DWORD dwSimulatorId;
};

IGNORE_TEST(DocumentationSnippets, emTestVoeReadWrite)
{
    // InstallVoeReceiveCallback();
    EC_T_BYTE  abyVoeDataOutBuf[6] = { 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF };
    EC_T_BYTE  abyVoeDataInBuf[6];
    EC_T_DWORD dwSlaveId = emGetSlaveId(dwInstanceId, 1006);
    EC_T_DWORD dwDataOutLen = 0;
    dwRes = EC_E_ERROR;

    OsMemset(abyVoeDataInBuf, 0, 6);
    /** DocumentationSnippetsVoeWriteExample */
    dwRes = emVoeWrite(dwInstanceId, dwSlaveId, abyVoeDataOutBuf, 
        sizeof(abyVoeDataOutBuf), 5000);
    if(dwRes != EC_E_NOERROR) {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, 
            "emVoeWrite(...): %s (0x%lx))\n", ecatGetText(dwRes), dwRes));
    }
    /** DocumentationSnippetsVoeWriteExample */
    dwRes = esVoeSend(dwSimulatorId, 1006, 0, abyVoeDataOutBuf, 6);
    /** DocumentationSnippetsVoeReadExample */
    dwRes = emVoeRead(dwInstanceId, dwSlaveId, abyVoeDataInBuf, 
        sizeof(abyVoeDataInBuf), &dwDataOutLen, 5000);
    if(dwRes != EC_E_NOERROR) {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, 
            "emVoeRead(...): %s (0x%lx))\n", ecatGetText(dwRes), dwRes));
    }
    /** DocumentationSnippetsVoeReadExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(DocumentationSnippets, emVoeWriteReq)
{
    EC_T_BYTE  abyVoeDataInBuf[6];
    OsMemset(abyVoeDataInBuf, 0, 6);
    EC_T_DWORD dwSlaveId = emGetSlaveId(dwInstanceId, 1006 /* slave station address */);

    /** DocumentationSnippetsVoeWriteReqExampleCreateMbxTferObject */
    EC_T_MBXTFER_DESC oMbxTferDesc; /* mailbox transfer descriptor */
    OsMemset(&oMbxTferDesc, 0, sizeof(EC_T_MBXTFER_DESC));
    oMbxTferDesc.dwMaxDataLen = sizeof(abyVoeDataInBuf);
    oMbxTferDesc.pbyMbxTferDescData = abyVoeDataInBuf;

    /* create mailbox transfer object with pre-allocate payload memory */
    EC_T_MBXTFER* pMbxTfer = EC_NULL;
    pMbxTfer = emMbxTferCreate(dwInstanceId, &oMbxTferDesc);
    if (EC_NULL == pMbxTfer)
    {
        dwRetVal = EC_E_NOMEMORY;
        goto Exit;
    }
    /** DocumentationSnippetsVoeWriteReqExampleCreateMbxTferObject */

    /** DocumentationSnippetsVoeWriteReqExampleApiCall */
    dwRes = emVoeWriteReq(dwInstanceId, pMbxTfer, dwSlaveId, 5000);
    if (dwRes != EC_E_NOERROR)
    {
        dwRetVal = dwRes;
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "emVoeWriteReq: %s (0x%lx))\n", ecatGetText(dwRes), dwRes));
        goto Exit;
    }
    /** DocumentationSnippetsVoeWriteReqExampleApiCall */

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
        /** DocumentationSnippetsVoeWriteReqExampleDeleteMbxTferObject */
        emMbxTferDelete(dwInstanceId, pMbxTfer);
        /** DocumentationSnippetsVoeWriteReqExampleDeleteMbxTferObject */
    }
    /** DocumentationSnippetsVoeWriteReqExample */
    SafeOsFree(oMbxTferDesc.pbyMbxTferDescData);

    CHECK_NOERROR(dwRes);
}

} } /* namespace EcMasterTests/DocumentationSnippets */

#endif /* INC_DOC_ECMASTER_SNIPPETS_CLASSB_MBX_VOE */
