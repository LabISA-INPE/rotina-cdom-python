from pathlib import Path
import pandas as pd
from scipy.interpolate import interp1d
import os

def interpolate_cdom_data(input_file, output_file=None, min_wavelength=220, max_wavelength=800):
    try:
        print(f"Loading data from: {input_file}")

        # Check if input file exists
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        # Load the CSV data
        tr15 = pd.read_csv(input_file, sep=";", decimal=",", na_values="")

        # Rename the first column to "Wave"
        tr15.columns.values[0] = "Wave"

        # Create new DataFrame with desired wavelength range
        tr15_completa = pd.DataFrame({"Wave": range(min_wavelength, max_wavelength + 1)})

        # Iterate through data columns and interpolate
        successful_columns = 0
        for col_name in tr15_completa:
            try:
                # Remove NaN values
                valid_indices = ~tr15[col_name].isna()
                if valid_indices.sum() < 2:
                    continue

                interpolator = interp1d(
                    tr15.loc[valid_indices, "Wave"],
                    tr15.loc[valid_indices, col_name],
                    kind="linear",
                    fill_value="extrapolate" 
                )

                # Apply interpolation
                tr15_completa[col_name] = interpolator(tr15_completa["Wave"])
                successful_columns += 1
            
            except Exception as e:
                print(f"Error interpolating {col_name}: {e}")
            
        print(f"Successfully interpolated {successful_columns} columns")
    
        if output_file is None:
            input_path = Path(input_file)
            output_file = input_path.parent / f"{input_path.stem}_interpolated{input_path.suffix}"
        
        # Create output directory if if doesn't exist
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save the results to CSV
        tr15_completa.to_csv(output_file, sep=";", index=False)

        return tr15_completa, str(output_file)

    except Exception as e:
        print(f"Error during interpolation {e}")