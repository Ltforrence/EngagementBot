USE engagementbot;


set @user_id = 718475920194068480,
	@event_time = now(),
    @event_string = 'This is a test! But this means user followed',
    @event_type_id = 1;

INSERT INTO user_history (user_id, event_time, event_string, event_type_id)
values(@user_id, @event_time, @event_string, @event_type_id);


SELECT * FROM user_history;