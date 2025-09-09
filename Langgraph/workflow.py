from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from Automation.aws_automation import get_ips_aws
from Automation.fetching_sql_data import query_reports
from Automation.jasper_automation import run_jaspersoft

class AgentState(TypedDict) :
    ip_address: list[str]
    pdf_input: dict
    validation_status: bool

def get_ips(state:AgentState) :
    ips = get_ips_aws()
    state['ip_address'] = ips
    return state

def get_db_details(state:AgentState) :
    db_data = query_reports(101)
    state['pdf_input'] = db_data
    return state

def get_pdf_reports(state:AgentState) :
    sql_data_for_pdf = state['pdf_input']
    run_jaspersoft(sql_data_for_pdf)
    return state

graph = StateGraph(AgentState)

graph.add_node("get_ips", get_ips)
graph.add_node("get_db_details", get_db_details)
graph.add_node("get_pdf_reports", get_pdf_reports)

graph.add_edge(START, "get_ips")
graph.add_edge("get_ips", "get_db_details")
graph.add_edge("get_db_details", "get_pdf_reports")
graph.add_edge("get_pdf_reports", END)

initial_state: AgentState = {
    "ip_address": [],
    "pdf_input": {},
    "validation_status": False
}

app = graph.compile()
app.invoke(initial_state)