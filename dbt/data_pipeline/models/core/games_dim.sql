

{{ config(materialized='table') }}


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
    FROM {{ source('core','games') }}