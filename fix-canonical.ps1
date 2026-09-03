# Fix all canonical tags with /index/ pattern
$publicDir = "C:\Users\matte\dolarexpress-final\public"
$fileCount = 0
$fixedCount = 0

Get-ChildItem -Path $publicDir -Filter "*.html" -Recurse | ForEach-Object {
    $filePath = $_.FullName
    $content = Get-Content -Path $filePath -Raw
    $fileCount++

    # Check if file contains /index/ in canonical
    if ($content -match 'canonical.*href="[^"]*\/index\/"') {
        # Replace /index/" with /"
        $newContent = $content -replace 'canonical\s+href="([^"]*)\/index\/"', 'canonical" href="$1/"'

        # Also handle single line with /index/
        $newContent = $newContent -replace 'href="([^"]*)/index/"', 'href="$1/"'

        Set-Content -Path $filePath -Value $newContent -Encoding UTF8
        Write-Host "✅ Fixed: $($_.Name)"
        $fixedCount++
    }
}

Write-Host "`n✅ Total files processed: $fileCount"
Write-Host "✅ Files fixed: $fixedCount"
