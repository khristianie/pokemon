/* Create the database */
CREATE DATABASE IF NOT EXISTS pokemon
  DEFAULT CHARACTER SET utf8
  DEFAULT COLLATE utf8_general_ci;

/* Switch to the pokemon database */
USE pokemon;

/* Drop existing tables */
DROP TABLE IF EXISTS pokemon_abilities;
DROP TABLE IF EXISTS pokemons;
DROP TABLE IF EXISTS abilities;

/* Create the tables */
CREATE TABLE abilities (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  api_id INT UNSIGNED NULL,
  name VARCHAR(100) NOT NULL,
  url VARCHAR(2048) NULL,

  PRIMARY KEY (id),
  UNIQUE KEY uk_api_id (api_id)
) ENGINE=InnoDB;

CREATE TABLE pokemons (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  api_id INT UNSIGNED NULL,
  name VARCHAR(255) NOT NULL,
  position INT NULL,
  url VARCHAR(2048) NULL,

  PRIMARY KEY (id),
  UNIQUE KEY uk_api_id (api_id)
) ENGINE=InnoDB;

CREATE TABLE pokemon_abilities (
  pokemon_id INT UNSIGNED NOT NULL,
  ability_id INT UNSIGNED NOT NULL,

  PRIMARY KEY (pokemon_id, ability_id),
  INDEX idx_ability_id (ability_id),

  FOREIGN KEY (pokemon_id) REFERENCES pokemons(id) ON DELETE CASCADE,
  FOREIGN KEY (ability_id) REFERENCES abilities(id) ON DELETE CASCADE
) ENGINE=InnoDB;
