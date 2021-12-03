SELECT
       regions.region as region,
       crossref.published_year,
       COUNT(DISTINCT(IF(unpaywall.is_oa, doi, null))) as oa_outputs,
       COUNT(DISTINCT doi) as total_outputs,
       SAFE_DIVIDE(COUNT(DISTINCT(IF(unpaywall.is_oa, doi, null))),COUNT(DISTINCT doi)) * 100 as percent_oa
FROM {table}, UNNEST(affiliations.countries) as dt
        JOIN `coki-unesco.unesco.unesco_regions` as regions on regions.country = dt.name
WHERE crossref.published_year < 2021
AND crossref.published_year > 2009

GROUP BY crossref.published_year, region
ORDER BY crossref.published_year DESC