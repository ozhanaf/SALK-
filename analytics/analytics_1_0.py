import mysql.connector
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt


def pull_data():
    utc_year = datetime.utcnow().strftime("%Y")  # Get year in UTC Time Zone
    utc_month = datetime.utcnow().strftime("%m")  # Get month in UTC Time Zone
    utc_day = datetime.utcnow().strftime("%d")  # Get day in UTC Time Zone
    db_access = mysql.connector.connect(user='salk',
                                        password='enGage', host='138.68.246.61',
                                        database='salk')  # Connect to database
    dbcursor = db_access.cursor()  # Create SQL cursor
    # dbcursor.execute("SELECT * from temporal_trails WHERE timestamp BETWEEN "
    #                  "'" + utc_year + "-" + utc_month + "-" + str(int(utc_day)-1) +
    #                  " 08:00:00' AND CURRENT_TIMESTAMP")                         # Query for all of today's data
    dbcursor.execute("SELECT * from temporal_trails WHERE timestamp BETWEEN '2017-11-09 "
                     "08:00:00' AND '2017-11-10 08:00:00'")
    trials_data = dbcursor.fetchall()  # Fetch today's trial data

    # dbCursor.execute("SELECT * from temporal_session WHERE timestamp BETWEEN '" +
    #                  utc_year + "-" + utc_month + "-" + str(int(utc_day)-1) +
    #                  " 08:00:00' AND CURRENT_TIMESTAMP")                         # Query for all of today's data
    dbcursor.execute("SELECT * from temporal_session WHERE timestamp BETWEEN '2017-11-09"
                     " 08:00:00' AND '2017-11-10 08:00:00'")
    sessions_data = dbcursor.fetchall()
    dbcursor.close()
    db_access.close()

    return sessions_data, trials_data


def extract_data(sessions_data, trials_data):
    i = len(trials_data)                                                          # number of points in today's data
    data_sessions = set()                                                               # initialize data sessions set
    for x in xrange(0, i):
        data_sessions.add(trials_data[x][2])                                      # today's session values
    daily_sessions = sorted(list(data_sessions))                                        # convert session into a sorted list
    num = len(daily_sessions)
    mouse_ids = []
    for x in range(0, len(sessions_data)):
        session = daily_sessions_data[x][0]
        for y in range(0, num):
            if session == daily_sessions[y]:
                mouse_ids.append(sessions_data[x][1])
    t_tot = [0] * num
    t_temp = [0] * num
    t_nt = [0] * num
    l_incor = [0] * num
    l_cor = [0] * num
    l_none = [0] * num
    l_incor_t = [0] * num
    l_cor_t = [0] * num
    l_none_t = [0] * num
    l_incor_nt = [0] * num
    l_cor_nt = [0] * num
    l_none_nt = [0] * num

    for x in range(0, len(daily_trials_data)):
        if daily_trials_data[x][8] == 0 and daily_trials_data[x][9] != 0:
            for y in range(0, num):
                if daily_trials_data[x][2] == daily_sessions[y]:
                    l_cor[y] = l_cor[y] + 1
                    t_tot[y] = t_tot[y] + 1
                    if "C8 E9 G8 C9" in str(daily_trials_data[x][5]):
                        t_temp[y] = t_temp[y] + 1
                        l_cor_t[y] = l_cor_t[y] + 1
                    else:
                        t_nt[y] = t_nt[y] + 1
                        l_cor_nt[y] = l_cor_nt[y] + 1
        if daily_trials_data[x][8] == 1:
            for y in range(0, num):
                if daily_trials_data[x][2] == daily_sessions[y]:
                    l_incor[y] = l_incor[y] + 1
                    t_tot[y] = t_tot[y] + 1
                    if "C8 E9 G8 C9" in str(daily_trials_data[x][5]):
                        t_temp[y] = t_temp[y] + 1
                        l_incor_t[y] = l_incor_t[y] + 1
                    else:
                        t_nt[y] = t_nt[y] + 1
                        l_incor_nt[y] = l_incor_nt[y] + 1
        if daily_trials_data[x][9] == 0:
            for y in range(0, num):
                if daily_trials_data[x][2] == daily_sessions[y]:
                    l_none[y] = l_none[y] + 1
                    t_tot[y] = t_tot[y] + 1
                    if "C8 E9 G8 C9" in str(daily_trials_data[x][5]):
                        t_temp[y] = t_temp[y] + 1
                        l_none_t[y] = l_none_t[y] + 1
                    else:
                        t_nt[y] = t_nt[y] + 1
                        l_none_nt[y] = l_none_nt[y] + 1

    t = [t_tot, l_cor, l_incor, l_none]
    temp = [t_temp, l_cor_t, l_incor_t, l_none_t]
    nt = [t_nt, l_cor_nt, l_incor_nt, l_none_nt]

    return t, temp, nt, mouse_ids, num


def create_stacked_graph(correct, incorrect, none, total, sessions, mouse_ids):
    plot_data = {}
    for a in range(0, sessions):
        plot_data[str(mouse_ids[a])] = [100 * float(correct[a]) / total[a],
                                        100 * float(incorrect[a]) / total[a],
                                        100 * float(none[a]) / total[a]]

    panda_plot_data = pd.DataFrame(data=plot_data)
    panda_plot_data_tp = pd.DataFrame(data=plot_data).transpose()
    ax = panda_plot_data_tp.plot.barh(stacked=True)
    columns = list(panda_plot_data)
    for b in range(0, sessions):
        percent_correct = panda_plot_data[str(mouse_IDs[b])][0]
        percent_incorrect = panda_plot_data[str(mouse_IDs[b])][1]
        percent_no_lick = panda_plot_data[str(mouse_IDs[b])][2]
        for c in range(0, sessions):
            if str(mouse_IDs[b]) == str(columns[c]):
                ax.text(percent_correct / 2 - 1, c, str(int(percent_correct * 100) / 100.00) + "%", fontsize=20)
                ax.text(percent_correct + percent_incorrect / 2 - 1, c,
                        str((int(percent_incorrect * 100) / 100.00)) + "%", fontsize=20)
                ax.text(percent_correct + percent_incorrect + percent_no_lick / 2 - 1, c,
                        str((int(percent_no_lick * 100) / 100.00)) + "%", fontsize=20)


[daily_sessions_data,
 daily_trials_data] = pull_data()

[[trials_total, licks_correct, licks_incorrect, licks_none],
 [trials_template, licks_correct_template, licks_incorrect_template, licks_none_template],
 [trials_non_template, licks_incorrect_non_template, licks_correct_non_template, licks_none_non_template],
 mouse_IDs,
 num_sessions] = extract_data(daily_sessions_data, daily_trials_data)

#trials_total                    = trials[0]
#licks_correct                   = trials[1]
#licks_incorrect                 = trials[2]
#licks_none                      = trials[3]
#trials_template                 = template[0]
#licks_correct_template          = template[1]
#licks_incorrect_template        = template[2]
#licks_none_template             = template[3]
#trials_non_template             = non_template[0]
#licks_incorrect_non_template    = non_template[1]
#licks_correct_non_template      = non_template[2]
#licks_none_non_template         = non_template[3]

create_stacked_graph(licks_correct,
                     licks_incorrect,
                     licks_none,
                     trials_total,
                     num_sessions,
                     mouse_IDs)
create_stacked_graph(licks_correct_template,
                     licks_incorrect_template,
                     licks_none_template,
                     trials_template,
                     num_sessions,
                     mouse_IDs)
create_stacked_graph(licks_correct_non_template,
                     licks_incorrect_non_template,
                     licks_none_non_template,
                     trials_non_template,
                     num_sessions,
                     mouse_IDs)
plt.show()
