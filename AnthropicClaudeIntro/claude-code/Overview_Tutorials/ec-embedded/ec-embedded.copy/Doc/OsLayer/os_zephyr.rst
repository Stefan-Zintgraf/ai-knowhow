..
    ******
    Zephyr
    ******

Setting up and running EcMasterDemo
***********************************

#. Prerequisites
    - Up Squared board
    - Docker

#. Clone the Zephyr repository and checkout the sha: d489765be4e57ca0d836d391dbda23284ac09e7f
    .. prompt::

        git clone https://github.com/zephyrproject-rtos/zephyr
        cd zephyr
        git checkout d489765be4e57ca0d836d391dbda23284ac09e7f

#. Download the latest Docker container of the build environment
    .. prompt::

        docker pull zephyrprojectrtos/zephyr-build:latest

#. Start the Docker Container (On Windows make sure to use absolute paths with forward slashes)
    .. prompt::
    
        docker run -ti -v <ZEPHYR_REPO_PATH>:/workdir -v <EC_MASTER_BASE_PATH>:/Master zephyrprojectrtos/zephyr-build:latest

#. Inside the Container change the directory
    .. prompt::
    
        /Master/Workspace/Zephyr/EcMasterDemo

#. Build the EcMasterDemo
    .. prompt::

        mkdir build && cd build
        cmake .. -DBOARD=up_squared -DRELEASE_MODE=Release
        make install

#. The stripped project file can be found in
    .. prompt::

        <EC_MASTER_BASE_PATH>/Bin/Zephyr/x64/Release/EcMasterDemo.strip

#. To run the demo place the stripped project file on the Up Squared board and connect to the serial console on UART 1. After booting into the Application it will prompt for command line arguments on the serial console.

.. seealso:: :ref:`gettingstarted:Running EcMasterDemo`

OS Compiler settings
********************

Besides the general settings from :ref:`gettingstarted:Compiling the EcMasterDemo` the following settings are necessary to build the example application for Zephyr.

Extra include paths
    .. code-block::
        
        <InstallPath>/SDK/INC/Zephyr
        <InstallPath>/Examples/Common/Zephyr

Extra source paths
    .. code-block::
    
        <InstallPath>/Examples/Common/Zephyr
        <InstallPath>/Sources/OsLayer/Zephyr

Extra library paths to the main EtherCAT components
    .. code-block::

        <InstallPath>/SDK/LIB/Zephyr