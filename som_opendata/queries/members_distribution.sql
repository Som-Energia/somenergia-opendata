SELECT
    codi_pais,
    pais,
    codi_ccaa,
    comunitat_autonoma,
    codi_provincia,
    provincia,
    codi_ine,
    municipi,
    {}
FROM (
    SELECT
        m.name AS municipi,
        p.ref AS num_soci,
        p.vat AS nif,
        pa.email AS email,
        pa.name AS nom,
        prov.name AS provincia,
        pa.zip AS codi_postal,
        p.lang AS idioma,
        com.name AS comarca,
        ccaa.name AS comunitat_autonoma,
        country.name AS pais,
        p.id AS id,
        m.id AS id_municipi,
        m.ine AS codi_ine,
        prov.code AS codi_provincia,
        ccaa.codi AS codi_ccaa,
        country.code AS codi_pais,
        address.partner_id AS partner_id,
        p.date as first_date,
        pa.active as active,
        ss.data_baixa_soci as last_date
    FROM res_partner_address AS pa
    JOIN (
        SELECT
            address.partner_id,
            MIN(address.id) AS id_unic
        FROM
            res_partner_address as address
        WHERE
            address.active
        GROUP BY address.partner_id
        ) AS address ON address.id_unic = pa.id
    LEFT JOIN res_partner AS p ON (p.id=pa.partner_id)
    LEFT JOIN res_municipi AS m ON (m.id=pa.id_municipi)
    LEFT JOIN res_country_state AS prov ON (prov.id=pa.state_id)
    LEFT JOIN res_comunitat_autonoma AS ccaa ON (ccaa.id=prov.comunitat_autonoma)
    LEFT JOIN res_comarca AS com ON (com.id=m.comarca)
    LEFT JOIN res_country AS country ON (country.id=pa.country_id)
    JOIN somenergia_soci as ss on (ss.partner_id=p.id)
    ORDER BY p.ref
) AS item
GROUP BY
    codi_pais,
    codi_ccaa,
    codi_provincia,
    codi_ine,
    pais,
    provincia,
    municipi,
    comunitat_autonoma,
    TRUE
ORDER BY
    pais ASC,
    comunitat_autonoma ASC,
    provincia ASC,
    municipi ASC,
    0 ASC;

