from fastmcp import FastMCP

mcp=FastMCP("Mathserver")

@mcp.tool()
def multiply(a:int,b:int)->int:
    """Multiplies two numbers"""
    return a*b
def add(a:float,b:float)->float:
    """Adds two float numbers and returns the result"""
    return a+b

if __name__=="__main__":
    mcp.run()