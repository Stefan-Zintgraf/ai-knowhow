************
Introduction
************

The Rust Wrapper provides a Rust interface to use EC-Master, EC-Simulator and RAS Client/Server.

Requirements
************

Rust v1.90.0 and above
  - Download "rustup" and install Rust

Windows (x86/x64)
  - Microsoft Windows 10 and above
  - Microsoft Visual C++ 2015 Runtime

Linux (x86/x64/ARM)
    - Ubuntu 18.04 and above

Architecture
************

.. figure:: /Media/architecture.png
    :alt: Rust programming interface layer model

The architecture contains 4 basic layers:

Customer Rust application or our examples (EcMasterDemoRust, …)
  - Demo application, written in Rust
Programming Interface (EcWrapperRust)
  - Provides an object oriented API written in Rust
Wrapper Library (EcWrapper)
  - Native wrapper library, which provides API for object oriented access
Native Libraries
  - Master Core Library
  - Simulator Library
  - RAS Client Library