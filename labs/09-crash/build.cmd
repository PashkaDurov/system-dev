@echo off
cl /nologo /Zi /Od /W4 /D_CRT_SECURE_NO_WARNINGS crash.c /Fe:crash.exe
if errorlevel 1 exit /b 1
cl /nologo /Zi /Od /W4 /D_CRT_SECURE_NO_WARNINGS /fsanitize=address crash.c /Fe:crash_asan.exe
if errorlevel 1 exit /b 1
cl /nologo /Zi /Od /W4 /D_CRT_SECURE_NO_WARNINGS /fsanitize=address crash_fixed.c /Fe:crash_fixed.exe
