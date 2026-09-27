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
