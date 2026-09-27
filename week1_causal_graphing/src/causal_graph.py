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
