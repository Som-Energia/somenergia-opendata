SELECT
	codi_pais,
	pais,
	codi_ccaa,
	comunitat_autonoma,
	codi_provincia,
	provincia,
	codi_ine,
	municipi,
	{} -- here go the count columns
FROM (
	SELECT
		codi_pais,
		pais,
		codi_ccaa,
		comunitat_autonoma,
		codi_provincia,
		provincia,
		codi_ine,
		municipi,
		energia_exportada_kwh as value,
		month as time
	FROM dbt_prod.dm_plant_production_monthly__opendata
) AS item
GROUP BY
	codi_pais,
	codi_ccaa,
	codi_provincia,
	codi_ine,
	pais,
	provincia,
	municipi,
	comunitat_autonoma
ORDER BY
	pais ASC,
	comunitat_autonoma ASC,
	provincia ASC,
	municipi ASC
;
