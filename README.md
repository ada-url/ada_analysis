# ada_analysis
Repository of benchmarking results for the ada-url library

Experimental results are found in jsurl/ and overall/. They cover two systems (Apple M2 and AMD Rome).

We also have data regarding the characteristics of URLs in big_url_set. This repository contains two CSV files. For each URL in a set, on a given system, we include the number of cycles and instructions needed to process the URL as well as many other attributes of the URL, including its protocol type, length of the path and so forth.
You can open CSV files in a spreadsheet tool. The performance results are not primary: these files are used mostly to understand the statistical characteristics of URLs. The big_url_set is based on the URL collection at (github//ada-url/url-dataset/out.txt).


## Systems

The rome machine refers to an AMD Rome server (AMD EPYC 7262 8-Core Processor) running Ubuntu with GCC 11.3. The m2 machine refers to a MacBook Air 2022 with LLVM 14.

## Python scripts


We require a recent Python 3 interpreter. The Python scripts require pandas, numpy, sklearn, seaborn and matplotlib. 
You may be able to install these dependencies with `pip` or `pip3` as follows:

```
pip install pandas matplotlib scikit-learn numpy seaborn
```

(Replace `pip` with `pip3` if needed.)


### Overall data (Google benchmark)

To collect the data, see `overall/README.md`.

The overall data comes from various datasets and is produced by the google-benchmark executable `benchdata` from the main `ada-url/ada` repository.

You can process the overall data and generate the tables and figures.

```
python scripts/overall.py
```
(replace python by `python3` if needed)


### jsurl

The jsurl data refers to https://github.com/ada-url/js_url_benchmark


```
python scripts/jsurl.py
```
(replace python by `python3` if needed)
