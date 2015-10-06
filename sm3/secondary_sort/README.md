Local test mr task

$ head -n 100 /home/sandello/logs/access.log > input.txt
$ cat input.txt | ./mapper.py
$ cat input.txt | ./mapper.py | less -S
$ cat input.txt | ./mapper.py | sort -t $'\t' -k1,1 -k2,2 | less -S
$ cat input.txt | ./mapper.py | sort -t $'\t' -k1,1 -k2,2 | ./reducer.py
