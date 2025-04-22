from datetime import datetime, timezone
from datetime import timedelta
import pandas as pd


def schedule_job(
    start_time: datetime,
    duration: timedelta,
    flex_window: timedelta,
    carbon_intensity_dataset: pd.DataFrame
) -> float:
    """Finds the optimal time to schedule a job based on carbon intensity.
    
    Returns the carbon intensity (gCO2/kWh) and scheduled start time for the following cases:
    - Optimal case (the start time w/ the minimum carbon intensity
    - Median case (the start time w/ the median carbon intensity)
    - Naive case (the start time w/ no flex window)
    - Worst case (the start time w/ the maximum carbon intensity)
    
    Args:
        start_time (datetime): The start time of the job
        duration (timedelta): The duration of the job
        flex_window (timedelta): The flex window for the job
        carbon_intensity_dataset (pd.DataFrame): DataFrame containing carbon intensity data
            This DataFrame should have a datetime index or a timestamp column
            and contain carbon intensity values for different regions
    
    Returns:
        float: The carbon intensity (gCO2/kWh) and scheduled start time for the following cases:
            - Optimal case (the start time w/ the minimum carbon intensity
            - Median case (the start time w/ the median carbon intensity)
            - Naive case (the start time w/ no flex window)
            - Worst case (the start time w/ the maximum carbon intensity)
    """
    # rollup the carbon intensity dataset by the duration of the job
    # this will give us a list of carbon intensity values for each time window
    carbon_intensity_dataset = carbon_intensity_dataset.resample(duration).mean()

    # find the optimal, median, naive, and  worst carbon intensity
    optimal_case_idx = carbon_intensity_dataset.idxmin()
    naive_case_idx = carbon_intensity_dataset.index[0]
    worst_case_idx = carbon_intensity_dataset.idxmax()

    # get value at optimal_case_idx
    breakpoint()
    optimal_carbon_intensity = list(carbon_intensity_dataset.loc[optimal_case_idx].to_dict()['value'].items())[0]
    naive_carbon_intensity = list(carbon_intensity_dataset.loc[naive_case_idx].to_dict()['value'].items())[0]
    worst_carbon_intensity = list(carbon_intensity_dataset.loc[worst_case_idx].to_dict()['value'].items())[0]

    return {
        "optimal": (optimal_carbon_intensity),
        "naive": (naive_carbon_intensity),
        "worst": (worst_carbon_intensity),
    }


if __name__ == "__main__":
    from historical_data import fetch_carbon_intensity

    # Example usage
    df = fetch_carbon_intensity(
        start_time="2025-04-15T00:00:00Z",
        end_time="2025-04-21T00:00:00Z",
        region="CAISO_NORTH"
    )
    print(schedule_job(
        start_time=datetime(2025, 4, 15, 0, 0, 0, tzinfo=timezone.utc),
        duration=timedelta(hours=1),
        flex_window=timedelta(hours=1),
        carbon_intensity_dataset=df
    ))
    