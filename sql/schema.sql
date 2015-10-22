drop table if exists TenderRegionMap;
drop table if exists TenderGSINMap;
drop table if exists Regions;
drop table if exists GSINs;
drop table if exists Tenders;

create table Tenders (
  tender varchar(32) primary key,
  title_en varchar(256) not null,
  title_fr varchar(256) not null
) engine=InnoDB default charset=utf8;

create table GSINs (
  gsin varchar(32) primary key
) engine=InnoDB default charset=utf8;

create table Regions (
  region varchar(8) primary key
) engine=InnoDB default charset=utf8;

create table TenderGSINMap (
  tender varchar(32) not null,
  gsin varchar(32) not null,
  primary key(tender, gsin),
  foreign key(tender) references Tenders(tender),
  foreign key(gsin) references GSINs(gsin)
) engine=InnoDB default charset=utf8;

create table TenderRegionMap (
  tender varchar(32) not null,
  region varchar(8) not null,
  rel enum('delivery', 'opportunity') not null,
  primary key(tender, region, rel),
  foreign key(tender) references Tenders(tender),
  foreign key(region) references Regions(region)
) engine=InnoDB default charset=utf8;

