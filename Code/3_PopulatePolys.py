# -*- coding: utf-8 -*-
''' Author: Nathan Thomas
    Email: nathan.m.thomas@nasa.gov, @DrNASApants
    Date: 11/26/2020
    Version: 1.0
    Copyright 2020 Natha M Thomas
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.'''

# A script to populate the vector
# objects with raster values

import argparse
import rsgislib
from rsgislib import zonalstats
from rsgislib import vectorutils
import glob
import os
from multiprocessing import Pool
import multiprocessing
import subprocess



def PopulateVectors(GPKG, rasterDir, outdir):
    
        rasters = glob.glob(rasterDir + '/*')
        
        outfile = os.path.join(outdir, GPKG.split('/')[-1])
        if os.path.isfile(outfile):
            print('FILE EXISTS: SKIPPING')
        else:
            layername = GPKG.split('/')[-1]
            mem_ds, veclyr = rsgislib.vectorutils.read_vec_lyr_to_mem(GPKG, layername)

            for img in rasters:
                minthresh = -1
                maxthresh = 1
                band = 1
                mean_name = img.split('_')[-1].split('.')[0] + '_mean'
                min_name = img.split('_')[-1].split('.')[0] + '_min'
                max_name = img.split('_')[-1].split('.')[0] + '_max'
                std_name = img.split('_')[-1].split('.')[0] + '_std'
                sum_name = img.split('_')[-1].split('.')[0] + '_sum'
                count_name = img.split('_')[-1].split('.')[0] + '_count'
                mode_name = img.split('_')[-1].split('.')[0] + '_mode'
                med_name = img.split('_')[-1].split('.')[0] + '_med'
                
                rsgislib.zonalstats.calc_zonal_band_stats_test_poly_pts(veclyr, img, band, minthresh, maxthresh, min_field=min_name, max_field=max_name, mean_field=mean_name, stddev_field=std_name, sum_field=sum_name, count_field=count_name, mode_field=mode_name, median_field=med_name, out_no_data_val=0)
                
                print('Done')

            rsgislib.vectorutils.write_vec_lyr_to_file(veclyr, outfile, 'LayerName', 'GPKG', options=['OVERWRITE=YES', 'SPATIAL_INDEX=YES'])


def main():
    print("Use 'python 3_PopulatePolys.py -h' for help")
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--segments", type=str, help="Specify the dir to the vectorized segmentation (GPKGs)")
    parser.add_argument("-r", "--rasters", type=str, help="Specify the dir to the rasters to populate into the objects")
    parser.add_argument("-o", "--outdir", type=str, help="Specify the output dir for the populated vectors")
    parser.add_argument("-c", "--cores", type=str, help="Specify the output dir for the populated vectors")
    args = parser.parse_args()

    if str(args.segments) == None:
        print("INPUT VECTOR SEGMENTATION DIR MISSING")
        os._exit(1)
    elif args.rasters == None:
        print("SPECIFY THE DIR TO THE RASTERS")
        os._exit(1)
    else:
        print(args.segments)

    GPKGDir = args.segments
    GPKGfiles = glob.glob(GPKGDir + '/*.gpkg')
    print(GPKGfiles)

    rastersDir = args.rasters

    rasterDirectory = [rastersDir for x in GPKGfiles]
    outputdirectory = [args.outdir for x in GPKGfiles]
    
    if os.path.isdir(args.outdir):
        print("OUPUT DIR EXISTS")
    else:
        subprocess.call('mkdir ' + args.outdir, shell=True)
    

    ncores = int(args.cores)
    with multiprocessing.Pool(processes=ncores) as pool:
        pool.starmap(PopulateVectors, zip(GPKGfiles, rasterDirectory, outputdirectory))
    

if __name__ == "__main__":
    main()


