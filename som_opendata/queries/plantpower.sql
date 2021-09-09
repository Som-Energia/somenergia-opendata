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
FROM (
	select
		first_date,
		null::date as last_date,
		city.id as city_id,
		--plant.city_code as plant_ine,
		--city.ine as city_code,
		--city.name,
		--registry.description,
		--registry.name,
		--registry.*,
		nominal_power_kw as value
	from (
	values
		('25120','2012-01-01'::date,'Lleida',         '388828084',   99,  104),
		('17148','2012-01-01'::date,'Riudarenes_SM',  '501215455',   20,   22),
		('17148','2012-01-01'::date,'Riudarenes_BR',  '501215456',   20,   22),
		('17148','2012-01-01'::date,'Riudarenes_ZE',  '501215457',   18,   19),
		('08112','2013-01-01'::date,'Manlleu_Piscina',' 28301116',   90,   95),
		('08112','2013-01-01'::date,'Manlleu_Pavello', '28301134',  100,  109),
		('25228','2013-03-01'::date,'Torrefarrera',    '28302095',   90,   98),
		('46193','2013-03-01'::date,'Picanya',            '70312',  290,  335),
		('25230','2013-09-01'::date,'Torregrossa',     '28301107',  500,  500),
		('47114','2015-08-01'::date,'Valteina',        '80429506', 1000, 1000),
		('41006','2016-05-01'::date,'Alcolea',        '501600324', 1890, 2160),
		('41055','2018-09-01'::date,'Matallana',      '502016144', 2000, 2376),
		('05074','2019-01-01'::date,'Fontivsolar',    '501815908',  800,  990),
		('41055','2019-10-01'::date,'Florida',         '44711885', 1400, 1658),
		('04090','2020-10-01'::date,'Tahal',           '88300909',  720,  841),
		('18152','2021-08-22'::date,'Llanillos',      '502016257', 3200, 3800) --- TODO: Unconfirmed date, the month is right which is enough
	) as plant(city_code, first_date, plant_name, meter_name, nominal_power_kw, peak_power_kw)
	left join giscedata_registrador as registry
	on registry.name = plant.meter_name
	left join res_municipi as city
	on city.ine = plant.city_code
) AS item
LEFT JOIN res_municipi AS municipi
	ON item.city_id=municipi.id
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
;

--select * from giscedata_registrador;

