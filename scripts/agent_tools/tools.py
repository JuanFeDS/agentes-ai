"""tools.py"""
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from tavily import create_tavily_tool
from retriever import create_web_retriever_tool

load_dotenv()

def manage_tools(
    url: str = 'https://es.wired.com/articulos/que-es-nano-banana-te-explicamos-como-funciona-el-nuevo-editor-de-imagenes-de-google'
    ):
    """Manage the tools for the agent."""

    tavily_tool = create_tavily_tool()
    retriever_tool = create_web_retriever_tool(url)

    tools = [tavily_tool, retriever_tool]


    model = ChatOpenAI(
        model='gpt-4o',
        temperature=0,
        # max_tokens=1000,
        # streaming=True
    )

    # Crear un diccionario de herramientas para facilitar su búsqueda
    tools_dict = {tool.name: tool for tool in tools}
    
    # Obtener la respuesta del modelo con las herramientas
    response = model.bind_tools(tools).invoke(
        [HumanMessage(content='Hola, sabes que es nano banana?')]
    )
    
    # Verificar si hay llamadas a herramientas
    if hasattr(response, 'tool_calls') and response.tool_calls:
        # Tomar la primera llamada a herramienta
        tool_call = response.tool_calls[0]
        tool_name = tool_call['name']
        tool_args = tool_call['args']
        
        print(f"\n=== EJECUTANDO HERRAMIENTA ===")
        print(f"Herramienta: {tool_name}")
        print(f"Argumentos: {tool_args}")
        
        # Obtener y ejecutar la herramienta
        tool = tools_dict[tool_name]
        tool_result = tool.invoke(tool_args)
        
        print("\n=== RESULTADO DE LA HERRAMIENTA ===")
        print(f"Tipo: {type(tool_result).__name__}")
        print("Contenido:")
        if isinstance(tool_result, dict):
            for key, value in list(tool_result.items())[:5]:  # Mostrar solo las primeras 5 entradas
                print(f"  {key}: {str(value)[:200]}..." if len(str(value)) > 200 else f"  {key}: {value}")
            if len(tool_result) > 5:
                print(f"  ... y {len(tool_result) - 5} entradas más")
        else:
            content = str(tool_result)
            print(content[:500] + "..." if len(content) > 500 else content)
        print("=" * 50 + "\n")
        
        # Obtener la respuesta final del modelo usando el resultado de la herramienta
        final_response = model.invoke([
            HumanMessage(content='Hola, sabes que es nano banana?'),
            response,
            {"role": "tool", "tool_call_id": tool_call['id'], "name": tool_name, "content": str(tool_result)}
        ])
        
        return final_response.content
    
    return response.content
