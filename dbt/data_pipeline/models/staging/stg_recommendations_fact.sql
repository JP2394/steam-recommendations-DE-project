{{ config(materialized='view') }}

SELECT  
   app_id
  ,helpful
  ,funny
  ,date
  ,is_recommended
  ,hours
  ,user_id
  ,review_id
FROM {{ source('staging','recommendations') }}


