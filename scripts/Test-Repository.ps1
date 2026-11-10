# Requires PowerShell 7. Uses existing Python; installs nothing.
# Windows execution is verified by CI when a workflow run is available.
$ErrorActionPreference = 'Stop'
if ($PSVersionTable.PSVersion.Major -lt 7) { throw 'PowerShell 7 or later is required.' }
$repoRoot = Split-Path -Parent $PSScriptRoot
$pythonCommand = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCommand) { $pythonCommand = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $pythonCommand) { throw 'Install/configure Python 3.12+ before running repository checks.' }
Push-Location $repoRoot
try {
    & $pythonCommand.Source -B -c 'import sys; assert sys.version_info >= (3,12), "Python 3.12+ required"'
    if ($LASTEXITCODE -ne 0) { throw 'Unsupported Python interpreter.' }
    & $pythonCommand.Source -B -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) { throw 'Unit tests failed.' }
    & $pythonCommand.Source -B scripts/check_repository.py
    if ($LASTEXITCODE -ne 0) { throw 'Repository publication checks failed.' }
} finally { Pop-Location }
