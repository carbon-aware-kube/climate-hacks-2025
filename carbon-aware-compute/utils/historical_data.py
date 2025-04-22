from typing import Union
from datetime import datetime
import pandas as pd
import plotly.express as px
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
        
        # Index the dataframe by point_time
        df = df.set_index('point_time')
        
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
        

def graph_carbon_intensity(df: pd.DataFrame) -> None:
    px.line(df, x=df.index, y="value").show()


if __name__ == "__main__":
    # Fetch historical data for the last year (April 23, 2024 to April 22, 2025)
    # We need to fetch month by month since the API can only handle one month at a time
    from datetime import datetime
    import pandas as pd
    
    # Set the region
    region = "CAISO_NORTH"
    
    # Set end date to current day (April 22, 2025)
    end_date = datetime(2025, 4, 22)
    
    # Set start date to one year ago (April 23, 2024)
    start_date = datetime(2024, 4, 23)
    
    # Initialize an empty list to store all monthly dataframes
    all_data = []
    
    # Current date for iteration
    current_start = start_date
    
    print(f"Fetching carbon intensity data for {region} from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}...")
    
    # Loop through each month
    while current_start < end_date:
        # Calculate the end of the current month period (or end_date if it's the last period)
        # Add one month to current_start
        if current_start.month == 12:
            next_month = datetime(current_start.year + 1, 1, current_start.day)
        else:
            next_month = datetime(current_start.year, current_start.month + 1, current_start.day)
        
        # If next_month is beyond our end_date, use end_date instead
        current_end = min(next_month, end_date)
        
        print(f"Fetching data from {current_start.strftime('%Y-%m-%d')} to {current_end.strftime('%Y-%m-%d')}...")
        
        try:
            # Format dates for the API
            start_str = current_start.strftime("%Y-%m-%dT00:00:00Z")
            end_str = current_end.strftime("%Y-%m-%dT23:59:59Z")
            
            # Fetch data for the current month
            monthly_df = fetch_carbon_intensity(
                start_time=start_str,
                end_time=end_str,
                region=region
            )
            
            # Add to our list of dataframes
            all_data.append(monthly_df)
            print(f"Successfully fetched data for period ending {current_end.strftime('%Y-%m-%d')}")
            
        except Exception as e:
            print(f"Error fetching data for period {current_start.strftime('%Y-%m-%d')} to {current_end.strftime('%Y-%m-%d')}: {str(e)}")
        
        # Move to the next month
        current_start = next_month
    
    # Combine all monthly data into a single dataframe
    if all_data:
        combined_df = pd.concat(all_data)
        print(f"Combined data contains {len(combined_df)} records from {combined_df.index.min()} to {combined_df.index.max()}")
        
        # Save the combined data
        output_file = f"carbon_intensity_{region}_{start_date.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}.csv"
        combined_df.to_csv(output_file)
        print(f"Data saved to {output_file}")
        
        # Generate a graph of the data
        print("Generating graph...")
        graph_carbon_intensity(combined_df)
    else:
        print("No data was fetched successfully.")
