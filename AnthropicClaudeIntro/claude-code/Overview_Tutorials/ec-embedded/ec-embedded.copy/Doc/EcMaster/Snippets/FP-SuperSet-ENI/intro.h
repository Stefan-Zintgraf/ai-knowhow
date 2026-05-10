namespace EcMasterTests { namespace DocumentationSnippets {

IGNORE_TEST(DocumentationSnippets, SupersetENI_ConfigExcludeSlave)
{
    dwRes = emInitMaster(dwInstanceId, &oInitMasterParms);

    /* load configuration from ENI */
    dwRes = emConfigLoad(dwInstanceId, eCnfType_Filename, (EC_T_BYTE*)"eni.xml", (EC_T_DWORD)OsStrlen("eni.xml"));

    /* exclude slaves from configuration */
    dwRes = emConfigExcludeSlave(dwInstanceId, 1002);
    dwRes = emConfigExcludeSlave(dwInstanceId, 1004);

    /* apply modified configuration */
    dwRes = emConfigApply(dwInstanceId);
    /*IGNORE_TEST(DocumentationSnippets, SupersetENI_ConfigExcludeSlave)*/
}
IGNORE_TEST(DocumentationSnippets, SupersetENI_ConfigIncludeSlave)
{
    dwRes = emInitMaster(dwInstanceId, &oInitMasterParms);

    /* load configuration from ENI */
    dwRes = emConfigLoad(dwInstanceId, eCnfType_Filename, (EC_T_BYTE*)"eni.xml", (EC_T_DWORD)OsStrlen("eni.xml"));

    /* exclude all alternative slaves from configuration */
    dwRes = emConfigExcludeSlave(dwInstanceId, 9001);
    dwRes = emConfigExcludeSlave(dwInstanceId, 9002);

    /* ... */

    /* select alternative slave from configuration */
    dwRes = emConfigIncludeSlave(dwInstanceId, 9002);

    /* apply modified configuration */
    dwRes = emConfigApply(dwInstanceId);
    /*IGNORE_TEST(DocumentationSnippets, SupersetENI_ConfigIncludeSlave)*/
}

} } /* namespace EcMasterTests::DocumentationSnippets */

