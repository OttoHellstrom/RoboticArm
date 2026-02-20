@echo off
cd /d "C:\Users\Therese\Documents\RobotArmURDF"

echo Adding changes...
git add .

echo Commit message:
set /p msg="> "

git commit -m "%msg%"

echo Pushing to GitHub...
git push

echo Done!
pause
