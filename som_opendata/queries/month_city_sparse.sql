--- This query scheleton is not currently used but
--- is keept as reference just in case we need the
--- unrolled data instead the one we are taking now
--- in month_city_distribution
SELECT
	thedate AS thedate,
	pais.code AS codi_pais,
	pais.name AS pais,
	comunitat.codi AS codi_ccaa,
	comunitat.name AS comunitat_autonoma,
	provincia.code AS codi_provincia,
	provincia.name AS provincia,
	municipi.ine AS codi_ine,
	municipi.name AS municipi,
	count(CASE
		WHEN item_first_date IS NULL THEN NULL
		WHEN item.first_date > thedate THEN NULL
		WHEN item.last_date is NULL then item.id::text
		WHEN item.last_date > thedate THEN item.id::text
		ELSE NULL
		END) AS quants,
	string_agg(CASE
		WHEN item.first_date IS NULL THEN NULL
		WHEN item.first_date > thedate THEN NULL
		WHEN item.last_date is NULL then item.id::text
		WHEN item.last_date > thedate THEN item.id::text
		ELSE NULL
		END, ',' ORDER BY item.id) AS ids
FROM (
{}
) AS item
LEFT JOIN unnest({}) AS thedate
	ON TRUE
LEFT JOIN res_municipi AS municipi
	ON item.city_id=municipi.id
LEFT JOIN res_country_state AS provincia
	ON provincia.id = municipi.state
LEFT JOIN res_comunitat_autonoma AS comunitat
	ON comunitat.id = provincia.comunitat_autonoma
LEFT JOIN res_country AS pais
	ON pais.id = provincia.country_id
GROUP BY
	thedate,
	codi_pais,
	codi_ccaa,
	codi_provincia,
	codi_ine,
	pais,
	provincia,
	municipi,
	comunitat.name
ORDER BY
	pais ASC,
	comunitat_autonoma ASC,
	provincia ASC,
	municipi ASC,
	thedate ASC,
	0 ASC
;
