{{ config(materialized='table') }}

SELECT  
   app_id
  ,helpful
  ,funny
  ,date
  ,is_recommended
  ,hours
  ,user_id
  ,review_id
FROM {{ source('core','recommendations') }}


