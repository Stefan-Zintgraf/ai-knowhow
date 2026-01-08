# ##############################################################################################
# # Workspace/cmake/EcMasterDemoMinimal/CMakeLists.txt                                         #
# # Copyright                acontis technologies GmbH, Weingarten, Germany                    #
# # Response                 Paul Bussmann                                                     #
# # Description              EcMasterDemoMinimal                                               #
# ##############################################################################################

cmake_minimum_required (VERSION 3.5)

# EcMasterDemoMinimal
project(EcMasterDemoMinimal LANGUAGES C CXX)
if (EXISTS "${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoMinimal")
    # LxWin
    set (ECMASTERDEMOMINIMAL_SOURCES 
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoMinimal/EcDemoApp.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoMinimal/EcDemoParms.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoMinimal/EcSelectLinkLayer.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoMinimal/EcDemoMain.cpp
        ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoMinimal/EcDemoTimingTaskPlatform.cpp)
    set (ECMASTERDEMOMINIMAL_INCLUDE_DIRS ${EC_TOP_LEVEL_DIR}/SDK/Examples/Linux/EcMasterDemoMinimal ${EC_DEMO_OS_LAYER_INC} ${EC_TOP_LEVEL_DIR}/Examples/Common)
else()
    set (ECMASTERDEMOMINIMAL_SOURCES 
        ${EC_TOP_LEVEL_DIR}/Examples/EcMasterDemoMinimal/EcDemoApp.cpp
        ${EC_TOP_LEVEL_DIR}/Examples/Common/EcDemoParms.cpp
        ${EC_TOP_LEVEL_DIR}/Examples/Common/EcDemoTimingTask.cpp
        ${EC_TOP_LEVEL_DIR}/Examples/Common/EcSelectLinkLayer.cpp
        ${EC_DEMO_OS_LAYER_TIMING_TASK_SOURCES}
        ${EC_DEMO_OS_LAYER_SOURCES})
    set (ECMASTERDEMOMINIMAL_INCLUDE_DIRS ${EC_TOP_LEVEL_DIR}/Examples/EcMasterDemoMinimal ${EC_DEMO_OS_LAYER_INC} ${EC_TOP_LEVEL_DIR}/Examples/Common)
endif()
add_executable(EcMasterDemoMinimal ${ECMASTERDEMOMINIMAL_SOURCES})
target_include_directories(EcMasterDemoMinimal PRIVATE ${ECMASTERDEMOMINIMAL_INCLUDE_DIRS})
if (EC_OS STREQUAL Linux)
    target_link_libraries(EcMasterDemoMinimal -lEcMaster ${LDFLAGS_APP_LIBS})
elseif (EC_OS STREQUAL LxWin)
    target_link_libraries(EcMasterDemoMinimal -L"${RTE_LXWIN}SDK/Lib/Linux/${EC_ARCH}" -lEcMaster ${LDFLAGS_APP_LIBS})
elseif (EC_OS STREQUAL Windows)
    target_link_libraries(EcMasterDemoMinimal EcMaster.lib setupapi.lib ws2_32.lib winmm.lib)
endif()
if (EXISTS "${EC_TOP_LEVEL_DIR}/Workspace/cmake/EcMaster/CMakeLists.txt")
    add_dependencies(EcMasterDemoMinimal EcMaster)
endif()

# ###END OF FILE################################################################################