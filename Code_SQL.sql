--url : https://danso.org/
USE DANSO
GO
-- Xem dữ liệu
SELECT * FROM Data_DanSo
SELECT * FROM Data_Region
SELECT * FROM Data_table

-- Merge Dữ liệu Dân số vào region
SELECT DD.*,DR.Region
FROM Data_DanSo as DD
LEFT JOIN Data_Region as DR
ON DD.Country = DR.Country

-- Tạo view để xem truy vấn
CREATE VIEW Visualization_Table as
WITH Visualization_Table ( Country, Each_Year ,Region, Population_per_year,Migrate,percent_city,percent_world,Area,Population_2023 ,Average_age)
as
(
	SELECT DT.Country,DT.[Year] as Each_Year,Table_Region.Region,DT.[Population] as Population_per_year,round(DT.Migrate,2) as Migrate,
		CONCAT(round(DT.percent_city,2),'%') as Percent_city,DT.percent_world,
		round(Table_Region.Area,2) as Area,
		Table_Region.[Population] as Population_2023,
		round(Table_Region.Average_age,2) as Average_age
	FROM Data_table as DT
	LEFT JOIN
	(
		SELECT DD.*,DR.Region
		FROM Data_DanSo as DD
		LEFT JOIN Data_Region as DR
		ON DD.Country = DR.Country
	) as Table_Region
	ON DT.Country = Table_Region.Country
)
SELECT * FROM Visualization_Table

-- Đưa truy vấn vào bảng để visualization
SELECT DT.Country,DT.[Year] as Each_Year,Table_Region.Region,DT.[Population] as Population_per_year,round(DT.Migrate,2) as Migrate,
	CONCAT(round(DT.percent_city,2),'%') as Percent_city,DT.percent_world,
	round(Table_Region.Area,2) as Area,
	Table_Region.[Population] as Population_2023,
	round(Table_Region.Average_age,2) as Average_age
INTO Table_Visualization
FROM Data_table as DT
LEFT JOIN
(
	SELECT DD.*,DR.Region
	FROM Data_DanSo as DD
	LEFT JOIN Data_Region as DR
	ON DD.Country = DR.Country
) as Table_Region
ON DT.Country = Table_Region.Country

-- GROUP Lại data để tổng hợp thành 1 bảng tóm tắt
SELECT Country,MAX(Population_per_year) as Population_2020, max(Average_age) as Average_age, 
	max(Area) as Area , max(Population_2023) as Population_2023
FROM Table_Visualization
GROUP BY Country

SELECT Country, sum(Migrate) as Migrate
FROM Table_Visualization
GROUP BY Country

-- Tạo view cho bảng tóm tắt
CREATE VIEW Group_table_Visualization as
WITH Group_table_Visualization ( Country, Population_2020, Average_age, Area, Population_2023, Migrate)
as
(
	SELECT group_table_1.*,group_table_2.Migrate
	FROM
	(
		SELECT Country,MAX(Population_per_year) as Population_2020,max(Average_age) as Average_age, 
			max(Area) as Area , max(Population_2023) as Population_2023
		FROM Table_Visualization
		GROUP BY Country
	) as group_table_1
	LEFT JOIN
	(
		SELECT Country, sum(Migrate) as Migrate
		FROM Table_Visualization
		GROUP BY Country
	) as group_table_2
	ON group_table_1.Country = group_table_2.Country
)
SELECT * FROM Group_table_Visualization

SELECT group_table_1.*,group_table_2.Migrate,CONCAT(Round(Population_2023/Population_2020,2),'%') as Rate_increase
INTO Table_Visualization_2
FROM
(
	SELECT Country,MAX(Population_per_year) as Population_2020,max(Average_age) as Average_age, max(Area) as Area , max(Population_2023) as Population_2023
	FROM Table_Visualization
	GROUP BY Country
) as group_table_1
LEFT JOIN
(
	SELECT Country, sum(Migrate) as Migrate
	FROM Table_Visualization
	GROUP BY Country
) as group_table_2
ON group_table_1.Country = group_table_2.Country

SELECT * FROM Table_Visualization
SELECT * FROM Table_Visualization_2