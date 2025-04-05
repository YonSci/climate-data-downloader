from datetime import datetime

# Function to format date into IRI-compatible string (Month%20Year)
def format_date_iri(date_str):
    """
    Converts a date string (YYYY-MM-DD) to IRI format (Month%20Year).
    
    Parameters:
    - date_str (str): Date in 'YYYY-MM-DD' format.
    
    Returns:
    - str: Date in 'Month%20Year' format (e.g., 'Jan%201991').
    """
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%b%%20%Y")  # %b is abbreviated month (e.g., Jan), %%20 for URL-encoded space
    except ValueError as e:
        raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD (e.g., 1991-01-01).")

# Function to construct the full URL with parameterized components
def construct_url(source, dataset, version, frequency, resolution, variable, scope="global", 
                  lon_min=None, lon_max=None, lat_min=None, lat_max=None, start_date=None, end_date=None):
    """
    Constructs the IRIDL URL with fully parameterized components.
    
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
    - start_date (str): Start date in 'YYYY-MM-DD' format (e.g., '1991-01-01').
    - end_date (str): End date in 'YYYY-MM-DD' format (e.g., '2000-12-31').
    
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
    if start_date is not None and end_date is not None:
        start = format_date_iri(start_date)
        end = format_date_iri(end_date)
        url_parts.append(f"T/{start}/{end}/RANGE")

    # Combine all parts and append the file format
    full_url = "/".join(url_parts) + "/data.nc"
    return full_url

# Example usage with user-defined parameters
if __name__ == "__main__":
    # Example 1: Full parameterization
    params = {
        "source": ".UCSB",
        "dataset": ".CHIRPS",
        "version": ".v2p0",
        "frequency": ".daily",
        "resolution": ".0p05",
        "variable": ".prcp",
        "scope": ".global",
        "lon_min": 48,
        "lon_max": 49,
        "lat_min": 18,
        "lat_max": 16,
        "start_date": "2023-01-01",
        "end_date": "2023-01-05"
    }

    url1 = construct_url(**params)
    print(f"URL with .daily frequency: {url1}")

    # Example 2: Using .daily-improved
    # params["frequency"] = ".daily-improved"
    # url2 = construct_url(**params)
    # print(f"URL with .daily-improved frequency: {url2}")

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
    start_date = input("Enter start date (YYYY-MM-DD, e.g., 2023-01-01): ")
    end_date = input("Enter end date (YYYY-MM-DD, e.g., 2023-01-05): ")

    full_url = construct_url(source, dataset, version, frequency, resolution, variable, scope,
                             lon_min, lon_max, lat_min, lat_max, start_date, end_date)
    print(f"Constructed URL: {full_url}")
    """