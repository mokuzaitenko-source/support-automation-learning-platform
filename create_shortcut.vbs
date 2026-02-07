Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = oWS.SpecialFolders("Desktop") & "\PyLearn Platform.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
    oLink.TargetPath = "C:\Users\alvin\TEst\introtodeeplearning\aca\.venv\Scripts\python.exe"
    oLink.Arguments = "app.py"
    oLink.WorkingDirectory = "C:\Users\alvin\TEst\introtodeeplearning\aca"
    oLink.Description = "Python Learning Platform - Modern UI"
    oLink.IconLocation = "C:\Users\alvin\TEst\introtodeeplearning\aca\.venv\Scripts\python.exe, 0"
oLink.Save

WScript.Echo "Desktop shortcut created successfully!"
