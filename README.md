# PBAD_mathematical-modelling-using-LLMs
### Requirements
- Python3

### Create OpenRouter account
Register at [OpenRouter]{https://openrouter.ai}, charge your account with funds https://openrouter.ai/credits and generate token https://openrouter.ai/keys. Save it somewhere.

### Clone repository
```
git clone https://github.com/GRO4T/PBAD_mathematical-modelling-using-LLMs.git
```
or
```
git clone git@github.com:GRO4T/PBAD_mathematical-modelling-using-LLMs.git
```

### [Optional] Create python virtual environment
```
python3 -m venv .venv
```
and activate it
```
source ./.venv/bin/activate
```

### Install required dependencies
```
pip install -r ./requirements.txt
```

### Benchmark
To run benchmarks:
```
OPENROUTER_API_KEY=<OPENROUTER_TOKEN> python3 benchmark.py --model nousresearch/nous-capybara-7b:free
```
or
```
export OPENROUTER_API_KEY=<OPENROUTER_TOKEN>
python3 benchmark.py --model nousresearch/nous-capybara-7b:free
```
