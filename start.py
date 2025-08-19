# start.py
import subprocess
import sys
import signal

# Function to terminate child processes on exit
def terminate_processes(processes):
    for p in processes:
        try:
            p.terminate()
        except Exception as e:
            print(f"Error terminating process: {e}")

processes = []

try:
    # Start main.py
    main_process = subprocess.Popen([sys.executable, "main.py"])
    processes.append(main_process)
    print("Started main.py")

    # Wait for both processes to finish
    for p in processes:
        p.wait()

except KeyboardInterrupt:
    print("KeyboardInterrupt received. Terminating processes...")
    terminate_processes(processes)
except Exception as e:
    print(f"Error: {e}")
    terminate_processes(processes)
