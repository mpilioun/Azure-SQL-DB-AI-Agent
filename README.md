# Database Agent with RAG and LLMs on Azure SQL Metadata

## Overview

This project implements a **Azure SQL Database Agent** powered by **Retrieval-Augmented Generation (RAG)** and **Large Language Models (LLMs)**, which allows users to conduct advanced queries on Azure SQL Database metadata. The agent uses the **Vanna.AI** library for intelligent query generation and processing. It is designed to help developers, data scientists, and database administrators interact with and explore Azure SQL databases efficiently.

## Features

- **Metadata Retrieval**: The agent is initially trained on Azure SQL Database metadata to extract detailed insights from the database schema.
- **RAG Integration**: Combines information retrieval techniques with large language models to enhance query accuracy and relevance.
- **Vanna.AI Library**: Utilizes the Vanna.AI library for robust query generation and processing.
- **Dynamic Query Execution**: Supports a wide range of SQL queries, from basic to advanced analytics.
- **Dynamic Plot Creation**: Supports teh creation of metrics shown as cisualization.
- **User-Friendly Interface**: Provides a natural language interface to ask questions about the database and retrieve relevant information.


## Quick Start Guide 🏃‍♂️

### Prerequisites 📋

Before running the application, you'll need:

1. **API Keys**
   - OpenAI API key with sufficient credits

2. **Python Environment**
   - Python 3.9 or higher
   - pip package manager

Note: All API keys should be stored in your `.env` file. See the Configuration section below for details.

### Installation 🛠️

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/database-agent.git
   ```
2. **Set up virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   - Copy `.env_sample` to `.env`
   - Add your configuration values
   - Get your Azzure SQL Database ODBC string (I use SQL auhentication method)
   - Custome the connection part for different connection methods

### Running the Application 🚀

1. **Initialize VectorStore**
   Manually run the file metadata_training.py once

2. **Start Database QnA**
   Manually run the file app.py and use your localholst url to query the database

## Tips

 - While using the QnA Frontend app. If you ask a question and the query/answer generated are correct. Click to add it in the training database.
 - The better your database is structured in terms of metadata (comments on column, fk relationships, constraints) the better the performance
 - THe mroe you use it correctly (i.e. add correct queries to training database) the smarter it becomes

## 🪪 License

This project is licensed under the MIT License. See the LICENSE file for more details.