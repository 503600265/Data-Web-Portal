# BW CS Web Portal

This repository is to maintain and track all of the code used to create the BW Self Service Web Portal

## Name
Bates White Self Service Portal

## Description
This web application is meant to act as a self service location for Client Services to be able to access, and perform minor tasks, like basic OCR, file conversions, email data extractions, excel file merging, etc. without needing the assistance of the Data Engineering/TS team.

## Set Up
To install and setup this repository, you can simply clone it to the server you are working on.

```
git config --global user.name "<user name>"
git config --global user.email "<user email>"
git config --global http.sslVerify flase
git clone git@gitlab.bateswhite.com:ts/dataengineering/bw-cs-web-portal.git
```
Or
```
git clone https://gitlab.bateswhite.com/ts/dataengineering/bw-cs-web-portal.git
```

## Support
douglas.post@bateswhite.com
balaji.lakshmanan@bateswhite.com

## Run 
Install required packages
```
pip install -r requirements.txt
```
Run from Localhost:
```
python manage.py runserver
```
If you visit http://127.0.0.1:8000/, you should be able to see the website to be tested! 





