namespace EcMasterTests { namespace DocumentationSnippets {

#if (defined EC_IOCTL_SET_SPLIT_FRAME_PROCESSING_ENABLED)
IGNORE_TEST(DocumentationSnippets, SplitFrame_Config)
{
    /* IGNORE_TEST(DocumentationSnippets, SplitFrame_Config)_IoControl */
    dwRes = emInitMaster(dwInstanceId, &oInitMasterParms);
    /* Enable split frame processing */
    {
        EC_T_BOOL bEnableSplitFrameProc = EC_TRUE;
        EC_T_IOCTLPARMS oIoCtlParms;

        OsMemset(&oIoCtlParms, 0, sizeof(EC_T_IOCTLPARMS));
        oIoCtlParms.pbyInBuf = (EC_T_BYTE*)&bEnableSplitFrameProc;
        oIoCtlParms.dwInBufSize = sizeof(EC_T_BOOL);

        dwRes = emIoControl(dwInstanceId, EC_IOCTL_SET_SPLIT_FRAME_PROCESSING_ENABLED, &oIoCtlParms);
    }
    /* create cyclic task to trigger jobs */

    /* IGNORE_TEST(DocumentationSnippets, SplitFrame_Config)_IoControl */

    /* IGNORE_TEST(DocumentationSnippets, SplitFrame_Config)_Interrupt */
    {
        EC_T_CYCFRAME_RX_CBDESC oCyRxDesc;
        EC_T_IOCTLPARMS         oIoCtlParms;

        /* setup callback function which is called after RX */
        OsMemset(&oCyRxDesc, 0, sizeof(EC_T_CYCFRAME_RX_CBDESC));
        oCyRxDesc.pfnCallback = CycFrameReceivedCallback;
        oCyRxDesc.pCallbackContext = EC_NULL;

        OsMemset(&oIoCtlParms, 0, sizeof(EC_T_IOCTLPARMS));
        oIoCtlParms.dwInBufSize = sizeof(oCyRxDesc);
        oIoCtlParms.pbyInBuf = (EC_T_PBYTE)&oCyRxDesc;

        dwRes = emIoControl(dwInstanceId, EC_IOCTL_REGISTER_CYCFRAME_RX_CB, &oIoCtlParms);
    }
    /* IGNORE_TEST(DocumentationSnippets, SplitFrame_Config)_Interrupt */
}
#endif /* EC_IOCTL_SET_SPLIT_FRAME_PROCESSING_ENABLED */
IGNORE_TEST(DocumentationSnippets, SplitFrame_JobTask)
{
    EC_T_USER_JOB_PARMS oJobParms;

    /* process cyclic frames with task id 0 */
    oJobParms.ProcessRxFramesByTaskId.dwTaskId = 0;
    dwRes = emExecJob(dwInstanceId, eUsrJob_ProcessRxFramesByTaskId, &oJobParms);

    /* process acyclic frames */
    dwRes = emExecJob(dwInstanceId, eUsrJob_ProcessAcycRxFrames, EC_NULL);

    /* myAppWorkpd(); */

    /* send cyclic frames related to task id 0 */
    oJobParms.SendCycFramesByTaskId.dwTaskId = 0;
    dwRes = emExecJob(dwInstanceId, eUsrJob_SendCycFramesByTaskId, &oJobParms);

    /* Execute some administrative jobs. No bus traffic is performed by this function */
    dwRes = emExecJob(dwInstanceId, eUsrJob_MasterTimer, EC_NULL);

    /* send queued acyclic EtherCAT frames */
    dwRes = emExecJob(dwInstanceId, eUsrJob_SendAcycFrames, EC_NULL);
    /*IGNORE_TEST(DocumentationSnippets, SplitFrame_JobTask)*/
}

} } /* namespace EcMasterTests::DocumentationSnippets */

