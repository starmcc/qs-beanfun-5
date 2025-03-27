@echo off

pyinstaller --clean -w ^
--distpath="compile/dist" ^
--workpath="compile/build" ^
--add-data="resources/plugins/*;resources/plugins/" ^
--icon="resources/images/logo.png" ^
--name="Beanfun" ^
--uac-admin ^
src/QsBeanfun.py -y