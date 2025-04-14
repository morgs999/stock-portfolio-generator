"""
Generates performance reports for your stock portfolio.
"""
import argparse
import sys
import csv
from collections import OrderedDict
import requests
import json


def main():
    """
    Entrypoint into program.
    """
    get_args()
    input_file = sys.argv[2]
    output_file = sys.argv[4]
    data = calculate_metrics(input_file=read_portfolio(input_file), market_data=get_market_data('SNAP,AAPL,AMZN'))
    save_portfolio(output_data=data, filename=output_file)


def read_portfolio(filename):
    """
    Returns data from a CSV file
    """
    with open(filename, newline='') as input_file:
        csv_reader = csv.DictReader(input_file, delimiter=',')
        for row in csv_reader:
            return OrderedDict([
                ('symbol', row['symbol']),
                ('units', row['units']),
                ('cost', row['cost'])
            ])
        return input_file


def get_args(args=None):
    """
    Parse and return command line argument values
    """
    parser = argparse.ArgumentParser(description='Set source and target for CSV Files')
    parser.add_argument('--source', help='Which CSV File to import symbols from')
    parser.add_argument('--target', help='Which CSV File to write values to')
    return parser.parse_args(args)


def get_market_data(stocks_list):
    """
    Get the latest market data for the given stock symbols
    """
    # my_token = pk_757c3f05c0b747188a68d8157b3f73e4
    api = f'https://cloud.iexapis.com/stable/tops?token=pk_757c3f05c0b747188a68d8157b3f73e4&symbols={stocks_list}'
    response = requests.get(api)
    market_data = json.loads(response.content)
    return market_data


def calculate_metrics(input_file, market_data):
    """
    Calculates the various metrics of each of the stocks
    -symbol: The stock ticker symbol
    -units: The amount of shares held
    -cost: The original cost per share
    -latest_price: The latest market price per share
    -book_value: The value of the shares at time of purchase
    -market_value: The value of the shares based on the latest market value
    -gain_loss: The dollar amount either gained or lost
    -change: A percentage (decimal) of the gain/loss
    """
    symbol = read_portfolio(input_file.get('symbol'))
    units = int(read_portfolio(input_file.get('units')))
    cost = int(read_portfolio(input_file.get('cost')))
    latest_price = int(market_data.lastSalePrice)
    book_value = units * cost
    market_value = units * latest_price
    gain_loss = market_value - book_value
    change = f'{(gain_loss / book_value)*100}%'

    output_data = [symbol, units, cost, latest_price, book_value, market_value, gain_loss, change]

    return output_data


def save_portfolio(output_data, filename):
    """
    Saves data to a CSV file
    """
    with open(filename, 'w', newline='') as file:
        fieldnames = ['symbol', 'units', 'cost', 'latest_price', 'book_value', 'market_value', 'gain_loss', 'change']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerows(output_data)


if __name__ == '__main__':
    main()
