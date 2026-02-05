import pandas as pd

from src.core.interfaces.data_aggregation_interface import IDataAggregationRepository
from src.core.interfaces.spark_interface import ISparkRepository


class DataAggregationRepository(IDataAggregationRepository):
    def __init__(self, spark_repository: ISparkRepository):
        self.spark_repository = spark_repository

    def get_all_table_data(self, table_name: str) -> pd.DataFrame:
        spark_df = self.spark_repository.read_table(table_name)
        return self.spark_repository.to_pandas(spark_df)

    def get_sakila_united_data(self) -> pd.DataFrame:
        return self._read_and_united_sakila_data_spark()

    def _read_and_united_sakila_data_spark(self) -> pd.DataFrame:
        query = """
        SELECT 
            f.film_id, f.title, f.description, f.release_year, f.language_id, f.rental_duration,
            f.rental_rate, f.length, f.replacement_cost, f.rating,
            act.actor_id, act.first_name actor_fn, act.last_name actor_ln,

            c.customer_id, c.first_name cust_fn, c.last_name cust_ln, c.email, c.active,
            r.rental_id, r.rental_date, r.return_date,
            p.payment_id, p.amount, p.payment_date,


            i.inventory_id,
            s.store_id, s.manager_staff_id,
            stf.staff_id, stf.first_name staff_fn, stf.last_name staff_ln,


            addr.address_id, addr.address, addr.address2, addr.district, addr.postal_code,
            ct.city_id, ct.city,
            co.country_id, co.country,

            cat.category_id, cat.name category,
            l.name language,
        
            fc.film_id film_category_id,
            fa.actor_id film_actor_id  
        FROM film f
        JOIN film_actor fa ON f.film_id = fa.film_id
        JOIN actor act ON fa.actor_id = act.actor_id
        JOIN inventory i ON f.film_id = i.film_id
        JOIN rental r ON i.inventory_id = r.inventory_id
        JOIN customer c ON r.customer_id = c.customer_id
        JOIN payment p ON r.rental_id = p.rental_id
        JOIN store s ON c.store_id = s.store_id
        JOIN staff stf ON s.manager_staff_id = stf.staff_id
        JOIN address addr ON c.address_id = addr.address_id
        JOIN city ct ON addr.city_id = ct.city_id
        JOIN country co ON ct.country_id = co.country_id
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category cat ON fc.category_id = cat.category_id
        JOIN language l ON f.language_id = l.language_id
        """
        spark_df = self.spark_repository.read_sql(query)
        return self.spark_repository.to_pandas(spark_df)