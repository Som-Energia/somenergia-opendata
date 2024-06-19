SELECT
	city.countrycode AS codi_pais,
	city.country AS pais,
	city.regioncode AS codi_ccaa,
	city.region AS comunitat_autonoma,
	city.provincecode AS codi_provincia,
	city.province AS provincia,
	city.inecode AS codi_ine,
	city.name AS municipi,
	{} -- here go the count columns
FROM (
	SELECT
		params.nominal_power_w / 1000 as value,
		params.connection_date as first_date,
		null::date as last_date,
		plant.municipality as city_id
	FROM plant
	LEFT JOIN plantparameters AS params
	ON params.plant = plant.id
	WHERE plant.description != 'SomRenovables'
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
	municipi ASC,
	0 ASC
;

