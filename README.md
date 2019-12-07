# Mail API microservice
### (mail-client-api)

## Description:
```
Microservice that can receive and process all messages from the local server mailbox.
Supports mail encoding variants: UTF-8, UTF-16-LE, CP1251, KOI8-R, KOI8-U, ISO-8859-1.
```

## Author:
- @artur0us

## Usage:
(Run as administrator/superuser)
- Windows: py main.py
- Linux: sudo python3 main.py
- ...

## Requirements:
### OS:
- Ubuntu
- Windows
- macOS
- *BSD
- ...
### Software:
- Python 3.x(should work w/ python 2.x)
- PIP3 for Python 3.x(similar to previous line)
- Mail software

### Python dependencies:
- quart
- python-dateutil
- html2text
- naiveBayesClassifier(will be replaced)

## Future plans:
- Built-in web client for viewing all messages
- Writing messages to databases
- Specific JSON API instead of REST API
- More features
- Refactoring and revising architecture?
- Optimizations?

## Other:
### Supervisor config:
```
[program:mail-api-microservice]
directory=/home/system_username/app_work_dir
command=python3 /home/system_username/app_work_dir/main.py
stderr_logfile=/home/system_username/app_work_dir/mail_api_errs.txt
stderr_logfile_maxbytes=1MB
stdout_logfile=/home/system_username/app_work_dir/mail_api_logs.txt
stdout_logfile_maxbytes=1MB
autostart=true
autorestart=true
user=root
stopsignal=KILL
numprocs=1
process_name=mail-api-microservice
```