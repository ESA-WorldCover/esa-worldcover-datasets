
def query_products(bbox, max_items=None, year=2021):
    
    from pystac_client import Client

    stac_endopoint = 'https://services.terrascope.be/stac/'

    # collection ids for both maps in the Terrascope STAC Catalogue
    collection_ids = {2020: 'urn:eop:VITO:ESA_WorldCover_10m_2020_AWS_V1',
                      2021: 'urn:eop:VITO:ESA_WorldCover_10m_2021_AWS_V2'}

    client = Client.open(stac_endopoint)

    search_results = client.search(
        collections=[collection_ids[year]],
        bbox=bbox
    )

    # Search results fetched and represented as dictionary
    results = search_results.get_all_items()
    
    return results