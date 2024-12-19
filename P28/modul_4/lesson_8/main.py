#
# CREATE VIEW category_name_film_c AS
# select c.name, count(fc.film_id) as film_count from category c
# inner join film_category fc on c.category_id = fc.category_id group by c.name order by film_count desc;
#
# create function add_numbers(a int , b int) returns integer
#     as
#     $$
#         begin
#             return a + b;
#         end;
#     $$
# language plpgsql;
#
# select add_numbers(5,7);
#
#
# create function fullname(first_name varchar(255),last_name varchar(255))
#     returns varchar as
#     $$
#         begin
#             return first_name || ' ' || last_name;
#         end;
#     $$
# language plpgsql;
# -- drop function fullname;
#
# select fullname('Aziz','Panjiyev');
#
# create function limit_par(limit_count int)
# returns table(title varchar) as
#     $$
#         begin
#             return query
#             select f.title
#             from film f
#             limit limit_count;
#         end;
#     $$
# language plpgsql;
#
# -- drop function limit_par;
#
# select limit_par(3);
