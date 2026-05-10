# ##############################################################################################
# # Workspace/cmake/EcMasterDemoDc/CMakeLists.txt                                              #
# # Copyright                acontis technologies GmbH, Weingarten, Germany                    #
# # Response                 Paul Bussmann                                                     #
# # Description              EcMasterDemoDc                                                    #
# ##############################################################################################

cmake_minimum_required (VERSION 3.5)

# EcMasterDemoDc
project(EcMasterDemoDc LANGUAGES C CXX)
if (EXISTS "${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoDc")
    # LxWin
    set(ECMASTERDEMODC_SOURCES
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoDc/EcDemoApp.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoDc/EcDemoParms.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoDc/EcDemoTimingTask.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoDc/EcLogging.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoDc/EcNotification.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoDc/EcSdoServices.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoDc/EcSelectLinkLayer.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoDc/EcSlaveInfo.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoDc/EcThread.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoDc/EcTimer.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoDc/EcDemoMain.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoDc/EcDemoTimingTaskPlatform.cpp)
    set (ECMASTERDEMODC_INCLUDE_DIRS ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoDc ${EC_DEMO_OS_LAYER_INC} ${EC_TOP_LEVEL_DIR}/Examples/Common)
else()
    set(ECMASTERDEMODC_SOURCES
        ${EC_TOP_LEVEL_DIR}/Examples/EcMasterDemoDc/EcDemoApp.cpp
        ${EC_TOP_LEVEL_DIR}/Examples/Common/EcDemoParms.cpp
        ${EC_TOP_LEVEL_DIR}/Examples/Common/EcDemoTimingTask.cpp
        ${EC_TOP_LEVEL_DIR}/Examples/Common/EcLogging.cpp
        ${EC_TOP_LEVEL_DIR}/Examples/Common/EcNotification.cpp
        ${EC_TOP_LEVEL_DIR}/Examples/Common/EcSdoServices.cpp
        ${EC_TOP_LEVEL_DIR}/Examples/Common/EcSelectLinkLayer.cpp
        ${EC_TOP_LEVEL_DIR}/Examples/Common/EcSlaveInfo.cpp
        ${EC_TOP_LEVEL_DIR}/Sources/Common/EcThread.cpp
        ${EC_TOP_LEVEL_DIR}/Sources/Common/EcTimer.cpp
        ${EC_DEMO_OS_LAYER_TIMING_TASK_SOURCES}
        ${EC_DEMO_OS_LAYER_SOURCES})
    set (ECMASTERDEMODC_INCLUDE_DIRS ${EC_TOP_LEVEL_DIR}/Examples/EcMasterDemoDc ${EC_DEMO_OS_LAYER_INC} ${EC_TOP_LEVEL_DIR}/Examples/Common)
endif()
add_executable(EcMasterDemoDc ${ECMASTERDEMODC_SOURCES})
target_include_directories(EcMasterDemoDc PRIVATE ${ECMASTERDEMODC_INCLUDE_DIRS})
target_compile_definitions(EcMasterDemoDc PRIVATE INCLUDE_PCAP_RECORDER)
target_compile_definitions(EcMasterDemoDc PRIVATE INCLUDE_FRAME_MIRROR)
if (EC_OS STREQUAL Linux)
    target_link_libraries(EcMasterDemoDc -lEcMasterRasServer -lEcMaster ${LDFLAGS_APP_LIBS})
elseif (EC_OS STREQUAL LxWin)
    target_link_libraries(EcMasterDemoDc -L"${RTE_LXWIN}SDK/Lib/Linux/${EC_ARCH}" -lEcMasterRasServer -lEcMaster ${LDFLAGS_APP_LIBS})
elseif (EC_OS STREQUAL Windows)
    target_link_libraries(EcMasterDemoDc EcMasterRasServer.lib EcMaster.lib setupapi.lib winmm.lib)
endif()
if (EXISTS "${EC_TOP_LEVEL_DIR}/Workspace/cmake/EcMaster/CMakeLists.txt")
    add_dependencies(EcMasterDemoDc EcMaster)
endif()
if (EXISTS "${EC_TOP_LEVEL_DIR}/Workspace/cmake/EcMasterRasServer/CMakeLists.txt")
    add_dependencies(EcMasterDemoDc EcMasterRasServer)
endif()

# ###END OF FILE################################################################################