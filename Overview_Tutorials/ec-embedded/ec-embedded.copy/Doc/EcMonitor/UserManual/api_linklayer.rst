*******************************************
Real-time Ethernet Driver Control Interface
*******************************************

emonIoControl - EC_IOCTL_ISLINK_CONNECTED
*****************************************

.. emonIoControl:: EC_IOCTL_ISLINK_CONNECTED
    :pbyOutBuf: Pointer to buffer of type struct EC_T_LINK_CONNECTED_INFO
    :dwOutBufSize: Size of the output buffer in bytes, sizeof(EC_T_LINK_CONNECTED_INFO)
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer

.. doxygenstruct:: EC_T_LINK_CONNECTED_INFO
    :members:

emonIoControl - EC_IOCTL_GET_LINKLAYER_MODE
*******************************************

.. emonIoControl:: EC_IOCTL_GET_LINKLAYER_MODE
    :pbyOutBuf: Pointer to buffer of type struct EC_T_LINKLAYER_MODE_DESC
    :dwOutBufSize: Size of the output buffer in bytes, sizeof(EC_T_LINKLAYER_MODE_DESC)
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer

.. doxygenstruct:: EC_T_LINKLAYER_MODE_DESC
    :members:

emonIoControl - EC_LINKIOCTL...
*******************************

The generic control interface provides access to the main network adapter when adding :c:macro:`EC_IOCTL_LINKLAYER_MAIN` to the :c:macro:`EC_LINKIOCTL` parameter at dwCode.

.. code-block:: cpp

    EC_T_DWORD dwCode = (EC_IOCTL_LINKLAYER_MAIN | EC_LINKIOCTL_GET_ETHERNET_ADDRESS);

emonIoControl - EC_LINKIOCTL_GET_ETHERNET_ADDRESS
*************************************************

Provides MAC addresses of main or red line.

.. emonIoControl:: EC_LINKIOCTL_GET_ETHERNET_ADDRESS
    :pbyOutBuf: Pointer to MAC address buffer (6 bytes). 
    :dwOutBufSize: Size of the output buffer in bytes (at least 6).
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer.
    
emonIoControl - EC_LINKIOCTL_GET_SPEED
**************************************

.. emonIoControl:: EC_LINKIOCTL_GET_SPEED
    :pbyOutBuf: Pointer to EC_T_DWORD. Set by Real-time Ethernet Driver to 10/100/1000.
    :dwOutBufSize: Size of the output buffer in bytes.
    :pdwNumOutData: Pointer to EC_T_DWORD. Amount of bytes written to the output buffer.