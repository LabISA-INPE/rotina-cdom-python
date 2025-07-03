import os
import sys
from pathlib import Path
from functions.dados import dados

def load_config_from_input_txt(file_path="input.txt"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file not found: {file_path}")

    config = {}

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line and "=" in line:
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()

        
    return config

def check_dependencies():
    required_modules = ["numpy", "pandas", "matplotlib", "scipy"]
    missing_modules = []

    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        for module in missing_modules:
            print(f"-{module}")
        print("Please instal missing modules")
        return False

    print("All required dependencies are available")
    return True

def run_cdom_analysis():
    try:
        print("CDOM ANALYSIS - STARTING")

        # Check dependencies
        if not check_dependencies():
            return {"status": "error", "messagge": "Missing dependencies"}
    
        # Load configuration from input.txt
        config = load_config_from_input_txt()

        # Print configuration symmary
        print("\nConfiguration loaded:")
        print(f"  • Sample groups: {config.get('num_grps_amos')}")
        print(f"  • Water samples: {config.get('amostra_agua')}")
        print(f"  • Input file: {config.get('path_arquivo')}")
        print(f"  • Plot title: {config.get('titulo_grafico')}")
        print(f"  • Output CDOM: {config.get('path_cdom')}")
        print(f"  • Output final data: {config.get('path_dados_finais')}")
        print(f"  • Output plot: {config.get('path_grafico')}")

        # Check if input file exists
        input_file = config.get("path_arquivo")
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input data file not found: {input_file}")

        print(f"Input file found: {input_file}")

        # Create output directory if the don't exist
        output_paths = ["path_cdom", "path_daddos_finais", "path_grafico"]
        for path_key in output_paths:
            if path_key in config:
                output_dir = os.path.dirname(config[path_key])
                if output_dir and not os.path.exists(output_dir):
                    os.makedirs(output_dir, exist_ok=True)
                    print(f"Created output directory: {output_dir}")

        
        print("\n Starting CDOM analysis...")

        dados(
            num_grps_amos=config['num_grps_amos'],
            amostra_agua=config['amostra_agua'],
            path_cdom=config['path_cdom'],
            path_dados_finais=config['path_dados_finais'],
            titulo_grafico=config['titulo_grafico'],
            path_grafico=config['path_grafico'],
            path_arquivo=config['path_arquivo']    
        )

        # Check if output files were created
        print("ANALYSIS COMPLETED!")

        output_files = {
            "CDOM data": config["path_cdom"],
            "Final data": config["path_dados_finais"],
            "Plot": config["path_grafico"]
        }

        all_files_created = True
        for file_type, file_path in output_files.items():
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"  ✅ {file_type}: {file_path} ({file_size:,} bytes)")
            else:
                print(f"  ❌ {file_type}: {file_path} (NOT FOUND)")
                all_files_created = False

        if all_files_created:
            return {'status': 'success', 'message': 'Analysis completed successfully'}
        else:
            return {'status': 'warning', 'message': 'Analysis completed but some output files are missing'}

    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return{"status": "error", "message": str(e)}

    except Exception as e:
        print("Error during analysis: {e}")
        return{"status": "error", "message": str(e)}

def main():
    print("CDOM analysis application")

    # Run analysis
    try:
        results = run_cdom_analysis()

        if results["status"] == "success":
            print("\n Analysis completed successfully")
            sys.exit(0)
        elif results["status" == "warning"]:
            print(f"\n Analysis completed with warnings: {results.get("message")}")
            sys.exit(0)
        else:
            print(f"\n Analysis failed: {results.get('message', 'Unknown error')}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n Unexpected error: {e}")
        sys.exit(1)
    
if __name__ == "__main__":
    main()
            