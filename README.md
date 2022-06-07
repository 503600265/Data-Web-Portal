# BW CS Web Portal

This repository is to maintain and track all of the code used to create the BW Self Service Web Portal

## Name
Bates White Self Service Portal

## Description
This web application is meant to act as a self service location for Client Services to be able to access, and perform minor tasks, like basic OCR, file conversions, email data extractions, excel file merging, etc. without needing the assistance of the Data Engineering/TS team.

## Installation
To install and setup this repository, you can simply clone it to the server you are working on.

```
git config --global user.name "<user name>"
git config --global user.email "<user email>"
git config --global http.SslVerify flase
git clone git@gitlab.bateswhite.com:ts/dataengineering/bw-cs-web-portal.git
```

## Support
douglas.post@bateswhite.com
balaji.lakshmanan@bateswhite.com

## Project Status
I currently have this set up in Flask, but that in no way means it needs to stay that way, feel free to transition to another web application framework, but I added the Flask code in for you to look at. If you

```
cd bw-cs-web-portal/flask/DataWebPortal
flask run
```

the application will start in development mode, and you can go to http://localhost:4212 to see the current state of that applicaiton.
