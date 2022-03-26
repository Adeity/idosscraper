from bs4 import BeautifulSoup
import requests

url = "https://idos.idnes.cz/pid/spojeni/"

#
# runs a selector on element and returns the first result
#
def get_inner_html_first(element, selector):
    return element.select(selector)[0]

def get_inner_html_all(element, selector):
    return element.select(selector)

def get_total_time_distance(e):
    inner_html_all = get_inner_html_all(e, "p.reset.total strong")
    time = inner_html_all[0].decode_contents()
    distance = inner_html_all[1].decode_contents()
    return time, distance


    

def get_starting_date(e):
    return get_inner_html_first(e, "span.date-after").decode_contents()

def parse_transfer_info(transfer):
    # get the name
    line_title = transfer.select(".title-container")[0]
    name = line_title.select("h3 span")[0].decode_contents()

    # get current delayo
    delay = transfer.select(".")

    return True


# 
# header_box contains info about when link starts and total time and so on
#
def parse_headerbox_info(header_box):
    e = header_box[0]
    starting_date = get_starting_date(e)
    total_time, distance = get_total_time_distance(e)
    return starting_date, total_time, distance

#
# @param is is connection list
# @return connection list parsed into json
#
def parse_connection_list_into_json(connection_list_array) :
    for detail_box in connection_list_array:
        # get data from header, the header is just one even for complex connections
        header_box = detail_box.select("div.date-total")
        starting_date, total_time, distance = parse_headerbox_info(header_box)
        #print("starting_date:", starting_date, "total_time:", total_time, "distance:", distance)

        # get data from body of each connection
        connection_details_box = detail_box.select("div.outside-of-popup")
        print("outside_of_popup len:",len(connection_details_box))
        for transfer in connection_details_box:
            #type_of_vehicle, name_of_vehicle, current_delay, source_dest, tar_dest, departure_time, arrival_time = parse_transfer_info(transfer)
            parse_transfer_info(transfer)
            #print("type_of_vehicle:", type_of_vehicle,"name_of_vehicle:", name_of_vehicle, "current_delay:", current_delay,"source_dest", source_dest, "tar_dest", tar_dest, "departure_time", departure_time, "arrival_time", arrival_time)

#  find every connection 
#  returns result set of connections
def get_connection_result_set(url):
    result = requests.get(url)

    doc = BeautifulSoup(result.text, "html.parser")
    connection_list_array = doc.select("div.detail-box")
    return connection_list_array

def get_connection_home():
    return get_connection_result_set(home_to_school_url())

#  each connection has a number of subconnections (1..n)  
#  each subconnection has departure time and arrival time
#  return list of subconnections
def get_subconnection_list(connection):
    return connection.find_all("div", {"class":"line-item"})


def print_departure_time_of_connection(connection):
    first_subconnection = get_subconnection_list(connection)[0]
    departure_time = first_subconnection.find("ul", {"class": ["reset", "stations"]}).find("p", {"class":["reset", "time"]}) 
    print("departure time: " + departure_time.text)


def home_to_school_url():
    res_url = "" 
    res_url += url 
    res_url += "?"
    res_url += "f=Velke%20Prilepy&"
    res_url += "t=Andel&"
    res_url += "submit=true"
    return res_url



connection_box = get_connection_home()
#print(connection_box)
parsed_to_json = parse_connection_list_into_json(connection_box)
#print(home_to_school_url())
#print_departure_time_of_connection(connection_box)
