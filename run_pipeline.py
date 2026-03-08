import os
import subprocess
import sys

def main():
    print("="*50)
    print("Credit Portfolio Analytics Pipeline")
    print("="*50)
    
    # Check if inside venv
    python_cmd = sys.executable
    dbt_cmd = "dbt"
    
    # 1. Generate Synthetic Data and load into DB
    print("\n--- 1. Generating synthetic data to SQLite ---")
    try:
        subprocess.run([python_cmd, "database/init_db.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during data generation: {e}")
        sys.exit(1)
        
    # 2. Run dbt models
    print("\n--- 2. Running dbt transformations ---")
    try:
        dbt_project_dir = os.path.join(os.getcwd(), "dbt_project")
        # Locate dbt executable in the same directory as the Python executable
        scripts_dir = os.path.dirname(python_cmd)
        dbt_exe = os.path.join(scripts_dir, "dbt.exe") if os.name == "nt" else os.path.join(scripts_dir, "dbt")
        if not os.path.exists(dbt_exe):
            dbt_exe = "dbt"  # fallback to PATH
        subprocess.run([dbt_exe, "run", "--profiles-dir", "."], cwd=dbt_project_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during dbt transformations: {e}")
        sys.exit(1)
        
    # 3. Completion message
    print("\n" + "="*50)
    print("Pipeline Complete!")
    print("All transformations applied successfully.")
    print("\nTo view the dashboard, run:")
    print("    streamlit run dashboard/app.py")
    print("="*50)

if __name__ == "__main__":
    main()
