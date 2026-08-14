# Batch Content Generator — Stoic Wisdom × Zodiac Signs
# Requires: PowerShell 5.1+
# Sources sign data from the canonical `sign_master_data.json`.
# Purpose: Generate content calendar for N days
#
# USAGE: .\batch_content_generator.ps1 [-Days 30] [-OutputDir ..\..\03_CONTENT_CALENDAR\generated]
#
# NOTE: This is a secondary implementation. The primary generator is the Python version.
#       Both read from the same source of truth (sign_master_data.json).
#       If you change sign data, edit the JSON file — NOT the PowerShell arrays below.

param(
    [int]$Days = 7,
    [string]$OutputDir = "..\..\03_CONTENT_CALENDAR\generated"
)

# Locate the master data file (relative to this script's directory)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$MasterDataPath = Join-Path (Split-Path -Parent $ScriptDir) "sign_master_data.json"

if (-not (Test-Path $MasterDataPath)) {
    Write-Error "sign_master_data.json not found at: $MasterDataPath"
    Write-Error "Run the Python generator instead, or restore the JSON file."
    exit 1
}

# Read canonical sign data
$MasterData = Get-Content $MasterDataPath -Raw | ConvertFrom-Json
$Signs = $MasterData.signs
$Rotation = $MasterData."30_day_rotation"
$SignById = @{}
foreach ($s in $Signs) { $SignById[$s.id] = $s }

$ReelTypes = @(
    "Quote Narration",
    "Sign Comparison",
    "Rapid Wisdom",
    "Philosopher Speaks"
)

$WeekDays = @("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

# Ensure output directory exists
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

# Generate content calendar using the master data rotation
$Calendar = @()
$StartDate = (Get-Date).Date

for ($i = 0; $i -lt $Days; $i++) {
    $CurrentDate = $StartDate.AddDays($i)
    $DayOfWeek = $CurrentDate.DayOfWeek
    $WeekDayName = $WeekDays[$DayOfWeek]
    $WeekNumber = [Math]::Floor($i / 7) + 1

    # Use the curated rotation for the first 30 days, then cycle through signs
    if ($i -lt $Rotation.Count) {
        $DayEntry = $Rotation[$i]
        $SignId = $DayEntry.sign_id
        $Philosopher = $DayEntry.philosopher
        $Theme = $DayEntry.theme
    } else {
        $SignIndex = $i % $Signs.Count
        $SignId = $Signs[$SignIndex].id
        $Philosopher = $SignById[$SignId].philosopher
        $Theme = ""
    }

    $Sign = $SignById[$SignId]
    $SignName = $Sign.name
    $SignSymbol = $Sign.symbol
    $Element = $Sign.element

    $HasReel = $WeekDayName -in @("Monday","Wednesday","Friday")
    $ReelType = if ($HasReel) { $ReelTypes[$i % 4] } else { "No" }

    $CarouselType = "No"
    if ($WeekDayName -in @("Tuesday","Friday")) {
        $CarouselType = "Yes - Sign Spotlight"
    } elseif ($WeekDayName -eq "Sunday") {
        $CarouselType = "Yes - Weekly Forecast"
    }

    $Entry = [PSCustomObject]@{
        Day = $i + 1
        Date = $CurrentDate.ToString("yyyy-MM-dd")
        WeekDay = $WeekDayName
        Week = "Week $WeekNumber"
        Sign = $SignName
        Symbol = $SignSymbol
        Element = $Element
        Philosopher = $Philosopher
        Theme = $Theme
        DailyPost = "$SignSymbol $SignName - $Philosopher"
        Reel = $ReelType
        Carousel = $CarouselType
        Story = "Yes - Daily Prompt"
        Status = "PENDING"
    }
    $Calendar += $Entry
}

# Export to CSV
$CsvPath = Join-Path $OutputDir "content_calendar_$(Get-Date -Format 'yyyyMMdd').csv"
$Calendar | Export-Csv -Path $CsvPath -NoTypeInformation

# Export to readable Markdown
$MdPath = Join-Path $OutputDir "content_calendar_$(Get-Date -Format 'yyyyMMdd').md"
@"
# Content Calendar — Stoic Wisdom × Zodiac Signs
**Generated**: $(Get-Date -Format 'yyyy-MM-dd HH:mm')
**Days**: $Days
**Start Date**: $($StartDate.ToString('yyyy-MM-dd'))
**Source**: `sign_master_data.json`

---

$(($Calendar | Group-Object Week | ForEach-Object {
    $Week = $_.Name
    $Rows = $_.Group | ForEach-Object {
        "| $($_.Day) | $($_.Date) | $($_.WeekDay) | $($_.Symbol) $($_.Name) | $($_.Philosopher) | $($_.Theme) | $($_.DailyPost) | $($_.Reel) | $($_.Carousel) | $($_.Story) | $($_.Status) |"
    } -join "`n"

@"
## $Week

| Day | Date | WeekDay | Sign | Philosopher | Theme | Daily Post | Reel | Carousel | Story | Status |
|-----|------|---------|------|-------------|-------|------------|------|----------|-------|--------|
$Rows

"@
}) -join "`n")

---

## Legend
- **Daily Post**: Square image (1080×1080) — quote + sign
- **Reel**: Video (1080×1920) — narrated voiceover + visuals
- **Carousel**: Multi-slide (1080×1080) — deep dive or forecast
- **Story**: Vertical (1080×1920) — daily prompt
- **Status**: PENDING / DONE / SCHEDULED / POSTED
"@ | Out-File -FilePath $MdPath -Encoding utf8

Write-Host "✅ Calendar generated (from sign_master_data.json):"
Write-Host "   CSV: $CsvPath"
Write-Host "   MD:  $MdPath"
Write-Host ""
Write-Host "📋 Next step: Copy the output into ChatGPT using the prompt in"
Write-Host "   05_AI_WORKFLOWS\prompts\master_prompt_library.md (Prompt 1)"
Write-Host ""
Write-Host "💡 Tip: To update sign data, edit sign_master_data.json."
Write-Host "       The Python generator is the primary version; this PowerShell"
Write-Host "       version reads the same JSON for consistency."