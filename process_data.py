import pg8000 as pg
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame

# Connect to the database
# Will need to be on Mines VPN for this to work
user = 'smsovereign'
password = 'Jag283sam240'
db_conn = pg.connect(user=user, password=password, host='codd.mines.edu', port=5433, database='csci403')

# Establish the database cursor
cursor = db_conn.cursor()

# Move into correct schema
schema_correction = "SET search_path TO iradley, "+user+", public"
cursor.execute(schema_correction)

# Example code of simple query
'''
cursor.execute("SELECT * FROM tax_revenue")

results = cursor.fetchall()
for row in results:
    print(row)
'''

# Get the data for the states
states_to_examine = ['CO', 'WA', 'NV', 'MA', 'CA', 'MI', 'AK', 'OR']
# Get state populations
state_query = "("
for state in states_to_examine:
    state_query += '\''+state+'\''+', '
state_query = state_query[:-2]
state_query += ')'

execution = "SELECT * FROM state_pop WHERE state IN " + state_query

cursor.execute(execution)
state_pops = cursor.fetchall()

# Add to population dict
pops_dict = {}
for state in state_pops:
    pops_dict[state[0]] = state[1]

# Get state marijuana tax revenues
execution = "SELECT * FROM tax_revenue WHERE state IN " + state_query
cursor.execute(execution)
state_rev = cursor.fetchall()

# Add to revenue dict
state_dict = {}

for state in state_rev:
    state_dict.setdefault(state[0], []).append([state[1], state[2]])

# Get state patent numbers
execution = "Select * FROM patents WHERE state IN " + state_query
cursor.execute(execution)
state_patents = cursor.fetchall()


patents_dict = {}

for state in state_patents:
    patents_dict.setdefault(state[1], []).append([state[0], state[2]])

# Add to state
for state in state_patents:
    for curr_state in state_dict[state[1]]:
        patent_year = state[0]
        dict_year = curr_state[0]
        if(patent_year == dict_year):
            curr_state.append(state[2])

i = 0
for state in state_patents:
    while i < len(state_dict[state[1]]):
        curr_state = state_dict[state[1]][i]
        if len(curr_state) < 3:
            state_dict[state[1]].pop(i)
            i -= 1
        i += 1
    i = 0

# Graphing state stats per capita

curr_plot = 0

for curr_state in states_to_examine:
    fig, ax = plt.subplots()
    twin1 = ax.twinx()

    x_axis = [int(state[0]) for state in state_dict[curr_state]]

    # Make left y-axis marijuana revenue per capita
    p1_y = [round(state[1]/(pops_dict[curr_state]*1000000), 2) for state in state_dict[curr_state]]
    p1, = ax.plot(x_axis, p1_y, "g-", label="Marijuana Revenue")

    # Make right y-axis patent numbers per capita
    #p2_y = [round(state[2]/pops_dict[curr_state]) for state in state_dict[curr_state]]
    p2_y = [state[1]/(pops_dict[curr_state]*1000000) for state in patents_dict[curr_state]]
    patent_x_axis = [int(state[0]) for state in patents_dict[curr_state]]
    p2, = twin1.plot(patent_x_axis, p2_y, "b-", label="Number of Patents")
    
    # Set bounds for the axes
    ax.set_xlim(min(patent_x_axis), max(x_axis))
    ax.set_ylim(0, float(max(p1_y))+(.1*float(max(p1_y))))
    twin1.set_ylim(max(min(p2_y)-10, 0), float(max(p2_y))+(.1*float(max(p2_y))))

    # Label the axes
    ax.set_xlabel("Year")
    ax.set_ylabel("Marijuana Revenue per Capita")
    twin1.set_ylabel("Patents per Capita")

    # Color the axes
    ax.yaxis.label.set_color(p1.get_color())
    twin1.yaxis.label.set_color(p2.get_color())

    # Set the legend
    ax.legend(handles=[p1, p2])

    # Set title
    title = "Marijuana Revenue and Patent Number Per Capita in " + curr_state
    plt.title(label=title)

    curr_plot += 1
    # Display plot
    plt.show()
