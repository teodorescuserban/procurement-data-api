drop table if exists TenderRegionMap;
drop table if exists TenderGSINMap;
drop table if exists Regions;
drop table if exists GSINs;
drop table if exists TenderSearch;
drop table if exists Tenders;

create table Tenders (
  tender varchar(32) primary key,
  title_en text not null,
  title_fr text not null
) engine=InnoDB default charset=utf8;

create table TenderSearch (
  tender varchar(32) not null,
  lemma text not null,
  lang enum('en', 'fr') not null,
  index(tender),
  fulltext(lemma)
) engine=MyISAM default charset=utf8;

create table TenderGSINMap (
  tender varchar(32) not null,
  gsin varchar(32) not null,
  primary key(tender, gsin),
  foreign key(tender) references Tenders(tender) on delete cascade,
  index(gsin)
) engine=InnoDB default charset=utf8;

create table TenderRegionMap (
  tender varchar(32) not null,
  region varchar(8) not null,
  rel enum('delivery', 'opportunity') not null,
  primary key(tender, region, rel),
  foreign key(tender) references Tenders(tender) on delete cascade,
  index(region)
) engine=InnoDB default charset=utf8;

drop view if exists TenderView;
create view TenderView as
select T.*, G.gsin, R1.region as region_delivery, R2.region as region_opportunity
from Tenders T
left join TenderGSINMap G on T.tender=G.tender
left join TenderRegionMap R1 on T.tender=R1.tender and R1.rel='delivery'
left join TenderRegionMap R2 on T.tender=R2.tender and R2.rel='opportunity';
