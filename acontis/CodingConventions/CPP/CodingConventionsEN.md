# Programming Guidelines

## History

| Date | Author | Changed | Version |
|------|------|------|------|
| 1.10.1999 | Christoph Widmann | Created | 1.0 |
| 4.03.2003 | Christoph Widmann | Company name adjusted | 1.1 |
| 27.11.2025 | Stefan Zintgraf | Reformatted to MD format and slightly changed | 1.2 |
| 09.12.2025 | Stefan Zintgraf | Added EC-Embedded conventions | 1.3 |
| 10.12.2025 | Stefan Zintgraf | Added Security-by-Design / CRA coding requirements | 1.4 |
| 18.12.2025 | Paul Bußmann | Review EC-Embedded conventions | 1.5 |

## Document Information

**Responsible:** Stefan Zintgraf
**Originally Created:** 04.03.2003
**Latest Version:** 1.5
**Copyright:** acontis technologies GmbH
## Table of Contents

0. [GENERAL](#0-general)
   - 0.1 [Coding Conventions prefix mappings](#01-coding-conventions-prefix-mappings)
1. [MODULE](#1-module)
   - 1.1 [Definition of a Module](#11-definition-of-a-module)
   - 1.2 [Module Types](#12-module-types)
   - 1.3 [Interface / Public Interface](#13-interface-public-interface)
2. [NAMING CONVENTIONS](#2-naming-conventions)
   - 2.1 [Language Elements](#21-language-elements)
     - 2.1.1 [Name Type Prefix](#211-name-type-prefix)
     - 2.1.2 [Data Types](#212-data-types)
     - 2.1.3 [Enums](#213-enums)
     - 2.1.4 [Classes](#214-classes)
     - 2.1.5 [Functions and Methods](#215-functions-and-methods)
     - 2.1.6 [Variables](#216-variables)
       - 2.1.6.1 [Scope](#2161-scope)
       - 2.1.6.2 [Referencing](#2162-referencing)
       - 2.1.6.3 [Constants](#2163-constants)
   - 2.2 [Preprocessor Elements (Macros & Literals)](#22-preprocessor-elements-macros-literals)
   - 2.3 [Files](#23-files)
     - 2.3.1 [File Naming](#231-file-naming)
       - 2.3.1.1 [Name](#2311-name)
     - 2.3.1.2 [Type](#2312-type)
     - 2.3.2 [Source Code Files](#232-source-code-files)
     - 2.3.3 [Header Files](#233-header-files)
3. [FILE LAYOUT](#3-file-layout)
   - 3.1 [Sections Within the File](#31-sections-within-the-file)
     - 3.1.1 [File Header](#311-file-header)
     - 3.1.2 [Includes](#312-includes)
       - 3.1.2.1 [Source Files](#3121-source-files)
       - 3.1.2.2 ["Precompiled header" Entry (Visual C++)](#3122-precompiled-header-entry-visual-c)
       - 3.1.2.3 [Header Files](#3123-header-files)
     - 3.1.3 [Definitions & Macros](#313-definitions-macros)
     - 3.1.4 [Type Definitions, Enums](#314-type-definitions-enums)
     - 3.1.5 [Variables](#315-variables)
       - 3.1.5.1 [Definition of Global Variables](#3151-definition-of-global-variables)
       - 3.1.5.2 [Definition of Module-Related Variables](#3152-definition-of-module-related-variables)
       - 3.1.5.3 [Declaration of Global Variables](#3153-declaration-of-global-variables)
       - 3.1.5.4 [Initialization of Static Variables of a Class](#3154-initialization-of-static-variables-of-a-class)
     - 3.1.6 [Functions](#316-functions)
       - 3.1.6.1 [Declaration of Module-Related Functions](#3161-declaration-of-module-related-functions)
       - 3.1.6.2 [Definition of Module-Related Functions](#3162-definition-of-module-related-functions)
       - 3.1.6.3 [Declaration of Global Functions](#3163-declaration-of-global-functions)
       - 3.1.6.4 [Definition of Global Functions](#3164-definition-of-global-functions)
       - 3.1.6.5 [Definition of Class Methods](#3165-definition-of-class-methods)
     - 3.1.7 [Class Header](#317-class-header)
     - 3.1.8 [End of File](#318-end-of-file)
   - 3.2 [Source Code File Layout](#32-source-code-file-layout)
   - 3.3 [Header File Layout](#33-header-file-layout)
4. [CODING STYLE](#4-coding-style)
   - 4.1 [Spacing](#41-spacing)
     - 4.1.1 [Horizontal Spacing](#411-horizontal-spacing)
     - 4.1.2 [Vertical Spacing](#412-vertical-spacing)
   - 4.2 [Indentation](#42-indentation)
   - 4.3 [Comments](#43-comments)
     - 4.3.1 [Content of Comments](#431-content-of-comments)
     - 4.3.2 [Doxygen Documentation](#432-doxygen-documentation)
     - 4.3.3 [Comments During Development Phase](#433-comments-during-development-phase)
     - 4.3.4 [Comment Style Consistency](#434-comment-style-consistency)
5. [GENERAL PROGRAMMING GUIDELINES](#5-general-programming-guidelines)
   - 5.1 [Mandatory Guidelines](#51-mandatory-guidelines)
     - 5.1.1 [General](#511-general)
     - 5.1.4 [Class Design](#514-class-design)
       - 5.1.4.1 [No Malloc in Constructors](#5141-no-malloc-in-constructors)
     - 5.1.2 [Variables](#512-variables)
     - 5.1.3 [Functions](#513-functions)
   - 5.2 [Recommendations](#52-recommendations)
     - 5.2.1 [Language of Source Text and Comments](#521-language-of-source-text-and-comments)
     - 5.2.2 [General](#522-general)
     - 5.2.7 [Design Patterns](#527-design-patterns)
       - 5.2.7.1 [Threads](#5271-threads)
       - 5.2.7.1 [Locks](#5271-locks)
       - 5.2.7.1 [No exeptions, return code handling](#5271-no-exeptions-return-code-handling)
     - 5.2.3 [Formatting](#523-formatting)
     - 5.2.4 [Code Extensions in Debug Configuration](#524-code-extensions-in-debug-configuration)
       - 5.2.4.1 [Memory Checks](#5241-memory-checks)
     - 5.2.5 [Variables](#525-variables)
     - 5.2.6 [Functions](#526-functions)
       - 5.2.6.1 [Error Handling Strategy](#5261-error-handling-strategy)
       - 5.2.6.2 [Error Handling Pattern: dwRetVal and dwRes](#5262-error-handling-pattern-dwretval-and-dwres)
   - 5.3 [Modern C++ Guidelines (C++11 and Later)](#53-modern-c-guidelines-c11-and-later)
     - 5.3.1 [Null Pointers](#531-null-pointers)
     - 5.3.2 [Type Inference](#532-type-inference)
     - 5.3.3 [Smart Pointers](#533-smart-pointers)
     - 5.3.4 [Range-Based For Loops](#534-range-based-for-loops)
     - 5.3.5 [Move Semantics](#535-move-semantics)
   - 5.4 [Security-by-Design and Cyber Resilience Act (CRA)](#54-security-by-design-and-cyber-resilience-act-cra)
     - 5.4.1 [General Principles](#541-general-principles)
     - 5.4.2 [Input Validation and Attack Surface Reduction](#542-input-validation-and-attack-surface-reduction)
     - 5.4.3 [Authentication, Authorisation and Access Control](#543-authentication-authorisation-and-access-control)
     - 5.4.4 [Cryptography and Secrets Handling](#544-cryptography-and-secrets-handling)
     - 5.4.5 [Error Handling, Logging and Traceability](#545-error-handling-logging-and-traceability)
     - 5.4.6 [Updates, Dependencies and Vulnerability Handling](#546-updates-dependencies-and-vulnerability-handling)
6. [APPENDIX](#6-appendix)
   - 6.1 [Terms/Abbreviations](#61-termsabbreviations)
   - 6.2 [Base Documents](#62-base-documents)
7. [EC-EMBEDDED SPECIFIC CODING CONVENTIONS](#7-ec-embedded-specific-coding-conventions)
   - 7.1 [EC-Embedded Repository Directory Structure](#71-ec-embedded-repository-directory-structure)
   - 7.2 [EC-Embedded Products](#72-ec-embedded-products)
   - 7.3 [EC-Embedded Components](#73-ec-embedded-components)
   - 7.4 [EC-Embedded Source Code location](#74-ec-embedded-source-code-location)
   - 7.5 [EC-Embedded Spacing](#75-ec-embedded-spacing)
     - 7.5.1 [Horizontal Spacing](#751-horizontal-spacing)
   - 7.6 [EC-Embedded parenthesis and conditions](#76-ec-embedded-parenthesis-and-conditions)
   - 7.7 [EC-Embedded Type System and Hungarian Notation](#77-ec-embedded-type-system-and-hungarian-notation)
     - 7.7.1 [EC-Embedded Naming Prefixes](#771-ec-embedded-naming-prefixes)
     - 7.7.2 [EC-Embedded Type Prefixes](#772-ec-embedded-type-prefixes)
   - 7.2 [EC-Embedded Specific Constants and Defines](#72-ec-embedded-specific-constants-and-defines)
     - 7.2.1 [Boolean Constants](#721-boolean-constants)
     - 7.2.2 [Null Pointer Constant and check](#722-null-pointer-constant-and-check)
   - 7.3 [EC-Embedded Specific Restrictions](#73-ec-embedded-specific-restrictions)
     - 7.3.1 [C++ Syntax Restriction](#731-c-syntax-restriction)
     - 7.3.2 [Comment Style Restriction](#732-comment-style-restriction)
     - 7.3.3 [Inline Functions](#733-inline-functions)
   - 7.4 [EC-Embedded Programming Guidelines](#74-ec-embedded-programming-guidelines)
     - 7.4.1 [Namespace Usage](#741-namespace-usage)
     - 7.4.2 [Marking of Modules (Configuration)](#742-marking-of-modules-configuration)
     - 7.4.3 [Troubleshooting](#743-troubleshooting)
       - 7.4.1.1 [Compiler Errors](#7411-compiler-errors)
   - 7.5 [Relationship to Base Document](#75-relationship-to-base-document)
     - 8.11.1 [Key Differences from Base Document:](#key-differences-from-base-document)
     - 8.11.2 [Base Document Sections Still Apply:](#base-document-sections-still-apply)
   - 7.6 [References](#76-references)

---

## 0 GENERAL

### 0.1 Coding Conventions prefix mappings

In this coding conventions document, there are various places where specific prefixes for type names, class names etc. are used. These prefixes may be adjusted depending on the product or project for which the source code is being used.
The below table is a list of these mappings and how a potential neutral version may look

<table>
  <tr>
    <th>Prefix</th>
    <th>Meaning</th>
    <th>Examples</th>
    <th>Neutral Versions</th>
  </tr>
  <tr>
    <td rowspan="2">EC_T_</td>
    <td rowspan="2">Prefix for type definitions</td>
    <td>EC_T_DWORD</td>
    <td>DWORD</td>
  </tr>
  <tr>
    <td>EC_T_WORD</td>
    <td>WORD</td>
  </tr>
  <tr>
    <td>_EC_T_</td>
    <td>Prefix for struct</td>
    <td>_EC_T_STRUCT</td>
    <td>_STRUCT</td>
  </tr>
  <tr>
    <td rowspan="3">EC_</td>
    <td rowspan="3">Prefix for specific values</td>
    <td>EC_NULL</td>
    <td>NULL</td>
  </tr>
  <tr>
    <td>EC_TRUE</td>
    <td>TRUE</td>
  </tr>
  <tr>
    <td>EC_FALSE</td>
    <td>FALSE</td>
  </tr>
  <tr>
    <td>CEc</td>
    <td>Prefix for class definition</td>
    <td>CEcMyClass</td>
    <td>CMyClass</td>
  </tr>
</table>

## 1 MODULE

From a technical and organizational perspective, the definition of (software) modules is a useful concept. Many of the guidelines in the following sections make use of this.

### 1.1 Definition of a Module

A module is a piece of software (code and documentation) that is capable of executing functions. These functions are provided to external users through an interface.
Technically, a module is a way to manage functions in homogeneous groups. The interface hides the implementation and system dependencies from the user.
From an organizational perspective, a module is the basic unit for planning, project monitoring, and configuration management.
There are no rules for how large a module may be. Programming experience and intuition should be sufficient to recognize what can be treated as a unit.

### 1.2 Module Types

- Executable file (.EXE)
- Dynamic Link Library (.DLL)
- Static Library (.LIB)
- COM object (.DLL, .OCX, .EXE)
- Device driver (.SYS, .VXD)
- Object file (.O)
- Archive (.A)

### 1.3 Interface / Public Interface

In relation to the entire system, modules are "Black Boxes". Each module provides a public interface in the form of a header or IDL file, in which the access points to the various services are defined.
Module services are provided in functions or methods and properties. The interface file of the public interface contains all definitions necessary to call the module from a program.
In detail, the interface file should contain:
- Includes of header files used by the module interface
- Constant declarations
- Class and data type declarations
- Function prototypes
The interface file must not contain:
- Global data definitions
- Includes of header files that are only needed for the module implementation
Inline code should be placed in special files with the .inl file extension, which are included by the corresponding header files.

## 2 NAMING CONVENTIONS

The following conventions define the standards for naming modules, variables, constants, macros, types, structure and union elements.
Naming conventions help to:
- make identification of objects easier,
- improve consistency of the entire system,
- avoid conflicts,
- make the code uniform and readable.
Terms must case-sensitively match terms from the acontis glossary, if possible. Synonyms must be avoided. The acontis glossary is part of the Consense Management system.
The name should reflect the function of the object. It should be MEANINGFULLY abbreviated. Both names that are too long and too short should be avoided. In case of doubt, a longer, more meaningful name is preferable to an unclear abbreviation.
When defining names, it should be noted that code is written only once but read very often. Names should be meaningful and readable. Unclear abbreviations should be avoided.
Naming conventions do not apply to special objects such as Make files, READMEs, etc., if naming rules have already been established and established for these files.
**Examples:**
- `CHCIExportDBFromControllerMediator` - too long
- `AnzDp_` - too short
- `CEcEditTreeCtrl` - Meaningful shortened

### 2.1 Language Elements

Names meaningfully and readably describe the intent of the respective language element.
Names consist of words formed from letters (a-z, A-Z) and numbers (0-9). The name must begin with a letter.
Compound names are separated by capital letters.
All public names of a module are prefixed with the module abbreviation.

#### 2.1.1 Name Type Prefix

The name type prefix describes the type of element.
The following elements are distinguished:

| Language Element | Prefix |
|------|------|
| Function | - |
| Enumeration | E |
| Class | C |
| "Structure-Class" | S |
| Variable | - |
| array | a |
| C-Structure | sc |

**Examples:**

```c
enum EOpMode
{
    ...
};

class CRecording
{
    ...
};

struct SMsp
{
    ...
};

typedef int HND_MSP;

typedef _DEVICE
{
    int nPort;
    int nInterrupt;
} DEVICE, *PDEVICE;
```

#### 2.1.2 Data Types

The name of the data type describes the kind of data type. Elementary types (integer, float, char, etc.) or complex types such as classes, structures, or units can be defined.
In C++, structures can also be defined in the style of classes (inheritance, etc.). The difference to classes is that structures have no access restrictions (public, protected, private) - all members are public by default.
**Terminology:**
- **"Structure-Class"** (prefix `S`): C++ structs that use class-like features (constructors, methods, inheritance) but maintain public-by-default visibility
- **"C-Structure"** (prefix `sc` in typedef): Traditional C structs without methods
- **"Class"** (prefix `C`): C++ classes with explicit access control
Structures should be defined in C++ manner when:
- they are used in a C++ environment,
- inheritance is to be used,
- special initializations are desired.
**Examples:**

```c
typedef __int16 HND_ANA_VIEW;  // (private data type of a module)

typedef _MOD_DEVICE            // (C-struct)
{
    int nPort;
    int nInterrupt;
} MOD_DEVICE;

struct SAnaViewDesc: public SAnaDesc  // ( C++-struct)
{
    CString strShortName;
    bool bOnline;
};
```

#### 2.1.3 Enums

The enum type or an appropriate abbreviation is used as the prefix of enums.
**Examples:**

```c
enum EOpMode
{
    eOpModeManual,
    eOpModeAuto
};

enum EDrvCommand
{
    eCmdServerInit = 0,
    eCmdServerDeInit = 1,
    eCmdActivateCycleRead = 4,
    eCmdDeActivateCycleRead = 8,
};
```

#### 2.1.4 Classes

The class name describes its purpose. Each class designation begins with the prefix "C" (Exception: embedded classes). Derived classes contain (possibly in abbreviated form) the name of their base class before their own name.
**Examples:**

```c
class CHTTPServer
{
    CHTTPServer();
    ~CHTTPServer();
};

class CModuleOS9: public CModule
{
    CModuleOS9();
    ~CModuleOS9();
};

class CDrvCursor
{
    class Desc
    {
        Desc();
        ~Desc();
        CString m_strName;
    }
    CDrvCursor();
    ~CDrvCursor();

    Desc m_oDesc;
};
```

#### 2.1.5 Functions and Methods

Methods are the functions of a class. Their scope is always class-related. Therefore, only global functions exist, no global methods.
The method name of a class that belongs to the public interface does not need to be prefixed with the module name prefix, since the class name already indicates this. Public functions, on the other hand, are always prefixed with the module prefix.
**Examples:**

```c
// C-functions:
void RTWSetup();  // (RTW is the module name)

// methods of a class:
class CDrv
{
    bool Init();
    void DeInit();
};
```

For the public functions of a module, logically related functions can be marked with common name abbreviations. The Module-Noun-Verb rule is suitable for this:
- `RTWVxDLoad`
- `RTWIRQSet`
- `taskDelete`
- `taskSpawn`
- `taskSwitchHookAdd`
- `ThreadPrioritySet`
**Function Naming Convention:**
Use Camel Case for functions. If the function is an API, it starts with a capital letter. Local functions start with a lower case letter.
**Good:** `ReadEeprom` (API function)
**Bad:** `ReadEEProm`, `ReadEEPROM`

#### 2.1.6 Variables

The variable name describes its purpose. Each variable designation begins with a type prefix. The prefix should be based on the use of the variable. The type of use can be divided into the following categories:
**Variable Naming Style:**
Variable names must use Camel Case after the type prefix:
**Good:** `dwPdoIdx`
**Bad:** `dwpdoIdx`, `dwPDOIdx`, `dwpdoIDX`, `DwPdoIdx`
**Rationale:** Ensures consistent naming style and improves readability. The type prefix (e.g., `dw`, `n`, `b`) is followed by a Camel Case name where the first letter after the prefix is capitalized.
- general integer
- general floating point number
- boolean expression
- number where value is placed on the value range
- characters and strings
- user interface object
- ...
**General integers:**

| C/C++ Data Type | Prefix |
|------|------|
| int | n |
| unsigned int | u |
| Enumeration | e |

**General floating point number:**

| C/C++ Data Type | Prefix |
|------|------|
| float, double | f |

**Number where value is placed on the value range:**
Use size-specific prefixes when:
- Interfacing with hardware
- Network protocols
- Binary file formats
- Cross-platform size guarantees are critical

| C/C++ Data Type | Prefix |
|------|------|
| BYTE (8 bit) | by |
| unsigned char, UINT8 (8 bit) | u8 |
| WORD (16 bit) | w |
| unsigned short, UINT16 (16 bit) | u16 |
| DWORD (32 bit) | dw |
| unsigned long, UINT32 (32 bit) | u32 |
| char | n8 |
| short | n16 |
| long | n32 |

**Note:** For general-purpose integers where the conceptual meaning matters more than the exact size, use the general integer prefixes (`n` for `int`, `u` for `unsigned int`) from the table above.
**Boolean expression:**

| C/C++ Data Type | Prefix |
|------|------|
| bool, BOOL | b |

**Note:** Prefer `bool` (C++ standard type) for new code. Use `BOOL` only for Win32 API compatibility or when interfacing with legacy code that requires it.
**Characters and strings:**

| C/C++ Data Type | Prefix |
|------|------|
| char | ch |
| zero terminated string | sz |
| General string object | str |
| UNICODE string | ustr |
| ANSI string | astr |

**Other useful prefixes:**

| C/C++ Data Type | Prefix |
|------|------|
| Function pointer | pfn |
| General objects | o |
| WINDOWS handle | h |
| WINDOWS handle to device context | hdc |
| WINDOWS handle to window | hwnd |

**Special Variable Naming Conventions:**
- **Count Variables:** Variables for count end with "Cnt", e.g. `dwVarCnt`, `nItemCnt`
- **Loop Variables:** Variables for loops end with "Idx", e.g. `dwVarIdx`, `nItemIdx`
**Examples:**

```c
DWORD dwVarCnt;      /* number of variables */
int nItemCnt;        /* number of items */
DWORD dwVarIdx;      /* loop index */
int nItemIdx;        /* loop index */
```

**Rationale:** Provides consistent naming patterns for count and loop index variables, making it immediately clear what the variable represents.
- **State Machine Loop Variables:** Loop variables for state machines end with "Cur", e.g. `nStateCur`.

##### 2.1.6.1 Scope

Variables receive - depending on type - one of the following prefixes:

| Type | Prefix |
|------|------|
| member of a class | m_ |
| Static member of a class | s_ |
| Const member of a class | c_ |
| Global variable | G_ |
| Static variable (file scope) | S_ |
| Const variable | C_ |

Member variables of structures and unions do not receive class prefixes.
**Examples:**

```c
class CEcMyClass
{
public:
    int m_nMyVar;
};

typedef struct _EC_T_MY_STRUCT
{
    int nMyVar;
} EC_T_MY_STRUCT;
EC_T_MY_STRUCT G_oMyStruct;
```

```c
EC_T_VOID MyFunc()
{
    int nMyVar;
    CEcMyClass oMyClassInstance;
    CEcMyClass* poMyClassInstance = &oMyClassInstance;
```

```c
    oMyClassInstance.m_nMyVar = 1;
```

```c
    G_oMyStruct.nMyVar = 1;
}
```

##### 2.1.6.2 Referencing

The referencing prefix describes how a variable is referenced. The referencing prefix must not be used for functions, data types, etc.

| Referencing | Prefix |
|------|------|
| Struct / Class Variable | o |
| Pointer | p |
| Array | a |

Pointer variable names have the prefix p for each dependent level.
**Examples:**

```c
    CEcMyClass oMyClassInstance;
    CEcMyClass* poMyClassInstance = &oMyClassInstance;
    CEcMyClass** ppoMyClassInstance = &poMyClassInstance;
    EC_T_MY_STRUCT aoMyData[2];
    EC_T_DWORD adwMyData[2];
```

##### 2.1.6.3 Constants

The constant name is the logical meaning (e.g., nMaxUsers) of the constant. Naming constants with their numeric value should be avoided. Public constants of a module receive the module name as prefix.
**Examples:**

```c
const int C_nMaxUsers = 42;                          // (private constant of a module)
const CString C_strModDefaultConnect = "Admin";      // (public constant of module mod)
```

**Don't use the following:**

```c
const int nThousand = 1000;  // bad use
```

**Exception:**
- `EC_NULL`: NULL pointer

### 2.2 Preprocessor Elements (Macros & Literals)

The macro name corresponds to the logical meaning.
Literals are definitions of typeless constants. They are replaced by the preprocessor with the content of the definition. The compiler only sees what was replaced.
Macros are definitions of identifiers that are replaced by the preprocessor with the corresponding code or corresponding data. Macros can also be provided with arguments, which are also replaced.
A definition (both literal and macro) should be avoided if possible. In C++ it is usually not necessary to use definitions. Instead of literals that describe numeric values, enums or const should be used, and instead of macros, inline functions should be used.
Macro names consist of words where only capital letters (A-Z) and numbers (0-9) are used. These words, which together form a name, are separated by an underscore "_" (e.g., "MAKE_ERROR_CODE").
If a macro belongs to the interface of a module, the module prefix is placed before the macro name.
Predefined macros (such as OK, ERROR, etc.) should not be redefined.
**Macro Definition Format:**
Spaces between the macro name and the argument list cannot be handled by some compilers (e.g., the ARM Compiler for QNX):
**Incorrect:**

```c
#define GET_FRM_BOOL (ptr)       DWORDSWAP(GETDWORD((ptr)))
#define GET_FRM_WORD (ptr)       WORDSWAP (GETWORD ((ptr)))
```

**Correct:**

```c
#define GET_FRM_BOOL(ptr)        DWORDSWAP(GETDWORD((ptr)))
#define GET_FRM_WORD(ptr)        WORDSWAP(GETWORD((ptr)))
```

**Examples:**

```c
#define BUFFER_SIZE 5000                    // (Literal)
#define TRACE(STRING) AfxTrace(#STRING)     // (Macro)

RTW_STATUS                                  // (public macro of module RTW)
MESSAGE_SIZE                                // (private macro of module mod)
```

### 2.3 Files

A file is identified by: `<FileName>.<FileType>`

#### 2.3.1 File Naming

##### 2.3.1.1 Name

Only one "." may appear in the file name, namely exactly the one between "FileName" and "FileType". The "file name" should represent the content/function of the file.
Allowed characters are a-z, A-Z, 0-9 and _. Umlauts, spaces, and special characters should be avoided.
The name may be longer than 8 characters but should be "meaningfully" abbreviated.

#### 2.3.1.2 Type

The "FileType" indicates what kind of file it is, e.g., source, header, etc.
For the following file types, the specified extension is to be used:

| File Type | Extension |
|------|------|
| MS-Word document | *.docx |
| C source code file | *.c |
| C++ source code file | *.cpp |
| C & C++ header file | *.h |
| Executable file | *.exe |
| Dynamic Link Library | *.dll/.so |
| Workspace | *.sln |
| Project file | *.vcxprj/.pro |
| Resource script | *.rc, *.rc2 |
| Icon, Bitmap files | *.ico, *.bmp |
| Object code | *.obj |
| Compiled resources | *.res |
| Import Library / Static Library | *.lib |

The same applies to the following GNU-specific file types:

| File Type | GNU |
|------|------|
| Makefile | Makefile (without extension) |
| Object code | *.o |
| Library | *.a |
| Shell scripts | *.sh |
| WinSCP | *.scp |

#### 2.3.2 Source Code Files

For source code files, the following additional rules must be observed:
- if a source file contains a class, the file name is the same as the class name. Normally, the definition and declaration of exactly one class is located in a source and the associated header file.
- if a source file contains a single function, the file name is the same as the function name.
- multiple functions in a source file are useful if they have a close relationship to each other. In this case, the file name is based on the functionality.
- All source code of a class (e.g., its method definitions) is collected in a single source file.
- Inline code is either kept in a .inl file or after the class definition in the header file.
- Each source file must be independently compilable, i.e., no source files may be included.

#### 2.3.3 Header Files

All functions, data types, and macros that are to be accessed from other modules are declared in the public header file "ModuleName.h". This represents the public interface of the module.
Functions, data types, and macros that are only used within the module but are declared in various files are declared in the private header file "ModuleNamePrivate.h".
If files are shared in SourceSafe across multiple different projects, general-purpose names must be used for the public and private header files. In this case, the names "Module.h" and "ModulePrivate.h" are to be used.
**Example:**

```c
#include "ModulePrivate.h"     /* private include in Sources/EcMaster */
#include "Module.h"            /* public interface in SDK/INC */

```

## 3 FILE LAYOUT

A common file layout must be maintained for source code files. To be able to specify or restore the layout as automatically as possible, the individual sections are to be marked with identifiers.
**Example-Section (Block Comments - ****Doxygen****-Style):**

```c
/*-----------------------------------------------------------------------------
 * ...
 *---------------------------------------------------------------------------*/
```

**Section Headers:**
Sections are marked with block comment format:

```c
/*-SECTION NAME--------------------------------------------------*/
```

**Examples from template files:**

```c
/*-INCLUDES------------------------------------------------------------------*/
/*-DEFINES/MACROS------------------------------------------------------------*/
/*-TYPEDEFS/ENUMS------------------------------------------------------------*/
/*-GLOBAL VARIABLE DEFINITIONS-----------------------------------------------*/
/*-MODULE VARIABLE DEFINITIONS-----------------------------------------------*/
/*-LOCAL VARIABLES-----------------------------------------------------------*/
/*-FUNCTION DECLARATIONS-----------------------------------------------------*/
/*-MODULE FUNCTION DECLARATIONS----------------------------------------------*/
/*-HELPER FUNCTIONS----------------------------------------------------------*/
/*-GLOBAL FUNCTION DEFINITIONS-----------------------------------------------*/
/*-MODULE FUNCTION DEFINITIONS-----------------------------------------------*/
/*-END OF SOURCE FILE--------------------------------------------------------*/
```

**Note on Section Names:** Section names can be customized to better organize code while maintaining the standard format. Common alternatives include:
- `/*-LOCAL VARIABLES---*/` as an alternative to `/*-MODULE VARIABLE DEFINITIONS---*/` for static file-scope variables
- `/*-HELPER FUNCTIONS---*/` or `/*-FUNCTION DECLARATIONS---*/` for organizing helper/utility functions or forward declarations
**Note:** All section headers use block comments (`/* */`), not line comments (`//`).

### 3.1 Sections Within the File

Listed below are the various sections that can exist in a C/C++ source and header file. Except for the file header, all other sections and their headings are optional. If at least one entry exists for a section, then the heading is also to be placed. Otherwise, these can be omitted.
Two lines of spacing must be maintained between each section.

#### 3.1.1 File Header

The file header includes:
- File name
- Copyright notice
- optional: Response (responsible person/contact)
- optional: Description (short module description)
**Copyright Notice:**
The copyright notice is always: `acontis technologies GmbH, Weingarten, Germany`
**Response Field:**
The Response field contains the name of the responsible person or contact for the file.
**File Header Format (****Doxygen****-Style):**
All file headers use Doxygen-style block comments:

```c
/*-----------------------------------------------------------------------------
 * FunctionTemplate.c 
 * Copyright                acontis technologies GmbH, Weingarten, Germany
 * Response                 Stefan Zintgraf
 * Description              TODO: Add a module description
 *---------------------------------------------------------------------------*/
```

**Note:** The file header always uses block comments (`/* */`) in Doxygen style, not line comments (`//`).

#### 3.1.2 Includes

The include block consists of one or more C preprocessor #include statements. In this block, all header files that are included in a module are listed together.
An absolute path in #include statements is not allowed. Instead, the compiler option -I should be used, or relative #includes.

##### 3.1.2.1 Source Files

As the first file after the precompiled header, the module-internal private header file "ModuleNamePrivate.h" is always specified.
This is followed by the associated header file; then all other required header files are included.

##### 3.1.2.2 "Precompiled header" Entry (Visual C++)

The precompiled-header entry is only used in source files. It should only be used when the compiler supports this function. The precompiled-header file includes those header files that do not change within the project. This also includes all system include files.
The precompiled-header file is to be named "stdafx.h", all includes should be in stdafx.h
**Example (C++ with precompiled header):**

```c
/*-INCLUDES------------------------------------------------------------------*/
#include "stdafx.h"

```

**Example (C without precompiled header):**

```c
/*-INCLUDES------------------------------------------------------------------*/
#include "EcOs.h"
#include "EcList.h"
```

**Note:** The precompiled-header is only used in C++ files. In pure C files it is omitted.

##### 3.1.2.3 Header Files

In the header file, exactly those (and only these) header files are to be found that are necessary for compiling the content of the header file. These are the header files of the referenced data types, functions, classes, macros, etc.
Classes and structs that are only referenced by pointer (e.g., `CEcMyClass* m_poMyVar`, `struct _EC_T_MY_STRUCT*`) are made known to the compiler through a forward declaration.
**Example:**

```c
/*-INCLUDES------------------------------------------------------------------*/
#include "EcMaster.h"
```

```c
/*-FORWARD DECLARATIONS------------------------------------------------------*/
struct _EC_T_MBXTFER;
```

#### 3.1.3 Definitions & Macros

In this block, all definitions and macro definitions (#define) of a module are listed together.
**Usage:** Header file, source file.
**Example:**

```c
/*-DEFINES/MACROS------------------------------------------------------------*/
#if (defined DEBUG)
#define EC_ESMC_BUFSIZE      1460    /**< RX/TX buffer size in task level */
#endif /* DEBUG */

#ifndef EC_ESMC_BUFSIZE
#define EC_ESMC_BUFSIZE      1536    /**< RX/TX buffer size in task level */
#endif
```

#### 3.1.4 Type Definitions, Enums

In this block, all type definitions (typedef) of a module are listed together.
**Usage:** Header file, source file.
**Example:**

```c
/*-TYPEDEFS/ENUMS------------------------------------------------------------*/
typedef _EC_T_DEVICE
{
    int nPort;
    int nInterrupt;
} EC_T_DEVICE;
```

#### 3.1.5 Variables

##### 3.1.5.1 Definition of Global Variables

In this block, all globally valid variables that are declared in the associated header file (with extern) are initialized.
**Usage:** Source file.
**Example:**

```c
/*-GLOBAL VARIABLE DEFINITIONS-----------------------------------------------*/
int G_nAppInstance;
```

##### 3.1.5.2 Definition of Module-Related Variables

In this block, all module-related variables are defined.
**Usage:** Source file.
**Example:**

```c
/*-MODULE VARIABLE DEFINITIONS-----------------------------------------------*/
DWORD S_nModuleType;
```

##### 3.1.5.3 Declaration of Global Variables

In this block, all global variables are declared with extern.
**Usage:** Header file.
**Example:**

```c
/*-GLOBAL VARIABLE DECLARATIONS----------------------------------------------*/
extern int G_nAppInstance;
```

##### 3.1.5.4 Initialization of Static Variables of a Class

In this block, all static variables of a class are initialized.
**Usage:** Source file.
**Example:**

```c
/*-STATIC CLASS-MEMBERS------------------------------------------------------*/
static int CObjectCPP::m_nDevice = 5;
```

#### 3.1.6 Functions

The block with function or method definitions is placed either in the source file or in the .inl file. It serves to describe the function and its parameters.
**Example with ****Doxygen**** block-comments:**

```c
/*****************************************************************************/
/** \brief short comment
*
* detailed description. This: #moduleCFunction is a link. This: #S_nStaticVar, too!
*
* \return OK or ERROR
*/
STATUS
globalCFunction
(   int      wParam1,                   /**< [in] comment */
    int*     wParam2 )                  /**< [in, out] comment */
{
char chLocal1;  /* first local variable */
WORD wLocal2;   /* second local variable */

    if( wParam1 == wLocal2 )
    {
        chLocal1 = 'A';
    }

}
```

**Example for C++ class methods:**

```c
/*****************************************************************************/
/** \brief TODO: add a method-description.
*
* \param nX [in,out] comment
* \param nY [in,out] comment
* \return comment
*/
bool
CObjectCPP::Method
(   int nX,                             /* [in,out] comment */
    int nY )                            /* [in,out] comment */
{
}
```

The function declaration itself is not commented, but the function definition is.
**Example (simple declaration):**

```c
STATUS globalCFunction( int wParam1, int* wParam2 );
```

**Example (when the argument list exceeds the maximum character limit):**

```c
BOOL IoControl( LPVOID  lpInBuffer, DWORD dwInBufferSize,
                LPVOID  lpOutBuffer, DWORD dwOutBufferSize,
                LPDWORD pdwBytesReturned);
```

**Example (C++ method declaration in header):**

```c
bool Method( int nX, int nY );     /**< method description */
```

##### 3.1.6.1 Declaration of Module-Related Functions

In this block, all functions that are only needed within the module are declared.
**Usage:** Source file.
**Example:**

```c
/*-MODULE FUNCTION DECLARATIONS----------------------------------------------*/
static STATUS moduleCFunction( );
```

##### 3.1.6.2 Definition of Module-Related Functions

In this block, all function definitions that are only needed within the module are listed together.
**Usage:** Source file.
**Example:**

```c
/*-MODULE FUNCTION DEFINITIONS-----------------------------------------------*/

/*****************************************************************************/
/** \brief short comment
*
* detailed description. This: #globalCFunction is a link.
*
* \return OK or ERROR
*/
static STATUS
moduleCFunction
( )
{
char chLocal1;  /* first local variable */
WORD wLocal2;   /* second local variable */

}
```

##### 3.1.6.3 Declaration of Global Functions

In this block, all functions that are also visible outside the module are declared.
**Usage:** Header file.
**Example:**

```c
/*-GLOBAL FUNCTION DECLARATIONS----------------------------------------------*/
STATUS globalCFunction( int wParam1, int* wParam2 );
```

##### 3.1.6.4 Definition of Global Functions

In this block, all function definitions that are also visible outside the module are listed together.
**Usage:** Source file.
**Example:**

```c
/*-GLOBAL FUNCTION DEFINITIONS-----------------------------------------------*/

/*****************************************************************************/
/** \brief short comment
*
* detailed description. This: #moduleCFunction is a link. This: #S_nStaticVar, too!
*
* \param wParam1 [in] comment
* \param wParam2 [in,out] comment
* \return OK or ERROR
*/
STATUS
globalCFunction
(   int      wParam1,                   /**< [in] comment */
    int*     wParam2 )                  /**< [in, out] comment */
{
char chLocal1;  /* first local variable */
WORD wLocal2;   /* second local variable */

    if( wParam1 == wLocal2 )
    {
        chLocal1 = 'A';
    }
}
```

##### 3.1.6.5 Definition of Class Methods

In this block, all method definitions are listed together.
**Usage:** Source file, inline file.
**Example:**

```c
/*-CLASS-METHODS-------------------------------------------------------------*/

/*****************************************************************************/
/** \brief TODO: add a method-description.
*
* \param nX [in,out] comment
* \param nY [in,out] comment
* \return comment
*/
bool
CObjectCPP::Method
(   int nX,                             /* [in,out] comment */
    int nY )                            /* [in,out] comment */
{
}
```

#### 3.1.7 Class Header

A class header is to be placed before each class definition. This serves the purpose of a short class description.
**Example:**

```c
/*****************************************************************************/
/** \brief Use this control to show percentual relations in a pie-diagram.
 */
class CCapacityCtrl : public CStatic
{
    ...
};
```

The various parts of a class definition are to be ordered in the following sequence (the individual parts are optional):
1. friend classes
2. MACROS (e.g., DECLARE_DYNAMIC)
3. Type definitions/Enums (public)
4. Type definitions/Enums (protected)
5. Type definitions/Enums (private)
6. Embedded Classes (public)
7. Embedded Classes (protected)
8. Embedded Classes (private)
9. Constructors and Destructors (public), as well as the associated methods, if constructor/destructor are not public
10. Constructors and Destructors (protected)
11. Constructors and Destructors (private)
12. Member variables (public)
13. Member variables (protected)
14. Member variables (private)
15. Methods (public)
16. Methods (protected)
17. Methods (private)
Classes that contain a larger number of member variables and methods can alternatively also group them by function.

#### 3.1.8 End of File

Optionally, the following identifier can be appended at the end of a source code file:
**End of file identifier (block comments):**

```c
/*-END OF SOURCE FILE--------------------------------------------------------*/
```

For header or .inl files, this should be avoided, since there is already an end identifier via the "#ifndef ..." - "#endif ..." statements.

### 3.2 Source Code File Layout

Source files, identified by the .c/.cpp extension, contain the implementation of the associated header file.
The source file layout follows the examples below.
**Example of a function-oriented implementation-file (****Doxygen**** block comments style):**

```c
/*-----------------------------------------------------------------------------
 * FunctionTemplate.c       implementation file
 * Copyright                acontis technologies GmbH, Weingarten, Germany
 * Response                 Stefan Zintgraf
 * Description              TODO: Add a module description
 *---------------------------------------------------------------------------*/

/*! \mainpage Ampro Ethernet2 SMC-91c9x Ethernet network interface driver
 *
 * \section intro Introduction
 *
 * This module implements the Ampro Ethernet2 SMC-91c9x Ethernet network interface driver
 */

/** @defgroup FuncGroup1    functions of group 1 */
/** @defgroup FuncGroup2    functions of group 2 */

/*-INCLUDES------------------------------------------------------------------*/
#include "FunctionTemplateBlockComments.h"

/*-DEFINES/MACROS------------------------------------------------------------*/
//...

/*-TYPEDEFS/ENUMS------------------------------------------------------------*/
/** \brief ring buffer element */
typedef struct _LOCAL_RING_ELEM
{
    BOOL        bEmpty;     /**< TRUE if element buffer is empty */
    void*       pBuf;       /**< pointer to element buffer */
} LOCAL_RING_ELEM;

/*-GLOBAL VARIABLE DEFINITIONS-----------------------------------------------*/
/** @addtogroup Settings */
/*@{*/
int G_nGlobalSetting = 0;       /**< this is a global variable used in #globalCFunction() */
/*@}*/
int G_nGlobalVar = 0;           /* this variable is not part of a group */

/*-MODULE VARIABLE DEFINITIONS-----------------------------------------------*/
/** @defgroup SubSettings   sub-settings
  * @ingroup Settings
  */
/*@{*/
static int S_nSubSetting1 = 0;  /**< this is the sub setting 1 */
static int S_nSubSetting2 = 0;  /**< this is the sub setting 2 */
/*@}*/
static int S_nStaticVar = 0;    /* this variable is not part of a group */

/*-MODULE FUNCTION DECLARATIONS----------------------------------------------*/
static STATUS moduleCFunction( );

/*-GLOBAL FUNCTION DEFINITIONS-----------------------------------------------*/

/** @addtogroup FuncGroup1 */
/*@{*/
/*****************************************************************************/
/** \brief short comment
*
* detailed description. This: #moduleCFunction is a link. This: #S_nStaticVar, too!
*
* \return OK or ERROR
*/
STATUS
globalCFunction
(   int      wParam1,                   /**< [in] comment */
    int*     wParam2 )                  /**< [in, out] comment */
{
char chLocal1;  /* first local variable */
WORD wLocal2;   /* second local variable */

    if( wParam1 == wLocal2 )
    {
        chLocal1 = 'A';
    }

}
/*@}*/

/*-MODULE FUNCTION DEFINITIONS-----------------------------------------------*/

/** @addtogroup FuncGroup2 */
/*@{*/
/*****************************************************************************/
/** \brief short comment
*
* detailed description. This: #globalCFunction is a link.
*
* \return OK or ERROR
*/
static STATUS
moduleCFunction
( )
{
char chLocal1;  /* first local variable */
WORD wLocal2;   /* second local variable */

}
/*@}*/

/*-END OF SOURCE FILE--------------------------------------------------------*/
```

**Example of a class-oriented implementation-file (****Doxygen**** block comments style):**

```c
/*-----------------------------------------------------------------------------
 * ClassTemplate.cpp        implementation file
 * Copyright                acontis technologies GmbH, Weingarten, Germany
 * Response                 Stefan Zintgraf
 *---------------------------------------------------------------------------*/

/*-INCLUDES------------------------------------------------------------------*/
#include "stdafx.h"
#include "ModuleNamePrivate.h"
#include "ClassTemplate.h"

/*-DEFINES/MACROS------------------------------------------------------------*/
//...

/*-TYPEDEFS/ENUMS------------------------------------------------------------*/
//...

/*-STATIC CLASS-MEMBERS------------------------------------------------------*/
static int CObjectCPP::m_nDevice = 5;

/*-CLASS-METHODS-------------------------------------------------------------*/

/*****************************************************************************/
/** \brief TODO: add a method-description.
*
* \param nX [in,out] comment
* \param nY [in,out] comment
* \return comment
*/
bool
CObjectCPP::Method
(   int nX,                             /* [in,out] comment */
    int nY )                            /* [in,out] comment */
{
}

/*-END OF SOURCE FILE--------------------------------------------------------*/
```

### 3.3 Header File Layout

Header files, identified by the .h extension, contain definitions of status codes, type definitions, class definitions, function prototypes, and other declarations that are needed by one or more modules (via #include).
No executable code should be in header files, except for template code. Inline code should be placed in the corresponding .inl file.
The following compiler check is to be inserted at the beginning and end of each header file to avoid multiple inclusions:
**Example: (filename: ****func.h****)**

```c
#ifndef INC_FUNC
#define INC_FUNC 1

.........
.........
.........

#endif /* INC_FUNC */
```

**Examples from template files:**
**C-Header with extern "C" (****Doxygen****-Style):**

```c
#ifndef INC_FUNCTIONTEMPLATE
#define INC_FUNCTIONTEMPLATE 1

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/* ... content ... */

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* INC_FUNCTIONTEMPLATE */
```

**C++-Header with #pragma once (optional):**

```c
#if !defined(AFX_DoxygenCppExample_H)
#define AFX_DoxygenCppExample_H

#if _MSC_VER > 1000
#pragma once
#endif /* _MSC_VER > 1000 */

/* ... content ... */

#endif /* !defined(AFX_DoxygenCppExample_H) */
```

The following preprocessor elements should only appear in the code when they are really necessary.
The following compiler check is to be inserted at the beginning of the header file when C includes are not desired:
**Example:**

```c
#ifndef __cplusplus
#error SC: This is a C++ header file, it cannot be used from plain C !
#endif
```

In C header files, the following sequence is additionally to be inserted:
**Example:**

```c
#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */
    ...
#ifdef __cplusplus
}
#endif /* __cplusplus */
```

Header files are to be organized so that the same element types are in the same section.
The source file layout follows the examples below (empty sections should be avoided).
**Example of a function-oriented header-file:**

```c
/*-----------------------------------------------------------------------------
 * FunctionTemplate.h       header file
 * Copyright                acontis technologies GmbH, Weingarten, Germany
 * Response                 Stefan Zintgraf
 * Description              TODO: Add a module description.
 *---------------------------------------------------------------------------*/

#ifndef INC_FUNCTIONTEMPLATE
#define INC_FUNCTIONTEMPLATE

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*-INCLUDES------------------------------------------------------------------*/
#include "MyInclude.h"

/*-DEFINES/MACROS------------------------------------------------------------*/
#define ESMC_BUFSIZE            1536    /**< RX/TX buffer size in task level */

/*-TYPEDEFS/ENUMS------------------------------------------------------------*/

typedef char BOOL;
typedef int STATUS;
typedef unsigned char WORD;

/** \brief ring buffer element. */
typedef struct _GLOBAL_RING_ELEM
{
    BOOL        bEmpty;     /**< TRUE if element buffer is empty */
    void*       pBuf;       /**< pointer to element buffer */
} GLOBAL_RING_ELEM;

/*-GLOBAL VARIABLE DECLARATIONS----------------------------------------------*/

/*-GLOBAL FUNCTION DECLARATIONS----------------------------------------------*/
STATUS globalCFunction( int wParam1, int* wParam2 );

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* INC_FUNCTIONTEMPLATE */
```

**Example of a class-oriented header-file (****Doxygen**** block comments style):**

```c
/*-----------------------------------------------------------------------------
 * ClassTemplate.h          header file
 * Copyright                acontis technologies GmbH, Weingarten, Germany
 * Response                 Stefan Zintgraf
 *---------------------------------------------------------------------------*/

#ifndef INC_CLASSTEMPLATE
#define INC_CLASSTEMPLATE

/*-INCLUDES------------------------------------------------------------------*/
//...

/*-DEFINES/MACROS------------------------------------------------------------*/
//...

/*-TYPEDEFS/ENUMS------------------------------------------------------------*/
//...

/*****************************************************************************/
/** \brief TODO: add a class-description.
 */
class CObjectCPP: public CObject
{

/*-FRIEND-CLASSES------------------------------------------------------------*/
public:
protected:
private:

/*-MACROS--------------------------------------------------------------------*/
public:
protected:
private:

/*-DEFINITIONS/ENUMERATIONS--------------------------------------------------*/
public:
protected:
private:

/*-EMBEDDED CLASSES----------------------------------------------------------*/
public:
protected:
private:

/*-CONSTRUCTORS/DESTRUCTORS-------------------------------------------------*/
public:
protected:
private:

/*-ATTRIBUTES----------------------------------------------------------------*/
public:
protected:
private:
    static int m_nDevice;      /**< device number */

/*-METHODS-------------------------------------------------------------------*/
public:
protected:
private:
    bool Method( int nX, int nY );     /**< method description */

};

#endif /* INC_CLASSTEMPLATE */
```

## 4 CODING STYLE

The following guidelines serve to increase readability and give the source code a uniform appearance.

### 4.1 Spacing

#### 4.1.1 Horizontal Spacing

Spaces are to be set:
- before and after binary operators
- after commas
- after an opening round parenthesis and before a closing one (this is an acontis-specific convention that improves readability in complex expressions, though it differs from some industry standards like K&R or Google C++ Style)
- before the end of a comment block (*/)
- after colons (conditional, bit-field-members)
- after semicolons
- beginning of a block comment
- beginning of a line comment
Spaces must not be inserted:
- when accessing structure elements
- in pointer operations
- in scope selectors
- when accessing array elements
**Examples:**

```c
x = y * z;
nError = RTWCall( arg1, arg2, arg3 );
oMsp.strShortname
pWnd->ShowWindow( SW_SHOW );
aReadBuffer[4]
CDrvCursor::Desc oDesc;
```

If a statement extends over multiple lines, lines 2 through n are to be aligned with the first:
**Example:**

```c
bWholeWeekFree = bFreeOnMonday & bFreeOnTuesday & bFreeOnWednesday
                 & bFreeOnThursday & bFreeOnFriday;
```

#### 4.1.2 Vertical Spacing

Blank lines should be used to make the code more organized and to group logically related sections together.
**No more than one consecutive empty line should be used.**
A blank line is to be inserted before a comment line.
Each statement gets a new line (exception: for loop).
Curly braces and case labels always have their own line.
The if statement is no exception: the statements to be executed after the condition are to be written on separate lines.
After keywords (if, for, case, ...) the bracket expressions are always to be set in separate lines. The following block is to be indented.
**Block Formatting:**
Blocks with `{ }` get a line for each parenthesis plus lines for the actual code in the block:
**Good:**

```c
if( nCount > nMax )
{
    nCount = nMax;
}
```

**Bad:**

```c
if( nCount > nMax ) {
    nCount = nMax;
}
```

**Bad:**

```c
if( nCount > nMax )    {
    nCount = nMax;  }
```

**Example:**

```c
if( nCount > nMax )
{
    nCount = nMax;
}
```

If a compound statement extends over many code lines, the closing brace should be commented.
**Example:**

```c
if( nStatus != ERROR )
{
    /* many lines... */
    ...;
    ...;
} /* nStatus != ERROR */
```

Between logical sections (method definition, include block, file header, ...) a spacing of 2 blank lines must be maintained.

### 4.2 Indentation

Each indentation level corresponds to four characters. The module, method headings, and method declarations begin in column one.
Tabs are not allowed in source code. It should be possible to read the source code in any editor without editing the tab settings. The respective development environment is to be adjusted accordingly.
The following statements are indented:
- Declarations of class members
- Conditional statements
- Loops
- switch statements
- case labels
- Structure definitions in a typedef
**Constants in Comparisons:**
Constants go in front in an `==` or `!=` comparison (Yoda conditions):
**Good:**

```c
if( NULL == pAdapter )
{
    …
}
```

**Bad:**

```c
if( pAdapter == NULL )
{
    …
}
```

**Rationale:** Prevents accidental assignment (`=` instead of `==`) and makes null pointer checks more obvious.
**Special rule for C functions:** Local variables in C functions are declared directly after the opening brace without additional indentation, aligned to the column of the opening brace.
**Example:**

```c
STATUS
globalCFunction
(   int      wParam1,
    int *    wParam2 )
{
char chLocal1;  /* first local variable */
WORD wLocal2;   /* second local variable */

    if( wParam1 == wLocal2 )
    {
        chLocal1 = 'A';
    }
}
```

The else statement of an if statement stands in the same column as the associated if statement:
**Example:**

```c
if( !bDrunkTooMuch )
{
    GoToWork( );
}
else
{
    StayAtHome( );
}
```

The form of an if statement with an else if statement looks as follows:
**Example:**

```c
if( bUseWindows )
{
    InitializeWindowsSubsystem( );
}
else if( bUseLinux )
{
    InitializeLinuxSubsystem( );
}
else
{
    UseDefaultSubsystem( );
}
```

The general form of a switch statement is:
**Example:**

```c
switch( nDayLeftToWeekend )
{
case 5:
    FeelHappy( dwNotAtAll );
    break;
case 1:
    FeelHappy( dwABit );
    break;
case 0:
    FeelHappy( dwVeryMuch );
    break;
default:
    ASSERT( 0 );
    break;
}
```

If the action is very short and almost identical in all cases, an alternative form of the switch statement is acceptable.
**Example:**

```c
switch( nDayLeftToWeekend )
{
case 5: nFeelState = dwNotAtAll; break;
case 1: nFeelState = dwABit; break;
case 0: nFeelState = dwVeryMuch; break;
default: nFeelState = dwNotAtAll; break;
}
FeelHappy( nFeelState );
```

For case bodies containing multiple statements or complex logic, braces can be used to create a block scope:
**Example:**

```c
switch( dwCode )
{
case EC_LINKIOCTL_GET_ETHERNET_ADDRESS:
{
    if ((EC_NULL == pbyOutBuf) || (dwOutBufSize < ETHERNET_ADDRESS_LEN))
    {
        dwRetVal = EC_E_INVALIDPARM;
        goto Exit;
    }

    dwRes = EcLinkGetEthernetAddress(pAdapter, (EC_T_BYTE*)pbyOutBuf);
    if (EC_E_NOERROR != dwRes)
    {
        dwRetVal = dwRes;
        goto Exit;
    }
    dwNumOutData = ETHERNET_ADDRESS_LEN;
} break;

default:
{
    dwRetVal = EC_E_NOTSUPPORTED;
    goto Exit;
} /* no break */
}
```

**Rationale:** Braces in case blocks provide block scope for local variables and improve code organization for complex case bodies.
If the break command is omitted, this should be mentioned in a short comment.
The form of loop constructs looks as follows:
**Example:**

```c
for( int nBeer = 0; nBeer < 10 ; nBeer++ )
{
    DrinkIt( nBeer );
}

while( bHungry )
{
    bHungry = EatASteak( );
}

do
{
    bHardDiskFull = InstallSoftwareProduct( );
}
while( !bHardDiskFull );
```

### 4.3 Comments

**IMPORTANT: File headers and function comments use ****Doxygen****-Style block comments:**
All file headers, function descriptions, and documentation comments use Doxygen-style block comments (`/* */`), not line comments (`//`).
**Example (file header):**

```c
/*-----------------------------------------------------------------------------
 * FunctionTemplate.c       implementation file
 * Copyright                acontis technologies GmbH, Weingarten, Germany
 * Response                 Stefan Zintgraf
 * Description              TODO: Add a module description
 *---------------------------------------------------------------------------*/
```

**Example (function comment):**

```c
/*****************************************************************************/
/** \brief short comment
*
* detailed description. This: #moduleCFunction is a link.
*
* \param wParam1 [in] comment
* \param wParam2 [in,out] comment
* \return OK or ERROR
*/
STATUS
globalCFunction
(   int      wParam1,                   /**< [in] comment */
    int*     wParam2 )                  /**< [in, out] comment */
```

Comments in code should precede the code to which they belong and be indented equally. A blank line should always precede comments.
In-line comments should look as follows:
**Example:**

```c
......................;                 // line-comment.
....................;                   // .................
........................;               // ................
......................;                 /* block-comment... */
....................;                   /* ....................  */
........................;               /* .................   */
```

This type of commenting is used to enable, for example, variable usage or a short description of statements. The distance between a statement and the following comment must be at least 3 spaces. Comments over multiple lines should always start in the same column.
In-line comments over multiple lines should be avoided. If required, they should look as follows:
**Example:**

```c
....................;               /* .................
                                     * .............
                                     * ...................
                                     */
```

`#ifdef/#endif` constructs are to be commented at the end:
**Example:**

```c
#ifndef _ASMLANGUAGE
    ....;
    ....; /* many lines... */
    ....;
#endif  /* _ASMLANGUAGE */
```

#### 4.3.1 Content of Comments

Comments are explanations of the respective code sequences. The more the sequences are written in a self-documenting manner, the less a comment is required. In stylistically well-written programs, comments are the "icing on the readability cake".
Comments must always be kept current. They can be divided into the following classes:
**Repetition of program code:**
A repetitive comment says again what the program code does, this time however in other words. One has - except for more reading material - no advantages through these comments.
**Explanation of program code:**
Explanatory comments are normally used at complicated, tangled, and sensitive program points. In these situations they are useful, but mostly only because the program code itself is confusing. If this is the case, the program code should be improved instead of explaining it.
**Summary of the program:**
A summary comment draws the essence from a few lines of source code in a few words. These comments are much more useful than the repetitive ones, since they allow the source code to be quickly searched. They are especially used when someone other than the original author wants to modify the program.
**Explanation of intent:**
This comment explains what the developer intends with the following program section. These comments are more related to the problem than to its solution.
So, for example,

```c
/* start data acquisition */
```

is an intent-explaining comment, while

```c
/* read remote-server-name from database */
```

is a summary comment of the problem solution.
The only two types of comments that come into question for a finished program are the summary and the statement of intent.

#### 4.3.2 Doxygen Documentation

Doxygen can be used for automatic documentation generation. The following Doxygen comment styles are used in the template files:
**Block comments for functions:**

```c
/** \brief short comment
*
* detailed description. This: #moduleCFunction is a link. This: #S_nStaticVar, too!
*
* \return OK or ERROR
*/
STATUS
globalCFunction
(   int      wParam1,                   /**< [in] comment */
    int*     wParam2 )                  /**< [in, out] comment */
```

**Inline comments for variables and structure members:**

```c
int G_nGlobalSetting = 0;       /**< this is a global variable used in #globalCFunction() */

typedef struct _GLOBAL_RING_ELEM
{
    BOOL        bEmpty;     /**< TRUE if element buffer is empty */
    void*       pBuf;       /**< pointer to element buffer */
} GLOBAL_RING_ELEM;
```

**Doxygen**** grouping:**

```c
/** @defgroup FuncGroup1    functions of group 1 */
/** @defgroup FuncGroup2    functions of group 2 */

/** @addtogroup FuncGroup1 */
/*@{*/
STATUS globalCFunction(...);
/*@}*/
```

**Doxygen**** for macros:**

```c
#define ESMC_BUFSIZE            1536    /**< RX/TX buffer size in task level */
```

**Doxygen**** for classes (C++):**

```c
/*!
 *  \author Gunnar Trost
 *  \version 2.0
 *  \date 01.10.2004 - Created
 *  \brief Here is some text that briefly describes the class.
 */
class CDoxygenCppExample
{
    /// A simple variable description
    CSimpleVariable m_SimpleVariable;

    /// This is an example of a function description
    void run(void);
};
```

**Doxygen**** for C++ methods:**

```c
/*!
    The BRIEF symbol is normally not needed because the comment in the header is automatically
    considered as a summary / brief description.
 */
CDoxygenCppExample::~CDoxygenCppExample()
{
}
```

#### 4.3.3 Comments During Development Phase

During development, it often happens that special code sequences should be marked in some form so that they can be easily found again later (e.g., using "Find in Files").
- Markings that are only inserted for implementation purposes use the abbreviation `TODO_USER`.
- Markings that, for example, should comment on issues that will not be fixed in the short term use the abbreviation `TOOPTIMIZE`.
**Example:**

```c
#ifdef _DEBUG
    bShow = ScGetApp( )->GetRegInt( REG_GET_DEBSHOWDRVSTART );
#else
    /* TODO_HGs -> only temporary until the autostart-mechanism is implemented */
    bShow = ScGetApp( )->GetProfileInt( "Driver", "bShowDrvStart", true );
#endif

/* TOOPTIMIZE: ODBC doesn't work with exactly 255 WHERE-clauses */
if( oIdInputValueArr.GetSize() & 0x000000FF )
{
    oStrAdd.Format( " OR (IdInputValue=0)" );
    oStrSelect += oStrAdd;
}
```

#### 4.3.4 Comment Style Consistency

The document uses multiple comment styles. Follow these guidelines for consistency:
**Block comments (mandatory for):**
- File headers (Doxygen-style)
- Function/method documentation (Doxygen-style)
- Section headers (`/*-SECTION NAME---*/`)
- Multi-line explanatory comments
**Inline comments (may be used for):**
- Brief variable or member documentation: `/**< description */` (Doxygen)
- End-of-line explanations: `// comment` or `/* comment */`
- Parameter documentation in function signatures
**Guidelines:**
- C++ files may use `//` for inline comments
- C files should use `/* */` for all comments
- Always use block comment style (`/* */`) for Doxygen documentation
- Be consistent within a file - don't mix styles unnecessarily
**Note on Project-Specific Restrictions:**
Some projects may have specific requirements that restrict the use of `//` comments due to compiler compatibility or other project-specific constraints. In such cases, projects should document their specific comment style requirements. For example, some embedded projects may require `/* */` comments exclusively due to compiler limitations.
**Example:**

```c
/* Block comment for file header and functions */
/** \brief Doxygen block comment for documentation */
int nValue;     /**< Doxygen inline comment for members */
nValue++;       // Simple inline comment (C++ only)
nValue++;       /* Simple inline comment (C and C++) */
```

## 5 GENERAL PROGRAMMING GUIDELINES

### 5.1 Mandatory Guidelines

#### 5.1.1 General

- Empty statements like `;` and `};` are to be avoided.
- Lengths of data fields must not be explicitly declared, but are to be calculated by the compiler using `sizeof()`.
- For type conversion, the cast operator is to be used. If the compiler supports RTTI (Runtime Type Information), the _cast operators are to be used (dynamic_cast, static_cast, ...).
- Access to data must be independent of the physical size and compiler alignment.
- For each switch statement, a default label is to be provided, regardless of whether it can occur or not. This reveals programming errors (using `ASSERT( 0 )` in the default label).
- All data that originates outside the module (for example network packets, files, user input, shared memory, environment variables) must be treated as untrusted and validated for type, length, range, and format before use. Return values of parsing and conversion functions must always be checked and handled.
- Secret data such as passwords, cryptographic keys, authentication tokens, or personally identifiable information must never be written to debug output or log files in plain text and must not be left in memory longer than necessary. If specific secure storage or wiping primitives are available in the project, they must be used.
- New or changed code must not deliberately introduce known exploitable vulnerabilities (for example by using banned APIs, disabling compiler security features, or introducing dependencies with unresolved high-severity CVEs) without an approved risk acceptance according to the project process.

#### 5.1.4 Class Design

##### 5.1.4.1 No Malloc in Constructors

Since exceptions may not be available in some environments, the constructor cannot report errors. Instead, `InitInstance()` should be used for memory allocation. If memory runs out, `InitInstance` should report an appropriate error code.
**Rationale:** Some embedded or legacy environments may not support C++ exceptions.
- The order of processing of function parameters must not have any effect on the program flow. If a certain order is desired, then this must be clearly made through intermediate steps. In one line, a variable may only be either modified or used.
**Example:**

```c
FuncDoNothing( x * i, y / i, i++ );     // incorrect

FuncDoNothing( x * i, y / i, i );       // correct
i++;
```

- Access to imported function prototypes, constants, type definitions, etc. must be through inclusion of the appropriate .h file. Redefining them (e.g., with extern) is not allowed.
- To test the validity of a pointer, the constant `NULL` is to be used, not the number 0.
- Macros must not be used to define data types. For this, the keyword `typedef` is to be used.
- At the highest warning level, no compiler warnings may be output in the Release build. Non-sensical compiler warnings should be suppressed in the private module header file.
- In projects that support multiple languages, all text outputs that appear at the interface are to be placed in the string table of the resource file.
- In projects that read from or write values to the registry areas HKEY_CURRENT_USER and HKEY_LOCAL_MACHINE, this is to be realized through the methods GetRegInt / GetRegString / WriteRegInt / WriteRegString.
- In the ASSERT & TRACE macros, no functions may be called, since these are removed by the preprocessor in the Release configuration.
- For complex code sequences, parentheses should also be used when they are not required - to improve code readability. This avoids errors that arise from misunderstood operator precedence.

#### 5.1.2 Variables

- All member variables of a class are to be initialized in the constructor.
- Local (auto) variables must never be used uninitialized.
- Variables have to be declared at top of function and initialized:
**Good:**

```c
DWORD CInterface::ConfigureNetwork(
    CNF_TYPE eCnfType,
    BYTE*    pbyCnfData,
    DWORD    dwCnfDataLen
)
{
    DWORD  dwRetVal = ERROR;
    DWORD  dwRes    = 0;
    BOOL   bJobDisabled = FALSE;
    switch (eCnfType)
    {
        ….
    }
}
```

**Bad:**

```c
DWORD CInterface::ConfigureNetwork(...)
{
    DWORD  dwRetVal = ERROR;
    DWORD  dwRes    = 0;
    switch (eCnfType)
    {
        ….
    }
    BOOL   bJobDisabled = FALSE;  /* Wrong: declared after switch */
}
```

**Note:** This requirement may conflict with C99/C++ ability to declare variables anywhere. For projects requiring C99/C++ compatibility, this should be treated as a recommendation rather than a strict requirement.

#### 5.1.3 Functions

- Objects, structures, and unions are always to be passed as pointers or references.
- Objects, structures, and unions that are changed and returned in functions are always to be passed as pointers (not as references, never as values).
- Objects, structures, and unions as return values are to be returned as values. If the return value is guaranteed to exist at runtime, a const pointer can also be returned.
- Objects, structures, and unions that are only read are always to be passed using const/const reference.
- If a function's return value is never used anyway, it is to be declared as a void function.
- In C, module-related functions and data are to be declared as static.

### 5.2 Recommendations

#### 5.2.1 Language of Source Text and Comments

Variable designations, function and class names, as well as comments should be provided with English designations. If it cannot be avoided, German can also be used.

#### 5.2.2 General

- Instead of macros with parameters, inline functions should be used.
- Macros should only be used when there is no appropriate alternative.
- Macros should not be used to define constants. For this, the keyword enum or const is to be used.
- The use of goto statements should be avoided. As an exception routine, try...catch should be used. If required, gotos should be clearly commented. As an alternative to exceptions, the FATAL_EXIT macro can be used in C, which internally uses the goto command.
- Functions must clean up resources if they fail. Use the `goto Exit` pattern to ensure cleanup code is executed (see section 5.2.6.2 for error handling pattern).
- friend statements in a class definition should be avoided.
- If the same index addresses two or more data elements, this should be combined in a structure.
**Example:**

```c
int nIdxShortName;
int nIdxDesc;

/* avoid this: */
nIdxDesc = 3;
nIdxShortname = 3;

CString strDesc = oDescArr[nIdxDesc];
CString strShortName = oShortNameArr[nIdxShortName];

/* use this: */
int nIndex = 3;

SDevice sDev = oDeviceArr[nIndex];
CString strShortName = sDev.strShortName;
CString strDesc = sDev.strDesc;
```

- Loop variables should not be modified in the middle of the loop. Otherwise it is harder to find the loop control sequence and under certain circumstances the exit condition can then be overlooked.
- Code tuning: The implementation of a code sequence should always be oriented toward the main goals of modularity and performance. Highly optimized code sequences should only be used when they are really required in that form. The same applies to code that should require particularly little memory.
- Special cases should - if possible - not be solved with an if statement if the algorithm can be modified accordingly. Special cases to be handled should not lie hidden in the code but should be realized through isolated program parts.
- If possible, one should avoid calling functions that return error codes, since these must always be evaluated.
- The `?:` operator should be avoided.
- Memory of other subsystems should not be accessed directly.
- Allocating and freeing resources: Calls to allocate and free resources (memory, synchronization objects, ...) belong together in pairs. There is only one call to allocate and one call to free the resource.

#### 5.2.7 Design Patterns

##### 5.2.7.1 Threads

Thread header:

```c
#include "EcThread.h"
```

Keep call stack as small as possible. See also: "threadProc is run in separate thread and calls listenStep while thread is not stopped".
**Rationale:** Embedded systems and some applications have limited stack space.
**Example:**

```c
EC_T_VOID InterruptServiceThreadEntry(EC_T_VOID* pvContext)
{
    CEcRemoteLinkLayer* pAdapter = (CEcRemoteLinkLayer*)pvContext;
```

```c
    /* check parameters */
    if (EC_NULL == pAdapter)
    {
        return;
    }
    /* wait for any frame */
    OsWaitForEvent(pAdapter->m_oLinkDesc.pvFrameRecvEvent, EC_WAITINFINITE);
```

```c
    /* process all stored frames */
    {
        EC_T_LINK_FRAMEDESC oFrameDesc;
        OsLock(pAdapter->m_poLock);
        while (pAdapter->m_oFramePool.GetPendingFrame(oFrameDesc))
        {
            EC_T_BOOL bProcessed = EC_FALSE;
            OsUnlock(pAdapter->m_poLock);
```

```c
            /* call receive callback */
            pAdapter->pfReceiveFrameCallback(pvCallbackContext, …);
```

```c
            /* free frame */
            OsLock(pAdapter->m_poLock);
            EcLinkFreeRecvFrame(pAdapter, &oFrameDesc);
        }
        OsUnlock(pAdapter->m_poLock);
    }
}
```

##### 5.2.7.1 Locks

Thread header:

```c
#include "EcLock.h"
```

Keep lock as short as possible. Ensure to return lock in case of error. “bLocked” helps for the decision at the end of a long function:

```c
EC_T_DWORD CEcMasterRasConnection::TransmitRequest(
    EC_T_DWORD  dwOutSize,      /**< [in]       Size of Data to transmit */
    EC_T_PBYTE  pbyOutData,     /**< [in]       Data pointer (Header+Data) */
    EC_T_DWORD* pdwInSize,      /**< [in, out]  Size of Receive Buffer / received data */
    EC_T_PBYTE  pbyInData,      /**< [in]       Receive buffer */ ...)
{
…
    EC_T_BOOL bLocked = EC_FALSE;
```

```c
    if ((EC_NULL == pbyOutData) || (0 == dwOutSize))
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "CEcMasterRasConnection::TransmitRequest: if( (EC_NULL == pbyOutData) || (0 == dwOutSize) ) goto Exit, 0x%x\n", EC_E_INVALIDPARM));
        dwRetVal = EC_E_INVALIDPARM;
        goto Exit;
    }
```

```c
    m_oSockLock.Lock();
    bLocked = EC_TRUE;
```

```c
...
```

```c
    dwRetVal = EC_E_NOERROR;
Exit:
    if (bLocked)
    {
        m_oSockLock.UnLock();
    }
```

```c
    return dwRetVal;
}
```

##### 5.2.7.1 No exeptions, return code handling

- For all functions that can return errors, this error should be passed through to the highest function in the function hierarchy so that every error that occurs can be exactly localized.

#### 5.2.3 Formatting

- The recommended maximum length of a line is 100 characters.
- Multi-line statements promote readability.
- A block should be at most 2-3 screen pages long. Longer blocks should - if possible - be meaningfully divided into sub-functions.
- For empty statements, e.g., `else {}`, `case : break;` it should be meaningfully commented why these are empty.

#### 5.2.4 Code Extensions in Debug Configuration

As many ASSERT checks as possible should be built in so that any programming errors can be detected in the Debug configuration.
- Function parameters should be secured with ASSERT.
- The validity of assumptions should be secured with ASSERT (e.g., the value range of variables).
- Defensive programming must not lead to hidden errors (no self-healing); these errors should be detected by ASSERTs.
- ASSERT checks should be intuitively understandable; if necessary, a comment is required so that it is understood what is to be checked.
- Critical algorithms where speed matters should be checked in the Debug version through a slower but safer implementation of the algorithm.
- Debug statements should be avoided in released code. To suppress debug output, `#ifdef _DEBUG` should be checked.

##### 5.2.4.1 Memory Checks

- In the Debug version of the software, allocated memory should be initialized with special values (e.g., 0xbeefcafe).
- In the Debug version of the software, memory should be overwritten before freeing (e.g., with 0xfeedc0de)

#### 5.2.5 Variables

- As a status variable within a function, "bOk" is suitable.
- Alternatively, `dwRetVal` and `dwRes` (with `NOERROR` and `ERROR`) can be used, especially in complex functions or APIs (see section [5.2.6.2](#5262-error-handling-pattern-dwretval-and-dwres)).
- char variables should only be used for storing characters/letters. Otherwise, appropriate data types (BYTE) are to be used.
- Global variables should not be used, except in special exceptions (and even then the use of the variable should only be in one module of a larger application).
- If possible, the data type bool should be used for boolean variables.
- Right-shift (>>) or left-shift (<<) operators should not be applied to signed variables, as these can be executed differently depending on the machine. Also, shift operators should not be used as dividers or multipliers.
- Non-boolean variables should not be checked for boolean values (and vice versa).
**Example:**

```c
int x;
CORRECT:    if( x == 0 )
INCORRECT:  if( ! x )

bool bOk;
CORRECT:    if( bOk )
INCORRECT:  if( bOk == TRUE )
INCORRECT:  if( bOk == 0 )
```

- Data should never be passed through global or static variables.
- Expressions or variables should never overflow or underflow.

#### 5.2.6 Functions

- To get access to global functions, scope operators (::) should always be used in C++.
- Routines that return a status value should return either "OK" or an error code that does not correspond to "OK".
- The return statement should only be present at one point in the subroutine, except when the routine is aborted due to an error. If system resources are needed (for example memory), these should be freed again before the return.
- A function should have only one task. Multi-function interfaces should be avoided.
- Each function parameter represents only one data type (-> robust interfaces).
- Instead of special values for error codes (e.g., -1, NULL), status values should be used as return values (e.g., bool bOk).
- Function parameters should be self-explanatory through their naming (enum values are, for example, better than TRUE/FALSE values).
- Functions should - if possible - not return error codes; this makes them easier to use (e.g., `void DeInit()`).

##### 5.2.6.1 Error Handling Strategy

Error handling recommendations depend on the context. Use the following decision priority:
**1. For C++ code:**
- Prefer exceptions (try...catch) for exceptional error conditions
- Use `bool` return values for expected success/failure operations
- Use `void` for operations that cannot fail
**2. For C code or C++ interfaces to C code:**
- Use STATUS return codes (OK or specific error codes)
- For C, use the `FATAL_EXIT` macro pattern for cleanup on error (see section 5.2.2)
- Ensure all error codes are documented and consistently checked
**3. For legacy API compatibility:**
- Maintain existing error handling patterns for consistency
- Document any deviations from modern practices
**General principle:** Functions that can fail should communicate this clearly through their signature. Avoid silent failures or functions that appear infallible but can fail.

##### 5.2.6.2 Error Handling Pattern: dwRetVal and dwRes

For functions that return error codes, use a consistent error handling pattern:
- Use `dwRes` for the result of a function call
- Use `dwRetVal` for the return value of the current function
**Example:**

```c
DWORD CInterface::SetParms(INIT_PARMS* pParms)
{
    DWORD dwRetVal = ERROR;
    DWORD dwRes    = ERROR;

    /* check if parameters are OK */
    dwRes = CheckParms(pParms);
    if (NOERROR != dwRes)
    {
        dwRetVal = dwRes;
        goto Exit;
    }
    …
Exit:
    return dwRetVal;
}
```

**Rationale:** This pattern ensures consistent error propagation and makes error handling explicit throughout the codebase. The `goto Exit` pattern ensures cleanup code is executed even when errors occur.

### 5.3 Modern C++ Guidelines (C++11 and Later)

**Note:** This document primarily targets C++98/03. The following guidelines apply when using C++11 or later features in new code.

#### 5.3.1 Null Pointers

- Use `nullptr` instead of `NULL` or `0` for null pointers in C++11 and later
- `NULL` may still be used in C code or for compatibility with C APIs
**Example:**

```c
void* pData = nullptr;  // C++11 and later
void* pData = NULL;     // C or C++98 compatibility
```

#### 5.3.2 Type Inference

- Use `auto` for type inference when the type is obvious from the initializer or when it improves readability
- Do not overuse `auto` when explicit types improve code clarity
**Example:**

```c
auto it = mapData.begin();              // Good: iterator type is verbose
auto pDevice = new CDevice();           // Acceptable
int nCount = 10;                        // Better: simple type is clear
```

#### 5.3.3 Smart Pointers

- Prefer smart pointers (`std::unique_ptr`, `std::shared_ptr`) over raw pointers for ownership management
- Use raw pointers only for non-owning references
- Document ownership semantics clearly when mixing smart and raw pointers
**Example:**

```c
std::unique_ptr<CDevice> pDevice = std::make_unique<CDevice>();
CDevice* pReference = pDevice.get();  // Non-owning reference
```

#### 5.3.4 Range-Based For Loops

- Use range-based for loops when iterating over containers
- Use `const auto&` for read-only iteration to avoid copies
**Example:**

```c
for( const auto& item : vecItems )
{
    ProcessItem( item );
}
```

#### 5.3.5 Move Semantics

- Implement move constructors and move assignment operators for classes that manage resources
- Use `std::move()` when transferring ownership of resources
- Follow the Rule of Five (destructor, copy constructor, copy assignment, move constructor, move assignment) or Rule of Zero

### 5.4 Security-by-Design and Cyber Resilience Act (CRA)

This section describes additional coding requirements that support compliance with the EU Cyber Resilience Act (CRA, Regulation (EU) 2024/2847) for products with digital elements. It focuses on software design and implementation aspects and complements the general guidelines in Sections 5.1–5.3 and the EC-Embedded development workflow (AT5010). Non-technical obligations such as CE marking, vulnerability reporting and PSIRT processes are defined in separate process documents.

#### 5.4.1 General Principles

- Security must be considered from the start of design and throughout the whole lifecycle of the product. Code changes must preserve or improve the security posture of existing modules; “quick fixes” that weaken security are not acceptable.
- All modules that process data from outside the process (for example network, fieldbus, files, IPC, user input, configuration) must be designed under the assumption that this data is malicious until proven otherwise.
- New code must be written such that the product can be shipped without known exploitable vulnerabilities and with secure default settings. See also the mandatory guidelines in Section 5.1.1.

#### 5.4.2 Input Validation and Attack Surface Reduction

- Public interfaces (APIs, protocol handlers, parsers) must validate all inputs for type, range, length and consistency before use. Invalid input must be rejected with a defined error code; it must never cause undefined behaviour, buffer overflows, unbounded memory consumption or uncontrolled recursion.
- Input-dependent loops must be bounded so that malformed data cannot cause unbounded CPU or memory usage.
- Only the minimal set of interfaces that are required for the intended use case may be implemented and enabled. Debug or test-only interfaces must be disabled or removed in production builds.
- Dangerous or obsolete functionality (for example weak cryptographic algorithms or legacy protocol variants) must not be enabled by default. If they must exist for backwards compatibility, they have to be explicitly switched on and clearly documented.

#### 5.4.3 Authentication, Authorisation and Access Control

- Access checks (authentication and authorisation) must be performed before executing any operation that changes state or exposes non-public data.
- Access control decisions must be enforced in a single, well-defined place per subsystem (for example a centralised check function) and must not be bypassed locally for performance or convenience.
- All failed authentication and authorisation attempts must be logged at an appropriate log level without leaking secrets (see Section 5.4.5).

#### 5.4.4 Cryptography and Secrets Handling

- Only approved and well-reviewed cryptographic libraries may be used. Self-written cryptographic algorithms or protocol implementations are not allowed without explicit approval.
- Keys, passwords, tokens and other secrets must be stored and processed using the project-specific abstractions for secure storage and memory handling where available.
- Secrets and other sensitive data must never appear in log output, formatted error messages, protocol traces or core dumps in plain text. If logging cannot be avoided, data must be redacted or irreversibly masked.

#### 5.4.5 Error Handling, Logging and Traceability

- Error paths must be implemented so that they do not leak sensitive information such as keys, passwords, internal memory addresses or full stack traces in customer-visible messages.
- For security-relevant events (authentication failures, configuration changes, denied operations, protocol violations) the code must generate log entries that include at least timestamp, module, event type and a stable identifier for the affected object or connection.
- Each software component must provide a version identifier (for example build number, Git hash or semantic version) that can be retrieved at runtime and logged. This is required to support incident response and vulnerability management.

#### 5.4.6 Updates, Dependencies and Vulnerability Handling

- Update mechanisms must verify the integrity and authenticity of update packages (for example via digital signatures) before installing them. Updates must be applied in an atomic way so that a failed update does not leave the system in an unusable or insecure state.
- Third-party dependencies (libraries, tools, code generators) must be declared in the project-specific dependency management or SBOM artefacts as defined by the project. Ad-hoc inclusion of external source code without traceability is not allowed.
- Known vulnerabilities in own code or third-party dependencies must be addressed without undue delay. When a vulnerability cannot be fixed immediately, a temporary mitigation must be implemented and documented according to the project’s vulnerability handling process.
These rules are mandatory for all new code and for significant changes to existing code in products that fall under the CRA. For existing modules, compliance with this section must be evaluated during refactoring and major feature work.

## 6 APPENDIX

### 6.1 Terms/Abbreviations

- **VxWorks:** Real-time operating system from WindRiver
- **Win95:** Operating system MS Windows 95 *(legacy reference)*
- **DAU:** Dumbest Assumable User
- **MDI:** Multi Document Interface
- **MFC:** Microsoft Foundation Classes
- **MS:** Microsoft
- **MSVC:** Microsoft Visual C++
- **SDI:** Single Document Interface
- **SC:** Software Components
- **COM:** Component Object Model *(legacy technology, primarily for Windows compatibility)*

### 6.2 Base Documents

| No. | Title/Version | Author | Date | Source |
|------|------|------|------|------|
|  | Code Complete | McConnell, Steve | 1993 | Microsoft Press |
|  | The C++ Programming Language | Stroustrup, Bjarne | 1992 | Addison-Wesley-Verlag |
|  | Programming in C | Kernighan, Brian & Ritchie, Dennis | 1990 | Hanser-Verlag |
|  | Writing Solid Code | Steve Maguire | 1993 | Microsoft Press |
|  | Cyber Resilience Act (CRA) – Regulation (EU) 2024/2847, Annex I | European Parliament & Council | 2024 | EUR-Lex / European Commission |

## 7 EC-EMBEDDED SPECIFIC CODING CONVENTIONS

This section contains coding conventions that are specific to the EC-Embedded software products (EC-Master, EC-Monitor, EC-Simulator). These conventions enhance and, in some cases, override the base coding conventions in this document.
**Source:** AT5010_EC-Embedded-Development-Workflow
**Document No.:** AT5010
**Workflow Revision No.:** 5

### 7.1 EC-Embedded Repository Directory Structure

The source code repository is structured as follows:

| Path | Description |
|------|------|
| Bin\<OS>\<Arch>\[Release|Protected|…] | Runtime Binaries (.exe, .dll) |
| Build\00_BuildProgram | Build Program |
| Build\60_SetupOutput | Product installation packages from Build |
| SDK\INC | SDK Header |
| SDK\LIB | SDK Libraries |
| Doc | Documentation |
| Sources\[EcMaster|EcSimulator|…] | Product source code |
| Tests | Test Data, Test Source Code and Test Scripts |
| Workspace\<OS-IDE> | Project files for Visual Studio/Eclipse,cmake |

### 7.2 EC-Embedded Products

acontis EC-Embedded is made up of different products:
- EC-EAP
- EC-Master
- EC-Monitor
- EC-Simulator
- Real-Time Ethernet Drivers
- …

### 7.3 EC-Embedded Components

Each acontis EC-Embedded product (EC-EAP, EC-Master, EC-Monitor, EC-Simulator, …) is structured in components:
- Core (EcMaster.dll, EcSimulator.dll, …)
- RAS Server and Clients (EcMasterRasServer.dll, …)
- Example programs (EcMasterDemo.exe)
The components contain source files, documentation and generated files. The generated files (DLLs, .exe files) are created mostly created using the Jenkins Build Servers as described in the development workflow AT5010.
The products may contain other products like the acontis Real-Time Ethernet Drivers (emllIntelGbe.dll, …).
From a organizational perspective, the definition of the modules is typically done by the product owners.
There is a large shared code basis between similar components (emllIntelGbe, emllI8254x, …) or even same components that only slightly differ like the EcMasterRasServer and the EcSimulatorRasServer.

### 7.4 EC-Embedded Source Code location

Location for Source Code:
- Doc\<Product>\Snippets: Example source code included in documentation
- Examples: Source code of example programs
- SDK\INC: public interface header files
- Sources\<Product>: Source code of product’s core library
- Sources\<Component>: Source code of other product’s components like RAS
- Sources\Common: Source code that has no clear primary relation to any product or component and is rather used at all components

### 7.5 EC-Embedded Spacing

#### 7.5.1 Horizontal Spacing

Spaces width is 4, not tabs. Spaces are to be set:
- before and after binary operators
- after commas
- before an opening round parenthesis and after a closing one
- after start of a comment block and before the end of a comment block (/* my text */)
- after colons (conditional, bit-field-members)
- after semicolons
- block comments are used instead of line comment
Spaces must not be inserted:
- when accessing structure elements
- in pointer operations
- in scope selectors
- when accessing array elements
**Examples:**

```c
dwMyVar1 = dwMyVar2 * dwMyVar3;
dwRes = EcMyCall(dwMyVar1, dwMyVar2, dwMyVar3);
oMsp.dwMyVar1 = 1;
poMsp->Start(10);
aoReadBuffer[4];
CEcDrv::Desc oDesc;
```

If a statement extends over multiple lines, lines 2 through n are to be aligned with the first:
**Example:**

```c
bWholeWeekFree = bFreeOnMonday & bFreeOnTuesday & bFreeOnWednesday
                 & bFreeOnThursday & bFreeOnFriday;
```

### 7.6 EC-Embedded parenthesis and conditions

Parenthesis must be set around macros:

```c
#define dwEcLogLevel      (GetLogParms()->dwLogLevel)
```

Parenthesis must be set around boolean terms:
**Good:**

```c
if (((1 == 1) && (0 == 0)) || (0 == 0))
```

**Bad:**

```c
if (1 == 1 && 0 == 0)
```

**Rational:**
Misinterpretation of some compilers depending on some terms and prevent warnings about GCC suggestions.

A set value (expected or unexpected value) in comparision is placed first:
**Good:**

```c
if (1 == dwMyVar)
```

**Bad:**

```c
if (dwMyVar == 1)
```

**Rational:**

```c
Prevent undetected typings like if (dwMyVar = 1) and to match the ordering of checks in tests:
CHECK_DWORD_EQUAL(1, dwMyVar1)
```

Use increment, decrement suffix not prefix:
**Good:**

```c
nMyIdx++
```

**Bad:**

```c
++nMyIdx
```

**Rational:**
Unified code style.

### 7.7 EC-Embedded Type System and Hungarian Notation

#### 7.7.1 EC-Embedded Naming Prefixes

In EC-Embedded, specific prefixes are mandatory to avoid naming conflicts and clearly identify module components:
- **Defines:** Every `#define` should have the prefix `EC_`. This prevents overlaps with definitions from other header files and clearly identifies them as project-specific defines.
- **Classes:** All classes should start with `CEc` (e.g., `CEcMyClass`).
- **Structures:** Structures should start with `EC_T_` (e.g., `EC_T_DATATYPE`).

#### 7.7.2 EC-Embedded Type Prefixes

EC-Embedded uses a specific type system (`EC_T_*` types) with corresponding Hungarian Notation prefixes. This extends the base document's type prefix conventions (section [2.1.6](#216-variables)) with EC-Embedded specific mappings.
All variables are created with type-specific prefix:

```c
EC_T_DWORD dwIdx = 0;
```

**EC-Embedded Type Prefix Mappings:**

| Type | Prefix | Example |
|------|------|------|
| `EC_T_DWORD` / `unsigned int` | `dw` | `dwPdoIdx` |
| `EC_T_WORD` / `unsigned short` | `w` | `wPort` |
| `EC_T_INT` / `int` | `n` | `nCount` |
| `EC_T_BYTE` / `unsigned char` | `by` | `byData` |
| `EC_T_SBYTE` / `char` | `sby` | `sbyValue` |
| `EC_T_REAL` / `float` | `f` | `fValue` |
| `EC_T_LREAL` / `double` | `lf` | `lfPrecision` |
| `EC_T_BOOL` / `bool` | `b` | `bIsValid` |
| `enum` | `e` | `eState` |
| Array of bytes | `aby` | `abyData` |
| Pointer to byte(s) | `pby` | `pbyBuffer` |
| `struct`/class instance | `o` | `oConfig` |
| Pointer to struct / class instance | `po` or `p` | `poDevice` or `pDevice` |
| C-string (0 terminated `char*`) | `sz` | `szFileName` |

**Note:** These mappings align with the base document's Hungarian Notation principles but use EC-Embedded specific type names.
**Note on Variable Naming:** The variable naming conventions (Camel Case, Count suffix "Cnt", Loop variable suffix "Idx") are now part of the base document. See section [2.1.6](#216-variables) for details.

### 7.2 EC-Embedded Specific Constants and Defines

#### 7.2.1 Boolean Constants

Use EC-Embedded specific boolean defines instead of standard C/C++ constants:
- Write `EC_TRUE` and `EC_FALSE` instead of `true` and `false`
**Rationale:** Ensures consistency across all EC-Embedded code and compatibility with C code.

#### 7.2.2 Null Pointer Constant and check

Use EC-Embedded specific null pointer constant:
- Write `EC_NULL` for null pointers, not `0` or `NULL`
**Example:**

```c
EC_T_DWORD* pdwValue = EC_NULL;
if (EC_NULL == pdwValue)
{
    /* handle null pointer */
}
```

**Good:**

```c
if (EC_NULL != pdwValue)
```

**Bad:**

```c
if (pdwValue)
```

**Rationale:** Project-specific define ensures consistent null pointer handling across EC-Embedded codebase.

### 7.3 EC-Embedded Specific Restrictions

#### 7.3.1 C++ Syntax Restriction

**CER 07.03.17:** `std::unique_ptr` is not portable (VS6 and also partially GCC!) usable!
**Reference:** See `EcTestCasesErrorDetectionAndDiagnosis.cpp` Version 67 -> 68
**Rationale:** EC-Embedded must support older compilers (including Visual Studio 6) that don't fully support C++11 features.
**Impact:** When using C++11 features, verify compiler compatibility across all supported platforms.

#### 7.3.2 Comment Style Restriction

**EC-Embedded Requirement:** Use `/**/` comments, not `//`
**Rationale:** Some compilers used in EC-Embedded development (particularly for embedded targets) may not fully support `//` comments or may have issues with them in certain contexts.
**Exception:** This restriction applies to EC-Embedded projects. Other projects may allow `//` comments as per the base document (section [4.3.4](#434-comment-style-consistency)).

#### 7.3.3 Inline Functions

Use EC-Embedded specific macros for inline functions:
- Use `EC_INLINESTART` and `EC_INLINESTOP`
**Rationale:** Ensures consistent inline function handling across EC-Embedded codebase and compiler compatibility.

### 7.4 EC-Embedded Programming Guidelines

#### 7.4.1 Namespace Usage

In EC-Embedded, namespaces are not applied at the function declaration level but at the implementation level.
**Implementation:**

```c
namespace EC_NAMESPACE
{
EC_T_VOID CEcMyClass::MyFunction()
{
}
} /* namespace EC_NAMESPACE */
```

**Usage:**

```c
using EC_NAMESPACE;
EC_T_VOID MyModuleFunction()
{
    CEcMyClass oMyClass;
    oMyClass.MyFunction();
}
```

#### 7.4.2 Marking of Modules (Configuration)

In EC-Embedded, only static libraries are marked, but not Debug/Eval/Release configurations. This is because we provide the linker with search paths so that it selects "the best possible" version.
However, since V3.3, control over static/non-static is required, so the filenames of StaticLibs (e.g., on Linux) have been adapted accordingly.

#### 7.4.3 Troubleshooting

##### 7.4.1.1 Compiler Errors

The following table lists compiler / build errors and the corresponding chapter in the workflow document:

| Error | Chapter |
|------|------|
| ERROR: Outdated EC-Wrapper (/CHECK)! | 9.1 |
| EcWrapperTypes.h: … enumerator value for 'assert_line_1869' is not an integer constant | 9.2 |
| EcWrapperTypes.h(1756): error C2118: negative subscript | 9.2 |

**Note on Function Design Patterns:** The error handling pattern (dwRetVal/dwRes), resource cleanup requirements, variable declaration at top, function naming conventions, and programming guidelines (class design, threads) are now part of the base document. See sections [2.1.5](#215-functions-and-methods), [5.1.2](#512-variables), [5.2.2](#522-general), [5.2.6.2](#5262-error-handling-pattern-dwretval-and-dwres), [5.1.4](#514-class-design), and [5.2.7](#527-design-patterns) for details.

### 7.5 Relationship to Base Document

This section **enhances** the base coding conventions in this document with EC-Embedded specific requirements. Where conflicts exist, EC-Embedded specific rules take precedence for EC-Embedded projects.

#### Key Differences from Base Document:

1. **Type System:** Uses `EC_T_*` types with specific prefix mappings (see section [7.1.1](#711-ec-embedded-type-prefixes))
2. **Constants:** Uses `EC_TRUE`, `EC_FALSE`, `EC_NULL` instead of standard constants (see section [7.2](#72-ec-embedded-specific-constants-and-defines))
3. **Comments:** Requires `/* */` comments only (no `//`) due to compiler compatibility (see section [7.3.2](#732-comment-style-restriction))
4. **C++ Features:** Restrictions on C++11 features due to compiler compatibility (see section [7.3.1](#731-c-syntax-restriction))
5. **Inline Functions:** Uses `EC_INLINESTART` and `EC_INLINESTOP` macros (see section [7.3.3](#733-inline-functions))
**Note:** The following conventions are now part of the base document and apply to all projects:
- Function naming (Camel Case, API vs local) - see section [2.1.5](#215-functions-and-methods)
- Variable naming (Camel Case, Count/Index suffixes) - see section [2.1.6](#216-variables)
- Error handling pattern (dwRetVal/dwRes) - see section [5.2.6.2](#5262-error-handling-pattern-dwretval-and-dwres)
- Variable declaration at top of function - see section [5.1.2](#512-variables)
- Resource cleanup on failure - see section [5.2.2](#522-general)
- Class design (no malloc in constructors) - see section [5.1.4](#514-class-design)
- Thread design patterns - see section [5.2.7](#527-design-patterns)

#### Base Document Sections Still Apply:

- File layout (section [3](#3-file-layout))
- General spacing and indentation (section [4.1](#41-spacing), [4.2](#42-indentation))
- Doxygen documentation style (section [4.3.2](#432-doxygen-documentation))
- General programming guidelines (section [5](#5-general-programming-guidelines))
- Module structure (section [1](#1-module))
- Naming conventions principles (section [2](#2-naming-conventions))

### 7.6 References

- **Workflow Document:** AT5010_EC-Embedded-Development-Workflow (Revision 5)
- **Conflict Analysis:** `ConvConflicts.md`
- **Base Enhancements:** `BaseConvEnhancements.md`
This section 7 was extracted from AT5010_EC-Embedded-Development-Workflow (Revision 5) and organized as EC-Embedded specific enhancements to the base coding conventions.