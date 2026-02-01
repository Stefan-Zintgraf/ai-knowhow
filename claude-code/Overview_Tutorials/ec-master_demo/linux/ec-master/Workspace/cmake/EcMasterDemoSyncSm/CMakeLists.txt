# ##############################################################################################
# # Workspace/cmake/EcMasterDemoSyncSm/CMakeLists.txt                                          #
# # Copyright                acontis technologies GmbH, Weingarten, Germany                    #
# # Response                 Paul Bussmann                                                     #
# # Description              EcMasterDemoSyncSm                                                #
# ##############################################################################################

cmake_minimum_required (VERSION 3.5)

# EcMasterDemoSyncSm
project(EcMasterDemoSyncSm LANGUAGES C CXX)
if (EXISTS "${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoSyncSm")
    # LxWin
    set(ECMASTERDEMOSYNCSM_SOURCES
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoSyncSm/EcDemoApp.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoSyncSm/EcDemoParms.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoSyncSm/EcDemoTimingTask.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoSyncSm/EcLogging.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoSyncSm/EcNotification.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoSyncSm/EcSdoServices.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoSyncSm/EcSelectLinkLayer.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoSyncSm/EcSlaveInfo.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoSyncSm/EcThread.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoSyncSm/EcTimer.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoSyncSm/EcDemoMain.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoSyncSm/EcDemoTimingTaskPlatform.cpp)
    set (ECMASTERDEMOSYNCSM_INCLUDE_DIRS ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoSyncSm ${EC_DEMO_OS_LAYER_INC} ${EC_TOP_LEVEL_DIR}/Examples/Common)
else()
    set(ECMASTERDEMOSYNCSM_SOURCES
        ${EC_TOP_LEVEL_DIR}/Examples/EcMasterDemoSyncSm/EcDemoApp.cpp
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
    set (ECMASTERDEMOSYNCSM_INCLUDE_DIRS ${EC_TOP_LEVEL_DIR}/Examples/EcMasterDemoSyncSm ${EC_DEMO_OS_LAYER_INC} ${EC_TOP_LEVEL_DIR}/Examples/Common)
endif()
add_executable(EcMasterDemoSyncSm ${ECMASTERDEMOSYNCSM_SOURCES})
target_include_directories(EcMasterDemoSyncSm PRIVATE ${ECMASTERDEMOSYNCSM_INCLUDE_DIRS})
target_compile_definitions(EcMasterDemoSyncSm PRIVATE INCLUDE_PCAP_RECORDER)
if (EC_OS STREQUAL Linux)
    target_link_libraries(EcMasterDemoSyncSm -lEcMasterRasServer -lEcMaster ${LDFLAGS_APP_LIBS})
elseif (EC_OS STREQUAL LxWin)
    target_link_libraries(EcMasterDemoSyncSm -L"${RTE_LXWIN}SDK/Lib/Linux/${EC_ARCH}" -lEcMasterRasServer -lEcMaster ${LDFLAGS_APP_LIBS})
elseif (EC_OS STREQUAL Windows)
    target_link_libraries(EcMasterDemoSyncSm EcMasterRasServer.lib EcMaster.lib setupapi.lib ws2_32.lib winmm.lib)
endif()
if (EXISTS "${EC_TOP_LEVEL_DIR}/Workspace/cmake/EcMaster/CMakeLists.txt")
    add_dependencies(EcMasterDemoSyncSm EcMaster)
endif()
if (EXISTS "${EC_TOP_LEVEL_DIR}/Workspace/cmake/EcMasterRasServer/CMakeLists.txt")
    add_dependencies(EcMasterDemoSyncSm EcMasterRasServer)
endif()

# ###END OF FILE################################################################################
