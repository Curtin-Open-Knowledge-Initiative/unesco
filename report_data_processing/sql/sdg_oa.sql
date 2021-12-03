WITH target_dois AS (
    SELECT doi as d,
           unpaywall.is_oa,
           crossref.published_year
    FROM
    {table}
WHERE crossref.published_year
    > 2009
  AND crossref.published_year
    < 2021
    )
    , sdgs_oa AS (

SELECT *
FROM target_dois as t INNER JOIN `coki-scratch-space.curtin.doi_sdgs` as s
on d=doi
    )

SELECT published_year,
       COUNT(doi)                                         as total_outputs,
       COUNTIF(sdg_1_no_poverty)                          as sdg_1_no_poverty,
       COUNTIF(sdg_2_zero_hunger)                         as sdg_2_zero_hunger,
       COUNTIF(sdg_3_health_well_being)                   as sdg_3_health_well_being,
       COUNTIF(sdg_4_quality_education)                   as sdg_4_quality_education,
       COUNTIF(sdg_5_gender_equality)                     as sdg_5_gender_equality,
       COUNTIF(sdg_6_clean_water)                         as sdg_6_clean_water,
       COUNTIF(sdg_7_clean_energy)                        as sdg_7_clean_energy,
       COUNTIF(sdg_8_decent_work)                         as sdg_8_decent_work,
       COUNTIF(sdg_9_infrastructure_innovation)           as sdg_9_infrastructure_innovation,
       COUNTIF(sdg_10_reduced_inequalities)               as sdg_10_reduced_inequalities,
       COUNTIF(sdg_11_sustainable_cities)                 as sdg_11_sustainable_cities,
       COUNTIF(sdg_12_responsible_consumption)            as sdg_12_responsible_consumption,
       COUNTIF(sdg_13_climate_action)                     as sdg_13_climate_action,
       COUNTIF(sdg_14_life_below_water)                   as sdg_14_life_below_water,
       COUNTIF(sdg_15_life_on_land)                       as sdg_15_life_on_land,
       COUNTIF(sdg_16_peace_institutions)                 as sdg_16_peace_institutions,
       COUNTIF(sdg_17_partnerships)                       as sdg_17_partnerships,
       COUNTIF(is_oa)                                     as is_oa,
       COUNTIF(sdgs_ref_in_title_abs)                     as sdgs_ref_in_title_abs,
       COUNTIF((sdg_1_no_poverty OR sdg_2_zero_hunger OR sdg_3_health_well_being OR sdg_4_quality_education OR
       sdg_5_gender_equality OR sdg_6_clean_water OR sdg_7_clean_energy OR sdg_8_decent_work OR sdg_9_infrastructure_innovation OR
       sdg_10_reduced_inequalities OR sdg_11_sustainable_cities OR sdg_12_responsible_consumption OR sdg_13_climate_action OR sdg_14_life_below_water OR
       sdg_15_life_on_land OR sdg_16_peace_institutions OR sdg_17_partnerships)) as any_sdg,

       COUNTIF(sdg_1_no_poverty AND is_oa)                as sdg_1_no_poverty_oa,
       COUNTIF(sdg_2_zero_hunger AND is_oa)               as sdg_2_zero_hunger_oa,
       COUNTIF(sdg_3_health_well_being AND is_oa)         as sdg_3_health_well_being_oa,
       COUNTIF(sdg_4_quality_education AND is_oa)         as sdg_4_quality_education_oa,
       COUNTIF(sdg_5_gender_equality AND is_oa)           as sdg_5_gender_equality_oa,
       COUNTIF(sdg_6_clean_water AND is_oa)               as sdg_6_clean_water_oa,
       COUNTIF(sdg_7_clean_energy AND is_oa)              as sdg_7_clean_energy_oa,
       COUNTIF(sdg_8_decent_work AND is_oa)               as sdg_8_decent_work_oa,
       COUNTIF(sdg_9_infrastructure_innovation AND is_oa) as sdg_9_infrastructure_innovation_oa,
       COUNTIF(sdg_10_reduced_inequalities AND is_oa)     as sdg_10_reduced_inequalities_oa,
       COUNTIF(sdg_11_sustainable_cities AND is_oa)       as sdg_11_sustainable_cities_oa,
       COUNTIF(sdg_12_responsible_consumption AND is_oa)  as sdg_12_responsible_consumption_oa,
       COUNTIF(sdg_13_climate_action AND is_oa)           as sdg_13_climate_action_oa,
       COUNTIF(sdg_14_life_below_water AND is_oa)         as sdg_14_life_below_water_oa,
       COUNTIF(sdg_15_life_on_land AND is_oa)             as sdg_15_life_on_land_oa,
       COUNTIF(sdg_16_peace_institutions AND is_oa)       as sdg_16_peace_institutions_oa,
       COUNTIF(sdg_17_partnerships AND is_oa)             as sdg_17_partnerships_oa,
       COUNTIF(sdgs_ref_in_title_abs AND is_oa) as sdgs_ref_in_title_abs_oa,
       COUNTIF((sdg_1_no_poverty OR sdg_2_zero_hunger OR sdg_3_health_well_being OR sdg_4_quality_education OR
       sdg_5_gender_equality OR sdg_6_clean_water OR sdg_7_clean_energy OR sdg_8_decent_work OR sdg_9_infrastructure_innovation OR
       sdg_10_reduced_inequalities OR sdg_11_sustainable_cities OR sdg_12_responsible_consumption OR sdg_13_climate_action OR sdg_14_life_below_water OR
       sdg_15_life_on_land OR sdg_16_peace_institutions OR sdg_17_partnerships) AND is_oa) as any_sdg_oa,

FROM sdgs_oa

GROUP BY published_year
ORDER BY published_year DESC