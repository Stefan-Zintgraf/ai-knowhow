********************************************
Application programming interface, reference
********************************************

The main header file to include is :file:`EcMotionAdvanced.h`. There the API function
prototypes, error codes and motion control function blocks can be found. Structure
definitions are specified in :file:`EcMotionDef.h` which is included directly by
:file:`EcMotionAdvanced.h` and therefor must not be included by the application.

Functions for initialization and deinitialization
*************************************************

mcInit
======

.. doxygenfunction:: mcInit

.. doxygenstruct:: MC_T_INIT_PARMS
    :members:

.. doxygenstruct:: EC_T_LOG_PARMS
    :members:

For further information about the treatment of log messages see the user manual of
EC-Master.

.. dropdown:: Example

    .. literalinclude:: ..\Snippets\EcMotionAdvancedSnippets.cpp
        :start-after: IGNORE_TEST(DocumentationSnippets, mcInit)
        :end-before: IGNORE_TEST(DocumentationSnippets, mcInit)
        :language: cpp
        :dedent: 4
        :lines: 2-

mcSetEthercatApiFunctions
=========================

.. doxygenfunction:: mcSetEthercatApiFunctions

.. doxygenstruct:: MC_T_INIT_ECAT_PARMS
    :members:

.. doxygentypedef:: MC_PF_GET_SLAVE_STATE

.. doxygentypedef:: MC_PF_COE_SDO_DOWNLOAD_REQ

.. dropdown:: Example

    .. literalinclude:: ..\Snippets\EcMotionAdvancedSnippets.cpp
        :start-after: IGNORE_TEST(DocumentationSnippets, mcSetEthercatApiFunctions)
        :end-before: IGNORE_TEST(DocumentationSnippets, mcSetEthercatApiFunctions)
        :language: cpp
        :dedent: 4
        :lines: 2-

An example for the definition of a SDO download function can be found in the demo
application.

mcDeinit
========

.. doxygenfunction:: mcDeinit

.. dropdown:: Example

    .. literalinclude:: ..\Snippets\EcMotionAdvancedSnippets.cpp
        :start-after: IGNORE_TEST(DocumentationSnippets, mcDeinit)
        :end-before: IGNORE_TEST(DocumentationSnippets, mcDeinit)
        :language: cpp
        :dedent: 4
        :lines: 2-

Create axis
***********

Almost all motion control function blocks have an :cpp:class:`AxisRef` as input. It is an
abstraction of the hardware and its drive.

.. doxygenclass:: AxisRef
    :undoc-members:

An object of this class must be created by one of the next functions.

mcCreateVirtualAxis
===================

.. doxygenfunction:: mcCreateVirtualAxis

.. doxygenstruct:: MC_T_AXIS_PARMS
    :members:

.. dropdown:: Example

    .. literalinclude:: ..\Snippets\EcMotionAdvancedSnippets.cpp
        :start-after: IGNORE_TEST(DocumentationSnippets, mcCreateVirtualAxis)
        :end-before: IGNORE_TEST(DocumentationSnippets, mcCreateVirtualAxis)
        :language: cpp
        :dedent: 4
        :lines: 2-

mcCreateDS402Axis
=================

.. doxygenfunction:: mcCreateDS402Axis

.. seealso::
    :cpp:struct:`MC_T_AXIS_PARMS`

.. doxygenstruct:: MC_T_AXIS_IO_ENDPOINT
    :members:

.. doxygenstruct:: MC_T_AXIS_ECAT_PARMS
    :members:

.. doxygenenum:: MC_T_DS402_OPERATION_MODE

.. dropdown:: Example

    .. literalinclude:: ..\Snippets\EcMotionAdvancedSnippets.cpp
        :start-after: IGNORE_TEST(DocumentationSnippets, mcCreateDS402Axis)
        :end-before: IGNORE_TEST(DocumentationSnippets, mcCreateDS402Axis)
        :language: cpp
        :dedent: 4
        :lines: 2-

Cyclic functions
****************

The EC-Motion-Advanced library itself does not create any threads. The application must
therefore cyclically call some functions to update the inputs and outputs and, for
example, calculate new target positions. A description of these function is given in the
next sections.

mcRefreshAxisInputs
===================

.. doxygenfunction:: mcRefreshAxisInputs

mcRefreshAxisOutputs
====================

.. doxygenfunction:: mcRefreshAxisOutputs

mcCyclicTask
============

.. doxygenfunction:: mcCyclicTask

.. dropdown:: Example

    .. literalinclude:: ..\Snippets\EcMotionAdvancedSnippets.cpp
        :start-after: IGNORE_TEST(DocumentationSnippets, CyclicCalls)
        :end-before: IGNORE_TEST(DocumentationSnippets, CyclicCalls)
        :language: cpp
        :dedent: 4
        :lines: 2-

General functions
*****************

mcGetText
=========

.. doxygenfunction:: mcGetText

Motion Control Function Blocks
******************************

Motion control function blocks are designed as callable C++ classes. They consist of a set of input
variables which are readable and writable and a set of output variables which are only
readable. Furthermore almost all function blocks have an instance of :cpp:class:`AxisRef`
as input output variable. In the description of the function blocks basic variables
are marked with '**B**' and optional parameters are marked with '**E**'. Additional
variables are indicated by '**V**'.

Each function block is callable. This means that an instance of the function block can
be used as a function. This executes the function block in the sense that the desired
operation is performed on the specified axis. The input variables have to be set before
the call, the output variables are calculated during the call and could be read afterwards.
Not all inputs need to be defined. In this case, the input values from the previous call
are used, or default values are used when the function block is invoked for the first
time.

.. dropdown:: Example

    .. literalinclude:: ..\Snippets\EcMotionAdvancedSnippets.cpp
        :start-after: IGNORE_TEST(DocumentationSnippets, CallMCFB)
        :end-before: IGNORE_TEST(DocumentationSnippets, CallMCFB)
        :language: cpp
        :dedent: 4
        :lines: 5-

McPower
=======

.. table::
    :widths: 2 4 20 25 50

    +----------------+---+---------------+---------------------+-------------------------------+
    | Function block                     | McPower                                             |
    +----------------+---+---------------+---------------------+-------------------------------+
    | This function block controls the    power stage (On or Off)                              |
    +----------------+---+---------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Axis          | AxisRef             | Reference to the axis         |
    +----------------+---+---------------+---------------------+-------------------------------+
    | VAR_IN                                                                                   |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Enable        | EC_T_BOOL           | As long as 'Enable' is true,  |
    |                |   |               |                     | power is being enabled.       |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | EnablePositive| EC_T_BOOL           | As long as 'Enable' is true,  |
    |                |   |               |                     | this permits motion in        |
    |                |   |               |                     | positive direction.           |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | EnableNegative| EC_T_BOOL           | As long as 'Enable' is true,  |
    |                |   |               |                     | this permits motion in        |
    |                |   |               |                     | negative direction.           |
    +----------------+---+---------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                  |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Status        | EC_T_BOOL           | Effective state of the power  |
    |                |   |               |                     | stage.                        |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | Valid         | EC_T_BOOL           | If true, a valid set of       |
    |                |   |               |                     | outputs is available at the   |
    |                |   |               |                     | function block.               |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Error         | EC_T_BOOL           | Signals that an error has     |
    |                |   |               |                     | occurred within the function  |
    |                |   |               |                     | block.                        |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | ErrorID       | EC_T_DWORD          | Error identification.         |
    +----------------+---+---------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McPower.tex
    :type: tikz
    :align: center

.. hint::
    Per axis only one function block McPower should be issued. Otherwise an error is given.

McStop
======

.. table::
    :widths: 2 4 20 25 50

    +----------------+---+---------------+---------------------+-------------------------------+
    | Function block                     | McStop                                              |
    +----------------+---+---------------+---------------------+-------------------------------+
    | This function block commands a controlled motion stop and transfers the axis to the      |
    | state 'Stopping'. It aborts any ongoing function block execution. While the axis is in   |
    | state 'Stopping', no other function block can perform any motion on the same axis. After |
    | the axis has reached 'Velocity' zero, the 'Done' output is set to TRUE immediately. The  |
    | axis remains in the state 'Stopping' as long as 'Execute' is still TRUE or 'Velocity'    |
    | zero is not yet reached. As soon as 'Done' is SET and 'Execute' is FALSE the axis goes   |
    | to state 'Standstill'.                                                                   |
    +----------------+---+---------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Axis          | AxisRef             | Reference to the axis         |
    +----------------+---+---------------+---------------------+-------------------------------+
    | VAR_IN                                                                                   |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Execute       | EC_T_BOOL           | Start the action at rising    |
    |                |   |               |                     | edge.                         |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | Deceleration  | EC_T_LREAL          | Value of the deceleration     |
    |                |   |               |                     | [u/s^2].                      |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | Jerk          | EC_T_LREAL          | Value of the jerk [u/s^3].    |
    +----------------+---+---------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                  |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Done          | EC_T_BOOL           | Zero velocity reached.        |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | Busy          | EC_T_BOOL           | The function block is not     |
    |                |   |               |                     | finished and new output values|
    |                |   |               |                     | are to be expected.           |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | CommandAborted| EC_T_BOOL           | 'Command' is aborted by       |
    |                |   |               |                     | switching off power (only     |
    |                |   |               |                     | possibility to abort).        |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Error         | EC_T_BOOL           | Signals that an error has     |
    |                |   |               |                     | occurred within the function  |
    |                |   |               |                     | block.                        |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | ErrorID       | EC_T_DWORD          | Error identification.         |
    +----------------+---+---------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McStop.tex
    :type: tikz
    :align: center

.. hint::
    As long as 'Execute' is high, the axis remains in the state 'Stopping' and may not be executing
    any other motion command.

McHalt
======

.. table::
    :widths: 2 4 20 25 50

    +----------------+---+---------------+---------------------+-------------------------------+
    | Function block                     | McHalt                                              |
    +----------------+---+---------------+---------------------+-------------------------------+
    | This function block commands a controlled motion stop. The axis is moved to the state    |
    | 'DiscreteMotion', until the velocity is zero. With the 'Done' output set, the state is   |
    | transferred to 'Standstill'.                                                             |
    +----------------+---+---------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Axis          | AxisRef             | Reference to the axis         |
    +----------------+---+---------------+---------------------+-------------------------------+
    | VAR_IN                                                                                   |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Execute       | EC_T_BOOL           | Start the action at rising    |
    |                |   |               |                     | edge.                         |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | Deceleration  | EC_T_LREAL          | Value of the deceleration     |
    |                |   |               |                     | [u/s^2].                      |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | Jerk          | EC_T_LREAL          | Value of the jerk [u/s^3].    |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | BufferMode    | MC_T_BUFFER_MODE    | Defines the chronological     |
    |                |   |               |                     | sequence of the function      |
    |                |   |               |                     | block.                        |
    +----------------+---+---------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                  |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Done          | EC_T_BOOL           | Zero velocity reached.        |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | Busy          | EC_T_BOOL           | The function block is not     |
    |                |   |               |                     | finished and new output values|
    |                |   |               |                     | are to be expected.           |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | Active        | EC_T_BOOL           | Indicates that the function   |
    |                |   |               |                     | block has control on the axis.|
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | CommandAborted| EC_T_BOOL           | 'Command' is aborted by       |
    |                |   |               |                     | another command.              |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Error         | EC_T_BOOL           | Signals that an error has     |
    |                |   |               |                     | occurred within the function  |
    |                |   |               |                     | block.                        |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | ErrorID       | EC_T_DWORD          | Error identification.         |
    +----------------+---+---------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McHalt.tex
    :type: tikz
    :align: center

McMoveAbsolute
==============

.. table::
    :widths: 2 4 20 25 50

    +--------------+---+-----------------+---------------------+-------------------------------+
    | Function block                     | McMoveAbsolute                                      |
    +--------------+---+-----------------+---------------------+-------------------------------+
    | This function block commands a controlled motion to a specified absolute position.       |
    +--------------+---+-----------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Axis            | AxisRef             | Reference to the axis         |
    +--------------+---+-----------------+---------------------+-------------------------------+
    | VAR_IN                                                                                   |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Execute         | EC_T_BOOL           | Start the motion at rising    |
    |              |   |                 |                     | edge.                         |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | ContinuousUpdate| EC_T_BOOL           | If TRUE use the current values|
    |              |   |                 |                     | of the input variables and    |
    |              |   |                 |                     | apply it to the ongoing       |
    |              |   |                 |                     | movement.                     |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Position        | EC_T_LREAL          | Commanded position for the    |
    |              |   |                 |                     | motion (in technical unit     |
    |              |   |                 |                     | [u]).                         |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Velocity        | EC_T_LREAL          | Value of the maximum velocity |
    |              |   |                 |                     | (not necessarily reached)     |
    |              |   |                 |                     | [u/s].                        |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Acceleration    | EC_T_LREAL          | Value of the acceleration     |
    |              |   |                 |                     | (increasing energy of the     |
    |              |   |                 |                     | motor) [u/s^2].               |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Deceleration    | EC_T_LREAL          | Value of the deceleration     |
    |              |   |                 |                     | (decreasing energy of the     |
    |              |   |                 |                     | motor) [u/s^2].               |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Jerk            | EC_T_LREAL          | Value of the Jerk [u/s^3].    |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Direction       | MC_T_DIRECTION      | Determine the approach to     |
    |              |   |                 |                     | calculate the path to move    |
    |              |   |                 |                     | for a modulo axis.            |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | BufferMode      | MC_T_BUFFER_MODE    | Defines the chronological     |
    |              |   |                 |                     | sequence of the function      |
    |              |   |                 |                     | block.                        |
    +--------------+---+-----------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                  |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Done            | EC_T_BOOL           | Commanded distance reached.   |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Busy            | EC_T_BOOL           | The function block is not     |
    |              |   |                 |                     | finished and new output values|
    |              |   |                 |                     | are to be expected.           |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Active          | EC_T_BOOL           | Indicates that the function   |
    |              |   |                 |                     | block has control on the axis.|
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | CommandAborted  | EC_T_BOOL           | 'Command' is aborted by       |
    |              |   |                 |                     | another command.              |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Error           | EC_T_BOOL           | Signals that an error has     |
    |              |   |                 |                     | occurred within the function  |
    |              |   |                 |                     | block.                        |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | ErrorID         | EC_T_DWORD          | Error identification.         |
    +--------------+---+-----------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McMoveAbsolute.tex
    :type: tikz
    :align: center

McMoveRelative
==============

.. table::
    :widths: 2 4 20 25 50

    +--------------+---+-----------------+---------------------+-------------------------------+
    | Function block                     | McMoveRelative                                      |
    +--------------+---+-----------------+---------------------+-------------------------------+
    | This function block commands a controlled motion of a specific distance relative to the  |
    | set position at the time of the execution.                                               |
    +--------------+---+-----------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Axis            | AxisRef             | Reference to the axis         |
    +--------------+---+-----------------+---------------------+-------------------------------+
    | VAR_IN                                                                                   |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Execute         | EC_T_BOOL           | Start the motion at rising    |
    |              |   |                 |                     | edge.                         |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | ContinuousUpdate| EC_T_BOOL           | If TRUE use the current values|
    |              |   |                 |                     | of the input variables and    |
    |              |   |                 |                     | apply it to the ongoing       |
    |              |   |                 |                     | movement.                     |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Distance        | EC_T_LREAL          | Relative distance for the     |
    |              |   |                 |                     | motion (in technical unit     |
    |              |   |                 |                     | [u]).                         |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Velocity        | EC_T_LREAL          | Value of the maximum velocity |
    |              |   |                 |                     | (not necessarily reached)     |
    |              |   |                 |                     | [u/s].                        |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Acceleration    | EC_T_LREAL          | Value of the acceleration     |
    |              |   |                 |                     | (increasing energy of the     |
    |              |   |                 |                     | motor) [u/s^2].               |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Deceleration    | EC_T_LREAL          | Value of the deceleration     |
    |              |   |                 |                     | (decreasing energy of the     |
    |              |   |                 |                     | motor) [u/s^2].               |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Jerk            | EC_T_LREAL          | Value of the Jerk [u/s^3].    |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | BufferMode      | MC_T_BUFFER_MODE    | Defines the chronological     |
    |              |   |                 |                     | sequence of the function      |
    |              |   |                 |                     | block.                        |
    +--------------+---+-----------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                  |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Done            | EC_T_BOOL           | Commanded distance reached.   |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Busy            | EC_T_BOOL           | The function block is not     |
    |              |   |                 |                     | finished and new output values|
    |              |   |                 |                     | are to be expected.           |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Active          | EC_T_BOOL           | Indicates that the function   |
    |              |   |                 |                     | block has control on the axis.|
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | CommandAborted  | EC_T_BOOL           | 'Command' is aborted by       |
    |              |   |                 |                     | another command.              |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Error           | EC_T_BOOL           | Signals that an error has     |
    |              |   |                 |                     | occurred within the function  |
    |              |   |                 |                     | block.                        |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | ErrorID         | EC_T_DWORD          | Error identification.         |
    +--------------+---+-----------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McMoveRelative.tex
    :type: tikz
    :align: center

McMoveVelocity
==============

.. table::
    :widths: 2 4 20 25 50

    +--------------+---+-----------------+---------------------+-------------------------------+
    | Function block                     | McMoveVelocity                                      |
    +--------------+---+-----------------+---------------------+-------------------------------+
    | This function block commands a never ending controlled motion at a specified velocity.   |
    +--------------+---+-----------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Axis            | AxisRef             | Reference to the axis         |
    +--------------+---+-----------------+---------------------+-------------------------------+
    | VAR_IN                                                                                   |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Execute         | EC_T_BOOL           | Start the motion at rising    |
    |              |   |                 |                     | edge.                         |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | ContinuousUpdate| EC_T_BOOL           | If TRUE use the current values|
    |              |   |                 |                     | of the input variables and    |
    |              |   |                 |                     | apply it to the ongoing       |
    |              |   |                 |                     | movement.                     |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Velocity        | EC_T_LREAL          | Value of the maximum velocity |
    |              |   |                 |                     | [u/s]. Can be a signed value. |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Acceleration    | EC_T_LREAL          | Value of the acceleration     |
    |              |   |                 |                     | (increasing energy of the     |
    |              |   |                 |                     | motor) [u/s^2].               |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Deceleration    | EC_T_LREAL          | Value of the deceleration     |
    |              |   |                 |                     | (decreasing energy of the     |
    |              |   |                 |                     | motor) [u/s^2].               |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Jerk            | EC_T_LREAL          | Value of the Jerk [u/s^3].    |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Direction       | MC_T_DIRECTION      | Direction of movement.        |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | BufferMode      | MC_T_BUFFER_MODE    | Defines the chronological     |
    |              |   |                 |                     | sequence of the function      |
    |              |   |                 |                     | block.                        |
    +--------------+---+-----------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                  |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | InVelocity      | EC_T_BOOL           | Commanded velocity reached.   |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Busy            | EC_T_BOOL           | The function block is not     |
    |              |   |                 |                     | finished and new output values|
    |              |   |                 |                     | are to be expected.           |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Active          | EC_T_BOOL           | Indicates that the function   |
    |              |   |                 |                     | block has control on the axis.|
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | CommandAborted  | EC_T_BOOL           | 'Command' is aborted by       |
    |              |   |                 |                     | another command.              |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Error           | EC_T_BOOL           | Signals that an error has     |
    |              |   |                 |                     | occurred within the function  |
    |              |   |                 |                     | block.                        |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | ErrorID         | EC_T_DWORD          | Error identification.         |
    +--------------+---+-----------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McMoveVelocity.tex
    :type: tikz
    :align: center

.. hint::
    In order to stop the motion, the function block has to be interrupted by another function block
    issuing a new motion command.

.. hint::
    A negative velocity combined with a negative direction leads to a positive velocity.

McMoveContinuousAbsolute
========================

.. table::
    :widths: 2 4 20 25 50

    +--------------+---+-----------------+---------------------+-------------------------------+
    | Function block                     | McMoveContinuousAbsolute                            |
    +--------------+---+-----------------+---------------------+-------------------------------+
    | This function block commands a controlled motion to a specified absolute position ending |
    | with the specified velocity.                                                             |
    +--------------+---+-----------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Axis            | AxisRef             | Reference to the axis         |
    +--------------+---+-----------------+---------------------+-------------------------------+
    | VAR_IN                                                                                   |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Execute         | EC_T_BOOL           | Start the motion at rising    |
    |              |   |                 |                     | edge.                         |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | ContinuousUpdate| EC_T_BOOL           | If TRUE use the current values|
    |              |   |                 |                     | of the input variables and    |
    |              |   |                 |                     | apply it to the ongoing       |
    |              |   |                 |                     | movement.                     |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Position        | EC_T_LREAL          | Commanded position for the    |
    |              |   |                 |                     | motion (in technical unit     |
    |              |   |                 |                     | [u]).                         |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | EndVelocity     | EC_T_LREAL          | Value of the end velocity     |
    |              |   |                 |                     | [u/s]. Signed value.          |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Velocity        | EC_T_LREAL          | Value of the maximum velocity |
    |              |   |                 |                     | (not necessarily reached)     |
    |              |   |                 |                     | [u/s].                        |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Acceleration    | EC_T_LREAL          | Value of the acceleration     |
    |              |   |                 |                     | (increasing energy of the     |
    |              |   |                 |                     | motor) [u/s^2].               |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Deceleration    | EC_T_LREAL          | Value of the deceleration     |
    |              |   |                 |                     | (decreasing energy of the     |
    |              |   |                 |                     | motor) [u/s^2].               |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Jerk            | EC_T_LREAL          | Value of the Jerk [u/s^3].    |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Direction       | MC_T_DIRECTION      | Determine the approach to     |
    |              |   |                 |                     | calculate the path to move    |
    |              |   |                 |                     | for a modulo axis.            |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | BufferMode      | MC_T_BUFFER_MODE    | Defines the chronological     |
    |              |   |                 |                     | sequence of the function      |
    |              |   |                 |                     | block.                        |
    +--------------+---+-----------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                  |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | InEndVelocity   | EC_T_BOOL           | Commanded position reached and|
    |              |   |                 |                     | running at requested end      |
    |              |   |                 |                     | velocity.                     |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Busy            | EC_T_BOOL           | The function block is not     |
    |              |   |                 |                     | finished and new output values|
    |              |   |                 |                     | are to be expected.           |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Active          | EC_T_BOOL           | Indicates that the function   |
    |              |   |                 |                     | block has control on the axis.|
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | CommandAborted  | EC_T_BOOL           | 'Command' is aborted by       |
    |              |   |                 |                     | another command.              |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Error           | EC_T_BOOL           | Signals that an error has     |
    |              |   |                 |                     | occurred within the function  |
    |              |   |                 |                     | block.                        |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | ErrorID         | EC_T_DWORD          | Error identification.         |
    +--------------+---+-----------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McMoveContinuousAbsolute.tex
    :type: tikz
    :align: center

.. hint::
    If the commanded position is reached and no new motion command is given, the axis
    continues to run with the specified 'EndVelocity'.

McMoveContinuousRelative
========================

.. table::
    :widths: 2 4 20 25 50

    +--------------+---+-----------------+---------------------+-------------------------------+
    | Function block                     | McMoveContinuousRelative                            |
    +--------------+---+-----------------+---------------------+-------------------------------+
    | This function block commands a controlled motion of a specific relative distance ending  |
    | with the specified velocity.                                                             |
    +--------------+---+-----------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Axis            | AxisRef             | Reference to the axis         |
    +--------------+---+-----------------+---------------------+-------------------------------+
    | VAR_IN                                                                                   |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Execute         | EC_T_BOOL           | Start the motion at rising    |
    |              |   |                 |                     | edge.                         |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | ContinuousUpdate| EC_T_BOOL           | If TRUE use the current values|
    |              |   |                 |                     | of the input variables and    |
    |              |   |                 |                     | apply it to the ongoing       |
    |              |   |                 |                     | movement.                     |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Distance        | EC_T_LREAL          | Relative distance for the     |
    |              |   |                 |                     | motion (in technical unit     |
    |              |   |                 |                     | [u]).                         |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | EndVelocity     | EC_T_LREAL          | Value of the end velocity     |
    |              |   |                 |                     | [u/s]. Signed value.          |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Velocity        | EC_T_LREAL          | Value of the maximum velocity |
    |              |   |                 |                     | (not necessarily reached)     |
    |              |   |                 |                     | [u/s].                        |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Acceleration    | EC_T_LREAL          | Value of the acceleration     |
    |              |   |                 |                     | (increasing energy of the     |
    |              |   |                 |                     | motor) [u/s^2].               |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Deceleration    | EC_T_LREAL          | Value of the deceleration     |
    |              |   |                 |                     | (decreasing energy of the     |
    |              |   |                 |                     | motor) [u/s^2].               |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Jerk            | EC_T_LREAL          | Value of the Jerk [u/s^3].    |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | BufferMode      | MC_T_BUFFER_MODE    | Defines the chronological     |
    |              |   |                 |                     | sequence of the function      |
    |              |   |                 |                     | block.                        |
    +--------------+---+-----------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                  |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | InEndVelocity   | EC_T_BOOL           | Commanded distance reached and|
    |              |   |                 |                     | running at requested end      |
    |              |   |                 |                     | velocity.                     |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Busy            | EC_T_BOOL           | The function block is not     |
    |              |   |                 |                     | finished and new output values|
    |              |   |                 |                     | are to be expected.           |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | Active          | EC_T_BOOL           | Indicates that the function   |
    |              |   |                 |                     | block has control on the axis.|
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | CommandAborted  | EC_T_BOOL           | 'Command' is aborted by       |
    |              |   |                 |                     | another command.              |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | B | Error           | EC_T_BOOL           | Signals that an error has     |
    |              |   |                 |                     | occurred within the function  |
    |              |   |                 |                     | block.                        |
    +--------------+---+-----------------+---------------------+-------------------------------+
    |              | E | ErrorID         | EC_T_DWORD          | Error identification.         |
    +--------------+---+-----------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McMoveContinuousRelative.tex
    :type: tikz
    :align: center

.. hint::
    If the commanded position is reached and no new motion command is given, the axis
    continues to run with the specified 'EndVelocity'.

McSetPosition
=============

.. table::
    :widths: 2 4 20 25 50

    +----------------+---+---------------+---------------------+-------------------------------+
    | Function block                     | McSetPosition                                       |
    +----------------+---+---------------+---------------------+-------------------------------+
    | This function block shifts the coordinate system of an axis by manipulating both the     |
    | set-point position as well as the actual position of an axis with the same value without |
    | any movement caused. This can be used for instance for a reference situation. This       |
    | function block can also be used during motion without changing the commanded position,   |
    | which is now positioned in the shifted coordinate system.                                |
    +----------------+---+---------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Axis          | AxisRef             | Reference to the axis         |
    +----------------+---+---------------+---------------------+-------------------------------+
    | VAR_IN                                                                                   |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Execute       | EC_T_BOOL           | Start setting position in     |
    |                |   |               |                     | axis.                         |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Position      | EC_T_LREAL          | Position in unit [u] (Means   |
    |                |   |               |                     | 'Distance' if 'Relative' is   |
    |                |   |               |                     | TRUE).                        |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | Relative      | EC_T_BOOL           | 'Relative' distance if TRUE,  |
    |                |   |               |                     | 'Absolute' position if FALSE  |
    |                |   |               |                     | (default).                    |
    +----------------+---+---------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                  |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Done          | EC_T_BOOL           | Position has new value.       |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | Busy          | EC_T_BOOL           | The function block is not     |
    |                |   |               |                     | finished and new output values|
    |                |   |               |                     | are to be expected.           |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Error         | EC_T_BOOL           | Signals that an error has     |
    |                |   |               |                     | occurred within the function  |
    |                |   |               |                     | block.                        |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | ErrorID       | EC_T_DWORD          | Error identification.         |
    +----------------+---+---------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McSetPosition.tex
    :type: tikz
    :align: center

.. hint::
    'Relative' means that 'Position' is added to the actual position value of the axis at the time of execution.
    This results in a recalibration by a specified distance. 'Absolute' means that the actual position value of the
    axis is set to the value of specified in the 'Position' parameter.

McReadParameter
===============

.. table::
    :widths: 2 4 20 25 50

    +----------------+---+----------------+---------------------+-------------------------------+
    | Function block                      | McReadParameter                                     |
    +----------------+---+----------------+---------------------+-------------------------------+
    | This function block returns the value of a specific parameter. The returned value is      |
    | converted to Real if necessary.                                                           |
    +----------------+---+----------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                 |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Axis           | AxisRef             | Reference to the axis         |
    +----------------+---+----------------+---------------------+-------------------------------+
    | VAR_IN                                                                                    |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Enable         | EC_T_BOOL           | Get the value of the parameter|
    |                |   |                |                     | continuously while enabled.   |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Parameternumber| EC_T_DWORD          | Number of the parameter.      |
    +----------------+---+----------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                   |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Valid          | EC_T_BOOL           | A valid output is available at|
    |                |   |                |                     | the function block.           |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | E | Busy           | EC_T_BOOL           | The function block is not     |
    |                |   |                |                     | finished and new output values|
    |                |   |                |                     | are to be expected.           |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Error          | EC_T_BOOL           | Signals that an error has     |
    |                |   |                |                     | occurred within the function  |
    |                |   |                |                     | block.                        |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | E | ErrorID        | EC_T_DWORD          | Error identification.         |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Value          | EC_T_LREAL          | Value of the specified        |
    |                |   |                |                     | parameter.                    |
    +----------------+---+----------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McReadParameter.tex
    :type: tikz
    :align: center

A list of supported parameter number is given by the enumeration :cpp:enum:`MC_T_PARAMETER_NUMBER`. It contains
both readable and writable parameter.

.. doxygenenum:: MC_T_PARAMETER_NUMBER

McReadBoolParameter
===================

.. table::
    :widths: 2 4 20 25 50

    +----------------+---+----------------+---------------------+-------------------------------+
    | Function block                      | McReadBoolParameter                                 |
    +----------------+---+----------------+---------------------+-------------------------------+
    | This function block returns the value of a specific parameter with data type BOOL.        |
    +----------------+---+----------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                 |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Axis           | AxisRef             | Reference to the axis         |
    +----------------+---+----------------+---------------------+-------------------------------+
    | VAR_IN                                                                                    |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Enable         | EC_T_BOOL           | Get the value of the parameter|
    |                |   |                |                     | continuously while enabled.   |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Parameternumber| EC_T_DWORD          | Number of the parameter.      |
    +----------------+---+----------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                   |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Valid          | EC_T_BOOL           | A valid output is available at|
    |                |   |                |                     | the function block.           |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | E | Busy           | EC_T_BOOL           | The function block is not     |
    |                |   |                |                     | finished and new output values|
    |                |   |                |                     | are to be expected.           |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Error          | EC_T_BOOL           | Signals that an error has     |
    |                |   |                |                     | occurred within the function  |
    |                |   |                |                     | block.                        |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | E | ErrorID        | EC_T_DWORD          | Error identification.         |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Value          | EC_T_BOOL           | Value of the specified        |
    |                |   |                |                     | parameter.                    |
    +----------------+---+----------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McReadBoolParameter.tex
    :type: tikz
    :align: center

.. seealso::
    :cpp:enum:`MC_T_PARAMETER_NUMBER`

McWriteParameter
================

.. table::
    :widths: 2 4 20 25 50

    +----------------+---+----------------+---------------------+-------------------------------+
    | Function block                      | McWriteParameter                                    |
    +----------------+---+----------------+---------------------+-------------------------------+
    | This function block modifies the value of a specific parameter.                           |
    +----------------+---+----------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                 |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Axis           | AxisRef             | Reference to the axis         |
    +----------------+---+----------------+---------------------+-------------------------------+
    | VAR_IN                                                                                    |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Execute        | EC_T_BOOL           | Write the value of the        |
    |                |   |                |                     | parameter at rising edge.     |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Parameternumber| EC_T_DWORD          | Number of the parameter.      |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Value          | EC_T_LREAL          | New value of the specified    |
    |                |   |                |                     | parameter.                    |
    +----------------+---+----------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                   |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Done           | EC_T_BOOL           | Parameter successfully        |
    |                |   |                |                     | written.                      |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | E | Busy           | EC_T_BOOL           | The function block is not     |
    |                |   |                |                     | finished and new output values|
    |                |   |                |                     | are to be expected.           |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Error          | EC_T_BOOL           | Signals that an error has     |
    |                |   |                |                     | occurred within the function  |
    |                |   |                |                     | block.                        |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | E | ErrorID        | EC_T_DWORD          | Error identification.         |
    +----------------+---+----------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McWriteParameter.tex
    :type: tikz
    :align: center

.. seealso::
    :cpp:enum:`MC_T_PARAMETER_NUMBER`

McWriteBoolParameter
====================

.. table::
    :widths: 2 4 20 25 50

    +----------------+---+----------------+---------------------+-------------------------------+
    | Function block                      | McWriteBoolParameter                                |
    +----------------+---+----------------+---------------------+-------------------------------+
    | This function block modifies the value of a specific parameter of data type BOOL.         |
    +----------------+---+----------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                 |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Axis           | AxisRef             | Reference to the axis         |
    +----------------+---+----------------+---------------------+-------------------------------+
    | VAR_IN                                                                                    |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Execute        | EC_T_BOOL           | Write the value of the        |
    |                |   |                |                     | parameter at rising edge.     |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Parameternumber| EC_T_DWORD          | Number of the parameter.      |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Value          | EC_T_BOOL           | New value of the specified    |
    |                |   |                |                     | parameter.                    |
    +----------------+---+----------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                   |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Done           | EC_T_BOOL           | Parameter successfully        |
    |                |   |                |                     | written.                      |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | E | Busy           | EC_T_BOOL           | The function block is not     |
    |                |   |                |                     | finished and new output values|
    |                |   |                |                     | are to be expected.           |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Error          | EC_T_BOOL           | Signals that an error has     |
    |                |   |                |                     | occurred within the function  |
    |                |   |                |                     | block.                        |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | E | ErrorID        | EC_T_DWORD          | Error identification.         |
    +----------------+---+----------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McWriteBoolParameter.tex
    :type: tikz
    :align: center

.. seealso::
    :cpp:enum:`MC_T_PARAMETER_NUMBER`

McReadDigitalInput
==================

.. table::
    :widths: 2 4 20 25 50

    +----------------+---+----------------+---------------------+-------------------------------+
    | Function block                      | McReadDigitalInput                                  |
    +----------------+---+----------------+---------------------+-------------------------------+
    | This function block gives access to the value of the digital input of an axis. It provides|
    | the value of the referenced input.                                                        |
    +----------------+---+----------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                 |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Axis           | AxisRef             | Reference to the axis         |
    +----------------+---+----------------+---------------------+-------------------------------+
    | VAR_IN                                                                                    |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Enable         | EC_T_BOOL           | Get the value of the selected |
    |                |   |                |                     | input signal continuously     |
    |                |   |                |                     | while enabled.                |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | E | Inputnumber    | EC_T_DWORD          | Selects the digital input.    |
    +----------------+---+----------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                   |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Valid          | EC_T_BOOL           | A valid output is available at|
    |                |   |                |                     | the function block.           |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | E | Busy           | EC_T_BOOL           | The function block is not     |
    |                |   |                |                     | finished and new output values|
    |                |   |                |                     | are to be expected.           |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Error          | EC_T_BOOL           | Signals that an error has     |
    |                |   |                |                     | occurred within the function  |
    |                |   |                |                     | block.                        |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | E | ErrorID        | EC_T_DWORD          | Error identification.         |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Value          | EC_T_BOOL           | The value of the selected     |
    |                |   |                |                     | input signal.                 |
    +----------------+---+----------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McReadDigitalInput.tex
    :type: tikz
    :align: center

McReadDigitalOutput
===================

.. table::
    :widths: 2 4 20 25 50

    +----------------+---+----------------+---------------------+-------------------------------+
    | Function block                      | McReadDigitalOutput                                 |
    +----------------+---+----------------+---------------------+-------------------------------+
    | This function block gives access to the value of the digital output of an axis. It        |
    | provides the value of the referenced output.                                              |
    +----------------+---+----------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                 |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Axis           | AxisRef             | Reference to the axis         |
    +----------------+---+----------------+---------------------+-------------------------------+
    | VAR_IN                                                                                    |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Enable         | EC_T_BOOL           | Get the value of the selected |
    |                |   |                |                     | output signal continuously    |
    |                |   |                |                     | while enabled.                |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | E | Outputnumber   | EC_T_DWORD          | Selects the digital output.   |
    +----------------+---+----------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                   |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Valid          | EC_T_BOOL           | A valid output is available at|
    |                |   |                |                     | the function block.           |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | E | Busy           | EC_T_BOOL           | The function block is not     |
    |                |   |                |                     | finished and new output values|
    |                |   |                |                     | are to be expected.           |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Error          | EC_T_BOOL           | Signals that an error has     |
    |                |   |                |                     | occurred within the function  |
    |                |   |                |                     | block.                        |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | E | ErrorID        | EC_T_DWORD          | Error identification.         |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Value          | EC_T_BOOL           | The value of the selected     |
    |                |   |                |                     | output signal.                |
    +----------------+---+----------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McReadDigitalOutput.tex
    :type: tikz
    :align: center

McWriteDigitalOutput
====================

.. table::
    :widths: 2 4 20 25 50

    +----------------+---+----------------+---------------------+-------------------------------+
    | Function block                      | McWriteDigitalOutput                                |
    +----------------+---+----------------+---------------------+-------------------------------+
    | This function block write a value to the digital output once.                             |
    +----------------+---+----------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                 |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Axis           | AxisRef             | Reference to the axis         |
    +----------------+---+----------------+---------------------+-------------------------------+
    | VAR_IN                                                                                    |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Execute        | EC_T_BOOL           | Write the value of the        |
    |                |   |                |                     | selected digital output at    |
    |                |   |                |                     | rising edge.                  |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | E | Outputnumber   | EC_T_DWORD          | Selects the digital output.   |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Value          | EC_T_BOOL           | The value of the selected     |
    |                |   |                |                     | digital output.               |
    +----------------+---+----------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                   |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Done           | EC_T_BOOL           | Writing of the digital output |
    |                |   |                |                     | signal is done.               |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | E | Busy           | EC_T_BOOL           | The function block is not     |
    |                |   |                |                     | finished and new output values|
    |                |   |                |                     | are to be expected.           |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | B | Error          | EC_T_BOOL           | Signals that an error has     |
    |                |   |                |                     | occurred within the function  |
    |                |   |                |                     | block.                        |
    +----------------+---+----------------+---------------------+-------------------------------+
    |                | E | ErrorID        | EC_T_DWORD          | Error identification.         |
    +----------------+---+----------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McWriteDigitalOutput.tex
    :type: tikz
    :align: center

McReadActualPosition
====================

.. table::
    :widths: 2 4 20 25 50

    +----------------+---+---------------+---------------------+-------------------------------+
    | Function block                     | McReadActualPosition                                |
    +----------------+---+---------------+---------------------+-------------------------------+
    | This function block returns the actual position.                                         |
    +----------------+---+---------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Axis          | AxisRef             | Reference to the axis         |
    +----------------+---+---------------+---------------------+-------------------------------+
    | VAR_IN                                                                                   |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Enable        | EC_T_BOOL           | Get the value of the parameter|
    |                |   |               |                     | continuously while enabled.   |
    +----------------+---+---------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                  |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Valid         | EC_T_BOOL           | A valid output is available at|
    |                |   |               |                     | the function block.           |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | Busy          | EC_T_BOOL           | The function block is not     |
    |                |   |               |                     | finished and new output values|
    |                |   |               |                     | are to be expected.           |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Error         | EC_T_BOOL           | Signals that an error has     |
    |                |   |               |                     | occurred within the function  |
    |                |   |               |                     | block.                        |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | ErrorID       | EC_T_DWORD          | Error identification.         |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | ActPosition   | EC_T_LREAL          | New absolute position (in     |
    |                |   |               |                     | axis' unit [u]).              |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | V | CmdPosition   | EC_T_LREAL          | Commanded position (in axis'  |
    |                |   |               |                     | unit [u]).                    |
    +----------------+---+---------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McReadActualPosition.tex
    :type: tikz
    :align: center

McReadActualVelocity
====================

.. table::
    :widths: 2 4 20 25 50

    +----------------+---+---------------+---------------------+-------------------------------+
    | Function block                     | McReadActualVelocity                                |
    +----------------+---+---------------+---------------------+-------------------------------+
    | This function block returns the value of the actual velocity as long as 'Enable' is set. |
    | 'Valid' is true when the data output 'Velocity' is valid. If 'Enable' is reset, the data |
    | loses its validity, and all outputs are reset, no matter if new data is available.       |
    +----------------+---+---------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Axis          | AxisRef             | Reference to the axis         |
    +----------------+---+---------------+---------------------+-------------------------------+
    | VAR_IN                                                                                   |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Enable        | EC_T_BOOL           | Get the value of the parameter|
    |                |   |               |                     | continuously while enabled.   |
    +----------------+---+---------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                  |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Valid         | EC_T_BOOL           | A valid output is available at|
    |                |   |               |                     | the function block.           |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | Busy          | EC_T_BOOL           | The function block is not     |
    |                |   |               |                     | finished and new output values|
    |                |   |               |                     | are to be expected.           |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Error         | EC_T_BOOL           | Signals that an error has     |
    |                |   |               |                     | occurred within the function  |
    |                |   |               |                     | block.                        |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | ErrorID       | EC_T_DWORD          | Error identification.         |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | ActVelocity   | EC_T_LREAL          | The value of the actual       |
    |                |   |               |                     | velocity (in axis' unit [u/s])|
    |                |   |               |                     | .                             |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | V | CmdVelocity   | EC_T_LREAL          | The value of the commanded    |
    |                |   |               |                     | velocity (in axis' unit [u/s])|
    |                |   |               |                     | .                             |
    +----------------+---+---------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McReadActualVelocity.tex
    :type: tikz
    :align: center

.. hint::
    The output 'Velocity' is a signed value.

McReadStatus
============

.. table::
    :widths: 2 4 22 25 50

    +----------------+---+--------------------+---------------------+---------------------------------------+
    | Function block                          | McReadStatus                                                |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    | This function block returns in detail the status of the state diagram of the                          |
    | selected axis.                                                                                        |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    | VAR_INOUT                                                                                             |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | B | Axis               | AxisRef             | Reference to the axis                 |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    | VAR_IN                                                                                                |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | B | Enable             | EC_T_BOOL           | Get the value of the parameter        |
    |                |   |                    |                     | continuously while enabled.           |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    | VAR_OUT                                                                                               |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | B | Valid              | EC_T_BOOL           | A valid set of outputs is             |
    |                |   |                    |                     | available at the function             |
    |                |   |                    |                     | block.                                |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | E | Busy               | EC_T_BOOL           | The function block is not             |
    |                |   |                    |                     | finished and new output values        |
    |                |   |                    |                     | are to be expected.                   |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | B | Error              | EC_T_BOOL           | Signals that an error has             |
    |                |   |                    |                     | occurred within the function          |
    |                |   |                    |                     | block.                                |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | E | ErrorID            | EC_T_DWORD          | Error identification.                 |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | B | ErrorStop          | EC_T_BOOL           | Axis is at state ERRORSTOP.           |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | B | Disabled           | EC_T_BOOL           | Axis is at state DISABLED.            |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | B | Stopping           | EC_T_BOOL           | Axis is at state STOPPING.            |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | E | Homing             | EC_T_BOOL           | Axis is at state HOMING.              |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | B | Standstill         | EC_T_BOOL           | Axis is at state STANDSTILL.          |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | E | DiscreteMotion     | EC_T_BOOL           | Axis is at state DISCRETEMOTION.      |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | E | ContinuousMotion   | EC_T_BOOL           | Axis is at state CONTINUOUSMOTION.    |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | E | SynchronizedMotion | EC_T_BOOL           | Axis is at state SYNCHRONIZEDMOTION.  |
    +----------------+---+--------------------+---------------------+---------------------------------------+

.. kroki::
    :filename: ../Media/McReadStatus.tex
    :type: tikz
    :align: center

McReadMotionState
=================

.. table::
    :widths: 2 4 22 25 50

    +----------------+---+--------------------+---------------------+---------------------------------------+
    | Function block                          | McReadMotionState                                           |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    | This function block returns in detail the status of the axis with respect to the motion currently in  |
    | progress.                                                                                             |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    | VAR_INOUT                                                                                             |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | B | Axis               | AxisRef             | Reference to the axis                 |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    | VAR_IN                                                                                                |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | B | Enable             | EC_T_BOOL           | Get the value of the parameter        |
    |                |   |                    |                     | continuously while enabled.           |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    | VAR_OUT                                                                                               |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | B | Valid              | EC_T_BOOL           | A valid set of outputs is             |
    |                |   |                    |                     | available at the function             |
    |                |   |                    |                     | block.                                |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | E | Busy               | EC_T_BOOL           | The function block is not             |
    |                |   |                    |                     | finished and new output values        |
    |                |   |                    |                     | are to be expected.                   |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | B | Error              | EC_T_BOOL           | Signals that an error has             |
    |                |   |                    |                     | occurred within the function          |
    |                |   |                    |                     | block.                                |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | E | ErrorID            | EC_T_DWORD          | Error identification.                 |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | E | ConstantVelocity   | EC_T_BOOL           | Velocity is constant. Velocity may be |
    |                |   |                    |                     | zero.                                 |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | E | Accelerating       | EC_T_BOOL           | Increasing the absolute value of the  |
    |                |   |                    |                     | velocity.                             |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | E | Decelerating       | EC_T_BOOL           | Decreasing the absolute value of the  |
    |                |   |                    |                     | velocity.                             |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | E | DirectionPositive  | EC_T_BOOL           | Signals that the position is          |
    |                |   |                    |                     | increasing.                           |
    +----------------+---+--------------------+---------------------+---------------------------------------+
    |                | E | DirectionNegative  | EC_T_BOOL           | Signals that the position is          |
    |                |   |                    |                     | decreasing.                           |
    +----------------+---+--------------------+---------------------+---------------------------------------+

.. kroki::
    :filename: ../Media/McReadMotionState.tex
    :type: tikz
    :align: center

McReadAxisInfo
==============

.. table::
    :widths: 2 4 20 25 50

    +----------------+---+--------------------+---------------------+-------------------------------+
    | Function block                          | McReadAxisInfo                                      |
    +----------------+---+--------------------+---------------------+-------------------------------+
    | This function block reads information concerning an axis, like modes,                         |
    | inputs directly related to the axis, and certain status information.                          |
    +----------------+---+--------------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                     |
    +----------------+---+--------------------+---------------------+-------------------------------+
    |                | B | Axis               | AxisRef             | Reference to the axis         |
    +----------------+---+--------------------+---------------------+-------------------------------+
    | VAR_IN                                                                                        |
    +----------------+---+--------------------+---------------------+-------------------------------+
    |                | B | Enable             | EC_T_BOOL           | Get the axis information      |
    |                |   |                    |                     | constantly while enabled.     |
    +----------------+---+--------------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                       |
    +----------------+---+--------------------+---------------------+-------------------------------+
    |                | B | Valid              | EC_T_BOOL           | True if a valid set of outputs|
    |                |   |                    |                     | is available.                 |
    +----------------+---+--------------------+---------------------+-------------------------------+
    |                | E | Busy               | EC_T_BOOL           | The function block is not     |
    |                |   |                    |                     | finished and new output values|
    |                |   |                    |                     | are to be expected.           |
    +----------------+---+--------------------+---------------------+-------------------------------+
    |                | B | Error              | EC_T_BOOL           | Signals that an error has     |
    |                |   |                    |                     | occurred within the function  |
    |                |   |                    |                     | block.                        |
    +----------------+---+--------------------+---------------------+-------------------------------+
    |                | E | ErrorID            | EC_T_DWORD          | Error identification.         |
    +----------------+---+--------------------+---------------------+-------------------------------+
    |                | E | Simulation         | EC_T_BOOL           | Axis is in simulation mode.   |
    +----------------+---+--------------------+---------------------+-------------------------------+
    |                | E | CommunicationReady | EC_T_BOOL           | 'Network' is initialized and  |
    |                |   |                    |                     | ready for communication.      |
    +----------------+---+--------------------+---------------------+-------------------------------+
    |                | E | ReadyForPowerOn    | EC_T_BOOL           | Drive is ready to be enabled  |
    |                |   |                    |                     | (power on).                   |
    +----------------+---+--------------------+---------------------+-------------------------------+
    |                | E | PowerOn            | EC_T_BOOL           | If true shows that the power  |
    |                |   |                    |                     | stage is switched on.         |
    +----------------+---+--------------------+---------------------+-------------------------------+
    |                | V | StatusWord         | EC_T_WORD           | Status word of axis.          |
    +----------------+---+--------------------+---------------------+-------------------------------+
    |                | V | ControlWord        | EC_T_WORD           | Control word of axis.         |
    +----------------+---+--------------------+---------------------+-------------------------------+
    |                | V | DriveState         | EC_T_WORD           | Drive state of axis.          |
    +----------------+---+--------------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McReadAxisInfo.tex
    :type: tikz
    :align: center

McReadAxisError
===============

.. table::
    :widths: 2 4 20 25 50

    +----------------+---+--------------------+---------------------+-------------------------------+
    | Function block                          | McReadAxisError                                     |
    +----------------+---+--------------------+---------------------+-------------------------------+
    | This function block presents general axis errors not relating to the function blocks (for     |
    | instance axis errors, drive errors, communication errors).                                    |
    +----------------+---+--------------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                     |
    +----------------+---+--------------------+---------------------+-------------------------------+
    |                | B | Axis               | AxisRef             | Reference to the axis         |
    +----------------+---+--------------------+---------------------+-------------------------------+
    | VAR_IN                                                                                        |
    +----------------+---+--------------------+---------------------+-------------------------------+
    |                | B | Enable             | EC_T_BOOL           | Get the value of the parameter|
    |                |   |                    |                     | continuously while enabled.   |
    +----------------+---+--------------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                       |
    +----------------+---+--------------------+---------------------+-------------------------------+
    |                | B | Valid              | EC_T_BOOL           | True if a valid output is     |
    |                |   |                    |                     | available at the function     |
    |                |   |                    |                     | block.                        |
    +----------------+---+--------------------+---------------------+-------------------------------+
    |                | E | Busy               | EC_T_BOOL           | The function block is not     |
    |                |   |                    |                     | finished and new output values|
    |                |   |                    |                     | are to be expected.           |
    +----------------+---+--------------------+---------------------+-------------------------------+
    |                | B | Error              | EC_T_BOOL           | Signals that an error has     |
    |                |   |                    |                     | occurred within the function  |
    |                |   |                    |                     | block.                        |
    +----------------+---+--------------------+---------------------+-------------------------------+
    |                | E | ErrorID            | EC_T_DWORD          | Error identification.         |
    +----------------+---+--------------------+---------------------+-------------------------------+
    |                | E | AxisErrorID        | EC_T_DWORD          | The value of the axis error.  |
    +----------------+---+--------------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McReadAxisError.tex
    :type: tikz
    :align: center

McReset
=======

.. table::
    :widths: 2 4 20 25 50

    +----------------+---+---------------+---------------------+-------------------------------+
    | Function block                     | McReset                                             |
    +----------------+---+---------------+---------------------+-------------------------------+
    | This function block makes the transition from the state 'ErrorStop' to 'Standstill' or   |
    | 'Disabled' by resetting all internal axis-related errors - it does not affect the output |
    | of the function block instances.                                                         |
    +----------------+---+---------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Axis          | AxisRef             | Reference to the axis         |
    +----------------+---+---------------+---------------------+-------------------------------+
    | VAR_IN                                                                                   |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Execute       | EC_T_BOOL           | Resets all internal           |
    |                |   |               |                     | axis-related errors.          |
    +----------------+---+---------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                  |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Done          | EC_T_BOOL           | 'Standstill' or 'Disabled'    |
    |                |   |               |                     | state is reached.             |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | Busy          | EC_T_BOOL           | The function block is not     |
    |                |   |               |                     | finished and new output values|
    |                |   |               |                     | are to be expected.           |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | B | Error         | EC_T_BOOL           | Signals that an error has     |
    |                |   |               |                     | occurred within the function  |
    |                |   |               |                     | block.                        |
    +----------------+---+---------------+---------------------+-------------------------------+
    |                | E | ErrorID       | EC_T_DWORD          | Error identification.         |
    +----------------+---+---------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McReset.tex
    :type: tikz
    :align: center

McCamTableSelect
================

.. table::
    :widths: 2 4 20 25 50

    +--------------+---+------------------+---------------------+-------------------------------+
    | Function block                      | McCamTableSelect                                    |
    +--------------+---+------------------+---------------------+-------------------------------+
    | This function block selects the CAM tables by setting the connections to the relevant     |
    | tables.                                                                                   |
    +--------------+---+------------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                 |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | Master           | AxisRef             | Reference to the master axis. |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | Axis             | AxisRef             | Reference to the slave axis.  |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | CamTable         | MC_T_CAM_REF        | Reference to CAM description. |
    +--------------+---+------------------+---------------------+-------------------------------+
    | VAR_IN                                                                                    |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | Execute          | EC_T_BOOL           | Selection at rising edge.     |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | Periodic         | EC_T_BOOL           | Distinguish between periodic  |
    |              |   |                  |                     | and non-periodic (single shot)|
    |              |   |                  |                     | mode.                         |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | MasterAbsolute   | EC_T_BOOL           | Distinguish between absolute  |
    |              |   |                  |                     | and relative coordinates of   |
    |              |   |                  |                     | master axis.                  |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | SlaveAbsolute    | EC_T_BOOL           | Distinguish between absolute  |
    |              |   |                  |                     | and relative coordinates of   |
    |              |   |                  |                     | slave axis.                   |
    +--------------+---+------------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                   |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | Done             | EC_T_BOOL           | Pre-selection done.           |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | Busy             | EC_T_BOOL           | The function block is not     |
    |              |   |                  |                     | finished and new output values|
    |              |   |                  |                     | are to be expected.           |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | Error            | EC_T_BOOL           | Signals that an error has     |
    |              |   |                  |                     | occurred within the function  |
    |              |   |                  |                     | block.                        |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | ErrorID          | EC_T_DWORD          | Error identification.         |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | CamTableID       | MC_T_CAM_ID         | Identifier of CAM table to be |
    |              |   |                  |                     | used in function block        |
    |              |   |                  |                     | McCamIn.                      |
    +--------------+---+------------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McCamTableSelect.tex
    :type: tikz
    :align: center

.. doxygenstruct:: MC_T_CAM_REF
    :members:

McCamIn
=======

.. table::
    :widths: 2 4 20 25 50

    +--------------+---+------------------+---------------------+-------------------------------+
    | Function block                      | McCamIn                                             |
    +--------------+---+------------------+---------------------+-------------------------------+
    | This function block engages the CAM.                                                      |
    +--------------+---+------------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                 |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | Master           | AxisRef             | Reference to the master axis. |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | Axis             | AxisRef             | Reference to the slave axis.  |
    +--------------+---+------------------+---------------------+-------------------------------+
    | VAR_IN                                                                                    |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | Execute          | EC_T_BOOL           | Start the CAM process at      |
    |              |   |                  |                     | the rising edge.              |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | ContinuousUpdate | EC_T_BOOL           | If TRUE use the current values|
    |              |   |                  |                     | of the input variables and    |
    |              |   |                  |                     | apply it to the ongoing       |
    |              |   |                  |                     | movement.                     |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | MasterOffset     | EC_T_LREAL          | Offset of the master shaft to |
    |              |   |                  |                     | cam.                          |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | SlaveOffset      | EC_T_LREAL          | Offset of slave table.        |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | MasterScaling    | EC_T_LREAL          | Factor for the master profile.|
    |              |   |                  |                     | From the slave point of view  |
    |              |   |                  |                     | the master overall profile is |
    |              |   |                  |                     | multiplied by this factor.    |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | SlaveScaling     | EC_T_LREAL          | Factor for the slave profile. |
    |              |   |                  |                     | The overall slave profile is  |
    |              |   |                  |                     | multiplied by this factor.    |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | StartMode        | MC_T_START_MODE     | Defines the mode how cam is   |
    |              |   |                  |                     | started.                      |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | MasterValueSource| MC_SOURCE           | Defines the source for        |
    |              |   |                  |                     | synchronization.              |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | CamTableID       | MC_T_CAM_ID         | Identifier of CAM table to be |
    |              |   |                  |                     | used, linked to the output of |
    |              |   |                  |                     | McCamTableSelect.             |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | BufferMode       | MC_T_BUFFER_MODE    | Defines the chronological     |
    |              |   |                  |                     | sequence of the function      |
    |              |   |                  |                     | block.                        |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | V | Velocity         | EC_T_LREAL          | Value of the velocity for     |
    |              |   |                  |                     | start mode RAMP_IN.           |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | V | Acceleration     | EC_T_LREAL          | Value of the acceleration for |
    |              |   |                  |                     | the start mode RAMP_IN.       |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | V | Deceleration     | EC_T_LREAL          | Value of the deceleration for |
    |              |   |                  |                     | the start mode RAMP_IN.       |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | V | Jerk             | EC_T_LREAL          | Value of the jerk for the     |
    |              |   |                  |                     | start mode RAMP_IN.           |
    +--------------+---+------------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                   |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | InSync           | EC_T_BOOL           | The commanded value is equal  |
    |              |   |                  |                     | to set value.                 |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | Busy             | EC_T_BOOL           | The function block is not     |
    |              |   |                  |                     | finished and new output values|
    |              |   |                  |                     | are to be expected.           |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | Active           | EC_T_BOOL           | Indicates that the function   |
    |              |   |                  |                     | block has control on the axis.|
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | CommandAborted   | EC_T_BOOL           | 'Command' is aborted by       |
    |              |   |                  |                     | another command.              |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | Error            | EC_T_BOOL           | Signals that an error has     |
    |              |   |                  |                     | occurred within the function  |
    |              |   |                  |                     | block.                        |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | ErrorID          | EC_T_DWORD          | Error identification.         |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | EndOfProfile     | EC_T_BOOL           | Pulsed output signaling the   |
    |              |   |                  |                     | cyclic end of the CAM profile.|
    |              |   |                  |                     | It is displayed every time the|
    |              |   |                  |                     | end of the CAM profile is     |
    |              |   |                  |                     | reached.                      |
    +--------------+---+------------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McCamIn.tex
    :type: tikz
    :align: center

.. hint::
    If the position of the slave axis does not correspond to the CAM profile, a jump at the slave
    axis will possibly occur.

McCamOut
========

.. table::
    :widths: 2 4 20 25 50

    +--------------+---+------------------+---------------------+-------------------------------+
    | Function block                      | McCamOut                                            |
    +--------------+---+------------------+---------------------+-------------------------------+
    | This function block disengages the slave axis from the master axis immediately.           |
    +--------------+---+------------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                 |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | Axis             | AxisRef             | Reference to the slave axis.  |
    +--------------+---+------------------+---------------------+-------------------------------+
    | VAR_IN                                                                                    |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | Execute          | EC_T_BOOL           | Start to disengage the slave  |
    |              |   |                  |                     | from the master.              |
    +--------------+---+------------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                   |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | Done             | EC_T_BOOL           | Disengaging completed.        |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | Busy             | EC_T_BOOL           | The function block is not     |
    |              |   |                  |                     | finished and new output values|
    |              |   |                  |                     | are to be expected.           |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | Error            | EC_T_BOOL           | Signals that an error has     |
    |              |   |                  |                     | occurred within the function  |
    |              |   |                  |                     | block.                        |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | ErrorID          | EC_T_DWORD          | Error identification.         |
    +--------------+---+------------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McCamOut.tex
    :type: tikz
    :align: center

.. hint::
    This command should be followed by another command, for instance McStop, McGearIn or any other
    move command. Otherwise the last velocity is maintained and there is no function block active on
    the slave axis till the next function block is issued.

McGearIn
========

.. table::
    :widths: 2 4 20 25 50

    +--------------+---+------------------+---------------------+-------------------------------+
    | Function block                      | McGearIn                                            |
    +--------------+---+------------------+---------------------+-------------------------------+
    | This function block commands a ratio between the velocity of the slave and master axis.   |
    +--------------+---+------------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                 |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | Master           | AxisRef             | Reference to the master axis. |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | Axis             | AxisRef             | Reference to the slave axis.  |
    +--------------+---+------------------+---------------------+-------------------------------+
    | VAR_IN                                                                                    |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | Execute          | EC_T_BOOL           | Start the gearing process at  |
    |              |   |                  |                     | the rising edge.              |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | ContinuousUpdate | EC_T_BOOL           | If TRUE use the current values|
    |              |   |                  |                     | of the input variables and    |
    |              |   |                  |                     | apply it to the ongoing       |
    |              |   |                  |                     | movement.                     |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | RatioNumerator   | EC_T_INT            | Gear ratio numerator.         |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | RatioDenominator | EC_T_DWORD          | Gear ratio denominator.       |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | MasterValueSource| MC_SOURCE           | Defines the source for        |
    |              |   |                  |                     | synchronization.              |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | Acceleration     | EC_T_LREAL          | Acceleration for gearing in.  |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | Deceleration     | EC_T_LREAL          | Deceleration for gearing in.  |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | Jerk             | EC_T_LREAL          | Jerk for gearing.             |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | BufferMode       | MC_T_BUFFER_MODE    | Defines the chronological     |
    |              |   |                  |                     | sequence of the function      |
    |              |   |                  |                     | block.                        |
    +--------------+---+------------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                   |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | InGear           | EC_T_BOOL           | The commanded value is equal  |
    |              |   |                  |                     | to set value.                 |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | Busy             | EC_T_BOOL           | The function block is not     |
    |              |   |                  |                     | finished and new output values|
    |              |   |                  |                     | are to be expected.           |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | Active           | EC_T_BOOL           | Indicates that the function   |
    |              |   |                  |                     | block has control on the axis.|
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | CommandAborted   | EC_T_BOOL           | 'Command' is aborted by       |
    |              |   |                  |                     | another command.              |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | Error            | EC_T_BOOL           | Signals that an error has     |
    |              |   |                  |                     | occurred within the function  |
    |              |   |                  |                     | block.                        |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | ErrorID          | EC_T_DWORD          | Error identification.         |
    +--------------+---+------------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McGearIn.tex
    :type: tikz
    :align: center

.. hint::
    The slave axis ramps to the ratio of the master axis velocity and locks in when this is reached.
    Any lost distance during synchronization is not caught up.

.. hint::
    Changing the gear ratio while McGearIn is running a consecutive McGearIn command can be used
    without the necessity to MCGearOut first.

McGearOut
=========

.. table::
    :widths: 2 4 20 25 50

    +--------------+---+------------------+---------------------+-------------------------------+
    | Function block                      | McGearOut                                           |
    +--------------+---+------------------+---------------------+-------------------------------+
    | This function block disengages the slave axis from the master axis.                       |
    +--------------+---+------------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                 |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | Axis             | AxisRef             | Reference to the slave axis.  |
    +--------------+---+------------------+---------------------+-------------------------------+
    | VAR_IN                                                                                    |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | Execute          | EC_T_BOOL           | Start disengaging process at  |
    |              |   |                  |                     | the rising edge.              |
    +--------------+---+------------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                   |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | Done             | EC_T_BOOL           | Disengaging completed.        |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | Busy             | EC_T_BOOL           | The function block is not     |
    |              |   |                  |                     | finished and new output values|
    |              |   |                  |                     | are to be expected.           |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | Error            | EC_T_BOOL           | Signals that an error has     |
    |              |   |                  |                     | occurred within the function  |
    |              |   |                  |                     | block.                        |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | ErrorID          | EC_T_DWORD          | Error identification.         |
    +--------------+---+------------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McGearOut.tex
    :type: tikz
    :align: center

.. hint::
    This command should be followed by another command, for instance McStop, McGearIn or any other
    move command. Otherwise the last velocity is maintained and there is no function block active on
    the slave axis till the next function block is issued.

McForwardPosition
=================

.. table::
    :widths: 2 4 20 25 50

    +--------------+---+------------------+---------------------+-------------------------------+
    | Function block                      | McForwardPosition                                   |
    +--------------+---+------------------+---------------------+-------------------------------+
    | This function block sets the axis to the state SynchronizedMotion and forwards the        |
    | position input directly to the commanded position.                                        |
    +--------------+---+------------------+---------------------+-------------------------------+
    | VAR_INOUT                                                                                 |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | Axis             | AxisRef             | Reference to axis.            |
    +--------------+---+------------------+---------------------+-------------------------------+
    | VAR_IN                                                                                    |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | Execute          | EC_T_BOOL           | Start forwarding position at  |
    |              |   |                  |                     | rising edge.                  |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | Position         | EC_T_LREAL          | Position to forward.          |
    +--------------+---+------------------+---------------------+-------------------------------+
    | VAR_OUT                                                                                   |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | Busy             | EC_T_BOOL           | The function block is not     |
    |              |   |                  |                     | finished and new output values|
    |              |   |                  |                     | are to be expected.           |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | Active           | EC_T_BOOL           | Indicates that the function   |
    |              |   |                  |                     | block has control on the axis.|
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | CommandAborted   | EC_T_BOOL           | 'Command' is aborted by       |
    |              |   |                  |                     | another command.              |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | B | Error            | EC_T_BOOL           | Signals that an error has     |
    |              |   |                  |                     | occurred within the function  |
    |              |   |                  |                     | block.                        |
    +--------------+---+------------------+---------------------+-------------------------------+
    |              | E | ErrorID          | EC_T_DWORD          | Error identification.         |
    +--------------+---+------------------+---------------------+-------------------------------+

.. kroki::
    :filename: ../Media/McForwardPosition.tex
    :type: tikz
    :align: center