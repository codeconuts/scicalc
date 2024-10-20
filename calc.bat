@echo off
echo This is a Python interactive interpreter. Some guidelines:
echo.
echo 1. Units are supported for numbers, physical constants are supported.
echo 2. Numbers with uncertainties are supported. "ufloat(0.1,0.23)" constructs the number 0.1+/-0.23
echo 3. Numpy is supported, including for numbers with uncertainties
echo 4. To import number array from excel, call from_excel(), then paste the column of numbers copied from excel, 
echo    and hit ENTER twice. Errors will be automatically generated as if the values are from multimeter.
echo    Call from_excel(False, oscilloscope) to generate errors as if the values are from oscilloscope.
echo    If you want to import errors as well, call from_excel(True) instead.
echo 5. To export number array to excel, call to_excel(nparr), copy the printed numbers and paste to excel.
echo 6. Use minimum(a,b) instead of min(a,b), since "min" is the unit for minute.
echo.
.\.venv\scripts\python -i .\calc.py