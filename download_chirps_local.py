import ee
import pandas as pd

# Initialize the Earth Engine module with error handling
try:
    ee.Initialize()
    print("Earth Engine initialized successfully.")
except ee.EEException as e:
    print(f"Error initializing Earth Engine: {e}")
    print("Please ensure you are signed up for GEE and have authenticated using 'earthengine authenticate'.")
    exit(1)

# Define the point of interest (Longitude, Latitude)
point = ee.Geometry.Point([38.75, 9.0192])

# Define the date range
start_date = '2023-01-01'
end_date = '2023-01-05'

# Load the CHIRPS daily precipitation dataset
chirps = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY') \
    .filterDate(start_date, end_date) \
    .select('precipitation')

# Function to extract precipitation data at the point
def extract_precipitation(image):
    value = image.reduceRegion(
        reducer=ee.Reducer.first(),
        geometry=point,
        scale=5566  # CHIRPS resolution (~0.05 degrees)
    ).get('precipitation')
    
    return ee.Feature(None, {
        'system:time_start': image.get('system:time_start'),
        'precipitation': value
    })

# Apply the extraction function to the image collection
precipitation_data = chirps.map(extract_precipitation)

# Convert dates to readable format and prepare the data
precipitation_list = precipitation_data.map(
    lambda feature: ee.Feature(None, {
        'date': ee.Date(feature.get('system:time_start')).format('YYYY-MM-dd'),
        'precipitation_mm': feature.get('precipitation')
    })
)

# Get the data as a list of dictionaries from GEE
try:
    data = precipitation_list.getInfo()['features']
except ee.EEException as e:
    print(f"Error retrieving data from GEE: {e}")
    exit(1)

# Extract relevant properties into a list of dictionaries
processed_data = [
    {
        'date': feature['properties']['date'],
        'precipitation_mm': feature['properties']['precipitation_mm']
    }
    for feature in data
]

# Convert to a Pandas DataFrame
df = pd.DataFrame(processed_data)

# Display the DataFrame
print("Precipitation Data:")
print(df)

# Save the DataFrame to a local CSV file
output_file = 'CHIRPS_Precipitation_2023_Jan_1_to_5_Lat_9.0192_Lon_38.75.csv'
df.to_csv(output_file, index=False)

print(f"Data saved to {output_file}")