WITH target_dois AS (
    SELECT doi as d,
           unpaywall.is_oa,
           crossref.published_year
    FROM
    {table}
WHERE crossref.published_year
    >= {start_year}
  AND crossref.published_year
    < {end_year}
    )
    , sdgs_oa AS (

SELECT *
FROM target_dois as t INNER JOIN `coki-scratch-space.curtin.doi_sdgs` as s
on d=doi
    )

SELECT published_year,
       COUNT(doi)                                         as total_outputs,
       COUNTIF(sdg_1_no_poverty)                          as sdg_1,
       COUNTIF(sdg_2_zero_hunger)                         as sdg_2,
       COUNTIF(sdg_3_health_well_being)                   as sdg_3,
       COUNTIF(sdg_4_quality_education)                   as sdg_4,
       COUNTIF(sdg_5_gender_equality)                     as sdg_5,
       COUNTIF(sdg_6_clean_water)                         as sdg_6,
       COUNTIF(sdg_7_clean_energy)                        as sdg_7,
       COUNTIF(sdg_8_decent_work)                         as sdg_8,
       COUNTIF(sdg_9_infrastructure_innovation)           as sdg_9,
       COUNTIF(sdg_10_reduced_inequalities)               as sdg_10,
       COUNTIF(sdg_11_sustainable_cities)                 as sdg_11,
       COUNTIF(sdg_12_responsible_consumption)            as sdg_12,
       COUNTIF(sdg_13_climate_action)                     as sdg_13,
       COUNTIF(sdg_14_life_below_water)                   as sdg_14,
       COUNTIF(sdg_15_life_on_land)                       as sdg_15,
       COUNTIF(sdg_16_peace_institutions)                 as sdg_16,
       COUNTIF(sdg_17_partnerships)                       as sdg_17,
       COUNTIF(is_oa)                                     as is_oa,
       COUNTIF((sdg_1_no_poverty OR sdg_2_zero_hunger OR sdg_3_health_well_being OR sdg_4_quality_education OR
       sdg_5_gender_equality OR sdg_6_clean_water OR sdg_7_clean_energy OR sdg_8_decent_work OR sdg_9_infrastructure_innovation OR
       sdg_10_reduced_inequalities OR sdg_11_sustainable_cities OR sdg_12_responsible_consumption OR sdg_13_climate_action OR sdg_14_life_below_water OR
       sdg_15_life_on_land OR sdg_16_peace_institutions OR sdg_17_partnerships)) as any_sdg,

       COUNTIF(sdg_1_no_poverty AND is_oa)                as sdg_1_oa,
       COUNTIF(sdg_2_zero_hunger AND is_oa)               as sdg_2_oa,
       COUNTIF(sdg_3_health_well_being AND is_oa)         as sdg_3_oa,
       COUNTIF(sdg_4_quality_education AND is_oa)         as sdg_4_oa,
       COUNTIF(sdg_5_gender_equality AND is_oa)           as sdg_5_oa,
       COUNTIF(sdg_6_clean_water AND is_oa)               as sdg_6_oa,
       COUNTIF(sdg_7_clean_energy AND is_oa)              as sdg_7_oa,
       COUNTIF(sdg_8_decent_work AND is_oa)               as sdg_8_oa,
       COUNTIF(sdg_9_infrastructure_innovation AND is_oa) as sdg_9_oa,
       COUNTIF(sdg_10_reduced_inequalities AND is_oa)     as sdg_10_oa,
       COUNTIF(sdg_11_sustainable_cities AND is_oa)       as sdg_11_oa,
       COUNTIF(sdg_12_responsible_consumption AND is_oa)  as sdg_12_oa,
       COUNTIF(sdg_13_climate_action AND is_oa)           as sdg_13_oa,
       COUNTIF(sdg_14_life_below_water AND is_oa)         as sdg_14_oa,
       COUNTIF(sdg_15_life_on_land AND is_oa)             as sdg_15_oa,
       COUNTIF(sdg_16_peace_institutions AND is_oa)       as sdg_16_oa,
       COUNTIF(sdg_17_partnerships AND is_oa)             as sdg_17_oa,
       COUNTIF((sdg_1_no_poverty OR sdg_2_zero_hunger OR sdg_3_health_well_being OR sdg_4_quality_education OR
       sdg_5_gender_equality OR sdg_6_clean_water OR sdg_7_clean_energy OR sdg_8_decent_work OR sdg_9_infrastructure_innovation OR
       sdg_10_reduced_inequalities OR sdg_11_sustainable_cities OR sdg_12_responsible_consumption OR sdg_13_climate_action OR sdg_14_life_below_water OR
       sdg_15_life_on_land OR sdg_16_peace_institutions OR sdg_17_partnerships) AND is_oa) as any_sdg_oa,

FROM sdgs_oa

GROUP BY published_year
ORDER BY published_year DESC