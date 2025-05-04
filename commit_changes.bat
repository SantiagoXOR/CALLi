@echo off
cd C:\Users\marti\Desktop\DESARROLLOSW\CALLi
git add scripts/security_check_local.py
git commit -m "fix(security): eliminar impresión de secretos en texto claro"
git push origin security-improvements
