@ SET EXCLUDE_AUTHOR=YourNameHere
@ SET PROJECT_ID=00000000
@ SET TODOIST_API_KEY=ffffffffffffffffffffffffffffffffffffffff

@ if %PROJECT_ID% == 00000000 echo Configure the script first. & goto END

CHCP 65001
SET PYTHONIOENCODING=utf-8

SET RUNCMD=Python.exe monitor-moddb.py

%RUNCMD% NitpickerModpack
%RUNCMD% YetAnotherCampfireSaving
%RUNCMD% Kiltrak
%RUNCMD% ToggleScope

@ ECHO Done.

:END