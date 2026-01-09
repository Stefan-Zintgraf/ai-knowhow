*********************************
|Product| Source Code
*********************************

In a source code delivery the |Product| sources are divided into 4 parts:

- SDK Header files
- Real-time Ethernet Driver files (multiple Real-time Ethernet Drivers may be shipped)
- Link OS layer files (only valid for the Real-time Ethernet Drivers)
- |Product| files (configuration, core and interface layer)
- OS layer files

The |Product| can be ported to several different operating systems and CPU architectures with different compilers and development environments. Typically no supported build environment files like IDE projects are shipped with the source code.

To build the |Product| the appropriate build environment for the target operating system has to be used. If an integrated development environment (IDE) exists (Visual Studio, Eclipse, etc.) several projects containing all necessary files are needed to build the artefacts. If no integrated development environment is available makefiles and dependency rules may have to be created which contain the necessary |Product| source and header files.

For most platforms three separate independent binaries will have to be generated:

#. Real-time Ethernet Driver Binary. The Real-time Ethernet Driver binary will be dynamically bound to the application at runtime.
#. |Product| Library
#. Remote API Server Library

Real-time Ethernet Driver Binaries
==================================

The following files have to be included into an IDE project or makefile:

- Real-time Ethernet Driver files. Only one single Real-time Ethernet Driver must be selected even if multiple Real-time Ethernet Driver are shipped. For each Real-time Ethernet Driver a separate binary has to be created.
- Link OS layer files
- Windows: a dynamic link library (.dll) has to be created. The name of the DLL has to be emllXxxx.dll where Xxxx shall be replaced by the Link Layer type (e.g. emllI8255x.dll for the I8255x Link Layer).

|Product| Binaries
=====================

The following files have to be included into an IDE project or makefile:

- |Product| files
- OS layer files
- For all platforms a static library has to be created. This library will have to be linked together with the application.

Remote API Server Binaries: 
===========================

The following files have to be included into an IDE project or makefile:

- Remote API server files.
- For all platforms a static library has to be created. This library will have to be linked together with the application.

.. seealso:: :ref:`os:Platform and Operating Systems (OS)` for required tool chain settings
