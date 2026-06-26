#!/bin/bash
# Use this for your user data (script from top to bottom)
#if running manually from CLI
#sudo su


writeLog () {
	logMessage=$1
	runDate=`date +"%Y-%m-%d-%T"`
	echo "$runDate: $logMessage" >> /home/userData_logfile.txt
}

installLinuxPackages() {
	yum update -y
	
	# install httpd (Linux 2 version)
	yum install -y httpd
	writeLog "installLinuxPackages: httpd installed"
	
	#install git
	yum install -y git
	writeLog "installLinuxPackages: git installed"
}

moveFiles() {
	#Create directories for apps to run and store data.
	#mkdir proxyApps
	cd /home
	git clone https://github.com/EmergenceProxy/ByProxy.git

	writeLog "moveFiles: git repo cloned"
	#mkdir proxyHome
	moveHtmlFiles
	movePythonFiles
	
	rm -rf ByProxy/
	writeLog "moveFiles: git repo removed"
}

moveHtmlFiles(){
	htmlFilesDir="/var/www/html"
	#clone httpd code to html dir
	#mv /home/ByProxy/AWS/AWShtml/index.html $htmlFilesDir/.
	#mv /home/ByProxy/AWS/AWSpython/proxyApps/login.html $htmlFilesDir/.
	#mv /home/ByProxy/AWS/AWSpython/proxyApps/login2.html $htmlFilesDir/.
	#mv /home/ByProxy/AWS/AWSpython/proxyApps/login2_script.js $htmlFilesDir/.
	#mv /home/ByProxy/AWS/AWSpython/proxyApps/login2_style.css /$htmlFilesDir/.
	
	#Todo: Move html related files in github to AWShtml folder
	mv /home/ByProxy/AWS/AWShtml/* /var/www/html
	writeLog "moveHtmlFiles: html files moved"
}
movePythonFiles(){
	mv /home/ByProxy/AWS/AWSpython/proxyApps /home/
	writeLog "movePythonFiles: python files moved"
}

startServices(){
	writeLog "startServices: Initalize"
	ytcDLWorkingDir="/home/proxyApps/appData/ytcData"
	
	#startHttpd
	systemctl start httpd
	systemctl enable httpd
	
	#startYtcdl
	startYtcdl
	
	writeLog "startServices: Complete"
}

startYtcdl(){

	appScriptsDir="/home/proxyApps"
	appDataDir="/home/proxyApps/appData"
	userDataDir="/home/proxyHome"
	
	if [ -d "$appScriptsDir" ]; then
		writeLog "startYtcdl: Directory $appScriptsDir exists."
		cd proxyApps
		#mkdir appData

		python3 -m venv proxy_test_env
		writeLog "startYtcdl:Directory $appScriptsDir exists."

		#Activate virtual env
		source proxy_test_env/bin/activate
		writeLog "startYtcdl: virtual env activated."
		
		#Deactivate virtual env
		#

		#Python modules to install in the proxy_test_env virtual python environment
		pip install Flask
		pip install dominate
		pip install urllib3==1.26.6
		pip install youtube_comment_downloader
		writeLog "startYtcdl: virtual env modules installed."

		#touch hello.py

		#Create test pages:
		echo "from flask import Flask
		app = Flask(__name__)
		@app.route('/')
		def hello_world():
			return 'Hello world!'" > /home/proxyApps/hello.py

		echo "from flask import Flask
		app = Flask(__name__)
		@app.route('/')
		def hello():
			return 'Hello from Flask on EC2!'

		if __name__ == '__main__':
			app.run(host='0.0.0.0', port=5000)"> /home/proxyApps/helloEC2.py

		#5 Load test page into flask
		export FLASK_APP=helloEC2.py

		#6 Load app page into flask, and run listening to any/httpd for requests.
		export FLASK_APP=proxyFlaskApp.py; flask run --host=0.0.0.0 &> $appDataDir/flaskOutput.log;
		# export FLASK_APP=proxyFlaskApp.py; flask run --host=0.0.0.0 --debug
		writeLog "startYtcdl: flask activated."

		# When testing wwith no httpd:
		# look for log similar to "Running on http://123.0.0.1:5000"
		# Copy the actual ipAddress:" Running on <yourFoundIP>"
	else
		writeLog "startYtcdl: Error: Directory $appScriptsDir does not exist."
		writeLog "startYtcdl: Exiting"
	fi
}
###################################################################################
writeLog "Main: user data start"

installLinuxPackages
moveFiles
startServices

writeLog "Main: user data completed!"