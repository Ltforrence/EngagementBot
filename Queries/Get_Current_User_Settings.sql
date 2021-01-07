USE engagementbot;

SELECT us.user_id, us.reply_string, us.retweet, us.likes, us.reply, us.verified from user u
join user_settings us on u.user_id = us.user_id
where u.current = 1;