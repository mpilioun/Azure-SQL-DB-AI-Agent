import os
from vanna.openai import OpenAI_Chat
from vanna.chromadb import ChromaDB_VectorStore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DBAgentClass(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, api_key, model, db_password):
        # Initialize parent classes
        ChromaDB_VectorStore.__init__(self, config={'api_key': api_key})
        OpenAI_Chat.__init__(self, config={'api_key': api_key, 'model': model})
        self.db_password = db_password

    def connect_to_database(self):
        # Create a connection string
        ODBC_SQL_AUTHENTICATION = os.getenv("ODBC_SQL_AUTHENTICATION")
        connection_string = ODBC_SQL_AUTHENTICATION = ODBC_SQL_AUTHENTICATION.replace("{your_password_here}", self.db_password)

        # Establish connection
        self.connect_to_mssql(odbc_conn_str=connection_string)

    def get_information_schema(self):
        # Query the database schema
        return self.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")

    def get_fk_relationships(self):
        # Query the database schema
        fk_relationships = self.run_sql("""SELECT 
                                    fk.name AS FK_name,
                                    tp.name AS parent_table,
                                    c1.name AS parent_column,
                                    ref.name AS referenced_table,
                                    c2.name AS referenced_column
                                FROM 
                                    sys.foreign_keys AS fk
                                    INNER JOIN sys.foreign_key_columns AS fkc 
                                        ON fk.object_id = fkc.constraint_object_id
                                    INNER JOIN sys.tables AS tp 
                                        ON fkc.parent_object_id = tp.object_id
                                    INNER JOIN sys.tables AS ref 
                                        ON fkc.referenced_object_id = ref.object_id
                                    INNER JOIN sys.columns AS c1 
                                        ON fkc.parent_column_id = c1.column_id 
                                        AND c1.object_id = tp.object_id
                                    INNER JOIN sys.columns AS c2 
                                        ON fkc.referenced_column_id = c2.column_id 
                                        AND c2.object_id = ref.object_id
                                ORDER BY 
                                    fk.name, tp.name, ref.name"""
                        )
        sentences = []
        
        # Iterate over the DataFrame rows and create sentences
        for index, row in fk_relationships.iterrows():
            sentence = f"You can join table {row['parent_table']} with {row['referenced_table']} using the key {row['parent_column']} from {row['parent_table']} and the key {row['referenced_column']} from {row['referenced_table']}."
            sentences.append(sentence)
        
        # Join all sentences into a single string
        documentation = "\n".join(sentences)
        return documentation

    def get_constraint_documentation(self):
        # Query the database schema for constraints
        constraints = self.run_sql("""
        SELECT 
            t.TABLE_SCHEMA,
            t.TABLE_NAME,
            c.COLUMN_NAME,
            tc.CONSTRAINT_TYPE
        FROM 
            INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tc
        JOIN 
            INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE AS ccu
            ON tc.CONSTRAINT_NAME = ccu.CONSTRAINT_NAME
        JOIN 
            INFORMATION_SCHEMA.COLUMNS AS c
            ON c.TABLE_NAME = ccu.TABLE_NAME 
            AND c.COLUMN_NAME = ccu.COLUMN_NAME
        JOIN 
            INFORMATION_SCHEMA.TABLES AS t
            ON t.TABLE_NAME = c.TABLE_NAME
        ORDER BY 
            t.TABLE_NAME, c.COLUMN_NAME;
        """)
        
        # Create a list to store the sentences
        constraint_sentences = []

        # Iterate over the DataFrame rows and create sentences
        for index, row in constraints.iterrows():
            # For each constraint, generate a sentence
            sentence = f"Table {row['TABLE_NAME']} in schema {row['TABLE_SCHEMA']} has a {row['CONSTRAINT_TYPE']} constraint on column {row['COLUMN_NAME']}."
            constraint_sentences.append(sentence)
        
        # Return the list of sentences
        return constraint_sentences

    def get_view_definitions(self):
        # Query the database to retrieve view definitions
        view_definitions = self.run_sql("""
                                    SELECT 
                                        v.name AS ViewName,
                                        m.definition,
                                        SUBSTRING(m.definition, CHARINDEX(' AS', m.definition) + 3, LEN(m.definition)) AS ViewQuery
                                    FROM 
                                        sys.views AS v
                                    JOIN 
                                        sys.sql_modules AS m 
                                        ON v.object_id = m.object_id
                                    WHERE v.name not in ('database_firewall_rules')
                                    ORDER BY 
                                        v.name;
                                        """)
        return view_definitions

    def get_stored_procedures(self):
        # Query the database to retrieve stored procedures and their definitions
        stored_procedures = self.run_sql("""
        SELECT 
            p.name AS ProcedureName,
            m.definition AS ProcedureDefinition
        FROM 
            sys.procedures AS p
        JOIN 
            sys.sql_modules AS m 
            ON p.object_id = m.object_id
        ORDER BY 
            p.name;
        """)
        
        return stored_procedures

    def create_training_plan(self, data):
        # Generate a training plan from the schema
        return self.get_training_plan_generic(data)

    def train_with_documentation(self, documentation):
        """Add business-specific documentation to training."""
        self.train(documentation=documentation)

    def train_with_sql(self, question, sql_query):
        """Add SQL queries as examples for training."""
        self.train(question=question, sql=sql_query)

    def ask_question(self, question):
        """Ask the AI model a question."""
        return self.ask(question=question)

if __name__ == "__main__":
    # Load API key and database password from environment
    openai_api_key = os.getenv("OPENAI_API_KEY")
    db_password = os.getenv("DB_PASSWORD")

    # Ensure the required environment variables are set
    if not openai_api_key or not db_password:
        raise EnvironmentError("Missing required environment variables: OPENAI_API_KEY or DB_PASSWORD.")

    # Initialize the MyVanna instance
    vn = DBAgentClass(api_key=openai_api_key, model='gpt-4o-mini', db_password=db_password)

    # Connect to the database
    vn.connect_to_database()

    # Retrieve the information schema
    df_information_schema = vn.get_information_schema()

    # Generate and inspect the training plan from the informations schema
    training_plan = vn.create_training_plan(df_information_schema)

    # Train using the generated plan
    vn.train(plan=training_plan)

    # Train with custom documentation
    # vn.train_with_documentation(
    #     documentation="Our business defines OTIF score as the percentage of orders that are delivered on time and in full."
    # )

    # Train with custom SQL query
    # vn.train_with_sql(
    #     sql_query="SELECT * FROM my-table WHERE name = 'John Doe';"
    # )

    # print("Training process completed!")
