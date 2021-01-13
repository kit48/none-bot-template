$root = "D:\Program Files\go-cqhttp"
$qq = "./go-cqhttp-v0.9.35-fix1-windows-amd64.exe"

Clear-Host
Set-Location $root
"Call QQ client"
Invoke-Command -ScriptBlock {
  & $qq
}
