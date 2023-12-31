-- lists all bands with Glam rock as their main style ranked by their longevity
-- script can be executed on any database
SELECT band_name, (IFNULL(split, 2023) - formed) AS lifespan
	FROM metal_bands
	WHERE style LIKE '%Glam rock%'
	ORDER BY lifespan DESC
