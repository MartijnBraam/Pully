# Pully: Gitlab webhook receiver

This is a simple Python 2 script without any module dependencies that can receive gitlab webhooks and run a command for them.

The simpelest example:

```bash
$ ./pully.py --source="1.2.3.4" --exec-push="git pull"
```

This listens to port 30123 and waits for a Gitlab webhook from the IP address 1.2.3.4 and executes the git pull command.

If no source IP is defined the filter defaults to localhost so this command is never accidentally exposed to everyone on the internet

## More examples

Only pull when new tags are pushed:

```bash
$ ./pully.py --source="1.2.3.4" --exec-tag="git pull"
```

Run multiple commands when pulling new versions

```bash
$ pully.py --source="1.2.3.4" --exec-push="git reset --hard; git pull; drush cache-clear all"
```

Bind to another port than 30123

```bash
$ ./pully.py --source="1.2.3.4" --port=1337 --exec-push="git pull"
```

Run the commands in another working directory

```bash
$ ./pully.py --source="1.2.3.4" --cwd="/var/www/website" --exec-push="git pull"
```

## Options

```
usage: pully.py [-h] [--port PORT] [--source SOURCE] [--exec-push EXEC_PUSH]
                [--exec-tag EXEC_TAG]

Pully Gitlab webhook receiver

optional arguments:
  -h, --help            show this help message and exit
  
  --port PORT, -p PORT  Port to listen on (default: 30123)
  
  --source SOURCE, -s SOURCE
                        Source IP of the Gitlab webhooks (default: 127.0.0.1)
                        
  --exec-push EXEC_PUSH
                        Command to execute when commits are pushed to the
                        repository (default: nothing)
                        
  --exec-tag EXEC_TAG   Command to execute when tags are pushed to the
                        repository (default: nothing)
                        
  --cwd CWD, -c CWD     Define the working directory the commands are executed
                        in
```