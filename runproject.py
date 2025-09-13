# This program runs your application and times it
# We assume that your application has a main() function
# which accepts no arguments and forms the starting point
# for your application.  
# While you can alter this file if you wish for testing purposes,
# the un-altered original form of this file will always be used
# for actual submission testing.  Thus, any changes made to this
# file will not be part of your application.  No features 
# should be implemented in this file as it will not be used during
# submission testing.

# To use this runner:
# Implement your application with a starting point of main() in project.py
# Run the following command:
#     python runproject.py


from project import main
import time
start_time = time.perf_counter()
main()
end_time = time.perf_counter()
total_time = (end_time-start_time)
print("The time below does not affect MS1 grade, only MS2 grade")
print(f"Total Time = {total_time} seconds")
if total_time <= 10.0:
    print("Timing Rubric level 4 for MS2 if MS2 Application Correctness rubric level is at >= 1")
elif total_time <= 15.0:
    print("Timing Rubric level 3 for MS2 if MS2 Application Correctness rubric level is at >= 1")
elif total_time <= 30.0:
    print("Timing Rubric level 2 for MS2 if MS2 Application Correctness rubric level is at >= 1")
elif total_time <= 60.0:
    print("Timing Rubric level 1 for MS2 if MS2 Application Correctness rubric level is at >= 1")
else:
    print("Timing Rubric level 0")