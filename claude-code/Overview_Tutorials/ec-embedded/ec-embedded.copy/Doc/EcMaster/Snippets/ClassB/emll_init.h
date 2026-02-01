namespace EcMasterTests { namespace DocumentationSnippets {

IGNORE_TEST(DocumentationSnippets, Init_SockRawLinkParms)
{
    EC_T_LINK_PARMS_SOCKRAW oLinkParmsSockRaw;
    OsMemset(&oLinkParmsSockRaw, 0, sizeof(EC_T_LINK_PARMS_SOCKRAW));

    /* identify Link Layer in the common struture */
    oLinkParmsSockRaw.linkParms.dwSignature = EC_LINK_PARMS_SIGNATURE_SOCKRAW;
    oLinkParmsSockRaw.linkParms.dwSize = sizeof(EC_T_LINK_PARMS_SOCKRAW);
    OsStrncpy(&oLinkParmsSockRaw.linkParms.szDriverIdent, EC_LINK_PARMS_IDENT_SOCKRAW, EC_DRIVER_IDENT_MAXLEN);

    /* specific Link Layer parameters should be set here */

    /* pass Link Layer parameters */
    oInitMasterParms.dwSignature = ATECAT_SIGNATURE;
    oInitMasterParms.dwSize = sizeof(EC_T_INIT_MASTER_PARMS);
    oInitMasterParms.pLinkParms = &oLinkParmsSockRaw.linkParms;

    /* more parameters should be set here */

    /* initialize master */
    emInitMaster(dwInstanceId, &oInitMasterParms);
    /* IGNORE_TEST(DocumentationSnippets, Init_SockRawLinkParms) */
}

} } /* namespace EcMasterTests::DocumentationSnippets */

