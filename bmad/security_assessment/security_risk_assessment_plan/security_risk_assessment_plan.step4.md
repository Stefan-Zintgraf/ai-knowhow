# Step 4 — Map Interfaces and Trust Boundaries

**Status:** [ ]

**Session rule:** Complete this step, run the gate, mark `[x]`, then stop.

**Prerequisites:** Step 3 (component documentation) must be complete.

---

## Goal

Document all inter-component interfaces, data flows crossing trust boundaries, and external-facing surfaces. This is a critical input for STRIDE threat modeling (Step 5) and Threagile model generation (Step 5b).

---

## Input

- Component documentation from Step 3: `03_component_documentation\*.md`
- Key interface headers:
  - `rtv\Common\All\SDK\Inc\vmfInterface.h` (VMF API)
  - `rtv\Common\All\SDK\Inc\rtosLib.h` (RtosLib API)
  - `rtv\Windows\Source\Driver\RtosDrv\Vmf\vmfDrvInterface.cpp`
  - `rtv\Linux\Source\Driver\hrtosdrv\Vmf\vmfDrvInterface.cpp`
  - `rtv\Linux\Source\HostRtosDrvInterfaceUserMode\HostRtosDrvIf.h`
  - `rtv\Hypervisor\Source\HvWeb\` (web API endpoints)
  - `rtv\Hypervisor\Source\virtio_events\` (virtio event interface)
  - `rtv\Hypervisor\Source\MQTTnet\` (MQTT messaging)

## Tasks

1. Identify all trust boundary crossings:
   - **Guest → Host** (VMF calls, virtio, IVSHMEM shared memory)
   - **User-mode → Kernel-mode** (driver IOCTLs, system calls)
   - **Network → Application** (HvWeb HTTP/WebSocket, MQTT, SystemManager)
   - **Unprivileged → Privileged** (service interfaces, installer elevation)
   - **External → Internal** (file uploads, configuration inputs, USB passthrough)
2. For each interface, document: calling convention, data format, validation performed, authentication required, error handling.
3. Draw a text-based interface diagram showing trust zones.

---

## Output files

Write to `C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\04_interface_map\`:

- `index.md` — Overview with ASCII trust boundary diagram
- `kernel_user_interfaces.md` — Driver ↔ user-mode boundaries
- `vmf_call_interface.md` — VMF call dispatch (host ↔ guest)
- `network_interfaces.md` — RtosVnet, IVSHMEM, MQTT, virtio
- `ipc_shared_memory.md` — IVSHMEM, shared memory regions
- `web_api_interfaces.md` — HvWeb REST/WebSocket, SystemManager
- `installer_deployment.md` — Setup chains, signing, privilege escalation

---

## Agent prompt

```
You are a security architect performing interface analysis on the acontis hypervisor product family.

Read the component documentation at:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\03_component_documentation\

Then analyze these key interface files in the source:
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Common\All\SDK\Inc\vmfInterface.h
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Common\All\SDK\Inc\rtosLib.h
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Windows\Source\Driver\RtosDrv\Vmf\ (vmfDrvInterface)
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Linux\Source\Driver\hrtosdrv\Vmf\ (vmfDrvInterface)
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Linux\Source\HostRtosDrvInterfaceUserMode\
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Hypervisor\Source\HvWeb\ (web API)
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Hypervisor\Source\virtio_events\
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Hypervisor\Source\MQTTnet\
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Windows\Source\SystemManager\
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Framework\Source\Core\ (IVSHMEM headers)

Identify and document ALL inter-component interfaces, organized by trust boundary:
1. Guest-to-Host boundaries (VMF calls, virtio, IVSHMEM shared memory)
2. User-mode to Kernel-mode boundaries (driver IOCTLs)
3. Network-facing interfaces (HTTP, WebSocket, MQTT)
4. IPC / shared memory interfaces
5. Installer / deployment privilege transitions
6. External input surfaces (config files, USB, PCI passthrough)

For each interface document: protocol/mechanism, data format, input validation,
authentication, error handling, privilege levels on each side.

Create an ASCII trust-boundary diagram in index.md showing trust zones and crossings.

Write output to:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\04_interface_map\

IMPORTANT: Ignore all folders named brainstormingPlatform or brainstormingPlatformPlus.
```

---

## Verifiable result

- [ ] All 7 output files exist under `04_interface_map\` and are non-empty.
- [ ] `index.md` contains an ASCII trust boundary diagram.
- [ ] Each interface file documents: protocol, data format, validation, auth, error handling.
- [ ] All five trust boundary categories are covered.

---

## Gate

```bash
cd 04_interface_map
for f in index.md kernel_user_interfaces.md vmf_call_interface.md network_interfaces.md ipc_shared_memory.md web_api_interfaces.md installer_deployment.md; do
  test -s "$f" && echo "PASS: $f" || echo "FAIL: $f"
done

# Verify trust boundary diagram exists
grep -q "trust\|boundary\|zone" index.md && echo "PASS: trust boundary content" || echo "FAIL: no trust boundary content"
```

**Human interaction:** None required.
