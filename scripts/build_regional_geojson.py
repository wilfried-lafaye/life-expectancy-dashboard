"""
Script to create WHO regions GeoJSON file.
Generates a GeoJSON file containing WHO region boundaries.
"""

import json
import urllib.request
from shapely.geometry import shape, mapping
from shapely.ops import unary_union

WHO_REGIONS = {
    'AFR': {
        'name': 'Africa',
        'countries': ['DZA', 'AGO', 'BEN', 'BWA', 'BFA', 'BDI', 'CMR', 'CPV',
                      'CAF', 'TCD', 'COM', 'COG', 'CIV', 'COD', 'GNQ', 'ERI',
                      'ETH', 'GAB', 'GMB', 'GHA', 'GIN', 'GNB', 'KEN', 'LSO',
                      'LBR', 'MDG', 'MWI', 'MLI', 'MRT', 'MUS', 'MOZ', 'NAM',
                      'NER', 'NGA', 'RWA', 'STP', 'SEN', 'SYC', 'SLE', 'ZAF',
                      'SSD', 'SWZ', 'TGO', 'UGA', 'TZA', 'ZMB', 'ZWE', 'MAR',
                      'SOM', 'SDN','EGY','LBY', 'TUN', 'DJI']
    },
    'AMR': {
        'name': 'Americas',
        'countries': ['ATG', 'ARG', 'BHS', 'BRB', 'BLZ', 'BOL', 'BRA', 'CAN',
                      'CHL', 'COL', 'CRI', 'CUB', 'DMA', 'DOM', 'ECU', 'SLV',
                      'GRD', 'GTM', 'GUY', 'HTI', 'HND', 'JAM', 'MEX', 'NIC',
                      'PAN', 'PRY', 'PER', 'KNA', 'LCA', 'VCT', 'SUR', 'TTO',
                      'USA', 'URY', 'VEN','GUF']
    },
    'SEAR': {
        'name': 'South-East Asia',
        'countries': ['BGD', 'BTN', 'IND', 'IDN', 'MDV', 'MMR', 'NPL',
                      'LKA', 'THA', 'TLS','MYS']
    },
    'EUR': {
        'name': 'Europe',
        'countries': ['ALB', 'AND', 'ARM', 'AUT', 'AZE', 'BLR', 'BEL', 'BIH',
                      'BGR', 'HRV', 'CYP', 'CZE', 'DNK', 'EST', 'FIN', 'FRA',
                      'GEO', 'DEU', 'GRC', 'HUN', 'ISL', 'IRL', 'ITA',
                      'KAZ', 'KGZ', 'LVA', 'LTU', 'LUX', 'MLT', 'MCO', 'MNE',
                      'NLD', 'MKD', 'NOR', 'POL', 'PRT', 'MDA', 'ROU', 'RUS',
                      'SMR', 'SRB', 'SVK', 'SVN', 'ESP', 'SWE', 'CHE', 'TJK',
                      'TUR', 'TKM', 'UKR', 'GBR', 'UZB','RS-KM']
    },
    'EMR': {
        'name': 'Eastern Mediterranean',
        'countries': ['AFG', 'BHR', 'IRN', 'IRQ', 'JOR', 'KWT',
                      'LBN', 'OMN', 'PAK', 'PSE', 'QAT', 'SAU',
                      'SYR', 'ARE', 'YEM','ISR']
    },
    'WPR': {
        'name': 'Western Pacific',
        'countries': ['AUS', 'BRN', 'KHM', 'CHN', 'COK', 'FJI', 'JPN', 'KIR',
                      'LAO', 'MHL', 'FSM', 'MNG', 'NRU', 'NZL', 'NIU',
                      'PLW', 'PNG', 'PHL', 'KOR','PRK','WSM', 'SGP', 'SLB', 'TON',
                      'TUV', 'VUT', 'VNM']
    }
}

def create_who_regions_geojson():
    """
    Creates a GeoJSON file with WHO regions by merging country geometries.
    """
    # Load world countries GeoJSON
    url = (
        "https://raw.githubusercontent.com/johan/world.geo.json"
        "/master/countries.geo.json"
    )
    with urllib.request.urlopen(url, timeout=15) as response:
        world_geojson = json.load(response)

    # Create regions GeoJSON
    regions_features = []

    for region_code, region_info in WHO_REGIONS.items():
        region_countries = region_info['countries']
        region_geometries = []

        for feature in world_geojson['features']:
            if feature.get('id') in region_countries:
                geom = shape(feature['geometry'])
                region_geometries.append(geom)

        if region_geometries:
            merged_geom = unary_union(region_geometries)
            regions_features.append({
                'type': 'Feature',
                'id': region_code,
                'properties': {'name': region_info['name']},
                'geometry': mapping(merged_geom)
            })

    regions_geojson = {
        'type': 'FeatureCollection',
        'features': regions_features
    }

    # Save to file
    with open('data/who_regions.geojson', 'w', encoding='utf-8') as file:
        json.dump(regions_geojson, file, indent=2)
