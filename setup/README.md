## Environment Setup

###  1 - SSH Keys creation
Check https://cloud.google.com/compute/docs/connect/create-ssh-keys . 
More specifically,
- `Linux and macOS`: https://cloud.google.com/compute/docs/connect/create-ssh-keys#linux-and-macos 
- `Windows`: https://cloud.google.com/compute/docs/connect/create-ssh-keys#windows-10-or-later

If you have gitbash, ssh-keygen command is supported. 
- Create .ssh folder under user folder 
  - Windows: C:\USERS\YOUR_USER_NAME
  - Linux: ~
- Run the command: 

  - Linux/gitbash  `ssh-keygen -t rsa -f ~/.ssh/YOUR_USER_NAME -C YOUR_USER_NAME -b 2048`
  - Windows `ssh-keygen -t rsa -f C:\USERS\YOUR_USER_NAME\.ssh\KEY_FILENAME -C YOUR_USER_NAME -b 2048`

This will generate public and private keys.
Go to Compute Engine: https://console.cloud.google.com/compute and add the public key (KEY_FILENAME.pub).
`GCP->Compute Engine->Metadata->ssh-keys->Add key`


###  2 - VM instance creation
`GCP->Compute Engine->VM instances->Create instance`
`e2-standard-4`
`Ubuntu 20.14LTS 50GB`
`16 GB RAM`

###  3 - Creation project and services account
Create a project called `de-data-steam-recommendations` in GCP and create a *Service Account* with these permissions:
- `BigQuery Admin`
- `Storage Admin`
- `Services Account User`
- `Dataproc Administrator`
- `Looker Admin`

Download the Service Account json file, rename it to `google_credentials.json` and store it in `$HOME/.google/credentials/` .

Also make sure that these APIs are activated:
* https://console.cloud.google.com/apis/library/iam.googleapis.com
* https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com

## 4 - GCP authentication
Perform de authentication:  
`gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS`  



## 5 - Clone repo in vm instance.
   ```
     git clone steam-Recommendations-DE-project.git
   ```
   ```
     cd steam-recommendations-DE-project
   ```

## 5 - Execute the setup.vm
cd into `setup` to execute the setup_vm.sh script:
- Make the vm_setup executable with the following commnands.
 ```
   chmod +x setup_vm.sh
 ```
- run the executable to install all the neccesary components for the vm.
 ```
 ./setup.vm
 ```

## 6 - Deploy resources with terraform
cd into `terraform` to create the resources on the cloud (bucket, bigquery dataset):

* **Initialize terraform**:
	```sh
	 terraform init
* **Check that you're creating the correct resources (GCS bucket and BigQuery dataset)**:
    ```sh
    terraform plan
    ```
* **Create the resources**:
    ```sh
    terraform apply <your-project-id>
    ```

## 7 - Generate kaggle api token 
Go to kaggle page:
* https://www.kaggle.com/settings
* On the api section generate a token to use it on the .env file inside the airflow-dev
* The token will allow airflow to download the dataset from kaggle
```
     ENV KAGGLE_USERNAME= <the username of the token>
     ENV KAGGLE_KEY= <key of the token>
   ```

## 8 - Initialize (Astronomer) apache airflow
```
     cd airflow-dev
   ```
```
     astro dev start
   ```
     
Now Airflow running on 8080 port, so can forward it and open in browser at localhost:8080.

   `Trigger the following Dag manually from Airflow's UI.:` 1_dag_master

master will run the following dags automatically:
*  `2_dag_kaggle_to_gcs`
*   `3_dag_pyspark_submit`
*   `4_parquet_to_bigquery`
*   `5_dbt_run`

For more detailed information on the processes in Apache Airflow, click [here](https://github.com/technomonah/CSSE_data_de/blob/main/prereqs-setup.md).

