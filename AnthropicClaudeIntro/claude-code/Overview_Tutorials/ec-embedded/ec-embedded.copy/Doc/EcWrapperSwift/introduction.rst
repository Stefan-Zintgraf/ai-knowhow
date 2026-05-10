************
Introduction
************

The Swift Wrapper provides a Swift interface to use EC-Master, EC-Simulator and RAS Client/Server.

Requirements
************

Swift v5.9 and above

MacOS (ARM64)
    - macOS Ventura 13.5 and above

Windows (x86/x64)
  - Microsoft Windows 10 and above
  - Microsoft Visual C++ 2015 Runtime

Linux (x86/x64/ARM)
    - Ubuntu 20.04 and above

Architecture
************

.. figure:: /Media/architecture.png
    :alt: Swift programming interface layer model

The architecture contains 4 basic layers:

Customer Swift Application or our examples (EcMasterDemoSwift, …)
  - Demo application, written in Swift
Programming Interface (EcWrapperSwift)
  - Provides an object oriented API written in Swift
Wrapper Library (EcWrapper)
  - Native wrapper library, which provides API for object oriented access
Native Libraries
  - Master Core Library
  - Simulator Library
  - RAS Client Library