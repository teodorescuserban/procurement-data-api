drop table if exists TenderRegionMap;
drop table if exists TenderGSINMap;
drop table if exists Regions;
drop table if exists GSINs;
drop table if exists Tenders;

create table Tenders (
  tender varchar(32) primary key,
  title_en text not null,
  title_fr text not null
) engine=InnoDB default charset=utf8;

create table TenderGSINMap (
  tender varchar(32) not null,
  gsin varchar(32) not null,
  primary key(tender, gsin),
  foreign key(tender) references Tenders(tender) on delete cascade
) engine=InnoDB default charset=utf8;

create table TenderRegionMap (
  tender varchar(32) not null,
  region varchar(8) not null,
  rel enum('delivery', 'opportunity') not null,
  primary key(tender, region, rel),
  foreign key(tender) references Tenders(tender) on delete cascade
) engine=InnoDB default charset=utf8;

create view TenderView as
select T.*, G.gsin, R.region, R.rel from Tenders T
join TenderGSINMap G using(tender)
join TenderRegionMap R using(tender);
