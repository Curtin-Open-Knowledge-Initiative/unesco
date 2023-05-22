WITH oa_status AS (
  SELECT
    doi,
    crossref.published_year,
    academic_observatory.coki.oa_color.gold_just_doaj AND (doaj.apc != FALSE) as gold,
    academic_observatory.coki.oa_color.gold_just_doaj AND (doaj.apc = FALSE) as diamond,
    academic_observatory.coki.oa_color.hybrid as hybrid,
    academic_observatory.coki.oa_color.green_only as green,
    academic_observatory.coki.oa_color.bronze as bronze,
    academic_observatory.coki.oa_coki.closed as closed,
    academic_observatory.coki.oa_coki.open as open,
    academic_observatory.coki.oa_coki.publisher_only as publisher_only_open,
    academic_observatory.coki.oa_coki.other_platform_only as other_platform_only_open,
    academic_observatory.coki.oa_coki.both as both_open

    FROM

      `{doi_table}` as academic_observatory
      LEFT JOIN `utrecht-university.doaj.apc_issnl_20220427` as doaj on doaj.journal_issn_l = academic_observatory.unpaywall.journal_issn_l

    WHERE crossref.published_year >= {start_year} and crossref.published_year < {end_year}
)

SELECT
  published_year,
  COUNTIF(gold) as count_gold,
  COUNTIF(diamond) as count_diamond,
  COUNTIF(hybrid) as count_hybrid,
  COUNTIF(green) as count_green,
  COUNTIF(bronze) as count_bronze,
  COUNTIF(closed) as count_closed,
  COUNTIF(publisher_only_open) as count_publisher_only,
  COUNTIF(other_platform_only_open) as count_other_platform_only,
  COUNTIF(both_open) as count_both,

  COUNT(DISTINCT doi) as count_ao_total,

  COUNTIF(open) / COUNT(DISTINCT doi) * 100 as pc_open

FROM
  oa_status

GROUP BY
  published_year
ORDER BY published_year ASC