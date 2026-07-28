Option Explicit

Dim shell, fileSystem, projectDirectory, pythonwPath, command

Set shell = CreateObject("WScript.Shell")
Set fileSystem = CreateObject("Scripting.FileSystemObject")

projectDirectory = fileSystem.GetParentFolderName(WScript.ScriptFullName)
pythonwPath = shell.ExpandEnvironmentStrings( _
    "%LocalAppData%\Programs\Python\Python313\pythonw.exe" _
)

If Not fileSystem.FileExists(pythonwPath) Then
    pythonwPath = "pythonw.exe"
End If

shell.CurrentDirectory = projectDirectory
command = """" & pythonwPath & """ -m pgzero """ & _
    projectDirectory & "\game.py"""

shell.Run command, 1, False
