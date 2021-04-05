docker build --target dev -t telegram_watcher .
docker run -it -v $PWD:/app telegram_watcher python app/main.py filter-fx-nv