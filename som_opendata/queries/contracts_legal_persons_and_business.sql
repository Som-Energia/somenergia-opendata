-- Contracts having a legal entity as owner
-- or a non residential economic activity
SELECT
	polissa.id as id,
	polissa.data_alta as first_date,
	polissa.data_baixa as last_date,
	cups.id_municipi as city_id,
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
	-- ABCDEFGHJPQRSUVNW
	owner.vat like 'ESA%%' OR
	owner.vat like 'ESB%%' OR
	owner.vat like 'ESC%%' OR
	owner.vat like 'ESD%%' OR
	owner.vat like 'ESE%%' OR
	owner.vat like 'ESF%%' OR
	owner.vat like 'ESG%%' OR
	owner.vat like 'ESH%%' OR
	owner.vat like 'ESJ%%' OR
	owner.vat like 'ESP%%' OR
	owner.vat like 'ESQ%%' OR
	owner.vat like 'ESR%%' OR
	owner.vat like 'ESS%%' OR
	owner.vat like 'ESU%%' OR
	owner.vat like 'ESV%%' OR
	owner.vat like 'ESN%%' OR
	owner.vat like 'ESW%%' OR
	(
		cnae.name != '9810' AND 
		cnae.name != '9820' AND 
		TRUE
	)
ORDER BY cnae, vat
