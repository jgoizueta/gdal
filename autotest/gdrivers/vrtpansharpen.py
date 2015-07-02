#!/usr/bin/env python
###############################################################################
# $Id$
#
# Project:  GDAL/OGR Test Suite
# Purpose:  Test VRTPansharpenedDataset support.
# Author:   Even Rouault <even.rouault at spatialys.com>
# 
###############################################################################
# Copyright (c) 2015, Even Rouault <even.rouault at spatialys.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
###############################################################################

import sys
from osgeo import gdal

sys.path.append( '../pymod' )

import gdaltest

###############################################################################
# Error cases

def vrtpansharpen_1():
    
    src_ds = gdal.Open('data/small_world.tif')
    src_data = src_ds.GetRasterBand(1).ReadRaster()
    src_ds = None
    pan_ds = gdal.GetDriverByName('GTiff').Create('tmp/small_world_pan.tif', 800, 400)
    pan_ds.GetRasterBand(1).WriteRaster(0,0,800,400,src_data,400,200)
    pan_ds = None
    
    # Missing PansharpeningOptions
    gdal.PushErrorHandler()
    vrt_ds = gdal.Open("""<VRTDataset rasterXSize="800" rasterYSize="400" subClass="VRTPansharpenedDataset">
    <VRTRasterBand dataType="Byte" band="1" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Red</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="2" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Green</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="3" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Blue</ColorInterp>
    </VRTRasterBand>
</VRTDataset>""")
    gdal.PopErrorHandler()
    if vrt_ds is not None:
        gdaltest.post_reason('fail')
        return 'fail'

    # PanchroBand missing
    gdal.PushErrorHandler()
    vrt_ds = gdal.Open("""<VRTDataset rasterXSize="800" rasterYSize="400" subClass="VRTPansharpenedDataset">
    <VRTRasterBand dataType="Byte" band="1" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Red</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="2" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Green</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="3" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Blue</ColorInterp>
    </VRTRasterBand>
    <PansharpeningOptions>
        <Algorithm>WeightedBrovey</Algorithm>
        <AlgorithmOptions>
            <Weights>0.33333,0.333333,0.333333</Weights>
        </AlgorithmOptions>
        <Resampling>Cubic</Resampling>
        <NumThreads>ALL_CPUS</NumThreads>
        <BitDepth>8</BitDepth>
        <SpectralBand dstBand="1">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="2">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>2</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="3">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>3</SourceBand>
        </SpectralBand>
    </PansharpeningOptions>
</VRTDataset>""")
    gdal.PopErrorHandler()
    if vrt_ds is not None:
        gdaltest.post_reason('fail')
        return 'fail'

    # PanchroBand.SourceFilename missing
    gdal.PushErrorHandler()
    vrt_ds = gdal.Open("""<VRTDataset rasterXSize="800" rasterYSize="400" subClass="VRTPansharpenedDataset">
    <VRTRasterBand dataType="Byte" band="1" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Red</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="2" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Green</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="3" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Blue</ColorInterp>
    </VRTRasterBand>
    <PansharpeningOptions>
        <Algorithm>WeightedBrovey</Algorithm>
        <AlgorithmOptions>
            <Weights>0.33333,0.333333,0.333333</Weights>
        </AlgorithmOptions>
        <Resampling>Cubic</Resampling>
        <NumThreads>ALL_CPUS</NumThreads>
        <BitDepth>8</BitDepth>
        <PanchroBand>
        </PanchroBand>
        <SpectralBand dstBand="1">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="2">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>2</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="3">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>3</SourceBand>
        </SpectralBand>
    </PansharpeningOptions>
</VRTDataset>""")
    gdal.PopErrorHandler()
    if vrt_ds is not None:
        gdaltest.post_reason('fail')
        return 'fail'

    # Invalid dataset name
    gdal.PushErrorHandler()
    vrt_ds = gdal.Open("""<VRTDataset rasterXSize="800" rasterYSize="400" subClass="VRTPansharpenedDataset">
    <VRTRasterBand dataType="Byte" band="1" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Red</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="2" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Green</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="3" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Blue</ColorInterp>
    </VRTRasterBand>
    <PansharpeningOptions>
        <Algorithm>WeightedBrovey</Algorithm>
        <AlgorithmOptions>
            <Weights>0.33333,0.333333,0.333333</Weights>
        </AlgorithmOptions>
        <Resampling>Cubic</Resampling>
        <NumThreads>ALL_CPUS</NumThreads>
        <BitDepth>8</BitDepth>
        <PanchroBand>
                <SourceFilename relativeToVRT="0">/does/not/exist</SourceFilename>
                <SourceBand>1</SourceBand>
        </PanchroBand>
        <SpectralBand dstBand="1">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="2">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>2</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="3">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>3</SourceBand>
        </SpectralBand>
    </PansharpeningOptions>
</VRTDataset>""")
    gdal.PopErrorHandler()
    if vrt_ds is not None:
        gdaltest.post_reason('fail')
        return 'fail'

    # Inconsistant declared VRT dimensions with panchro dataset
    gdal.PushErrorHandler()
    vrt_ds = gdal.Open("""<VRTDataset rasterXSize="1800" rasterYSize="400" subClass="VRTPansharpenedDataset">
    <VRTRasterBand dataType="Byte" band="1" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Red</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="2" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Green</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="3" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Blue</ColorInterp>
    </VRTRasterBand>
    <PansharpeningOptions>
        <Algorithm>WeightedBrovey</Algorithm>
        <AlgorithmOptions>
            <Weights>0.33333,0.333333,0.333333</Weights>
        </AlgorithmOptions>
        <Resampling>Cubic</Resampling>
        <NumThreads>ALL_CPUS</NumThreads>
        <BitDepth>8</BitDepth>
        <PanchroBand>
                <SourceFilename relativeToVRT="1">tmp/small_world_pan.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </PanchroBand>
        <SpectralBand dstBand="1">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="2">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>2</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="3">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>3</SourceBand>
        </SpectralBand>
    </PansharpeningOptions>
</VRTDataset>""")
    gdal.PopErrorHandler()
    if vrt_ds is not None:
        gdaltest.post_reason('fail')
        return 'fail'

    # VRTRasterBand of unrecognised subclass 'blabla'
    gdal.PushErrorHandler()
    vrt_ds = gdal.Open("""<VRTDataset rasterXSize="800" rasterYSize="400" subClass="VRTPansharpenedDataset">
    <VRTRasterBand dataType="Byte" band="1" subClass="blabla">
        <ColorInterp>Red</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="2" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Green</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="3" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Blue</ColorInterp>
    </VRTRasterBand>
    <PansharpeningOptions>
        <Algorithm>WeightedBrovey</Algorithm>
        <AlgorithmOptions>
            <Weights>0.33333,0.333333,0.333333</Weights>
        </AlgorithmOptions>
        <Resampling>Cubic</Resampling>
        <NumThreads>ALL_CPUS</NumThreads>
        <BitDepth>8</BitDepth>
        <PanchroBand>
                <SourceFilename relativeToVRT="1">tmp/small_world_pan.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </PanchroBand>
        <SpectralBand dstBand="1">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="2">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>2</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="3">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>3</SourceBand>
        </SpectralBand>
    </PansharpeningOptions>
</VRTDataset>""")
    gdal.PopErrorHandler()
    if vrt_ds is not None:
        gdaltest.post_reason('fail')
        return 'fail'

    # Algorithm unsupported_alg unsupported
    gdal.PushErrorHandler()
    vrt_ds = gdal.Open("""<VRTDataset rasterXSize="800" rasterYSize="400" subClass="VRTPansharpenedDataset">
    <VRTRasterBand dataType="Byte" band="1" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Red</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="2" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Green</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="3" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Blue</ColorInterp>
    </VRTRasterBand>
    <PansharpeningOptions>
        <Algorithm>unsupported_alg</Algorithm>
        <AlgorithmOptions>
            <Weights>0.33333,0.333333,0.333333</Weights>
        </AlgorithmOptions>
        <Resampling>Cubic</Resampling>
        <NumThreads>ALL_CPUS</NumThreads>
        <BitDepth>8</BitDepth>
        <PanchroBand>
                <SourceFilename relativeToVRT="1">tmp/small_world_pan.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </PanchroBand>
        <SpectralBand dstBand="1">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="2">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>2</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="3">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>3</SourceBand>
        </SpectralBand>
    </PansharpeningOptions>
</VRTDataset>""")
    gdal.PopErrorHandler()
    if vrt_ds is not None:
        gdaltest.post_reason('fail')
        return 'fail'

    # 10 invalid band of tmp/small_world_pan.tif
    gdal.PushErrorHandler()
    vrt_ds = gdal.Open("""<VRTDataset rasterXSize="800" rasterYSize="400" subClass="VRTPansharpenedDataset">
    <VRTRasterBand dataType="Byte" band="1" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Red</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="2" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Green</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="3" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Blue</ColorInterp>
    </VRTRasterBand>
    <PansharpeningOptions>
        <Algorithm>WeightedBrovey</Algorithm>
        <AlgorithmOptions>
            <Weights>0.33333,0.333333,0.333333</Weights>
        </AlgorithmOptions>
        <Resampling>Cubic</Resampling>
        <NumThreads>ALL_CPUS</NumThreads>
        <BitDepth>8</BitDepth>
        <PanchroBand>
                <SourceFilename relativeToVRT="1">tmp/small_world_pan.tif</SourceFilename>
                <SourceBand>10</SourceBand>
        </PanchroBand>
        <SpectralBand dstBand="1">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="2">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>2</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="3">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>3</SourceBand>
        </SpectralBand>
    </PansharpeningOptions>
</VRTDataset>""")
    gdal.PopErrorHandler()
    if vrt_ds is not None:
        gdaltest.post_reason('fail')
        return 'fail'

    # SpectralBand.dstBand = '-1' invalid
    gdal.PushErrorHandler()
    vrt_ds = gdal.Open("""<VRTDataset rasterXSize="800" rasterYSize="400" subClass="VRTPansharpenedDataset">
    <VRTRasterBand dataType="Byte" band="1" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Red</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="2" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Green</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="3" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Blue</ColorInterp>
    </VRTRasterBand>
    <PansharpeningOptions>
        <Algorithm>WeightedBrovey</Algorithm>
        <AlgorithmOptions>
            <Weights>0.33333,0.333333,0.333333</Weights>
        </AlgorithmOptions>
        <Resampling>Cubic</Resampling>
        <NumThreads>ALL_CPUS</NumThreads>
        <BitDepth>8</BitDepth>
        <PanchroBand>
                <SourceFilename relativeToVRT="1">tmp/small_world_pan.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </PanchroBand>
        <SpectralBand dstBand="-1">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="2">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>2</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="3">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>3</SourceBand>
        </SpectralBand>
    </PansharpeningOptions>
</VRTDataset>""")
    gdal.PopErrorHandler()
    if vrt_ds is not None:
        gdaltest.post_reason('fail')
        return 'fail'


    # SpectralBand.SourceFilename missing
    gdal.PushErrorHandler()
    vrt_ds = gdal.Open("""<VRTDataset rasterXSize="800" rasterYSize="400" subClass="VRTPansharpenedDataset">
    <VRTRasterBand dataType="Byte" band="1" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Red</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="2" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Green</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="3" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Blue</ColorInterp>
    </VRTRasterBand>
    <PansharpeningOptions>
        <Algorithm>WeightedBrovey</Algorithm>
        <AlgorithmOptions>
            <Weights>0.33333,0.333333,0.333333</Weights>
        </AlgorithmOptions>
        <Resampling>Cubic</Resampling>
        <NumThreads>ALL_CPUS</NumThreads>
        <BitDepth>8</BitDepth>
        <PanchroBand>
                <SourceFilename relativeToVRT="1">tmp/small_world_pan.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </PanchroBand>
        <SpectralBand dstBand="1">
                <SourceBand>1</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="2">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>2</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="3">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>3</SourceBand>
        </SpectralBand>
    </PansharpeningOptions>
</VRTDataset>""")
    gdal.PopErrorHandler()
    if vrt_ds is not None:
        gdaltest.post_reason('fail')
        return 'fail'

    # Invalid dataset name
    gdal.PushErrorHandler()
    vrt_ds = gdal.Open("""<VRTDataset rasterXSize="800" rasterYSize="400" subClass="VRTPansharpenedDataset">
    <VRTRasterBand dataType="Byte" band="1" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Red</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="2" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Green</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="3" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Blue</ColorInterp>
    </VRTRasterBand>
    <PansharpeningOptions>
        <Algorithm>WeightedBrovey</Algorithm>
        <AlgorithmOptions>
            <Weights>0.33333,0.333333,0.333333</Weights>
        </AlgorithmOptions>
        <Resampling>Cubic</Resampling>
        <NumThreads>ALL_CPUS</NumThreads>
        <BitDepth>8</BitDepth>
        <PanchroBand>
                <SourceFilename relativeToVRT="1">tmp/small_world_pan.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </PanchroBand>
        <SpectralBand dstBand="1">
                <SourceFilename relativeToVRT="1">/does/not/exist</SourceFilename>
                <SourceBand>1</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="2">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>2</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="3">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>3</SourceBand>
        </SpectralBand>
    </PansharpeningOptions>
</VRTDataset>""")
    gdal.PopErrorHandler()
    if vrt_ds is not None:
        gdaltest.post_reason('fail')
        return 'fail'

    # 10 invalid band of data/small_world.tif
    gdal.PushErrorHandler()
    vrt_ds = gdal.Open("""<VRTDataset rasterXSize="800" rasterYSize="400" subClass="VRTPansharpenedDataset">
    <VRTRasterBand dataType="Byte" band="1" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Red</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="2" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Green</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="3" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Blue</ColorInterp>
    </VRTRasterBand>
    <PansharpeningOptions>
        <Algorithm>WeightedBrovey</Algorithm>
        <AlgorithmOptions>
            <Weights>0.33333,0.333333,0.333333</Weights>
        </AlgorithmOptions>
        <Resampling>Cubic</Resampling>
        <NumThreads>ALL_CPUS</NumThreads>
        <BitDepth>8</BitDepth>
        <PanchroBand>
                <SourceFilename relativeToVRT="1">tmp/small_world_pan.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </PanchroBand>
        <SpectralBand dstBand="1">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>10</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="2">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>2</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="3">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>3</SourceBand>
        </SpectralBand>
    </PansharpeningOptions>
</VRTDataset>""")
    gdal.PopErrorHandler()
    if vrt_ds is not None:
        gdaltest.post_reason('fail')
        return 'fail'

    # Another spectral band is already mapped to output band 1
    gdal.PushErrorHandler()
    vrt_ds = gdal.Open("""<VRTDataset rasterXSize="800" rasterYSize="400" subClass="VRTPansharpenedDataset">
    <VRTRasterBand dataType="Byte" band="1" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Red</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="2" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Green</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="3" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Blue</ColorInterp>
    </VRTRasterBand>
    <PansharpeningOptions>
        <Algorithm>WeightedBrovey</Algorithm>
        <AlgorithmOptions>
            <Weights>0.33333,0.333333,0.333333</Weights>
        </AlgorithmOptions>
        <Resampling>Cubic</Resampling>
        <NumThreads>ALL_CPUS</NumThreads>
        <BitDepth>8</BitDepth>
        <PanchroBand>
                <SourceFilename relativeToVRT="1">tmp/small_world_pan.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </PanchroBand>
        <SpectralBand dstBand="1">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="1">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>2</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="3">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>3</SourceBand>
        </SpectralBand>
    </PansharpeningOptions>
</VRTDataset>""")
    gdal.PopErrorHandler()
    if vrt_ds is not None:
        gdaltest.post_reason('fail')
        return 'fail'

    # No spectral band defined
    gdal.PushErrorHandler()
    vrt_ds = gdal.Open("""<VRTDataset rasterXSize="800" rasterYSize="400" subClass="VRTPansharpenedDataset">
    <VRTRasterBand dataType="Byte" band="1" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Red</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="2" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Green</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="3" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Blue</ColorInterp>
    </VRTRasterBand>
    <PansharpeningOptions>
        <Algorithm>WeightedBrovey</Algorithm>
        <AlgorithmOptions>
            <Weights>0.33333,0.333333,0.333333</Weights>
        </AlgorithmOptions>
        <Resampling>Cubic</Resampling>
        <NumThreads>ALL_CPUS</NumThreads>
        <BitDepth>8</BitDepth>
        <PanchroBand>
                <SourceFilename relativeToVRT="1">tmp/small_world_pan.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </PanchroBand>
    </PansharpeningOptions>
</VRTDataset>""")
    gdal.PopErrorHandler()
    if vrt_ds is not None:
        gdaltest.post_reason('fail')
        return 'fail'

    # Hole in SpectralBand.dstBand numbering
    gdal.PushErrorHandler()
    vrt_ds = gdal.Open("""<VRTDataset subClass="VRTPansharpenedDataset">
    <PansharpeningOptions>
        <Algorithm>WeightedBrovey</Algorithm>
        <AlgorithmOptions>
            <Weights>0.33333,0.333333,0.333333</Weights>
        </AlgorithmOptions>
        <Resampling>Cubic</Resampling>
        <NumThreads>ALL_CPUS</NumThreads>
        <BitDepth>8</BitDepth>
        <PanchroBand>
                <SourceFilename relativeToVRT="1">tmp/small_world_pan.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </PanchroBand>
        <SpectralBand dstBand="1">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="2">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>2</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="4">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>3</SourceBand>
        </SpectralBand>
    </PansharpeningOptions>
</VRTDataset>""")
    gdal.PopErrorHandler()
    if vrt_ds is not None:
        gdaltest.post_reason('fail')
        return 'fail'

    # Band 4 of type VRTPansharpenedRasterBand, but no corresponding SpectralBand
    gdal.PushErrorHandler()
    vrt_ds = gdal.Open("""<VRTDataset rasterXSize="800" rasterYSize="400" subClass="VRTPansharpenedDataset">
    <VRTRasterBand dataType="Byte" band="1" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Red</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="2" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Green</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="3" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Blue</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="4" subClass="VRTPansharpenedRasterBand">
    </VRTRasterBand>
    <PansharpeningOptions>
        <Algorithm>WeightedBrovey</Algorithm>
        <AlgorithmOptions>
            <Weights>0.33333,0.333333,0.333333</Weights>
        </AlgorithmOptions>
        <Resampling>Cubic</Resampling>
        <NumThreads>ALL_CPUS</NumThreads>
        <BitDepth>8</BitDepth>
        <PanchroBand>
                <SourceFilename relativeToVRT="1">tmp/small_world_pan.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </PanchroBand>
        <SpectralBand dstBand="1">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="2">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>2</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="3">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>3</SourceBand>
        </SpectralBand>
    </PansharpeningOptions>
</VRTDataset>""")
    gdal.PopErrorHandler()
    if vrt_ds is not None:
        gdaltest.post_reason('fail')
        return 'fail'

    # SpectralBand.dstBand = '3' invalid
    gdal.PushErrorHandler()
    vrt_ds = gdal.Open("""<VRTDataset rasterXSize="800" rasterYSize="400" subClass="VRTPansharpenedDataset">
    <VRTRasterBand dataType="Byte" band="1" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Red</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="2" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Green</ColorInterp>
    </VRTRasterBand>
    <PansharpeningOptions>
        <Algorithm>WeightedBrovey</Algorithm>
        <AlgorithmOptions>
            <Weights>0.33333,0.333333,0.333333</Weights>
        </AlgorithmOptions>
        <Resampling>Cubic</Resampling>
        <NumThreads>ALL_CPUS</NumThreads>
        <BitDepth>8</BitDepth>
        <PanchroBand>
                <SourceFilename relativeToVRT="1">tmp/small_world_pan.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </PanchroBand>
        <SpectralBand dstBand="1">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="2">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>2</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="3">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>3</SourceBand>
        </SpectralBand>
    </PansharpeningOptions>
</VRTDataset>""")
    gdal.PopErrorHandler()
    if vrt_ds is not None:
        gdaltest.post_reason('fail')
        return 'fail'

    # 2 weights defined, but 3 input spectral bands
    gdal.PushErrorHandler()
    vrt_ds = gdal.Open("""<VRTDataset rasterXSize="800" rasterYSize="400" subClass="VRTPansharpenedDataset">
    <VRTRasterBand dataType="Byte" band="1" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Red</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="2" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Green</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="3" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Blue</ColorInterp>
    </VRTRasterBand>
    <PansharpeningOptions>
        <Algorithm>WeightedBrovey</Algorithm>
        <AlgorithmOptions>
            <Weights>0.33333,0.333333</Weights>
        </AlgorithmOptions>
        <Resampling>Cubic</Resampling>
        <NumThreads>ALL_CPUS</NumThreads>
        <BitDepth>8</BitDepth>
        <PanchroBand>
                <SourceFilename relativeToVRT="1">tmp/small_world_pan.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </PanchroBand>
        <SpectralBand dstBand="1">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="2">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>2</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="3">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>3</SourceBand>
        </SpectralBand>
    </PansharpeningOptions>
</VRTDataset>""")
    gdal.PopErrorHandler()
    if vrt_ds is not None:
        gdaltest.post_reason('fail')
        return 'fail'

    # Just warnings
    # No spectral band is mapped to an output band
    # No output pansharpened band defined
    gdal.PushErrorHandler()
    vrt_ds = gdal.Open("""<VRTDataset rasterXSize="800" rasterYSize="400" subClass="VRTPansharpenedDataset">
    <PansharpeningOptions>
        <Algorithm>WeightedBrovey</Algorithm>
        <AlgorithmOptions>
            <Weights>0.33333,0.333333,0.333333</Weights>
        </AlgorithmOptions>
        <Resampling>Cubic</Resampling>
        <NumThreads>ALL_CPUS</NumThreads>
        <BitDepth>8</BitDepth>
        <PanchroBand>
                <SourceFilename relativeToVRT="1">tmp/small_world_pan.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </PanchroBand>
        <SpectralBand>
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </SpectralBand>
        <SpectralBand>
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>2</SourceBand>
        </SpectralBand>
        <SpectralBand>
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>3</SourceBand>
        </SpectralBand>
    </PansharpeningOptions>
</VRTDataset>""")
    gdal.PopErrorHandler()
    if vrt_ds is None:
        gdaltest.post_reason('fail')
        return 'fail'

    # Unsupported
    gdal.PushErrorHandler()
    ret = vrt_ds.AddBand(gdal.GDT_Byte) 
    gdal.PopErrorHandler()
    if ret == 0:
        gdaltest.post_reason('fail')
        return 'fail'

    return 'success'

###############################################################################
# Nominal cases

def vrtpansharpen_2():

    # Super verbose case
    vrt_ds = gdal.Open("""<VRTDataset rasterXSize="800" rasterYSize="400" subClass="VRTPansharpenedDataset">
    <SRS>GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]]</SRS>
    <GeoTransform> -1.8000000000000000e+02,  4.5000000000000001e-01,  0.0000000000000000e+00,  9.0000000000000000e+01,  0.0000000000000000e+00, -4.5000000000000001e-01</GeoTransform>
    <VRTRasterBand dataType="Byte" band="1" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Red</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="2" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Green</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="3" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Blue</ColorInterp>
    </VRTRasterBand>
    <PansharpeningOptions>
        <Algorithm>WeightedBrovey</Algorithm>
        <AlgorithmOptions>
            <Weights>0.33333333333333333,0.33333333333333333,0.33333333333333333</Weights>
        </AlgorithmOptions>
        <Resampling>Cubic</Resampling>
        <NumThreads>ALL_CPUS</NumThreads>
        <BitDepth>8</BitDepth>
        <PanchroBand>
                <SourceFilename relativeToVRT="1">tmp/small_world_pan.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </PanchroBand>
        <SpectralBand dstBand="1">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="2">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>2</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="3">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>3</SourceBand>
        </SpectralBand>
    </PansharpeningOptions>
</VRTDataset>""")
    if vrt_ds is None:
        gdaltest.post_reason('fail')
        return 'fail'
    if vrt_ds.GetFileList() != [ 'tmp/small_world_pan.tif', 'data/small_world.tif' ]:
        gdaltest.post_reason('fail')
        print(vrt_ds.GetFileList())
        return 'fail'
    cs = [ vrt_ds.GetRasterBand(i+1).Checksum() for i in range(vrt_ds.RasterCount) ]
    if cs != [4735, 10000, 9742]:
        gdaltest.post_reason('fail')
        print(cs)
        return 'fail'

    # Compact case
    vrt_ds = gdal.Open("""<VRTDataset subClass="VRTPansharpenedDataset">
    <PansharpeningOptions>
        <PanchroBand>
                <SourceFilename relativeToVRT="1">tmp/small_world_pan.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </PanchroBand>
        <SpectralBand dstBand="1">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="2">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>2</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="3">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>3</SourceBand>
        </SpectralBand>
    </PansharpeningOptions>
</VRTDataset>""")
    if vrt_ds is None:
        gdaltest.post_reason('fail')
        return 'fail'
    cs = [ vrt_ds.GetRasterBand(i+1).Checksum() for i in range(vrt_ds.RasterCount) ]
    if cs != [4735, 10000, 9742]:
        gdaltest.post_reason('fail')
        print(cs)
        return 'fail'


    # Expose pan band too
    vrt_ds = gdal.Open("""<VRTDataset rasterXSize="800" rasterYSize="400" subClass="VRTPansharpenedDataset">
    <SRS>GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]]</SRS>
    <GeoTransform> -1.8000000000000000e+02,  4.5000000000000001e-01,  0.0000000000000000e+00,  9.0000000000000000e+01,  0.0000000000000000e+00, -4.5000000000000001e-01</GeoTransform>
    <VRTRasterBand dataType="Byte" band="1">
        <SimpleSource>
            <SourceFilename relativeToVRT="1">tmp/small_world_pan.tif</SourceFilename>
            <SourceBand>1</SourceBand>
        </SimpleSource>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="2" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Red</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="3" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Green</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="4" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Blue</ColorInterp>
    </VRTRasterBand>
    <PansharpeningOptions>
        <Algorithm>WeightedBrovey</Algorithm>
        <AlgorithmOptions>
            <Weights>0.33333333333333333,0.33333333333333333,0.33333333333333333</Weights>
        </AlgorithmOptions>
        <Resampling>Cubic</Resampling>
        <NumThreads>ALL_CPUS</NumThreads>
        <BitDepth>8</BitDepth>
        <PanchroBand>
                <SourceFilename relativeToVRT="1">tmp/small_world_pan.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </PanchroBand>
        <SpectralBand dstBand="2">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="3">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>2</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="4">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>3</SourceBand>
        </SpectralBand>
    </PansharpeningOptions>
</VRTDataset>""")
    if vrt_ds is None:
        gdaltest.post_reason('fail')
        return 'fail'
    gdal.GetDriverByName('GTiff').CreateCopy('out1.tif', vrt_ds)
    cs = [ vrt_ds.GetRasterBand(i+1).Checksum() for i in range(vrt_ds.RasterCount) ]
    if cs != [50261, 4735, 10000, 9742]:
        gdaltest.post_reason('fail')
        print(cs)
        return 'fail'


    # Same, but everything scambled
    vrt_ds = gdal.Open("""<VRTDataset rasterXSize="800" rasterYSize="400" subClass="VRTPansharpenedDataset">
    <SRS>GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]]</SRS>
    <GeoTransform> -1.8000000000000000e+02,  4.5000000000000001e-01,  0.0000000000000000e+00,  9.0000000000000000e+01,  0.0000000000000000e+00, -4.5000000000000001e-01</GeoTransform>
    <VRTRasterBand dataType="Byte" band="1">
        <SimpleSource>
            <SourceFilename relativeToVRT="1">tmp/small_world_pan.tif</SourceFilename>
            <SourceBand>1</SourceBand>
        </SimpleSource>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="2" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Red</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="3" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Green</ColorInterp>
    </VRTRasterBand>
    <VRTRasterBand dataType="Byte" band="4" subClass="VRTPansharpenedRasterBand">
        <ColorInterp>Blue</ColorInterp>
    </VRTRasterBand>
    <PansharpeningOptions>
        <Algorithm>WeightedBrovey</Algorithm>
        <AlgorithmOptions>
            <Weights>0.33333333333333333,0.33333333333333333,0.33333333333333333</Weights>
        </AlgorithmOptions>
        <Resampling>Cubic</Resampling>
        <NumThreads>ALL_CPUS</NumThreads>
        <BitDepth>8</BitDepth>
        <PanchroBand>
                <SourceFilename relativeToVRT="1">tmp/small_world_pan.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </PanchroBand>
        <SpectralBand dstBand="3">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>2</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="2">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>1</SourceBand>
        </SpectralBand>
        <SpectralBand dstBand="4">
                <SourceFilename relativeToVRT="1">data/small_world.tif</SourceFilename>
                <SourceBand>3</SourceBand>
        </SpectralBand>
    </PansharpeningOptions>
</VRTDataset>""")
    if vrt_ds is None:
        gdaltest.post_reason('fail')
        return 'fail'
    gdal.GetDriverByName('GTiff').CreateCopy('out2.tif', vrt_ds)
    cs = [ vrt_ds.GetRasterBand(i+1).Checksum() for i in range(vrt_ds.RasterCount) ]
    if cs != [50261, 4735, 10000, 9742]:
        gdaltest.post_reason('fail')
        print(cs)
        return 'fail'

    return 'success'

###############################################################################
# Cleanup

def vrtpansharpen_cleanup():
    
    gdal.GetDriverByName('GTiff').Delete('tmp/small_world_pan.tif')

    return 'success'


gdaltest_list = [
    vrtpansharpen_1,
    vrtpansharpen_2,
    vrtpansharpen_cleanup,
]


if __name__ == '__main__':

    gdaltest.setup_run( 'vrtpansharpen' )

    gdaltest.run_tests( gdaltest_list )

    gdaltest.summarize()
