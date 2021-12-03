WITH regions_table as (
    SELECT
        regions.region,
        crossref.published_year,
        unpaywall.is_oa,
        CASE WHEN unpaywall.is_oa is TRUE THEN open_citations.citations_two_years ELSE null END as oa_citations_two_year,
        CASE WHEN unpaywall.is_oa is NOT TRUE THEN open_citations.citations_two_years ELSE null END as noa_citations_two_year,
        open_citations.citations_two_years,
        doi
    FROM
        `{table}`, UNNEST(affiliations.countries) as dt
        JOIN `coki-unesco.unesco.unesco_regions` as regions on regions.country = dt.name
    WHERE
        crossref.published_year < 2021
        AND crossref.published_year > 2009
)

SELECT
       region,
       published_year,
       COUNT(DISTINCT doi) as total_outputs,
       COUNT(DISTINCT(IF(is_oa, doi, null))) as oa_outputs,
       SAFE_DIVIDE(COUNT(DISTINCT(IF(is_oa, doi, null))),COUNT(DISTINCT doi)) * 100 as percent_oa,
       AVG(oa_citations_two_year) as avg_oa_citations_two_years,
       AVG(noa_citations_two_year) as avg_noa_citations_two_years

FROM (SELECT DISTINCT * from regions_table)

GROUP BY published_year, region
ORDER BY published_year DESC, region ASC