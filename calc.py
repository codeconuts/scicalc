minimum = min

from astropy.units import *
from scipy.constants import *
from astropy.constants import *
from uncertainties import *
from uncertainties import unumpy

def multimeter(str_arr):

    def multimeter_uncertainty(val_str):
        
        import math
        value = float(val_str)
        power = math.floor(math.log(abs(value), 10))
        if math.floor(abs(value / 10 ** power)) < 6:
            return 10 ** (power - 3)
        else:
            err_pow = val_str[::-1].find('.')
            if err_pow == -1:
                err_pow = len(val_str) - len(val_str.rstrip('0'))
            else:
                err_pow *= -1
            return 10 ** minimum(power - 2, err_pow)
        
    return [multimeter_uncertainty(str) for str in str_arr if str]

def oscilloscope(str_arr):

    def sig_fig(val_str):
        err_pow = val_str[::-1].find('.')
        if err_pow == -1:
            err_pow = len(val_str) - len(val_str.rstrip('0'))
        else:
            err_pow *= -1
        return err_pow
    
    max_err_pow = max([sig_fig(str) for str in str_arr if str])
    return [max_err_pow] * len(str_arr)


def from_excel(with_errs = False, determine_uncertainty = multimeter):
    print("Paste the values from excel (only one column):")
    numbers = []

    def input_nums(arr):
        while True:
            val = input("")
            if val == "":
                break
            try:
                float(val)
                arr.append(val)
            except ValueError:
                print("Invalid input. Please try again.")
            
    input_nums(numbers)

    if with_errs:
        errs = []
        print("Paste the errors from excel (only one column):")
        input_nums(errs)
        if len(numbers) > len(errs):
            print(f"Error: There are {len(numbers)} numbers but {len(errs)} errors. Truncating the numbers array.")
        elif len(errs) > len(numbers):
            print(f"Error: There are {len(numbers)} numbers but {len(errs)} errors. Truncating the errors array.")
        length = minimum(len(numbers), len(errs))
        return unumpy.uarray(numbers[:length], errs[:length])
    
    return excel_to_ufloats(numbers, determine_uncertainty)


def excel_to_ufloats(numbers, determine_uncertainty = multimeter):
    
    uerrors = determine_uncertainty(numbers)
    
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