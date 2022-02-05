drop table if exists questions;

create table questions (
    id integer primary key, 
    question text,
    is_last integer
);

insert into questions values
    (0, 'You are taking part in a guided tour of a museum. You:', 0),
    (1, 'During dinner parties at your home, you have a hard time with people who:', 0),
    (2, 'You crack a joke at work, but nobody seems to have noticed. You:', 0),
    (3, 'This morning, your agenda seems to be free. You:', 1);


drop table if exists answers;

create table answers (
    id integer primary key, 
    question_id integer, 
    answer text, 
    score integer
);

insert into answers values
    (0, 0, "Are a bit too far towards the back so don't really hear what the guide is saying", 0),
    (1, 0, 'Follow the group without question', 1),
    (2, 0, 'Make sure that everyone is able to hear properly', 2),
    (3, 0, 'Are right up the front, adding your own comments in a loud voice', 3),
    (4, 1, 'Ask you to tell a story in front of everyone else', 0),
    (5, 1, 'Talk privately between themselves', 1),
    (6, 1, 'Hang around you all evening', 2),
    (7, 1, 'Always drag the conversation back to themselves', 3),
    (8, 2, 'Think it’s for the best — it was a lame joke anyway', 0),
    (9, 2, 'Wait to share it with your friends after work', 1),
    (10, 2, 'Try again a bit later with one of your colleagues', 2),
    (11, 2, 'Keep telling it until they pay attention', 3),
    (12, 3, 'Know that somebody will find a reason to come and bother you', 0),
    (13, 3, 'Heave a sigh of relief and look forward to a day without stress', 1),
    (14, 3, 'Question your colleagues about a project that’s been worrying you', 2),
    (15, 3, 'Pick up the phone and start filling up your agenda with meetings', 3);