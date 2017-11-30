# f17-message-log-th-m

This application allows people to create instances of the game Avalon and it also assigns character information to specific players.

## Attributes
#### Attributes for Players

* id
* game_id
* game_title
* character_title
* character_data    
* player_number
* player_name   
* is_active
    
#### Attributes for sessions

* id
* user_id
    
#### Attributes for games

* id
* title
* is_active

#### Attributes for users

* id
* email
* password
* first_name
* last_name
* age


    
## Schema
CREATE TABLE session (id text, user_id integer);

CREATE TABLE games (id integer primary key, title varchar(20), is_active integer);

CREATE TABLE users (id integer primary key, email varchar(20), encr_pass text, first_name varchar(30), last_name varchar(30),  age integer);

CREATE TABLE players (id integer primary key, game_id integer, game_title varchar(20), character_title varchar(20), character_data text, player_number integer, player_name varchar(20));

## Rest End Points

### GET
```
/sessions
```
get session associated with user

```
/players
```
Retrieve list of players.
```
/games
```
Retrieve list of games.
```
/players/{id}
```
Retrieve player details.
```
/games/{game_id}/players
```
Retrieve list of players in particular game.
### DELETE
```
/players/{id}
```
Delete a player.
### PUT
```
/games/{game_id}/players
```
Update players in game.
### POST
```
/players
```
Create a player.
```
/games
```
Create a game.
```
/users
```
Create a User.
```
/sessions
```
Create a Session

## Hashing
I am using python bcrypt module I encrypt passwords with a secret salt, that only I know.
Doing encryption like this provides a uniform method by which I can decode the passwords 
and check that they match the hash. I am only ever storing the hashed version of passwords.

