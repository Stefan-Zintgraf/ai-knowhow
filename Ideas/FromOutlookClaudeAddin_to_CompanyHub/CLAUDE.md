# OutlookClaudeAddin - Session Notes

## Environment

- Platform: Windows (win32)
- Shell: Use `powershell.exe -Command "..."` for Windows commands, NOT bash syntax like `ls "path\with\backslashes"`
- Bash tool is available but runs in a Unix-like shell — Windows paths with backslashes and spaces cause quoting issues

## File System Operations

**Always use PowerShell for listing files, not bash `ls`:**
```powershell
powershell.exe -Command "Get-ChildItem 'C:\PROJ\...' | Format-Table Name, Length, LastWriteTime"
```

## Building the Solution

**MSBuild location:**
```
C:\Program Files\Microsoft Visual Studio\2022\Professional\MSBuild\Current\Bin\MSBuild.exe
```

**Build command (use PowerShell — bash quoting breaks with spaces in path):**
```powershell
powershell.exe -Command "& 'C:\Program Files\Microsoft Visual Studio\2022\Professional\MSBuild\Current\Bin\MSBuild.exe' 'C:\PROJ\OutlookClaudeAddin\OutlookClaudeAddin.sln' /p:Configuration=Debug '/p:Platform=Any CPU' /v:minimal"
```

**Note on `/p:Platform=Any CPU`:** The space in "Any CPU" must be inside a single-quoted string when passed through PowerShell, otherwise MSBuild misinterprets extra tokens as additional project files and fails with `MSB1008`.

## Certificate / Signing

The original `OutlookClaudeAddin_TemporaryKey.pfx` was password-protected and not importable without the password.

**Fix applied:** A new self-signed certificate was generated and the PFX was replaced:
```powershell
$cert = New-SelfSignedCertificate -Subject 'CN=OutlookClaudeAddin' -CertStoreLocation 'Cert:\CurrentUser\My' -KeyUsage DigitalSignature -Type CodeSigningCert -NotAfter (Get-Date).AddYears(10)
Export-PfxCertificate -Cert $cert -FilePath 'C:\PROJ\OutlookClaudeAddin\OutlookClaudeAddin\OutlookClaudeAddin_TemporaryKey.pfx' -Password (New-Object System.Security.SecureString)
```

Current thumbprint in `OutlookClaudeAddin.csproj`: `4EB164A0BAD21C91F2AEF51C0A8C72B58C216ACA`

The certificate must be present in `Cert:\CurrentUser\My` on the build machine. If building on a new machine, re-run the commands above and update `<ManifestCertificateThumbprint>` in the .csproj.

**Note:** VSTO Office Tools targets (`Microsoft.VisualStudio.Tools.Office.targets`) require `<SignManifests>true</SignManifests>` — setting it to `false` causes a hard build error. Signing cannot be skipped for VSTO add-ins.

## Build Output

Successful build produces in `OutlookClaudeAddin\bin\Debug\`:
- `OutlookClaudeAddin.dll` — compiled add-in
- `OutlookClaudeAddin.dll.manifest` — ClickOnce manifest
- `OutlookClaudeAddin.vsto` — VSTO deployment descriptor
- `OutlookClaudeAddin.pdb` — debug symbols
- Runtime DLLs: VSTO utilities, Newtonsoft.Json, Office PIAs
