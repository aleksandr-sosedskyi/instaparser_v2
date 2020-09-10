dump: 
	@docker-compose exec postgres pg_dump "host=postgres port=5432 dbname=instaparser user=instaparser password=instaparser" > dump.sql
	@tar -zcvf dump.sql.tar.gz dump.sql
	@rm dump.sql