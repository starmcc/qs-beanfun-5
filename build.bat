@echo off

pyinstaller --clean -w ^
--uac-admin ^
--name="Beanfun" ^
--icon="resources/images/logo.ico" ^
--distpath="compile/dist" ^
--workpath="compile/build" ^
--exclude PySide6.QtBluetooth ^
--exclude PySide6.QtMultimedia ^
--exclude PySide6.QtOpenGL ^
--exclude PySide6.QtQuick ^
--exclude PySide6.QtQml ^
--exclude PySide6.QtSerialPort ^
--exclude PySide6.QtSql ^
--exclude PySide6.QtTest ^
--exclude PySide6.QtWebSockets ^
src/QsBeanfun.py -y