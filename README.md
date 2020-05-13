# finance
Python Flask finance tracker


docker build -t finance:latest .

docker save -o finance.tar finance:latest


docker run -p 4568:5000 --rm finance

docker run -v docktest_vol:/home/docktest/storage -it --rm docktest
