***
TLS
***

The Remote Access Service TLS package provides a secure communication between the server and the client.

Needed installations
********************
On both systems running the server and the client, an OpenSSL library is needed:

- On Windows you can install OpenSSL 3.6.0 from the following link: https://slproweb.com/products/Win32OpenSSL.html
- On Ubuntu/Debian-based Linux you can install the package using apt install. On other distributions the user may need to compile it himself. 


TLS integration
***************
On the server side a certificate and a private key are needed. Those are currently supported in a file format.

On the client side two options are possible:

- a root certificate in a file or buffer format for one-way-TLS (Standard TLS)
- or a certificate and a private key in file format for mutual TLS (mTLS)

Additional API description
**************************
The following server init parameters are used for TLS:

- :cpp:member:`ECMASTERRAS_T_SRVPARMS::pbyTlsCert`
- :cpp:member:`ECMASTERRAS_T_SRVPARMS::dwTlsCertSize`
- :cpp:member:`ECMASTERRAS_T_SRVPARMS::eTlsCertType`
- :cpp:member:`ECMASTERRAS_T_SRVPARMS::pbyTlsPrivKey`
- :cpp:member:`ECMASTERRAS_T_SRVPARMS::dwTlsPrivKeySize`
- :cpp:member:`ECMASTERRAS_T_SRVPARMS::eTlsPrivKeyType`

An extended connection descriptor is needed for the client initialization. It should be passed as a pointer to :cpp:member:`ECMASTERRAS_T_CLNTCONDESC::pvConHandle` 

.. doxygenstruct:: ECMASTERRAS_T_CLNTCONEX_DESC
    :members:
    
.. doxygenenum:: EC_T_TLS_CERT_TYPE

.. doxygenenum:: EC_T_TLS_PRIVKEY_TYPE
