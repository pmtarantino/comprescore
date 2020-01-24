# CompreScore

Method to measure diversity of T-Cell receptors using compression libraries.

# Usage

## Installation:

You need to have Python 3.6.8 installed and PIP. After that, clone this repo and create a virtual enviroment:

```python3 -m venv .env```

Activate the virtual enviroment:

```source .env/bin/activate```

Once the virtual enviroment is activated, install the dependencies:

```pip install -r requirements.txt```

## Test

To test the experiments used on the thesis, simply run `testmodel.py`. The paramenters available are:

`iter` : Amount of iterations to run the experiments. More iterations will return a _better_ average but it will take more time.
`compressor` : Library to use as compressor. Available: GZIP, B2, LZMA and ZLIB.
`blosum` : If use the Blosum reduction. It improves the error.

To run with your own data and get the score, the file to use is `comprescore.py`. It has the same parameters as `testmodel.py`, plus a new one, `input`, which is the path to the input file. The format of the input file is `{QUANTITY} {SEQUENCE}`, one per line. You can check the `example_file.txt` if you still have doubts (by the way, that's the default value for the `input` parameter)