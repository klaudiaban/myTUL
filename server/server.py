import threading
import time
import database_admin as da
import calculate
from datetime import datetime

# array for cameras/streams
tasks = ["Task A", "Task B"]
task_threads = []
tasks_lock = threading.Lock()
running = True

# Worker thread function, this will run for every camera/stream and insert data from the camera/stream to the
# database on database/AdminData/Alltime every x minutes, and update database/UserData/Current
def worker(task_name):
    while running:
        #here goes the camera handling code
        current_data = 0 #here will be the code for getting data
        timestamp_data = 0 #this is the data like amount itp.
        date = 0 #this is the date that will be used as a header for the data insert(name of the dict in json)
        room = 0 #this is the name of the room, that will help to add data to the right table
        da.set_realtime_data(room, date, current_data)
        print("[Worker: "+ task_name +"] realtime data updated")
        da.insert_data(timestamp_data)
        print("[Worker: " + task_name + "] inserted data")

# Server thread function, this will run and calculate the statistics and insert them to the database/UserData/Stats
def server():
    while running:
        stats = calculate.calculate_stats() #calculates the stats, from the all time data
        da.update_stats(stats) #updates the stats in the database
        print("[Server] Stats updated! Current date:" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        time.sleep(86400) # does the above only every 24h

def task_manager_thread_func():
    global running
    print("[Task Manager] Ready. Type a new task name or 'exit' to quit.")
    while running:
        new_task = input("Enter new task: ").strip()
        if new_task.lower() == "exit":
            print("[Task Manager] Shutting down server.")
            running = False
        with tasks_lock:
            tasks.append(new_task)
            t = threading.Thread(target=worker, args=(new_task,))
            t.start()
            task_threads.append(t)

# Main function to start threads
def main():
    # Start the server thread
    server_thread = threading.Thread(target=server)
    server_thread.start()

    # Start worker threads
    worker_threads = []
    for task in tasks:
        t = threading.Thread(target=worker, args=(task,))
        t.start()
        worker_threads.append(t)

    task_manager_thread = threading.Thread(target=task_manager_thread_func)
    task_manager_thread.start()

    task_manager_thread.join()


    # Wait for all threads to finish
    for t in worker_threads:
        t.join()

    server_thread.join()
    print("All threads completed.")

if __name__ == "__main__":
    main()