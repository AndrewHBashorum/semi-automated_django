# Author: ANDREW BASHORUM: C00238900
# 4th YEAR PROJECT
"""!@file database_interaction.py
@brief Contains Database Object.
Used to handle any interaction with NPS database

@author Andrew Bashorum
"""
from pathlib import Path

if 'lukecoburn' not in str(Path.home()):
    user = 'andrew'
else:
    user = 'luke'

import psycopg2
import warnings
import numpy as np
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

class Database(object):
    """!@brief Database Class

    This Database object is used to process interaction from NPS Dataset

    @author Andrew Bashorum
    """
    def __init__(self):
        """!@brief Database constructor

        Establishes connection to postgres database and table

        @author Andrew Bashorum
        """
        if user == 'andrew':
            self.con = psycopg2.connect(database="sdb_course", user="postgres", password="$£x25zeD", host="localhost", port="5432")
        else:
            self.con = psycopg2.connect(database="nps_database_cropped", user="postgres", password="$£x25zeD", host="localhost", port="5433")
        self.cur = self.con.cursor()

    def ST_Contains(self, x, y):
        """!@brief Returns sites which contain x,y point

        @return MULTIPOLYGON list containing site geometry

        @param x: X point query NPS dataset
        @param y: Y point query NPS dataset
        """
        do = """SELECT ST_AsText(geom) FROM public."nps_cropped_lynmouth" WHERE ST_Contains(ST_AsText(geom), ST_GeomFromText('POINT(""" + str(
            x) + " " + str(y) + ")'))"
        self.cur.execute(do)
        return self.cur.fetchall()

    def single_spatial_to_string(self, geom):

        """!@brief Converts MULTIPOLYGON string list to clean string with just x,y points

        @return simple string containing x,y points

        @param geom: MULTIPOLYGON string to clean
        """

        geom = geom.replace('MULTIPOLYGON','')
        geom = geom.replace('(', '')
        geom = geom.replace(')', '')
        geom = geom.replace(',', '')
        geom = geom.replace('"', '')
        geom = geom.replace('', '')

        return geom

    def single_spatial_to_list(self, g):

        """!@brief Converts MULTIPOLYGON string list to clean list with both x,y points

        @return list containing x,y points

        @param geom: MULTIPOLYGON string to clean
        """

        g = g.replace("MULTIPOLYGON", "")
        g = g.replace("(", "")
        g = g.replace(")", "")
        g = g.replace(",", " ")
        g = g.replace('"', " ")
        g = g.replace("'", " ")
        g = g.split()

        return g

    def list_to_single_spatial(self, theList):
        """!@brief Converts  list to clean to MULTIPOLYGON string

         @return MULTIPOLYGON string

         @param theList: Clean x,y list to convert
        """
        multi_string_start = 'MULTIPOLYGON((('
        multi_string_end = ')))'
        multi_string = ''
        for i in range(0, len(theList), 2):
            if i == len(theList) - 2:
                multi_string = multi_string + str(theList[i]) + ' ' + str(theList[i + 1])
            else:
                multi_string = multi_string + str(theList[i]) + ' ' + str(theList[i + 1]) + ','
        final_multi = multi_string_start + multi_string + multi_string_end

        return final_multi

    def x_y_list_to_single_spatial(self, x, y):
        """!@brief Converts separate x and y list to clean to MULTIPOLYGON string

         x,y lists converted to 4326 global coordinates
         @return MULTIPOLYGON string

         @param x: Clean x list to convert
         @param y: Clean y list to convert
        """
        multi_string_start = 'MULTIPOLYGON((('
        multi_string_end = ')))'
        multi_string = ''
        for i in range(0, len(x)):
            if i == len(y) - 1:
                multi_string = multi_string + str(x[i]) + ' ' + str(y[i])
            else:
                multi_string = multi_string + str(x[i]) + ' ' + str(y[i]) + ','
        final_multi = multi_string_start + multi_string + multi_string_end
        f = self.ST_Transform_4326(final_multi)

        return f

    def x_y_list_to_single_spatial_27700(self, x, y):
        """!@brief Converts separate x and y list to clean to MULTIPOLYGON string

          Keeps british (27700) format
          @return MULTIPOLYGON string

          @param x: Clean x list to convert
          @param y: Clean y list to convert
        """
        multi_string_start = 'MULTIPOLYGON((('
        multi_string_end = ')))'
        multi_string = ''
        for i in range(0, len(x)):
            if i == len(y) - 1:
                multi_string = multi_string + str(x[i]) + ' ' + str(y[i])
            else:
                multi_string = multi_string + str(x[i]) + ' ' + str(y[i]) + ','
        final_multi = multi_string_start + multi_string + multi_string_end

        return final_multi

    def single_spatial_to_x_y_list(self, geom):
        """!@brief Converts MULTIPOLYGON string list to clean list with sperate x,y lists of points

        Transforms points into 4326 global coordinates first

        @return list containing x points
        @return list containing y points
        @param geom: MULTIPOLYGON string to clean
        """
        g = self.ST_Transform(geom)
        g = g.replace("MULTIPOLYGON", "")
        g = g.replace("(", "")
        g = g.replace(")", "")
        g = g.replace(",", " ")
        g = g.replace('"', " ")
        g = g.replace("'", " ")
        g = g.split()

        x_list = []
        y_list = []
        for i in range(0, len(g), 2):
            x_list.append(float(g[i]))
            y_list.append(float(g[i+1]))
        return x_list, y_list

    def single_spatial_to_x_y_list_keep_spatial(self, geom):
        """!@brief Converts MULTIPOLYGON string list to clean list with sperate x,y lists of points

        @return list containing x points
        @return list containing y points
        @param geom: MULTIPOLYGON string to clean
        """
        g = geom
        g = g.replace("MULTIPOLYGON", "")
        g = g.replace("(", "")
        g = g.replace(")", "")
        g = g.replace(",", " ")
        g = g.replace('"', " ")
        g = g.replace("'", " ")
        g = g.split()

        x_list = []
        y_list = []
        for i in range(0, len(g), 2):
            x_list.append(float(g[i]))
            y_list.append(float(g[i+1]))
        return x_list, y_list

    def ST_DWithin(self, x, y, d):
        """!@brief Returns sites which are distance d away from x,y point

        @return MULTIPOLYGON list containing site geometry

        @param x: X point query NPS dataset
        @param y: Y point query NPS dataset
        @param d: Distance / tolerance from x,y point accepted
        """
        do = """SELECT ST_AsText(geom) FROM public."nps_cropped_lynmouth" WHERE _ST_DWithin(ST_AsText(geom), ST_GeomFromText('POINT(""" + str(
            x) + " " + str(y) + ")')," + str(d) + ")"
        self.cur.execute(do)
        neigh_geometry = self.cur.fetchall()
        return neigh_geometry

    def ST_Transform(self, geom):
        """!@brief Transforms geometry from 4326 (global) into 27700(british)


        @return MULTIPOLYGON string
        @param geom: MULTIPOLYGON List to convert
        """
        do = """SELECT ST_AsText(ST_Transform(ST_GeomFromText(""" + "'" + geom + "',4326), 27700)) As wgs_geom"
        self.cur.execute(do)
        list = self.cur.fetchall()
        geo = list[0][0]
        return geo

    def ST_Transform_4326(self, geom):
        """!@brief Transforms geometry from 27700(british) into 4326 (global)


        @return MULTIPOLYGON string
        @param geom: MULTIPOLYGON string to convert
        """
        do = """SELECT ST_AsText(ST_Transform(ST_GeomFromText(""" + "'" + geom + "',27700), 4326)) As wgs_geom"
        self.cur.execute(do)
        geo = self.cur.fetchall()[0][0]
        return geo

    def ST_Area(self, geom):
        """!@brief Finds area of given MULTIPOLYGON geometry


        @return MULTIPOLYGON string
        @param geom: MULTIPOLYGON string to convert
        """
        do = """SELECT ST_Area(ST_GeomFromText(""" + "'" + geom + "'))"
        self.cur.execute(do)
        geo = self.cur.fetchall()
        return geo

    def ST_Convex(self, geom):
        """!@brief Finds convex hull of given MULTIPOLYGON geometry


        @return MULTIPOLYGON string
        @param geom: MULTIPOLYGON string to convert
        """
        do = """SELECT ST_AsText(ST_ConvexHull(ST_GeomFromText(""" + "'" + geom + "'))) As wgs_geom "
        self.cur.execute(do)
        geo = self.cur.fetchall()
        return geo

    def ST_Concave(self, geom, target_percentage = None):
        """!@brief Finds concave hull of given MULTIPOLYGON geometry


        @return MULTIPOLYGON string
        @param geom: MULTIPOLYGON string to convert
        @param target_percentage: Percentage of area of the convex hull the solution tries to approach
        """
        if target_percentage == None:
            target_percentage = "0.8"
        do = """SELECT ST_AsText(ST_ConcaveHull(ST_GeomFromText(""" + "'" + geom + "'), """ + target_percentage + """)) As wgs_geom """""
        self.cur.execute(do)
        geo = self.cur.fetchall()
        return geo

    def ST_ShortestLine(self, geom, geom2=None):
        """!@brief Finds shortest line between two given MULTIPOLYGON geometrys


        @return MULTIPOLYGON string
        @param geom: MULTIPOLYGON string to convert
        """
        do = """SELECT ST_AsText(ST_ShortestLine(ST_GeomFromText(""" + "'" + geom + "'), """+"ST_GeomFromText(" + "'" + geom2 + "')))"""
        self.cur.execute(do)
        geo = self.cur.fetchall()[0][0]
        return geo

    def linestring_to_length(self, geo):
        """!@brief Finds length on inputted linestring geometry

        @return length of line
        @param geom: linestring string to calculate
        """
        g = self.ST_Transform(geo)
        g = g.replace("LINESTRING", "")
        g = g.replace("(", "")
        g = g.replace(")", "")
        g = g.replace(",", " ")
        g = g.replace('"', " ")
        g = g.replace("'", " ")
        g = g.split()
        x_list = []
        y_list = []
        for i in range(0, len(g), 2):
            x_list.append(float(g[i]))
            y_list.append(float(g[i + 1]))
        return np.sqrt((x_list[0] - x_list[1])**2 + (y_list[0] - y_list[1])**2)


    def close_connection(self):
        """!@brief Closes connection to db

        """
        self.con.close()