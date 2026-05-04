# Step 0a — BMAD Baseline: Document Project

**Status:** [ ]

**Session rule:** Complete this step, run the gate, mark `[x]`, then stop.

**Prerequisites:** BMAD Method installed in the `rtv` repository (`npx bmad-method install`).

---

## Goal

Produce comprehensive baseline documentation of the `rtv` codebase — architecture, technology stack, source tree, integration points, dependencies — so that subsequent security analysis steps (especially Step 3) can build on this foundation rather than rediscovering the same information.

---

## Tasks

1. Open a fresh chat session in your AI IDE.
2. Load the BMAD Analyst agent: `bmad-analyst`.
3. Run: `document-project`.
4. When prompted for scan depth, select **Deep Scan** or **Exhaustive Scan** (not Quick — the security assessment needs source-level detail).
5. Point the workflow at the `rtv` repository root: `C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\`.
6. The workflow will classify the project, detect components and parts, scan technology stacks, and generate structured documentation under `_bmad-output/`.
7. After the full scan completes, run **deep-dive** sessions for the six component groups:

| Session | Components |
|---|---|
| 3a | Framework VMF Core (`Framework\Source\Core\`) |
| 3b | Windows Drivers (`Windows\Source\Driver\*`) |
| 3c | Windows User-Mode (`Windows\Source\RtosLib\`, `RtosService\`, `SystemManager\`, `VmfInterfaceUserMode\`) |
| 3d | Linux Components (`Linux\Source\*`, `Linux\target\hv\`) |
| 3e | Hypervisor Components (`Hypervisor\Source\*`) |
| 3f | LxWin/VxWin/SDK (`LxWin\Source\*`, `VxWin\Source\*`, `Common\All\*`) |

### How to run each deep-dive session

The full scan (tasks 1–6) must be complete before starting deep-dives.
Repeat the following procedure for each session (3a → 3f), using a **fresh chat** every time to avoid context exhaustion:

1. Open a **new chat session** in your AI IDE.
2. Load the Analyst agent: `bmad-analyst`.
3. Invoke the skill: `document-project` (or menu code `DP`).
4. The workflow finds the existing `index.md` and asks what to do — select **"Deep-dive into specific area"** (option 2).
5. When prompted for a target, enter the folder path(s) from the table above (e.g. `Framework\Source\Core\` for session 3a). For sessions covering multiple folders (3c, 3d, 3f), provide all listed paths.
6. The workflow shows a confirmation with the target name, path, and estimated file count. Review and confirm with **y**.
7. Wait for the exhaustive scan to complete (reads every file, builds dependency graph, traces data flow). Expect 30–120 min per session depending on file count.
8. When the workflow asks whether to deep-dive another area or finish, select **Finish** (option 2).
9. Verify that `_bmad-output/deep-dive-{name}.md` was created and that `index.md` was updated with a link to it.

---

## Verifiable result

- [ ] `rtv\_bmad-output\index.md` exists (master project documentation index).
- [ ] `rtv\_bmad-output\project-overview.md` exists.
- [ ] `rtv\_bmad-output\architecture.md` (or per-part architecture files) exists.
- [ ] `rtv\_bmad-output\source-tree-analysis.md` exists.
- [ ] Deep-dive files exist for all six component groups listed above.
- [ ] All output files are non-empty and contain meaningful content.

---

## Gate

```
Verify the following files exist and are non-empty under rtv\_bmad-output\:
  - index.md
  - project-overview.md
  - architecture.md (or multiple per-part files)
  - source-tree-analysis.md
  - Deep-dive files for each of the 6 component groups
```

Manual verification: open `index.md` and confirm it links to the component deep-dives.

**Human interaction:** Minimal — select scan depth, confirm project classification, choose deep-dive targets.
