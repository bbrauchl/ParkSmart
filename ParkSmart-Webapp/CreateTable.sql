USE parksmartdb;
DROP TABLE IF EXISTS Lot_D;
DROP TRIGGER IF EXISTS set_end_timestamp_on_insert;
DROP TRIGGER IF EXISTS set_end_timestamp_on_update;
DROP TRIGGER IF EXISTS edit_end_timestamp_on_insert;
DROP TRIGGER IF EXISTS edit_end_timestamp_on_update;
DROP PROCEDURE IF EXISTS setup_table;

CREATE TABLE Lot_D (
    Space INTEGER, 
    IsOccupied BOOLEAN, 
    Confidence FLOAT, 
    Type ENUM ('student','faculty','visitor','handicap','electric_vehicle'), 
    Extra TEXT, 
    start_timestamp TIMESTAMP(6) DEFAULT NOW() ON UPDATE NOW(), 
    end_timestamp TIMESTAMP(6) NULL
    );

DELIMITER $$

CREATE PROCEDURE setup_table() 
BEGIN
    DECLARE i INT DEFAULT 0;
    WHILE i < 84 DO
        INSERT INTO Lot_D (Space) VALUES (i);
        SET i = i + 1;
    END WHILE;
END;$$

CALL setup_table();$$

CREATE TRIGGER set_end_timestamp_on_insert BEFORE INSERT ON Lot_D 
FOR EACH ROW BEGIN 
    SET NEW.end_timestamp = NOW() + INTERVAL 2 MINUTE; 
END;$$

CREATE TRIGGER set_end_timestamp_on_update BEFORE UPDATE ON Lot_D 
FOR EACH ROW BEGIN 
    IF (NEW.end_timestamp = NULL OR NEW.end_timestamp = TIMESTAMP(0)) THEN
        SET NEW.end_timestamp = NOW() + INTERVAL 2 MINUTE; 
    END IF;
END;$$

DELIMITER ;