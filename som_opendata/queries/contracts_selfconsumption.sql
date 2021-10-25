SELECT
	polissa.id as id,
	MIN(modi.data_inici) as first_date,
	polissa.data_baixa as last_date,
	cups.id_municipi as city_id,
	cups.dp as postalcode,
	NULL::integer as country_id,
	TRUE
FROM giscedata_polissa AS polissa
LEFT JOIN giscedata_polissa_modcontractual AS modi
	ON polissa.id = modi.polissa_id
INNER JOIN giscedata_cups_ps AS cups
	ON polissa.cups = cups.id
WHERE
	modi.autoconsumo IS NOT NULL AND
	modi.autoconsumo != '00' AND
	TRUE
GROUP BY
	polissa.id,
	cups.id
