📥 Load Data into Internal Stage

Upload file to internal stage via UI or script

🔎 Preview Raw Data

SELECT $1, $2
FROM @SMOOTHIES.PUBLIC.MY_UPLOAD_FILES/fruits_available_for_smoothies.txt
(FILE_FORMAT => SMOOTHIES.PUBLIC.two_headerrow_pct_delim);

📤 Copy File Into Table

COPY INTO smoothies.public.fruit_options
FROM (
  SELECT $2 AS FRUIT_ID, $1 AS FRUIT_NAME
  FROM @SMOOTHIES.PUBLIC.MY_UPLOAD_FILES/fruits_available_for_smoothies.txt
)
FILE_FORMAT = (FORMAT_NAME = smoothies.public.two_headerrow_pct_delim)
ON_ERROR = ABORT_STATEMENT
PURGE = TRUE;

