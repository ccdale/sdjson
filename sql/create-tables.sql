drop table if exists schedulemd5;
create table schedulemd5 (
    md5 text,
    stationid text,
    datestr text,
    datets int,
    modified int,
    primary key(md5, stationid)
);

drop table if exists schedule;
create table schedule (
    programid text,
    md5 text,
    stationid text,
    airdate int,
    duration int,
    primary key(programid, stationid, airdate)
);

drop table if exists channel;
create table channel (
    stationid text,
    name text,
    callsign text,
    broadcastlang text,
    descriptionlang text,
    logoid int,
    source text,
    channelnumber int,
    primary key(name, stationid)
);

drop table if exists program;
create table program (
    programid text,
    md5 text,
    title text,
    episodetitle text,
    shortdesc text,
    longdesc text,
    originalairdate text,
    series int,
    episode int,
    primary key(programid, md5)
);

drop table if exists person;
create table person (
    personid int,
    nameid int,
    name text,
    primary key(name, personid)
);

drop table if exists personmap;
create table personmap (
    personid int,
    programid text,
    billingorder int,
    role text,
    primary key(personid, programid)
);

