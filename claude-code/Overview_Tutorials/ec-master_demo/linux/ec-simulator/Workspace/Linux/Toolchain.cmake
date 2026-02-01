# ##############################################################################################
# # Workspace/Linux/Toolchain.cmake                                                            #
# # Copyright                acontis technologies GmbH, Weingarten, Germany                    #
# # Response                 Paul Bussmann                                                     #
# # Description              Linux cross compilation toolchain settings (optional)             #
# ##############################################################################################
# Example usage to cross compile for Linux x64 Debug on Windows with cmake and ninja:
# Workspace\Linux\x64\Debug> cmake.exe -G Ninja ..\..\..\.. -DCMAKE_TOOLCHAIN_FILE=..\..\..\Toolchain.cmake -DEC_OS=Linux -DEC_ARCH=x64 -DCMAKE_BUILD_TYPE=Debug
# Workspace\Linux\x64\Debug> ninja.exe
# ##############################################################################################
# Example usage to cross compile for LxWin x64 Debug on Windows with cmake and ninja:
# Workspace\LxWin\x64\Debug> cmake.exe -G Ninja ..\..\..\.. -DCMAKE_TOOLCHAIN_FILE=..\..\..\..\Linux\Toolchain.cmake -DEC_OS=LxWin -DEC_ARCH=x64 -DCMAKE_BUILD_TYPE=Debug
# Workspace\LxWin\x64\Debug> ninja.exe
# ##############################################################################################

cmake_minimum_required (VERSION 3.5)

# ##############################################################################################
# work-around cmake bug in passing parameters (environment variables are always preserved)
if (EC_OS)
    set(ENV{_EC_OS} "${EC_OS}")
else ()
    set(EC_OS "$ENV{_EC_OS}")
endif ()
if (EC_ARCH)
    set(ENV{_EC_ARCH} "${EC_ARCH}")
else ()
    set(EC_ARCH "$ENV{_EC_ARCH}")
endif ()

# ##############################################################################################
# check parameters
if (NOT DEFINED EC_OS)
  message(FATAL_ERROR "EC_OS not set!")
endif()
if (NOT DEFINED EC_ARCH)
  message(FATAL_ERROR "EC_ARCH not set!")
endif()

# ##############################################################################################
# Linux settings
set(CMAKE_SYSTEM_NAME Linux)

# Linux / LxWin
if (EC_OS STREQUAL Linux)
    # aarch64
    if (EC_ARCH STREQUAL aarch64)
        set(CMAKE_SYSTEM_PROCESSOR arm)
        set(DPDK_SDK_DIRECTORY_ARCH "C:/dpdk-23.11/Linux/${EC_ARCH}" CACHE STRING "" FORCE)
        set(CMAKE_C_COMPILER C:/MinGW/opt/gcc-linaro-7.3.1-2018.05-i686-mingw32_aarch64-linux-gnu/bin/aarch64-linux-gnu-gcc.exe)
        set(CMAKE_CXX_COMPILER C:/MinGW/opt/gcc-linaro-7.3.1-2018.05-i686-mingw32_aarch64-linux-gnu/bin/aarch64-linux-gnu-g++.exe)
        set(CMAKE_C_FLAGS "-IC:/MinGW/opt/gcc-linaro-7.3.1-2018.05-i686-mingw32_aarch64-linux-gnu/aarch64-linux-gnu/libc/usr/include" CACHE STRING "" FORCE)
        set(CMAKE_CXX_FLAGS "-IC:/MinGW/opt/gcc-linaro-7.3.1-2018.05-i686-mingw32_aarch64-linux-gnu/aarch64-linux-gnu/libc/usr/include" CACHE STRING "" FORCE)

    # armv4t-eabi
    elseif (EC_ARCH STREQUAL armv4t-eabi)
        set(CMAKE_SYSTEM_PROCESSOR arm)
        set(CMAKE_C_COMPILER C:/MinGW/opt/Debian-Wheezy-armv4t-linux-gnueabi-SDK/bin/arm-unknown-linux-gnueabi-gcc.exe)
        set(CMAKE_CXX_COMPILER C:/MinGW/opt/Debian-Wheezy-armv4t-linux-gnueabi-SDK/bin/arm-unknown-linux-gnueabi-g++.exe)

    # armv6-vfp-eabihf
    elseif (EC_ARCH STREQUAL armv6-vfp-eabihf)
        set(CMAKE_SYSTEM_PROCESSOR arm)
        set(CMAKE_C_COMPILER C:/MinGW/opt/Debian-Wheezy-armv6-rpi-linux-gnueabi-SDK/bin/armv6-rpi-linux-gnueabi-gcc.exe)
        set(CMAKE_CXX_COMPILER C:/MinGW/opt/Debian-Wheezy-armv6-rpi-linux-gnueabi-SDK/bin/armv6-rpi-linux-gnueabi-g++.exe)

    # armv7-vfp-eabihf
    elseif (EC_ARCH STREQUAL armv7-vfp-eabihf)
        set(CMAKE_SYSTEM_PROCESSOR arm)
        set(CMAKE_C_COMPILER C:/MinGW/opt/gcc-linaro-5.5.0-2017.10-i686-mingw32_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-gcc.exe)
        set(CMAKE_CXX_COMPILER C:/MinGW/opt/gcc-linaro-5.5.0-2017.10-i686-mingw32_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-g++.exe)

    # PPC
    elseif (EC_ARCH STREQUAL PPC)
        set(CMAKE_SYSTEM_PROCESSOR powerpc)
        set(CMAKE_C_COMPILER C:/MinGW/opt/freescale-2011.03/bin/powerpc-linux-gnu-gcc.exe)
        set(CMAKE_CXX_COMPILER C:/MinGW/opt/freescale-2011.03/bin/powerpc-linux-gnu-g++.exe)
        set(CMAKE_C_FLAGS "-te500v2 -D_ARCH_PPC" CACHE STRING "" FORCE)
        set(CMAKE_CXX_FLAGS "-te500v2 -D_ARCH_PPC" CACHE STRING "" FORCE)
        set(CMAKE_MODULE_LINKER_FLAGS "-te500v2" CACHE STRING "" FORCE)

    # x64
    elseif (EC_ARCH STREQUAL x64)
        set(DPDK_SDK_DIRECTORY_ARCH "C:/dpdk-23.11/Linux/${EC_ARCH}" CACHE STRING "" FORCE)
        set(CMAKE_SYSTEM_PROCESSOR x86_64)
        set(CMAKE_C_COMPILER C:/MinGW/opt/Debian-Wheezy-x86_64-pc-linux-gnu-SDK/bin/x86_64-pc-linux-gnu-gcc.exe)
        set(CMAKE_CXX_COMPILER C:/MinGW/opt/Debian-Wheezy-x86_64-pc-linux-gnu-SDK/bin/x86_64-pc-linux-gnu-g++.exe)
            
    # x86
    elseif (EC_ARCH STREQUAL x86)
        set(CMAKE_SYSTEM_PROCESSOR i686)
        set(CMAKE_C_COMPILER C:/MinGW/opt/Debian-Wheezy-i686-pc-linux-gnu-SDK/bin/i686-pc-linux-gnu-gcc.exe)
        set(CMAKE_CXX_COMPILER C:/MinGW/opt/Debian-Wheezy-i686-pc-linux-gnu-SDK/bin/i686-pc-linux-gnu-g++.exe)
    endif()

    # DPDK
    if (DEFINED DPDK_SDK_DIRECTORY_ARCH)
        set(CMAKE_INCLUDE_DIRECTORIES_ARCH ${DPDK_SDK_DIRECTORY_ARCH}/include ${CMAKE_INCLUDE_DIRECTORIES_ARCH})
        set(CMAKE_LINK_DIRECTORIES_ARCH ${DPDK_SDK_DIRECTORY_ARCH}/lib ${CMAKE_LINK_DIRECTORIES_ARCH})
    endif()

elseif (EC_OS STREQUAL LxWin)
    # x64
    if (EC_ARCH STREQUAL x64)
        set(CMAKE_SYSTEM_PROCESSOR x86_64)
        # available at http://software.acontis.com/LxWin/MinGw64.zip
        if (EXISTS "C:/MinGw64/bin/x86_64-pc-linux-gnu-g++.exe")
            set(CMAKE_C_COMPILER C:/MinGw64/bin/x86_64-pc-linux-gnu-gcc.exe)
            set(CMAKE_CXX_COMPILER C:/MinGw64/bin/x86_64-pc-linux-gnu-g++.exe)
        endif()
        
    # x86
    elseif (EC_ARCH STREQUAL x86)
        set(CMAKE_SYSTEM_PROCESSOR i686)
        # available at http://software.acontis.com/LxWin/MinGW.zip
        if (EXISTS "C:/MinGw/bin/i686-pc-linux-gnu-g++.exe")
            set(CMAKE_C_COMPILER C:/MinGw/bin/i686-pc-linux-gnu-gcc.exe)
            set(CMAKE_CXX_COMPILER C:/MinGw/bin/i686-pc-linux-gnu-g++.exe)
        endif()
    endif()

    set(CMAKE_C_FLAGS "-DLXWIN -Wrestrict" CACHE STRING "" FORCE)
    set(CMAKE_CXX_FLAGS "-DLXWIN -Wrestrict" CACHE STRING "" FORCE)
    set(CMAKE_MODULE_LINKER_FLAGS "-lrtos" CACHE STRING "" FORCE)
endif()

# ##############################################################################################
# check settings
if (NOT DEFINED CMAKE_CXX_COMPILER)
  message(FATAL_ERROR "CMAKE_CXX_COMPILER not set!")
endif()

# ###END OF FILE################################################################################
