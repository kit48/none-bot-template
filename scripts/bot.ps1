$root = "E:\Workspaces\github\nonebot-template"

Clear-Host
Set-Location $root
"Call bot.py"
Invoke-Command -ScriptBlock { 
  pipenv shell "python bot.py"
}
