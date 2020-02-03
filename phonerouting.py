import re
import warnings
import numpy as np


def check_number_string(string):
    """Check that string only consists of numbers

    Parameters
    ----------
    string : str
    """
    return not bool(re.compile(r'[^z0-9]').search(string))


class PhoneOperator(object):
    """Class for organizing the phone number prefixes in a tree structre.
    The tree has up to ten branches from a single note, representing all
    possible next digits in the prefix. Complexity of the prefix matching
    should thus be O(log10(prefix)).

    Parameters
    ----------
    price_list : dict
        Ditcionary with prefixes as keys and prices per minute as values
        prefixes must be strings, prices must be floats

    validate : bool
        Test that price_list has keys and values of the correct types
        and that keys only contains digits
    """

    def __init__(self, price_list, validate=True):
        if validate:
            for prefix, price in price_list.items():
                if type(prefix) != str:
                    raise TypeError('Keys of price_list must be strings.')
                if not check_number_string(prefix):
                    raise ValueError('Keys of price_list may only contain ' +
                                     'digits.')
                if type(price) != float:
                    raise TypeError('Prices must be floats.')

        self._sub_operators = {}

        # An empty string as a prefix means the associated price is to be
        # used when the prefix cannot be extended further
        if '' in price_list.keys():
            self.price = price_list['']
        else:
            self.price = np.inf

        # Sort the prefixes by starting digit and pass those prefixes to
        # new PhoneOperators after removing the starting digit
        for k in range(10):
            k = str(k)
            new_price_list = {prefix[1:]: price
                              for prefix, price in price_list.items()
                              if prefix.startswith(k)}
            if len(new_price_list) > 0:
                self._sub_operators[k] = PhoneOperator(new_price_list,
                                                       validate=False)

    def get_price(self, number):
        """Search the list for the price to call a given phone number

        Parameters
        ----------
        number: str
            Phone number to search for, should only contain numbers
        """
        if type(number) != str:
            raise TypeError('number must be a string')
        if not check_number_string(number):
            raise ValueError('number may only contain the numbers 0-9')

        if len(number) == 0:
            warnings.warn('The number you entered was exactly as long as ' +
                          ' a prefix or shorter. The result may be ' +
                          'inaccurate.')
            return self.price
        elif number[0] not in self._sub_operators.keys():
            # There is no longer prefix matching this number
            return self.price
        else:
            # Longer matching prefix exists
            price = self._sub_operators[number[0]].get_price(number[1:])

            if np.isinf(price):
                # Double check whether there was a valid price along the way
                return self.price
            else:
                return price


class PhoneOperatorList(object):
    """Class for organizing multiple PhoneOperators and querying the best
    price among them.

    Parameters
    ----------
    names : list
        List of names of the operators [str]
    price_lists : list
        List ditcionaries with prefixes as keys and prices per minute as values
        prefixes must be strings, prices must be floats
    """
    def __init__(self, names, price_lists):
        self.names = names
        self.operators = [PhoneOperator(pl) for pl in price_lists]

    def get_price(self, number):
        """Search the list of each operator for the price to call a given phone
        number and return the cheapest option.

        Parameters
        ----------
        number: str
            Phone number to search for, should only contain numbers
        """
        prices = np.array([op.get_price(number) for op in self.operators])

        # Check that at least one result is not np.inf (i.e. no price)
        if np.any(~np.isinf(prices)):
            k = np.argmin(prices)
            return self.names[k], prices[k]
        else:
            return None, np.inf
