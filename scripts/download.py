import argparse
import sys
from pathlib import Path

import geopandas as gpd
import requests
from tqdm.auto import tqdm


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="ESA WorldCover download helper")
    parser.add_argument('-o', '--output', default='.',
                        help="Output folder path, defaults to current folder.")
    parser.add_argument('-c', '--country', help="Optionally specify a country")
    parser.add_argument('-b', '--bounds', nargs=4, type=float,
                        help="Optionally specify a set of lat lon bounds "
                        "(4 values: xmin ymin xmax ymax)")
    parser.add_argument('-y', '--year', default=2021, type=int,
                        choices=[2020, 2021],
                        help="Map year, defaults to the most recent 2021 map")
    parser.add_argument('--overwrite', action='store_true',
                        help="Overwrite existing files")
    parser.add_argument('--dry', action='store_true', help="Perform a dry run")
    args = parser.parse_args()

    output_folder = Path('.') if args.output is None else Path(args.output)
    year = args.year  # select which map version. Most recent is 2021
    country = args.country
    bounds = args.bounds
    dryrun = args.dry

    # algo version (depends on the year)
    version = {2020: 'v100',
               2021: 'v200'}[year]

    s3_url_prefix = "https://esa-worldcover.s3.eu-central-1.amazonaws.com"

    geom = None
    if country is not None:
        # load natural earth low res shapefile
        ne = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

        if country not in ne.name.values:
            print(f"Selected country '{country}' is not available."
                  " The 'country' parameter should match one of:\n"
                  f"{ne.name.values.tolist()}")
            sys.exit()

        geom = ne[ne.name == country].iloc[0].geometry

    if bounds is not None:
        from shapely.geometry import Polygon
        geom_bounds = Polygon.from_bounds(*bounds)

        if geom is None:
            geom = geom_bounds
        else:
            print("Both 'country' and 'bounds' parameter were provided, "
                  "restricting download area to the intersection of the two.")
            geom = geom.intersection(geom_bounds)

    # load worldcover grid
    url = f'{s3_url_prefix}/v100/2020/esa_worldcover_2020_grid.geojson'
    grid = gpd.read_file(url)

    if geom is not None:
        # get grid tiles intersecting AOI
        tiles = grid[grid.intersects(geom)]
    else:
        tiles = grid

    if tiles.shape[0] == 0:
        print(f"No tiles in the selected area {geom.bounds}")
        sys.exit()

    for tile in tqdm(tiles.ll_tile):
        url = f"{s3_url_prefix}/{version}/{year}/map/ESA_WorldCover_10m_{year}_{version}_{tile}_Map.tif"
        out_fn = output_folder / \
            f"ESA_WorldCover_10m_{year}_{version}_{tile}_Map.tif"

        if out_fn.is_file() and not args.overwrite:
            print(f"{out_fn} already exists.")
            continue

        if not dryrun:
            r = requests.get(url, allow_redirects=True)
            with open(out_fn, 'wb') as f:
                f.write(r.content)
        else:
            print(f"Downloading {url} to {out_fn}")
