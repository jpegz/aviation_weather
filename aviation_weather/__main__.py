if __name__ == '__main__':
    import argparse
    from .tools import aviation_weather
    PARSER = argparse.ArgumentParser(description='Get metars or tafs for the specified stations')
    PARSER.add_argument('--hours-before-now', required=False, default=24,
                        help='hours before now')
    PARSER.add_argument('--most-recent', '-r', required=False, default=True, action='store_true',
                        help='Only return most recent metars or tafs for the stations')
    PARSER.add_argument('data_source', choices=['metars', 'tafs'])
    PARSER.add_argument('--text', '-t', required=False, default=True, action='store_true',
                        help='display in human-readable text format')
    PARSER.add_argument('stations', nargs='+',
                        help='station code or short code for multiple stations')
    ARGS = PARSER.parse_args()
    STATIONS = ','.join(ARGS.stations)
    RESULT = aviation_weather(ARGS.data_source, STATIONS,
                              ARGS.hours_before_now, ARGS.most_recent,
                              ARGS.text)
    if ARGS.text:
        print(RESULT)
    elif len(RESULT) > 0:
        print('\n'.join(RESULT))
    else:
        raise ValueError("Error encountered outputting results.")
