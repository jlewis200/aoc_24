#!/usr/bin/env python3

import re
from json import dump, load
import dash
import dash_cytoscape as cyto
from dash import html, Input, callback
import networkx as nx


def get_graph(states, operations):
    """
    Build the graph based on states and operations.
    """
    graph = nx.DiGraph()

    for dst, (operator, src_0, src_1) in operations.items():
        graph.add_edge(src_0, dst, classes=operator)
        graph.add_edge(src_1, dst, classes=operator)
        graph.nodes[dst]["classes"] = operator

    for node, state in states.items():
        graph.nodes[node]["value"] = state

    return graph


def parse(data):
    states = {}
    operations = {}

    states_data, operations_data = data.split("\n\n")

    for line in states_data.split("\n"):
        key, value = line.split(":")
        states[key.strip()] = value.strip() == "1"

    for line in operations_data.strip().split("\n"):
        match = re.fullmatch(
            "(?P<operand_0>.+) (?P<operator>.*) (?P<operand_1>.*) -> (?P<destination>.*)",
            line,
        )
        operations[match.group("destination")] = (
            match.group("operator"),
            match.group("operand_0"),
            match.group("operand_1"),
        )

    return states, operations


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def get_position_map(graph):
    try:
        with open("node_positions.json", "rb") as f_in:
            position_map = load(f_in)

    except FileNotFoundError:
        position_map = nx.nx_agraph.graphviz_layout(graph)

    return position_map


def main():
    states, operations = parse(read_file("input.txt"))
    graph = get_graph(states, operations)
    for node in graph:
        if "classes" not in graph.nodes[node]:
            if "classes" not in graph.nodes[node]:
                graph.nodes[node]["classes"] = None

    app = get_app(graph, get_position_map(graph))
    app.run_server(debug=True)


# node_color_map = {}

# edge_color_map = {
#     "XOR": "red",
#     "AND": "green",
#     "OR": "blue",
# }


def get_app(graph, position_map):
    elements = []

    for src, dst in graph.edges:
        elements.append({"data": {"id": f"{src}-{dst}", "source": src, "target": dst}})

    for node in graph.nodes:
        x, y = position_map[node]
        elements.append(
            {
                "data": {"id": node},
                "position": {"x": x, "y": y},
                "classes": graph.nodes[node]["classes"],
            }
        )

    app = dash.Dash(__name__)
    app.layout = html.Div(
        [
            cyto.Cytoscape(
                id="cytoscape",
                layout={"name": "preset"},
                style={"width": "100%", "height": "1200px"},
                elements=elements,
                userZoomingEnabled=True,
                userPanningEnabled=True,
                stylesheet=[
                    {
                        "selector": "node",
                        "style": {
                            "label": "data(id)",
                        },
                    },
                    {
                        "selector": "edge",
                        "style": {
                            "target-arrow-shape": "triangle",
                            "curve-style": "bezier",
                            "line-color": "data(color)",
                            # "target-arrow-color": color_map[op],
                        },
                    },
                ],
            ),
        ]
    )
    return app


@callback(Input("cytoscape", "elements"))
def node_dropped(elements):
    node_positions = {
        el["data"]["id"]: (el["position"]["x"], el["position"]["y"])
        for el in elements
        if "position" in el
    }

    with open("node_positions.json", "w", encoding="utf-8") as f_out:
        dump(node_positions, f_out)


if __name__ == "__main__":
    main()
