#!/usr/bin/env python3

#Import various libraries for use in the script.
import cgi
from jinja2 import Environment, FileSystemLoader
import cx_Oracle

#Open and read the Oracle login password file. The login details are stored in a separate password file to ensure the
#Oracle database login details are not open visible to the public.
with open("../../oracle", 'r') as pwf:
    pw=pwf.read().strip()

#A function to open a connection to the Oracle database and provide access to the relevant tables. The open connection is
#returned for use by other functions. The connection is closed once the script has been successfully run.
def db_connect():
    conn=cx_Oracle.connect(dsn="geosgen", user="student", password=pw)
    db_con=conn.cursor()
    return db_con

#A function to define the bounds of the survey overall area based on the minimum and maximum coordinates (LX, LY, UX, UY) from the "FIELDS"
#table in the database. Four values are returned representing the lower-left X,Y and upper-right X,Y coordinates of the survey area.
def survey_area(db_con):
    survey_area_lx=[]
    survey_area_ly=[]
    survey_area_ux=[]
    survey_area_uy=[]
    db_con.execute("SELECT * FROM GISTEACH.FIELDS")
    for row in db_con:
        survey_area_lx.append(row[1]-1.0)
        survey_area_ly.append(row[2]-0.5)
        survey_area_ux.append(row[3]+1.5)
        survey_area_uy.append(row[4]+1.6)
    sa_minx = min(survey_area_lx)
    sa_miny = min(survey_area_ly)
    sa_maxx = max(survey_area_ux)
    sa_maxy = max(survey_area_uy)
    return sa_minx, sa_miny, sa_maxx, sa_maxy

#A function to create a coordinate grid and labels for the survey area based on the minimum and maximum coordinates (LX, LY, UX, UY) from
#the "FIELDS" table in the database. Once the maximum "X" and "Y" values are determined, the values are then used to build up the grid using
#SVG lines. A label is added to the edge of each line to indicate it coordinate value. Two lists are returned from the function; the first
#containing the vertical lines (X) and labels of the grid and the second containing the horizontal lines (Y) and labels of the grid.
def grid_lines (db_con):
    up_x=[]
    up_y=[]
    db_con.execute("SELECT * FROM GISTEACH.FIELDS")
    for row in db_con:
        up_x.append(row[3])
        up_y.append(row[4])
    grid_x=max(up_x)
    grid_y=max(up_y)
    i=0
    itextpos=-0
    grid_vert=''
    j=0
    jtextpos=0.10
    jtext=grid_y
    grid_hori=''
    #A while loop to create the vertical grid lines.
    while i <= grid_x:
        grid_vert = grid_vert + '<line class="grid" x1="'+ str(i) + '" y1="0" x2="' + str(i) + '" y2="' + str(grid_y) + '"></line><text class="grid" x="' + str(itextpos) + '" y="16.40" font-size="0.35" opacity="0.7" text-anchor="middle" >'+ str(i) +'</text>'
        i=i+1
        itextpos=itextpos+1
    #A while loop to create the horizontal grid lines.
    while j <= grid_y:
        grid_hori = grid_hori + '<line class="grid" x1="0" y1="' + str(j) + '" x2="' + str(grid_x) + '" y2="' + str(j) + '"></line><text class="grid" x="-0.28" y="' + str(jtextpos) + '" font-size="0.35" opacity="0.7" text-anchor="middle" fill="grey" >'+ str(jtext) +'</text>'
        j=j+1
        jtextpos=jtextpos+1
        jtext=jtext-1
    return grid_vert, grid_hori

#A function which uses SQL to query the "FINDS" and CLASS" tables in the database in order to build up a list containing an SVG circle for
#each archaeological find in the "FINDS" table including information necessary to display a circle for each find and text information about
#each find. The function also builds up and formats a list containing labels for each find. Two lists are returned from the function; the first containing
#information necessary to display and describe an SVG for each find, and the second containing information to label each find.
def finds(db_con):
    db_con.execute("SELECT FINDS.FIND_ID, FINDS.XCOORD, FINDS.YCOORD, FINDS.TYPE, FINDS.DEPTH, FINDS.FIELD_NOTES, CLASS.TYPE, CLASS.NAME, CLASS.PERIOD, CLASS.USE FROM GISTEACH.FINDS, GISTEACH.CLASS WHERE FINDS.TYPE=CLASS.TYPE")
    finds_svg=''
    finds_label=''
    for row in db_con:
        finds_svg = finds_svg + '<circle class="find" id="myfind" cx="' + str(row[1]) + '" cy="' + str(row[2]) + '" r="0.3"><title id="tooltip">Find Name: '+str(row[7]).capitalize() + ' <br>Find Notes: '+ str(row[5]).capitalize() + ' <br>Find Depth: '+ str(row[4]) + ' metres <br>Find Period: '+ str(row[8]).capitalize() + ' <br>Find Use: '+ row[9].capitalize() + ' <br>Find Coordinates (x,y): '+ str(row[1]) + ',' + str(row[2]) + '</title></circle>'

        finds_label = finds_label + '<text class="find label_find" id="myfind" x="' + str(row[1]-0.13) + '" y="' + str((16-row[2])+0.15) + '" font-family="Verdana" font-size="0.4">'+ str(row[0]) + '</text>'
    return finds_svg, finds_label

#A function which uses SQL to query the "FIELDS" and "CROPS" tables in the database in order to build up a list containing an SVG rectangle for
#each farmers' field in the "FIELDS" table including information necessary to display a rectangle for each field and text information about each field.
#The function uses a series of if/elif statements to determine what type of crop is being grown in each field, allowing the fields to be symbolized
#accordingly. The function also builds up and formats a list containing labels for each field. Two lists are returned from the function; the first containing
#information necessary to display and describe an SVG for each field, and the second containing information to label each find.
def fields(db_con):
    db_con.execute("SELECT FIELDS.FIELD_ID, FIELDS.LOWX, FIELDS.LOWY, FIELDS.HIX, FIELDS.HIY, FIELDS.AREA, FIELDS.OWNER, FIELDS.CROP, CROPS.CROP, CROPS.NAME, CROPS.START_OF_SEASON, CROPS.END_OF_SEASON FROM GISTEACH.FIELDS, GISTEACH.CROPS WHERE FIELDS.CROP=CROPS.CROP")
    field_svg=''
    field_label=''
    for row in db_con:
        if row[8] == 1:
            field_svg = field_svg + '<rect class="field" x="' + str(row[1]) + '" y="' + str(row[2]) + '" width="' + str(row[3]-row[1]) + '" height="' + str(row[4]-row[2]) + '" fill="#dda0dd"><title>Owner: '+row[6].title() +' <br>Crop: '+str(row[9]).capitalize() + ' <br>Growing Season: {:%d-%m-%y}'.format(row[10]) + ' to {:%d-%m-%y}'.format(row[11])+ ' <br>Field Size: '+"{:.2f}".format(row[5])+' hectares</title></rect>'
        elif row[8] == 2:
            field_svg = field_svg + '<rect class="field" x="' + str(row[1]) + '" y="' + str(row[2]) + '" width="' + str(row[3]-row[1]) + '" height="' + str(row[4]-row[2]) + '" fill="#ffff96"><title>Owner: '+row[6].title() +' <br>Crop: '+str(row[9]).title() + ' <br>Growing Season: {:%d-%m-%y}'.format(row[10]) + ' to {:%d-%m-%y}'.format(row[11])+ ' <br>Field Size: '+"{:.2f}".format(row[5])+' hectares</title></rect>'
        elif row[8] == 3:
            field_svg = field_svg + '<rect class="field" x="' + str(row[1]) + '" y="' + str(row[2]) + '" width="' + str(row[3]-row[1]) + '" height="' + str(row[4]-row[2]) + '" fill="#ec7063"><title>Owner: '+row[6].title() +' <br>Crop: '+str(row[9]).title() + ' <br>Growing Season: {:%d-%m-%y}'.format(row[10]) + ' to {:%d-%m-%y}'.format(row[11])+ ' <br>Field Size: '+"{:.2f}".format(row[5])+' hectares</title></rect>'
        elif row[8] == 4:
            field_svg = field_svg + '<rect class="field" x="' + str(row[1]) + '" y="' + str(row[2]) + '" width="' + str(row[3]-row[1]) + '" height="' + str(row[4]-row[2]) + '" fill="#7dcea0"><title>Owner: '+row[6].title() +' <br>Crop: '+str(row[9]).title() + ' <br>Growing Season: {:%d-%m-%y}'.format(row[10]) + ' to {:%d-%m-%y}'.format(row[11])+ ' <br>Field Size: '+"{:.2f}".format(row[5])+' hectares</title></rect>'
        elif row[8] == 5:
            field_svg = field_svg + '<rect class="field" x="' + str(row[1]) + '" y="' + str(row[2]) + '" width="' + str(row[3]-row[1]) + '" height="' + str(row[4]-row[2]) + '" fill="#cca883"><title>Owner: '+row[6].title() +' <br>Crop: '+str(row[9]).title() + ' <br>Growing Season: {:%d-%m-%y}'.format(row[10]) + ' to {:%d-%m-%y}'.format(row[11])+ ' <br>Field Size: '+"{:.2f}".format(row[5])+' hectares</title></rect>'
        else:
            field_svg = field_svg + '<rect class="field" x="' + str(row[1]) + '" y="' + str(row[2]) + '" width="' + str(row[3]-row[1]) + '" height="' + str(row[4]-row[2]) + '" fill="gray"><title>Owner: '+row[6].title() +' <br>Crop: '+str(row[9]).title() + ' <br>Growing Season: {:%d-%m-%y}'.format(row[10]) + ' to {:%d-%m-%y}'.format(row[11])+ ' <br>Field Size: '+"{:.2f}".format(row[5])+' hectares</title></rect>'

        field_label = field_label + '<text class="field label_field" x="' + str((row[1]+row[3])/2-0.3) + '" y="' + str(16-((row[2]+row[4])/2)+0.2) + '" font-family="Verdana" font-size="01" fill="black">' + str(row[0]) +' </text>'
    return field_svg, field_label

#A function which uses SQL to query the tables in the database in order to build up and format a list of relevant information for each "FIND"
#and "FIELD" record in the tables. The two lists are returned which are used to display seperate tables for each of the "FINDS" and "FIELDS".
def find_field_tables(db_con):
    db_con.execute("SELECT * FROM GISTEACH.FINDS, GISTEACH.CLASS WHERE FINDS.TYPE=CLASS.TYPE")
    find_table=''
    for row in db_con:
        find_table = find_table + '<tr class="table_body"><td>' + str(row[0]) + '</td><td>' + str(row[7]).capitalize() + '</td><td>' + str(row[8]).capitalize() + '</td><td>' + str(row[9]).capitalize() + '</td><td>' + str(row[1]) + '</td><td>' + str(row[2]) + '</td><td>' + str(row[4]) + '</td><td>' + str(row[5]).capitalize() + '</td></tr>'
    db_con.execute("SELECT * FROM GISTEACH.FIELDS, GISTEACH.CROPS WHERE FIELDS.CROP=CROPS.CROP")
    field_table=''
    for row in db_con:
        field_table = field_table + '<tr class="table_body"><td>' + str(row[0]) + '</td><td>' + str(row[6]).title() + '</td><td>' +"{:.2f}".format(row[5]) + '</td><td>' + str(row[9]).title()+ '</td><td>' + str(row[1]) +', ' + str(row[2]) + ', ' + str(row[3]) + ', ' + str(row[4]) + '</td><td>' + '{:%d - %m - %y}'.format(row[10]) + '</td><td>' + '{:%d - %m - %y}'.format(row[11]) + '</td></tr>'
    return find_table, field_table

#A function to call the various functions in the script and, using Jinga, pass information to the HTML for display.
def print_html():
    db_con = db_connect()
    env = Environment(loader=FileSystemLoader('.'))
    temp = env.get_template('fields_finds.html')
    find_circ, find_label = finds(db_con)
    field_rect, field_label = fields(db_con)
    sa_minx, sa_miny, sa_maxx, sa_maxy = survey_area(db_con)
    grid_vert, grid_hori = grid_lines(db_con)
    find_table, field_table=find_field_tables(db_con)
    db_con.close()
    #Passing variables returned from functions to the HTML side using Jinga
    print(temp.render(inp_minx=sa_minx, inp_miny=sa_miny, inp_maxx=sa_maxx, inp_maxy=sa_maxy, inp_gridv=grid_vert, inp_gridh=grid_hori, inp_field_rect=field_rect, inp_find_circ=find_circ, inp_field_label=field_label, inp_find_label=find_label, inp_find_table=find_table, inp_field_table=field_table))

if __name__=='__main__':
    print_html()
