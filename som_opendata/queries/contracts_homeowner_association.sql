-- Contracts having a legal entity as owner
-- or a non residential economic activity
SELECT
	polissa.id as id,
	polissa.data_alta as first_date,
	polissa.data_baixa as last_date,
	cups.id_municipi as city_id,
	NULL::integer as country_id,
	cups.dp as postalcode,
	owner.vat as vat,
	cnae.name as cnae,
	TRUE
FROM giscedata_polissa AS polissa
INNER JOIN giscedata_cups_ps AS cups
	ON polissa.cups = cups.id
LEFT JOIN res_partner AS owner
ON owner.id = polissa.titular
LEFT JOIN giscemisc_cnae AS cnae
ON cnae.id = polissa.cnae
WHERE
	owner.vat like 'ESH%%'
ORDER BY cnae, vat
