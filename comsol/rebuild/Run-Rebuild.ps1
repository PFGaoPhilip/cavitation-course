param(
  [ValidateSet('A','B','Checks')][string]$Model = 'B',
  [string]$ComsolBin = (Join-Path $env:ProgramFiles 'COMSOL\COMSOL64\Multiphysics\bin\win64')
)
$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$sourceDir = Join-Path $projectRoot 'scripts'
$buildDir = Join-Path $projectRoot '.build'
foreach ($directory in @('.build','scratch','final','data','logs','plots','native-config\A','native-config\B')) {
  New-Item -ItemType Directory -Path (Join-Path $projectRoot $directory) -Force | Out-Null
}
$compiler = Join-Path $ComsolBin 'comsolcompile.exe'
$batch = Join-Path $ComsolBin 'comsolbatch.exe'
if (-not (Test-Path -LiteralPath $compiler) -or -not (Test-Path -LiteralPath $batch)) {
  throw 'COMSOL compile/batch runtime not found. Set -ComsolBin to the installed 6.4 win64 folder.'
}
$stages = switch ($Model) {
  'A' { @('PressureEnvelope3D','SmallGasRefinement3D','UniformPfpFinalRefinement3D','FinalModelA3D') }
  'B' { @('FreeCoreShellFine3D','GelSensitivityValid3D','FinalModelB3D') }
  'Checks' { @('WorstGasTime3D','WorstGasMesh3D','FivePfpDomain3D','FreeCoreShellPfp3D') }
}
$nativeRoot = $projectRoot.Replace('\','/') + '/'
foreach ($stage in $stages) {
  $original = Join-Path $sourceDir ($stage + '.java')
  $target = Join-Path $buildDir ($stage + '.java')
  $source = [System.IO.File]::ReadAllText($original)
  $source = [regex]::Replace($source, 'ROOT="[^"]*"', ('ROOT="' + $nativeRoot + '"'))
  [System.IO.File]::WriteAllText($target,$source,[System.Text.UTF8Encoding]::new($false))
  $compileStart = Get-Date
  Push-Location -LiteralPath $buildDir
  try {
    Write-Output ('Building ' + $stage)
    & $compiler ($stage + '.java')
    $classPath = Join-Path $buildDir ($stage + '.class')
    if (-not (Test-Path -LiteralPath $classPath) -or (Get-Item -LiteralPath $classPath).LastWriteTime -lt $compileStart.AddSeconds(-2)) {
      throw ('Fresh class missing for ' + $stage)
    }
    $batchLog = Join-Path $projectRoot ('logs\rebuild_' + $stage + '.log')
    $consoleLog = Join-Path $projectRoot ('logs\rebuild_' + $stage + '.console.log')
    & $batch -np 2 -inputfile ($stage + '.class') -batchlog $batchLog *> $consoleLog
    $messages = [System.IO.File]::ReadAllText($consoleLog)
    if ($LASTEXITCODE -ne 0 -or $messages -match '(?m)^Error:|Exception|Failed to find a solution|Unknown property') {
      throw ('Native stage needs investigation. See ' + $consoleLog)
    }
    if ($messages -notmatch 'SOLVED|SAVED_WITH_NATIVE_EXPORTS') {
      throw ('Native completion marker missing. See ' + $consoleLog)
    }
  } finally { Pop-Location }
}
Write-Output 'Native stages completed. Inspect exported tables and compare the independent references before accepting a new result.'
Write-Output 'The saved reference outputs are not automatically replaced by learner mastery credit.'
