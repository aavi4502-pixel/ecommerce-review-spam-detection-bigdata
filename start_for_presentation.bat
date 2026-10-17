@echo off
echo ======================================================================
echo    STARTING BIG DATA E-COMMERCE SPAM DETECTION CLUSTER FOR VIVA
echo ======================================================================
echo.

echo [0/4] Checking Docker Desktop status...
docker info >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Docker Desktop is not running. Launching Docker Desktop...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    echo Waiting for Docker Desktop engine to start...
    :wait_docker
    timeout /t 5 /nobreak >nul
    docker info >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo Still waiting for Docker engine...
        goto wait_docker
    )
    echo Docker engine is now READY!
)

echo.
echo [1/4] Starting Hadoop and Spark Docker Containers...
docker start namenode datanode1 datanode2 spark-master spark-worker
echo Containers started!
echo.

echo [2/4] Waiting 10 seconds for HDFS to initialize...
timeout /t 10 /nobreak >nul
docker exec namenode hdfs dfsadmin -safemode leave
echo Safe mode is OFF!
echo.

echo [3/4] Launching Spark UI Showcase (Port 4040)...
docker cp presentation_showcase.py spark-master:/tmp/presentation_showcase.py
docker exec -d spark-master bash -c "/spark/bin/spark-submit /tmp/presentation_showcase.py > /tmp/showcase.log 2>&1"
echo Spark UI is loading with 4 completed jobs and DAGs!
echo.

echo [4/4] Launching Interactive Web Dashboard (Port 5000)...
start python dashboard\run_dashboard.py
echo.

echo ======================================================================
echo    ALL SYSTEMS ARE ONLINE AND READY FOR YOUR PRESENTATION!
echo    - Dashboard:    http://localhost:5000/index.html
echo    - Spark Master: http://localhost:8080
echo    - Spark App UI: http://localhost:4040/jobs/
echo    - HDFS:         http://localhost:9870/explorer.html#/project
echo ======================================================================
pause
