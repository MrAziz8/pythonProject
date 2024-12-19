
--  4-savol

create or replace function filter_movies_by_year(from_year int , to_year int)
returns table(id int,title varchar, genre varchar, release_year int) as $$
    begin
        return query
        select m.id, m.title,m.genre,m.release_year
        from movies m
        where m.release_year between from_year and to_year;
    end;
    $$ language plpgsql;

-- drop function filter_movies_by_year(from_year int, to_year int);

select * from filter_movies_by_year(2000, 2010);


-- 5 savol

create or replace  function update_movie()
returns trigger as $$
    begin
        update movies
        set film_count = (select count(*) from movie_actors where movie_id = new.id)
        where id in (select movie_id  from movie_actors where actor_id = new.id);
        return new;
    end;
    $$ language plpgsql;

create trigger actor_insert_tr
after insert on actors
for each row
execute function update_movie();

