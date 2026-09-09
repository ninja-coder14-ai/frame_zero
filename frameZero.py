import os
from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

grafana_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command='uvx',
            args=['mcp-grafana'],
            env={
                'GRAFANA_URL': os.getenv('GRAFANA_URL'),
                'GRAFANA_SERVICE_ACCOUNT_TOKEN': os.getenv('GRAFANA_SERVICE_ACCOUNT_TOKEN'),
            },
        ),
        timeout=60,
    ),
)

root_agent = Agent(
    model='gemini-3.5-flash',
    name='frame_zero',
    description='An agent that investigates anomalies in a media production pipeline using Grafana.',
    instruction=(
        'You are Frame Zero, a security investigation agent for a media production pipeline. '
        'You are on a strict API budget: work efficiently and decisively, minimizing the number '
        'of tool calls and reasoning steps. Do not re-query the same data twice. '
        'When asked to investigate an anomaly: '
        '1. Make ONE targeted Loki query covering the relevant time window and service. '
        '2. Analyze the results in a single pass. '
        '3. If you find a genuine anomaly, immediately call create_annotation once with a concise '
        'summary and relevant tags. '
        '4. Give your final answer citing the specific data you queried. '
        'Do not repeat queries, do not second-guess yourself with additional tool calls, and do not '
        'ask the user clarifying questions unless the request is genuinely ambiguous.'
    ),
    tools=[grafana_tools],
) 