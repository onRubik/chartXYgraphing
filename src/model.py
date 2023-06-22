# from controller import Controller
import platform
import os
from pathlib import Path
import numpy as np
import random
import operator
import pandas as pd
import matplotlib.pyplot as plt
import math
from itertools import permutations
import csv
from tqdm import trange
import sqlite3


class Model:
    def __init__(self, file_name: str, points_name: str, distance_name: str, n: int, multiplier: int, db_name):
        self.file_name = file_name
        self.points_name = points_name
        self.distance_name = distance_name
        self.n = n
        self.multiplier = multiplier
        self.img_path = None
        self.os_type = None
        self.db_name = db_name
        self.con = None


    def imgFolder(self):
        os_type = platform.system()
        if os_type == 'Windows':
            img_path = os.path.dirname(__file__)
        elif os_type == 'Linux':
            img_path = os.path.dirname(os.path.abspath(__file__))

        img_path = Path(img_path)
        img_path = img_path.parent
        self.img_path = img_path
        self.os_type = os_type
    
    
    def createRandomPoints(self):
        if self.os_type == 'Windows':
            comb_input_fix = str(self.img_path) + '\\input\\' + 'ran_' + self.file_name + '.csv'
        if self.os_type == 'Linux':
            comb_input_fix = str(self.img_path) + '/input/' + 'ran_' + self.file_name + '.csv'

        arr = []
        for i in range(0,self.n):
            arr.append([int(random.random() * self.multiplier), int(random.random() * self.multiplier)])

        df = pd.DataFrame(arr, columns=['x','y'])

        return [df, comb_input_fix]

    
    def createRandomPointsWithDistance(self):
        if self.os_type == 'Windows':
            perm_input_fix = str(self.img_path) + '\\input\\' + 'ran_dis_' + self.file_name + '.csv'
            points_input_fix = str(self.img_path) + '\\input\\' + 'ran_points_' + self.file_name + '.csv'
        if self.os_type == 'Linux':
            perm_input_fix = str(self.img_path) + '/input/' + 'ran_dis_' + self.file_name + '.csv'
            points_input_fix = str(self.img_path) + '/input/' + 'ran_points_' + self.file_name + '.csv'
        
        arr = []
        dist_list = []

        for i in range(0,self.n):
            arr.append([round(random.random() * self.multiplier, 6), round(random.random() * self.multiplier, 6)])
        
        df_points = pd.DataFrame(arr, columns=['x','y'])
        perm = list(permutations(arr, 2))
        for index, item in enumerate(perm):
            distance = float(math.sqrt((item[1][0] - item[0][0])**2 + ((item[1][1] - item[0][1])**2)))
            dist_list.append([item[1][0], item[0][0], item[1][1], item[0][1], distance])
        
        df_perm = pd.DataFrame(dist_list, columns=['x2', 'x1', 'y2', 'y1','distance'])

        return [[df_points, points_input_fix], [df_perm, perm_input_fix]]


    def addDistanceToPoints(self):
        pass


    def saveToCsv(self, items):
        for item in items:
            item[0].to_csv(item[1], index=False)


    def dfInput(self):
        if self.os_type == 'Windows':
            perm_input_fix = str(self.img_path) + '\\input\\' + self.distance_name + '.csv'
            points_input_fix = str(self.img_path) + '\\input\\' + self.points_name + '.csv'
            route_output_fix = str(self.img_path) + '\\output\\' + 'route_' + self.file_name + '.png'
            progress_output_fix = str(self.img_path) + '\\output\\' + 'progress_' + self.file_name + '.png'
            csv_output_fix = str(self.img_path) + '\\output\\' + 'route_' + self.file_name + '.csv'
        if self.os_type == 'Linux':
            perm_input_fix = str(self.img_path) + '/input/' + self.distance_name + '.csv'
            points_input_fix = str(self.img_path) + '/input/' + self.points_name + '.csv'
            route_output_fix = str(self.img_path) + '/output/' + 'route_' + self.file_name + '.png'
            progress_output_fix = str(self.img_path) + '/output/' + 'progress_' + self.file_name + '.png'
            csv_output_fix = str(self.img_path) + '/output/' + 'route_' + self.file_name + '.csv'
        
        with open(points_input_fix, 'r') as f:
            reader = csv.reader(f)
            points = list(reader)

        points = [[round(float(j), 6) for j in i] for i in points[1:]]
        combination_distance = pd.read_csv(perm_input_fix)

        return points, combination_distance, route_output_fix, progress_output_fix, csv_output_fix
    

    def initDb(self):
        if self.os_type == 'Windows':
            db_path_fix = str(self.img_path) + '\\' + self.db_name
        if self.os_type == 'Linux':
            db_path_fix = str(self.img_path) + '/' + self.db_name

        con = sqlite3.connect(db_path_fix)
        self.con = con
        
        return con
    

    def closeDb(self):
        self.con.close()