#!/usr/bin/env python3

import os
from datetime import datetime
import AntuinoTerm
import argparse

bands = {
    '80m': ["3500000", "4000000", "10000"],
    '40m': ["3500000", "4000000", "10000"],
    '30m': ["10100000", "10150000", "5000"],
    '20m': ["14000000", "14350000", "10000"],
    '17m': ["18068000", "18168000", "5000"],
    '15m': ["21000000", "21450000", "10000"],
    '12m': ["24890000", "24990000", "5000"],
    '10m': ["28000000", "29700000", "10000"],
    '06m': ["50000000", "54000000", "20000"],
    '02m': ["144000000", "148000000", "20000"],
    '00.7m': ["420000000", "450000000", "100000"]
}

def main(bands, outdir='./logs/'):
    time = datetime.now().strftime('%Y%m%d%H%M%S')

    for band in bands:
        print(band)
        (frequencies, swrs) = AntuinoTerm.main(bands[band][0], bands[band][1], bands[band][2])

        with open(os.path.join(outdir, time+'-'+band), 'w') as logfile:
            logfile.write("frequency\tswr\n")
            for (freq, swr) in zip(frequencies, swrs):
                logfile.write(str(freq)+"\t"+str(swr)+"\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='analyse SWR using Antuino for specified bands')
    parser.add_argument('-l', '--logdir', type=str,
        help='directory to store raw data', default="./logs")
    parser.add_argument('-b', '--bands', type=str,
        help='bands, comma-separated, e.g. "06m,02m,00.7m"', default=None)

    args = parser.parse_args()

    if args.bands:
        testBands = {}
        for band in args.bands.split(","):
            print(args.bands, band)
            testBands[band] = bands[band]
    else:
        testBands = bands

    main(testBands, outdir=args.logdir)


