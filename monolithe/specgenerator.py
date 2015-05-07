#!/usr/bin/env python

import argparse
import sys

sys.path.append("../")


def main(argv=sys.argv):
    parser = argparse.ArgumentParser(description="VSD Specs Generator.")

    parser.add_argument('-u', "--vsdurl",
                        dest="vsdurl",
                        help="URL of your VSD API where to get the get JSON information without version (ex: https://host:port/web/docs/api/)",
                        type=str)

    parser.add_argument('-v', "--apiversion",
                        dest="version",
                        help="version of the spec to generate (example: 3.2)",
                        type=float)

    parser.add_argument('-f', "--file",
                        dest="path",
                        help="Path to a repository containing api-docs file ",
                        type=str)

    parser.add_argument('-o', "--output",
                        dest='dest',
                        help="directory where the sources will be generated",
                        type=str)

    args = parser.parse_args()

    from monolithe import Command

    Command.generate_specs(vsdurl=args.vsdurl, path=args.path, apiversion=args.version, output_path=args.dest)

if __name__ == '__main__':
    main()