$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$configPath = Join-Path $repoRoot "bridge.config.json"

function Get-BridgeConfig {
    param(
        [string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        throw "Missing config file: $Path"
    }

    try {
        $rawConfig = Get-Content -LiteralPath $Path -Raw
        $parsedConfig = $rawConfig | ConvertFrom-Json
    }
    catch {
        throw "Invalid config file: $Path. $($_.Exception.Message)"
    }

    if ($null -eq $parsedConfig.poll_seconds -or [int]$parsedConfig.poll_seconds -lt 1) {
        throw "Invalid config value: poll_seconds must be an integer greater than 0."
    }

    if ([string]::IsNullOrWhiteSpace([string]$parsedConfig.prompt_folder)) {
        throw "Invalid config value: prompt_folder is required."
    }

    return [pscustomobject]@{
        poll_seconds = [int]$parsedConfig.poll_seconds
        auto_open_vscode = [bool]$parsedConfig.auto_open_vscode
        auto_open_prompt_file = [bool]$parsedConfig.auto_open_prompt_file
        copy_to_clipboard = [bool]$parsedConfig.copy_to_clipboard
        prompt_folder = [string]$parsedConfig.prompt_folder
    }
}

$config = Get-BridgeConfig -Path $configPath
$pollSeconds = $config.poll_seconds
$autoOpenVsCode = $config.auto_open_vscode
$autoOpenPromptFile = $config.auto_open_prompt_file
$copyToClipboard = $config.copy_to_clipboard
$promptFolder = Join-Path $repoRoot $config.prompt_folder
$doneFolder = Join-Path (Split-Path -Parent $promptFolder) "done"

if (-not (Test-Path -LiteralPath $promptFolder)) {
    New-Item -ItemType Directory -Path $promptFolder -Force | Out-Null
}

if (-not (Test-Path -LiteralPath $doneFolder)) {
    New-Item -ItemType Directory -Path $doneFolder -Force | Out-Null
}

$codeCommand = Get-Command code -ErrorAction SilentlyContinue
$openedRepoInCode = $false
$processedPrompts = New-Object 'System.Collections.Generic.HashSet[string]'
$lastGitError = $null

function Open-RepoInVsCode {
    param(
        [string]$RepoPath
    )

    if (-not $script:autoOpenVsCode) {
        return
    }

    if (-not $script:codeCommand) {
        Write-Warning "VS Code command 'code' was not found on PATH."
        return
    }

    if (-not $script:openedRepoInCode) {
        & $script:codeCommand.Path $RepoPath | Out-Null
        $script:openedRepoInCode = $true
    }
}

function Open-PromptFileInVsCode {
    param(
        [string]$FilePath
    )

    if (-not $script:autoOpenPromptFile) {
        return
    }

    if (-not $script:codeCommand) {
        Write-Warning "VS Code command 'code' was not found on PATH."
        return
    }

    & $script:codeCommand.Path -g $FilePath | Out-Null
}

function Get-NewestPromptFile {
    param(
        [string]$FolderPath
    )

    $files = Get-ChildItem -LiteralPath $FolderPath -File -Recurse -ErrorAction SilentlyContinue |
        Where-Object {
            $_.Extension -in @(".md", ".txt") -and
            $_.Name -notmatch '(?i)(example|sample|test)'
        } |
        Sort-Object LastWriteTimeUtc -Descending

    return $files | Select-Object -First 1
}

function Get-PromptKey {
    param(
        [System.IO.FileInfo]$File
    )

    return "{0}|{1}|{2}" -f $File.FullName, $File.LastWriteTimeUtc.Ticks, $File.Length
}

function Invoke-GitPullQuietly {
    $gitOutput = & git -C $script:repoRoot pull --quiet 2>&1
    $gitExitCode = $LASTEXITCODE

    if ($gitExitCode -eq 0) {
        $script:lastGitError = $null
        return
    }

    $message = ($gitOutput | ForEach-Object { "$_" }) -join [Environment]::NewLine

    if ([string]::IsNullOrWhiteSpace($message)) {
        $message = "git pull failed with exit code $gitExitCode."
    }

    $message = $message.Trim()

    if ($message -ne $script:lastGitError) {
        Write-Warning ("git pull failed: {0}" -f $message)
        $script:lastGitError = $message
    }
}

function Move-PromptToDone {
    param(
        [System.IO.FileInfo]$PromptFile
    )

    $destinationPath = Join-Path $script:doneFolder $PromptFile.Name

    if (Test-Path -LiteralPath $destinationPath) {
        $baseName = [System.IO.Path]::GetFileNameWithoutExtension($PromptFile.Name)
        $extension = [System.IO.Path]::GetExtension($PromptFile.Name)
        $suffix = Get-Date -Format "yyyyMMdd_HHmmss"
        $destinationPath = Join-Path $script:doneFolder ("{0}_{1}{2}" -f $baseName, $suffix, $extension)
    }

    Move-Item -LiteralPath $PromptFile.FullName -Destination $destinationPath
    return Get-Item -LiteralPath $destinationPath
}

function Print-And-HandlePrompt {
    param(
        [System.IO.FileInfo]$PromptFile,
        [string]$Content
    )

    Write-Host ""
    Write-Host ("=" * 80)
    Write-Host ("New prompt: {0}" -f $PromptFile.FullName)
    Write-Host ("Updated: {0}" -f $PromptFile.LastWriteTime)
    Write-Host ("=" * 80)
    Write-Host $Content
    Write-Host ("=" * 80)

    if ($script:copyToClipboard) {
        try {
            Set-Clipboard -Value $Content
        }
        catch {
            Write-Warning ("Failed to copy prompt to clipboard: {0}" -f $_.Exception.Message)
        }
    }

    Open-RepoInVsCode -RepoPath $script:repoRoot
    Open-PromptFileInVsCode -FilePath $PromptFile.FullName
}

Open-RepoInVsCode -RepoPath $repoRoot

while ($true) {
    try {
        Invoke-GitPullQuietly

        $latestPrompt = Get-NewestPromptFile -FolderPath $promptFolder

        if ($null -ne $latestPrompt) {
            $currentPromptKey = Get-PromptKey -File $latestPrompt

            if (-not $processedPrompts.Contains($currentPromptKey)) {
                $promptContent = Get-Content -LiteralPath $latestPrompt.FullName -Raw
                $archivedPrompt = Move-PromptToDone -PromptFile $latestPrompt
                Print-And-HandlePrompt -PromptFile $archivedPrompt -Content $promptContent
                $null = $processedPrompts.Add($currentPromptKey)
            }
        }
    }
    catch {
        Write-Warning ("Bridge loop error: {0}" -f $_.Exception.Message)
    }

    Start-Sleep -Seconds $pollSeconds
}
