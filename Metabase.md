# Отчет работы с Metabase

## 1. Подключение базы данных

<img width="905" height="358" alt="Снимок экрана 2026-05-12 в 23 26 19" src="https://github.com/user-attachments/assets/341b847c-d436-491d-a945-763b4c2c96f9" />
<img width="1512" height="372" alt="Снимок экрана 2026-05-12 в 23 29 45" src="https://github.com/user-attachments/assets/96092608-58ef-4f33-be81-8f8537f4ed71" />

## 2. Дашборд

<table>
  <tr>
    <td>
      <img width="527" height="625" alt="Снимок экрана 2026-05-13 в 11 36 39" src="https://github.com/user-attachments/assets/c05185fa-b3c6-4473-a64d-b8dde0f1de0f" />
    </td>
    <td>
      <img width="527" height="756" alt="Снимок экрана 2026-05-13 в 11 36 51" src="https://github.com/user-attachments/assets/600bc4ab-3bed-4f82-9b38-145dac25b52e" />
    </td>
  </tr>
</table>

## 3. SQL запросы
  ### 1. Анализ кэшбека по категориям
  ```sql
  SELECT 
    `Категория`, 
    SUM(`Кэшбэк`) AS total_cashback 
  FROM Operations
  WHERE `Кэшбэк` > 0
    [[AND {{category_filter}}]]
    [[AND {{date_range}}]]
  GROUP BY 
  `Категория`
  ORDER BY 
  total_cashback DESC;
  ```
  <img width="1512" height="370" alt="Снимок экрана 2026-05-13 в 12 42 44" src="https://github.com/user-attachments/assets/24824f75-934d-4071-a08c-58fce3892ee2" />

  ### 2. Распределение суммарных трат по категориям
  ```sql
  SELECT
    `Категория`,
    SUM(ABS(`Сумма Операции`)) AS total_spent
  FROM Operations
  WHERE `Сумма Операции` < 0 
    [[AND {{category_filter}}]] 
    [[AND {{date_range}}]]
  GROUP BY
    `Категория`
  ORDER BY
    total_spent DESC;
  ```
  <img width="1512" height="370" alt="Снимок экрана 2026-05-13 в 12 53 35" src="https://github.com/user-attachments/assets/b3a23130-1a21-4b77-aaed-51dba6524247" />

  ### 3.Распределение суммарных трат по категориям и месяцам
  ```sql
  SELECT 
      DATE_FORMAT(`Дата Операции`, '%M %Y') AS operation_month,
      `Категория`,
      SUM(ABS(`Сумма Операции`)) AS total_spent
  FROM Operations
  WHERE `Сумма Операции` < 0
    [[AND {{category_filter}}]]
    [[AND {{date_range}}]]
  GROUP BY 
      DATE_FORMAT(`Дата Операции`, '%Y-%m'), 
      operation_month, 
      `Категория`
  ORDER BY 
      DATE_FORMAT(`Дата Операции`, '%Y-%m') ASC, 
      total_spent DESC;
  ```
  <img width="1512" height="370" alt="Снимок экрана 2026-05-13 в 12 59 37" src="https://github.com/user-attachments/assets/3b710e9c-55ec-495f-b757-3317a38e3407" />

  ### 4.Индикатор среднемесячных трат
  ```sql
  SELECT
    AVG(monthly_spent) AS average_monthly_spending
  FROM
    (
      SELECT
        DATE_FORMAT(`Дата Операции`, '%Y-%m') AS operation_month,
        SUM(ABS(`Сумма Операции`)) AS monthly_spent
      FROM Operations
      WHERE `Сумма Операции` < 0
        [[AND {{category_filter}}]] 
        [[AND {{date_range}}]]
      GROUP BY
        operation_month
    ) AS monthly_totals;
  ```
  <img width="1512" height="383" alt="Снимок экрана 2026-05-13 в 13 01 28" src="https://github.com/user-attachments/assets/8b90f3af-6f76-4144-bedc-9cbb7e014daf" />

  ### 5.Суммарный приход/расход по месяцам
  ```sql
  SELECT
    DATE_FORMAT(`Дата Операции`, '%Y-%m') AS operation_month,
    CASE
      WHEN `Сумма Операции` > 0 THEN 'Пополнение'
      ELSE 'Списание'
    END AS operation_type,
    SUM(`Сумма Операции`) AS total_amount
  FROM Operations
  WHERE 1=1
    [[AND {{category_filter}}]] 
    [[AND {{date_range}}]]
  GROUP BY
    operation_month,
    operation_type
  ORDER BY
    operation_month;
  ```
  <img width="1512" height="383" alt="Снимок экрана 2026-05-13 в 13 05 23" src="https://github.com/user-attachments/assets/7816735d-eece-4069-8514-3928d2f252ed" />

  ### 6.Динамика движения средств
  ```sql
  WITH
    daily_totals AS (
      SELECT
        DATE(`Дата Операции`) AS operation_day,
        SUM(`Сумма Операции`) AS daily_sum
      FROM Operations
      WHERE 1 = 1 
        [[AND {{category_filter}}]] 
        [[AND {{date_range}}]]
      GROUP BY
        operation_day
    )
  SELECT
    operation_day,
    SUM(daily_sum) OVER (ORDER BY operation_day) AS cumulative_balance
  FROM daily_totals
  ORDER BY
    operation_day;
  ```
  <img width="1512" height="383" alt="Снимок экрана 2026-05-13 в 13 09 28" src="https://github.com/user-attachments/assets/209ce6cc-db65-428b-b2d2-bb6adc6fc9f5" />

## 4. Кросс-фильтрация и фильтрация
  ### 1. Кросс-фильтрация
  #### 1. Общий вид
  
  <img width="703" height="552" alt="Снимок экрана 2026-05-13 в 13 14 15" src="https://github.com/user-attachments/assets/bff48036-8b8f-41c2-af37-ce026ba630cb" />
  <img width="702" height="519" alt="Снимок экрана 2026-05-13 в 13 14 23" src="https://github.com/user-attachments/assets/012f82da-f3ae-4b81-b7c6-75e38537793e" />
  
  #### 2. Кросс-фильтры
  
  <img width="257" height="254" alt="Снимок экрана 2026-05-13 в 13 14 41" src="https://github.com/user-attachments/assets/69730aa0-9655-44e1-b6a2-9460ca4f2ff8" />
  <img width="257" height="254" alt="Снимок экрана 2026-05-13 в 13 15 24" src="https://github.com/user-attachments/assets/4b4b4a9e-818e-4613-8a73-a1aa9071faf0" />
  <img width="257" height="254" alt="Снимок экрана 2026-05-13 в 13 15 28" src="https://github.com/user-attachments/assets/025a096a-5b16-4db5-a00e-5d082e6e2ffe" />

  ### 2. Фильтрация

  <img width="1512" height="542" alt="Снимок экрана 2026-05-13 в 20 30 51" src="https://github.com/user-attachments/assets/dd20a56e-0e0b-4546-b157-00a373feb91d" />
  <img width="1512" height="542" alt="Снимок экрана 2026-05-13 в 20 30 59" src="https://github.com/user-attachments/assets/18c95d7f-b2d6-4a60-bdec-f4c35bb84d5a" />
  <img width="296" height="439" alt="Снимок экрана 2026-05-13 в 20 31 49" src="https://github.com/user-attachments/assets/e6475919-d287-4ad3-9ee0-cf36489a56e1" />
  <img width="584" height="451" alt="Снимок экрана 2026-05-13 в 20 32 14" src="https://github.com/user-attachments/assets/c0bfea2b-1ddb-42f0-b900-7fdd82ccd1e5" />

  











