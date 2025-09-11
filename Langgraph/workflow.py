from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from Automation.aws_automation import get_ips_aws
from Automation.fetching_sql_data import query_for_measurements, query_for_part_requirement
from Automation.jasper_automation import run_jaspersoft
from Automation.maintenix_automation import run_mx
from Automation.pdf_vertical_text import check_vertical_text_blocks

class AgentState(TypedDict) :
    ip_address: list[str]
    barcode : str
    part_requirement_sql_data : dict
    measurements_sql_data : dict
    validation_status: bool

def get_ips(state:AgentState) :
    ips = get_ips_aws()
    state['ip_address'] = ips
    return state

def get_barcode(state:AgentState) :
    barcode = run_mx()
    state['barcode'] = barcode
    return state

def get_sqldata(state:AgentState) :
    part_requirement_sql_data = query_for_part_requirement(101)
    state['part_requirement_sql_data'] = part_requirement_sql_data
    barcode = state['barcode']
    state['measurements_sql_data'] = query_for_measurements(barcode)
    return state

def get_pdf_reports(state:AgentState) :
    input_params_casa_faa = {"inventory_barcode": "I0002JMAN", "user_id": "100933"}
    input_params_part_requirement = state['part_requirement_sql_data']
    input_params_measurements = state['measurements_sql_data']
    run_jaspersoft(input_params_casa_faa, input_params_part_requirement, input_params_measurements)
    return state

def pdf_verification(state:AgentState) :
    status = check_vertical_text_blocks(r"D:\Rakesh\Study materials\PDF Parsing Agent\Utils\Sample PDF.pdf")
    if status :
        state['validation_status'] = True
        return state
    
graph = StateGraph(AgentState)

graph.add_node("get_ips", get_ips)
graph.add_node("get_barcode", get_barcode)
graph.add_node("get_sql_data", get_sqldata)
graph.add_node("get_pdf_reports", get_pdf_reports)
graph.add_node("pdf_verification", pdf_verification)

graph.add_edge(START, "get_ips")
graph.add_edge("get_ips", "get_barcode")
graph.add_edge("get_barcode", "get_sql_data")
graph.add_edge("get_sql_data", "get_pdf_reports")
graph.add_edge("get_pdf_reports", "pdf_verification")
graph.add_edge("pdf_verification", END)

initial_state: AgentState = {
    "ip_address": [],
    "barcode" : "",
    "part_requirement_sql_data": {},
    "measurements_sql_data": {},
    "validation_status": False
}

app = graph.compile()
app.invoke(initial_state)