/*-----------------------------------------------------------------------------
 * Doc/EcMaster/Snippets/ClassB/mbx_foe.h
 * Copyright                acontis technologies GmbH, Ravensburg, Germany
 * Response                 Paul Bussmann
 * Description
 *---------------------------------------------------------------------------*/

#ifndef INC_DOC_ECMASTER_SNIPPETS_CLASSB_MBX_FOE
#define INC_DOC_ECMASTER_SNIPPETS_CLASSB_MBX_FOE

namespace EcMasterTests { namespace DocumentationSnippets {

TEST_GROUP(MbxFoe), CDocumentationSnippetsBase
{
};

#define MY_FOE_SLAVE_ADDRESS EM_TEST_SLAVE /* e.g. 1001 */
#define MY_FOE_TRANSFER_LOCAL_FILENAME (EC_T_CHAR*)ECMASTERTESTS_FILES_DIR FOE_SEG_UPLOAD_IN_FILENAME  /* e.g. (EC_T_CHAR*)"MyFile.dat" */
#define MY_FOE_TRANSFER_SLAVE_FILENAME (EC_T_CHAR*)FOE_SEG_UPLOAD_IN_FILENAME  /* e.g. (EC_T_CHAR*)"MyFile.dat" */

EC_T_DWORD FoeDownloadExample(EC_T_DWORD* pdwBufferSize)
{
    /** DocumentationSnippetsFoeDownloadExample */
    EC_T_DWORD dwRetVal = EC_E_ERROR;
    EC_T_DWORD dwRes = EC_E_ERROR;

    EC_T_WORD  wSlaveAddress = MY_FOE_SLAVE_ADDRESS /* e.g. 1001 */;
    EC_T_DWORD dwSlaveId = ecatGetSlaveId(wSlaveAddress);

    FILE*      pfLocalFile = EC_NULL;

    EC_T_BYTE* pbyBuffer = EC_NULL;
    EC_T_DWORD dwBufferSize = 0;

    /* read file to buffer */
    pfLocalFile = OsFopen(MY_FOE_TRANSFER_LOCAL_FILENAME, "rb");
    if (EC_NULL == pfLocalFile)
    {
        dwRetVal = EC_E_OPENFAILED;
        goto Exit;
    }
    dwBufferSize = OsGetFileSize(pfLocalFile);

    pbyBuffer = (EC_T_BYTE*)OsMalloc(dwBufferSize);
    if (EC_NULL == pbyBuffer)
    {
        dwRetVal = EC_E_NOMEMORY;
        goto Exit;
    }
    dwRes = (EC_T_DWORD)OsFread(pbyBuffer, 1, dwBufferSize, pfLocalFile);
    if (dwRes != dwBufferSize)
    {
        dwRetVal = EC_E_ERROR;
        goto Exit;
    }

    /* download buffer to slave */
    dwRes = ecatFoeFileDownload(dwSlaveId, MY_FOE_TRANSFER_SLAVE_FILENAME,
        (EC_T_DWORD)OsStrlen(MY_FOE_TRANSFER_SLAVE_FILENAME),
        pbyBuffer, dwBufferSize, 0, 600000 /* 10 minutes */);
    if (EC_E_NOERROR != dwRes)
    {
        dwRetVal = dwRes;
        goto Exit;
    }

    dwRetVal = EC_E_NOERROR;
Exit:
    /* free resources */
    if (EC_NULL != pfLocalFile)
    {
        OsFclose(pfLocalFile);
    }
    SafeOsFree(pbyBuffer);
    /** DocumentationSnippetsFoeDownloadExample */

    *pdwBufferSize = dwBufferSize;
    return dwRetVal;
}
#undef MY_FOE_SLAVE_ADDRESS 
#undef MY_FOE_TRANSFER_LOCAL_FILENAME 
#undef MY_FOE_TRANSFER_SLAVE_FILENAME

#define MY_FOE_SLAVE_ADDRESS EM_TEST_SLAVE                         /* e.g. 1001 */
#define MY_FOE_TRANSFER_LOCAL_FILENAME FOE_SEG_UPLOAD_OUT_FILENAME /* e.g. (EC_T_CHAR*)"MyFile.dat" */
#define MY_FOE_TRANSFER_SLAVE_FILENAME FOE_SEG_UPLOAD_IN_FILENAME  /* e.g. (EC_T_CHAR*)"MyFile.dat" */
EC_T_DWORD FoeSegmentedUploadReqExample(EC_T_DWORD* pdwFileSize)
{
    /** DocumentationSnippetsFoeSegmentedUploadReqExample */
    EC_T_DWORD dwRetVal = EC_E_ERROR;
    EC_T_DWORD dwRes = EC_E_ERROR;

    EC_T_WORD  wSlaveAddress = MY_FOE_SLAVE_ADDRESS /* e.g. 1001 */;
    EC_T_DWORD dwSlaveId = ecatGetSlaveId(wSlaveAddress);

    EC_T_CFG_SLAVE_INFO oCfgSlaveInfo;

    FILE*               pfLocalFile = EC_NULL;
    EC_T_DWORD          dwFileSize = 0;

    EC_T_MBXTFER_DESC   oMbxTferDesc;
    EC_T_MBXTFER*       pMbxTfer = EC_NULL;
    EC_T_BYTE*          pbyBuffer = EC_NULL;
    EC_T_DWORD          dwBufferSize = 0;

    OsMemset(&oCfgSlaveInfo, 0, sizeof(EC_T_CFG_SLAVE_INFO));
    OsMemset(&oMbxTferDesc, 0, sizeof(EC_T_MBXTFER_DESC));

    /* get max. FoE segment size */
    dwRes = ecatGetCfgSlaveInfo(EC_TRUE, wSlaveAddress, &oCfgSlaveInfo);
    if (EC_E_NOERROR != dwRes)
    {
        dwRetVal = dwRes;
        goto Exit;
    }
    /* mailbox contains mailbox header, FoE header and payload for buffer */
    dwBufferSize = oCfgSlaveInfo.dwMbxInSize - ETHERCAT_MAX_FOE_MBOX_HDR_LEN;

    /* allocate segment buffer */
    pbyBuffer = (EC_T_BYTE*)OsMalloc(dwBufferSize);
    if (EC_NULL == pbyBuffer)
    {
        dwRetVal = EC_E_NOMEMORY;
        goto Exit;
    }
    oMbxTferDesc.pbyMbxTferDescData = pbyBuffer;
    oMbxTferDesc.dwMaxDataLen = dwBufferSize;
    pMbxTfer = ecatMbxTferCreate(&oMbxTferDesc);
    if (EC_NULL == pMbxTfer)
    {
        dwRetVal = EC_E_NOMEMORY;
        goto Exit;
    }
    pMbxTfer->dwTferId = 0x12345678; /* uniq ID from application */

    /* open local file */
    pfLocalFile = OsFopen(MY_FOE_TRANSFER_LOCAL_FILENAME /* e.g. (EC_T_CHAR*)"MyFile.dat" */, "wb");
    if (EC_NULL == pfLocalFile)
    {
        dwRetVal = EC_E_OPENFAILED;
        goto Exit;
    }

    /* start upload */
    dwRes = ecatFoeSegmentedUploadReq(pMbxTfer, dwSlaveId,
        MY_FOE_TRANSFER_SLAVE_FILENAME /* e.g. (EC_T_CHAR*)"MyFile.dat" */, (EC_T_DWORD)OsStrlen(MY_FOE_TRANSFER_SLAVE_FILENAME),
        0xFFFFFFFF /* unknown file size */, 0, MBX_TIMEOUT /* e.g. 5000 */);
    if (EC_E_NOERROR != dwRes)
    {
        dwRetVal = dwRes;
        goto Exit;
    }

    /* upload file writing segments to disk */
    while ((eMbxTferStatus_Pend == pMbxTfer->eTferStatus)
        || (eMbxTferStatus_TferWaitingForContinue == pMbxTfer->eTferStatus))
    {
        /* wait for master received data from slave */
        if (eMbxTferStatus_TferWaitingForContinue == pMbxTfer->eTferStatus)
        {
            /* write segment */
            OsFwrite(pMbxTfer->pbyMbxTferData, pMbxTfer->dwDataLen, 1, pfLocalFile);
            dwFileSize = dwFileSize + pMbxTfer->dwDataLen;

            /* acknowledge segment so master can receive the next segment */
            dwRes = ecatFoeSegmentedUploadReq(pMbxTfer, 0, EC_NULL, 0, 0, 0, 0);
            if (EC_E_NOERROR != dwRes)
            {
                dwRetVal = dwRes;
                goto Exit;
            }
        }
        OsSleep(10);
    }
    if (eMbxTferStatus_TferReqError == pMbxTfer->eTferStatus)
    {
        dwRetVal = pMbxTfer->dwErrorCode;
        goto Exit;
    }

    /* transfer done */
    if (eMbxTferStatus_TferDone == pMbxTfer->eTferStatus)
    {
        dwRetVal = pMbxTfer->dwErrorCode; /* e.g. EC_E_NOERROR */
        pMbxTfer->eTferStatus = eMbxTferStatus_Idle;
    }

Exit:
    /* free resources */
    if (EC_NULL != pfLocalFile)
    {
        OsFclose(pfLocalFile);
    }
    if (EC_NULL != pMbxTfer)
    {
        if (eMbxTferStatus_Pend == pMbxTfer->eTferStatus)
        {
            CEcTimer oTimeout(MBX_TIMEOUT);
            ecatMbxTferAbort(pMbxTfer);
            while ((eMbxTferStatus_Pend == pMbxTfer->eTferStatus) && !oTimeout.IsElapsed())
            {
                OsSleep(100);
            }
        }
        ecatMbxTferDelete(pMbxTfer);
    }
    SafeOsFree(pbyBuffer);
    /** DocumentationSnippetsFoeSegmentedUploadReqExample */
    *pdwFileSize = dwFileSize;
    return dwRetVal;
}
#undef MY_FOE_SLAVE_ADDRESS 
#undef MY_FOE_TRANSFER_LOCAL_FILENAME 
#undef MY_FOE_TRANSFER_SLAVE_FILENAME

/* PBN, 2022-08-01, V3.1.4.03: test changed to include snippets for EC-Master User Manual
   TODO: Fix */
IGNORE_TEST(MbxCoe, DOC_TestSegmentedUploadReqExample)
{
    CEcSimulatorSilTestApplication oTestApplication;
    oTestApplication.SetupMaster(oTestApplication.GetEniFileName(), eEcatState_PREOP);

    GenerateFoeSegUploadInFile();

    /* download test data */
    {
        EC_T_DWORD dwBufferSize = 0;
        CHECK_NOERROR(FoeDownloadExample(&dwBufferSize));
        CHECK_DWORD_EQUAL(FOE_SEG_UPLOAD_FILESIZE, dwBufferSize);
    }

    /* upload test data */
    {
        EC_T_DWORD dwFileSize = 0;
        CHECK_NOERROR(FoeSegmentedUploadReqExample(&dwFileSize));
        CHECK_DWORD_EQUAL(FOE_SEG_UPLOAD_FILESIZE, dwFileSize);
    }

    CHECK_FILES_EQUAL(FOE_SEG_UPLOAD_IN_FILENAME, FOE_SEG_UPLOAD_OUT_FILENAME);
}

} } /* namespace EcMasterTests::DocumentationSnippets */

#endif /* INC_DOC_ECMASTER_SNIPPETS_CLASSB_MBX_FOE */
