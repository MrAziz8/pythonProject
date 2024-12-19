
-- 1-savol
create table movies(
    id serial primary key ,
    title varchar(255),
    genre varchar(255),
    release_year integer
);
--  ============================================================
-- 2-savol
create table actors(
    id serial primary key ,
    name varchar(255)
);

CREATE TABLE movie_actors (
    movie_id integer references movies(id),
    actor_id integer references actors(id),
    primary key  (movie_id, actor_id)
);

insert into actors(name)
select concat('Actor', floor(random()*10000)+1)
from(select 1 from information_schema.tables limit 10000) as temp;

select
    avg(movie_count) as average_movies_per_actor
from (
    select
        actor_id,
        COUNT(movie_id) AS movie_count
    from
        movie_actors
    group by
        actor_id
) ma;


select * from movie_actors limit 10;

-- =====================================================
-- 3 savol


select genre, count(*) as total_movies
from movies
group by genre;


-- ===========================================================