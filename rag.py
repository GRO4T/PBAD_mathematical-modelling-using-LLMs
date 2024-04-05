import os

import weaviate
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Weaviate
from langchain_community.document_loaders import PyPDFLoader
from weaviate.embedded import EmbeddedOptions

# Prepare document vector store
client = weaviate.Client(embedded_options=EmbeddedOptions())
chunks = []
for source in os.listdir("./sources/"):
    # Load document
    loader = PyPDFLoader(f"sources/{source}")
    document = loader.load()
    # Split document into chunks
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks.extend(text_splitter.split_documents(document))

vectorstore = Weaviate.from_documents(
    client=client, documents=chunks, embedding=OpenAIEmbeddings(), by_text=False
)
retriever = vectorstore.as_retriever()

# Create prompt template
# template = """You are an assistant for question-answering tasks.
# Use the following pieces of retrieved context to answer the question.
# If you don't know the answer, just say that you don't know.
# Use three sentences maximum and keep the answer concise.
# Question: {question}
# Context: {context}
# Answer:
# """
template = """
{question}

### CONTEXT:
{context}
"""
prompt = ChatPromptTemplate.from_template(template)

rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt

query = """
You are an operations analyst and expert mathematical modeller AI bot.
Your task is to formulate and solve the given optimization problem as a LP. Please read the problem information, input format, and objective carefully and provide a detailed mathematical formulation.

### PROBLEM INFORMATION:


- A state wants to plan its electricity capacity for the next \var{T} years. 
- The state has a forecast of \var{demand_t} megawatts, presumed accurate, of the demand for electricity during year \var{t}.
- The existing capacity, which is in oil-fired plants, that will not be retired and will be available during year \var{t}, is \var{oil_t}.
- There are two alternatives for expanding electric capacity: coal­ fired or nuclear power plants.
- There is a capital cost of \var{coal_cost} per megawatt of coal-fired capacity that becomes operational at the beginning of year \var{t}.
- There is a capital cost of \var{nuke_cost} per megawatt of nuclear power capacity that becomes operational at the beginning of year \var{t}.
- For various political and safety reasons, it has been decided that no more than \var{max_nuke}% of the total capacity should ever be nuclear (\var{max_nuke} is a number between 0 and 100).
- Coal plants last for \var{coal_life} years, while nuclear plants last for \var{nuke_life} years.


### INPUT FORMAT:


{
    "demand": [demand_t for t in 1, ..., T],
    "oil_cap": [oil_t for t in 1, ..., T],
    "coal_cost": coal_cost,
    "nuke_cost": nuke_cost,
    "max_nuke": max_nuke,
    "coal_life": coal_life,
    "nuke_life": nuke_life,
}



- Variables enclosed in [ ] represent lists of values.
- Names enclosed in quotes (") represent keys and are identical to those in the data file.
- All other items are variables as described in the problem description and should be replaced with their actual values from the data file.

### OBJECTIVE: 

What is the capacity expansion plan that results in the minimum cost?

### OUTPUT INFORMATION:


- the output should represent how much coal and nuclear capacity should be added in each year, and how much the total cost is.
- the output should be a dictionary with three keys: "coal_cap_added", "nuke_cap_added", and "total_cost".
- the value of "coal_cap_added" should be a list of the coal capacity added in each year.
- the value of "nuke_cap_added" should be a list of the nuclear capacity added in each year.
- the value of "total_cost" should be a single floating point number showing the total cost of the system.



### OUTPUT FORMAT:


{
    "coal_cap_added": [coal_t for t in 1, ..., T],
    "nuke_cap_added": [nuke_t for t in 1, ..., T],
    "total_cost": total_cost,
}



### INSTRUCTIONS:
1. Clearly define the decision variables.
2. Formulate the objective function precisely.
3. List all the constraints, ensuring they are complete and non-redundant.
4. Ensure the formulation is coherent, logical, and solvable.
5. Provide any necessary explanations or clarifications for your formulation.

Please respond with a well-structured mathematical formulation of the given optimization problem, adhering to the instructions and format provided above.
"""
with open("rag.out", "w", encoding="utf-8") as f:
    f.write(rag_chain.invoke(query).to_string())
