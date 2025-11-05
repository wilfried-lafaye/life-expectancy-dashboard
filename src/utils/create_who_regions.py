import json
import urllib.request
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
from config import WORLD_GEOJSON_URL 


# WHO regions mapping with ISO3 country codes
WHO_REGIONS = {
    'AFR': {
        'name': 'African Region',
        'countries': ['DZA', 'AGO', 'BEN', 'BWA', 'BFA', 'BDI', 'CMR', 'CPV', 'CAF', 'TCD', 
                     'COM', 'CIV', 'COD', 'GNQ', 'ERI', 'ETH', 'GAB', 'GMB', 'GHA', 'GIN', 
                     'GNB', 'KEN', 'LSO', 'LBR', 'MDG', 'MWI', 'MLI', 'MRT', 'MUS', 'MOZ', 
                     'NAM', 'NER', 'NGA', 'COG', 'RWA', 'STP', 'SEN', 'SYC', 'SLE', 'ZAF', 
                     'SSD', 'SWZ', 'TGO', 'UGA', 'TZA', 'ZMB', 'ZWE', 'SOM', 'DJI']
    },
    'AMR': {
        'name': 'Region of the Americas',
        'countries': ['ATG', 'ARG', 'BHS', 'BRB', 'BLZ', 'BOL', 'BRA', 'CAN', 'CHL', 'COL', 
                     'CRI', 'CUB', 'DMA', 'DOM', 'ECU', 'SLV', 'GRD', 'GTM', 'GUY', 'HTI', 
                     'HND', 'JAM', 'MEX', 'NIC', 'PAN', 'LCA', 'VCT', 'SUR', 'TTO', 'USA', 
                     'URY', 'VEN', 'PRY', 'PER','GUF']
    },
    'SEAR': {
        'name': 'South-East Asia Region',
        'countries': ['BGD', 'BTN', 'IND', 'MDV', 'MMR', 'NPL', 'LKA', 'THA', 'TLS']
    },
    'EUR': {
        'name': 'European Region',
        'countries': ['ALB', 'AND', 'ARM', 'AUT', 'AZE', 'BLR', 'BEL', 'BIH', 'BGR', 'HRV', 
                     'CYP', 'CZE', 'DNK', 'EST', 'FIN', 'FRA', 'GEO', 'DEU', 'GRC', 'HUN', 
                     'ISL', 'IRL', 'ITA', 'KAZ', 'KGZ', 'LVA', 'LTU', 'LUX', 'MLT', 
                     'MDA', 'MCO', 'MNE', 'NLD', 'MKD', 'NOR', 'POL', 'PRT', 'ROU', 'RUS', 
                     'SMR', 'SRB', 'SVK', 'SVN', 'ESP', 'SWE', 'CHE', 'TJK', 'TUR', 'TKM', 
                     'UKR', 'GBR', 'UZB', 'XXK','UKR','CS-KM']
    },
    'EMR': {
        'name': 'Eastern Mediterranean Region',
        'countries': ['AFG', 'BHR', 'EGY', 'IRN', 'IRQ', 'JOR', 'KWT', 'LBN', 'LBY',
                     'OMN', 'PAK', 'PSE', 'QAT', 'SAU', 'SDN', 'SYR', 'TUN', 'ARE', 'YEM', 'ISR']
    },
    'WPR': {
        'name': 'Western Pacific Region',
        'countries': ['AUS', 'BRN', 'KHM', 'CHN', 'COK', 'FJI', 'IDN', 'JPN', 'KIR', 'LAO', 
                     'MYS', 'MHL', 'FSM', 'MNG', 'NRU', 'NZL', 'NIU', 'PLW', 'PNG', 'PHL', 
                     'WSM', 'SGP', 'SLB', 'KOR','PRK', 'TWN', 'TON', 'TUV', 'VUT', 'VNM']
    }
}



def create_who_regions_geojson():
    """
    Creates a GeoJSON file containing WHO regions by merging country geometries.
    
    Args:
        world_geojson_url (str): URL of the world countries GeoJSON
        output_file (str): Output file path for the regions GeoJSON
    
    Returns:
        dict: GeoJSON FeatureCollection of WHO regions
    """
    with urllib.request.urlopen(WORLD_GEOJSON_URL, timeout=15) as resp:
        world_geojson = json.load(resp)
    
    # Create a mapping of country code to geometry
    country_geometries = {}
    for feature in world_geojson['features']:
        country_code = feature.get('id')
        if country_code:
            country_geometries[country_code] = shape(feature['geometry'])
    
    # Create regional features
    regional_features = []
    
    for region_code, region_info in WHO_REGIONS.items():
        # Collect geometries for this region
        region_geoms = []
        
        for country_code in region_info['countries']:
            if country_code in country_geometries:
                region_geoms.append(country_geometries[country_code])
        
        if region_geoms:
            # Merge all geometries into one
            merged_geometry = unary_union(region_geoms)
            
            # Create feature for this region
            feature = {
                "type": "Feature",
                "id": region_code,
                "properties": {
                    "name": region_info['name'],
                    "region_code": region_code,
                    "country_count": len(region_geoms)
                },
                "geometry": mapping(merged_geometry)
            }
            
            regional_features.append(feature)
    
    # Create the final GeoJSON
    regions_geojson = {
        "type": "FeatureCollection",
        "features": regional_features
    }
    
    # Save to file
    with open('data/who_regions.geojson', 'w', encoding='utf-8') as f:
        json.dump(regions_geojson, f, indent=2, ensure_ascii=False)


