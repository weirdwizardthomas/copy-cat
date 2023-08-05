import argparse


def get_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('--source', '-s',
                        required=True,
                        type=str,
                        help='Source directory to replicate.')

    parser.add_argument('--replica', '-r',
                        required=True,
                        type=str,
                        help='Path to the replica directory.')

    parser.add_argument('--log', '-l',
                        required=True,
                        type=str,
                        help='File to write logs to.')

    parser.add_argument('--interval', '-i',
                        type=float,
                        default=500,
                        help='Synchronization interval in milliseconds [ms].')

    return parser.parse_args()
