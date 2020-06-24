




def get_hists(end_time): 
    a_year=31536000
    for i in range(1,6):
        print("\"?period1=" + str(end_time - ((i+1) * a_year)) + "&period2=" + str(end_time - i * a_year) + "&interval=1d&events=history\"", end=" ")


def get_sims(end_time):
    a_year=31536000
    for i in range(1,6): 
        print("\"?period1=" + str(end_time - (i * a_year)) + "&period2=" + str(end_time) + "&interval=1d&events=history\"", end=" ")

