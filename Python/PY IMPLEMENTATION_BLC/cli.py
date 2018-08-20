import argparse

from blockchain import Blockchain
from pow import Pow


def new_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--print", help="print all the blocks of the blockchain", action="store_true")
    parser.add_argument("--add", type=str,
                        help="add a block to the blockchain")

    return parser


def add_block(bc, data):
    bc.add_block(data)
    print("Success!")


def print_chain(bc):
    for block in bc.blocks:
        print("Prev. hash: {0}".format(block.prev_block_hash))
        print("Data: {0}".format(block.data))
        print("Hash: {0}".format(block.hash))
        pow = Pow(block)
        print("PoW: {0}".format(pow.validate()))


if __name__ == '__main__':
    parser = new_parser()
    args = parser.parse_args()
    bc = Blockchain()

    if args.print:
        print_chain(bc)

    if args.add:
        add_block(bc, args.add)
