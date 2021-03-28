create table schedulemd5 (
    md5 text,
    stationid text,
    datestr text,
    datets int,
    modified int,
    primary key(md5, stationid)
);

create table schedule (
    programid text,
    md5 text,
    stationid text,
    airdate int,
    duration int,
    primary key(programid, stationid)
);

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

create table program (
    programid text,
    md5 text,
    title text,
    shortdesc text,
    longdesc text,
    originalairdate text,
    primary key(programid, md5)
);

create table person (
    personid int,
    nameid int,
    name text,
    primary key(name, personid)
);

create table personmap (
    personid int,
    programid text,
    billingorder int,
    role text,
    primary key(personid, programid)
);

