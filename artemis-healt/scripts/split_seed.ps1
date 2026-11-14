$ErrorActionPreference = 'Stop'
$sqlRoot = Join-Path $PSScriptRoot 'sql'
$original = [IO.File]::ReadAllText((Join-Path $sqlRoot 'load_demo.sql'))
$marker = '$artemis_data$'
$start = $original.IndexOf($marker) + $marker.Length
$end = $original.IndexOf($marker, $start)
$rows = @($original.Substring($start, $end - $start) | ConvertFrom-Json)
if ($rows.Count -ne 4320) { throw 'Expected 4320 observations' }
$folder = Join-Path $sqlRoot 'load_demo_parts'
[IO.Directory]::CreateDirectory($folder) | Out-Null
$utf8 = [Text.UTF8Encoding]::new($false)
for ($offset = 0; $offset -lt $rows.Count; $offset += 400) {
    $last = [Math]::Min($offset + 399, $rows.Count - 1)
    $payload = ConvertTo-Json -InputObject @($rows[$offset..$last]) -Depth 12 -Compress
    $part = $original.Substring(0, $start) + $payload + $original.Substring($end)
    # Keep creation and use inside one statement, even with transaction pooling.
    $part = $part.Replace("DO `$seed`$`nBEGIN", '').Replace("DO `$seed`$`r`nBEGIN", '')
    $part = $part.Replace('CREATE TEMP TABLE artemis_seed_input ON COMMIT DROP AS', "DO `$seed`$`nBEGIN`nCREATE TEMP TABLE artemis_seed_input ON COMMIT DROP AS")
    # Each part can resume independently, with full field comparison on conflicts.
    $part = [regex]::Replace($part, 'IF NOT EXISTS\(SELECT 1 FROM artemis.import_batches WHERE id=''[^'']+''\) THEN', 'IF TRUE THEN')
    $part = $part.Replace("}'::jsonb);", "}'::jsonb) ON CONFLICT(id) DO NOTHING;")
    $part = $part.Replace('FROM artemis_seed_input;', 'FROM artemis_seed_input WHERE true ON CONFLICT(id) DO NOTHING;')
    $part = [regex]::Replace($part, '(?s) IF \(SELECT count\(\*\) FROM artemis.observations WHERE import_batch_id=.*?THEN RAISE EXCEPTION ''Unexpected import count''; END IF;', '')
    if ($part -eq $original -or $part -notmatch 'jsonb\) ON CONFLICT') { throw 'Split transformation failed' }
    $number = 1 + [int][Math]::Floor($offset / 400)
    $target = Join-Path $folder ('{0:D2}_cargar.txt' -f $number)
    [IO.File]::WriteAllText($target, $part, $utf8)
    if ((Get-Item -LiteralPath $target).Length -gt 250000) { throw 'Part exceeds size budget' }
}
$verification = $original.Substring($original.LastIndexOf('SELECT count(*) AS observations,'))
$batch = 'c8c80d090337c7bbca882eaa2b6fd8ffcdd3dd04a580c98b834f553a35d0a2c1'
$check = @"
DO `$verify`$
BEGIN
 IF (SELECT count(*) FROM artemis.observations WHERE import_batch_id='$batch') <> 4320
 OR (SELECT count(*) FROM artemis.observations WHERE import_batch_id='$batch' AND value IS NULL) <> 92
 OR (SELECT count(DISTINCT profile_id) FROM artemis.observations WHERE import_batch_id='$batch') <> 6
 OR (SELECT count(DISTINCT indicator) FROM artemis.observations WHERE import_batch_id='$batch') <> 4
 THEN RAISE EXCEPTION 'Incomplete demo: execute all 11 parts before continuing'; END IF;
END `$verify`$;
$verification
"@
[IO.File]::WriteAllText((Join-Path $folder '12_verificar.txt'), $check, $utf8)
Get-ChildItem -LiteralPath $folder | Select-Object Name, Length
