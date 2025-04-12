import requests

# Function to construct the full URL with parameterized components, including separate month and year
def construct_url(source, dataset, version, frequency, resolution, variable, scope="global", 
                  lon_min=None, lon_max=None, lat_min=None, lat_max=None, 
                  start_month=None, start_year=None, end_month=None, end_year=None):
    """
    Constructs the IRIDL URL with fully parameterized components, including separate month and year for dates.
    
    Parameters:
    - source (str): Data source (e.g., '.UCSB').
    - dataset (str): Dataset name (e.g., '.CHIRPS').
    - version (str): Dataset version (e.g., '.v2p0').
    - frequency (str): Data frequency (e.g., '.daily' or '.daily-improved').
    - resolution (str): Spatial resolution (e.g., '.0p05').
    - variable (str): Variable name (e.g., '.prcp').
    - scope (str, optional): Scope of data (e.g., '.global'), defaults to 'global'.
    - lon_min (float): Minimum longitude (X).
    - lon_max (float): Maximum longitude (X).
    - lat_min (float): Minimum latitude (Y).
    - lat_max (float): Maximum latitude (Y).
    - start_month (str): Start month (e.g., 'Jan', 'Feb', etc.).
    - start_year (int): Start year (e.g., 1991).
    - end_month (str): End month (e.g., 'Dec').
    - end_year (int): End year (e.g., 2000).
    - start_date (str): Start date in 'YYYY-MM-DD' format.
    - end_date (str): End date in 'YYYY-MM-DD' format.
    
    Returns:
    - str: The full URL for downloading the NetCDF file.
    """
    # Base URL structure
    base_url = f"https://iridl.ldeo.columbia.edu/SOURCES/{source}/{dataset}/{version}/{frequency}/{scope}/{resolution}/{variable}"

    # Add the second part (e.g., daily-improved) if specified
    if frequency == ".daily-improved":
        base_url += f"/SOURCES/{source}/{dataset}/{version}/{frequency}/{scope}/{resolution}/{variable}"

    # Add spatial and temporal ranges if provided
    url_parts = [base_url]
    if lon_min is not None and lon_max is not None:
        url_parts.append(f"X/{lon_min}/{lon_max}/RANGE")
    if lat_min is not None and lat_max is not None:
        url_parts.append(f"Y/{lat_min}/{lat_max}/RANGE")
    if start_month is not None and start_year is not None and end_month is not None and end_year is not None:
        # Construct the time range with %20 as the space separator
        start = f"{start_month}%20{start_year}"
        end = f"{end_month}%20{end_year}"
        url_parts.append(f"T/{start}/{end}/RANGE")

    # Combine all parts and append the file format
    full_url = "/".join(url_parts) + "/data.nc"
    return full_url

# Function to download the NetCDF file
def download_file(url, output_filename):
    """
    Downloads the file from the given URL and saves it locally.
    
    Parameters:
    - url (str): The full URL to download from.
    - output_filename (str): The name of the file to save locally.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad status codes
        with open(output_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Filter out keep-alive chunks
                    f.write(chunk)
        print(f"File downloaded successfully as {output_filename}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")

# Example usage with user-defined parameters
if __name__ == "__main__":
    # Example 1: Specific date range (e.g., Jan 2023 to Jan 2023)
    params = {
        "source": ".UCSB",
        "dataset": ".CHIRPS",
        "version": ".v2p0",
        "frequency": ".daily",
        "resolution": ".0p05",
        "variable": ".prcp",
        "scope": ".global",
        "lon_min": 38.75,  # Single point example
        "lon_max": 38.75,
        "lat_min": 9.0192,
        "lat_max": 9.0192,
        "start_month": "Jan",
        "start_year": 2023,
        "end_month": "Jan",
        "end_year": 2023
    }

    url1 = construct_url(**params)
    print(f"Constructed URL for Jan 2023 to Jan 2023: {url1}")
    download_file(url1, "chirps_2023_jan.nc")

    # Example 2: Different date range (e.g., Jun 1991 to Dec 1991)
 
 

    # Interactive version (uncomment to use)
    """
    source = input("Enter source (e.g., .UCSB): ")
    dataset = input("Enter dataset (e.g., .CHIRPS): ")
    version = input("Enter version (e.g., .v2p0): ")
    frequency = input("Enter frequency (e.g., .daily or .daily-improved): ")
    resolution = input("Enter resolution (e.g., .0p05): ")
    variable = input("Enter variable (e.g., .prcp): ")
    scope = input("Enter scope (e.g., .global, press Enter for default): ") or ".global"
    lon_min = float(input("Enter minimum longitude: "))
    lon_max = float(input("Enter maximum longitude: "))
    lat_min = float(input("Enter minimum latitude: "))
    lat_max = float(input("Enter maximum latitude: "))
    start_month = input("Enter start month (e.g., Jan): ")
    start_year = int(input("Enter start year (e.g., 2023): "))
    end_month = input("Enter end month (e.g., Dec): ")
    end_year = int(input("Enter end year (e.g., 2023): "))

    full_url = construct_url(source, dataset, version, frequency, resolution, variable, scope,
                             lon_min, lon_max, lat_min, lat_max, start_month, start_year, end_month, end_year)
    print(f"Constructed URL: {full_url}")
    download_file(full_url, "chirps_custom.nc")
    """