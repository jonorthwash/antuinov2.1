#!/usr/bin/env python3

import os
from datetime import datetime
import AntuinoTerm
import argparse

bands = {
    '80m': ["3500000", "4000000", "10000"],
    '40m': ["7000000", "7300000", "5000"],
    '30m': ["10100000", "10150000", "2000"],
    '20m': ["14000000", "14350000", "5000"],
    '17m': ["18068000", "18168000", "2000"],
    '15m': ["21000000", "21450000", "10000"],
    '12m': ["24890000", "24990000", "2000"],
    '10m': ["28000000", "29700000", "10000"],
    '06m': ["50000000", "54000000", "20000"],
    '02m': ["144000000", "148000000", "20000"],
    '00.7m': ["420000000", "450000000", "100000"]
}

def make_plot(infile, title, subtitle, outfile):
    with open(infile, 'r') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        x = []
        y = []
        for row in reader:
            x_value = row['frequency']
            y_value = row['swr']

            try:
                x.append(float(x_value))
                y.append(float(y_value))
            except ValueError:
                print(f"Skipping row with invalid data: {row}")

        figsize=(6.4, 4.8)

        fig, ax = plt.subplots(figsize=figsize)

        ax.plot(x, y, lw=5, color='red')
    
        plt.yscale('symlog')
        plt.ylim(1, 6)
        plt.yticks([1, 1.5, 2, 3, 4, 5, 6], [1, 1.5, 2, 3, 4, 5, 6])
        plt.axhline(y=1.5, color='silver')
        plt.axhline(y=2, color='silver')
        plt.axhline(y=3, color='silver')
        plt.axhline(y=4, color='silver')
        plt.axhline(y=5, color='silver')

        plt.grid(True) # Add grid lines
        plt.plot(x, y)
        plt.xlabel('Frequency (MHz)')
        plt.ylabel('SWR')
        plt.suptitle(title, fontsize=24, x=0.53)#, y=1)
        plt.title(subtitle, color='grey')
        plt.tick_params(axis='both', labelsize=18)
        #plt.show()
        #plt.margins(0.015, tight=True)
        #plt.tight_layout()
        margins = {  #     vvv margin in inches
            "left"   :     0.7 / figsize[0],
            "bottom" :     0.6 / figsize[1],
            "right"  : 1 - 0.2 / figsize[0],
            "top"    : 1 - 0.7 / figsize[1]
        }
        fig.subplots_adjust(**margins)


        plt.savefig(outfile)
        plt.close()

def make_plots(logdir):
    tsv_files = [os.path.join(logdir, f) for f in os.listdir(logdir) if re.match(r'.*\.tsv', f)]
    for fn in tsv_files:
        fn_elems = re.search(r'(.*\/([0-9]+)-([0-9\.]+m))\.tsv', fn)
        band = fn_elems[3].lstrip('0')
        band = "70cm" if band==".7m" else band
        date = datetime.strptime(fn_elems[2], '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M')
        outfile = fn_elems[1]+".png"

        make_plot(fn, band, date, outfile)

def sweep(bands, outdir='./logs/'):
    time = datetime.now().strftime('%Y%m%d%H%M%S')

    for band in bands:
        print(band)
        (frequencies, swrs) = AntuinoTerm.main(bands[band][0], bands[band][1], bands[band][2])

        with open(os.path.join(outdir, time+'-'+band+".tsv"), 'w') as logfile:
            logfile.write("frequency\tswr\n")
            for (freq, swr) in zip(frequencies, swrs):
                logfile.write(str(freq)+"\t"+str(swr)+"\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='analyse SWR using Antuino for specified bands')
    parser.add_argument('-l', '--logdir', type=str,
        help='directory to store raw data', default="./logs")
    parser.add_argument('-b', '--bands', type=str,
        help='bands, comma-separated, e.g. "06m,02m,00.7m"', default=None)
    parser.add_argument('-g', '--graph', action='store_true',
        help='generate graphs of all tsv files in log directory', default=None)
    parser.add_argument('-G', '--graph_only', action='store_true',
        help='do not connect to Antuino (useful together with -g, only generate graphs)', default=None)



    args = parser.parse_args()

    if args.bands:
        testBands = {}
        for band in args.bands.split(","):
            print(args.bands, band)
            testBands[band] = bands[band]
    else:
        testBands = bands

    if not args.graph_only:
        sweep(testBands, outdir=args.logdir)

    if args.graph:
        import csv
        import matplotlib.pyplot as plt
        #import matplotlib.patheffects as pe
        import re
        make_plots(args.logdir)
