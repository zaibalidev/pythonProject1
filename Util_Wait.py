import time
from random import randint

def wait_Min():
    time.sleep(1)

def wait_Min2():
    time.sleep(3)

def wait_Med():
    time.sleep(5)


def wait_Max():
    time.sleep(8)


def wait_Custom(_size):
    time.sleep(_size)

def wait_exponential(_exp_size):
    # # random milisecconds between 10-1000 and then converting to seconds
    # random_number_milliseconds = int(randint(10, 1000)/1000)
    random_number = randint(1, 5)
    maximum_backoff = 64
    n = _exp_size
    two_power_n = 1
    for power in range(n):
        two_power_n = two_power_n*2

    # wait_time = min(((2^n) + random_number_milliseconds), maximum_backoff)
    wait_time = min((two_power_n + random_number), maximum_backoff)
    if _exp_size>0:
        print("wait_exponential wait_time:"+str(wait_time))
        time.sleep(wait_time)

