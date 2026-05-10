# ##############################################################################################
# # Workspace/Linux/CMakeLists.txt                                                             #
# # Copyright                acontis technologies GmbH, Weingarten, Germany                    #
# # Response                 Paul Bussmann                                                     #
# # Description              Linux settings                                                    #
# ##############################################################################################

cmake_minimum_required (VERSION 3.5)

set(EC_OS_LAYER_INC_NAME Linux CACHE STRING "" FORCE)
set(EC_OS_LAYER_SOURCES                  ${EC_TOP_LEVEL_DIR}/Sources/OsLayer/Linux/EcOs.cpp CACHE STRING "" FORCE)
set(EC_LINK_OS_LAYER_INC                 ${EC_TOP_LEVEL_DIR}/Sources/LinkOsLayer/Linux/atemsys ${EC_TOP_LEVEL_DIR}/Sources/LinkOsLayer/Linux CACHE STRING "" FORCE)
set(EC_LINK_OS_LAYER_SOURCES             ${EC_TOP_LEVEL_DIR}/Sources/LinkOsLayer/Linux/LinkOsLayer.cpp CACHE STRING "" FORCE)
set(EC_DEMO_OS_LAYER_INC                 ${EC_TOP_LEVEL_DIR}/Examples/Common/Linux CACHE STRING "" FORCE)
set(EC_DEMO_OS_LAYER_TIMING_TASK_SOURCES ${EC_TOP_LEVEL_DIR}/Examples/Common/Linux/EcDemoTimingTaskPlatform.cpp CACHE STRING "" FORCE)
set(EC_DEMO_OS_LAYER_SOURCES             ${EC_TOP_LEVEL_DIR}/Examples/Common/Linux/EcDemoMain.cpp CACHE STRING "" FORCE)
set(EC_EOETAP_OS_LAYER_INC               ${EC_TOP_LEVEL_DIR}/Sources/NetworkDrv/EoE/LinuxTAP CACHE STRING "" FORCE)

if (EC_ARCH STREQUAL aarch64)
    set(CMAKE_C_FLAGS_ARCH "-fPIC -Wno-psabi -Wno-packed-not-aligned -Wno-stringop-truncation -Wno-address-of-packed-member" CACHE STRING "" FORCE)
elseif (EC_ARCH STREQUAL armv4t-eabi)
    set(CMAKE_C_FLAGS_ARCH "-fPIC -Wno-psabi" CACHE STRING "" FORCE)
elseif (EC_ARCH STREQUAL armv6-vfp-eabihf)
    set(CMAKE_C_FLAGS_ARCH "-fPIC -Wno-psabi" CACHE STRING "" FORCE)
elseif (EC_ARCH STREQUAL armv7-vfp-eabihf)
    set(CMAKE_C_FLAGS_ARCH "-fPIC -Wno-psabi" CACHE STRING "" FORCE)
elseif (EC_ARCH STREQUAL PPC)
    set(CMAKE_C_FLAGS_ARCH "-fPIC -te500v2" CACHE STRING "" FORCE)
elseif (EC_ARCH STREQUAL powerpc)
    set(CMAKE_C_FLAGS_ARCH "-fPIC -DTEST_WITH_LOW_PERFORMANCE" CACHE STRING "" FORCE)
elseif (EC_ARCH STREQUAL riscv64)
    set(CMAKE_C_FLAGS_ARCH "-fPIC -Wno-packed-not-aligned -Wno-address-of-packed-member -Wno-stringop-truncation -Wno-stringop-overflow" CACHE STRING "" FORCE)
elseif (EC_ARCH STREQUAL x64)
    set(CMAKE_C_FLAGS_ARCH "-fPIC -Wno-packed-not-aligned -Wno-stringop-truncation -Wno-address-of-packed-member" CACHE STRING "" FORCE)
elseif (EC_ARCH STREQUAL x86)
    set(CMAKE_C_FLAGS_ARCH "-fPIC" CACHE STRING "" FORCE)
endif()
set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS} ${CMAKE_C_FLAGS_ARCH} -g -O0 -DDEBUG -fmessage-length=0 -fno-strict-aliasing -Wall -Werror" CACHE STRING "" FORCE)
set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS} ${CMAKE_C_FLAGS_ARCH} -O2 -fmessage-length=0 -fno-strict-aliasing -Wall -Werror" CACHE STRING "" FORCE)
set(CMAKE_C_FLAGS_PROTECTED "${CMAKE_C_FLAGS} ${CMAKE_C_FLAGS_ARCH} -O2 -DPROTECTED_VERSION -fmessage-length=0 -fno-strict-aliasing -Wall -Werror" CACHE STRING "" FORCE)
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS} ${CMAKE_C_FLAGS_ARCH} -g -O0 -DDEBUG -fmessage-length=0 -fno-strict-aliasing -Wall -Werror" CACHE STRING "" FORCE)
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS} ${CMAKE_C_FLAGS_ARCH} -O2 -fmessage-length=0 -fno-strict-aliasing -Wall -Werror" CACHE STRING "" FORCE)
set(CMAKE_CXX_FLAGS_PROTECTED "${CMAKE_CXX_FLAGS} ${CMAKE_C_FLAGS_ARCH} -O2 -DPROTECTED_VERSION -fmessage-length=0 -fno-strict-aliasing -Wall -Werror" CACHE STRING "" FORCE)

if (EC_OS STREQUAL Linux)
    set(LDFLAGS_APP_LIBS "-L${BUILDOUTPUT}/Bin/${EC_OS}/${EC_ARCH}/${CMAKE_BUILD_TYPE} -L${BUILDOUTPUT}/Bin/${EC_OS}/${EC_ARCH} -L${BUILDOUTPUT}/SDK/LIB/${EC_OS}/${EC_ARCH}/${CMAKE_BUILD_TYPE} -L${BUILDOUTPUT}/SDK/LIB/${EC_OS}/${EC_ARCH} -ldl -lrt -lpthread" CACHE STRING "" FORCE)
    set(LDFLAGS_SO_LIBS "-L${BUILDOUTPUT}/Bin/${EC_OS}/${EC_ARCH}/${CMAKE_BUILD_TYPE} -L${BUILDOUTPUT}/Bin/${EC_OS}/${EC_ARCH} -L${BUILDOUTPUT}/SDK/LIB/${EC_OS}/${EC_ARCH}/${CMAKE_BUILD_TYPE} -L${BUILDOUTPUT}/SDK/LIB/${EC_OS}/${EC_ARCH} -ldl -lrt -lpthread" CACHE STRING "" FORCE)
elseif (EC_OS STREQUAL LxWin)
	if (EXISTS ${EC_TOP_LEVEL_DIR}/SDK/Examples)
		# EC-WinRT-Linux
		set(LDFLAGS_APP_LIBS "-L${BUILDOUTPUT}/Bin/Linux/${EC_ARCH}/${CMAKE_BUILD_TYPE} -L${BUILDOUTPUT}/Bin/Linux/${EC_ARCH} -L${BUILDOUTPUT}/SDK/LIB/Linux/${EC_ARCH}/${CMAKE_BUILD_TYPE} -L${BUILDOUTPUT}/SDK/LIB/Linux/${EC_ARCH} -lrtos -ldl -lrt -lpthread" CACHE STRING "" FORCE)
		set(LDFLAGS_SO_LIBS "-L${BUILDOUTPUT}/Bin/Linux/${EC_ARCH}/${CMAKE_BUILD_TYPE} -L${BUILDOUTPUT}/Bin/Linux/${EC_ARCH} -L${BUILDOUTPUT}/SDK/LIB/Linux/${EC_ARCH}/${CMAKE_BUILD_TYPE} -L${BUILDOUTPUT}/SDK/LIB/Linux/${EC_ARCH} -lrtos -ldl -lrt -lpthread" CACHE STRING "" FORCE)
	else()
		set(LDFLAGS_APP_LIBS "-L${BUILDOUTPUT}/Bin/${EC_OS}/${EC_ARCH}/${CMAKE_BUILD_TYPE} -L${BUILDOUTPUT}/Bin/${EC_OS}/${EC_ARCH} -L${BUILDOUTPUT}/SDK/LIB/${EC_OS}/${EC_ARCH}/${CMAKE_BUILD_TYPE} -L${BUILDOUTPUT}/SDK/LIB/${EC_OS}/${EC_ARCH} -lrtos -ldl -lrt -lpthread" CACHE STRING "" FORCE)
		set(LDFLAGS_SO_LIBS "-L${BUILDOUTPUT}/Bin/${EC_OS}/${EC_ARCH}/${CMAKE_BUILD_TYPE} -L${BUILDOUTPUT}/Bin/${EC_OS}/${EC_ARCH} -L${BUILDOUTPUT}/SDK/LIB/${EC_OS}/${EC_ARCH}/${CMAKE_BUILD_TYPE} -L${BUILDOUTPUT}/SDK/LIB/${EC_OS}/${EC_ARCH} -lrtos -ldl -lrt -lpthread" CACHE STRING "" FORCE)
	endif()
endif()

# ###END OF FILE################################################################################
