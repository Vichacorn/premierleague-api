# premierleague-api
## setup
1. clone the project
2. `python -m venv env`
3. `source env/bin/activeated`
4. `pip install -r requirment.txt`
5. `java -jar openapi-generator-cli.jar  generate -i openapi/premier-league-api.yaml -o autogen -g python-flask`
##Used Rest API
1. open server by `python app.py`
2. go to the http://0.0.0.0:8080/premier-league/ui
