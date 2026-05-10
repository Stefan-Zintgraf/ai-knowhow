************
New Features
************

V3.2 
****

- Update to expat V2.4.9 
- Refactor DCM interface; timing can now be handled by user provided callbacks (Example implementations provided, see also chapter Migration from V3.1) 
- Check EEPROM access of each new slave separately during ScanBus 
- Add support for TTS for Intel®  i210 and i211 
- Add emllMultiplier supporting CU2508 

V3.1
****

-  New delivery model:

   - Setup.exe only for Windows Delivery
   - ARM_32Bit, ARM_64Bit, x86_32Bit x86_64Bit, PPC_32BIT in the ZIP file name
   - AddOns deliveries are OS/Architecture specific
-  Simplified Examples:

   - Each OS has a own EcDemoMain.cpp, operating system related #ifdef
   - Common files moved to […]\\Examples\\Common
-  Reinforcement of Master Redundancy
-  Add NDIS link layer
-  Support CMSIS-RTOS (STM32)
-  Support EC-Simulator
-  Support Linux PHY driver (ePHY_OSDRIVER)
-  Support LxWin
-  Support Python programming interface
-  Support QNX7-ARM_64Bit
-  Support QNX7.1
-  Support R-IN32M4-CL3
-  Support RTX64 4.0
-  Support VxWorks70 SR6xx
-  Support Zephyr OS

V3.0
****

-  Master Redundancy
-  Split Frame Processing
-  Junction redundancy supported together with DC
-  Support revision checks with operator >=
-  Slave to slave mailbox communication
-  Hidden slave detection by junction redundancy