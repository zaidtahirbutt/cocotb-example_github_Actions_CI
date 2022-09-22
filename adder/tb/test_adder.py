'''
A cocotb-pytest test (this file) has two parts:

1. Testbench 
    - Any python function decorated with @cocotb.test()
    - Drives signals into pins of the design, reads the output/intermediate pins and compares with expected results
    - Uses async-await: 
        - Declared as def async
        - when "await Event()", simulator advances in simulation time until the Event() happens
    - You can have multiple such testbenches too. Pytest would find and run them all
2. PyTest 
    - The setup that connects the simulator of your choice, 
    - Feeds the design files, 
    - Finds your testbenches (1), 
    - Parametrizes them to generate multiple versions of the designs & tests
    - Runs all such tests and prints a report of pass & fails
'''


import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ClockCycles

import random
# import numpy as np

'''
1. Testbench
'''
@cocotb.test()
async def adder_tb(dut):

    ''' Clock Generation '''
    clock = Clock(dut.clk, 10, units="ns") # create a clock for dut.clk pin with 10 ns period
    cocotb.start_soon(clock.start()) # start clock in a seperate thread
#     in1 = {1,1,0,0}
#     in2 = {1,0,1,0}
    
    in1 = [1,1,0,0]
    in2 = [1,0,1,0]
    
    ''' Assign random values to input, wait for a clock and verify output '''
    for i in range(4): # 4 experiments
        
     # generate randomized input
        dut.i_bit1.value = in1[i] # drive pins
        dut.i_bit2.value = in2[i]

        sum_of_bits = in1[i]+in2[i]
        if sum_of_bits == 2:
            expectsum = 0
            expectcarry = 1
        elif sum_of_bits == 1:
            expectsum = 1
            expectcarry = 0
        else:
            expectsum = 0
            expectcarry = 0
        
        await FallingEdge(dut.clk) # wait for falling edge
        
#         computedsum = dut.o_sum.value.integer # Read pins as unsigned integer.
#         computedcarry = dut.o_carry.value.integer # Read pins as signed integer.
        
        computedsum = dut.o_sum.value
        computedcarry = dut.o_carry.value
            
        #assert expectsum == computedsum, f"Failed on the {i}th cycle. Got {computedsum}, expected {expectsum}" # If any assertion fails, the test fails, and the string would be printed in console
        assert expectsum == computedsum, f"Failed on the {i}th cycle. Got {computedsum}, expected {expectsum}" # If any assertion fails, the test fails, and the string would be printed in console
        
        print(f"Driven value: {expectsum} \t received value: {computedsum}")
#         assert expectcarry == computedcarry, f"Failed on the {i}th cycle. Got {computedcarry}, expected {expectcarry}" # If any assertion fails, the test fails, and the string would be printed in console
        assert expectcarry == 2, f"Failed on the {i}th cycle. Got {computedcarry}, expected {expectcarry}" # If any assertion fails, the test fails, and the string would be printed in console
        print(f"Driven value: {expectcarry} \t received value: {computedcarry}") 



'''
2. Pytest Setup
'''

from cocotb_test.simulator import run
import pytest
import glob

@pytest.mark.parametrize(
    # Two sets of parameters to test across
    "parameters", [
#         {"WIDTH_IN": "8", "WIDTH_OUT": "16"},
#         {"WIDTH_IN": "16"}
        {"random_para": "10"}
        ])
def test_adder(parameters):

    run(
        verilog_sources=glob.glob('adder/hdl/*'),
        toplevel="adder",    # top level HDL
        
        module="test_adder", # name of the file that contains @cocotb.test() -- this file
        simulator="icarus",

        parameters=parameters,
        extra_env=parameters,
        sim_build="adder/sim_build/" + ",".join((f"{key}={value}" for key, value in parameters.items())),
    )
