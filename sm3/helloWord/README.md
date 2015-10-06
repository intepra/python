Local test mr task

$ head -n 100 /home/sandello/logs/access.log > input.txt
$ cat input.txt | ./mapper.py
$ cat input.txt | ./mapper.py | sort | ./reducer.py 
