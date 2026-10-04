from agent import analyze_brain_dump


text = """
I need to submit my internship application tomorrow.
I still need a passport photo.
I also have a DBMS exam Thursday.
"""

result = analyze_brain_dump(text)

print(result)
