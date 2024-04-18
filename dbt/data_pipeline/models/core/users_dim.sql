

{{ config(materialized='table') }}


    SELECT
       user_id
      ,products
      ,reviews
    FROM {{ source('core','users') }}