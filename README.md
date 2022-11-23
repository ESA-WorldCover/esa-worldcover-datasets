# :earth_africa: ESA WorldCover

WorldCover provides the first global land cover products for 2020 and 2021 at 10 m resolution, developed and validated in near-real time based on Sentinel-1 and Sentinel-2 data.

More information can be found on the official project website https://esa-worldcover.org/ as well as
on ESA project pages https://worldcover2020.esa.int/ & https://worldcover2021.esa.int/

**Table of Contents**
- [:earth\_africa: ESA WorldCover](#earth_africa-esa-worldcover)
  - [:memo: Cite](#memo-cite)
  - [:satellite: Data Access](#satellite-data-access)
    - [:eyes: Viewers](#eyes-viewers)
    - [:floppy\_disk: Download](#floppy_disk-download)
      - [:snake: Download from AWS with a python script (country/bounding box)](#snake-download-from-aws-with-a-python-script-countrybounding-box)
      - [Download from AWS with the AWS CLI](#download-from-aws-with-the-aws-cli)
  - [:notebook:Notebooks](#notebooknotebooks)


## :memo: Cite

For **WorldCover 2020 v100**

Zanaga, D., Van De Kerchove, R., De Keersmaecker, W., Souverijns, N., Brockmann, C., Quast, R., Wevers, J., Grosu, A., Paccini, A., Vergnaud, S., Cartus, O., Santoro, M., Fritz, S., Georgieva, I., Lesiv, M., Carter, S., Herold, M., Li, Linlin, Tsendbazar, N.E., Ramoino, F., Arino, O., 2021. ESA WorldCover 10 m 2020 v100. https://doi.org/10.5281/zenodo.5571936 
 
For **WorldCover 2021 v200** :fire:

Zanaga, D., Van De Kerchove, R., Daems, D., De Keersmaecker, W., Brockmann, C., Kirches, G., Wevers, J., Cartus, O., Santoro, M., Fritz, S., Lesiv, M., Herold, M., Tsendbazar, N.E., Xu, P., Ramoino, F., Arino, O., 2022. ESA WorldCover 10 m 2021 v200. https://doi.org/10.5281/zenodo.7254221


If you are using the data as a layer in a published map, please include the following attribution text:

© ESA WorldCover project [year] / Contains modified Copernicus Sentinel data ([year]) processed by ESA WorldCover consortium
With year either 2020 or 2021 for the WorldCover 2020 and 2021 map, respectively.


## :satellite: Data Access

The 2020 and 2021 can be accessed (viewed or downloaded) through different channels:

### :eyes: Viewers
- [VITO Terrascope viewer](https://viewer.esa-worldcover.org/worldcover/)
- [VITO Google Earth Engine App](https://vitorsveg.users.earthengine.app/view/worldcover)
- [ESA viewer for 2020 map](https://worldcover2020.esa.int/viewer)
- [ESA viewer for 2021 map](https://worldcover2021.esa.int/viewer)

### :floppy_disk: Download

The products consist of 2631 tif files for a total of ~124gb.
You can either download single tifs or aggregated zip files covering 20 deg by 20 deg tiles.

The aggregated zip files can be downloaded from:
- [Zenodo](https://zenodo.org/record/7254221#.Y34VWNLMKV4)
- [ESA downloader](https://worldcover2021.esa.int/download)

If you want a more granular access you can download single files from the
[Terrascop viewer/downloader](https://viewer.esa-worldcover.org/worldcover/)

The data is also available on the [AWS Open Data Registry](https://registry.opendata.aws/esa-worldcover-vito/) which hosts the COGs on a public S3 bucket `s3://esa-worldcover/`
Direct download from AWS avoids unzipping steps.

#### :snake: Download from AWS with a python script (country/bounding box)
If you wish to restrict your download area to a certain bounding box or country,
you can use the download script under `scripts/download.py`

Make sure to install the required packages:
```
pip install geopandas requests tqdm
```

and run it with:
```
python scripts/download.py
```
This will download all the files. If you wish to filter on a country:
```
python scripts/download.py -c Italy
```
or a bounding box:
```
python scripts/download.py -b 0 0 20 20
```
You can also use both filters, the script will intersect the bounding box and the country geometry.
Please note that if you want to download data for a country with spaces in the name, wrap it in quotes:
```
python scripts/download.py -c "United States of America" --dry
```
A list of available country names is printed if the specified country doesn't match any of them.

Additional parameters:
- `-o/--output` specify an output folder. By default it will download in the current working directory.
- `-y/--year` to download either 2020 or 2021 data (defaults to 2021),
- `--dry` run a dryrun
- `--overwrite` overwrite existing files. By default existing files will be skipped to avoid repeating a download after an interruption.


#### Download from AWS with the AWS CLI

To download all the products using the AWS CLI tool:

To install the AWS command line interface, see https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html or open a python environment and run
```
pip install awscli
```
Once the AWS CLI is installed you can copy the whole bucket:

``` 
aws s3 sync s3://esa-worldcover/v200/2021/map /local/path --no-sign-request 
```
for WorldCover 2021 v200 

or  
```
aws s3 sync s3://esa-worldcover/v100/2020/map /local/path --no-sign-request 
```
for WorldCover 2020 v100 

(please modify **/local/path** to the desired download location)


## :notebook:Notebooks
We provide a series of Jupyter notebooks to illustrate how to access the data on AWS
in your scripts

