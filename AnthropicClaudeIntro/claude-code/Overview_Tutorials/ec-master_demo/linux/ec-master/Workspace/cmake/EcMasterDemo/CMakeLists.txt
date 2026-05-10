# ##############################################################################################
# # Workspace/cmake/EcMasterDemo/CMakeLists.txt                                                #
# # Copyright                acontis technologies GmbH, Weingarten, Germany                    #
# # Response                 Paul Bussmann                                                     #
# # Description              EcMasterDemo                                                      #
# ##############################################################################################

cmake_minimum_required (VERSION 3.5)

# EcMasterDemo
project(EcMasterDemo LANGUAGES C CXX)
if (EXISTS "${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemo")
    # LxWin
    set (ECMASTERDEMO_SOURCES
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemo/EcDemoApp.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemo/EcDemoParms.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemo/EcDemoTimingTask.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemo/EcLogging.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemo/EcNotification.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemo/EcSdoServices.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemo/EcSelectLinkLayer.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemo/EcSlaveInfo.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemo/EcThread.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemo/EcTimer.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemo/EcDemoMain.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemo/EcDemoTimingTaskPlatform.cpp)
    set (ECMASTERDEMO_INCLUDE_DIRS ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemo ${EC_DEMO_OS_LAYER_INC} ${EC_TOP_LEVEL_DIR}/Examples/Common)
else()
    set (ECMASTERDEMO_SOURCES 
        ${EC_TOP_LEVEL_DIR}/Examples/EcMasterDemo/EcDemoApp.cpp
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
    set (ECMASTERDEMO_INCLUDE_DIRS ${EC_TOP_LEVEL_DIR}/Examples/EcMasterDemo ${EC_DEMO_OS_LAYER_INC} ${EC_TOP_LEVEL_DIR}/Examples/Common)
endif()
add_executable(EcMasterDemo ${ECMASTERDEMO_SOURCES})
target_include_directories(EcMasterDemo PRIVATE ${ECMASTERDEMO_INCLUDE_DIRS})
target_compile_definitions(EcMasterDemo PRIVATE INCLUDE_PCAP_RECORDER)
target_compile_definitions(EcMasterDemo PRIVATE INCLUDE_FRAME_MIRROR)
if (EC_OS STREQUAL Linux)
    target_link_libraries(EcMasterDemo -lEcMasterRasServer -lEcMaster ${LDFLAGS_APP_LIBS})
elseif (EC_OS STREQUAL LxWin)
    target_link_libraries(EcMasterDemo -L"${RTE_LXWIN}SDK/Lib/Linux/${EC_ARCH}" -lEcMasterRasServer -lEcMaster ${LDFLAGS_APP_LIBS})
elseif (EC_OS STREQUAL Windows)
    target_link_libraries(EcMasterDemo EcMasterRasServer.lib EcMaster.lib setupapi.lib ws2_32.lib winmm.lib)
endif()
if (EXISTS "${EC_TOP_LEVEL_DIR}/Workspace/cmake/EcMaster/CMakeLists.txt")
    add_dependencies(EcMasterDemo EcMaster)
endif()
if (EXISTS "${EC_TOP_LEVEL_DIR}/Workspace/cmake/EcMasterRasServer/CMakeLists.txt")
    add_dependencies(EcMasterDemo EcMasterRasServer)
endif()

# ###END OF FILE################################################################################
