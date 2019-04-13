# CS4242 Mini-project

## Getting Started

Make sure you are using a virtual environment of some sort (e.g. `virtualenv` or
`pyenv`).

```
npm install
pip install -r requirements.txt
./manage.py migrate
./manage.py loaddata sites
npm run dev
```

Browse to http://localhost:3000/

## Django database functions

Navigate to the directory with manage.py and run the following in your terminal:

### Loading data
Unzip wikihow.json and instructables.json into mysite/json_data/ .
```
./manage.py load_json --where/--example/--store_wh/--store_in
```
| Command     | Detail                                      |
|-------------|---------------------------------------------|
| `--where`     |  returns the current location of manage.py  |
| `--store_wh`  |  stores data from wikihow.json              |
| `--store_in`  |  stores data from instructables.json        |


### Clearing data
```
./manage.py clear_db --art --cat --sub --all
```
| Command     | Detail                      |
|-------------|-----------------------------|
| `--art`     | deletes all articles        |
| `--cat`     | deletes all categories      |
| `--sub`     | deletes all sub-categories  |
| `--all`     | deletes all of the above    |
