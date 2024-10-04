minimum = min

from astropy.units import *
from scipy.constants import *
from astropy.constants import *
from uncertainties import *
from uncertainties import unumpy

def from_excel(with_errs = False):
    print("Paste the values from excel (only one column):")
    numbers = []

    def input_nums(arr):
        while True:
            val = input("")
            if val == "":
                break
            try:
                arr.append(float(val))
            except ValueError:
                print("Invalid input. Please try again.")
            
    input_nums(numbers)

    if with_errs:
        errs = []
        print("Paste the errors from excel (only one column):")
        input_nums(errs)
        if len(numbers) != len(errs):
            print("Error: Number of values and errors do not match.")
        return unumpy.uarray(numbers, errs)
    
    return excel_to_ufloats(numbers)


def excel_to_ufloats(numbers):
    
    def determine_uncertainty(value): # for multimeter measurements
        import math
        power = math.floor(math.log(abs(value), 10))
        if math.floor(abs(value / 10 ** power)) < 6:
            return 10 ** (power - 3)
        else:
            val_str = str(value)
            err_pow = val_str[::-1].find('.')
            if err_pow == -1:
                err_pow = len(val_str) - len(val_str.rstrip('0'))
            else:
                err_pow *= -1
            return 10 ** minimum(power - 2, err_pow)
    
    uerrors = [determine_uncertainty(num) for num in numbers if num]
    
    # Return as uarray
    return unumpy.uarray(numbers, uerrors)

def to_excel(uarray):
    # Extract nominal values and standard deviations
    values = unumpy.nominal_values(uarray)
    errors = unumpy.std_devs(uarray)

    print("Values: ")
    
    # Format values and errors as strings
    value_str = '\r\n'.join(f"{v:.10g}" for v in values) + '\r\n'
    print(value_str)
    print("Errors: ")

    error_str = '\r\n'.join(f"{e:.10g}" for e in errors) + '\r\n'
    print(error_str)
    # return value_str, error_str