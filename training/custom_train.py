import os
from agents.agent import DBAgentClass
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
db_password = os.getenv("DB_PASSWORD")

# Ensure the required environment variables are set
if not openai_api_key or not db_password:
    raise EnvironmentError("Missing required environment variables: OPENAI_API_KEY or DB_PASSWORD.")

# Initialize the Agent Instance instance
vn = DBAgentClass(api_key=openai_api_key, model='gpt-4o-mini', db_password=db_password)

# Connect to the database
vn.connect_to_database()

# Train with custom documentation
# vn.train_with_documentation(
#     documentation="Our business defines OTIF score as the percentage of orders that are delivered on time and in full."
# )

# Train with custom SQL query
# question = ""
# sql_query = ""
# vn.train_with_sql(
#     question=question,
#     sql_query=sql_query
# )