# nose-env-config
Plugin for configuration env variables with nose

Available options:    
Set variables on nose run:    
```
--env-vars='var1=val1,var2=val2'
```
Set file to read from:
```
[env]
var1=val1
var2=val2
```
and set path to it:
```
--env-vars-file=/path/to/created/file
```
If you don't want to pass any flags you can go to ways:
1. call your file `.nose-env` and put into directory you launch your tests from;    
2. set environment variable `NOSE_ENV_FILE` with path to your file
