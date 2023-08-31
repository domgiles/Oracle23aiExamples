import oracledb
from oracledb import Connection
from pyvis.network import Network
from prettytable import PrettyTable
from IPython.display import HTML, display
import time
import matplotlib.pyplot as plt
import pandas as pd
import json

def execute_plsql_and_dbmsoutput(connection, code):
    with connection.cursor() as cursor:
        cursor.callproc("dbms_output.enable")
        cursor.execute(code)
        chunk_size = 100
        # create variables to hold the output
        lines_var = cursor.arrayvar(str, chunk_size)
        num_lines_var = cursor.var(int)
        num_lines_var.setvalue(0, chunk_size)

        # fetch the text that was added by PL/SQL
        result = []
        while True:
            cursor.callproc("dbms_output.get_lines", (lines_var, num_lines_var))
            num_lines = num_lines_var.getvalue()
            lines = lines_var.getvalue()[:num_lines]
            for line in lines:
                result.append(line)
            if num_lines < chunk_size:
                break

        # format the content and write them to the screen
        cols = result[0].split(',')
        table = PrettyTable(cols)
        for row in result[1:]:
            table.add_row(row.split(','))

        display(HTML(table.get_html_string()))
        

def execute_plsql(connection, code):
    with connection.cursor() as cursor:
        cursor.callproc("dbms_output.enable")
        cursor.execute(code)
        

def render_graph(net:Network, connection:Connection) -> None:
    
    with connection.cursor() as cursor:
        cursor.execute('''select c.id,
                           c.first_name,
                           c.last_name 
                           from new_customers c''')
        rows = cursor.fetchall()
        for row in rows:
            net.add_node(int(row[0]), label=f'{row[1]} {row[2]}\n{row[0]}')
        cursor.execute('''select source_id,
                            target_id,
                            relationship 
                           from customer_relationships''')
        rows = cursor.fetchall()
        for row in rows:
            net.add_edge(int(row[0]), int(row[1]), label=row[2])
        net.repulsion(node_distance=100, spring_length=200)
        
    

def render_query(net:Network, connection:Connection, query:str, highlight:list) -> None:
    
    with connection.cursor() as cursor:
        
        cursor.execute(query)
        rows = cursor.fetchall()
        nodes_to_render = []
        
        table = PrettyTable(['Path'])
        
        for row in rows:
            table.add_row([row[0]])
            nodes = row[1].split(',')
            for node in nodes:
                if node.strip() not in nodes_to_render:
                    nodes_to_render.append(int(node.strip()))
        
        display(HTML(table.get_html_string()))
        
        cursor.execute('''select c.id,
                           c.first_name,
                           c.last_name 
                           from new_customers c''')
        rows = cursor.fetchall()
        for row in rows:
            if row[0] in nodes_to_render:
                net.add_node(int(row[0]), label=f'{row[1]} {row[2]}\n{row[0]}', color='red')
            elif row[0] in highlight:
                net.add_node(int(row[0]), label=f'{row[1]} {row[2]}\n{row[0]}', color='#8B2500')
            else:
                net.add_node(int(row[0]), label=f'{row[1]} {row[2]}\n{row[0]}')
        cursor.execute('''select source_id,
                            target_id,
                            relationship 
                           from customer_relationships''')
        rows = cursor.fetchall()
        for row in rows:
            net.add_edge(int(row[0]), int(row[1]), label=row[2])
        net.repulsion(node_distance=100, spring_length=200)


def compare_performance(things_to_execute:str, execution_count:int, connection:oracledb.Connection) -> None:
    cursor = connection.cursor()
    results = []
    for t in things_to_execute:
        sql = t["SQL"]
        title = t["Name"]
        start = time.time()
        for i in range(1, execution_count):
            cursor.execute(sql)
        results.append({"Title":title,"Result":time.time() - start})
    timings = [r["Result"] for r in results]
    columns_names = [r["Title"] for r in results]
    plt.bar(range(len(timings)), timings)
    plt.xticks(range(len(timings)),columns_names)
    plt.title (f"Comparison of Performance for {execution_count} executions")
    plt.ylabel("Seconds")
    plt.show()
        
    