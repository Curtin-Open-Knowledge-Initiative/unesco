WITH unesco_region_dois AS (
  SELECT
  regions.region,
  crossref.published_year,
  doi,
  unpaywall.is_oa
  FROM
   {table}, UNNEST(affiliations.countries) as dt
        JOIN `coki-unesco.unesco.unesco_regions` as regions on regions.country = dt.name
  WHERE crossref.published_year < 2021
AND crossref.published_year > 2009
),

regions_count AS (
  SELECT
    doi,
    published_year,
    COUNT(DISTINCT(region)) as collab_regions,
    is_oa
  FROM unesco_region_dois
  GROUP BY doi, published_year, is_oa)

SELECT
       collab_regions,
       published_year,
       COUNT(DISTINCT(IF(is_oa, doi, null))) as oa_outputs,
       COUNT(DISTINCT doi) as total_outputs,
       SAFE_DIVIDE(COUNT(DISTINCT(IF(is_oa, doi, null))),COUNT(DISTINCT doi)) * 100 as percent_oa
FROM
    regions_count
GROUP BY
    collab_regions, published_year
ORDER BY published_year DESC, collab_regions ASC

