@echo off
echo ¼¤»îÏµÍ³
slmgr.vbs /ckms
slmgr.vbs /ato

cscript "C:\Program Files (x86)\Microsoft Office\Office16\OSPP.VBS" /sethst:kms.yealink.com
cscript "C:\Program Files (x86)\Microsoft Office\Office16\OSPP.VBS" /act

cscript "C:\Program Files\Microsoft Office\Office16\OSPP.VBS" /sethst:kms.yealink.com
cscript "C:\Program Files\Microsoft Office\Office16\OSPP.VBS" /act
pause