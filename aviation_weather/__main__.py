import argparse

from .tools import aviation_weather


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Get metar or taf for the specified stations"
    )
    parser.add_argument("data_source", choices=["metar", "taf"])
    parser.add_argument(
        "stations",
        nargs="+",
        help="ICAO station code(s)",
    )
    parser.add_argument(
        "--hours-before-now",
        required=False,
        default=24,
        type=int,
        help="How many hours back to search (default: 24)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        default=False,
        help="Return all results in the time window instead of only the most recent",
    )
    parser.add_argument(
        "--text",
        "-t",
        action="store_true",
        default=False,
        help="Display in human-readable text format instead of raw",
    )

    args = parser.parse_args()
    most_recent = not args.all
    stations = ",".join(args.stations)
    result = aviation_weather(
        args.data_source, stations, args.hours_before_now, most_recent, args.text
    )
    if isinstance(result, list):
        print("\n".join(result))
    else:
        print(result)


if __name__ == "__main__":
    main()
