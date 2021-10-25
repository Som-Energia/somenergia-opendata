--- All contracts
SELECT
	polissa.id as id,
	polissa.data_alta as first_date,
	polissa.data_baixa as last_date,
	cups.id_municipi as city_id,
	cups.dp as postalcode,
	NULL::integer as country_id,
	TRUE
FROM giscedata_polissa AS polissa
INNER JOIN giscedata_cups_ps AS cups
	ON polissa.cups = cups.id
--limit 10;
