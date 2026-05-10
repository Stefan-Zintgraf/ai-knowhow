# ##############################################################################################
# # Workspace/cmake/EcMasterDemoMotion/CMakeLists.txt                                          #
# # Copyright                acontis technologies GmbH, Weingarten, Germany                    #
# # Response                 Paul Bussmann                                                     #
# # Description              EcMasterDemoMotion                                                #
# ##############################################################################################

cmake_minimum_required (VERSION 3.5)

# EcMasterDemoMotion
project(EcMasterDemoMotion LANGUAGES C CXX)
add_executable(EcMasterDemoMotion
    ${EC_TOP_LEVEL_DIR}/Sources/Common/AtXmlParser.cpp
    ${EC_TOP_LEVEL_DIR}/Examples/EcMasterDemoMotion/EcDemoApp.cpp
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
target_include_directories(EcMasterDemoMotion PRIVATE ${EC_TOP_LEVEL_DIR}/Examples/EcMasterDemoMotion ${EC_DEMO_OS_LAYER_INC} ${EC_TOP_LEVEL_DIR}/Examples/Common)
target_compile_definitions(EcMasterDemoMotion PRIVATE INCLUDE_PCAP_RECORDER)
if ((EC_OS STREQUAL Linux) OR (EC_OS STREQUAL LxWin))
    target_link_libraries(EcMasterDemoMotion -L${CMAKE_ARCHIVE_OUTPUT_DIRECTORY} -L${BUILDOUTPUT}/SDK/LIB/${EC_OS}/${EC_ARCH} -L${CMAKE_LIBRARY_OUTPUT_DIRECTORY} -lEcMasterRasServer -lEcMaster -lEcMotionControl ${LDFLAGS_APP_LIBS})
elseif (EC_OS STREQUAL Windows)
    target_link_libraries(EcMasterDemoMotion EcMasterRasServer.lib EcMaster.lib EcMotionControl.lib setupapi.lib ws2_32.lib winmm.lib)
endif()
if (EXISTS "${EC_TOP_LEVEL_DIR}/Workspace/cmake/EcMaster/CMakeLists.txt")
    add_dependencies(EcMasterDemoMotion EcMaster)
endif()
if (EXISTS "${EC_TOP_LEVEL_DIR}/Workspace/cmake/EcMasterRasServer/CMakeLists.txt")
    add_dependencies(EcMasterDemoMotion EcMasterRasServer)
endif()
if (EXISTS "${EC_TOP_LEVEL_DIR}/Workspace/cmake/EcMotionControl/CMakeLists.txt")
    add_dependencies(EcMasterDemoMotion EcMotionControl)
endif()

# ###END OF FILE################################################################################
