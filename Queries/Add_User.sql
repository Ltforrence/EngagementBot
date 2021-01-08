USE engagementbot;

set @current:= 1,
	@user_id:=1346966033073012740,
    @username:=1,
    @creation_date:=now(),
    @Updated_date:=now(),
    @since_id = 1346946600510386176;


INSERT INTO user (current, user_id, username, creation_date, Updated_date, since_id)
	values(@current, @user_id, @username, @creation_date, @Updated_date, @since_id);

#This whole thing is just bootstrapping the db. 


select * from user;