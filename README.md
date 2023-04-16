# OpenWPM-Data-Analytics

A repository for analyzing the results of a [OpenWPM](https://github.com/openwpm/OpenWPM) web crawl to find different types of
fingerprinting being preformed 

## Extraction of data from OpenWPM

We also maintain the repository [openwpm-mods](https://gitlab.com/wesleyancs-plp/openwpm-mods), which details in more depth what settings to use for OpenWPM.
In short ensure that:
- Instrument, at a minium, what is covered in the following [js_instrument_settings JSON](https://gitlab.com/wesleyancs-plp/openwpm-mods/-/blob/558ac99e65b9f51cbe51417f250928091c26516a/js_instrumentation_collections/additional_methods.json)
    - [OpenWPM docs of JavaScript dynamic instrumentation](https://github.com/openwpm/OpenWPM/blob/master/docs/Configuration.md#js_instrument)
- HTTP network request instrumenting is enabled, and `save_content` includes `"script"` to save the JavaScript files' source code. 
    - [OpenWPM docs on saving content from network requests](https://github.com/openwpm/OpenWPM/blob/master/docs/Configuration.md#save_content)
    - [OpenWPM docs on instrumenting http network requests](https://github.com/openwpm/OpenWPM/blob/master/docs/Configuration.md#http_instrument)
- The structured data is stored in a sqlite database under the name 'crawl-data.sqlite'
    - This is not a rigid requirement, another SQL implementation besides sqlite could easily be adapted for use. The python code in this repository uses sqlalchemy
    to interact with the SQL database. Thus switching to another SQL implementation should only require changing the [`sqlalchemy.create_engine()`](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) call
- The unstructured data is stored in a levelDB database
    - The default directory name we use is `"leveldb"`, but through the `--leveldb` CLI a user can specify a different name for
    what directory the levelDB is in


## Install

Only Supports Linux. Tested on a Debian-based Linux distribution.

Requirements:

- [micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html)
  - micromamba can be
    installed via [their installation instructions](https://mamba.readthedocs.io/en/latest/installation.html), or
    running `bash -i scripts/micromamba-install.sh`
  - Some other conda environment manager (conda, miniconda, mamba) may be used. Our bash scripts are under the `script/`
directory are all set up around micromamba. However, they are quite simple scripts, so preforming these actions yourself is
more than feasible.
- Install the virtual environment
    - `bash -i scripts/install.sh`

## Running

Enable the virtual enviroment via `micromamba activate openwpmdata`

The two Python files a user would run are `main/run_analysis.py` and `main/view_results.py`.

### `main/run_analysis.py` 

Intended to run all the analyses on the crawl data from OpenWPM, then store that data in new table in the SQL database. View 
the CLI arguments for this by running `python main/run_analysis.py --help`.

### `main/view_results.py`

Intended to be ran after running `main/run_analysis.py`, to view the results from the analysis. View 
the CLI arguments for this by running `python main/view_results.py --help`.

