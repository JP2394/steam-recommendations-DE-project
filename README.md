# Game Recommendations on Steam Project
Welcome to the Game Recommendations on Steam Project repository! This project uses advanced data engineering methods and cloud technologies to analyze game recommendations on Steam.

# Architecture Diagram

![alt text](https://github.com/JP2394/steam-Recommendations-DE-project/blob/acefa58b29425a0a81d563ce65d2ee665b010a0b/assets/architecture/steam_project.png)

# Problem 
The analysis of game recommendations data on the Steam platform has been hindered by the difficulty in handling large volumes of information in the past. The lack of robust data engineering practices has made it challenging to make informed decisions about which games should be promoted more based on their popularity and user preferences 

# Main objective
The objective of this project is to harness advanced data engineering techniques to extract, process, and analyze valuable statistics  of  games recommendations from the Steam platform

## * Some of the questions answered with the project

* How many users reviewed a game?
* What is the average playtime of a game?
* Which game was the most popular over a certain timespan?
* Which game is the most/least recommended on the platform?
* Which game has the most helpful/funny reviews? Which game has the most 
* What is the average ratio between the number of purchased games and posted reviews?


## Technologies
- **Cloud:** GCP
- **Infrastructure as code (IaC):** Terraform
- **Workflow orchestration**: Airflow (ingestion pipeline and transformation pipeline)
-   **Data Warehouse:** BigQuery
- **Data Lake:** GCS
- **Batch processing/Transformations:** dbt and DataProc/Spark 
- **Dashboard**: Google Data Studio

## Project Details

**Some of the technologies used in this project are:**

* **Google Cloud Platform**: to storage raw data in GCS (data lake) and to analyze it in BigQuery.

*  **Terraform**: Tool that provides Infraestructure as Code (IaC) to generate our resources in the cloud (buckets and datasets).

* **Airflow**: to orchestrate our data pipelines in a monthly schedule.

* **Spark**: A distributed processing engine that allows us to make complex transformations to the raw data (we mainly use the SQL API).

* **dbt**: A transformation workflow that helps compiles and runs analytics code against the data platform

## Dataset

**games_dim:** This table contains comprehensive information about games or add-ons available on the Steam platform. 

**users_dim:** This table comprises user profiles' public information, offering insights into their purchasing behavior and contribution to the platform.

**recommendations_fact:** This table captures user reviews and recommendations for products available on the Steam platform.


## Data Source

Dataset was taken from Kaggle: [game-recommendations-on-steam](https://www.kaggle.com/datasets/antonkozyriev/game-recommendations-on-steam).

 - **recommendations**
    - **File Type:** `CSV`
    - **File Size:** `2.02` GB
    - **Rows:** ` 41,154,794`

 - **games**
    - **File Type:** `CSV`
    - **File Size:** `4.86` MB
    - **Rows:** ` 50,872`

 - **users**
    - **File Type:** `CSV`
    - **File Size:** `4.86` MB
    - **Rows:** ` 14,306,064`


## Reproducibility 
>How to Recreate the Project? 

Go to the setup readme [here](/setup/README.md).


## Dashboard
You can view the dashboard [here](https://lookerstudio.google.com/reporting/2ccdf5bd-655e-4f15-9229-0dc7f072f6cb).
