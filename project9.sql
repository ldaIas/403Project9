DROP TABLE IF EXISTS patents;
DROP TABLE IF EXISTS state_pop;
DROP TABLE IF EXISTS tax_revenue;

CREATE TABLE state_pop (
    state CHARACTER(2) PRIMARY KEY,
    population NUMERIC
);

CREATE TABLE tax_revenue (
    state CHARACTER(2) REFERENCES state_pop(state),
    year TEXT,
    monthly_revenue NUMERIC,
    PRIMARY KEY(year, state)
);

CREATE TABLE patents (
    year TEXT,
    state CHARACTER(2) REFERENCES state_pop(state),
    number_of_patents NUMERIC,
    PRIMARY KEY(year, state)
);

\COPY state_pop FROM '/Users/maxgawason/cs403/project9/state_pop_data.csv' DELIMITER ',' CSV HEADER;
\COPY tax_revenue FROM '/Users/maxgawason/cs403/project9/tax_revenue_data.csv' DELIMITER ',' CSV HEADER;
\COPY patents FROM '/Users/maxgawason/cs403/project9/patent_data.csv' DELIMITER ',' CSV HEADER;

SELECT * FROM patents;
>>>>>>> 59e75cf624828f189a2109aaab3c5e87fc27a4e1
