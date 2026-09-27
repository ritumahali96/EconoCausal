import pandas as pd
from dowhy import CausalModel

df = pd.read_csv("week1_causal_graphing/data/retail_campaign_data.csv")

# A DAG (Directed Acyclic Graph) is a drawing where arrows show
# cause -> effect. Anything with an arrow into BOTH discount_given
# and purchased is a confounder and must be controlled for.

causal_graph = """
graph [
    directed 1
    node [ id "loyalty_score"   label "loyalty_score" ]
    node [ id "income"          label "income" ]
    node [ id "age"              label "age" ]
    node [ id "discount_given"  label "discount_given" ]
    node [ id "purchased"       label "purchased" ]

    edge [ source "loyalty_score"  target "discount_given" ]
    edge [ source "loyalty_score"  target "purchased" ]
    edge [ source "income"         target "discount_given" ]
    edge [ source "income"         target "purchased" ]
    edge [ source "age"            target "purchased" ]
    edge [ source "discount_given" target "purchased" ]
]
"""

# NOTE: loyalty_score and income each have TWO outgoing arrows
# (into discount_given AND purchased) -- that double-arrow pattern
# is the signature of a confounder. age has only one arrow, so it's
# a normal cause, not a confounder.

model = CausalModel(
    data=df,
    treatment="discount_given",
    outcome="purchased",
    graph=causal_graph,
)

identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)

print(identified_estimand)

# DoWhy's answer: to isolate the true effect of discount_given on
# purchased, you must control for loyalty_score and income.
# age does NOT need to be controlled for.

import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

edges = [
    ("loyalty_score", "discount_given"),
    ("loyalty_score", "purchased"),
    ("income", "discount_given"),
    ("income", "purchased"),
    ("age", "purchased"),
    ("discount_given", "purchased"),
]

G.add_edges_from(edges)

pos = {
    "loyalty_score": (0, 2),
    "income": (0, 1),
    "age": (0, 0),
    "discount_given": (2, 1.5),
    "purchased": (4, 1),
}

node_colors = []
for node in G.nodes():
    if node == "discount_given":
        node_colors.append("#ffb703")
    elif node == "purchased":
        node_colors.append("#2a9d8f")
    else:
        node_colors.append("#8ecae6")

plt.figure(figsize=(9, 5))

nx.draw(
    G, pos, with_labels=True, node_color=node_colors, node_size=3200,
    font_size=9, font_weight="bold", arrowsize=25, edge_color="#555555",
    width=1.8,
)

plt.figure(figsize=(9, 5))

nx.draw(
    G, pos, with_labels=True, node_color=node_colors, node_size=3200,
    font_size=9, font_weight="bold", arrowsize=25, edge_color="#555555",
    width=1.8,
)

plt.title("EconoCausal Week 1: Causal DAG", fontsize=11)

plt.tight_layout()
