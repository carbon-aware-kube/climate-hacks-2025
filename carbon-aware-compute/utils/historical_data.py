from typing import Union
from datetime import datetime
import pandas as pd
from watttime import WattTimeHistorical


def fetch_carbon_intensity(
    start_time: Union[str, datetime],
    end_time: Union[str, datetime],
    region: str,
) -> pd.DataFrame:
    """
    Fetches carbon intensity data (co2_moer) for a specific region between start and end times.
    
    Args:
        start_time (Union[str, datetime]): The start time of the period to fetch data for
        end_time (Union[str, datetime]): The end time of the period to fetch data for
        region (str): The power region to fetch data for (e.g., 'CAISO_NORTH')
    
    Returns:
        pd.DataFrame: A pandas DataFrame containing carbon intensity data with columns:
            - point_time: The timestamp of the data point
            - value: The carbon intensity value (gCO2/kWh)
            - version: The version of the data
    
    Raises:
        ValueError: If the region is not valid or if no data is found for the specified time period
    """
    # Initialize the WattTime Historical client
    wt_historical = WattTimeHistorical()
    
    try:
        # Fetch the carbon intensity data for the specified region and time period
        df = wt_historical.get_historical_pandas(
            start=start_time,
            end=end_time,
            region=region,
            signal_type="co2_moer"
        )
        
        # Check if we got any data
        if df.empty:
            raise ValueError(f"No carbon intensity data found for region {region} between {start_time} and {end_time}")
        
        # Ensure the dataframe has the expected columns
        if 'point_time' not in df.columns or 'value' not in df.columns:
            raise ValueError("Unexpected data format from WattTime API")
        
        # Sort by time for consistency
        df = df.sort_values('point_time')
        
        return df
    
    except Exception as e:
        # Handle specific API errors
        if "region" in str(e).lower():
            raise ValueError(f"Invalid region: {region}. Please check the region code.")
        elif "credentials" in str(e).lower():
            raise ValueError("Authentication failed. Please check your WattTime API credentials.")
        else:
            # Re-raise the original exception
            raise


if __name__ == "__main__":
    # Example usage
    df = fetch_carbon_intensity(
        start_time="2023-01-01T00:00:00Z",
        end_time="2023-01-02T00:00:00Z",
        region="CAISO_NORTH"
    )
    print(df.head())
