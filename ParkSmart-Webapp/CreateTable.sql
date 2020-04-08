USE parksmartdb;
DROP TABLE IF EXISTS Lot_D;
DROP TABLE IF EXISTS Lot_D_hist;
DROP TRIGGER IF EXISTS set_end_timestamp_on_insert;
DROP TRIGGER IF EXISTS set_end_timestamp_on_update;
DROP TRIGGER IF EXISTS set_end_timestamp_on_insert_hist;

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

CREATE TABLE Lot_D_hist (
    Space INTEGER, 
    IsOccupied BOOLEAN, 
    Confidence FLOAT, 
    Type ENUM ('student','faculty','visitor','handicap','electric_vehicle'), 
    Extra TEXT, 
    start_timestamp TIMESTAMP(6) NULL, 
    end_timestamp TIMESTAMP(6) DEFAULT NOW()
    );

DELIMITER $$

CREATE TRIGGER set_end_timestamp_on_insert BEFORE INSERT ON Lot_D
FOR EACH ROW BEGIN
    SET NEW.end_timestamp = (NOW() + INTERVAL 2 MINUTE);
END;$$

CREATE TRIGGER set_end_timestamp_on_update BEFORE UPDATE ON Lot_D
FOR EACH ROW BEGIN
    IF (NEW.start_timestamp AND NOT NEW.start_timestamp = TIMESTAMP(0)) THEN
        SET NEW.end_timestamp = (NOW() + INTERVAL 2 MINUTE);
    END IF;
END;$$

CREATE TRIGGER set_end_timestamp_on_insert_hist BEFORE INSERT ON Lot_D_hist
FOR EACH ROW BEGIN
    IF (NEW.end_timestamp AND NEW.end_timestamp > NOW()) THEN
        SET NEW.end_timestamp = NOW();
    END IF;
END;$$

DELIMITER ;