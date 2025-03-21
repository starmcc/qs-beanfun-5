@echo off

pyinstaller --clean -w ^
--distpath="out_put/dist" ^
--workpath="out_put/build" ^
--add-data="resources/plugins/*;resources/plugins/" ^
--icon="resources/images/logo.png" ^
--name="Beanfun" ^
--uac-admin ^
src/QsBeanfun.py -y
