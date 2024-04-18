

  create or replace view `de-data-jobs`.`dbt_dw`.`my_second_dbt_model`
  OPTIONS()
  as -- Use the `ref` function to select from other models

select *
from `de-data-jobs`.`dbt_dw`.`my_first_dbt_model`
where id = 1;

