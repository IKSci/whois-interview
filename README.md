# whois-interview

### Files
<b>Dockerfile</b> - file defining Docker image <br>
<b>requirements.txt</b> - contains list of dependancies <br>
<b>crawler.py</b> - python file containing Flask application <br>
<b>util_processing.py</b> - contain functions used to process queries <br>

### Building docker and running 
Navigate to the directory containing the `Dockerfile`. <br>
Build the Docker image using the following command:<br>
```sh
docker build -t flask-whois-app .
```
<br>After building Docker image, run it with following command:
```sh
docker run -d -p 5000:5000 flask-whois-app
```
You can run from github Packages using following command without building:
```sh
docker run -d -p 5000:5000 ghcr.io/iksci/whois-demo

```


### Running the app
Go to the http://127.0.0.1:5000/lookup_whois?domain_name=kiwi.kz <br>
Or any other IP address running on your system as shown below <br>
![image](https://github.com/IKSci/whois-interview/assets/70970615/4e1d63a9-7cda-47bb-893e-a9b091f1083a)

You can change domain which you will like to check by specifying `domain_name=` parameter

### Output

Returns information from ps.kz website in JSON format as following
```JSON
{
  "domain_name": "example.com",
  "status": "available" | "busy" | "error",
  "details": {
    "reason": "string",  // Optional, present only if status is "busy"
    "whois_data": {
      // ... WHOIS data fields (registrar, dates, etc.) if available
    }
  }
}
```

### Storage in SQL database
The application stores the WHOIS data in an SQLite database (whois_data.db) with the following structure:

<b>domain_name</b>: Primary key, string <br>
<b>status</b>: Status of the domain, string <br>
<b>details</b>: JSON formatted details of the WHOIS data, text

