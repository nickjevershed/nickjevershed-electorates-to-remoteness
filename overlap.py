from shapely.geometry import shape, mapping
import fiona
import simplejson as json
import pandas as pd

electorates = fiona.open('shapefiles/CED_2021_AUST_GDA2020.shp')
regions = fiona.open('shapefiles/RA_2016_AUST.shp')

all_results = []
 
for electorate in electorates:
	print(electorate['properties']['CED_NAME21'])
	results = []
	for region in regions:
		if electorate['geometry'] and region['geometry']:
			electorate_shape = shape(electorate['geometry'])
			region_shape = shape(region['geometry'])
			if electorate_shape.intersects(region_shape):
				overlap = (electorate_shape.intersection(region_shape).area/electorate_shape.area)*100
				print(region['properties']['RA_NAME16'])
				print(electorate['properties']['CED_NAME21'])
				results.append({"electorate":electorate['properties']['CED_NAME21'], "overlap":overlap, "remoteness":region['properties']['RA_NAME16']})
	if electorate['geometry']:
		results_df = pd.DataFrame(results)
		results_gp = results_df.groupby(['remoteness']).sum()
		results_gp_t = results_gp.T
		results_gp_t['electorate'] = electorate['properties']['CED_NAME21']
		all_results.append(results_gp_t.to_dict('records')[0])

final = pd.DataFrame(all_results)
final[['electorate','Major Cities of Australia','Inner Regional Australia','Outer Regional Australia','Remote Australia','Very Remote Australia',]].to_csv('electorate-remoteness.csv', index=False)
