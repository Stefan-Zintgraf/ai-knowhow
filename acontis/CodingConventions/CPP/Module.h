/*-----------------------------------------------------------------------------
 * EcDeviceDummy.h      header file
 * Copyright            acontis technologies GmbH, Ravensburg, Germany
 * Description          Internal used types and structures for I8255x
 *                      Ethercat LinkLayer
 *---------------------------------------------------------------------------*/

#ifndef INC_ECDEVICEDUMMY_H
#define INC_ECDEVICEDUMMY_H

/*-INCLUDE-------------------------------------------------------------------*/
#include "LinkOsLayer.h" /* First include in link layer source code */
#include "EcLinkDummy.h"

/*-DEFINES-------------------------------------------------------------------*/

/*-TYPEDEFS/ENUMS------------------------------------------------------------*/
typedef struct _T_DUMMY_INTERNAL
{
    EC_T_DWORD                  dwSignature;
    EC_T_LINK_PARMS_DUMMY       oInitParms;
    EC_T_RECEIVEFRAMECALLBACK   pfReceiveFrameCallback;

    EC_T_VOID*                  pvCallbackContext;
    EC_T_VOID*                  pvLinkOsContext;

    
    /* Address spaces */
    EC_T_DWORD                  dwMemRegisterBase;
    
    EC_T_DWORD                  dwDMASize;
    EC_T_DWORD                  dwDMAVirtAddr;					/* cached */
	EC_T_DWORD                  dwDMAVirtAddrUncached;			/* uncached */
    EC_T_DWORD                  dwDMAPhysAddr;

    EC_T_DWORD                  dwDMAOffset;

    /* IRQ handling */
    EC_T_LINKOS_IRQ_PARM        oIrqParms;

    /* Multicast entry counter */
    EC_T_DWORD                  dwActiveMulticastEntries;

    EC_T_BYTE*                  pbyIntBuffer;
    EC_T_DWORD                  dwFrameLen;
    EC_T_BOOL                   bNewData;
    
    struct _T_DUMMY_INTERNAL*  pPrev;
    struct _T_DUMMY_INTERNAL*  pNext;
} T_DUMMY_INTERNAL, *PT_DUMMY_INTERNAL;

#endif /* INC_ECDEVICEDUMMY_H */

/*-END OF SOURCE FILE--------------------------------------------------------*/

