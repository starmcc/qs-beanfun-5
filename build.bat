@echo off

pyinstaller --clean -w ^
--uac-admin ^
--name="Beanfun" ^
--icon="resources/images/logo.png" ^
--distpath="compile/dist" ^
--workpath="compile/build" ^
--exclude PyQt6.QtBluetooth ^
--exclude PyQt6.QtMultimedia ^
--exclude PyQt6.QtOpenGL ^
--exclude PyQt6.QtQuick ^
--exclude PyQt6.QtQml ^
--exclude PyQt6.QtSerialPort ^
--exclude PyQt6.QtSql ^
--exclude PyQt6.QtTest ^
--exclude PyQt6.QtWebSockets ^
src/QsBeanfun.py -y