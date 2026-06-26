## Usage

### Set Vars
appDataDir="/home/ec2-user/Proxy_YTCDL_WUI/proxyApps/appData"

cd proxyApps

### Create and start venv
python3 -m venv proxy_test_env
source proxy_test_env/bin/activate

#Python modules to install in the proxy_test_env virtual python environment
pip install Flask
pip install dominate
pip install urllib3==1.26.6
pip install youtube_comment_downloader


### Update "pageSketchBook.py" 'sys.path' with actual path.
sys.path.insert(0, '/home/ec2-user/Proxy_YTCDL_WUI/proxyApps/pyCode/')

### Update "pageSketchBook.py" 'homeIpAddress with EC2 public IP.
homeIpAddress = "http://<>

### Start Flask server
export FLASK_APP=proxyFlaskApp.py; flask run --host=0.0.0.0 &> $appDataDir/flaskOutput.log;

### run task in bg
ctrl + z
bg

### Verify start
ll appData/
less appData/flaskOutput.log

### Visit site
http://<ec2_public_ip>:5000/
