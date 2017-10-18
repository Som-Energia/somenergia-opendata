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
		WHEN polissa.data_alta IS NULL THEN NULL
		WHEN polissa.data_alta > thedate THEN NULL
		WHEN polissa.data_baixa is NULL then polissa.id::text
		WHEN polissa.data_baixa > thedate THEN polissa.id::text
		ELSE NULL
		END) AS quants,
	string_agg(CASE
		WHEN polissa.data_alta IS NULL THEN NULL
		WHEN polissa.data_alta > thedate THEN NULL
		WHEN polissa.data_baixa is NULL then polissa.id::text
		WHEN polissa.data_baixa > thedate THEN polissa.id::text
		ELSE NULL
		END, ',' ORDER BY polissa.id) AS ids
FROM giscedata_polissa polissa
LEFT JOIN unnest(%(dates)s) AS thedate
	ON TRUE
LEFT JOIN res_partner rp
	ON rp.id = polissa.soci
INNER JOIN giscedata_cups_ps AS cups
	ON polissa.cups = cups.id
LEFT JOIN res_municipi AS municipi
	ON cups.id_municipi=municipi.id
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
	TRUE ASC
;
