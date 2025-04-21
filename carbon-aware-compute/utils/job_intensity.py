"""Module to find carbon intensity for a particular job"""


import pandas as pd
from datetime import datetime, timezone


def compute_job_carbon_intensity(
    start_time: datetime,
    end_time: datetime,
    carbon_intensity_dataset: pd.DataFrame
) -> float:
    """
    Compute the mean carbon intensity for a job within a specified time window.
    
    Args:
        start_time (datetime): The start time of the job
        end_time (datetime): The end time of the job
        region (str): The power region where the job is running
        carbon_intensity_dataset (pd.DataFrame): DataFrame containing carbon intensity data
            This DataFrame should have a datetime index or a timestamp column
            and contain carbon intensity values for different regions
    
    Returns:
        float: The mean carbon intensity (gCO2/kWh) for the job during the specified time window
    
    Raises:
        ValueError: If no data points are found within the specified time window
        KeyError: If the power_region is not found in the dataset
    """
    # Filter the region data for the specified time window
    filtered_data = carbon_intensity_dataset[(carbon_intensity_dataset['point_time'] >= start_time) & (carbon_intensity_dataset['point_time'] <= end_time)]
    
    # Check if we have any data points
    if filtered_data.empty:
        raise ValueError("No data points found within the specified time window")

    # Compute the mean carbon intensity
    mean_carbon_intensity = filtered_data['value'].mean()
    return mean_carbon_intensity


if __name__ == "__main__":
    from historical_data import fetch_carbon_intensity

    # Example usage
    df = fetch_carbon_intensity(
        start_time="2025-04-15T00:00:00Z",
        end_time="2025-04-21T00:00:00Z",
        region="CAISO_NORTH"
    )
    print(compute_job_carbon_intensity(
        start_time=datetime(2025, 4, 15, 0, 0, 0, tzinfo=timezone.utc),
        end_time=datetime(2025, 4, 15, 0, 30, 0, tzinfo=timezone.utc),
        carbon_intensity_dataset=df
    ))

