# whois-interview

### Files
<b>Dockerfile</b> - file defining Docker image <br>
<b>requirements.txt</b> - contains list of dependancies <br>
<b>crawler.py</b> - python file containing Flask application <br>
<b>util_processing.py</b> - contain functions used to process queries <br>

### Building docker and running locally
Navigate to the directory containing the `Dockerfile`. <br>
Build the Docker image using the following command:<br>
```sh
docker build -t flask-whois-app .
```
<br>After building Docker image, run it with following command:
```sh
docker run -d -p 5000:5000 flask-whois-app
```
Go to the localchost:5000/lookup_whois?domain_name=kiwi.kz <br>
You can change domain which you will like to check by specifying `domain_name=` parameter

