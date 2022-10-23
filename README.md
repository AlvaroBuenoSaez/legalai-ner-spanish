# legalai-new-spanish

## Overview


## Set up
Install a venv in the folder you will clone the project:
``` 
python3 -m venv . 
source bin/activate
```
And now, you can clone the repository:
```
git clone https://github.com/AlvaroBuenoSaez/legalai-ner-spanish.git
```

Finally, enter to legalai-ner-spanish and instlal requirements.txt:
```
cd legalai-ner
pip install -r src/requirements.lock
```

## Folder structure

This project uses [Kedro](https://kedro.readthedocs.io/en/stable/) which contains:
- conf: defines data types and parameters
- data: contains the data ordered in 9 differend levels depending on its processing level.
- docs/source: TODO
- logs: TODO
- notebooks: TODO
- src: source code.

## Use

There are 1 pipeline which can be run as:
```
kedro run -p pipeline_name

```

The pipelines are:
- preprocess: processes html files to a single json, generates and plots results and extracts relevant data in html as names, descriptions, law quotes, etc.

## Results
<img align="left" src="https://github.com/AlvaroBuenoSaez/legalai-ner-spanish/blob/main/data/08_reporting/bar_relevant_data.png">
