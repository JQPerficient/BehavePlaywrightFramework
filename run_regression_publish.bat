@echo off
setlocal EnableDelayedExpansion

echo ========================================
echo  REGRESSION AUTOMATION PIPELINE
echo ========================================

REM ---------------- CONFIGURACION ----------------
set PROJECT_DIR=%cd%
set REPORTS_REPO_DIR=..\automation-reports
set TEST_STATUS=PASSED
echo.

REM ---------------- 1. ACTIVAR VENV ----------------
echo [1/7] Activando entorno virtual...
call .venv\Scripts\activate

REM ---------------- INSTALAR DEPENDENCIAS ----------------
echo Instalando dependencias...
python -m pip install -r requirements.txt
echo.

REM ---------------- LIMPIAR LOG POINTER ----------------
if exist current_log_path.txt (
    echo Limpiando log de ejecución anterior...
    del current_log_path.txt
)
echo.

REM ---------------- 2. LIMPIAR ALLURE ----------------
echo [2/7] Limpiando resultados anteriores...
if exist allure-results rmdir /s /q allure-results
if exist allure-report rmdir /s /q allure-report
echo.

REM ---------------- 3. EJECUTAR REGRESSION ----------------
echo [3/7] Ejecutando pruebas @Regression...

python -m behave ^
 --format allure_behave.formatter:AllureFormatter ^
 -o allure-results ^
 --logging-level INFO ^
 --tags=@Regression

if errorlevel 1 (
    echo ❌ Tests FALLARON
    set TEST_STATUS=FAILED
) else (
    echo ✅ Tests PASARON
)
echo.

REM ---------------- 4. GENERAR REPORTE ALLURE ----------------
echo [4/7] Generando reporte Allure...
call allure generate allure-results -o allure-report --clean
echo.

REM ---------------- 5. PUBLICAR SOLO SI PASA ----------------
if "%TEST_STATUS%"=="PASSED" (
    echo [5/7] Publicando reporte en GitHub Pages...

    cd %REPORTS_REPO_DIR%

    echo Limpiando repo automation-reports...
    git rm -rf .
    git clean -fd

    echo Copiando nuevo reporte...
    xcopy /E /I "%PROJECT_DIR%\allure-report\*" .

    git add .
    git commit -m "Update Allure report - Regression"
    git push

    cd %PROJECT_DIR%
    echo ✅ Reporte publicado correctamente
) else (
    echo [5/7] ❌ Reporte NO publicado (tests fallaron)
)
echo.


REM ---------------- 6. ENVIAR EMAIL SIEMPRE ----------------
echo [6/7] Enviando email de notificacion...

if exist current_log_path.txt (
    for /f "usebackq delims=" %%a in ("current_log_path.txt") do (
        set LOG_FILE_PATH=%%a
    )

    echo Log del run encontrado: !LOG_FILE_PATH!
    python send_report.py %TEST_STATUS% "!LOG_FILE_PATH!"
) else (
    echo ⚠️ No se encontro current_log_path.txt
    python send_report.py %TEST_STATUS%
)

echo.


REM ---------------- 7. FIN ----------------
echo ========================================
if "%TEST_STATUS%"=="PASSED" (
    echo ✅ PIPELINE COMPLETADO - RESULTADO: PASSED
    echo 🌐 Reporte:
    echo https://jqperficient.github.io/automation-reports/
) else (
    echo ❌ PIPELINE COMPLETADO - RESULTADO: FAILED
    echo 📧 Se envio email notificando el fallo
)
echo ========================================

pause
endlocal