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
  COUNT(DISTINCT IF((ao.coki.oa_coki.publisher_categories.oa_journal AND (NOT diamond_oa_status.diamond OR (diamond_oa_status.diamond is null))), ao.doi, null)) as count_gold,
  COUNT(DISTINCT IF(diamond_oa_status.diamond, ao.doi, null)) as count_diamond,
  COUNT(DISTINCT IF(ao.coki.oa_coki.publisher_categories.hybrid, ao.doi, null)) as count_hybrid,
  COUNT(DISTINCT IF(ao.coki.oa_coki.other_platform_only, ao.doi, null)) as count_green,
  COUNT(DISTINCT IF(ao.coki.oa_coki.publisher_categories.no_guarantees, ao.doi, null)) as count_bronze,
  COUNT(DISTINCT IF(ao.coki.oa_coki.closed, ao.doi, null)) as count_closed,
  COUNT(DISTINCT IF(ao.coki.oa_coki.publisher_only, ao.doi, null)) as count_publisher_only,
  COUNT(DISTINCT IF(ao.coki.oa_coki.other_platform_only, ao.doi, null)) as count_other_platform_only,
  COUNT(DISTINCT IF(ao.coki.oa_coki.both, ao.doi, null)) as count_both,

  COUNT(DISTINCT ao.doi) as count_ao_total,

  COUNT(DISTINCT IF(ao.coki.oa_coki.open, ao.doi, null)) / COUNT(DISTINCT ao.doi) * 100 as pc_open

FROM
  `{doi_table}` as ao
  LEFT JOIN diamond_oa_status on ao.doi = diamond_oa_status.doi

WHERE crossref.published_year >= {start_year} and crossref.published_year < {end_year}

GROUP BY
  published_year
ORDER BY published_year ASC