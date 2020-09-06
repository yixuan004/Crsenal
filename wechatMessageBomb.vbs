'使用方法：复制一句话，打开聊天框后运行此脚本
'脚本具有一定可扩展性，如有实际用途场景课后续补充

Set WshShell = CreateObject("WScript.Shell")

WshShell.AppActivate"Curious;"
WScript.Sleep 2000

for i=1 to 5
WScript.Sleep 100
WshShell.Sendkeys "^v"
WshShell.Sendkeys i

WshShell.Sendkeys "{ENTER}"
'WshShell.SendKeys "^{ENTER}"

Next
