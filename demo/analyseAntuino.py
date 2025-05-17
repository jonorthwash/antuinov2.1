#!/usr/bin/env python3

import os
from datetime import datetime
import AntuinoTerm

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

time = datetime.now().strftime('%Y%m%d%H%M%S')

for band in bands:
    print(band)
    (frequencies, swrs) = AntuinoTerm.main(bands[band][0], bands[band][1], bands[band][2])

    with open(os.path.join('./', 'logs/', time+'-'+band), 'w') as logfile:
        logfile.write("frequency\tswr\n")
        for (freq, swr) in zip(frequencies, swrs):
            logfile.write(str(freq)+"\t"+str(swr)+"\n")
