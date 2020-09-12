[General]
SyntaxVersion=2
BeginHotkey=121
BeginHotkeyMod=0
PauseHotkey=0
PauseHotkeyMod=0
StopHotkey=123
StopHotkeyMod=0
RunOnce=1
EnableWindow=
MacroID=222dc6e6-830d-49ba-86fc-03d0233a1f2d
Description=裁判文书网数据获取
Enable=1
AutoRun=0
[Repeat]
Type=0
Number=1
[SetupUI]
Type=1
QUI=Form1
[Relative]
SetupOCXFile=
[Comment]

[Attachment]
UEsDBBQAAgAIAKQzLFHck0KxaQEAAOYcAAAOABEAz8LSu9KzdGVtcC5ibXBVVA0AB75qXF++alxfvmpcX+2YMQ6CMBSG9RYOjg6ewAM0rp6ClRtwAVamHsGVxM07YIKMhNW6EQ5A6h9rXho0AhqxbfqnTUxLyv/1vVdM2e6ynN21QV+jb9FX6PPZ4j6ePuZ1SS+vCVXXdVVVRVGcjRdMwioMvwQRQpRl2TRN27bmbztMwioMw/ZzRDBuBUWHCLY70UG8gGljXcA2zOsjSD/rgkKhgXl9BNVk75HVMe9ZPItpLCcpWbCX2f4bD0mGRWI0ceAvH8CXg0XHE4/NZyGFhyuI0gier/r6GBzyCqNYiCgJ4iTLgRCCQhwtyjElxnPKMfzWo6NPTcmC5MeuSpl/w5IKmUb8jyyqQikrVPL3Nnq+w5IEnDZkSha8SJ1FvUfN8Lj8iyWM+Kgi7WUZPmVs7b9JRbtYSKruPljTQBZ1bnxQemNZ6P/G+zbqWEals4D3rql/cX4RF6PkWTzLxCwu3V24dKfk0l2fdOgOlqLjxt24l9ePdANQSwMEFAACAAgAijQsUT9qU73nAAAAdggAAAwAEQBuZXh0UGFnZS5ibXBVVA0AB3VsXF91bFxfdWxcX3PyLeNgAAMzINYAYh0gFgBiRgYJsLgDVB4Z/B8FOMC5//+dkpf/P7ucEkMmngUa0gFEzzdPx6rgOdCW6l3npnfQzg1wkLP5BdAlG6qBdr1ANh8oiMcK6roB7pKJyR0Tz14EWp0DtP35LjrEBQQ4Tb8IjwsgGzk0kKWIcQMwcoG++P//IiVu2PD8/4bq6WS4AZJy4KEHiVyCCK4ezQ0Tk6fDPUKMG4AKIGkbV9IlIxxIdUNO9XRiEg/xbiBeiuppEk+U0ccNaCUS8WbSwg2Q9IwnacHLVfyIpOwJTIFOydMJmolcYowCAFBLAQIXCxQAAgAIAKQzLFHck0KxaQEAAOYcAAAOAAkAAAAAAAAAIACAgQAAAADPwtK70rN0ZW1wLmJtcFVUBQAHvmpcX1BLAQIXCxQAAgAIAIo0LFE/alO95wAAAHYIAAAMAAkAAAAAAAAAIACAgaYBAABuZXh0UGFnZS5ibXBVVAUAB3VsXF9QSwUGAAAAAAIAAgCIAAAAyAIAAAAA


[Script]
Delay 5000
startDate = cdate("2017-01-01")

Do

	MoveTo 565, 400
	LeftClick 1
	Delay 2000
	
	MoveTo 1091, 608
	LeftClick 1
	//删除原有区域
	Delay 500
	
	KeyDown 17, 1
	KeyPress 65, 1
	KeyUp 17, 1
	Delay 500
	KeyPress "BackSpace", 1
	
	Delay 2000
	
	
	y = Year(startDate)
	m = Month(startDate)
	d = Day(startDate)
	
	SayString y
	KeyPress "-", 1
	SayString m
	KeyPress "-", 1
	SayString d
	Delay 1000
	MoveTo 1319, 617
	LeftClick 1
	Delay 2000
	
	MoveTo 1229, 610
	LeftClick 1
	//删除原有区域
	Delay 500	
	KeyDown 17, 1
	KeyPress 65, 1
	KeyUp 17, 1
	Delay 500
	KeyPress "BackSpace", 1


	
	Delay 1000
	
	SayString y
	KeyPress "-", 1
	SayString m
	KeyPress "-", 1
	SayString d
	Delay 1000
	MoveTo 1319, 617
	LeftClick 1
	Delay 1000
	
	startDate = startDate + 1
	

	MoveTo 863, 817
	LeftClick 1	
	Delay 2000



	//获取对应日期的文书
	MouseWheel -50
	
	MoveTo 1306, 827
	delay 1000
	LeftClick 1
	delay 1000
	
	MoveTo 1312, 888
	delay 1000
	LeftClick 1
	delay 1000
	
	
	
	Do
		//向上滚动
		delay 1000
		MouseWheel 50
		delay 1000
		
		//全选
		MoveTo 1586, 637
		delay 1000
		LeftClick 1
		delay 1000
		
		//点击批量下载
		MoveTo 1764, 641
		delay 1000
		LeftClick 1
		Delay 2000
		
		//清除掉下载框	
		MoveTo 1901, 1014
		LeftClick 1
		Delay 1000
		
		//再次向下滚动，点击下一页
		MouseWheel - 50
		Delay 3000
		
		//找图
		FindPic 526,775,1666,867,"C:\Users\Administrator\Desktop\每页15条.bmp",0.9,intX,intY
		If intX > 0 And intY > 0 Then 
			MoveTo intX-25, intY+10
			
			Delay 500
			FindPic 526,775,1666,867,"C:\Users\Administrator\Desktop\pressNextPage.bmp",0.9,intX,intY
			//如果icon改变，则点击
			If intX > 0 And intY > 0 Then
				LeftClick 1
				Delay 2000
			//如果icon不再发生改变，则break
			Else 
				exit do
			End If
			
		End If
		
	Loop

	//MessageBox "Done！"
	delay 1000
	MouseWheel 50
	delay 2000
Loop

