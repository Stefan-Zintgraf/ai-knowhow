************
Introduction
************

The Python Wrapper provides a Python interface to use EC-Master, EC-Simulator and RAS Client/Server.

Requirements
************

Python v3.7 and above
  - Python Pause. Required for ticked timing with pause.until(...) to lower JobTask's drift, e.g. for Distributed Clocks

    .. prompt:: bash
    
      pip install pause

  - PyQt5 (v5.15.1). Only required to run the GUI demo

    .. prompt:: bash
    
      pip install pyqt5

Windows (x86/x64)
  - Microsoft Windows 7 and above
  - Microsoft Visual C++ 2010 Runtime

Linux (x86/x64/ARM)
    - Ubuntu 12.04 and above

Architecture
************

.. figure:: /Media/architecture.png
    :alt: Python programming interface layer model

The architecture contains 4 basic layers:

Customer Python Script or our examples (EcMasterDemoPython, …)
  - Demo application, written in Python
Programming Interface (EcWrapperPython)
  - Provides an object oriented API written in Python
Wrapper Library (EcWrapper)
  - Native wrapper library, which provides API for object oriented access
Native Libraries
  - Master Core Library
  - Simulator Library
  - RAS Client Library