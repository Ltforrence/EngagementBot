USE engagementbot;

set @user_id:=1346966033073012740,
    @likes:=1,
    @reply:=0,
    @retweet:=0,
    @verified:=1,
    @reply_string = "",
    @updated_date = now();


INSERT INTO user_settings (user_id, likes, reply, retweet, verified, reply_string, updated_date)
	values(@user_id, @likes, @reply, @retweet, @verified, @reply_string, @updated_date);

#This whole thing is just bootstrapping the db. 


select * from user_settings;