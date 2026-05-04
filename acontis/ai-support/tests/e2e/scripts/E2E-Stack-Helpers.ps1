# Shared helpers for tests/e2e/scripts Start-*.ps1 and Stop-*.ps1
#
# After dot-sourcing, the caller must set:
#   $Root       — resolved repo root (e.g. Resolve-Path(Join-Path $PSScriptRoot "..\..\.."))
#   $E2eLogDir  — (Join-Path $Root "tests\e2e\logs")
#
# For Start-E2EProcess with -LogToFiles, $E2eLogDir must exist or be creatable by New-E2ELogBatch.

#Requires -Version 5.1

function Escape-ForBatchString {
    # Double internal double-quotes for use inside a double-quoted string in a .cmd file.
    param([string]$S)
    if ($null -eq $S) { return "" }
    return $S.Replace('"', '""')
}

function New-E2ELogBatch {
    # Returns a .cmd that runs: start "" /B <exename> <args> 1>out 2>err  then exit (batch exits, service keeps running).
    param(
        [string]$Name,
        [string]$FilePath,
        [string[]]$CommandArgs
    )
    if (-not (Test-Path -LiteralPath $E2eLogDir)) { New-Item -ItemType Directory -Path $E2eLogDir -Force | Out-Null }
    $out = Join-Path $E2eLogDir "e2e-$Name.stdout.log"
    $err = Join-Path $E2eLogDir "e2e-$Name.stderr.log"
    $rootQ = (Escape-ForBatchString (Resolve-Path -LiteralPath $Root).Path)
    $exeQ  = (Escape-ForBatchString $FilePath)
    $outQ  = (Escape-ForBatchString $out)
    $errQ  = (Escape-ForBatchString $err)
    if ($CommandArgs -and $CommandArgs.Count -gt 0) {
        # One batch-quoted token per argument: "a" "b" "c"
        $argPrefix = ( $CommandArgs | ForEach-Object { '"' + (Escape-ForBatchString $_) + '"' } ) -join ' '
    } else {
        $argPrefix = ""
    }
    $line = if ($argPrefix) {
        "start `"`" /B `"$exeQ`" $argPrefix 1> `"$outQ`" 2> `"$errQ`""
    } else {
        "start `"`" /B `"$exeQ`" 1> `"$outQ`" 2> `"$errQ`""
    }
    $b = @(
        '@echo off',
        "cd /d `"$rootQ`"",
        $line,
        'exit /b 0',
        ''
    ) -join "`r`n"
    $batch = Join-Path $E2eLogDir "e2e-run-$Name.cmd"
    # Default / OEM: cmd reads batch reliably on localized Windows; paths here are usually ASCII.
    $enc = [System.Text.Encoding]::GetEncoding([System.Text.Encoding]::Default.CodePage)
    [System.IO.File]::WriteAllText($batch, $b, $enc)
    return @{
        Path   = $batch
        Stdout = $out
        Stderr = $err
    }
}

function Start-AnythingLLMDesktop {
    <#
    .SYNOPSIS
      Launch AnythingLLM Desktop without attaching to the PowerShell console (default), or with
      stdout/stderr to tests/e2e/logs (same pattern as Start-E2EProcess -LogToFiles).

      PowerShell's Start-Process uses UseShellExecute=false for .exe by default, which lets the
      Electron/Node backend inherit this console and spam [backend] lines. UseShellExecute=true
      (quiet mode) avoids that; -LogToFiles uses the batch redirect helper instead.
    #>
    param(
        [Parameter(Mandatory = $true)][string]$ExePath,
        [switch]$LogToFiles
    )
    if ($LogToFiles) {
        if (-not (Test-Path -LiteralPath $E2eLogDir)) {
            New-Item -ItemType Directory -Path $E2eLogDir -Force | Out-Null
        }
        $info = New-E2ELogBatch -Name "anythingllm" -FilePath $ExePath -CommandArgs @()
        Start-Process -FilePath $Info.Path -WorkingDirectory $Root -WindowStyle Hidden
        Write-Host "  AnythingLLM log stdout: $($Info.Stdout)" -ForegroundColor DarkGray
        Write-Host "  AnythingLLM log stderr: $($Info.Stderr)" -ForegroundColor DarkGray
        Write-Host "  AnythingLLM launcher:   $($Info.Path)" -ForegroundColor DarkGray
        return
    }
    $psi = [System.Diagnostics.ProcessStartInfo]::new()
    $psi.FileName = $ExePath
    $psi.WorkingDirectory = $Root
    $psi.UseShellExecute = $true
    $psi.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Minimized
    [void][System.Diagnostics.Process]::Start($psi)
}

function Start-E2EProcess {
    param(
        [string]$Name,
        [string]$FilePath,
        [string[]]$CommandArgs = @(),
        [switch]$LogToFiles
    )
    if (-not $LogToFiles) {
        $p = @{
            FilePath         = $FilePath
            WorkingDirectory = $Root
            WindowStyle      = "Minimized"
        }
        if ($CommandArgs -and $CommandArgs.Count -gt 0) { $p.ArgumentList = $CommandArgs }
        Start-Process @p
        return
    }
    $info = New-E2ELogBatch -Name $Name -FilePath $FilePath -CommandArgs $CommandArgs
    Start-Process -FilePath $Info.Path -WorkingDirectory $Root -WindowStyle Hidden
    Write-Host "  log stdout: $($Info.Stdout)" -ForegroundColor DarkGray
    Write-Host "  log stderr: $($Info.Stderr)" -ForegroundColor DarkGray
    Write-Host "  launcher:   $($Info.Path)" -ForegroundColor DarkGray
}

function Test-TcpOpen {
    param([string]$ComputerName = "127.0.0.1", [int]$Port, [int]$TimeoutMs = 500)
    $c = $null
    try {
        $c = [System.Net.Sockets.TcpClient]::new()
        $iar = $c.BeginConnect($ComputerName, $Port, $null, $null)
        if (-not $iar.AsyncWaitHandle.WaitOne($TimeoutMs)) { return $false }
        $c.EndConnect($iar)
        return $true
    } catch {
        return $false
    } finally {
        if ($null -ne $c) { $c.Close() }
    }
}

function Wait-ForPort {
    param(
        [string]$Label,
        [int]$Port,
        [int]$TimeoutSec
    )
    $deadline = (Get-Date).AddSeconds($TimeoutSec)
    $t0 = Get-Date
    $nextMsg = 10
    while ((Get-Date) -lt $deadline) {
        if (Test-TcpOpen -Port $Port) {
            Write-Host "  OK: $Label listening on $Port" -ForegroundColor Green
            return
        }
        $elapsed = [int]((Get-Date) - $t0).TotalSeconds
        if ($elapsed -ge $nextMsg) {
            $remain = [math]::Max(0, [int]($deadline - (Get-Date)).TotalSeconds)
            Write-Host "  ... still waiting for $Label (127.0.0.1:$Port)  ${elapsed}s, ~${remain}s left" -ForegroundColor DarkGray
            try { [Console]::Out.Flush() } catch {}
            $nextMsg = $nextMsg + 10
        }
        Start-Sleep -Seconds 1
    }
    $hint = if ($Logs) { " See $E2eLogDir (e2e-*.stdout.log / e2e-*.stderr.log)" } else { " If the process exited, check the minimized window for errors" }
    throw "Timeout waiting for $Label on 127.0.0.1:$Port after ${TimeoutSec}s.$hint."
}

function Resolve-ExeInPath {
    # Walks $env:Path only (already merged with machine/user at script start). Skips UNC entries:
    # Test-Path in those folders can block for a long time on bad network paths.
    param([string]$Name)
    $candidates = [System.Collections.Generic.List[string]]::new()
    if ($Name -match "\.(exe|cmd|com|bat)$") {
        $candidates.Add($Name)
    } else {
        $candidates.Add($Name)
        $exts = if ($env:PATHEXT) { $env:PATHEXT -split ";" } else { @(".exe", ".cmd", ".com", ".bat") }
        foreach ($e in $exts) {
            if ($e) { $candidates.Add($Name + $e) }
        }
    }
    foreach ($dir in $env:Path -split ";") {
        if (-not $dir) { continue }
        $base = $dir.Trim().TrimEnd("\")
        if ($base -match '^\s*\\') { continue } # UNC: avoid hangs on unreachable shares
        if ($base -match '^".*"$') { $base = $base.Trim('"') }
        if (-not $base) { continue }
        foreach ($c in $candidates) {
            if (-not $c) { continue }
            $p = Join-Path $base $c
            if (Test-Path -LiteralPath $p) { return (Resolve-Path -LiteralPath $p).Path }
        }
    }
    return $null
}

function Resolve-Cmd {
    param([string]$Name)
    if (Test-Path -LiteralPath $Name -PathType Leaf) { return (Resolve-Path -LiteralPath $Name).Path }
    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    if ($Name -notmatch "\.(exe|cmd|com|bat)$") {
        $cmd = Get-Command ($Name + ".exe") -ErrorAction SilentlyContinue
        if ($cmd) { return $cmd.Source }
    }
    $r = Resolve-ExeInPath -Name $Name
    if ($r) { return $r }
    return $null
}

function Test-OllamaModelLocal {
    <#
    .SYNOPSIS
      Returns true if the model is already in the local Ollama library (ollama show exits 0).
    #>
    param(
        [Parameter(Mandatory = $true)][string]$OllamaExe,
        [Parameter(Mandatory = $true)][string]$Model
    )
    if (-not (Test-Path -LiteralPath $OllamaExe)) { return $false }
    $prevEap = $ErrorActionPreference
    $ErrorActionPreference = "SilentlyContinue"
    $null = & $OllamaExe show $Model 2>&1
    $ok = ($LASTEXITCODE -eq 0)
    $ErrorActionPreference = $prevEap
    return $ok
}

function Ensure-E2EOllamaModels {
    <#
    .SYNOPSIS
      Ensure the embedding and chat models for config.e2e + litellm-ollama-e2e (all-minilm, llama3.2:1b).
      Pulls each model only if it is not already available locally.
    #>
    param(
        [string]$OllamaExe,
        [switch]$WhatIf
    )
    if (-not $OllamaExe) {
        $OllamaExe = Resolve-OllamaExe
    }
    if (-not (Test-Path -LiteralPath $OllamaExe)) {
        Write-Host "Ollama: model check/pull skipped (ollama.exe not found)" -ForegroundColor DarkYellow
        return
    }
    if ($WhatIf) {
        Write-Host "Ollama: would pull all-minilm and llama3.2:1b only for any model not already local (ollama show)" -ForegroundColor DarkGray
        return
    }
    $e2eModels = @(
        @{ Name = "all-minilm"; Note = "embed" },
        @{ Name = "llama3.2:1b"; Note = "chat" }
    )
    foreach ($entry in $e2eModels) {
        $name = $entry.Name
        if (Test-OllamaModelLocal -OllamaExe $OllamaExe -Model $name) {
            Write-Host "Ollama: model $name [$($entry.Note)] already present; skip pull" -ForegroundColor DarkGray
            continue
        }
        Write-Host "Ollama: pulling $name [$($entry.Note)]" -ForegroundColor Cyan
        & $OllamaExe pull $name
        $rc = $LASTEXITCODE
        if ($rc -ne 0) { throw "ollama pull $name failed, rc=$rc. Install model or fix Ollama." }
    }
    Write-Host "Ollama: E2E models ready" -ForegroundColor Green
}

function Resolve-OllamaExe {
    $r = Resolve-Cmd "ollama"
    if ($r) { return $r }
    foreach ($c in @(
        (Join-Path $env:LOCALAPPDATA "Programs\Ollama\ollama.exe"),
        (Join-Path $env:ProgramFiles "Ollama\ollama.exe"),
        (Join-Path ${env:ProgramFiles(x86)} "Ollama\ollama.exe")
    )) {
        if (Test-Path -LiteralPath $c) { return (Resolve-Path -LiteralPath $c).Path }
    }
    return $null
}

function Get-ListenerPids {
    param([int]$Port)
    try {
        # Auto-import is not always present in all hosts (e.g. constrained ISE, some automation).
        Import-Module NetTCPIP -ErrorAction SilentlyContinue
        $conns = Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue
        if (-not $conns) { return @() }
        $conns | ForEach-Object { $_.OwningProcess } | Sort-Object -Unique
    } catch {
        @()
    }
}

function Stop-PortListener {
    param(
        [string]$Label,
        [int]$Port
    )
    $pids = Get-ListenerPids -Port $Port
    if (-not $pids) {
        Write-Host "${Label}: nothing listening on $Port" -ForegroundColor DarkGray
        return
    }
    foreach ($procId in $pids) {
        if ($procId -le 4) { continue }
        try {
            $p = Get-Process -Id $procId -ErrorAction Stop
            Write-Host "Stopping ${Label}: PID $procId ($($p.ProcessName)) 127.0.0.1:$Port" -ForegroundColor Yellow
            Stop-Process -Id $procId -Force -ErrorAction Stop
        } catch {
            Write-Host "Stopping $Label PID $procId failed: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

function Resolve-AnythingLlmDesktopExe {
    <#
    .SYNOPSIS
      Resolve path to AnythingLLM Desktop (Windows). See docs/e2e-anythingllm.md#one-time-setup
    #>
    param([string]$ExplicitPath = "")
    if ($ExplicitPath -and (Test-Path -LiteralPath $ExplicitPath)) {
        return (Resolve-Path -LiteralPath $ExplicitPath).Path
    }
    $envPath = $env:ANYTHINGLLM_DESKTOP_EXE
    if ($envPath -and (Test-Path -LiteralPath $envPath)) {
        return (Resolve-Path -LiteralPath $envPath).Path
    }
    $default = Join-Path $env:LOCALAPPDATA "Programs\AnythingLLM\AnythingLLM.exe"
    if (Test-Path -LiteralPath $default) {
        return (Resolve-Path -LiteralPath $default).Path
    }
    $msg = @"
AnythingLLM Desktop executable not found.
  Install: https://docs.useanything.com/installation-desktop/windows
  Or set environment variable ANYTHINGLLM_DESKTOP_EXE to the full path to AnythingLLM.exe
  Or pass -AnythingLlmExePath to Start-E2E-Stack.ps1
  Default path checked: $default
"@
    throw $msg
}

function Stop-AnythingLlmDesktop {
    <#
    .SYNOPSIS
      Stop AnythingLLM Desktop by process name (Electron). Port is optional (informational check).
    #>
    param(
        [int]$Port = 0,
        [switch]$Skip
    )
    if ($Skip) {
        Write-Host "AnythingLLM: skipped (-SkipAnythingLlm)" -ForegroundColor DarkGray
        return
    }
    $procs = Get-Process -Name "AnythingLLM" -ErrorAction SilentlyContinue
    if ($procs) {
        Write-Host "Stopping AnythingLLM Desktop (process name AnythingLLM)..." -ForegroundColor Yellow
        $procs | ForEach-Object {
            $proc = $_
            try {
                Write-Host "  Stop-Process -Id $($proc.Id) ($($proc.ProcessName))" -ForegroundColor DarkGray
                Stop-Process -Id $proc.Id -Force -ErrorAction Stop
            } catch {
                Write-Host "  Stop PID $($proc.Id) failed: $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    } else {
        Write-Host "AnythingLLM: no process named AnythingLLM" -ForegroundColor DarkGray
    }
    if ($Port -gt 0) {
        Start-Sleep -Seconds 1
        if (Test-TcpOpen -Port $Port) {
            Write-Host "AnythingLLM: port $Port still listening (another listener or app still starting)." -ForegroundColor DarkYellow
        }
    }
}
