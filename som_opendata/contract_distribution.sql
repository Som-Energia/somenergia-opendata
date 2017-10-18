SELECT
	pais.code AS codi_pais,
	pais.name AS pais, 
	comunitat.codi AS codi_ccaa, 
	comunitat.name AS comunitat_autonoma, 
	provincia.code AS codi_provincia, 
	provincia.name AS provincia, 
	municipi.ine AS codi_ine, 
	municipi.name AS municipi, 
	{} -- here go the count columns
FROM giscedata_polissa polissa
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
	TRUE ASC
;
