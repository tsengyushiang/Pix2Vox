#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
# Developed by Haozhe Xie <cshzxie@gmail.com>

import logging
import matplotlib
import multiprocessing as mp
import numpy as np
import os
import sys
# Fix problem: no $DISPLAY environment variable
matplotlib.use('Agg')

from argparse import ArgumentParser
from pprint import pprint

from config import cfg
from core.train import train_net
from core.test import test_net

def get_args_from_command_line():
    parser = ArgumentParser(description='Parser of Runner of Weighted-Voxel')
    parser.add_argument(
        '--gpu',
        dest='gpu_id',
        help='GPU device id to use [cuda0]',
        default=cfg.CONST.DEVICE,
        type=str)
    parser.add_argument(
        '--rand', dest='randomize', help='Randomize (do not use a fixed seed)', action='store_true')
    parser.add_argument(
        '--test', dest='test', help='Test neural networks', action='store_true')
    parser.add_argument(
        '--batch-size',
        dest='batch_size',
        help='name of the net',
        default=cfg.CONST.BATCH_SIZE,
        type=int)
    parser.add_argument(
        '--epoch',
        dest='epoch',
        help='number of epoches',
        default=cfg.TRAIN.NUM_EPOCHES,
        type=int)
    parser.add_argument(
        '--weights', dest='weights', help='Initialize network from the weights file', default=None)
    parser.add_argument('--out', dest='out_path', help='Set output path', default=cfg.DIR.OUT_PATH)
    args = parser.parse_args()
    return args

def main():
    # Get args from command line
    args = get_args_from_command_line()

    if args.gpu_id is not None:
        cfg.CONST.DEVICE = args.gpu_id
    if not args.randomize:
        np.random.seed(cfg.CONST.RNG_SEED)
    if args.batch_size is not None:
        cfg.CONST.BATCH_SIZE = args.batch_size
    if args.epoch is not None:
        cfg.TRAIN.NUM_EPOCHES = args.epoch
    if args.out_path is not None:
        cfg.DIR.OUT_PATH = args.out_path
    if args.weights is not None:
        cfg.CONST.WEIGHTS = args.weights
        cfg.TRAIN.RESUME_TRAIN = True

    # Print config
    print('Use config:')
    pprint(cfg)

    # Set GPU to use
    os.environ["CUDA_VISIBLE_DEVICES"] = cfg.CONST.DEVICE

    # Start train/test process
    if not args.test:
        train_net(cfg)
    else:
        test_net(cfg)

if __name__ == '__main__':
    # Check python version
    if sys.version_info < (3, 0):
        raise Exception("Please follow the installation instruction on 'https://github.com/hzxie/Pixel2Voxel'")

    # Setup logger
    mp.log_to_stderr()
    logger = mp.get_logger()
    logger.setLevel(logging.INFO)

    main()
