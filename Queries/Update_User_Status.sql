USE engagementbot;

set @user_id = 718475920194068480,
	@curr = 1,
    @updated = now();

select * from user
where user_id = @user_id;


update user 
set current = @curr, Updated_date = @updated
where user_id = @user_id;

select * from user
where user_id = @user_id;


