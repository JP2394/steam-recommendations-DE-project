

{{ config(materialized='view') }}


    SELECT
        app_id	
        ,title
        ,date_release	
        ,win	
        ,mac	
        ,linux	
        ,rating	
        ,user_reviews	
        ,price_original	
    FROM {{ source('staging','games') }}