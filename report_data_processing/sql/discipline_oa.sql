WITH diamond_oa_status AS (
  SELECT
    doi,
    MAX(academic_observatory.coki.oa_color.gold_just_doaj AND (doaj.apc = FALSE)) as diamond

    FROM
      `{doi_table}` as academic_observatory
      LEFT JOIN `utrecht-university.doaj.apc_issnl_20220427` as doaj on doaj.journal_issn_l = academic_observatory.unpaywall.journal_issn_l

    WHERE crossref.published_year >= {start_year} and crossref.published_year < {end_year}
    GROUP BY doi
)

SELECT
  ao.crossref.published_year,
  concept.display_name,
  COUNT(DISTINCT IF((ao.coki.oa_coki.publisher_categories.oa_journal AND (NOT diamond_oa_status.diamond OR (diamond_oa_status.diamond is null))), ao.doi, null)) as gold,
  COUNT(DISTINCT IF(diamond_oa_status.diamond, ao.doi, null)) as diamond,
  COUNT(DISTINCT IF(ao.coki.oa_coki.publisher_categories.hybrid, ao.doi, null)) as hybrid,
  COUNT(DISTINCT IF(ao.coki.oa_coki.other_platform_only, ao.doi, null)) as green,
  COUNT(DISTINCT IF(ao.coki.oa_coki.publisher_categories.no_guarantees, ao.doi, null)) as bronze,
  COUNT(DISTINCT IF(ao.coki.oa_coki.publisher_only, ao.doi, null)) as publisher_only,
  COUNT(DISTINCT IF(ao.coki.oa_coki.other_platform_only, ao.doi, null)) as other_platform_only,
  COUNT(DISTINCT IF(ao.coki.oa_coki.both, ao.doi, null)) as both,
  COUNT(DISTINCT IF(ao.coki.oa_coki.closed, ao.doi, null)) as closed,
  COUNT(DISTINCT ao.doi) as total_outputs
FROM `{doi_table}` as ao, UNNEST (openalex.concepts) as concept
    JOIN diamond_oa_status on ao.doi = diamond_oa_status.doi
WHERE concept.level=0 and crossref.published_year >= {start_year} and crossref.published_year < {end_year}
GROUP BY crossref.published_year, concept.display_name
ORDER BY concept.display_name ASC