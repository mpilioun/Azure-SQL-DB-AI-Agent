

##################################### RUN THIS FILE ONCE at the start
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
print("Connecting to DB")
vn.connect_to_database()

# Retrieve the information schema
df_information_schema = vn.get_information_schema()

# Generate the training plan from the informations schema
training_plan = vn.create_training_plan(df_information_schema)

# Train using the generated plan
print("Training based on INFORMATION SCHEMA")
vn.train(plan=training_plan)

print("Getting FKs")
# Retrieve all the fk relationships of the database
fk_relationships = vn.get_fk_relationships()

# Add the relationships to the documentation
vn.train(documentation=fk_relationships)

print("Getting Constraints")
# Retrieve all the fk relationships of the database
databse_constraints = vn.get_constraint_documentation()

# Add the constraints of the databse to the documentation
for sentence in databse_constraints:
    vn.train(documentation=sentence)

print("Getting Views Definitions")
# Get all DB view definitions
view_querys = vn.get_view_definitions()

# Add the constraints of the databse to the documentation
for index, row in view_querys.iterrows():
    view_name = row['ViewName']
    view_query = row['ViewQuery']
    vn.train(sql=view_query)
    
    
print("Getting Stored Procedures Definitions")
# Get all DB Stored Procedures definitions
procedure_definitions = vn.get_stored_procedures()

# Add the Procedures of the database to the documentation
for index, row in procedure_definitions.iterrows():
    procedure_name = row['ProcedureName']
    procedure_query = row['ProcedureDefinition']
    vn.train(question=procedure_name, sql=view_query)