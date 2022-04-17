set PYTHONPATH=%PYTHONPATH%;D:\repository\notes_scripts\python_learn_note
set DIR=D:\repository\notes_scripts\python_learn_note\ut_source\test\case
for /R %DIR% %%f in (test_*.py) do (
nosetests %%f
)
nosetests --with-coverage %DIR%
pause
