@echo off
echo VetrAI CSS Quick Fix
echo ==================

echo Clearing Next.js cache...
cd frontend\studio
if exist .next rmdir /s /q .next
if exist node_modules\.cache rmdir /s /q node_modules\.cache

cd ..\admin
if exist .next rmdir /s /q .next
if exist node_modules\.cache rmdir /s /q node_modules\.cache

echo Restarting development servers...
cd ..\..

echo Starting Studio UI...
start "Studio UI" cmd /k "cd frontend\studio && npm run dev"

echo Starting Admin Dashboard...  
start "Admin Dashboard" cmd /k "cd frontend\admin && npm run dev"

echo Fix complete! Check http://localhost:3000 and http://localhost:3001

pause
