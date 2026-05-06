# ec2-user-proxy-data.bash:

##Set env variables:
appDataDir="/home/ec2-user/Proxy_YTCDL_WUI/proxyApps/appData";
echo $appDataDir;

##Start venv. Install venv requirements. Start flask.
source proxy_test_env/bin/activate;
pip install -r requirements.txt
export FLASK_APP=proxyFlaskApp.py; flask run --host=0.0.0.0 --debug &> $appDataDir/flaskOutput.log;


##Run flask in background while logged out
Press "Ctrl + Z" to suspend the running command.
Type "bg" to resume it in the background.
Type "disown -h %1" (where %1 is the job number) to mark it so it survives logout.