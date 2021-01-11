Use EngagmentBot2;

#This should create all the tables for AWS the same as they are in my local
CREATE TABLE User (current TINYINT, user_id BIGINT, username NVARCHAR(255), creation_date DATETIME, Updated_date DATETIME, since_id BIGINT);
CREATE TABLE User_Settings (user_id BIGINT, likes TINYINT, reply TINYINT, retweet TINYINT, verified TINYINT, reply_string VARCHAR(255), updated_date DATETIME);
CREATE TABLE Run_Logs (since_id_start BIGINT, since_id_end BIGINT, session_id INT, session_time_start DATETIME, session_time_end DATETIME);
CREATE TABLE User_History(user_id BIGINT, event_time DATETIME, event_string TEXT, event_type_id TINYINT);
CREATE TABLE Error_Logs(user_id BIGINT, event_type_id TINYINT, event_time DATETIME, message BLOB);