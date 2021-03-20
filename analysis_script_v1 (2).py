import numpy as np

def read_from_file(p_num): #this reads a single fine
    path = "Data/Data" + str(p_num) + ".txt"
    f = open(path, "r")
    f.readline() #firstline is always file start
    #deals with header 
    global num_runs  #num runs for each file type

    global max_run_num
    
    num_runs = []
    num_runs.append(int(f.readline()))
    num_runs.append(int(f.readline()))
    num_runs.append(int(f.readline()))
    num_runs.append(int(f.readline()))

    for i in range(4):
        if(num_runs[i] > max_run_num[i]):
            max_run_num[i] = num_runs[i]

        
    

    run_num = 0 #indicates what run we are on

    #global variables that we use to store our data
    global file_run_tuples
    file_run_tuples = []
    global file_hit_tuples
    file_hit_tuples = []
    global file_death_tuples
    file_death_tuples = []



    run_num = [] #run num holds the number of runs for each setting type
    run_num.append(0)
    run_num.append(0)
    run_num.append(0)
    run_num.append(0)

    for line in f:
        if line == "RunStart\n": #deal with start of a run
            #now we work out our sound settings
            if f.readline() == "True\n":
                sound = True
            else:
                sound = False
            if f.readline() == "True\n":
                access_feat = True
            else:
                access_feat = False

            if(sound):
                if(access_feat):
                    setting = 0
                else:
                    setting = 1
            else:
                if(access_feat):
                    setting = 2
                else:
                    setting = 3
            run_num[setting] = run_num[setting] + 1 #add 1 to relelvant run num
            #work out our difficulty settings 
            if(f.readline() == "m\n"):
               diff = 0
            else:
                diff = 1
            #simple to work out values 
            total_time = float(f.readline())
            deaths = int(f.readline())
            hits = int(f.readline())
            shield_usage = float(f.readline())
            stam_usage = float(f.readline())

            #now room times
            room_times = []
            f.readline() #first room time is useless as it is the little start room
            f.readline()
            f.readline() #R
            room_times.append(float(f.readline()))
            f.readline() #R
            room_times.append(float(f.readline()))
            f.readline() #R
            room_times.append(float(f.readline()))
            f.readline() #R
            room_times.append(float(f.readline()))
            f.readline() #R
            room_times.append(float(f.readline()))

            temp_run_tuple = (p_num, run_num[setting], setting, diff, total_time, shield_usage, stam_usage, hits, deaths, room_times[0], room_times[1], room_times[2], room_times[3], room_times[4])
            file_run_tuples.append(temp_run_tuple)
        #end of the "header" section now we move onto hits and deaths
        if line == "H\n": #working with hits
            time = float(f.readline())
            if(time == 0):
                timed = False
            else:
                timed = True

            room_num = int(f.readline())
            temp_tuple = (p_num,run_num[setting],setting,room_num,timed,time)
            file_hit_tuples.append(temp_tuple)
        if line == "D\n":
            room_num = int(f.readline())
            temp_tuple = (p_num, run_num[setting], setting, room_num)
            file_death_tuples.append(temp_tuple)
            

            
            

            

            

def read_all_files(num_of_parts): #reads all the data from all the files
    #num_of_parts = 5 #will go from 0 to (num-1)
    global run_tuples
    run_tuples = []
    global hit_tuples
    hit_tuples = []
    global death_tuples
    death_tuples = []
    global total_num_runs #gives total number of runs for each setting
    total_num_runs = [0,0,0,0]
    
    for x in range(num_of_parts):
        read_from_file(x)
        run_tuples.extend(file_run_tuples)
        hit_tuples.extend(file_hit_tuples)
        death_tuples.extend(file_death_tuples)
        total_num_runs = np.add(total_num_runs, num_runs)
        



def run_tuple_analysis(): #runs analysis on the run_tuple list
    #global variables
    global total_setting_time #stores total time for each setting
    global total_setting_time_num
    total_setting_time = [0.0,0.0,0.0,0.0]
    total_setting_time_num = [0,0,0,0]

    global total_room_time #stores total time for each room
    global total_room_time_num
    total_room_time = [0.0,0.0,0.0,0.0,0.0]
    total_room_time_num = [0,0,0,0,0]


    global total_run_num_time
    global total_run_num_time_num
    total_run_num_time = [0.0 for i in range(4)]
    total_run_num_time_num = [0.0 for i in range(4)]

    global total_room_setting_time #stores total time for each room for each setting
    global total_room_setting_time_num
    total_room_setting_time = [[0.0 for i in range(4)] for j in range(5)] #max is [4][3], access: [room][setting]
    total_room_setting_time_num = [[0.0 for i in range(4)] for j in range(5)]

    global total_room_setting_run_time
    global total_room_setting_run_time_num
    total_room_setting_run_time = [[[0.0 for i in range(max(max_run_num))] for j in range(4)] for d in range(5)] #access[room][setting][run]
    total_room_setting_run_time_num = [[[0.0 for i in range(max(max_run_num))] for j in range(4)] for d in range(5)]

    global total_room_run_time
    global total_room_run_time_num
    total_room_run_time = [[0.0 for i in range(max(max_run_num))] for j in range(5)]
    total_room_run_time_num = [[0.0 for i in range(max(max_run_num))] for j in range(5)]
    global stam_setting_time
    stam_setting_time = [0.0 for i in range(4)]

    global shield_setting_time
    shield_setting_time = [0.0 for i in range(4)]
    
    global hit_setting_num
    hit_setting_num = [0.0 for i in range(4)]
    global death_setting_num
    death_setting_num = [0.0 for i in range(4)]
    
    

    
    for run_tuple in run_tuples:
        #gettings vals from tuple
        participant = run_tuple[0]
        run_number = run_tuple[1]
        setting = run_tuple[2]
        diff = run_tuple[3]
        run_time = run_tuple[4]
        shield_usage = run_tuple[5]
        stam_usage = run_tuple[6]
        hits = run_tuple[7]
        deaths = run_tuple[8]
        room_times = [0.0,0.0,0.0,0.0,0.0]
        room_times[0] = run_tuple[9]
        room_times[1] = run_tuple[10]
        room_times[2] = run_tuple[11]
        room_times[3] = run_tuple[12]
        room_times[4] = run_tuple[13]

        #total time for each setting for all runs 
        total_setting_time[setting] += run_time
        total_setting_time_num[setting] += 1

        total_run_num_time[run_number] += run_time
        total_run_num_time_num[run_number] += 1

        stam_setting_time[setting] += stam_usage
        
        shield_setting_time[setting] += shield_usage

        death_setting_num[setting] += deaths
        hit_setting_num[setting] += hits

        for i in range(5):
            total_room_time[i] += room_times[i] #add run room times to global
            total_room_time_num[i] += 1
            
            total_room_setting_time[i][setting] += room_times[i]
            total_room_setting_time_num[i][setting] += 1

            total_room_setting_run_time[i][setting][run_number-1] += room_times[i]
            total_room_setting_run_time_num[i][setting][run_number-1] += 1

            total_room_run_time[i][run_number-1] += room_times[i]
            total_room_run_time_num[i][run_number-1] += 1


            

            

    for i in range(len(total_setting_time)):
        if(total_setting_time_num[i] != 0):
            total_setting_time[i] = total_setting_time[i] / total_setting_time_num[i]

            
    for i in range(len(total_room_time)):
        if(total_room_time[i] != 0):
            total_room_time[i] = total_room_time[i] / total_room_time_num[i]

    for i in range(len(total_run_num_time)):
        if(total_run_num_time[i] != 0):
            total_run_num_time[i] = total_run_num_time[i] / total_run_num_time_num[i]


    for i in range(len(total_room_setting_time)):
       for j in range(len(total_room_setting_time[i])):
           if(total_room_setting_time[i][j] != 0):
               total_room_setting_time[i][j] = total_room_setting_time[i][j] / total_room_setting_time_num[i][j]

    for i in range(len(total_room_setting_run_time)):
        for j in range(len(total_room_setting_run_time[i])):
            for k in range(len(total_room_setting_run_time[i][j])):
                if(total_room_setting_run_time[i][j][k] != 0.0):
                    total_room_setting_run_time[i][j][k] = total_room_setting_run_time[i][j][k] / total_room_setting_run_time_num[i][j][k]

    for i in range(len(shield_setting_time)):
        if(shield_setting_time[i] != 0):
            shield_setting_time[i] = shield_setting_time[i] / total_setting_time_num[i]

    for i in range(len(stam_setting_time)):
        if(stam_setting_time[i] != 0):
            stam_setting_time[i] = stam_setting_time[i] / total_setting_time_num[i]
    
    for i in range(len(hit_setting_num)):
        if(hit_setting_num[i] != 0):
            hit_setting_num[i] = hit_setting_num[i] / total_setting_time_num[i]

    for i in range(len(death_setting_num)):
        if(death_setting_num[i] != 0):
            death_setting_num[i] = death_setting_num[i] / total_setting_time_num[i]

    for i in range(len(total_room_run_time)):
            for j in range(len(total_room_run_time[i])):
                if(total_room_run_time[i][j] != 0.0):
                    total_room_run_time[i][j] = total_room_run_time[i][j] / total_room_run_time_num[i][j]




def run_hit_analysis():

    global setting_hit_time #average hits for each setting
    setting_hit_time = [0.0 for i in range(4)]
    global setting_hit_time_num
    setting_hit_time_num = [0.0 for i in range(4)]

    global hit_setting
    hit_setting = [0.0 for j in range(4)]
    

    global hit_room #stores average number of hits for each room USE HIT_ROOM_TIME_NUM
    hit_room = [0.0 for j in range(5)]

    global hit_room_setting #stores average number of hits for each room for each setting
    hit_room_setting = [[0.0 for i in range(4)] for j in range(5)] #access[room][setting]

    global hit_room_setting_run #number of hits per room per setting per run
    hit_room_setting_run = [[[0.0 for i in range(max(max_run_num))] for j in range(4)] for d in range(5)]

    for hit_tuple in hit_tuples:
        participant = hit_tuple[0]
        run_num = hit_tuple[1]
        setting = hit_tuple[2]
        room_num = hit_tuple[3]
        time_bool = hit_tuple[4]
        time = hit_tuple[5]


        if(time_bool):
            setting_hit_time[setting] += time
            setting_hit_time_num[setting] += 1

        hit_room[room_num] += 1
        hit_room_setting[room_num][setting] += 1
        hit_room_setting_run[room_num][setting][run_num-1] +=1
        hit_setting[setting] += 1





    #averages
    for i in range(len(hit_setting)):
        if(hit_setting[i] != 0):
            hit_setting[i] = hit_setting[i] / total_setting_time_num[i]
            
    for i in range(len(setting_hit_time)):
        if(setting_hit_time[i] != 0):
            setting_hit_time[i] = setting_hit_time[i] / setting_hit_time_num[i]


    for i in range(len(hit_room)):
        if(hit_room[i] != 0):
            hit_room[i] = hit_room[i] / total_room_time_num[i]

    for i in range(len(hit_room_setting)):
        for j in range(len(hit_room_setting[i])):
            if(hit_room_setting[i][j] != 0):
                hit_room_setting[i][j] = hit_room_setting[i][j] / total_room_setting_time_num[i][j]


    for i in range(len(hit_room_setting_run)):
        for j in range(len(hit_room_setting_run[i])):
            for k in range(len(hit_room_setting_run[i][j])):
                if(hit_room_setting_run[i][j][k] != 0):
                    hit_room_setting_run[i][j][k] = hit_room_setting_run[i][j][k] / total_room_setting_run_time_num[i][j][k]


def run_death_analysis():
    global death_setting
    death_setting = [0.0 for j in range(4)]

    global death_room
    death_room = [0.0 for i in range(5)]

    global death_room_setting
    death_room_setting = [[0.0 for i in range(4)] for j in range(5)]

    global death_room_setting_run
    death_room_setting_run = [[[0.0 for i in range(max(max_run_num))] for j in range(4)] for d in range(5)]


    for death_tuple in death_tuples:
        participant = death_tuple[0]
        run_num = death_tuple[1]
        setting = death_tuple[2]
        room_num = death_tuple[3]

        death_room[room_num] += 1
        death_setting[setting] += 1
        death_room_setting[room_num][setting] += 1
        death_room_setting_run[room_num][setting][run_num-1] += 1


       
    for i in range(len(death_setting)):
        if(death_setting[i] != 0):
            death_setting[i] = death_setting[i] / total_setting_time_num[i]


    for i in range(len(death_room)):
        if(death_room[i] != 0):
            death_room[i] = death_room[i] / total_room_time_num[i]

    for i in range(len(death_room_setting)):
        for j in range(len(death_room_setting[i])):
            if(death_room_setting[i][j] != 0):
                death_room_setting[i][j] = death_room_setting[i][j] / total_room_setting_time_num[i][j]


    for i in range(len(death_room_setting_run)):
        for j in range(len(death_room_setting_run[i])):
            for k in range(len(death_room_setting_run[i][j])):
                if(death_room_setting_run[i][j][k] != 0):
                    death_room_setting_run[i][j][k] = death_room_setting_run[i][j][k] / total_room_setting_run_time_num[i][j][k]




    
         
        
           
#main
global max_run_num #gives the value of the largest number of runs for any setting
max_run_num = [0,0,0,0]
read_all_files(2) #sets the global variables we are going to use
run_tuple_analysis()
#print(total_setting_time) #average time per setting
#print(total_room_time) #average time per room
#print(total_room_setting_time) #average timer per room for each setting
#print(total_run_num_time) #average time per run
#print(total_room_setting_time) #average time per room for each setting
#print(total_room_setting_run_time) #average time for each room/setting/run_time
#print(stam_setting_time) #average stamina usage per setting
#print(shield_setting_time) #average shield usage per setting
#print(hit_setting_num) #average hits per setting
#print(death_setting_num) #average deaths per setting
#print(total_room_run_time) #average time per room for each run
run_hit_analysis()
#rint(setting_hit_time) # average hit time for each setting
#print(hit_room) #average hits per room
#print(hit_room_setting) #average hits per room for each setting
#print(hit_room_setting_run) #average hits per room per room for each setting
#print(hit_setting) #average hits per setting used for error checking 
run_death_analysis()
#print(death_room) average deaths per room
#print(death_room_setting) #average deaths per room for each setting
#print(death_room_setting_run) #average deaths per room per setting per run
#print(death_setting) #average deaths per setting, used for error checking 







            
            
        
