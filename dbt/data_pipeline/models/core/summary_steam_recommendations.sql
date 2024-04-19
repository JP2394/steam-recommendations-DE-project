
{{
    config(
        materialized='table'
    )
}}

with games_recommendations
as(
         
         select *
         from
         {{ ref('stg_games_dim') }} games
         left join 
         {{ ref('stg_recommendations_fact') }}  recommendations
        on games.app_id =recommendations.app_id 

)

     SELECT 
        title
        ,EXTRACT(YEAR FROM max(date_release)) AS release_year 
        ,SUM(case when is_recommended = true then 1 else 0 end) AS recommended
        ,SUM(case when is_recommended = false then 1 else 0 end) AS not_recommended
        ,SUM(ifnull(funny,0)) as funny_games
        ,SUM(ifnull(helpful,0)) as helpful_games
        ,FORMAT('%0.2f', ROUND(SUM(ifnull(hours,0)), 2)) as hours_played 
        ,FORMAT('%0.2f',  ROUND(AVG(ifnull(hours,0)), 2)) as average_played_times
        ,MAX(user_reviews) as total_reviews
    from  games_recommendations
    group by title
    
    