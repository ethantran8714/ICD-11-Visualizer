from ICD11 import release_data as database
import networkx as nx
import matplotlib.pyplot as plt

master = {}


def get_title(icd11_code):  # this returns a string title
    return database(str(icd11_code))["title"]["@value"]


def get_title_id(icd11_code):  # this returns a string id
    return database(str(icd11_code))["@id"][45:]


def get_child_id(icd11_code):  # this returns a child list of ICD11 codes
    if "child" in database(str(icd11_code)):  # reduce time by getting rid of .keys()
        temp_list = []
        codes = database(str(icd11_code))["child"]
        for i in codes:
            if i[45:].isdigit():  # stops taking in other/unspecified
                temp_list.append(i[45:])
        return temp_list


def get_child_name(icd11_code):  # this returns a child list of ICD11 names
    if "child" in database(str(icd11_code)):  # reduce time by getting rid of .keys()
        temp_list = []
        for i in get_child_id(icd11_code):
            temp_list.append(database(str(i))["title"]["@value"])
        return temp_list


def get_parent_id(icd11_code):
    if "parent" in database(str(icd11_code)):  # reduce time by getting rid of .keys()
        return database(str(icd11_code))["parent"][0][45:]


def master_dict_initializer(icd11_code):
    id_only = {}
    for i in get_child_id(icd11_code):
        master[get_title(i)] = get_child_name(i)
        id_only[get_title_id(i)] = get_child_id(i)
    return id_only


def increase_layer(dictionary):
    values = list(dictionary.values())
    hidden = {}
    for i in values:
        if i is None:
            continue
        else:
            for q in range(len(i)):
                master[get_title(i[q])] = get_child_name(i[q])
                hidden[get_title(i[q])] = get_child_id(i[q])
    return hidden


def tuple_creator(final_dict):
    tuple_list = []
    for k, v in final_dict.items():
        if v is not None:
            for i in range(len(v)):
                tuple_list.append((k, v[i]))
    return tuple_list


def graph_visual(start_code, layers):
    dict_ = master_dict_initializer(str(start_code))

    for i in range(layers):
        new_dict = increase_layer(dict_)
        dict_ = new_dict

    edges = tuple_creator(master)
    graph = nx.DiGraph()
    graph.add_nodes_from(master.keys())
    graph.add_edges_from(edges)

    plt.figure(figsize=(50, 50))
    nx.draw(graph, with_labels=True, pos=nx.spring_layout(graph, k=0.2))
    plt.savefig('example.png')


graph_visual(426429380, 4)
