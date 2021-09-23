SELECT
	partner.id AS id,
	partner.date AS first_date,
	member.data_baixa_soci AS last_date,
	address.country_id AS country_id,
	address.id_municipi AS city_id,
	address.city AS city_name,
	partner.name AS name, -- debug only
	TRUE
FROM res_partner AS partner
INNER JOIN somenergia_soci AS member
ON partner.id = member.partner_id
LEFT JOIN (
	SELECT
		ROW_NUMBER() OVER (
			PARTITION BY partner_id
			ORDER BY COALESCE(id_municipi, country_id) IS Not NULL DESC, address.id
		) AS order,
		address.id,
		address.country_id,
		address.partner_id,
		address.id_municipi,
		address.city
	FROM res_partner_address as address
	WHERE address.active = TRUE
	AND COALESCE(address.id_municipi, address.country_id) IS NOT NULL
) AS address
ON address.partner_id = partner.id
AND address.order = 1
WHERE
	-- PQS
	partner.vat like 'ESP%%' OR
	partner.vat like 'ESQ%%' OR
	partner.vat like 'ESS%%' OR
FALSE
ORDER BY partner.id
