# select Y.ShortName,Y.ConferenceSeriesID, Count(X.OriginalPaperTitle) as PaperAmt from Papers as X, ConferenceSeries as Y where Y.ConferenceSeriesID =  X.ConferenceSeriesIDMappedToVenueName Group By X.ConferenceSeriesIDMappedToVenueName Order by PaperAmt DESC Limit 100;
# select * from PaperAbstract
#select PaperID, OriginalPaperTitle from Papers where ConferenceSeriesIDMappedToVenueName = '42D493FC'
select PaperAbstract.Abstract 
	from IdId 
    join PaperAbstract
    on IdId.PaperID = PaperAbstract.PaperID
	where IdId.MagPaperID = '7692F8D9'
