; Inno Setup Script for FileFlip
[Setup]
AppName=FileFlip
AppVersion=1.0
DefaultDirName={pf}\FileFlip
DefaultGroupName=FileFlip
UninstallDisplayIcon={app}\FileFlip.exe
OutputDir=.
OutputBaseFilename=FileFlipSetup
Compression=lzma
SolidCompression=yes

[Files]
Source: "C:\Users\divye\OneDrive\Documents\Programming Projects\FileFlip\dist\FileFlip.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\FileFlip"; Filename: "{app}\FileFlip.exe"
Name: "{commondesktop}\FileFlip"; Filename: "{app}\FileFlip.exe"

[Run]
Filename: "{app}\FileFlip.exe"; Description: "Register Context Menu"; Flags: nowait postinstall runascurrentuser

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
