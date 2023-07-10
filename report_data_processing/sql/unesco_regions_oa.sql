WITH diamond_oa_status AS (
  SELECT
    doi,
    MAX(academic_observatory.coki.oa_color.gold_just_doaj AND (doaj.apc = FALSE)) as diamond

    FROM
      `{doi_table}` as academic_observatory
      LEFT JOIN `utrecht-university.doaj.apc_issnl_20220427` as doaj on doaj.journal_issn_l = academic_observatory.unpaywall.journal_issn_l
    GROUP BY doi
),

    regions_table as (
    SELECT
        doi,
        regions.region,
    FROM
        `{doi_table}`, UNNEST(affiliations.countries) as affs
        JOIN `coki-unesco.unesco.unesco_regions` as regions on regions.country = affs.name
)

SELECT
  region,
  crossref.published_year,
  COUNT(DISTINCT IF((ao.coki.oa_coki.publisher_categories.oa_journal AND (NOT diamond.diamond OR (diamond.diamond is null))), ao.doi, null)) as count_gold,
  COUNT(DISTINCT IF(diamond.diamond, ao.doi, null)) as count_diamond,
  COUNT(DISTINCT IF(ao.coki.oa_coki.publisher_categories.hybrid, ao.doi, null)) as count_hybrid,
  COUNT(DISTINCT IF(ao.coki.oa_coki.publisher_categories.no_guarantees, ao.doi, null)) as count_bronze,
  COUNT(DISTINCT IF(ao.coki.oa_coki.closed, ao.doi, null)) as count_closed,
  COUNT(DISTINCT IF(ao.coki.oa_coki.publisher_only, ao.doi, null)) as count_publisher_only,
  COUNT(DISTINCT IF(ao.coki.oa_coki.other_platform_only, ao.doi, null)) as count_other_platform_only,
  COUNT(DISTINCT IF(ao.coki.oa_coki.both, ao.doi, null)) as count_both,
  COUNT(DISTINCT IF(ao.coki.oa_coki.open, ao.doi, null)) as count_open,
  COUNT(DISTINCT ao.doi) as count_ao_total

FROM `{doi_table}` as ao
     LEFT JOIN regions_table as regions on ao.doi=regions.doi
     LEFT JOIN diamond_oa_status as diamond on ao.doi=diamond.doi

WHERE crossref.published_year >= {start_year} and crossref.published_year < {end_year}

GROUP BY published_year, region
ORDER BY published_year DESC, region ASC