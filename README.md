# CCC181-SSIS

Welcome to my project for **CCC181 - Application Development and Emerging Technologies**! This is a Simple Student Information System (SSIS) built with a Python Flask backend and a responsive **Bootstrap** frontend. It's designed to manage student, program, and college data efficiently.

***

## ✨ Core Functionality

* **User Authentication:** A secure login system for managing access.
* **Full CRUDL:** You can Create, Read, Update, Delete, and List all entries for students, programs, and colleges.
* **Advanced Data Tools:** I've implemented searching, sorting, and pagination to handle large amounts of data easily.
* **PostgreSQL Database:** All data is stored in a robust PostgreSQL database with defined relationships.
* **Hybrid Storage Solution:** Student profile pictures are stored securely in Supabase Cloud Storage, keeping the main PostgreSQL database fast and efficient.
* **Demo Data Included:** The database comes fully loaded with over 350 student records, 50 different programs, and 10 colleges so you can begin testing features immediately. The complete setup script, `PostgreSQL_schema.sql`, is included in this repository.

***

## 📚 Database Schema

I've designed the database with four main tables: `users`, `colleges`, `programs`, and `students`. The structure uses foreign key constraints to ensure data integrity.

#### `users` table

| Column   | Type           | Constraints                  |
| :------- | :------------- | :--------------------------- |
| `id`     | `SERIAL`       | **Primary Key** |
| `username` | `VARCHAR(100)` | `NOT NULL`, `UNIQUE`         |
| `email`    | `VARCHAR(150)` | `NOT NULL`, `UNIQUE`         |
| `password` | `VARCHAR(100)` | `NOT NULL`                   |

#### `colleges` table

| Column       | Type           | Constraints     |
| :----------- | :------------- | :-------------- |
| `college_code` | `VARCHAR(10)`  | **Primary Key** |
| `college_name` | `VARCHAR(100)` | `NOT NULL`      |

#### `programs` table

| Column         | Type           | Constraints                                |
| :------------- | :------------- | :----------------------------------------- |
| `program_code` | `VARCHAR(10)`  | **Primary Key** |
| `program_name` | `VARCHAR(100)` | `NOT NULL`                                 |
| `college_code` | `VARCHAR(10)`  | **Foreign Key** to `colleges(college_code)`|

* **Relationship:** `ON UPDATE CASCADE` and `ON DELETE SET NULL`. If a college code changes, it updates here. If a college is deleted, this field becomes null.

#### `students` table

| Column       | Type          | Constraints                                |
| :----------- | :------------ | :----------------------------------------- |
| `id_number`  | `VARCHAR(12)` | **Primary Key** |
| `first_name` | `VARCHAR(50)` | `NOT NULL`                                 |
| `last_name`  | `VARCHAR(50)` | `NOT NULL`                                 |
| `gender`     | `VARCHAR(10)` | `NOT NULL`, `CHECK ('Male', 'Female')`     |
| `year_level` | `SMALLINT`    | `NOT NULL`                                 |
| `program_code` | `VARCHAR(10)` | **Foreign Key** to `programs(program_code)`|
| `profile_picture_url` | `VARCHAR(255)` | `DEFAULT 'default_avatar.png`|

* **Relationship:** `ON UPDATE CASCADE` and `ON DELETE SET NULL`. Behavior is similar to the programs-colleges link.

***

## 🛠️ Getting Your Local Setup Ready

To get the project running, you only need to create a single **`.env`** file to hold your database credentials and secret key.

1.  **Create your `.env` file** in the project's root directory:
    ```powershell
    New-Item .env -ItemType File
    ```

2.  **Edit your new `.env` file** and add your specific database details. This file should be included in your `.gitignore` to keep your credentials private.

    ```env
    # A random, secret string for Flask sessions
    SECRET_KEY="your_super_secret_and_random_key_here"

    # Your local PostgreSQL database connection details
    DB_NAME="ssis_db"
    DB_USER="postgres"
    DB_PASSWORD="your_secure_password"
    DB_HOST="localhost"
    DB_PORT="5432"

    SUPABASE_URL=
    SUPABASE_KEY=
    SUPABASE_BUCKET=
    ```
    Your `config.py` is already set up to read these settings directly from this file.

***
3. **Set up Supabase Storage**
<br>Before launching the app, you must configure the cloud storage container and upload the default placeholder image.

 - **Create the Bucket**  
      In your Supabase Dashboard, go to **Storage** and create a new public bucket named `student_profile`.

- **Upload Default Avatar**  
      Upload your placeholder image file, `default_avatar.png`, directly to the root of the `student_profile` bucket.  
      This ensures all new records have a working image URL, matching the DEFAULT constraint in your database schema.

🚀 Installation and Running the App
-----------------------------------

Follow these three steps to get the application up and running.

### 1\. 🗄️ Set up the Database with pgAdmin

Before running the app, you need to create the database and then load the schema and data using the provided SQL file.

1.  **Create the Database:**

    -   In **pgAdmin**, connect to your server.

    -   Right-click on **Databases** and select **Create** -> **Database...**

    -   Name your database (e.g., `ssis_db`). **Important:** This name must exactly match the `DB_NAME` in your `.env` file.

2.  **Load the Schema and Data:**

    -   Select your new database (`ssis_db`) from the server tree.

    -   Open the **Query Tool** by clicking the `<>SQL` icon in the toolbar.

    -   In the Query Tool window, click the **Open File** icon (it looks like a folder).

    -   Navigate to and select the `PostgreSQL_schema.sql` file from this repository.

    -   Once the script is loaded, click the **Execute/Run** icon (it looks like a lightning bolt ⚡) to create all tables and populate them with the sample data.

### 2\. 🐍 Prepare the Python Environment

With the database ready, the next step is to set up the Python environment and install the required packages.

1.  **Install Pipenv** (if you don't have it already):

    ```
    pip install pipenv

    ```

2.  **Create and Activate the Virtual Environment**: Navigate to the project's root directory (the same one that contains the `Pipfile`) and run:

    ```
    # This command creates a new virtual environment and activates it.
    pipenv shell

    ```

3.  **Install Project Dependencies**: Once the shell is active, install all the required packages from the `Pipfile`:

    ```
    pipenv install

    ```

### 3\. ▶️ Launch the Application

Once your database is set up and the virtual environment is active, you're ready to start the server.

Just run this single command:

```
# This starts the Flask development server.
flask run

```

You should see output in your terminal indicating the server is running, typically on `http://127.0.0.1:5000`.

That's it! Fire up your web browser and navigate to that address to see the SSIS application live.

