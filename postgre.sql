create table if not exists public."token" (
    id bigserial not null,
    value varchar(300) not null,
    constraint token_pk primary key (id),
    constraint token_value_unique unique (value)
);

create table if not exists public."user" (
    id bigserial not null,
    name varchar(50) not null,
    password varchar(300) not null,
    email varchar(250) not null,
    is_admin boolean not null,
    is_active boolean not null default false,
    last_login date,
    date_joined date not null,
    token_id int not null,
    constraint user_pk primary key (id),
    constraint user_email_unique unique (email),
    constraint user_token_fk foreign key (token_id) references public.token(id) on delete cascade
);

create table if not exists public."project" (
    id bigserial not null,
    title varchar(200) not null,
    description text not null,
    budget float,
    started date,
    is_completed boolean not null default false,
    admin_id int not null,
    token_id int not null,
    constraint project_pk primary key (id),
    constraint project_admin_fk foreign key (admin_id) references public.user(id) on delete cascade,
    constraint project_token_fk foreign key (token_id) references public.token(id) on delete cascade
);

create table if not exists public."author" (
    id bigserial not null,
    name varchar(50) not null,
    email varchar(250) not null,
    birth date not null,
    gender varchar(1) not null,
    project_id int not null,
    token_id int not null,
    constraint author_pk primary key (id),
    constraint author_project_fk foreign key (project_id) references public.project(id) on delete cascade,
    constraint author_token_fk foreign key (token_id) references public.token(id) on delete cascade
);

create table if not exists public."link" (
    id bigserial not null,
    value varchar(300) not null,
    write boolean not null,
    project_id int not null,
    token_id int not null,
    constraint link_pk primary key (id),
    constraint link_value_unique unique (value),
    constraint link_project_fk foreign key (project_id) references public.project(id) on delete cascade,
    constraint link_token_fk foreign key (token_id) references public.token(id) on delete cascade
);