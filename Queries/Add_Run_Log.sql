USE engagementbot;

set @since_start:= 1346966033073012740,
	@since_end:=1346966033073012740,
    @sesh_id:=1,
    @start_time:=now(),
    @end_time:=now();


INSERT INTO run_logs (since_id_start, since_id_end, session_id, session_time_start, session_time_end)
	values(@since_start, @since_end, @sesh_id, @start_time, @end_time);

#This whole thing is just bootstrapping the db. 


select * from run_logs;