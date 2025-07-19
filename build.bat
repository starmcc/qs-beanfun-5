@echo off

pyinstaller --clean -w ^
--distpath="compile/dist" ^
--workpath="compile/build" ^
--icon="resources/images/logo.png" ^
--name="Beanfun" ^
--uac-admin ^
src/QsBeanfun.py -y