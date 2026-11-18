$ErrorActionPreference = 'Stop'
$recordDir = Join-Path $PSScriptRoot 'evidence'
New-Item -ItemType Directory -Force $recordDir | Out-Null
$ownedChildren = @()
$parentShell = $null
try {
    $parentShell = Start-Process cmd.exe -ArgumentList '/k "start /b ping -n 600 127.0.0.1 >nul"' -WindowStyle Hidden -PassThru
    Start-Sleep 2
    $processes = @(Get-CimInstance Win32_Process)
    $childRows = @($processes | Where-Object { $_.ParentProcessId -eq $parentShell.Id -and $_.Name -eq 'PING.EXE' })
    $ownedChildren += $childRows.ProcessId
    $ancestry = @()
    $currentRow = $processes | Where-Object ProcessId -eq $parentShell.Id
    $seenNumbers = @()
    while ($currentRow -and $currentRow.ProcessId -notin $seenNumbers) {
        $ancestry += $currentRow | Select-Object ProcessId,ParentProcessId,Name
        $seenNumbers += $currentRow.ProcessId
        $nextNumber = $currentRow.ParentProcessId
        $currentRow = $processes | Where-Object ProcessId -eq $nextNumber | Select-Object -First 1
    }
    $browserRows = @($processes | Where-Object Name -eq 'msedge.exe' | Select-Object ProcessId,ParentProcessId,Name)
    $temporaryShell = Start-Process cmd.exe -ArgumentList '/c "start /b ping -n 900 127.0.0.1 >nul"' -WindowStyle Hidden -PassThru
    $temporaryShell.WaitForExit()
    Start-Sleep 1
    $orphanRows = @(Get-CimInstance Win32_Process | Where-Object { $_.ParentProcessId -eq $temporaryShell.Id -and $_.Name -eq 'PING.EXE' })
    $ownedChildren += $orphanRows.ProcessId
    $measurement = [ordered]@{
        Time = (Get-Date).ToString('o')
        Roots = @($processes | Where-Object { $_.ProcessId -in 0,4 } | Select-Object ProcessId,ParentProcessId,Name)
        Ancestry = $ancestry
        Children = @($childRows | Select-Object ProcessId,ParentProcessId,Name)
        Browser = $browserRows
        OrphanParent = $temporaryShell.Id
        OrphanParentAlive = [bool](Get-Process -Id $temporaryShell.Id -ErrorAction SilentlyContinue)
        Orphans = @($orphanRows | Select-Object ProcessId,ParentProcessId,Name)
    }
    $measurement | ConvertTo-Json -Depth 8 | Set-Content (Join-Path $recordDir 'tree.json') -Encoding utf8
    $measurement | ConvertTo-Json -Depth 8
} finally {
    foreach ($number in $ownedChildren) { Stop-Process -Id $number -ErrorAction SilentlyContinue }
    if ($parentShell -and !$parentShell.HasExited) { Stop-Process -Id $parentShell.Id -ErrorAction SilentlyContinue }
}
