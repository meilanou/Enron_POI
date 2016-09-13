#!/usr/bin/python


def outlierCleaner(predictions, ages, net_worths):
    """
        clean away the 10% of points that have the largest
        residual errors (different between the prediction
        and the actual net worth)

        return a list of tuples named cleaned_data where 
        each tuple is of the form (age, net_worth, error)
    """
    
    cleaned_data = []

    ### your code goes here
    import math
    import numpy

    ages = [a.tolist()[0] for a in ages]
    net_worths = [w.tolist()[0] for w in net_worths]
    errors = [math.pow(net_worths[x] - predictions[x], 2) \
              for x in range(len(predictions))]

    cleaned_data = zip(ages, net_worths, errors)
    cleaned_data.sort(key=lambda x: x[2])
    cleaned_data = cleaned_data[:int(len(cleaned_data)*0.9)]

    return cleaned_data

