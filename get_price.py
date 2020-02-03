import os
from argparse import ArgumentParser

from phonerouting import PhoneOperatorList


def csv_to_dict(filename, delimiter=',', skip_header=1):
    """Read CSV file and convert it into a dictionary based on
    the first two columns. The first column is used as keys of
    type str, the second as the values, which are cast to float.

    Parameters
    ----------
    filename : str
        Path to the CSV file
    delimiter : str
        Delimiter between the columns
    skip_header : int
        Number of lines to skip
    """
    out_dict = {}
    f = open(filename)
    raw = f.read()
    f.close()

    raw = raw.split('\n')
    for line in raw[skip_header:]:
        columns = line.split(delimiter)
        out_dict[columns[0]] = float(columns[1])

    return out_dict


def main():
    script_description = 'Get the cheapest price to call a number along with'
    script_description += ' the  name of the operator. Price lists are loaded'
    script_description += ' from CSV files. By default, all files in the'
    script_description += ' directory operators will be loaded. Alternatively'
    script_description += ' specific operators can be selected using the'
    script_description += ' arguments below.'

    parser = ArgumentParser(description=script_description)
    parser.add_argument('number', type=str,
                        help='Phone number without leading "+" or zeros')
    parser.add_argument('--operators', type=str, default=None, nargs='+',
                        help='CSV files containing the price lists')
    parser.add_argument('--operator-path', type=str, default='operators',
                        help='Path to CSV files containing the price lists')

    args = parser.parse_args()

    if args.operators is None:
        args.operators = [os.path.join(args.operator_path, filename)
                          for filename in os.listdir(args.operator_path)
                          if filename.endswith('.csv')]

    if len(args.operators) == 0:
        raise ValueError("operator-path contains no CSV files")

    # Use filename without extension as operator name
    names = [fn.split('/')[-1][:-4] for fn in args.operators]
    price_lists = [csv_to_dict(fn) for fn in args.operators]

    # Initialize PhoneOperatorList with first operator file
    operator_list = PhoneOperatorList(names, price_lists)

    cheapest = operator_list.get_price(args.number)
    if cheapest[0] is not None:
        print('The cheapest price for this number is with ' +
              f'{cheapest[0]}: ${cheapest[1]:.2f}/minute.')
    else:
        print("This number cannot be called with any of the listed operators.")


if __name__ == '__main__':
    main()
