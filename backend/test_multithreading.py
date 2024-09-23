import threading
import time

def function_one():
    for i in range(20):
        print(f"Function One - Count: {i}")
        time.sleep(1)

def function_two():
    for i in range(20, 40, 1):
        print(f"Function Two - Count: {i}")
        time.sleep(1)

# Create threads
thread1 = threading.Thread(target=function_one)
thread2 = threading.Thread(target=function_two)

# Start threads
thread1.start()
thread2.start()

# Wait for both threads to complete
thread1.join()
thread2.join()

print("Both functions have finished executing.")
