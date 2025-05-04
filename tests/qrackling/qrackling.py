import os
import subprocess

def main():
    # simulation_file = 'qeyssat_test.json'
    simulation_file = 'qeyssat_2035_direct_overpass.json'
    run_qrackling(simulation_file=simulation_file)

def run_qrackling(simulation_file: str) -> None:
    qrackling_dir = 'tests/qrackling'
    current_dir = os.getcwd()
    os.chdir(qrackling_dir)
    subprocess.run([
        'matlab',
        '-batch',
        f"simulation_file='{simulation_file}'; qrackling"
    ])
    os.chdir(current_dir)

if __name__ == '__main__':
    main()