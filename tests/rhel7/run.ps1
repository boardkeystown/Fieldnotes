param([switch]$Prepare)
$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$kit = Join-Path $projectRoot '.artifacts\rhel7'
$podmanCommand = Get-Command podman -ErrorAction SilentlyContinue
if ($podmanCommand) { $podmanExe = $podmanCommand.Source }
else { $podmanExe = Join-Path $env:LOCALAPPDATA 'Programs\Podman\podman.exe' }
if (-not (Test-Path -LiteralPath $podmanExe)) { throw 'Install Podman and start its machine first.' }
$image = (Get-Content -LiteralPath (Join-Path $PSScriptRoot 'image.txt') -Raw).Trim()
New-Item -ItemType Directory -Path $kit -Force | Out-Null
$mounts = @('--volume', "${projectRoot}:/workspace:ro", '--volume', "${kit}:/kit:rw")
if ($Prepare) {
    & $podmanExe pull $image
    if ($LASTEXITCODE -ne 0) { throw 'Image download failed.' }
    & $podmanExe run --rm --pull=never @mounts $image python /workspace/tests/rhel7/container_check.py prepare
    if ($LASTEXITCODE -ne 0) { throw 'Dependency preparation failed.' }
    Copy-Item -LiteralPath (Join-Path $kit 'requirements.lock') -Destination (Join-Path $PSScriptRoot 'requirements.lock') -Force
}
if (-not (Test-Path -LiteralPath (Join-Path $kit 'checksums.json'))) { throw 'Run with -Prepare once while connected, or transfer a prepared .artifacts/rhel7 kit.' }
& $podmanExe run --rm --pull=never --network=none @mounts --env "FIELDNOTES_IMAGE=$image" $image python /workspace/tests/rhel7/container_check.py verify
if ($LASTEXITCODE -ne 0) { throw 'Offline container verification failed.' }
Write-Output "Passed. Report: $kit\result.json"
Write-Output "Built documentation: $kit\site\index.html"
