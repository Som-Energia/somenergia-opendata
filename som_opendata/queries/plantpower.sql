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
		plant_nominal_power_kw as value,
		connection_date as first_date,
		end_date as last_date
	FROM dbt_prod.dm_plants__opendata
) AS item
LEFT JOIN municipality AS city
ON item.city_id = city.id
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

