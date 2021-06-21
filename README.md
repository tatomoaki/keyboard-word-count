# Keyboard Word Count

Terminal script to keep track of words typed through out the day. Basic analysis on terminal including word count, file size and simple visual table on word frequency.

## Usage

1. Create virtual environment

```
python3.7 -m venv env
```
2. Activate environment & install packages from requirements file 
```
source env/bin/activate

pip install -r requirements.txt

```
3. Run script in backgroud using nohup 
```
nohup python main.py & 
```
4. Type away and retrieve summary later

## Report
To retrieve summary of your report

```
python main.py --report yes --interval 60
```
## License
MIT License, see [MIT](license)

