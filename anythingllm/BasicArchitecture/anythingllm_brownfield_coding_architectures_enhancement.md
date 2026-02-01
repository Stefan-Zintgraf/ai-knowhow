# Enhancement Document: Embedded C/C++ Adaptation for Brownfield Architectures

## Executive Summary
This document outlines critical enhancements required to adapt the standard **AnythingLLM Brownfield Architectures** for **Embedded C/C++ projects**. While the base architectures (specifically 2 and 4) provide a solid foundation for code retrieval and safety, they lack specific components necessary for handling hardware dependencies, preprocessor complexities, and cross-compilation workflows inherent in embedded systems.

---

## 1. Architectural Gap Analysis

The following table maps the standard brownfield components to the specific requirements of an embedded C/C++ environment.

| Component | Standard Brownfield Requirement | Embedded C/C++ Requirement | Implementation Gap |
| :--- | :--- | :--- | :--- |
| **Context Sources** | ADRs, Runbooks, Markdown Docs | **Datasheets, Schematics, SVD Files** | Need to ingest PDF datasheets and XML hardware maps (SVD) to answer register/timing questions. |
| **Code Indexing** | Tree-sitter / LSP | **Build-Aware LSP & Preprocessor** | Standard LSP fails on `#ifdef` blocks. Indexer must respect `compile_commands.json` to know the active build configuration. |
| **Execution** | `run_tests`, `run_build` | **Cross-Compilation & Simulation** | Code cannot run locally on the agent. Requires `arm-none-eabi-gcc` (or similar) + QEMU/Renode integration. |
| **Symbol Navigation**| `get_def`, `get_refs` | **Linker Script Awareness** | Variables defined in `.ld` files or memory-mapped I/O are invisible to standard software indexers. |

---

## 2. Enhanced Architecture: "The Embedded Agent"

This architecture builds upon **Architecture 2 (Dedicated Code Indexer)** and **Architecture 4 (Gated Execution)**, adding specialized loops for hardware verification.

### 2.1 Core Components

#### A. The Hardware-Aware Knowledge Base (AnythingLLM)
* **Ingestion Pipeline:**
    * **Datasheets (PDF):** Ingest specific MCU and sensor datasheets. Use OCR-enabled parsing if tables are complex.
    * **SVD to Markdown:** Convert System View Description (SVD) XML files into Markdown summaries. This allows the LLM to query "What is the offset of `CR1` in `USART1`?" with high precision.
    * **Errata Sheets:** Critical for explaining why "standard" code might not work on specific silicon revisions.

#### B. The Build-Aware Code Indexer
* **Dependency:** `compile_commands.json` (generated via CMake or Bear).
* **Tooling:** Use `clangd` or `ccls` configured with the cross-compiler's sysroot.
* **Macro Expansion Tool:** A specific tool for the agent: `expand_macro(file, line)`. This runs the preprocessor (`gcc -E`) so the agent sees the code *after* macros are resolved.

#### C. The Simulation & Verification Loop (Gated Execution)
Instead of simple unit tests, the validation phase must verify hardware behavior.

1.  **Cross-Compile:** Agent triggers build with target toolchain.
2.  **Simulation:** Binary is loaded into a headless simulator (e.g., **Renode** or **QEMU**).
3.  **Harness:** A Python script feeds inputs (simulated GPIO/UART) and asserts outputs.
4.  **Feedback:** The agent receives compilation errors *or* simulation logs, not just test exit codes.

---

## 3. Revised Workflow (Architecture 2.5)

**Scenario:** *Refactoring an I2C sensor driver.*

1.  **Developer Prompt:** "Update the BMI160 driver to support the C3 revision."
2.  **Retrieval Phase:**
    * **AnythingLLM:** Retrieves the BMI160 Datasheet and "C3 Revision Errata" note.
    * **Code Indexer:** Locates `bmi160.c` and `i2c_hal.h`.
3.  **Context Construction:**
    * Agent identifies that `BMI160_ACCEL_X` is a macro.
    * Agent uses `expand_macro` to verify the actual register address being used in the current build.
4.  **Modification Phase:**
    * Agent modifies `bmi160.c` to handle the new register layout.
5.  **Verification Phase (The Gate):**
    * Agent calls `run_simulation(test_scenario="init_sequence")`.
    * **System:** Compiles → Loads to Renode → Simulates I2C bus traffic.
    * **Feedback:** "Simulation failed: ACK missing on byte 0x44."
6.  **Iteration:** Agent reads feedback, corrects the I2C address, and retries.

---

## 4. Minimum Tool Contract Updates

To support this workflow, the **Minimum Tool Contract** must be expanded:

| Tool Category | Standard Tool | Embedded Addition | Description |
| :--- | :--- | :--- | :--- |
| **Indexer** | `get_def(symbol)` | `expand_macro(file, line)` | Returns preprocessed code to debug `#define` logic. |
| **Indexer** | `search_code` | `search_memory_map(addr)` | Finds which peripheral lives at a specific hex address (from SVD/Linker). |
| **Execution** | `run_tests` | `build_target(config)` | Runs the cross-compiler for a specific board config. |
| **Execution** | N/A | `simulate(binary, script)` | Runs the binary in a hardware simulator. |

---

## 5. Implementation Roadmap

1.  **Phase 1: Knowledge Ingestion (Immediate)**
    * Set up AnythingLLM workspace.
    * Ingest PDF Datasheets and Architecture Reference Manuals.
    * **Action:** Write a script to convert project `.svd` files to Markdown for ingestion.

2.  **Phase 2: Build-Aware Indexing**
    * Configure the project build system (CMake/Make) to export `compile_commands.json`.
    * Deploy a `clangd` instance that references this database for queries.

3.  **Phase 3: Simulation Integration**
    * Define a Docker container with the cross-compiler and QEMU/Renode.
    * Create a simple wrapper script `run_sim.py` that the agent can call to test its code.
    